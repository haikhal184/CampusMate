<template>
  <aside class="hidden md:flex flex-col w-72 h-full bg-[#F1F5F9] border-r border-slate-200/70 overflow-hidden relative z-20">
    
    <div class="p-6">
      <button 
        @click="startNewChat"
        class="w-full flex items-center justify-center gap-3 bg-indigo-600 hover:bg-indigo-700 text-white py-4 px-5 rounded-xl font-semibold btn-hover-effect shadow-md text-base transition-all"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        Obrolan Baru
      </button>
    </div>

    <div class="flex-1 overflow-y-auto p-4 space-y-2.5">
      <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4 px-3">Riwayat Terbaru</h3>
      
      <ul class="space-y-1.5">
        <li v-for="history in chatHistories" :key="history.id">
          <button 
            @click="loadChat(history.id)"
            class="w-full flex items-center gap-3 text-left px-4 py-3.5 rounded-xl text-base text-slate-700 hover:bg-white hover:text-indigo-700 transition-all border border-transparent hover:border-slate-100 group"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400 group-hover:text-indigo-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            <span class="truncate block w-full font-medium">{{ history.title }}</span>
          </button>
        </li>
      </ul>
    </div>

    <div class="p-6 border-t border-slate-200/70 bg-slate-50/50">
      <div class="flex items-center gap-3.5 px-2 py-3 cursor-pointer hover:bg-white rounded-xl transition-all">
        <div class="w-10 h-10 rounded-full bg-indigo-500/10 flex items-center justify-center text-indigo-700 font-bold text-xl border-2 border-indigo-100 shadow-inner flex-shrink-0">
          M
        </div>
        <div class="flex-1 overflow-hidden">
          <h4 class="text-base font-bold text-slate-900 truncate">Mahasiswa UIR</h4>
          <p class="text-sm text-slate-500 truncate">Teknik Informatika</p>
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-400 hover:text-slate-600 transition-colors flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </div>
    </div>
    
  </aside>
</template>

<script setup>
import { useChatStore } from '../stores/chatStore';
import { storeToRefs } from 'pinia';

const chatStore = useChatStore();
const { chatHistories } = storeToRefs(chatStore);

const startNewChat = () => {
  chatStore.startNewChat();
};

const loadChat = (id) => {
  chatStore.loadChat(id);
};
</script>