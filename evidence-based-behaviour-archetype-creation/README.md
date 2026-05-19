# Evidence-based behaviour archetype creation

Cursor skill and scripts for **segment-level behaviour archetypes** from research data — not fictional named personas.

## What’s in this repo

| Path | Purpose |
|------|---------|
| `SKILL.md` | Cursor agent skill (methodology + output structure) |
| `docs/` | Principles, methodology guide, HTML checklist |
| `scripts/` | Phase 3 survey pipeline, segment pains, employee-band profiles |

There is **no bundled survey mapping**. Every study has different questions; mapping is created per export.

## Install (Cursor)

Clone into your Cursor skills folder:

```powershell
git clone https://github.com/c44-ux/Research-Skills.git `
  "$env:USERPROFILE\.cursor\skills\Research-Skills"
```

Then use the skill at `Research-Skills/evidence-based-behaviour-archetype-creation/`, or clone/copy only that subfolder into `.cursor\skills\`.

## Surveys vs interviews

| Input | How to use this skill |
|-------|------------------------|
| **Survey** (`.xlsx` / `.csv`) | Run Phase 3 scripts below after you build a **per-survey** `.column_mapping.csv` |
| **Interviews** | Follow `SKILL.md` and `docs/` — synthesise from transcripts/notes in the agent; no column mapping file |

Phase 3 is **survey-only**. Interview evidence is handled through the methodology (separate from survey columns, never merged without triangulation).

## Python (Phase 3)

```powershell
pip install pandas openpyxl
```

### 1. Export mapping template (once per survey file)

```powershell
python scripts/phase3_from_survey_xlsx.py --export-mapping-template "C:\path\to\survey.xlsx"
```

Creates `survey.column_mapping.csv` beside your data. Open in Excel and map your question headers to fields (`usage_context`, `goals`, `pain_contains`, etc.).

### 2. Run Phase 3

```powershell
python scripts/phase3_from_survey_xlsx.py "C:\path\to\survey.xlsx"
```

Writes next to the survey file:

- `<survey>.behaviour_archetype_phase3.md`
- `<survey>.behaviour_archetype_phase3.analysis.json`

## Dependency: `cs-ux-personas`

Phase 3 calls **`PersonaGenerator`** from the sibling skill `cs-ux-personas` (`scripts/persona_generator.py`).

```text
.cursor/skills/
  evidence-based-behaviour-archetype-creation/   ← this repo
  cs-ux-personas/                                ← required for phase3_from_survey_xlsx.py
```

## Do not commit

- Raw survey CSV/XLSX with respondent data
- Per-project `.column_mapping.csv` if it encodes confidential study design (optional — usually fine as structure-only)
- API keys or `.env` files
