import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://tyra-lang.github.io',
  base: '/',
  output: 'static',
  integrations: [sitemap()],
  markdown: {
    // Tyra has no Shiki grammar; alias to Ruby (closest surface syntax) so
    // `tyra` code blocks in blog posts get sensible highlighting.
    shikiConfig: {
      langAlias: { tyra: 'ruby' },
    },
  },
  vite: {
    build: {
      rollupOptions: {
        external: ['/wasm/tyra_wasm.js'],
      },
    },
  },
});
