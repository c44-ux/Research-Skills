# Evidence Archetypes (Claude skill)

**Evidence-based behaviour archetypes** from **your** surveys and/or interviews — any product domain. Synthesis stays local; optional publish to **your** Miro via MCP.

Part of [Research-Skills](https://github.com/c44-ux/Research-Skills). **Cursor variant:** [`../cursor/`](../cursor/).

---

## What it does

| Input | Path | Output |
|-------|------|--------|
| Interviews / transcripts | Qual synthesis in chat or files | Behaviour archetype markdown |
| Survey `.xlsx` / `.csv` | Phase 3 Python scripts | `*.behaviour_archetype_phase3.md` + JSON |
| Mixed methods | Both paths + triangulation section | Separate evidence labels |
| Miro deliverable | Miro MCP after synthesis | Docs on **your** board |

---

## Install

### From Research-Skills (recommended)

```powershell
git clone https://github.com/c44-ux/Research-Skills.git `
  "$env:USERPROFILE\.claude\skills\Research-Skills"
Copy-Item -Recurse -Force `
  "$env:USERPROFILE\.claude\skills\Research-Skills\evidence-archetypes\claude" `
  "$env:USERPROFILE\.claude\skills\evidence-archetypes"
pip install -r "$env:USERPROFILE\.claude\skills\evidence-archetypes\requirements.txt"
```

Also install sibling skill **`cs-ux-personas`** under `.claude/skills/` for survey Phase 3.

### Claude Desktop / CoWork

1. Zip **`evidence-archetypes/claude/`** so the **root of the zip** contains `SKILL.md`:

   ```powershell
   cd Research-Skills\evidence-archetypes
   Compress-Archive -Path claude/* -DestinationPath evidence-archetypes-claude.zip -Force
   ```

2. **Claude Desktop** → **CoWork** → **Customize** → **Skills** → **+** → upload zip → toggle **on**.
3. Connect **Miro** integration for board delivery — see [CONNECTORS.md](CONNECTORS.md).

### Claude Code (project repo)

```text
.claude/skills/evidence-archetypes/    # copy contents of evidence-archetypes/claude/
.claude/skills/cs-ux-personas/         # required for survey scripts
```

---

## Use

**Triggers:**

- "Build behaviour archetypes from these interview transcripts"
- "Run Phase 3 on this survey export"
- "Put the archetypes on Miro" (after synthesis)

**Survey pipeline:**

```powershell
cd path\to\evidence-archetypes
python scripts/phase3_from_survey_xlsx.py --export-mapping-template "C:\path\to\survey.xlsx"
# Edit survey.column_mapping.csv
python scripts/phase3_from_survey_xlsx.py "C:\path\to\survey.xlsx"
```

---

## Layout

```text
evidence-archetypes/claude/
├── SKILL.md
├── README.md
├── CONNECTORS.md
├── CHANGELOG.md
├── requirements.txt
├── commands/
│   └── evidence-archetypes.md
├── docs/
└── scripts/
```

---

## Credits

Methodology in `docs/` grounded in Salminen et al. (2021) and Amin et al. (2025). Survey Phase 3 uses **`cs-ux-personas`**. Packaging and Claude port: Clare Reddan / c44-ux.

Full change list: [CHANGELOG.md](CHANGELOG.md).
