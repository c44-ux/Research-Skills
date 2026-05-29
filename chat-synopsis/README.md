# chat-synopsis (Cursor skill)

Salience-filtered markdown capture of a Cursor chat: **arc**, **attribution**, **standalone artifact** — not a transcript.

**Research playbook mode (v0.3.0):** document quant, qual, or mixed-methods analysis so the next wave or interview round is rerunnable.

Part of [Research-Skills](https://github.com/c44-ux/Research-Skills).

## Install

**From this repo (recommended):**

```powershell
git clone https://github.com/c44-ux/Research-Skills.git `
  "$env:USERPROFILE\.cursor\skills\Research-Skills"
```

Use folder: `Research-Skills/chat-synopsis/`

**Personal (flat path — works in every project):**

```powershell
Copy-Item -Recurse -Force `
  "$env:USERPROFILE\.cursor\skills\Research-Skills\chat-synopsis" `
  "$env:USERPROFILE\.cursor\skills\chat-synopsis"
```

**Inside a project repo:**

```text
.cursor/skills/chat-synopsis/
.cursor/commands/research-synopsis.md   # copy from chat-synopsis/commands/
.cursor/research-playbooks/             # optional; study rerun docs
```

## Use

**Agent mode** in any project.

**General capture:**
- `synopsis this chat` · `capture this conversation` · `@chat-synopsis`

**Research playbook** (after analysis is complete):
- `synopsis this research` · `document this analysis for next time`
- `synopsis this qual analysis` · `synopsis this interview analysis`
- **`research-synopsis`** command (copy from [`commands/research-synopsis.md`](commands/research-synopsis.md))

First run asks where to save and writes [references/destinations.md](references/destinations.md). Set `research_playbook_folder` for study docs (see [references/research-playbook.md](references/research-playbook.md)).

### Research types

| Type | When | Playbook captures |
|------|------|-------------------|
| **survey-analysis** | Cohort metrics, exports, segmentation | Metric definitions, denominators, script chain, quant rerun steps |
| **qual-analysis** | Interviews, transcripts, themes | Codebook, quote policy, scope, saturation, qual rerun steps |
| **mixed-methods** | Both in one study | Separate quant/qual sections; triangulation rules |

### Not working in another chat?

| Symptom | Fix |
|--------|-----|
| Agent ignores trigger phrase | Use **`@chat-synopsis`** or **`@chat-synopsis research`** |
| No playbook sections | Use research trigger or **`research-synopsis`** command |
| No file saved | Switch to **Agent** mode (not Ask) |
| Old behaviour after update | Re-copy folder, new chat |

## Layout

```text
chat-synopsis/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── commands/
│   └── research-synopsis.md
└── references/
    ├── destinations.md
    ├── examples.md
    ├── examples-research.md    # quant & qual playbook examples
    ├── research-playbook.md    # integration with other Research-Skills
    └── privacy.md
```

## Credits

Adapted from **[chat-synopsis](https://github.com/vanessachang-dev/chat-synopsis)** by [Vanessa Chang](https://vanessachang.com) (MIT License). See [LICENSE](LICENSE).

**Cursor port** by [Clare Reddan](https://github.com/c44-ux):
- **v0.2.1** — Cursor Agent mode, @mention, project destinations
- **v0.3.0** — research playbook mode (quant, qual, mixed-methods)

Full change list: [CHANGELOG.md](CHANGELOG.md).

Upstream: https://github.com/vanessachang-dev/chat-synopsis · https://vanessachang.com/chat-synopsis
