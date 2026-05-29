from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Mengimpor fungsi utama RAG (nanti akan kita tulis di rag_engine.py)
from app.core.rag_engine import generate_answer

# Membuat instance router untuk API
router = APIRouter()

# ---------------------------------------------------------
# SKEMA DATA (Pydantic Models)
# ---------------------------------------------------------

# Skema data yang akan dikirim oleh Vue.js (Frontend)
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session" # Untuk menyimpan riwayat chat per user nanti

# Skema data yang akan dikembalikan oleh FastAPI ke Vue.js
class ChatResponse(BaseModel):
    answer: str
    # source_documents: list = [] # Opsional: Aktifkan jika ingin menampilkan halaman PDF referensi di UI

# ---------------------------------------------------------
# ENDPOINT API
# ---------------------------------------------------------

@router.post("/ask", response_model=ChatResponse)
async def ask_campusmate(request: ChatRequest):
    """
    Endpoint utama untuk menerima kueri mahasiswa.
    Menerima JSON berupa {"message": "Tanya sesuatu..."}
    """
    # 1. Validasi Input: Pastikan user tidak mengirim pesan kosong
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Pertanyaan tidak boleh kosong.")
        
    try:
        # 2. Proses RAG: Memanggil fungsi generate_answer dari core/rag_engine.py
        # Parameter dikirim ke mesin LLM (Qwen 2.5 1.5B) untuk diolah bersama dokumen
        result = await generate_answer(request.message)
        
        # 3. Kembalikan Response: Format kembali menjadi JSON untuk frontend
        return ChatResponse(answer=result)
        
    except Exception as e:
        # Jika Ollama mati atau PDF gagal dibaca, kembalikan error 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan pada server AI: {str(e)}")