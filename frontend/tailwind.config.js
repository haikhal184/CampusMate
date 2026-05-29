/** @type {import('tailwindcss').Config} */
export default {
  // Memberi tahu Tailwind untuk memindai class di dalam file HTML dan Vue kita
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Menambahkan font Inter sebagai font utama (sans)
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      // Kamu bisa menambahkan palet warna khusus kampus UIR di sini jika diperlukan nanti
      colors: {
        // Contoh: 'kampus': '#1e3a8a'
      }
    },
  },
  plugins: [],
}