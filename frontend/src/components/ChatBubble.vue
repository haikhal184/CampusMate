<template>
  <div 
    class="flex w-full animate-fade-in mb-4"
    :class="isUser ? 'justify-end' : 'justify-start'"
  >
    
    <div 
      v-if="!isUser" 
      class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white shadow-md flex-shrink-0 mr-3 border-2 border-slate-200 overflow-hidden"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path d="M12 14l9-5-9-5-9 5 9 5z" />
        <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" />
      </svg>
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

      <div class="mt-2 flex justify-end items-center gap-2">
        
        <template v-if="!isUser && message.source">
          
          <a 
            v-if="message.source_type === 'url'" 
            :href="message.source" 
            target="_blank" 
            class="flex items-center text-[10px] font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 px-2 py-1.5 rounded-md transition-colors border border-blue-100 shadow-sm"
            title="Buka Halaman Web"
          >
            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path></svg>
            Web UIR
          </a>

          <a 
            v-else-if="message.source_type === 'file'" 
            :href="'http://127.0.0.1:8000/dokumen/' + message.source" 
            target="_blank" 
            class="flex items-center text-[10px] font-medium text-emerald-600 bg-emerald-50 hover:bg-emerald-100 px-2 py-1.5 rounded-md transition-colors border border-emerald-100 shadow-sm"
            title="Lihat Dokumen PDF"
          >
            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            Buka PDF
          </a>

        </template>

        <span 
          class="text-[10px] font-medium opacity-70 ml-1"
          :class="isUser ? 'text-indigo-100' : 'text-slate-400'"
        >
          {{ isUser ? 'Terkirim' : 'CampusMate AI' }}
        </span>
        
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  message: {
    type: Object,
    required: true,
  }
});

const isUser = computed(() => props.message.role === 'user');
</script>