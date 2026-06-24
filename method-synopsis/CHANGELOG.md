# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Upstream history: [vanessachang-dev/chat-synopsis/CHANGELOG.md](https://github.com/vanessachang-dev/chat-synopsis/blob/main/CHANGELOG.md).

---

## [0.4.0] — 2026-05-29

Renamed **chat-synopsis** → **method-synopsis** for reproducible research methods. Extension by [Clare Reddan](https://github.com/c44-ux).

### Changed

- Skill name, folder, @mention, and command: **method-synopsis**.
- Triggers reframed around **method synopsis** (e.g. `method synopsis this research`, `document this method for next time`).
- Output folders: `.cursor/method-synopses/`, `.cursor/method-playbooks/`.
- Destination field: `method_playbook_folder` (was `research_playbook_folder`).
- Frontmatter tags: `method-synopsis`, `method-playbook`.
- Reference doc renamed: `method-playbook.md` (was `research-playbook.md`).
- Command: `method-synopsis.md` (was `research-synopsis.md`).

### Added

- **Lineage** section in SKILL.md — credits Vanessa Chang upstream; documents rename rationale.

---

## [0.3.0] — 2026-05-29

Research playbook mode for reproducible quant, qual, and mixed-methods analysis. Extension by [Clare Reddan](https://github.com/c44-ux).

### Added

- **Research playbook mode** — triggers (`synopsis this research`, `document this analysis for next time`, qual variants) and `@chat-synopsis research`.
- **Extended output template** — Research decisions, Inputs & artefacts, Method steps (quant and/or qual rerun checklists), What changed vs last wave, Next wave playbook.
- **`research_type`** frontmatter: `survey-analysis`, `qual-analysis`, `mixed-methods`.
- **Qual analysis support** — codebook/theme rules, quote policy, participant scope, saturation notes, anonymisation in privacy pass, qual rerun checklist.
- **Research anchors** in salience check — definitions, denominators, filters, tool chains, deliverable routing (procedure-only wrap-ups valid).
- **`prior_playbook`** linking for longitudinal studies (new wave / interview round).
- **`references/examples-research.md`** — quant, qual, and mixed-methods worked examples.
- **`references/research-playbook.md`** — folder layout and integration with evidence-archetypes and uxr-planner.
- **`research_playbook_folder`** in destinations (e.g. `.cursor/research-playbooks/`).
- **`commands/research-synopsis.md`** — bundled command template for project repos.

### Changed

- Version 0.2.1 → **0.3.0**; skill description includes research triggers.
- First-run wizard adds **Research playbooks** destination option (6).
- Research playbook filename convention: `YYYY-MM-DD-{study-id}-{topic-slug}.md`.

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
