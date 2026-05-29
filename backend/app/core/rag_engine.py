import os
# PERBAIKAN 1: Menggunakan paket modern langchain_ollama sesuai rekomendasi sistem
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Path tempat Vector Database disimpan
CHROMA_PATH = "data/chroma_db"

# 1. Inisialisasi Model LLM menggunakan OllamaLLM (Bebas dari Warning Deprecated)
llm = OllamaLLM(model="qwen2.5:1.5b")

# 2. Inisialisasi Model Embedding Multilingual
# PERBAIKAN 2: Menambahkan opsi local_files_only agar sistem mencari di lokal terlebih dahulu jika internet mati
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'}
)

# Variabel global untuk menyimpan pipeline RAG berbasis LCEL
_lcel_rag_chain = None

def format_docs(docs):
    """Menggabungkan teks dari potongan dokumen yang ditemukan"""
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    """
    Fungsi untuk membangun RAG Chain menggunakan arsitektur LCEL murni.
    Sangat adaptif dan berjalan optimal di infrastruktur lokal.
    """
    global _lcel_rag_chain
    if _lcel_rag_chain is not None:
        return _lcel_rag_chain

    # 3. Memuat Vector Database ChromaDB
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # 4. Prompt Engineering Ketat (Anti-Hallucination)
    system_prompt = (
        "Anda adalah CampusMate AI, asisten akademik cerdas untuk mahasiswa Teknik Informatika UIR.\n"
        "Tugas Anda adalah menjawab pertanyaan berdasarkan Konteks Dokumen yang disediakan di bawah.\n"
        "Gunakan penalaran logis jika pertanyaan menggunakan sinonim kata (contoh: Tugas Akhir sama dengan Skripsi).\n"
        "KONDISI DARURAT: Jika pengguna bertanya atau melaporkan tentang 'kekerasan', 'pelecehan', 'perundungan', atau 'bullying', "
        "JANGAN gunakan konteks dokumen. Langsung berikan jawaban empati dan arahkan pengguna ke Satgas PPKS UIR dengan kalimat ini: "
        "'Jika Anda atau seseorang yang Anda kenal mengalami tindak kekerasan, perundungan, atau pelecehan, mohon segera laporkan ke Satgas PPKS UIR untuk mendapatkan perlindungan dan bantuan pendampingan. Anda tidak sendiri. Hubungi Hotline Satgas UIR atau kunjungi web resmi di: [https://satgasppks.uir.ac.id/]'.\n\n"
        "Jika informasi akademik tidak ada di dalam konteks dokumen, katakan secara jujur:\n"
        "\"Maaf, informasi tersebut tidak ditemukan dalam pedoman akademik.\"\n"
        "Dilarang keras mengarang jawaban di luar konteks. Jawablah dengan poin-poin yang rapi, jelas, dan ramah.\n\n"
        "Konteks Dokumen:\n"
        "{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])

    # 5. Membangun Pipeline Menggunakan Deklarasi LCEL (| Pipe Operator)
    _lcel_rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return _lcel_rag_chain

async def generate_answer(message: str) -> str:
    """
    Fungsi asinkron utama yang dipanggil oleh endpoint API (chat.py)
    """
    try:
        chain = get_rag_chain()
        response = chain.invoke(message)
        return response
    except Exception as e:
        return f"Mohon maaf, CampusMate sedang mengalami kendala teknis saat memproses kecerdasan buatan. Detail error: {str(e)}"