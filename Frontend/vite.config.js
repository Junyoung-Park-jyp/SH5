import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
// import dotenv from 'dotenv'
import { resolve } from 'path'

// dotenv.config({ path: resolve(__dirname, '../.env') });

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  define: {
    // 'import.meta.env': {
    //   ...import.meta.env,
    //   VITE_AILABAPI_API_KEY: process.env.VITE_AILABAPI_API_KEY,
    // }
  }
})
