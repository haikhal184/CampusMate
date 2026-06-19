from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # [TAMBAHAN BARU] Untuk melayani file PDF/statis
import uvicorn
import os  # [TAMBAHAN BARU] Untuk mengecek keberadaan folder

# Mengimpor router dari modul chat (app/api/chat.py) yang sudah kita buat sebelumnya
from app.api.chat import router as chat_router

# 1. Inisialisasi Aplikasi FastAPI
app = FastAPI(
    title="CampusMate AI API",
    description="Backend API untuk chatbot akademik berbasis RAG menggunakan LLM Qwen 2.5 (1.5B)",
    version="1.0.0"
)

# 2. Konfigurasi CORS (Sangat Penting untuk Integrasi dengan Vue.js)
# Frontend Vue (misal berjalan di http://localhost:5173) perlu izin 
# untuk berkomunikasi dengan Backend FastAPI (http://localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua origin untuk tahap pengembangan
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode (GET, POST, OPTIONS, dll)
    allow_headers=["*"],  # Mengizinkan semua header
)

# 3. [TAMBAHAN BARU] Mount Folder Dokumen
# Mengaktifkan folder 'data/raw' agar file di dalamnya bisa diakses via URL /dokumen/...
# Contoh: http://127.0.0.1:8000/dokumen/Buku_Pedoman_KP.pdf
if os.path.exists("data/raw"):
    app.mount("/dokumen", StaticFiles(directory="data/raw"), name="dokumen")
else:
    print("⚠️ Peringatan: Folder 'data/raw' belum ditemukan di dalam direktori backend.")

# 4. Mendaftarkan Router API
# Semua endpoint di dalam chat.py akan dapat diakses dengan awalan '/api/chat'
app.include_router(chat_router, prefix="/api/chat", tags=["Chatbot AI"])

# 5. Endpoint Root (Health Check)
# Sangat berguna untuk mengecek apakah server berhasil menyala
@app.get("/", tags=["Health"])
def read_root():
    return {
        "status": "success",
        "message": "Server Backend CampusMate AI (FastAPI) sedang berjalan!",
        "ai_model": "Qwen 2.5:1.5B (via Ollama)",
        "pipeline": "Retrieval-Augmented Generation (RAG)"
    }

# 6. Eksekusi Server
# Bagian ini memungkinkan kita menjalankan file ini secara langsung
if __name__ == "__main__":
    print("🚀 Memulai Server Backend CampusMate AI...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)