# Method synopsis

Salience-filtered session capture for **reproducible UX research** — arc, attribution, standalone artifact — not a transcript.

Documents rerunnable quant, qual, or mixed-methods analysis so the next wave or interview round does not start from scratch.

Part of [Research-Skills](https://github.com/c44-ux/Research-Skills). Adapted from [vanessachang-dev/chat-synopsis](https://github.com/vanessachang-dev/chat-synopsis) (MIT); renamed and extended by [Clare Reddan](https://github.com/c44-ux).

---

## Choose your platform

| Variant | Folder | Runtime | Install target |
|---------|--------|---------|----------------|
| **Cursor** | [`cursor/`](cursor/) | Cursor Agent mode | `%USERPROFILE%\.cursor\skills\method-synopsis\` or `.cursor/skills/method-synopsis/` |
| **Claude** | [`claude/`](claude/) | Claude Code, Desktop, CoWork | `~/.claude/skills/method-synopsis/` or `.claude/skills/method-synopsis/` |

Both variants share the same AAA discipline and reproducibility playbook structure. Platform-specific differences are file-save surfaces, install paths, and trigger mechanics (`@method-synopsis` in Cursor; skill auto-discovery in Claude).

---

## Quick install

**Cursor:**

```powershell
git clone https://github.com/c44-ux/Research-Skills.git `
  "$env:USERPROFILE\.cursor\skills\Research-Skills"
Copy-Item -Recurse -Force `
  "$env:USERPROFILE\.cursor\skills\Research-Skills\method-synopsis\cursor" `
  "$env:USERPROFILE\.cursor\skills\method-synopsis"
```

**Claude Code (personal):**

```powershell
git clone https://github.com/c44-ux/Research-Skills.git `
  "$env:USERPROFILE\.claude\skills\Research-Skills"
Copy-Item -Recurse -Force `
  "$env:USERPROFILE\.claude\skills\Research-Skills\method-synopsis\claude" `
  "$env:USERPROFILE\.claude\skills\method-synopsis"
```

**Claude Desktop / CoWork:** zip the [`claude/`](claude/) folder (root of zip must contain `SKILL.md`) and upload via Customize → Skills. See [claude/README.md](claude/README.md).

---

## Modes

| Mode | Trigger (either platform) | Output |
|------|---------------------------|--------|
| **General** | "method synopsis this session" | AAA synopsis |
| **Reproducibility** | "method synopsis this research" | Method playbook with rerun checklist |

See each variant's README for full trigger list, research types, and layout.
