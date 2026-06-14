# AGENTS.md

This file provides guidance to AI coding assistants (Claude Code, Codex, Cursor, Aider, Continue, Cline, etc.) when working with the Tyra website repository.

## Project Overview

This is the source for [tyra-lang.github.io](https://tyra-lang.github.io) — the official website for the Tyra programming language. It is a static Astro site deployed via GitHub Pages.

**Compiler/language source is in a separate repo:** [tyra-lang/tyra](https://github.com/tyra-lang/tyra). Do not add compiler code here.

## Stack

- **Astro** (static output) — `astro.config.mjs`
- **Pico CSS** (`pico.classless.zinc.min.css`) — classless, styles semantic HTML directly
- **CodeMirror 6** (npm) — Playground editor
- **WASM** — `public/wasm/tyra_wasm.js` + `tyra_wasm_bg.wasm` (built from tyra-lang/tyra)
- **GitHub Actions** — build + deploy on push to `main`

## Directory Structure

```
src/
  layouts/Base.astro      — shared layout (nav, theme toggle, Pico CSS)
  pages/
    index.astro           — home page (hero, benchmark table, code preview)
    playground.astro      — interactive WASM Playground
    leaderboard.astro     — LLM pass-rate leaderboard
    compare/
      go.astro            — Tyra vs Go comparison
      crystal.astro       — Tyra vs Crystal
      gleam.astro         — Tyra vs Gleam
      ruby.astro          — Tyra vs Ruby
      v.astro             — Tyra vs V
public/
  wasm/
    tyra_wasm.js          — wasm-bindgen JS glue (DO NOT edit manually)
    tyra_wasm_bg.wasm     — compiled Tyra WASM binary (DO NOT edit manually)
.github/workflows/
  deploy.yml              — GitHub Pages deployment
```

## Development

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # production build → dist/
npm run preview   # preview dist/ locally
```

## Updating WASM

The Playground runs Tyra code via WASM. To update:

```bash
# From the tyra-lang/tyra repo root:
wasm-pack build --target web compiler/crates/tyra-wasm

# Copy artifacts into this (website) repo — adjust path if repos are not siblings:
cp compiler/crates/tyra-wasm/pkg/tyra_wasm.js    ../website/public/wasm/
cp compiler/crates/tyra-wasm/pkg/tyra_wasm_bg.wasm ../website/public/wasm/
```

Then commit and push — GitHub Actions will redeploy.

## Playground Samples

Playground code samples are defined in `src/pages/playground.astro` in the `SAMPLES` object. Each sample must use the current Tyra stdlib API. Key constraints:

- `string.*`: use `string.to_ascii_upper`, `string.to_ascii_lower`, `string.reverse`, `string.len`, etc. (no `to_upper`, no `capitalize`)
- Map: use map literal `{"k": v}` and `.insert()` / `.get()` / `.remove()` method calls (no `map.new()`, `map.set()`, `map.get()` functions)
- Set: requires `import set` and explicit type annotation `let s: Set<T> = set.new()`, then `.insert()` / `.contains()` method calls
- JSON: `json.parse(text)` returns `Result<Value, JsonError>`; use `when Ok(doc)` / `when Err(_)` match syntax (not `=>`); `doc.get(key: "name")` returns `Option<Value>`
- Match syntax: `when Pattern` (not `Pattern =>`)
- io / fs / http are NOT available in the Playground (E0200 on use — correct behavior)

## Content Guidelines

The website's tone and claims must match the positioning in `docs/strategy.md` (in the tyra-lang/tyra repo). Key constraints:

- Do not claim Tyra is "simpler than" or "better than" other languages in general
- The benchmark claim is specific: "88.7% mean pass rate, 100 tasks, Claude, multi-seed, with spec injection"
- Compare pages acknowledge honest tradeoffs — do not omit where Go/Crystal/Ruby wins
- Do not add pages, sections, or claims without maintainer direction

## Styling

Pico CSS v2 (`pico.classless.zinc.min.css`) is the baseline. Color overrides use the full Pico primary token set:

- Light: `--pico-primary: #a5341c` (coral, high contrast on white)
- Dark: `--pico-primary: #f78166` (light coral)

All 10 `--pico-primary-*` tokens must be set together (see `Base.astro`). Legacy aliases (`--accent`, `--text-muted`, `--bg`, etc.) are defined in `Base.astro` and used across pages.

Theme (light/dark) is persisted in `localStorage` under key `tyra-theme`.

## Commit Messages

Follow the same format as tyra-lang/tyra:

```
<type>(scope): <description>
```

Types: `feat`, `fix`, `docs`, `chore`, `style`. Examples:
- `feat(playground): add sorted-map sample`
- `fix(leaderboard): correct pass-rate for run57`
- `docs(compare/go): add goroutine tradeoff note`

## Do Not

- Edit `public/wasm/*.js` or `*.wasm` by hand
- Add npm dependencies without a clear reason (keep the bundle small)
- Commit `dist/` (it is gitignored; CI builds it)
- Add pages or benchmark numbers without maintainer approval
- Break the Pico CSS theming (always set all 10 `--pico-primary-*` tokens)
