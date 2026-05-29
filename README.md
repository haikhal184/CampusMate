# 🎓 CampusMate AI (Prototype)

> **Asisten Akademik Cerdas Berbasis Web Menggunakan Pendekatan Retrieval-Augmented Generation (RAG) dan Local Large Language Model (Qwen 2.5 1.5B)**

CampusMate AI adalah sistem interpretasi regulasi akademik pintar yang dirancang untuk membantu mahasiswa memahami aturan, standar operasional prosedur (SOP), dan kebijakan universitas secara kontekstual melalui interaksi bahasa alami (*natural language*). 

Berbeda dengan *chatbot* konvensional berbasis FAQ statis atau kata kunci, sistem ini memanfaatkan kemampuan penalaran (*reasoning*) dari LLM lokal yang dikombinasikan dengan pipa data RAG untuk menghasilkan jawaban yang personal, valid, serta terbebas dari risiko informasi palsu (*anti-hallucination*).

---

## 👥 Anggota Kelompok & Pembagian Tugas

* **Haikhal** (*Project Manager & System Analyst*): Merancang alur logika kesisteman, mendefinisikan skenario kasus pengujian, dan menyusun dokumen analisis.
* **Fahmi** (*AI & RAG Engineer*): Mengelola ekstraksi dokumen PDF (*data ingestion*), melakukan pemotongan teks (*chunking*), dan mengonfigurasi basis data vektor.
* **Ferdinand** (*Prompt Engineer & LLM Integration*): Mengonfigurasi *framework* Ollama untuk model Qwen 2.5, serta merancang arsitektur instruksi *system prompt* yang ketat.
* **Lutfi** (*Backend Developer*): Membangun peladen web API menggunakan FastAPI dan mengintegrasikan pipa data LangChain.
* **Dheo** (*Frontend Developer*): Mengembangkan antarmuka pengguna cerdas (*chat interface*) berbasis Vue.js dengan gaya modern-minimalis.

---

## 🧠 Implementasi Prinsip Interaksi Manusia & Komputer (IMK)

Aplikasi ini dirancang dengan menerapkan landasan teoritis utama dalam pemrosesan informasi manusia dan psikologi desain:

1. **Prinsip *Recognition over Recall* (George Miller / Ben Shneiderman):** Menyediakan fitur *Quick Starter Chips* (tombol kueri cepat) di halaman utama. Mahasiswa cukup mengenali opsi pertanyaan yang relevan tanpa harus mengingat susunan perintah dari nol.
2. **Hukum Fitts (*Fitts' Law*):** Tombol aksi utama (tombol kirim pesan dan input teks) dibuat dengan ukuran yang proporsional, mencolok, dan memiliki *affordance* yang jelas sehingga mudah dijangkau dan meminimalkan kesalahan klik.
3. **Visibilitas Status Sistem (*Visibility of System Status* - Don Norman):** Menyediakan indikator animasi mengetik (*typing indicator*) tiga titik saat menunggu respons server dan lampu indikator "Sistem Online" untuk menjembatani *Gulf of Evaluation*.
4. **Hukum Gestalt (*Proximity & Similarity*):** Gelembung obrolan dipisahkan secara tegas (kanan dengan warna Indigo untuk pengguna, kiri dengan warna putih untuk AI) menggunakan kesamaan visual dan kedekatan posisi guna mempermudah pengelompokan informasi secara alami di pikiran pengguna.
5. **Reduksi Beban Kognitif (*Cognitive Load Theory*):** Antarmuka dirancang dengan gaya modern-minimalis berbalut efek *glassmorphism* dan palet warna pastel bersih guna mengeliminasi beban kognitif ekstrinsik (*extraneous cognitive load*).

---

## 🛠️ Spesifikasi Teknologi (*Tech Stack*)

### Backend
* **Language:** Python 3.10+
* **Framework:** FastAPI (Asynchronous ASGI Web Framework)
* **LLM Engine:** Ollama (Model: `qwen2.5:1.5b`)
* **Vector Store:** ChromaDB
* **Embedding Model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
* **Framework AI:** LangChain

### Frontend
* **Language:** JavaScript / TypeScript
* **Framework:** Vue.js 3 (Composition API)
* **State Management:** Pinia
* **Styling:** Tailwind CSS & PostCSS
* **Build Tool:** Vite

---

## 🚀 Panduan Memasang dan Menjalankan Aplikasi

### Prasyarat Sistem
* Sudah terinstal **Python 3.9 atau yang lebih baru** di komputer.
* Sudah terinstal **Node.js (v18+)** dan **npm**.
* Sudah mengunduh dan menjalankan **Ollama**.

---

### Langkah 1: Persiapan Model LLM Lokal
Buka Terminal atau Command Prompt di komputermu, lalu unduh model Qwen 2.5 (1.5B) dengan perintah berikut:
```bash
ollama run qwen2.5:1.5b