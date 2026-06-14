# CLAUDE.md

This project uses `AGENTS.md` as the primary instruction file for all AI coding assistants. **Read `AGENTS.md` first.**

## Claude Code specific additions

In addition to `AGENTS.md`:

### Conversation language

- Respond to the maintainer in Japanese
- Code, identifiers, commit messages remain English (per AGENTS.md)

### Tool usage

- Use TodoWrite for multi-step tasks (adding new pages, WASM updates)
- WASM files in `public/wasm/` are binary — do not Read or diff them

### Subagent guidance

- Content/benchmark questions: do not make changes without maintainer confirmation
- Mechanical tasks (formatting, adding a sample): subagents are appropriate
