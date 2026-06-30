# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.0] — 2026-06-30

Claude skill port from Cursor `evidence-archetypes/cursor/`. Published in [Research-Skills](https://github.com/c44-ux/Research-Skills) at `evidence-archetypes/claude/`. By [Clare Reddan](https://github.com/c44-ux).

### Added

- **Claude skill package** with `SKILL.md`, `README.md`, `CONNECTORS.md`, `CHANGELOG.md`.
- **Claude-adapted paths** — `~/.claude/skills/evidence-archetypes/` for scripts and pip install.
- **Conversational Miro board gate** — numbered options; wait for user reply before `board_create`.
- **`commands/evidence-archetypes.md`** — slash command template for Claude Code / CoWork.
- **Environment matrix** in CONNECTORS.md (Claude Code vs Desktop vs chat-only).

### Unchanged from Cursor source

- `docs/` methodology and guardrails.
- `scripts/` Phase 3 survey pipeline and segment reports.
- Output structure, guardrails, and Miro doc layout rules.
