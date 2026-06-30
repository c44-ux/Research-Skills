# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.0] — 2026-06-30

Claude skill port from Cursor `method-synopsis/cursor/`. Published in [Research-Skills](https://github.com/c44-ux/Research-Skills) at `method-synopsis/claude/`. By [Clare Reddan](https://github.com/c44-ux).

### Added

- **Claude skill package** at `.claude/skills/method-synopsis/` with `SKILL.md`, `README.md`, `LICENSE`.
- **Surface detection** for Claude Code vs Desktop/CoWork vs chat-only.
- **Conversational first-run wizard** — numbered destination options; agent waits for reply (replaces Cursor AskQuestion).
- **Default save paths** — `.claude/method-synopses/` and `.claude/method-playbooks/` (replacing `.cursor/` equivalents).
- **`source: Claude`** in frontmatter default (replacing `Cursor`).
- **`commands/method-synopsis.md`** — slash command template for Claude Code / CoWork.
- **`references/`** — destinations, examples, examples-research, method-playbook, privacy (paths updated for Claude layout).

### Unchanged from Cursor source

- AAA discipline (Arc, Attribution, Artifact).
- Reproducibility mode with quant / qual / mixed-methods types.
- Method anchor salience check.
- Privacy pass and preview-before-save workflow.
- Output structures for general and reproducibility modes.
