import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useChatStore = defineStore('chat', () => {
  // ==========================================
  // 1. STATE (Penyimpanan Data)
  // ==========================================
  
  // Menyimpan percakapan yang sedang aktif
  const messages = ref([]);
  
  // Status loading untuk menampilkan animasi indikator mengetik
  const isLoading = ref(false);
  
  // ID sesi unik agar backend bisa membedakan riwayat percakapan
  const sessionId = ref(`session_${Date.now()}`);

  // Data dummy untuk daftar riwayat obrolan di Sidebar
  const chatHistories = ref([
    { id: 1, title: 'Aturan Kerja Praktik (KP)' },
    { id: 2, title: 'Batas SKS IPK 2.65' },
    { id: 3, title: 'Syarat Pendaftaran Skripsi' },
  ]);

  // ==========================================
  // 2. ACTIONS (Fungsi untuk Mengubah Data)
  // ==========================================

  /**
   * Fungsi untuk mengirim pesan ke Backend (FastAPI)
   * @param {string} messageText - Teks pertanyaan dari user
   */
  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    // 1. Tampilkan pesan user di layar
    messages.value.push({ role: 'user', content: messageText });
    isLoading.value = true;

    try {
      // 2. Kirim permintaan (HTTP POST) ke server FastAPI
      // Pastikan backend FastAPI sedang berjalan di port 8000
      const response = await fetch('http://127.0.0.1:8000/api/chat/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageText,
          session_id: sessionId.value
        })
      });

      // Jika server error (misal Ollama mati)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // 3. Terima jawaban dari FastAPI (Qwen 2.5) dan tampilkan di layar
      const data = await response.json();
      messages.value.push({ role: 'assistant', content: data.answer });

    } catch (error) {
      console.error("Gagal menghubungi server AI:", error);
      // Tampilkan pesan error dengan ramah tanpa merusak UI
      messages.value.push({ 
        role: 'assistant', 
        content: 'Mohon maaf, CampusMate sedang mengalami kendala jaringan atau server AI sedang tidak aktif. Silakan hubungi administrator.' 
      });
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Fungsi untuk memulai obrolan baru
   */
  const startNewChat = () => {
    messages.value = []; // Bersihkan layar
    sessionId.value = `session_${Date.now()}`; // Buat ID sesi baru
  };

  /**
   * Fungsi untuk memuat riwayat obrolan lama (Untuk dikembangkan lebih lanjut)
   * @param {number} id - ID riwayat obrolan
   */
  const loadChat = (id) => {
    console.log(`Memuat riwayat chat dengan ID: ${id}`);
    // Untuk prototype, kita bersihkan layar dan beri pesan sambutan simulasi
    messages.value = [{ 
      role: 'assistant', 
      content: `Ini adalah simulasi memuat riwayat obrolan lama dengan ID ${id}. Pada tahap pengembangan penuh, data ini akan ditarik dari PostgreSQL.` 
    }];
  };

  // ==========================================
  // 3. RETURN (Ekspos data agar bisa dipakai di komponen Vue)
  // ==========================================
  return { 
    messages, 
    isLoading, 
    chatHistories, 
    sendMessage, 
    startNewChat, 
    loadChat 
  };
});