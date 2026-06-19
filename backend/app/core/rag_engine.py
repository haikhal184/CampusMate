import os
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Path tempat Vector Database disimpan
CHROMA_PATH = "data/chroma_db"

# 1. Inisialisasi Model LLM 
llm = OllamaLLM(model="qwen2.5:1.5b")

# 2. Inisialisasi Model Embedding Multilingual
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'}
)

# 3. Variabel global untuk komponen (agar tidak diload berulang kali)
_vectorstore = None
_prompt = None

def get_rag_components():
    """Memuat Vectorstore dan Prompt secara efisien (Singleton)"""
    global _vectorstore, _prompt
    
    if _vectorstore is None:
        _vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        
    if _prompt is None:
        # [PERBAIKAN]: Modifikasi System Prompt dengan Aturan Sapaan vs Dokumen
        system_prompt = (
            "Anda adalah CampusMate AI, asisten akademik cerdas untuk mahasiswa Teknik Informatika UIR.\n"
            "ATURAN KETAT YANG HARUS ANDA PATUHI:\n"
            "1. SAPAAN: Jika pesan pengguna HANYA berupa sapaan santai (contoh: 'halo', 'hai', 'selamat pagi', 'assalamualaikum', 'test', 'ping'), "
            "balaslah sapaan tersebut dengan ramah, perkenalkan diri Anda, dan tawarkan bantuan terkait pedoman akademik. "
            "JANGAN mengutip, merangkum, atau menyebutkan isi dokumen sama sekali pada tahap ini.\n\n"
            "2. SESUAI DOKUMEN: Jika pengguna bertanya tentang masalah akademik, jawab HANYA berdasarkan 'Konteks Dokumen' yang disediakan di bawah. "
            "Gunakan penalaran logis jika pertanyaan menggunakan sinonim kata (contoh: Tugas Akhir sama dengan Skripsi).\n\n"
            "3. DI LUAR DOKUMEN: Jika pertanyaan pengguna tidak ada informasinya di dalam konteks dokumen, DILARANG KERAS mengarang jawaban. "
            "Katakan secara jujur: \"Maaf, informasi tersebut tidak ditemukan dalam pedoman akademik resmi kampus.\"\n\n"
            "Jawablah dengan poin-poin yang rapi, jelas, dan ramah bila relevan.\n\n"
            "Konteks Dokumen:\n"
            "{context}"
        )
        _prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}"),
        ])
        
    return _vectorstore, _prompt

async def generate_answer(message: str) -> dict:
    """
    Fungsi asinkron utama yang dipanggil oleh endpoint API (chat.py)
    """
    try:
        # 1. [PERBAIKAN] Pencegatan Kata Kunci Darurat menggunakan kata dasar
        kata_darurat = ["keras", "leceh", "rundung", "bully", "satgas", "bunuh diri", "depresi"]
        if any(kata in message.lower() for kata in kata_darurat):
            return {
                "content": "Jika Anda atau seseorang yang Anda kenal mengalami tindak kekerasan, perundungan, atau pelecehan, mohon segera laporkan ke Satgas PPKS UIR untuk mendapatkan perlindungan dan bantuan pendampingan. Anda tidak sendiri.\n\nHubungi Hotline Satgas UIR atau kunjungi web resmi mereka.",
                "source": "https://satgasppks.uir.ac.id/",
                "source_type": "url"
            }

        # 2. Pencegatan Kata Kunci Tata Tertib ke Web Fakultas
        kata_tertib = ["tata tertib", "pakaian", "perkuliahan", "ujian", "aturan kampus"]
        if any(kata in message.lower() for kata in kata_tertib):
            return {
                "content": "Untuk informasi lengkap mengenai Tata Tertib Pakaian, Tata Tertib Perkuliahan, maupun Tata Tertib Ujian, Anda dapat melihat dan mengunduh dokumen resminya langsung melalui portal Fakultas Teknik Universitas Islam Riau.",
                "source": "https://eng.uir.ac.id/pedoman-akademik/",
                "source_type": "url"
            }

        vectorstore, prompt = get_rag_components()
        
        # A. Proses Retrieval
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        docs = retriever.invoke(message)
        
        # Gabungkan teks untuk diberikan ke LLM
        context_text = "\n\n".join(doc.page_content for doc in docs)
        
        # B. Ekstrak Metadata & CCTV Debugging
        source_name = ""
        source_type = ""
        
        print("\n" + "="*50)
        print(f"🧐 PERTANYAAN USER: {message}")
        
        if docs:
            source_name = docs[0].metadata.get("source", "")
            source_type = docs[0].metadata.get("source_type", "")
            
            print(f"✅ DOKUMEN DITEMUKAN: {source_name} (Tipe: {source_type})")
            print(f"📄 CUPLIKAN TEKS YANG AKAN DIBACA AI:\n{context_text[:200]}...")
        else:
            print("❌ GAGAL! TIDAK ADA DOKUMEN YANG RELEVAN DENGAN PERTANYAAN INI.")
            
        print("="*50 + "\n")

        # C. Proses Generation
        chain = prompt | llm | StrOutputParser()
        ai_response = chain.invoke({
            "context": context_text,
            "question": message
        })
        
        # D. Kembalikan data lengkap
        return {
            "content": ai_response,
            "source": source_name if docs else "", # Hindari misinformasi source jika sekadar sapaan
            "source_type": source_type if docs else ""
        }
        
    except Exception as e:
        return {
            "content": f"Mohon maaf, CampusMate sedang mengalami kendala teknis saat memproses kecerdasan buatan. Detail error: {str(e)}",
            "source": "",
            "source_type": ""
        }