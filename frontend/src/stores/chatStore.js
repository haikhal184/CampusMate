import { defineStore } from 'pinia';
import { ref, watch } from 'vue';

export const useChatStore = defineStore('chat', () => {
  // ==========================================
  // 1. STATE (Penyimpanan Data)
  // ==========================================
  
  const messages = ref([]);
  const isLoading = ref(false);
  const sessionId = ref(`session_${Date.now()}`);

  // [PERBAIKAN]: Ambil riwayat dari LocalStorage jika ada. Jika tidak, mulai kosong.
  const savedHistory = localStorage.getItem('campusmate_history');
  const chatHistories = ref(savedHistory ? JSON.parse(savedHistory) : []);

  // [FITUR BARU]: Otomatis simpan ke LocalStorage setiap kali chatHistories berubah
  watch(chatHistories, (newVal) => {
    localStorage.setItem('campusmate_history', JSON.stringify(newVal));
  }, { deep: true });

  // ==========================================
  // 2. ACTIONS (Fungsi untuk Mengubah Data)
  // ==========================================

  // Fungsi internal untuk mengupdate pesan ke dalam riwayat yang sedang aktif
  const _syncCurrentChatToHistory = () => {
    const currentIndex = chatHistories.value.findIndex(c => c.id === sessionId.value);
    if (currentIndex !== -1) {
      // Gunakan JSON stringify/parse untuk menghilangkan reaktivitas (deep copy)
      chatHistories.value[currentIndex].savedMessages = JSON.parse(JSON.stringify(messages.value));
    }
  };

  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    // [FITUR BARU]: Jika ini adalah pesan pertama di sesi ini, buatkan judul di sidebar
    const existingChat = chatHistories.value.find(chat => chat.id === sessionId.value);
    if (!existingChat) {
      chatHistories.value.unshift({
        id: sessionId.value,
        // Potong judul jika terlalu panjang (maks 25 karakter)
        title: messageText.length > 25 ? messageText.substring(0, 25) + '...' : messageText,
        savedMessages: [] 
      });
    }

    // 1. Tampilkan pesan user di layar
    messages.value.push({ role: 'user', content: messageText });
    _syncCurrentChatToHistory(); // Simpan ke riwayat
    isLoading.value = true;

    try {
      // 2. Kirim permintaan ke server FastAPI
      const response = await fetch('http://127.0.0.1:8000/api/chat/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: messageText,
          session_id: sessionId.value
        })
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      // 3. Terima jawaban dari FastAPI
      const data = await response.json();
      
      messages.value.push({ 
        role: 'ai', 
        content: data.answer,
        source: data.source || '',
        source_type: data.source_type || ''
      });

      _syncCurrentChatToHistory(); // Simpan jawaban AI ke riwayat

    } catch (error) {
      console.error("Gagal menghubungi server AI:", error);
      messages.value.push({ 
        role: 'ai', 
        content: 'Mohon maaf, CampusMate sedang mengalami kendala jaringan atau server.',
        source: '', source_type: ''
      });
      _syncCurrentChatToHistory();
    } finally {
      isLoading.value = false;
    }
  };

  const startNewChat = () => {
    // Hanya buat sesi baru jika layar saat ini tidak kosong
    if (messages.value.length > 0) {
      messages.value = []; 
      sessionId.value = `session_${Date.now()}`; 
    }
  };

  const loadChat = (id) => {
    // [PERBAIKAN]: Cari chat berdasarkan ID, lalu tampilkan isi pesan aslinya
    const targetChat = chatHistories.value.find(chat => chat.id === id);
    if (targetChat) {
      sessionId.value = targetChat.id;
      messages.value = JSON.parse(JSON.stringify(targetChat.savedMessages || []));
    }
  };

  const deleteChat = (id) => {
    // Hapus dari daftar
    chatHistories.value = chatHistories.value.filter(chat => chat.id !== id);
    
    // Jika obrolan yang sedang terbuka dihapus, bersihkan layar
    if (sessionId.value === id) {
      messages.value = [];
      sessionId.value = `session_${Date.now()}`;
    }
  };

  // ==========================================
  // 3. RETURN
  // ==========================================
  return { 
    messages, 
    isLoading, 
    chatHistories, 
    sendMessage, 
    startNewChat, 
    loadChat,
    deleteChat
  };
});