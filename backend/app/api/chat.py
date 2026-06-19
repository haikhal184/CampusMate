from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Mengimpor fungsi utama RAG (dari rag_engine.py)
from app.core.rag_engine import generate_answer

# Membuat instance router untuk API
router = APIRouter()

# ---------------------------------------------------------
# SKEMA DATA (Pydantic Models)
# ---------------------------------------------------------

# Skema data yang akan dikirim oleh Vue.js (Frontend)
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session" 

# [PERBAIKAN] Skema data yang dikembalikan ke Vue.js sekarang mendukung Sumber Dokumen
class ChatResponse(BaseModel):
    answer: str
    source: Optional[str] = None       # Contoh: "Buku_Pedoman_KP.pdf" atau "https://..."
    source_type: Optional[str] = None  # Contoh: "file" atau "url"

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
        # 2. Proses RAG: Memanggil fungsi generate_answer
        # Sekarang result berisi dictionary: {"content": "...", "source": "...", "source_type": "..."}
        result = await generate_answer(request.message)
        
        # 3. Kembalikan Response: Format kembali menjadi JSON untuk frontend
        return ChatResponse(
            answer=result.get("content", ""),
            source=result.get("source", ""),
            source_type=result.get("source_type", "")
        )
        
    except Exception as e:
        # Jika Ollama mati atau terjadi masalah, kembalikan error 500
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan pada server AI: {str(e)}")