---
name: evidence-based-behaviour-archetype-creation
description: UX research skill — create evidence-based behaviour archetypes from surveys, interviews, or mixed methods using a strict methodology. Use for user research synthesis, audience patterns, behavioural segments, or when the user says persona/archetype and provides study materials (any product domain).
disable-model-invocation: true
---

# Evidence-Based Behaviour Archetype Creation (UX)

## Purpose

Generate **evidence-grounded behaviour archetypes** for UX and product research from the user's actual study materials — any topic (B2B, consumer, internal tools, etc.).

- **Not** fictional named personas or stock-photo identity cards.
- **Yes** segment- or pattern-level profiles backed by counts, distributions, and traceable sources.
- Works for **surveys** (quant) and **interviews** (qual), separately or triangulated.

## Required inputs

Paths are relative to this skill folder.

- `docs/Evidence based behaviour_archetype_principles.md` — guardrails (non-negotiable)
- `docs/behaviour_archetype_methodology_guide.md` — workflow and quality bar

Optional: `docs/evidence_based_behaviour_archetypes_checklist.html`

## Two input paths

### A. Interviews, notes, workshops (qualitative)

When the user supplies **transcripts, interview notes, diary studies, or workshop outputs**:

1. Read both required docs first.
2. **Do not** run Phase 3 scripts (they only apply to tabular survey exports).
3. Synthesise archetypes in Markdown using the output structure below.
4. Keep **interview claims separate** from survey/analytics unless the user explicitly triangulates.
5. Use **real quotes only** — never invent “representative” quotes.

### B. Survey export (quantitative)

When the user supplies a **SurveyMonkey / Typeform / Qualtrics-style** `.xlsx` or `.csv`:

1. Generate a per-study column map (once per file):

```powershell
python "%USERPROFILE%\.cursor\skills\evidence-based-behaviour-archetype-creation\scripts\phase3_from_survey_xlsx.py" --export-mapping-template "C:\path\to\survey.xlsx"
```

2. User edits `<survey>.column_mapping.csv` in Excel — map **their** question headers to generic fields (`segment_primary`, `usage_context`, `goals`, `pain_contains`, etc.). No bundled maps ship with this skill.

3. Run Phase 3:

```powershell
python "%USERPROFILE%\.cursor\skills\evidence-based-behaviour-archetype-creation\scripts\phase3_from_survey_xlsx.py" "C:\path\to\survey.xlsx"
```

Outputs beside the survey: `*.behaviour_archetype_phase3.md` and `*.behaviour_archetype_phase3.analysis.json`.

Optional segment reports (after mapping a segment column):

```powershell
python "%USERPROFILE%\.cursor\skills\evidence-based-behaviour-archetype-creation\scripts\phase3_from_survey_xlsx.py" --segment-pains "C:\path\to\survey.xlsx"
python "%USERPROFILE%\.cursor\skills\evidence-based-behaviour-archetype-creation\scripts\phase3_from_survey_xlsx.py" --segment-detail "C:\path\to\survey.xlsx"
```

Segment **labels** are read from survey answers — never hard-coded.

### C. Mixed methods

If both survey and interviews exist: produce survey-backed patterns from Phase 3 (or manual survey synthesis), interview enrichment separately, then a short triangulation section only where evidence aligns. Do not merge qual and quant into one claim without labeling both sources.

## Workflow (all paths)

1. Read both required Markdown files from `docs/` before producing output.
2. Confirm evidence thresholds (see methodology guide — e.g. minimum records or interviews).
3. If the HTML checklist is available, append it under `## Checklist (HTML)` unchanged.
4. If a required source file is missing, stop and report the exact path.

## Output requirements

Markdown with:

1. `## Evidence scope` — sources, n, caveats  
2. `## Observed patterns` — behaviour only, no invented identity  
3. `## Behaviour archetype profile` — segment/pattern narrative; goals, needs, frustrations tied to evidence  
4. `## Design implications` — each with a “because” linked to data  
5. `## Limitations and confidence` — uncertainty and weak signals  
6. `## Checklist (HTML)` (optional)

## Guardrails

- Never invent names, quotes, or demographics.
- Never claim certainty when signals are weak.
- Separate qualitative and quantitative claims unless triangulated.
- Label any AI-assisted interpretation.
- Prefer “observed pattern” / “behaviour archetype” over fictional customer identity.

## Trigger cues

- behaviour archetype / evidence-based archetype  
- UX research synthesis / user research synthesis  
- audience definition / behavioural segments  
- survey + interview synthesis  
- (Legacy: “persona” → behaviour archetype unless they want a named persona card)
