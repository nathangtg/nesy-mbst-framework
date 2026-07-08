import { defineConfig } from 'vite';

export default defineConfig({
  base: '/nesy-mbst-framework/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
  server: {
    port: 3000,
    open: true,
  },
});
