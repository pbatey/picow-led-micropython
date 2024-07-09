import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react({
    jsxImportSource: "@emotion/react",
    babel: {
      plugins: ["@emotion/babel-plugin"],
    },
  })],

  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://10.0.0.97',
        changeOrigin: true,
      },
    },
  },
})
