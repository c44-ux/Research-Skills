---
name: evidence-based-behaviour-archetype-creation
description: Create evidence-based behaviour archetypes from research inputs using a strict methodology. Use when the user asks for behaviour archetype creation, audience definition, user pattern synthesis, or UX research synthesis, especially when they provide source documents or ask for evidence-grounded profiles.
disable-model-invocation: true
---

# Evidence-Based Behaviour Archetype Creation

## Purpose

Use this skill to generate evidence-grounded **behaviour archetype** outputs from supplied research materials while avoiding fabricated details, weak-signal overreach, and unsupported demographic inference.

Do **not** produce traditional named personas (fictional identity cards). Produce **segment-level behaviour archetypes** backed by distributions and observed patterns.

## Required inputs

Paths are relative to this skill folder (repo root when cloned from GitHub).

- Primary principles reference: `docs/Evidence based behaviour_archetype_principles.md`
- Methodology workflow reference: `docs/behaviour_archetype_methodology_guide.md`

Optional:
- Checklist reference (HTML): `docs/evidence_based_behaviour_archetypes_checklist.html`

## Interviews and other qualitative sources

When the user provides **interview transcripts, notes, or workshop outputs** (not a tabular survey), do **not** use Phase 3 scripts. Read `docs/` and produce behaviour archetype output directly from the supplied materials, keeping interview claims separate from any survey or analytics data unless explicitly triangulated.

## Phase 3 (survey Excel)

When the user provides an `.xlsx` or `.csv` survey export, run locally (agent shell may not execute on Windows):

```powershell
python "%USERPROFILE%\.cursor\skills\evidence-based-behaviour-archetype-creation\scripts\phase3_from_survey_xlsx.py" "C:\path\to\survey.xlsx"
```

Writes `<survey>.behaviour_archetype_phase3.md` and `.behaviour_archetype_phase3.analysis.json` next to the workbook, with full skill sections and the HTML checklist appended.

Column mapping is edited in Excel via **CSV** beside your survey file only:

- `<survey-file>.column_mapping.csv` (generated per study — not shipped with this skill)

Generate and populate the CSV with **every** survey column (merges into existing file, or use `--force` to rebuild):

```powershell
python "%USERPROFILE%\.cursor\skills\evidence-based-behaviour-archetype-creation\scripts\phase3_from_survey_xlsx.py" --export-mapping-template "C:\path\to\survey.xlsx"
python "%USERPROFILE%\.cursor\skills\evidence-based-behaviour-archetype-creation\scripts\phase3_from_survey_xlsx.py" --export-mapping-template --force "C:\path\to\survey.xlsx"
```

Inspect resolved mapping:

```powershell
python "%USERPROFILE%\.cursor\skills\evidence-based-behaviour-archetype-creation\scripts\phase3_from_survey_xlsx.py" --list-columns "C:\path\to\survey.xlsx"
```

## Workflow

1. Read both required Markdown files from `docs/` before producing any behaviour archetype output.
2. Treat the principles file as non-negotiable guardrails.
3. Treat the methodology guide as the execution sequence and quality standard.
4. If the HTML checklist is available, include it in the final output as-is under a `## Checklist (HTML)` section.
5. If a required source file is missing, stop and report exactly which file path could not be read.

## Output requirements

Produce a Markdown output with these sections:

1. `## Evidence scope`
   - Data/source summary
   - Data quality caveats
2. `## Observed patterns`
   - Behavioral patterns only
   - No fabricated identity
3. `## Behaviour archetype profile`
   - Evidence-grounded profile narrative (segment or pattern-level — not a named individual)
   - Goals, needs, and frustrations tied to evidence
4. `## Design implications`
   - Each implication must include a brief "because" rationale tied to observed signals
5. `## Limitations and confidence`
   - Explicitly state uncertainties, contradictions, and weak signals
6. `## Checklist (HTML)` (optional)
   - Include the checklist HTML exactly as provided when available

## Guardrails

- Never invent names, quotes, or demographics.
- Never claim certainty when signals are weak.
- Keep qualitative and quantitative claims clearly separated unless explicitly triangulated.
- If using AI-assisted interpretation, explicitly label where AI was used.
- Prefer "observed pattern" and "behaviour archetype" language over fictional customer identity.

## Trigger cues

Apply this skill when user requests include phrases like:

- "behaviour archetype creation"
- "evidence-based behaviour archetype"
- "target audience behaviour archetype"
- "ux research synthesis"
- "user behavior patterns"
- "audience definition"

(Legacy trigger: users may still say "persona" — treat that as behaviour archetype creation unless they explicitly want a named persona card.)
