import { defineConfig } from 'vite';

export default defineConfig({
  base: '/llm-mbst-research/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
  server: {
    port: 3000,
    open: true,
  },
});
