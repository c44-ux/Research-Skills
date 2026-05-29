---
name: method-synopsis
description: >-
  Captures a Cursor session as a durable method synopsis for reproducibility
  (arc, attribution, standalone artifact)—not a transcript. Invoke immediately when
  the user says "method synopsis," "method synopsis this research," "method synopsis
  this qual analysis," "document this method for next time," "preserve what we
  figured out," @mentions method-synopsis, or runs the method-synopsis command.
  Reproducibility mode documents rerunnable quant/qual/mixed-method playbooks.
  Do not use for generic summaries or transcript requests. Salience filter for
  reframes, decisions, and insights worth keeping.
version: 0.4.0
---

# Method Synopsis

Capture a Cursor session as a durable **method synopsis** — documentation of what was done, decided, and produced so the work can be reproduced. Three things get preserved:

1. **Arc** — how the session unfolded: where it started, where it shifted, where it landed. Not a chronological list of events.
2. **Attribution** — who contributed what. The user's contributions and the assistant's contributions are named, not collapsed into "we."
3. **Artifact** — a self-contained markdown file that stands alone, routed to the user's configured destination (Obsidian vault folder, local path, Notion, Drive, or chat output).

This is a salience filter, not a transcript. Capture the moments that produced new thinking — reframes, decisions, insights, and **locked method choices** — not every exchange.

---

## Triggers

Activate **only** on these natural-language phrases (or a per-run override of the form `<trigger> → <destination>`):

**General:**
- "method synopsis" / "method synopsis this session"
- "document this method"
- "preserve what we figured out" / "save what we figured out"

**Reproducibility mode** (activates method playbook output — see below):
- "method synopsis this research"
- "document this method for next time"
- "method synopsis this qual analysis" / "method synopsis this interview analysis"
- `@method-synopsis research` (reproducibility mode via @mention variant)

In Cursor, @mentioning **`method-synopsis`** (or this `SKILL.md`) always activates the workflow. Optional command:
- **`method-synopsis`** — reproducibility mode (`.cursor/commands/method-synopsis.md` or copy from [`commands/method-synopsis.md`](commands/method-synopsis.md))

**Do not activate without an explicit trigger** — but trigger phrases and @mentions count as explicit.

### If the skill does not run in a new chat

1. **Agent mode** — saving needs the Write tool; Ask/read-only mode can only preview in chat.
2. **@mention** — type `@` → Skills → **method-synopsis** (most reliable in any project).
3. **Personal install** — skill must live at `%USERPROFILE%\.cursor\skills\method-synopsis\`.
4. **Reload** — after installing or updating, start a **new** Agent chat (or restart Cursor).
5. **No `disable-model-invocation`** — this skill is designed to load on trigger phrases; if an old copy still has that flag, remove it and re-copy the folder.

---

## Modes

| Mode | When | Output focus |
|------|------|----------------|
| **General** | Default triggers | AAA synopsis — thinking, decisions, insights |
| **Reproducibility** | Research/method triggers or `method-synopsis` command | AAA + rerunnable method — definitions, inputs, rerun checklist, wave diff |

Reproducibility mode still uses the salience filter. It **adds** procedural capture; it does not become a transcript.

### Research data type

Infer from the conversation (or ask once if unclear):

| `research_type` | Use when |
|-----------------|----------|
| `survey-analysis` | Tabular exports, cohort metrics, segmentation scripts |
| `qual-analysis` | Interviews, transcripts, thematic synthesis, quotes, codebooks |
| `mixed-methods` | Explicit triangulation of qual + quant in one study |

Load [references/examples-research.md](references/examples-research.md) for quant and qual worked examples. See [references/method-playbook.md](references/method-playbook.md) for integration with other Research-Skills.

---

## Procedure

### Step 1 — Surface detection

Detect what the current Cursor session can do:

| Surface | When | Destinations |
|--------|------|----------------|
| **Agent mode** | Write tool and shell available | Obsidian (vault path), project or local file (`Write`), method playbooks folder, Notion/Drive (MCP if installed), show in chat + user copies |
| **Ask / read-only** | No file writes | Show full markdown in chat; offer clipboard copy; Notion/Drive only if MCP works without writes |

Surface awareness only affects which destinations are *offered*. The artifact format (markdown) is the same everywhere.

**Default `source` in frontmatter:** `Cursor`.

**Reproducibility mode save path:** If `method_playbook_folder` is set in [references/destinations.md](references/destinations.md), save method playbooks there; otherwise use the default destination with tag `method-playbook`.

### Step 2 — First-run wizard (if no destination configured)

Read [references/destinations.md](references/destinations.md). If **Configured Defaults** is empty or still has placeholder values, run the setup wizard inline before continuing:

> "Looks like this is your first time running method-synopsis. Where should your method synopses live? You'll only set this once.
>
> 1. **Obsidian** — paste the absolute path to the folder in your vault (e.g. `C:\Users\you\Documents\Obsidian\MyVault\Method-Synopses`).
> 2. **Notion** — paste a Notion database URL or share-link; extract the database ID for MCP.
> 3. **Google Drive** — paste a folder URL or ID (Drive MCP if installed).
> 4. **Local file** — synopses save under `~/method-synopses/` (Windows: `%USERPROFILE%\method-synopses\`).
> 5. **Project folder** — synopses save under `.cursor/method-synopses/` in the workspace (good for team repos).
> 6. **Method playbooks** — rerunnable study docs under `.cursor/method-playbooks/` (recommended for quant/qual analysis wrap-up).
> 7. **Skip for now** — use chat output only this run; configure later in `references/destinations.md`."

When the user picks a destination, update **Configured Defaults** in `references/destinations.md`. If they chose method playbooks, also set `method_playbook_folder`. Confirm in one sentence where the default was saved.

Then continue with Step 3.

### Step 3 — Salience check

Before generating the synopsis, scan the conversation for **anchors**:

**General anchors:**
- A reframe, decision, insight, breakthrough, useful artifact, or framing shift

**Method / research anchors** (when reproducibility mode is active — also scan for these):

| Anchor type | Quant example | Qual example |
|-------------|---------------|--------------|
| **Definition locked** | "Span = calendar days from timestamp, not sessions" | "Theme = behaviour pattern across ≥3 participants" |
| **Denominator / scope** | "Percentages use n=3,211 chat-active only" | "Synthesis covers n=12 interviews, Wave 3 SMEs only" |
| **Filter / cohort rule** | "High-volume = 5+ queries" | "Exclude pilot participants; include only completed 45-min sessions" |
| **Tool / skill chain** | "Ran `segment_pains.py` → archetype cards" | "Used evidence-based-behaviour-archetype-creation qual path → Miro board" |
| **Quote / evidence rule** | "Counts from workbook column X only" | "Real quotes only; anonymise business names; no invented 'representative' quotes" |
| **Codebook / theme decision** | — | "Merged 'payroll stress' and 'payday anxiety' into single theme" |
| **Deliverable routing** | "Tables in chat only; no HTML update" | "Themes to Confluence; quotes in appendix; Miro for stakeholder readout" |
| **Known gap** | "W3 30K benchmark still external" | "Saturation unclear for enterprise segment — need 3 more interviews" |

List the anchors found, briefly, before rendering. If **at least one** general or method anchor exists, proceed.

**Reproducibility mode exception:** If zero *insight* anchors but several *procedure* anchors (definitions, filters, rerun steps), proceed — valid method wrap-up.

If **zero** anchors exist, say so honestly and ask before proceeding. Only generate after explicit confirmation in the zero-anchor case.

### Step 4 — Privacy pass

Before rendering, scan for high-risk patterns and replace with `[REDACTED]`. **Reproducibility mode — also anonymise** participant/business identifiers in qual work. See [references/privacy.md](references/privacy.md).

### Step 5 — Render under AAA discipline

Apply Arc / Attribution / Artifact discipline. See [references/examples.md](references/examples.md) and [references/examples-research.md](references/examples-research.md).

#### Prior playbook (reproducibility mode only)

If a prior playbook for the same `study_id` exists, read it if accessible. Populate **What changed vs last wave**. Set `prior_playbook` in frontmatter to the prior filename.

### Output structure — general mode

**Omit empty sections.**

```markdown
---
title: "[Primary Topic]"
date: YYYY-MM-DD
source: Cursor
project: [if applicable]
tags:
  - method-synopsis
  - [topic-tags]
---

## Synopsis
## What Happened
## Decisions Made / Insights / Reframes
## Quotable Moments
## Open Threads
## Next Steps
```

(Section content unchanged from AAA discipline — see v0.3.0 examples.)

### Output structure — reproducibility mode

Use when reproducibility mode is active. **Omit empty sections.**

```markdown
---
title: "[Study ID] — [Topic]"
date: YYYY-MM-DD
source: Cursor
study_id: CXR###
wave: [Wave 3 | Round 2 | null]
research_type: survey-analysis | qual-analysis | mixed-methods
skills_used:
  - [skill-name if used]
data_sources:
  - path: "[file or folder path]"
    date_range: "[if applicable]"
    n: [sample size or interview count]
prior_playbook: [YYYY-MM-DD-study-id-topic.md or null]
tags:
  - method-synopsis
  - method-playbook
  - [study-id]
---

## Synopsis
## What Happened
## Research decisions (reproducibility)
## Inputs & artefacts
## Method steps (rerun checklist)
### Quant rerun
### Qual rerun
## Decisions Made / Insights / Reframes
## What changed vs last wave
## Quotable Moments
## Open Threads
## Next wave playbook
```

(Full section guidance unchanged — quant/qual/mixed table applies.)

### Step 6 — Mandatory preview, then save

Show rendered markdown; wait for Accept, Edit, or Cancel.

| Destination | Action |
|-------------|--------|
| Obsidian / local / project path | `Write` to `{folder}/YYYY-MM-DD-{slug}.md` |
| Method playbooks | `Write` to `{method_playbook_folder}/YYYY-MM-DD-{study-id}-{slug}.md` |
| Chat only / Clipboard / Notion / Drive | As in v0.3.0 |

---

## Filename convention

**General:** `YYYY-MM-DD-{kebab-case-topic}.md`

**Method playbook:** `YYYY-MM-DD-{study-id}-{topic-slug}.md` (optional wave suffix: `…-wave4.md`)

---

## Installing this skill

**Personal:** Copy `method-synopsis` to `~/.cursor/skills/method-synopsis/`.

**Project:** `.cursor/skills/method-synopsis/` + optional [`commands/method-synopsis.md`](commands/method-synopsis.md).

**From Research-Skills:** Clone [c44-ux/Research-Skills](https://github.com/c44-ux/Research-Skills) and use `method-synopsis/`.

**Workflow ritual:** When analysis is complete → **`method-synopsis`** or **"method synopsis this research"** → preview → Accept → close session.

---

## What this skill does NOT do

- Activate without an explicit trigger.
- Save without preview.
- Inflate or flatter — specific and grounded.
- Transcribe every exchange — capture salience.
- Treat "create a transcript" as a trigger.
- Invent participant quotes or merge qual/quant claims without user direction.

---

## Lineage

Adapted from **[chat-synopsis](https://github.com/vanessachang-dev/chat-synopsis)** by Vanessa Chang (MIT). Renamed and extended for **reproducible research methods** by Clare Reddan (v0.4.0).
