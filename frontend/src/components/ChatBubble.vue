<template>
  <div 
    class="flex w-full animate-fade-in mb-4"
    :class="isUser ? 'justify-end' : 'justify-start'"
  >
    
    <div 
      v-if="!isUser" 
      class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-lg flex-shrink-0 mr-3 shadow-sm border border-indigo-50"
    >
      🤖
    </div>

    <div 
      class="max-w-[80%] md:max-w-[70%] px-5 py-3 shadow-sm relative group"
      :class="[
        isUser 
          ? 'bg-indigo-600 text-white rounded-2xl rounded-br-none' 
          : 'bg-white border border-slate-200 text-slate-700 rounded-2xl rounded-tl-none'
      ]"
    >
      <p class="text-sm leading-relaxed whitespace-pre-wrap break-words">
        {{ message.content }}
      </p>

      <span 
        class="text-[10px] mt-1.5 block text-right font-medium opacity-70"
        :class="isUser ? 'text-indigo-100' : 'text-slate-400'"
      >
        {{ isUser ? 'Terkirim' : 'CampusMate AI' }}
      </span>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue';

// Mendefinisikan 'props' (data yang dikirim dari HomeView.vue ke komponen ini)
const props = defineProps({
  message: {
    type: Object,
    required: true,
    // Format yang diharapkan: { role: 'user' | 'assistant', content: 'Isi pesan...' }
  }
});

// Computed property untuk mengecek apakah pesan ini dari user atau bukan
// Ini akan otomatis mengatur warna dan posisi (kanan/kiri) di bagian template HTML atas
const isUser = computed(() => props.message.role === 'user');
</script>