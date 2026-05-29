import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  // Memasang plugin Vue agar Vite bisa membaca dan merender file .vue
  plugins: [vue()],
  
  // Konfigurasi Server Pengembangan (Development Server)
  server: {
    port: 5173, // Memastikan port ini konsisten dengan izin CORS di backend
    host: true, // Mengizinkan akses dari IP lokal (berguna jika kamu mau demo buka dari HP/Tablet yang satu WiFi)
    strictPort: true, // Akan memunculkan error jika port 5173 sedang dipakai aplikasi lain, alih-alih mengganti port acak
  }
})