import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Konfigurasi Path sesuai dengan Arsitektur Struktur File Proyek
RAW_DATA_PATH = "data/raw"
CHROMA_PATH = "data/chroma_db"

def main():
    print("🔄 [START] Memulai Proses Data Ingestion CampusMate AI...")
    
    # 1. Validasi dan Pembuatan Folder Direktori Data Raw
    if not os.path.exists(RAW_DATA_PATH):
        os.makedirs(RAW_DATA_PATH)
        print(f"📁 Folder Baru Terdeteksi: '{RAW_DATA_PATH}' telah dibuat secara otomatis.")
        print("👉 Silakan masukkan berkas PDF Regulasi Akademik UIR ke folder tersebut, lalu jalankan ulang skrip ini.")
        return

    # 2. Memuat Seluruh Berkas PDF dari Folder data/raw
    print(f"📖 Membaca berkas PDF dari direktori: {RAW_DATA_PATH} ...")
    loader = PyPDFDirectoryLoader(RAW_DATA_PATH)
    documents = loader.load()
    
    if len(documents) == 0:
        print("❌ ERROR: Tidak ada berkas PDF yang ditemukan di dalam folder 'data/raw/'.")
        print("👉 Pastikan berkas Pedoman Akademik atau SOP format .pdf sudah disalin ke folder tersebut.")
        return
        
    print(f"📄 Berhasil mengekstraksi total: {len(documents)} halaman dokumen mentah.")

    # 3. Proses Chunking / Pemotongan Teks (RAG-Optimized)
    # Ditargetkan khusus untuk menjaga keutuhan format regulasi (Bab, Pasal, dan Poin Berangka)
    print("✂️  Melakukan pemotongan teks secara modular (Text Splitting)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,      # Diperbesar agar batas SKS, IPK, dan pasal hukum masuk utuh dalam 1 fragmen
        chunk_overlap=250,    # Overlap yang cukup menjamin keterkaitan konteks antar potongan teks
        separators=[
            "\n\n",           # Prioritas 1: Pisahkan per paragraf utuh
            "\n",             # Prioritas 2: Pisahkan per baris baru
            "1.", "2.", "3.", # Prioritas 3: Deteksi urutan poin regulasi agar tidak terbelah tengah jalan
            " ",              # Prioritas 4: Pisahkan per kata
            ""                # Jalur darurat: Karakter tunggal
        ]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"🧩 Dokumen sukses dipecah menjadi {len(chunks)} potongan teks (chunks) siap indeks.")

    # 4. Inisialisasi Model Embedding Multilingual
    # Menggunakan model sentence-transformers dari HuggingFace yang optimal untuk Bahasa Indonesia
    print("🧠 Memuat Model Embedding (sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={'device': 'cpu'} # Setel ke 'cuda' jika komputer server memiliki GPU Nvidia aktif
    )

    # 5. Pembersihan dan Penyegaran Vector Database ChromaDB
    print("💾 Memperbarui Pangkalan Data Vektor (ChromaDB Vector Store)...")
    
    # Jika folder chroma_db lama sudah ada, kita hapus fisiknya agar koordinat vektor tidak tumpang tindih (corrupted)
    if os.path.exists(CHROMA_PATH):
        print("🧹 Menghapus index database vektor lama untuk mencegah duplikasi data...")
        try:
            shutil.rmtree(CHROMA_PATH)
            # Berikan jeda waktu sejenak agar OS menyelesaikan proses penghapusan file
            import time
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Peringatan saat membersihkan folder lama: {str(e)}")

    # 6. Membangun Basis Pengetahuan Vektor Baru
    try:
        vectorstore = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings, 
            persist_directory=CHROMA_PATH
        )
        print("✨ Persistensi data vektor ke direktori penyimpanan berhasil diselesaikan.")
    except Exception as e:
        print(f"❌ ERROR Kritis saat membangun ChromaDB: {str(e)}")
        return
    
    print("✅ [SUCCESS] Knowledge Base CampusMate AI berhasil diperbarui secara akurat dan tersimpan!")

if __name__ == "__main__":
    main()