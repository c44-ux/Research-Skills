---
name: chat-synopsis
description: >-
  Captures a Cursor chat as a durable markdown synopsis (arc, attribution,
  standalone artifact)—not a transcript. Invoke immediately when the user says
  "synopsis this chat," "synopsis this conversation," "capture this conversation,"
  "preserve this thinking," "preserve what we figured out," "save what we just
  figured out," @mentions chat-synopsis, or runs the synopsis command. Do not use
  for generic summaries or transcript requests. Salience filter for reframes,
  decisions, and insights worth keeping.
version: 0.2.1
---

# Chat Synopsis

Capture a Cursor conversation as a durable markdown artifact in the user's thinking system. Three things get preserved:

1. **Arc** — how the conversation unfolded: where it started, where it shifted, where it landed. Not a chronological list of events.
2. **Attribution** — who contributed what. The user's contributions and the assistant's contributions are named, not collapsed into "we."
3. **Artifact** — a self-contained markdown file that stands alone, routed to the user's configured destination (Obsidian vault folder, local path, Notion, Drive, or chat output).

This is a salience filter, not a transcript. Capture the moments that produced new thinking — reframes, decisions, insights — not every exchange.

---

## Triggers

Activate **only** on these natural-language phrases (or a per-run override of the form `<trigger> → <destination>`):

- "synopsis this chat" / "synopsis this conversation"
- "capture this conversation"
- "preserve this thinking" / "preserve what we figured out"
- "save what we just figured out"

In Cursor, @mentioning **`chat-synopsis`** (or this `SKILL.md`) always activates the workflow. The **`synopsis`** command works only in repos that include `.cursor/commands/synopsis.md` (optional; not bundled in Research-Skills).

**Do not activate without an explicit trigger** — but trigger phrases and @mentions count as explicit.

### If the skill does not run in a new chat

1. **Agent mode** — synopsis saving needs the Write tool; Ask/read-only mode can only preview in chat.
2. **@mention** — type `@` → Skills → **chat-synopsis** (most reliable in any project).
3. **Personal install** — skill must live at `%USERPROFILE%\.cursor\skills\chat-synopsis\` for non–design-playground repos.
4. **Reload** — after installing or updating, start a **new** Agent chat (or restart Cursor).
5. **No `disable-model-invocation`** — this skill is designed to load on trigger phrases; if an old copy still has that flag, remove it and re-copy the folder.

---

## Procedure

### Step 1 — Surface detection

Detect what the current Cursor session can do:

| Surface | When | Destinations |
|--------|------|----------------|
| **Agent mode** | Write tool and shell available | Obsidian (vault path), project or local file (`Write`), Notion/Drive (MCP if installed), show in chat + user copies |
| **Ask / read-only** | No file writes | Show full markdown in chat; offer clipboard copy; Notion/Drive only if MCP works without writes |

Surface awareness only affects which destinations are *offered*. The artifact format (markdown) is the same everywhere.

**Default `source` in frontmatter:** `Cursor`.

### Step 2 — First-run wizard (if no destination configured)

Read [references/destinations.md](references/destinations.md). If **Configured Defaults** is empty or still has placeholder values, run the setup wizard inline before continuing:

> "Looks like this is your first time running chat-synopsis. Where should your synopses live? You'll only set this once.
>
> 1. **Obsidian** — paste the absolute path to the folder in your vault where synopses go (e.g. `C:\Users\you\Documents\Obsidian\MyVault\Synopses` or `/Users/you/Documents/Obsidian/MyVault/Synopses`).
> 2. **Notion** — paste a Notion database URL or share-link; extract the database ID for MCP.
> 3. **Google Drive** — paste a folder URL or ID (Drive MCP if installed).
> 4. **Local file** — synopses save under `~/chat-synopses/` (Windows: `%USERPROFILE%\chat-synopses\`).
> 5. **Project folder** — synopses save under `.cursor/chat-synopses/` in the workspace (good for team repos).
> 6. **Skip for now** — use chat output only this run; configure later in `references/destinations.md`."

When the user picks a destination, update **Configured Defaults** in `references/destinations.md` (path / database ID / folder ID + destination type). Confirm in one sentence where the default was saved.

Then continue with Step 3.

### Step 3 — Salience check

Before generating the synopsis, scan the conversation for **anchors**:

- A reframe ("I was thinking about this wrong; the real question is X")
- A decision (a choice made between alternatives)
- An insight (something the user articulated that wasn't visible at the start)
- A breakthrough (a stuck point that resolved)
- A useful artifact (code shipped, plan written, document drafted)
- A notable framing shift (the topic itself changed shape)

List the anchors found, briefly, before rendering. If **at least one** anchor exists, proceed. A single anchor in a long thread is enough for a proportionally short artifact.

If **zero** anchors exist (e.g. single-topic lookup, "how do I install foo?"), say so honestly and ask before proceeding:

> "This looks like a [single-topic lookup / debugging recap / no-pivot Q&A] — I didn't find a reframe, decision, or insight that would otherwise be lost. A synopsis here would mostly restate what's already visible in the chat. Want me to run it anyway?"

Only generate after explicit confirmation in the zero-anchor case.

### Step 4 — Privacy pass

Before rendering, scan the conversation for high-risk patterns and replace matches with `[REDACTED]` in the synopsis output:

- API keys: `sk-[A-Za-z0-9]{20,}`, `ghp_[A-Za-z0-9]{20,}`, `xoxb-…`, `xoxp-…`, AWS-style `AKIA[A-Z0-9]{16}`, GCP-style `AIza[A-Za-z0-9_-]{35}`.
- JWTs: three base64 segments separated by dots where the first decodes to JSON containing `"alg"`.
- Lines whose left-hand label matches `password|secret|api_key|token|access_key|private_key` followed by `:` or `=` and a string value.

Best-effort only — see [references/privacy.md](references/privacy.md). Mandatory preview (Step 6) is the user's last line of defense.

### Step 5 — Render under AAA discipline

Apply Arc / Attribution / Artifact discipline. See [references/examples.md](references/examples.md) for worked positive/negative pairs.

**Arc discipline.** In **What Happened**, trace the through-line: start → shift → land. Do not produce a chronological event list. If there was no arc, say so explicitly ("Single-topic execution session, no significant pivots") rather than inflating one.

**Attribution discipline.** Every sentence describing action names the actor.

- **User verbs:** *directed, asked, decided, caught, reframed, pushed back, named, surfaced, clarified, refined, chose, rejected, noticed, vetoed, recognized, distinguished.*
- **Assistant verbs:** *drafted, proposed, scaffolded, explained, generated, suggested, summarized, restated, investigated, recommended.*
- **Forbidden:** "we" for one-party action; passive voice that hides the actor; narrating the assistant's work as the user's accomplishment.
- **Joint credit:** "User proposed X; assistant refined it into Y; user chose Y."

**Artifact discipline.** The output must read coherently to someone who wasn't in the conversation. No "earlier in this chat" or "as I said."

### Output structure

Use the section shape below. **Omit empty sections.** Section names may adapt (e.g. "Decisions Made" → "Insights"). Smart brevity throughout.

```markdown
---
title: "[Primary Topic]"
date: YYYY-MM-DD
source: Cursor
project: [if applicable]
tags:
  - chat-synopsis
  - [topic-tags]
---

## Synopsis
[2–4 sentences. What this conversation was about and what it produced.]

## What Happened
[Arc-traced narrative. Through-line, not event list. Attribution-disciplined throughout.]

## Decisions Made / Insights / Reframes
- [Anchor]: [Context — what was decided, seen, or shifted]

## Quotable Moments
> "[Verbatim user language when they coined a phrase, named a constraint, or articulated something precisely]"

## Open Threads
- [What's unresolved or wants future attention]

## Next Steps
- [ ] [Concrete follow-up if any]
```

### Step 6 — Mandatory preview, then save

Show the rendered markdown to the user. Wait for one of:

- **Accept** — save at the configured destination (or per-run override).
- **Edit** — apply changes, re-preview.
- **Cancel** — discard and end.
- **Per-run override** — if the trigger included `→ <destination>` (e.g. `synopsis this chat → clipboard`), route there *for this run only*; defaults in `destinations.md` do not change.

**Saving in Cursor (Agent mode):**

| Destination | Action |
|-------------|--------|
| Obsidian / local / project path | `Write` to `{folder}/YYYY-MM-DD-{slug}.md`; numeric suffix on collision (`-2`, `-3`) |
| Chat only | Post full markdown in the final message |
| Clipboard | Tell user to copy the preview block (no silent assumption it was copied) |
| Notion / Drive | Use installed MCP per tool schemas; if unavailable, state once and fall back to file or chat |

After save, confirm in one sentence what was written and where.

---

## Filename convention

`YYYY-MM-DD-{kebab-case-of-primary-topic}.md`. Truncate slug to ~60 characters. Numeric suffix on collision rather than overwriting.

---

## Installing this skill

**Personal (all projects):** Copy the `chat-synopsis` folder to `~/.cursor/skills/chat-synopsis/`.

**Project (repo):** Keep at `.cursor/skills/chat-synopsis/` and commit. Optionally add `.cursor/commands/synopsis.md` in that repo for a command entry point.

**From Research-Skills:** Clone [c44-ux/Research-Skills](https://github.com/c44-ux/Research-Skills) and use `chat-synopsis/` (see [README.md](README.md)).

---

## What this skill does NOT do

- Activate without an explicit trigger.
- Save without preview.
- Inflate or flatter — specific and grounded.
- Transcribe every exchange — capture salience.
- Match against a hardcoded framework list — infer from the conversation.
- Treat "create a transcript" as a trigger (intentionally excluded).
