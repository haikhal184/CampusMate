<template>
  <div class="h-screen w-screen bg-[#F8FAFC] flex font-sans text-slate-800 overflow-hidden antialiased">
    
    <Sidebar />

    <div class="flex-1 flex flex-col h-full bg-white relative">
      
      <header class="w-full px-8 py-4 flex items-center justify-between border-b border-slate-100/70 z-10 sticky top-0 bg-white/95 backdrop-blur-sm">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-indigo-50/70 rounded-full flex items-center justify-center text-lg shadow-inner border border-indigo-100">
            🎓
          </div>
          <div>
            <h1 class="text-slate-900 font-extrabold text-xl leading-tight tracking-tight">CampusMate AI</h1>
            <p class="text-slate-500 text-sm font-medium">Asisten Akademik Cerdas UIR (RAG)</p>
          </div>
        </div>
        
        <div class="flex items-center gap-2.5 px-4 py-2 bg-green-50 rounded-full border border-green-100">
          <span class="relative flex h-2.5 w-2.5">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500"></span>
          </span>
          <span class="text-green-800 text-xs font-semibold">Online</span>
        </div>
      </header>

      <div class="flex-1 overflow-y-auto px-6 py-10 bg-white" id="chat-container">
        
        <div class="max-w-4xl mx-auto space-y-3">
          
          <div v-if="messages.length === 0" class="flex flex-col items-center justify-center text-center space-y-5 animate-fade-in py-20">
             <div class="w-20 h-20 bg-indigo-50 rounded-full flex items-center justify-center text-5xl shadow-sm border-2 border-indigo-100">🎓</div>
             <h2 class="text-3xl font-extrabold text-slate-950 tracking-tight">Apa yang bisa saya bantu, Mahasiswa?</h2>
             <p class="text-lg text-slate-600 max-w-xl leading-relaxed">
               Tanyakan aturan Kerja Praktik, batas SKS, syarat Skripsi, atau sanksi Drop Out berdasarkan pedoman resmi kampus.
             </p>
          </div>

          <div class="space-y-4">
            <ChatBubble
              v-for="(msg, index) in messages"
              :key="index"
              :message="msg"
            />
          </div>

          <div v-if="isLoading" class="flex items-start gap-4 animate-fade-in mt-6">
            <div class="w-9 h-9 rounded-full bg-slate-100 flex items-center justify-center text-lg flex-shrink-0 shadow-sm border border-slate-200">🤖</div>
            <div class="bg-slate-50 border border-slate-100 rounded-2xl rounded-tl-none px-6 py-4 shadow-inner flex gap-2 items-center h-12">
              <div class="w-2.5 h-2.5 bg-slate-300 rounded-full animate-bounce"></div>
              <div class="w-2.5 h-2.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              <div class="w-2.5 h-2.5 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="messages.length === 0" class="w-full pb-8 pt-4 bg-white z-10">
        <div class="max-w-4xl mx-auto flex flex-wrap gap-2.5 justify-center">
          <button 
            v-for="prompt in quickPrompts" 
            :key="prompt" 
            @click="sendQuickPrompt(prompt)"
            class="text-sm bg-indigo-50 hover:bg-indigo-100 hover:text-indigo-800 text-indigo-900 font-semibold py-3 px-6 rounded-xl transition-all border border-indigo-100 shadow-sm hover:shadow-md"
          >
            {{ prompt }}
          </button>
        </div>
      </div>

      <div class="w-full px-6 pb-6 pt-4 bg-white z-10 sticky bottom-0">
        <form @submit.prevent="handleSubmit" class="max-w-4xl mx-auto relative flex items-center bg-slate-50 rounded-full border border-slate-200 shadow-xl focus-within:ring-2 focus-within:ring-indigo-300 focus-within:bg-white transition-all">
          <input
            v-model="userInput"
            type="text"
            placeholder="Tanyakan pedoman akademik di sini..."
            class="w-full bg-transparent text-slate-800 text-base rounded-full pl-8 pr-16 py-5 focus:outline-none transition-all"
            :disabled="isLoading"
          />
          <button
            type="submit"
            :disabled="!userInput.trim() || isLoading"
            class="absolute right-3.5 w-12 h-12 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full flex items-center justify-center transition-transform transform hover:scale-105 disabled:opacity-50 disabled:bg-slate-300 disabled:hover:scale-100 shadow-lg"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 ml-0.5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
            </svg>
          </button>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue';
import { storeToRefs } from 'pinia';
import Sidebar from '../components/Sidebar.vue';
import ChatBubble from '../components/ChatBubble.vue';
import { useChatStore } from '../stores/chatStore';

// Inisialisasi Store Pinia
const chatStore = useChatStore();
const { messages, isLoading } = storeToRefs(chatStore);

const userInput = ref('');

// Opsi kueri cepat untuk mahasiswa
const quickPrompts = [
  "Apa syarat Kerja Praktik (KP)?",
  "Kalkulasi batas SKS jika IPK 2.65",
  "Dokumen syarat pendaftaran Skripsi",
  "Aturan Remedial mahasiswa UIR?"
];

const sendQuickPrompt = (prompt) => {
  userInput.value = prompt;
  handleSubmit();
};

const handleSubmit = async () => {
  if (!userInput.value.trim() || isLoading.value) return;

  const text = userInput.value;
  userInput.value = ''; // Mengosongkan kolom input secara instan

  // Mengirimkan pesan ke Backend FastAPI via Pinia Store
  await chatStore.sendMessage(text);
};

// Logika otomatis gulir ke bawah
const scrollToBottom = () => {
  const container = document.getElementById('chat-container');
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
};

// Pantau perubahan pesan untuk memicu auto-scroll
watch(messages, () => {
  nextTick(() => {
    scrollToBottom();
  });
}, { deep: true });
</script>