# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Upstream history: [vanessachang-dev/chat-synopsis/CHANGELOG.md](https://github.com/vanessachang-dev/chat-synopsis/blob/main/CHANGELOG.md).

---

## [0.2.1] — 2026-05-29

Cursor port by [Clare Reddan](https://github.com/c44-ux). Based on upstream **v0.1.0** (MIT).

### Added

- **Cursor Agent mode** surface detection (Agent vs Ask/read-only) with a destinations table.
- **`@chat-synopsis`** @mention as an explicit trigger; expanded skill `description` frontmatter for Cursor invocation.
- **Project folder** destination: `.cursor/chat-synopses/` in the workspace (first-run wizard option 5).
- **Windows path examples** in the Obsidian wizard prompt and local-file destination notes.
- **Troubleshooting** section: Agent mode requirement, @mention reliability, personal install path, reload after updates, `disable-model-invocation` note.
- **Saving in Cursor** table in Step 6: `Write` tool paths, chat-only fallback, clipboard guidance, MCP fallback for Notion/Drive.
- Optional **`.cursor/commands/synopsis.md`** entry point (used in design-playground; documented, not bundled here).
- **Research-Skills** packaging and install docs for this monorepo.

### Changed

- Target runtime: Claude Code / Claude.ai → **Cursor** (Agent and Ask modes).
- Default frontmatter `source`: `Cursor` (was `Claude Code | Claude.ai`).
- Attribution wording: “Claude’s contributions” → “the assistant’s contributions”; assistant verb set unchanged.
- First-run wizard “Skip for now” saves to **chat output only** (upstream used local-file fallback).
- Trigger note: @mentions count as explicit triggers.
- `references/examples.md`: generic path references (no repo-specific relative links).

### Removed

- Claude Code `/synopsis` slash command and `install.sh` (replaced by Cursor install paths and optional command file).

---

## [0.1.0] — 2026-05-07 (upstream)

Original public release by [Vanessa Chang](https://github.com/vanessachang-dev/chat-synopsis). Arc / Attribution / Artifact discipline, salience check, first-run wizard, privacy pass, and reference examples.
