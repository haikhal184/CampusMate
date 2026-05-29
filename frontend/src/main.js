// ==========================================
// FILE: frontend/src/main.js
// ==========================================

import { createApp } from 'vue';
import { createPinia } from 'pinia';

// Mengimpor Komponen Akar (Root Component)
import App from './App.vue';

// Mengimpor file CSS yang berisi Tailwind dan kustomisasi desain kita
import './assets/style.css';

// 1. Membuat instance aplikasi Vue
const app = createApp(App);

// 2. Membuat instance Pinia (State Management)
const pinia = createPinia();

// 3. Memasang Pinia ke dalam aplikasi Vue
app.use(pinia);

// 4. Memasang (mount) aplikasi ke dalam div dengan id="app" di index.html
app.mount('#app');