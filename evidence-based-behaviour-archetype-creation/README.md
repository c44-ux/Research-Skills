# Evidence-based behaviour archetype creation (UX)

Cursor skill for **UX and product research**: build **your** segment-level **behaviour archetypes** from **your** surveys and/or interviews — any domain.

The skill produces evidence-based archetype synthesis as **local files** (`.md` / `.json`). You can **publish to your own Miro** when ready — approve a **new board** or paste **your** board URL. No shared boards, no bundled study data, no organisation-specific defaults.

## What’s in this repo

| Path | Purpose |
|------|---------|
| `SKILL.md` | Agent instructions (synthesis + Miro delivery) |
| `docs/` | Principles, methodology, checklist, `miro_delivery_guide.md` |
| `scripts/` | Survey Phase 3 pipeline; optional segment reports |
| `requirements.txt` | Python deps for survey scripts (`pandas`, `openpyxl`) |

**No bundled survey maps.** Each study gets its own `<survey>.column_mapping.csv` beside the export.

## End-to-end flow

```text
Survey / interviews  →  Synthesis (local .md / .json)  →  Miro board (Miro MCP in Cursor)
```

- **GitHub** stores this skill only — not your study data and not Miro content.
- **Miro** is the usual stakeholder deliverable. The agent uses **Miro MCP** to write into **your** Miro account — either on a board URL you paste, or on a **new board** it creates after you approve (not via git push).

## Install

```powershell
git clone https://github.com/c44-ux/Research-Skills.git `
  "$env:USERPROFILE\.cursor\skills\Research-Skills"
```

Use folder: `Research-Skills/evidence-based-behaviour-archetype-creation/`

Optional: copy that folder to `%USERPROFILE%\.cursor\skills\evidence-based-behaviour-archetype-creation\` if you prefer a flat skills path (update paths in commands accordingly).

## How researchers use it

| Step | What you do |
|------|-------------|
| **1. Install** | Clone this repo; open the skill folder in Cursor. For surveys: `pip install -r requirements.txt` and install sibling skill **`cs-ux-personas`** under `.cursor\skills\`. Enable **Miro MCP** in Cursor if you want board delivery. |
| **2. Your data** | Add **your** interview materials or survey export locally (never commit raw respondent data or PII raw data). |
| **3. Synthesise** | **Interviews:** agent follows `SKILL.md` + `docs/` (no Python). **Survey:** build `.column_mapping.csv`, then run Phase 3 scripts (below). **Both:** survey scripts + agent; triangulate only where evidence supports it. |
| **4. Miro (optional)** | Ask the agent for **Miro delivery** — it publishes to **your** Miro only: approve a **new board**, or paste **your** board URL. No shared or default boards. See [Miro delivery](#miro-delivery). |

**Outputs:** synthesis files beside your survey or in chat; stakeholder board in **your** Miro workspace when you run step 4.

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

## Miro delivery

After synthesis, use Cursor with **Miro MCP** enabled and signed in to Miro. Ask the agent to run **Miro delivery** (`SKILL.md` / `docs/miro_delivery_guide.md`).

| Option | What you do |
|--------|-------------|
| **New board** | Say e.g. “Create a new Miro board for this study” and confirm when asked |
| **Existing board** | Paste your board URL and say e.g. “Add archetypes to this board” |

The skill does not publish to GitHub or a central shared board — only to boards in **your** Miro workspace.

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

### Upstream: `cs-ux-personas` (survey Phase 3)

Survey quant analysis calls **`PersonaGenerator`** from the separate sibling skill **`cs-ux-personas`** (`scripts/persona_generator.py`). Install it next to this folder under `.cursor/skills/`. That module’s header cites **Salminen et al. (2021)** for data-driven persona development standards; this skill depends on it for pattern aggregation but does not redistribute its source.

### Methodology sources

Evidence standards and evaluation criteria in `docs/` are grounded in:

- **Salminen, J., et al. (2021).** *A Survey of 15 Years of Data-Driven Persona Development.* IJHCI. DOI: [10.1080/10447318.2021.1908670](https://doi.org/10.1080/10447318.2021.1908670)
- **Amin, D., et al. (2025).** *Creating and Evaluating Personas Using Generative AI: A Scoping Review of 81 Articles.* arXiv:2504.04927v2

The interactive **`docs/evidence_based_behaviour_archetypes_checklist.html`** translates those reviews into phase-by-phase peer-review-style checks (evidence base, GenAI risks, inclusivity, evaluation).

### Core adaptations in this skill (Clare Reddan / c44-ux)

This repository is **not** a copy of `cs-ux-personas`. It packages a **UX research workflow** with deliberate changes to reduce bias and misuse of AI-assisted synthesis:

| Area | What changed |
|------|----------------|
| **Artefact** | **Behaviour archetypes** (segment-level, evidence-counted) — not fictional named persona cards or stock identity. |
| **Scope** | **Domain-neutral** — no bundled survey maps, product-specific column maps, or default Miro boards; each study ships its own `.column_mapping.csv` beside the export. |
| **Survey path** | `phase3_from_survey_xlsx.py` + mapping template, optional `segment_pains` / `segment_detail` — segment **labels come from respondent data**, never hard-coded from another study. |
| **Qual / mixed** | Interview and survey claims stay **separate** unless the researcher explicitly triangulates; real quotes only. |
| **Bias & GenAI guardrails** | `SKILL.md` + `docs/Evidence based behaviour_archetype_principles.md` enforce evidence-before-inference, minimum thresholds, limitations/confidence blocks, no demographic invention, design implications with explicit “because” links, and documented AI involvement (aligned with Amin et al. PG1–PG7). |
| **Peer-review checklist** | HTML checklist maps Salminen gaps and GenAI evaluation obligations to actionable steps before sharing with stakeholders. |
| **Delivery** | **`docs/miro_delivery_guide.md`** — publish to **the current user’s** Miro via MCP only (new board with approval, or their URL); no shared repo boards. |
| **Agent workflow** | Cursor `SKILL.md` paths for qual-only, quant-only, and mixed methods, plus Miro tenancy rules (no reusing board URLs from other projects or chats). |

Earlier community methodology content informed `docs/`; file headers note where prose was adapted. **Your study data and boards stay local** — GitHub stores methodology and scripts only.
