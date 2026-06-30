---
name: evidence-archetypes
description: >-
  UX research skill (Claude variant) — create evidence-based behaviour archetypes
  from surveys, interviews, or mixed methods; synthesise locally then publish to
  Miro via Miro MCP. Use for user research synthesis, audience patterns, behavioural
  segments, evidence-based archetype, survey + interview synthesis, put on Miro, or
  when the user says persona/archetype and provides study materials.
---

# Evidence Archetypes (Claude)

**Upstream:** [Research-Skills/evidence-archetypes/claude/](https://github.com/c44-ux/Research-Skills/tree/main/evidence-archetypes/claude). **Cursor variant:** [evidence-archetypes/cursor/](../cursor/).

## Purpose

Generate **evidence-grounded behaviour archetypes** for UX and product research from **the current user's** study materials — any topic (B2B, consumer, internal tools, etc.). Each run is **self-contained**: their data, their synthesis, their Miro workspace. This skill does not point to, default to, or reuse any other researcher's boards or studies.

- **Not** fictional named personas or stock-photo identity cards.
- **Yes** segment- or pattern-level profiles backed by counts, distributions, and traceable sources.
- Works for **surveys** (quant) and **interviews** (qual), separately or triangulated.

## Required inputs

Paths are relative to this skill folder.

- `docs/Evidence based behaviour_archetype_principles.md` — guardrails (non-negotiable)
- `docs/behaviour_archetype_methodology_guide.md` — workflow and quality bar

Optional:

- `docs/evidence_based_behaviour_archetypes_checklist.html`
- `docs/miro_delivery_guide.md` — **Miro delivery** (required when user wants a board deliverable)

**Before Miro MCP calls:** read [CONNECTORS.md](CONNECTORS.md) and inspect Miro MCP tool schemas in your environment.

## Where outputs go (overview)

| Step | What | Where |
|------|------|--------|
| Synthesis | Evidence-backed archetype markdown (+ survey JSON) | Local files and/or chat |
| **Miro delivery** | Stakeholder-facing board | **User's Miro board** (via Miro MCP — not GitHub) |

GitHub only stores the **skill** (methodology + scripts). It does not host study results or Miro content.

## Two input paths

### A. Interviews, notes, workshops (qualitative)

When the user supplies **transcripts, interview notes, diary studies, or workshop outputs**:

1. Read both required docs first.
2. **Do not** run Phase 3 scripts (they only apply to tabular survey exports).
3. Synthesise archetypes in Markdown using the output structure below.
4. Keep **interview claims separate** from survey/analytics unless the user explicitly triangulates.
5. Use **real quotes only** — never invent "representative" quotes.

### B. Survey export (quantitative)

When the user supplies a **SurveyMonkey / Typeform / Qualtrics-style** `.xlsx` or `.csv`:

**Python prerequisites (one-time per machine)** — survey scripts need `pandas` and `openpyxl`. If the user has not installed them, say so explicitly and give:

```powershell
cd "%USERPROFILE%\.claude\skills\evidence-archetypes"
pip install -r requirements.txt
```

Phase 3 scripts also attempt a quiet `pip install` on first run if imports fail, but prefer telling the user to run the command above (clearer on locked-down PCs).

Also requires sibling skill **`cs-ux-personas`** (for `PersonaGenerator`) at `~/.claude/skills/cs-ux-personas/` or `.claude/skills/cs-ux-personas/`.

1. Generate a per-study column map (once per file):

```powershell
python "%USERPROFILE%\.claude\skills\evidence-archetypes\scripts\phase3_from_survey_xlsx.py" --export-mapping-template "C:\path\to\survey.xlsx"
```

2. User edits `<survey>.column_mapping.csv` in Excel — map **their** question headers to generic fields (`segment_primary`, `usage_context`, `goals`, `pain_contains`, etc.). No bundled maps ship with this skill.

3. Run Phase 3:

```powershell
python "%USERPROFILE%\.claude\skills\evidence-archetypes\scripts\phase3_from_survey_xlsx.py" "C:\path\to\survey.xlsx"
```

Outputs beside the survey: `*.behaviour_archetype_phase3.md` and `*.behaviour_archetype_phase3.analysis.json`.

Optional segment reports (after mapping a segment column):

```powershell
python "%USERPROFILE%\.claude\skills\evidence-archetypes\scripts\phase3_from_survey_xlsx.py" --segment-pains "C:\path\to\survey.xlsx"
python "%USERPROFILE%\.claude\skills\evidence-archetypes\scripts\phase3_from_survey_xlsx.py" --segment-detail "C:\path\to\survey.xlsx"
```

Segment **labels** are read from survey answers — never hard-coded.

### C. Mixed methods

If both survey and interviews exist: produce survey-backed patterns from Phase 3 (or manual survey synthesis), interview enrichment separately, then a short triangulation section only where evidence aligns. Do not merge qual and quant into one claim without labeling both sources.

## Miro delivery — publish to board

**Run after synthesis** when the user wants a visual deliverable (or says "put this on Miro", "Miro output").

**What this is (for general users):**

- Content is written to **the current user's Miro account** via **Miro MCP** — not to GitHub, not to a shared or example board.
- There is **no default board** in this skill and **no board URLs in the repo**. The only valid targets are a board **this user** supplies in the current session, or a **new** board after they approve creation.
- **Never** use, suggest, or publish to Miro URLs from prior chats, other projects, or other people's workspaces — even if they appear in conversation history.
- **Never create a board** without explicit user approval (Miro MCP requires confirmation).
- Do **not** describe this as "push" — say **publish to your Miro** or **add docs to your board**.

**Agent steps:**

1. Read `docs/miro_delivery_guide.md` and [CONNECTORS.md](CONNECTORS.md).
2. **Inputs:** final archetype markdown (and optional segment reports from survey).
3. **Board choice** (ask if unclear — present numbered options, wait for reply):
   - **Existing board** — user provides URL → `context_explore` → `doc_create` / `doc_update` on that board.
   - **New board** — user approves → `board_create` (name from study, e.g. `Behaviour archetypes — <study> — <date>`) → add docs to returned URL.
4. **Do not** use markdown tables in Miro docs — use **bullet lists**.
5. Create: one summary doc + one **doc per segment** (labels and n from data only).
6. Return the **board URL** and what was created/updated. If MCP auth fails, stop; local `.md` files remain the source of truth.

If the user only wants files (no Miro), skip Miro delivery.

## Workflow (all paths)

1. Read both required Markdown files from `docs/` before producing output.
2. Confirm evidence thresholds (see methodology guide — e.g. minimum records or interviews).
3. Produce synthesis (paths A/B/C above).
4. If the user needs a Miro deliverable, run **Miro delivery** (Miro MCP + `docs/miro_delivery_guide.md`).
5. If the HTML checklist is available, append it under `## Checklist (HTML)` in the **file** deliverable (optional on Miro summary doc only if user wants it short).
6. If a required source file is missing, stop and report the exact path.

## Output requirements

Markdown with:

1. `## Evidence scope` — sources, n, caveats  
2. `## Observed patterns` — behaviour only, no invented identity  
3. `## Behaviour archetype profile` — segment/pattern narrative; goals, needs, frustrations tied to evidence  
4. `## Design implications` — each with a "because" linked to data  
5. `## Limitations and confidence` — uncertainty and weak signals  
6. `## Checklist (HTML)` (optional)

## Guardrails

- Never invent names, quotes, or demographics.
- Never claim certainty when signals are weak.
- Separate qualitative and quantitative claims unless triangulated.
- Label any AI-assisted interpretation.
- Prefer "observed pattern" / "behaviour archetype" over fictional customer identity.
- **Miro tenancy:** publish only to boards the **current user** owns or explicitly pastes in **this** session; never reuse another project's board URL.

## Trigger cues

- evidence-archetypes / evidence-based archetype / behaviour archetype
- UX research synthesis / user research synthesis  
- audience definition / behavioural segments  
- survey + interview synthesis  
- put on Miro / update Miro board / Miro deliverable  
- (Legacy: "persona" → behaviour archetype unless they want a named persona card)

## Installing this skill

**Claude Desktop / CoWork:** Zip this folder and upload via Customize → Skills. See [README.md](README.md).

**Claude Code (project):** `.claude/skills/evidence-archetypes/` + optional [commands/evidence-archetypes.md](commands/evidence-archetypes.md).

**From Research-Skills:** Clone [c44-ux/Research-Skills](https://github.com/c44-ux/Research-Skills) and copy `evidence-archetypes/claude/`.
