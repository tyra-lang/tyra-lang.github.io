import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://tyra-lang.github.io',
  base: '/',
  output: 'static',
  integrations: [sitemap()],
  vite: {
    build: {
      rollupOptions: {
        external: ['/wasm/tyra_wasm.js'],
      },
    },
  },
});
