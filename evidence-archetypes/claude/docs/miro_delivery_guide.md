# Miro delivery guide (stakeholder board)

Use this after behaviour archetype synthesis is complete (survey Phase 3 markdown/JSON, or interview-led markdown from the agent).

Miro is **not** updated by `git push`. Claude writes to **the user’s own Miro workspace** using **Miro MCP** (after the user is signed in to Miro and the connector is enabled).

## For general users — do I need a board already?

**No.** Two supported paths:

| Path | You provide | What happens |
|------|-------------|--------------|
| **A. New board (typical first time)** | Approval when the agent asks (“create a new board?”) | Agent calls `board_create`, then adds summary + segment docs. You get a **new board link** to share. |
| **B. Existing board** | Board URL (paste from Miro) | Agent adds or updates docs on **that** board only. |

The skill does **not** host boards on GitHub, ship a default board, or include links to anyone else’s boards. **You** bring your study; **you** choose where it lands in **your** Miro.

**Agent rule:** Only use a `miro_url` that the **current user** provides in this session, or one returned from `board_create` after they approve. Do not pull board URLs from other conversations, org wikis, or prior projects.

**Requirements:** Claude with Miro MCP/connector enabled, Miro login, and permission to create boards in your team (for path A).

## Where outputs live

| Stage | Deliverable | Location |
|-------|-------------|----------|
| Survey pipeline | `*.behaviour_archetype_phase3.md`, `*.behaviour_archetype_phase3.analysis.json` | Beside the survey file |
| Optional | `*.segment_pains.json`, `*.segment_detail.md` | Beside the survey file |
| Interview / mixed | Archetype markdown in chat or user-specified path | User project |
| **Miro delivery (this guide)** | Segment cards + summary on a **Miro board** | User’s Miro workspace |

## Prerequisites

- Completed archetype content (do not publish draft or weak-signal fiction to Miro).
- **Board:** existing URL **or** explicit approval to create a new board (agent must not create silently).
- **Miro MCP** enabled in Claude; user signed in to Miro (agent may ask them to complete login if auth fails).
- Read [CONNECTORS.md](../CONNECTORS.md) before tool calls.

## Recommended board layout

Use **frames** per study. Inside each frame, use **`doc_create`** widgets (markdown documents), not tables, for segment profiles.

Suggested structure:

```text
[Frame] Study name + date + n + confidence
  ├── Doc: Evidence scope & limitations (short)
  ├── Doc: Cross-segment patterns (bullets + counts)
  ├── Doc: Segment — <label 1> (n=…)
  ├── Doc: Segment — <label 2> (n=…)
  └── Doc: Design implications (because-linked bullets)
```

### Per-segment document template

Use bullet lists only (Miro flattens markdown tables).

```markdown
# <Segment label> (n=<count>)

## How they behave
- …

## Goals / needs (evidence-gated)
- …

## Pains (with counts where survey)
- …

## Stated values / priorities
- …

## Design implications
- **Recommendation:** …
  - **Because:** …

## Source
- Survey: `<filename>` / Interviews: <n sessions>
- Generated: <date>
```

## Agent workflow (Miro delivery)

1. Confirm synthesis is final enough to share (limitations block included).
2. **Ask board preference** if not already stated:
   - “Paste an existing Miro board URL”, or
   - “Should I create a new board in your Miro account?” (wait for yes/no).
3. **Obtain a board URL:**
   - **New:** `board_create` with study name → use returned `miro_url`.
   - **Existing:** use user’s URL.
4. `context_explore` on that board — avoid duplicating content unless user asks to refresh or replace.
5. **Publish content** with `doc_create` (and `doc_update` if refreshing existing docs):
   - Summary doc first, then one doc per segment.
   - Space docs ~800–1200 px apart on x/y so they do not overlap.
   - Optional: `diagram_create` only if it adds clarity.
6. Return to the user: **board URL** + list of what was created/updated.
7. Do **not** paste respondent-level rows or PII onto the board.

## Content rules (same as skill guardrails)

- No invented quotes or names.
- Label quant vs qual sources on the board.
- Show **n** and confidence/limitations on the summary doc.
- Segment labels must match survey data or interview synthesis — never hard-coded segment names from other studies.

## If Miro MCP is unavailable

Tell the user clearly:

1. Primary outputs remain the local `.md` / `.json` files.
2. They can paste markdown into Miro manually, or enable Miro MCP and re-run Miro delivery.
3. Export PDF/slides from Miro is outside this skill.
