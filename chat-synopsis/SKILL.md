---
name: chat-synopsis
description: >-
  Captures a Cursor chat as a durable markdown synopsis (arc, attribution,
  standalone artifact)—not a transcript. Invoke immediately when the user says
  "synopsis this chat," "synopsis this conversation," "synopsis this research,"
  "document this analysis for next time," "capture this conversation,"
  "preserve this thinking," "preserve what we figured out," "save what we just
  figured out," @mentions chat-synopsis, or runs the synopsis or research-synopsis
  command. Research mode documents reproducible quant/qual/mixed-method playbooks.
  Do not use for generic summaries or transcript requests. Salience filter for
  reframes, decisions, and insights worth keeping.
version: 0.3.0
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

**General:**
- "synopsis this chat" / "synopsis this conversation"
- "capture this conversation"
- "preserve this thinking" / "preserve what we figured out"
- "save what we just figured out"

**Research playbook** (activates research mode — see below):
- "synopsis this research"
- "document this analysis for next time"
- "research playbook synopsis"
- "synopsis this qual analysis" / "synopsis this interview analysis"
- `@chat-synopsis research` (research mode via @mention variant)

In Cursor, @mentioning **`chat-synopsis`** (or this `SKILL.md`) always activates the workflow. Optional commands:
- **`synopsis`** — general capture (`.cursor/commands/synopsis.md`)
- **`research-synopsis`** — research playbook mode (`.cursor/commands/research-synopsis.md` or copy from [`commands/research-synopsis.md`](commands/research-synopsis.md))

**Do not activate without an explicit trigger** — but trigger phrases and @mentions count as explicit.

### If the skill does not run in a new chat

1. **Agent mode** — synopsis saving needs the Write tool; Ask/read-only mode can only preview in chat.
2. **@mention** — type `@` → Skills → **chat-synopsis** (most reliable in any project).
3. **Personal install** — skill must live at `%USERPROFILE%\.cursor\skills\chat-synopsis\` for non–design-playground repos.
4. **Reload** — after installing or updating, start a **new** Agent chat (or restart Cursor).
5. **No `disable-model-invocation`** — this skill is designed to load on trigger phrases; if an old copy still has that flag, remove it and re-copy the folder.

---

## Modes

| Mode | When | Output focus |
|------|------|----------------|
| **General** | Default triggers | AAA synopsis — thinking, decisions, insights |
| **Research playbook** | Research triggers or `research-synopsis` command | AAA + reproducibility — definitions, inputs, rerun checklist, wave diff |

Research mode still uses the salience filter. It **adds** procedural capture; it does not become a transcript.

### Research data type

Infer from the conversation (or ask once if unclear):

| `research_type` | Use when |
|-----------------|----------|
| `survey-analysis` | Tabular exports, cohort metrics, segmentation scripts |
| `qual-analysis` | Interviews, transcripts, thematic synthesis, quotes, codebooks |
| `mixed-methods` | Explicit triangulation of qual + quant in one study |

Load [references/examples-research.md](references/examples-research.md) for quant and qual worked examples. See [references/research-playbook.md](references/research-playbook.md) for integration with other Research-Skills.

---

## Procedure

### Step 1 — Surface detection

Detect what the current Cursor session can do:

| Surface | When | Destinations |
|--------|------|----------------|
| **Agent mode** | Write tool and shell available | Obsidian (vault path), project or local file (`Write`), research playbooks folder, Notion/Drive (MCP if installed), show in chat + user copies |
| **Ask / read-only** | No file writes | Show full markdown in chat; offer clipboard copy; Notion/Drive only if MCP works without writes |

Surface awareness only affects which destinations are *offered*. The artifact format (markdown) is the same everywhere.

**Default `source` in frontmatter:** `Cursor`.

**Research mode save path:** If `research_playbook_folder` is set in [references/destinations.md](references/destinations.md), save research playbooks there; otherwise use the default destination with tag `research-playbook`.

### Step 2 — First-run wizard (if no destination configured)

Read [references/destinations.md](references/destinations.md). If **Configured Defaults** is empty or still has placeholder values, run the setup wizard inline before continuing:

> "Looks like this is your first time running chat-synopsis. Where should your synopses live? You'll only set this once.
>
> 1. **Obsidian** — paste the absolute path to the folder in your vault where synopses go (e.g. `C:\Users\you\Documents\Obsidian\MyVault\Synopses` or `/Users/you/Documents/Obsidian/MyVault/Synopses`).
> 2. **Notion** — paste a Notion database URL or share-link; extract the database ID for MCP.
> 3. **Google Drive** — paste a folder URL or ID (Drive MCP if installed).
> 4. **Local file** — synopses save under `~/chat-synopses/` (Windows: `%USERPROFILE%\chat-synopses\`).
> 5. **Project folder** — synopses save under `.cursor/chat-synopses/` in the workspace (good for team repos).
> 6. **Research playbooks** — study rerun docs under `.cursor/research-playbooks/` (recommended for quant/qual analysis wrap-up).
> 7. **Skip for now** — use chat output only this run; configure later in `references/destinations.md`."

When the user picks a destination, update **Configured Defaults** in `references/destinations.md` (path / database ID / folder ID + destination type). If they chose research playbooks, also set `research_playbook_folder`. Confirm in one sentence where the default was saved.

Then continue with Step 3.

### Step 3 — Salience check

Before generating the synopsis, scan the conversation for **anchors**:

**General anchors:**
- A reframe ("I was thinking about this wrong; the real question is X")
- A decision (a choice made between alternatives)
- An insight (something the user articulated that wasn't visible at the start)
- A breakthrough (a stuck point that resolved)
- A useful artifact (code shipped, plan written, document drafted)
- A notable framing shift (the topic itself changed shape)

**Research anchors** (when research mode is active — also scan for these):

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

List the anchors found, briefly, before rendering. If **at least one** general or research anchor exists, proceed. A single anchor in a long thread is enough for a proportionally short artifact.

**Research mode exception:** If zero *insight* anchors but several *procedure* anchors (definitions, filters, rerun steps), proceed — valid research wrap-up.

If **zero** anchors exist (e.g. single-topic lookup, "how do I install foo?"), say so honestly and ask before proceeding:

> "This looks like a [single-topic lookup / debugging recap / no-pivot Q&A] — I didn't find a reframe, decision, or insight that would otherwise be lost. A synopsis here would mostly restate what's already visible in the chat. Want me to run it anyway?"

Only generate after explicit confirmation in the zero-anchor case.

### Step 4 — Privacy pass

Before rendering, scan the conversation for high-risk patterns and replace matches with `[REDACTED]` in the synopsis output:

- API keys: `sk-[A-Za-z0-9]{20,}`, `ghp_[A-Za-z0-9]{20,}`, `xoxb-…`, `xoxp-…`, AWS-style `AKIA[A-Z0-9]{16}`, GCP-style `AIza[A-Za-z0-9_-]{35}`.
- JWTs: three base64 segments separated by dots where the first decodes to JSON containing `"alg"`.
- Lines whose left-hand label matches `password|secret|api_key|token|access_key|private_key` followed by `:` or `=` and a string value.

**Research mode — also redact or anonymise:**
- Participant real names, business names, ABNs, emails, phone numbers (use synthetic labels: Participant A, Business B).
- Verbatim quotes that could identify a participant when the study requires anonymity.

Best-effort only — see [references/privacy.md](references/privacy.md). Mandatory preview (Step 6) is the user's last line of defense.

### Step 5 — Render under AAA discipline

Apply Arc / Attribution / Artifact discipline. See [references/examples.md](references/examples.md) for general pairs; [references/examples-research.md](references/examples-research.md) for research quant and qual pairs.

**Arc discipline.** In **What Happened**, trace the through-line: start → shift → land. Do not produce a chronological event list. If there was no arc, say so explicitly ("Single-topic execution session, no significant pivots") rather than inflating one.

**Attribution discipline.** Every sentence describing action names the actor.

- **User verbs:** *directed, asked, decided, caught, reframed, pushed back, named, surfaced, clarified, refined, chose, rejected, noticed, vetoed, recognized, distinguished.*
- **Assistant verbs:** *drafted, proposed, scaffolded, explained, generated, suggested, summarized, restated, investigated, recommended.*
- **Forbidden:** "we" for one-party action; passive voice that hides the actor; narrating the assistant's work as the user's accomplishment.
- **Joint credit:** "User proposed X; assistant refined it into Y; user chose Y."

**Artifact discipline.** The output must read coherently to someone who wasn't in the conversation. No "earlier in this chat" or "as I said."

#### Prior playbook (research mode only)

If the conversation or workspace references a prior playbook for the same `study_id`, read it if accessible. Populate **What changed vs last wave** with metric, scope, or method diffs. Set `prior_playbook` in frontmatter to the prior filename (not a chat-relative path).

### Output structure — general mode

Use when research mode is **not** active. **Omit empty sections.**

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

### Output structure — research playbook mode

Use when research mode is active. **Omit empty sections.** Include all AAA sections plus research sections below.

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
  - chat-synopsis
  - research-playbook
  - [study-id]
---

## Synopsis
[2–4 sentences. Study scope, what was analysed, what was produced.]

## What Happened
[Arc-traced narrative. Through-line, not event list. Attribution-disciplined throughout.]

## Research decisions (reproducibility)
- **[Category]:** [Precise rule — metric definition, cohort filter, theme rule, quote policy, etc.]

## Inputs & artefacts
| Item | Location | Notes |
|------|----------|-------|
| [Source data / transcripts / export] | [path or URL] | [date range, n, wave] |
| [Scripts / skills run] | [path] | [optional] |
| [Outputs] | [path] | [HTML, Miro, Confluence, .md synthesis] |

## Method steps (rerun checklist)

### Quant rerun (include when research_type is survey-analysis or mixed-methods)
1. [Export / ingest step with filename convention]
2. [Validate n and wave labels before any % table]
3. [Recompute key metrics with locked definitions]
4. [Regenerate breakdowns; compare to prior_playbook if present]
5. [Update deliverables; footnote denominator changes]

### Qual rerun (include when research_type is qual-analysis or mixed-methods)
1. [Ingest new transcripts / notes — naming convention, anonymisation]
2. [Confirm participant scope and exclusion rules]
3. [Apply codebook / theme structure — note merges or splits]
4. [Synthesise themes; real quotes only; mark saturation gaps]
5. [Route deliverables — Confluence, Miro, local synthesis file]
6. [Triangulation step if mixing with quant — keep claims separate unless user directed merge]

## Decisions Made / Insights / Reframes
- [Anchor]: [Context]

## What changed vs last wave
- [Only when prior_playbook exists — diffs in definitions, n, metrics, themes, or scope]

## Quotable Moments
> "[User or participant language — anonymised in qual work]"

## Open Threads
- [Unresolved benchmarks, saturation gaps, external data needed]

## Next wave playbook
- [ ] [Concrete rerun trigger — e.g. "When Wave 4 Langfuse export arrives…"]
- [ ] [Revalidate locked definitions from Research decisions]
- [ ] [Link updated deliverable back to this playbook]
```

**Section guidance by research type:**

| Section | survey-analysis | qual-analysis | mixed-methods |
|---------|-----------------|---------------|---------------|
| Research decisions | Metric + denominator rules | Theme, quote, scope rules | Both |
| Method steps — Quant rerun | Required | Omit unless quant leg exists | Required |
| Method steps — Qual rerun | Omit unless qual leg exists | Required | Required |
| What changed vs last wave | Metric/cohort diffs | Theme/participant diffs | Both |

### Step 6 — Mandatory preview, then save

Show the rendered markdown to the user. Wait for one of:

- **Accept** — save at the configured destination (or per-run override).
- **Edit** — apply changes, re-preview.
- **Cancel** — discard and end.
- **Per-run override** — if the trigger included `→ <destination>` (e.g. `synopsis this research → project`), route there *for this run only*; defaults in `destinations.md` do not change.

**Saving in Cursor (Agent mode):**

| Destination | Action |
|-------------|--------|
| Obsidian / local / project path | `Write` to `{folder}/YYYY-MM-DD-{slug}.md`; numeric suffix on collision (`-2`, `-3`) |
| Research playbooks | `Write` to `{research_playbook_folder}/YYYY-MM-DD-{study-id}-{slug}.md` |
| Chat only | Post full markdown in the final message |
| Clipboard | Tell user to copy the preview block (no silent assumption it was copied) |
| Notion / Drive | Use installed MCP per tool schemas; if unavailable, state once and fall back to file or chat |

After save, confirm in one sentence what was written and where.

---

## Filename convention

**General:** `YYYY-MM-DD-{kebab-case-of-primary-topic}.md`. Truncate slug to ~60 characters.

**Research playbook:** `YYYY-MM-DD-{study-id}-{topic-slug}.md` (e.g. `2026-05-22-cxr004-high-volume-span-analysis.md`). Add wave suffix when useful: `…-wave4.md`.

Numeric suffix on collision rather than overwriting.

---

## Installing this skill

**Personal (all projects):** Copy the `chat-synopsis` folder to `~/.cursor/skills/chat-synopsis/`.

**Project (repo):** Keep at `.cursor/skills/chat-synopsis/` and commit. Optionally add command files from [`commands/`](commands/).

**From Research-Skills:** Clone [c44-ux/Research-Skills](https://github.com/c44-ux/Research-Skills) and use `chat-synopsis/` (see [README.md](README.md)).

**Research workflow ritual:** When analysis is complete → run **`research-synopsis`** or say **"synopsis this research"** → review playbook → Accept save → close chat.

---

## What this skill does NOT do

- Activate without an explicit trigger.
- Save without preview.
- Inflate or flatter — specific and grounded.
- Transcribe every exchange — capture salience.
- Match against a hardcoded framework list — infer from the conversation.
- Treat "create a transcript" as a trigger (intentionally excluded).
- Invent participant quotes or merge qual/quant claims without user direction (research mode).
