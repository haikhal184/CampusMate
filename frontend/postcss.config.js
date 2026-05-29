// ==========================================
// FILE: frontend/postcss.config.js
// ==========================================

export default {
  plugins: {
    // 1. Mengaktifkan mesin Tailwind CSS untuk membaca class di file .vue kamu
    tailwindcss: {},
    
    // 2. Mengaktifkan Autoprefixer: Otomatis menambahkan vendor prefix (seperti -webkit-, -moz-)
    // agar efek Glassmorphism dan animasi CSS tetap berjalan mulus di browser lama atau Safari iOS (iPhone).
    autoprefixer: {},
  },
}