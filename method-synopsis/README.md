# method-synopsis (Cursor skill)

**Method synopsis** — salience-filtered capture of a Cursor session for **reproducibility**: arc, attribution, standalone artifact — not a transcript.

Documents rerunnable quant, qual, or mixed-methods analysis so the next wave or interview round does not start from scratch.

Part of [Research-Skills](https://github.com/c44-ux/Research-Skills).

## Install

**From this repo (recommended):**

```powershell
git clone https://github.com/c44-ux/Research-Skills.git `
  "$env:USERPROFILE\.cursor\skills\Research-Skills"
```

Use folder: `Research-Skills/method-synopsis/`

**Personal (flat path — works in every project):**

```powershell
Copy-Item -Recurse -Force `
  "$env:USERPROFILE\.cursor\skills\Research-Skills\method-synopsis" `
  "$env:USERPROFILE\.cursor\skills\method-synopsis"
```

**Inside a project repo:**

```text
.cursor/skills/method-synopsis/
.cursor/commands/method-synopsis.md   # copy from method-synopsis/commands/
.cursor/method-playbooks/             # rerunnable study docs
```

## Use

**Agent mode** in any project.

**General capture:**
- `method synopsis` · `method synopsis this session` · `@method-synopsis`

**Reproducibility** (after analysis is complete):
- `method synopsis this research` · `document this method for next time`
- `method synopsis this qual analysis` · `method synopsis this interview analysis`
- **`method-synopsis`** command (copy from [`commands/method-synopsis.md`](commands/method-synopsis.md))

First run asks where to save and writes [references/destinations.md](references/destinations.md).

### Research types

| Type | When | Playbook captures |
|------|------|-------------------|
| **survey-analysis** | Cohort metrics, exports, segmentation | Metric definitions, denominators, script chain |
| **qual-analysis** | Interviews, transcripts, themes | Codebook, quote policy, scope, saturation |
| **mixed-methods** | Both in one study | Separate quant/qual sections; triangulation rules |

### Not working in another chat?

| Symptom | Fix |
|--------|-----|
| Agent ignores trigger phrase | Use **`@method-synopsis`** or **`@method-synopsis research`** |
| No playbook sections | Use **`method-synopsis`** command or research trigger |
| No file saved | Switch to **Agent** mode (not Ask) |
| Old behaviour after update | Re-copy folder, new chat |

## Layout

```text
method-synopsis/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── commands/
│   └── method-synopsis.md
└── references/
    ├── destinations.md
    ├── examples.md
    ├── examples-research.md
    ├── method-playbook.md
    └── privacy.md
```

## Credits

Adapted from **[chat-synopsis](https://github.com/vanessachang-dev/chat-synopsis)** by [Vanessa Chang](https://vanessachang.com) (MIT License). See [LICENSE](LICENSE).

**Cursor port and rename** by [Clare Reddan](https://github.com/c44-ux):
- **v0.2.1** — Cursor Agent mode (as chat-synopsis)
- **v0.3.0** — research playbook mode (quant, qual, mixed)
- **v0.4.0** — renamed **method-synopsis** for reproducibility

Full change list: [CHANGELOG.md](CHANGELOG.md).

Upstream: https://github.com/vanessachang-dev/chat-synopsis · https://vanessachang.com/chat-synopsis
