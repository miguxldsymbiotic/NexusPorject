import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/formatos': 'http://127.0.0.1:8000',
      '/demands': 'http://127.0.0.1:8000',
      '/evaluar': 'http://127.0.0.1:8000',
      '/generar-documento': 'http://127.0.0.1:8000',
      '/editar-propuesta': 'http://127.0.0.1:8000',
      '/generar-pdf-final': 'http://127.0.0.1:8000',
      '/descargar-file': 'http://127.0.0.1:8000',
      '/audio-to-idea': 'http://127.0.0.1:8000',
      '/transcription-to-idea': 'http://127.0.0.1:8000',
      '/refinar-texto': 'http://127.0.0.1:8000'
    }
  }
})
