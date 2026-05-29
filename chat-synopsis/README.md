# chat-synopsis (Cursor skill)

Salience-filtered markdown capture of a Cursor chat: **arc**, **attribution**, **standalone artifact** — not a transcript.

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

Or copy this `chat-synopsis` folder directly to `~/.cursor/skills/chat-synopsis/`.

**Inside a project repo:**

```text
.cursor/skills/chat-synopsis/
```

Optional: add `.cursor/commands/synopsis.md` in that project for a command entry point (see [Cursor commands docs](https://cursor.com/docs)).

## Use

**Agent mode** in any project. Explicit triggers, for example:

- `synopsis this chat`
- `capture this conversation`
- `preserve what we figured out`
- **`@chat-synopsis`** (most reliable across chats)

First run asks where to save (Obsidian path, local folder, project folder, etc.) and writes [references/destinations.md](references/destinations.md).

### Not working in another chat?

| Symptom | Fix |
|--------|-----|
| Agent ignores trigger phrase | Use **`@chat-synopsis`** in that message |
| "Command not found" | Commands are per-repo; use @mention or trigger phrase |
| No file saved | Switch to **Agent** mode (not Ask) |
| Old behaviour after update | Re-copy folder to `%USERPROFILE%\.cursor\skills\chat-synopsis\`, new chat |

## Layout

```text
chat-synopsis/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
└── references/
    ├── destinations.md   # your default save location
    ├── examples.md       # AAA discipline examples
    └── privacy.md        # redaction limitations
```

## Credits

Adapted from **[chat-synopsis](https://github.com/vanessachang-dev/chat-synopsis)** by [Vanessa Chang](https://vanessachang.com) (MIT License). See [LICENSE](LICENSE).

**Cursor port (v0.2.1)** by [Clare Reddan](https://github.com/c44-ux). Changes from upstream v0.1.0:

- **Runtime** — Claude Code / Claude.ai → Cursor Agent mode and Ask/read-only mode.
- **Triggers** — `@chat-synopsis` @mention; optional `.cursor/commands/synopsis.md` command entry.
- **Destinations** — project folder (`.cursor/chat-synopses/`); Windows path examples; explicit Cursor `Write`-tool save table.
- **Troubleshooting** — Agent vs Ask, personal install at `~/.cursor/skills/`, reload after updates.
- **Packaging** — republished in [Research-Skills](https://github.com/c44-ux/Research-Skills) with Cursor install docs.

Full change list: [CHANGELOG.md](CHANGELOG.md).

Upstream: https://github.com/vanessachang-dev/chat-synopsis · https://vanessachang.com/chat-synopsis
