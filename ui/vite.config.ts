import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
const zebra = "http://zebra:8080"
export default defineConfig({
  server: {
    proxy: {
      "/api": zebra,
      "/image": zebra,
      "/cache": zebra,
    }
  },
  plugins: [react()],
})
