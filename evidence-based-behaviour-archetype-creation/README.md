# Evidence-based behaviour archetype creation (UX)

Cursor skill for **UX and product research**: build segment-level **behaviour archetypes** with data from **surveys** and/or **interviews**.

Use your own survey or interview data
Skill produces evidence based archetype synthesis (local files)
Publish it to your own Miro — either a new board, or to an existing URL that you provide


## What’s in this repo

| Path | Purpose |
|------|---------|
| `SKILL.md` | Agent instructions (qual + quant paths, output structure) |
| `docs/` | Principles, methodology, HTML checklist |
| `scripts/` | Survey Phase 3 pipeline; optional segment reports |
| `requirements.txt` | Python deps for survey scripts (`pandas`, `openpyxl`) |

**No bundled survey maps.** Each study gets its own `<survey>.column_mapping.csv` beside the export.

## Install

```powershell
git clone https://github.com/c44-ux/Research-Skills.git `
  "$env:USERPROFILE\.cursor\skills\Research-Skills"
```

Use folder: `Research-Skills/evidence-based-behaviour-archetype-creation/`

## How researchers use it

| You have | What to do |
|----------|------------|
| **Interview transcripts / notes** | Open in Cursor with this skill — agent follows `SKILL.md` + `docs/` (no Python required) |
| **Survey .xlsx / .csv** | Run Phase 3 scripts below after mapping columns |
| **Both** | Survey via Phase 3; interviews via agent; triangulate only where evidence supports it |

## Survey pipeline (Python)

**One-time setup** (from this skill folder):

```powershell
pip install -r requirements.txt
```

Also install sibling skill **`cs-ux-personas`** next to this folder under `.cursor\skills\`.

```powershell
cd path\to\evidence-based-behaviour-archetype-creation

# 1) Create mapping template from YOUR export
python scripts/phase3_from_survey_xlsx.py --export-mapping-template "C:\path\to\survey.xlsx"

# 2) Edit survey.column_mapping.csv in Excel (map headers → fields like segment_primary, goals, pain_contains)

# 3) Generate archetype markdown + JSON
python scripts/phase3_from_survey_xlsx.py "C:\path\to\survey.xlsx"
```

Optional:

```powershell
python scripts/phase3_from_survey_xlsx.py --segment-pains "C:\path\to\survey.xlsx"
python scripts/phase3_from_survey_xlsx.py --segment-detail "C:\path\to\survey.xlsx"
```

Requires a mapped segment column (`segment_primary`, `usage_context`, or `segment`).

## Dependency

Phase 3 uses `PersonaGenerator` from sibling skill **`cs-ux-personas`**:

```text
.cursor/skills/
  evidence-based-behaviour-archetype-creation/
  cs-ux-personas/
```

## Do not commit

- Raw survey files with respondent rows  
- API keys / `.env`

## Attribution
Evidence-based behaviour archetype creation.md is adapted from community methodology content (see file header for original source reference).
