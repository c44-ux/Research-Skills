# method-synopsis (Claude skill)

**Method synopsis** — capture a Claude session as durable, rerunnable documentation for UX research (quant, qual, or mixed methods).

Part of [Research-Skills](https://github.com/c44-ux/Research-Skills). **Cursor variant:** [`../cursor/`](../cursor/).

Licensed under [MIT](LICENSE). Copyright (c) 2026 Vanessa Chang; Clare Reddan (adaptations).

---

## What it does

The orchestrator ([`SKILL.md`](SKILL.md)) produces two kinds of output:

| Mode | Trigger | Output |
|------|---------|--------|
| **General** | "method synopsis this session" | AAA synopsis — arc, attribution, insights |
| **Reproducibility** | "method synopsis this research" / `/method-synopsis` | Method playbook — definitions, rerun checklist, wave diff |

Three research types: `survey-analysis`, `qual-analysis`, `mixed-methods`.

---

## Install

### From Research-Skills (recommended)

```powershell
git clone https://github.com/c44-ux/Research-Skills.git `
  "$env:USERPROFILE\.claude\skills\Research-Skills"
Copy-Item -Recurse -Force `
  "$env:USERPROFILE\.claude\skills\Research-Skills\method-synopsis\claude" `
  "$env:USERPROFILE\.claude\skills\method-synopsis"
```

Use folder: `Research-Skills/method-synopsis/claude/`

### Claude CoWork / Claude Desktop

1. Zip **`method-synopsis/claude/`** so the **root of the zip** contains `SKILL.md`:

   ```powershell
   cd Research-Skills\method-synopsis
   Compress-Archive -Path claude/* -DestinationPath method-synopsis-claude.zip -Force
   ```

2. Open **Claude Desktop** → **CoWork** → **Customize** → **Skills**.
3. Click **+** → **Upload a skill** → select `method-synopsis-claude.zip`.
4. Toggle the skill **on**.

### Claude Code (project repo)

```text
.claude/skills/method-synopsis/       # copy contents of method-synopsis/claude/
.claude/commands/method-synopsis.md   # copy from method-synopsis/claude/commands/
.claude/method-playbooks/             # rerunnable study docs
```

Add a project slash command (optional): copy [`commands/method-synopsis.md`](commands/method-synopsis.md) into `.claude/commands/method-synopsis.md`.

---

## Use

**Triggers:**

- `method synopsis this session` — general AAA capture
- `method synopsis this research` — reproducibility playbook after analysis
- `method synopsis this qual analysis` — force qual framing
- `/method-synopsis` (if command installed)

**Typical flow:**

1. Complete your analysis session in Claude.
2. Say **"method synopsis this research"** (or run `/method-synopsis`).
3. Review the anchor list Claude surfaces.
4. Preview the full markdown — Accept, Edit, or Cancel.
5. File saves to `.claude/method-playbooks/` (default) or your configured destination.

---

## Layout

```text
method-synopsis/claude/
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

---

## Default save paths

| Output | Default folder |
|--------|----------------|
| General synopses | `.claude/method-synopses/` |
| Method playbooks | `.claude/method-playbooks/` |

Configure in [`references/destinations.md`](references/destinations.md).

---

## Credits

- Upstream: [chat-synopsis](https://github.com/vanessachang-dev/chat-synopsis) by Vanessa Chang (MIT).
- Research extensions (Cursor v0.4.0) and Claude port v1.0.0: Clare Reddan / c44-ux.

Full change list: [CHANGELOG.md](CHANGELOG.md).
