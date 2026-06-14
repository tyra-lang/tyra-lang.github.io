# tyra-lang/website

Source for [tyra-lang.github.io](https://tyra-lang.github.io) — the official website for the [Tyra programming language](https://github.com/tyra-lang/tyra).

## Pages

| Path | Description |
|------|-------------|
| `/` | Home — language intro, benchmark table, code preview |
| `/playground` | Interactive WASM Playground (runs Tyra in the browser) |
| `/leaderboard` | LLM code-generation pass-rate leaderboard |
| `/compare/go` | Tyra vs Go |
| `/compare/crystal` | Tyra vs Crystal |
| `/compare/gleam` | Tyra vs Gleam |
| `/compare/ruby` | Tyra vs Ruby |
| `/compare/v` | Tyra vs V |

## Development

```bash
npm install
npm run dev       # dev server at http://localhost:4321
npm run build     # static build → dist/
npm run preview   # preview dist/
```

Requires Node 20+.

## Updating the Playground WASM

The Playground (`/playground`) compiles and runs Tyra code in the browser via WebAssembly. The WASM artifacts live in `public/wasm/` and must be rebuilt when the Tyra compiler changes:

```bash
# From the tyra-lang/tyra repo root:
wasm-pack build --target web compiler/crates/tyra-wasm

# Copy into this (website) repo — adjust path if repos are not siblings:
cp compiler/crates/tyra-wasm/pkg/tyra_wasm.js    ../website/public/wasm/
cp compiler/crates/tyra-wasm/pkg/tyra_wasm_bg.wasm ../website/public/wasm/
```

Commit the updated `public/wasm/` files and push — GitHub Actions will redeploy.

## Deploy

Push to `main` triggers `.github/workflows/deploy.yml`, which runs `npm run build` and deploys `dist/` to GitHub Pages.

## License

Apache-2.0
