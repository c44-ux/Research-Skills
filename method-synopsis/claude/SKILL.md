---
name: method-synopsis
description: >-
  Captures a Claude session as a durable method synopsis for reproducibility
  (arc, attribution, standalone artifact)—not a transcript. Invoke when the
  user says "method synopsis," "method synopsis this research," "method synopsis
  this qual analysis," "document this method for next time," "preserve what we
  figured out," or runs /method-synopsis. Reproducibility mode documents
  rerunnable quant/qual/mixed-method playbooks. Do not use for generic summaries
  or transcript requests.
---

# Method Synopsis (Claude)

Capture a Claude session as a durable **method synopsis** to document what was done, decided, and produced so the work can be reproduced. Three things get preserved:

1. **Arc** — how the session unfolded: where it started, where it shifted, where it landed. Not a chronological list of events.
2. **Attribution** — who contributed what. The user's contributions and Claude's contributions are named, not collapsed into "we."
3. **Artifact** — a self-contained markdown file that stands alone, routed to the user's configured destination (Obsidian vault folder, local path, project folder, or chat output).

This is a salience filter, not a transcript. Capture the moments that produced new thinking — reframes, decisions, insights, and **locked method choices** — not every exchange.

**Upstream:** [Research-Skills/method-synopsis/claude/](https://github.com/c44-ux/Research-Skills/tree/main/method-synopsis/claude). **Cursor variant:** [method-synopsis/cursor/](../cursor/).

---

## Triggers

Activate **only** on these natural-language phrases (or a per-run override of the form `<trigger> → <destination>`):

**General:**
- "method synopsis" / "method synopsis this session"
- "document this method"
- "preserve what we figured out" / "save what we figured out"

**Reproducibility mode** (activates method playbook output):
- "method synopsis this research"
- "document this method for next time"
- "method synopsis this qual analysis" / "method synopsis this interview analysis"
- `/method-synopsis` (if command installed — see [commands/method-synopsis.md](commands/method-synopsis.md))

**Do not activate without an explicit trigger.**

### If the skill does not run in a new chat

1. **Claude Desktop / CoWork** — upload the skill zip (see [README.md](README.md)); toggle it **on** in Customize → Skills.
2. **Claude Code** — skill must live in `.claude/skills/method-synopsis/` (project) or `~/.claude/skills/method-synopsis/` (personal).
3. **Reload** — start a new chat after installing or updating the skill.

---

## Modes

| Mode | When | Output focus |
|------|------|----------------|
| **General** | Default triggers | AAA synopsis — thinking, decisions, insights |
| **Reproducibility** | Research/method triggers or `/method-synopsis` | AAA + rerunnable method — definitions, inputs, rerun checklist, wave diff |

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

Detect what the current Claude session can do:

| Surface | When | Destinations |
|--------|------|----------------|
| **Claude Code** | Bash / file tools available | Obsidian (vault path), project or local file, method playbooks folder, show in chat |
| **Claude Desktop / CoWork** | Code execution enabled | Same as above via file write; otherwise chat output + user copies |
| **Chat-only** | No file write capability | Show full markdown in chat; offer clipboard copy |

Surface awareness only affects which destinations are *offered*. The artifact format (markdown) is the same everywhere.

**Default `source` in frontmatter:** `Claude`.

**Reproducibility mode save path:** If `method_playbook_folder` is set in [references/destinations.md](references/destinations.md), save method playbooks there; otherwise use the default destination with tag `method-playbook`.

### Step 2 — First-run wizard (if no destination configured)

Read [references/destinations.md](references/destinations.md). If **Configured Defaults** is empty or still has placeholder values, run the setup wizard inline before continuing.

Claude has no structured AskQuestion tool. Present **numbered options in one message**, then **stop and wait** for the user's reply:

> Looks like this is your first time running method-synopsis. Where should your method synopses live? You'll only set this once.
>
> 1. **Obsidian** — paste the absolute path to the folder in your vault (e.g. `C:\Users\you\Documents\Obsidian\MyVault\Method-Synopses`).
> 2. **Local file** — synopses save under `~/method-synopses/` (Windows: `%USERPROFILE%\method-synopses\`).
> 3. **Project folder** — synopses save under `.claude/method-synopses/` in the workspace (good for team repos).
> 4. **Method playbooks** — rerunnable study docs under `.claude/method-playbooks/` (recommended for quant/qual analysis wrap-up).
> 5. **Skip for now** — use chat output only this run; configure later in `references/destinations.md`.

When the user picks a destination:
- **Claude Code:** update **Configured Defaults** in `references/destinations.md` via file edit.
- **Claude Desktop:** confirm the path in chat; user may need to edit `destinations.md` manually or tell Claude the path each run.

Confirm in one sentence where the default was saved. Then continue with Step 3.

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
| **Tool / skill chain** | "Ran `segment_pains.py` → archetype cards" | "Used evidence-archetypes qual path → Miro board" |
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

If a prior playbook for the same `study_id` exists, read it if accessible (typically in `.claude/method-playbooks/`). Populate **What changed vs last wave**. Set `prior_playbook` in frontmatter to the prior filename.

### Output structure — general mode

**Omit empty sections.**

```markdown
---
title: "[Primary Topic]"
date: YYYY-MM-DD
source: Claude
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

### Output structure — reproducibility mode

Use when reproducibility mode is active. **Omit empty sections.**

```markdown
---
title: "[Study ID] — [Topic]"
date: YYYY-MM-DD
source: Claude
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

### Step 6 — Mandatory preview, then save

Show rendered markdown; wait for Accept, Edit, or Cancel.

| Destination | Action |
|-------------|--------|
| Obsidian / local / project path | Write `{folder}/YYYY-MM-DD-{slug}.md` (Claude Code: bash; Desktop: file tool if available) |
| Method playbooks | Write `{method_playbook_folder}/YYYY-MM-DD-{study-id}-{slug}.md` |
| Chat only / Clipboard | Full markdown in chat; user copies manually |

**Claude Code save example:**

```bash
mkdir -p .claude/method-playbooks
# Write file contents to .claude/method-playbooks/YYYY-MM-DD-study-id-topic.md
```

---

## Filename convention

**General:** `YYYY-MM-DD-{kebab-case-topic}.md`

**Method playbook:** `YYYY-MM-DD-{study-id}-{topic-slug}.md` (optional wave suffix: `…-wave4.md`)

---

## Installing this skill

**Claude Desktop / CoWork:** Zip this folder and upload via Customize → Skills. See [README.md](README.md).

**Claude Code (project):** `.claude/skills/method-synopsis/` + optional [commands/method-synopsis.md](commands/method-synopsis.md) copied to `.claude/commands/`.

**Claude Code (personal):** Copy to `~/.claude/skills/method-synopsis/`.

**From Research-Skills:** Clone [c44-ux/Research-Skills](https://github.com/c44-ux/Research-Skills) and copy `method-synopsis/claude/` to `.claude/skills/method-synopsis/`. **Cursor variant:** `method-synopsis/cursor/`.

**Workflow ritual:** When analysis is complete → **`/method-synopsis`** or **"method synopsis this research"** → preview → Accept → close session.

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

Adapted from **[chat-synopsis](https://github.com/vanessachang-dev/chat-synopsis)** by Vanessa Chang (MIT). Extended for **reproducible research methods** by Clare Reddan (v0.4.0 Cursor). Claude port v1.0.0 — same AAA discipline and reproducibility mode; adapted for Claude Code, Desktop, and CoWork file-save surfaces.
