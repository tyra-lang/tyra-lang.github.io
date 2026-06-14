import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://tyra-lang.github.io',
  base: '/',
  output: 'static',
  vite: {
    build: {
      rollupOptions: {
        external: ['/wasm/tyra_wasm.js'],
      },
    },
  },
});
