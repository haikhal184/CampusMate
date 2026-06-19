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
    print("✂️  Melakukan pemotongan teks secara modular (Text Splitting)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,      
        chunk_overlap=250,    
        separators=[
            "\n\n",           
            "\n",             
            "1.", "2.", "3.", 
            " ",              
            ""                
        ]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"🧩 Dokumen sukses dipecah menjadi {len(chunks)} potongan teks (chunks) siap indeks.")

    # [TAMBAHAN BARU]: Modifikasi Metadata untuk Frontend Vue.js
    print("🏷️  Menyuntikkan metadata 'source_type' pada setiap potongan teks...")
    for chunk in chunks:
        # PyPDFDirectoryLoader otomatis menyertakan metadata 'source' (contoh: data/raw/Pedoman.pdf).
        # Kita potong path-nya agar tersisa nama filenya saja (Pedoman.pdf) untuk keperluan URL di Frontend.
        if "source" in chunk.metadata:
            original_path = chunk.metadata["source"]
            file_name = os.path.basename(original_path)
            chunk.metadata["source"] = file_name
        
        # Tambahkan label tipe dokumen agar dikenali oleh tombol hijau di Vue.js
        chunk.metadata["source_type"] = "file"

    # 4. Inisialisasi Model Embedding Multilingual
    print("🧠 Memuat Model Embedding (sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={'device': 'cpu'} 
    )

    # 5. Pembersihan dan Penyegaran Vector Database ChromaDB
    print("💾 Memperbarui Pangkalan Data Vektor (ChromaDB Vector Store)...")
    if os.path.exists(CHROMA_PATH):
        print("🧹 Menghapus index database vektor lama untuk mencegah duplikasi data...")
        try:
            shutil.rmtree(CHROMA_PATH)
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