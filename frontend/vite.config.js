import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,          // binds to 0.0.0.0
    strictPort: true,    // uses the port without fallback
    port: process.env.PORT ? Number(process.env.PORT) : 3000,
  },
});
