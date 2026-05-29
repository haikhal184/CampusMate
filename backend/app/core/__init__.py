"""
Core System Package
Berisi logika inti kecerdasan buatan, pipeline Retrieval-Augmented Generation (RAG), 
dan konfigurasi Large Language Model (Qwen 2.5 1.5B).
"""

# Mengekspos fungsi utama agar bisa dipanggil langsung dari package core
# from .rag_engine import generate_answer, setup_rag

__all__ = ["generate_answer", "setup_rag"]