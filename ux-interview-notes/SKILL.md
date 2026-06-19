---
name: ux-interview-notes
description: >
  Convert user research interview transcripts (VTT or plain text) into structured,
  scannable interview notes. Use this skill whenever a user uploads a transcript file
  and asks for notes, a write-up, analysis, or a summary of a research session. Also
  triggers on phrases like "write up this interview", "turn this into notes",
  "summarise the session", or "participant notes". Works for any research study type:
  usability testing, contextual inquiry, concept testing, generative interviews.
---

# UX Interview Notes Skill

Convert raw interview transcripts into structured, researcher-ready notes that capture
participant context, workflow detail, concept reactions, and synthesis signals.

---

## Input

- A transcript file (`.vtt`, `.txt`, or pasted text)
- Optional context: study name, study guide URL, concepts being tested, participant codename

If context is not provided, extract what you can from the transcript itself (study type,
participant name/codename, product/business being discussed).

---

## Reading strategy

Transcripts can be long (1500-4000+ lines). Read in passes:

1. **First pass (lines 1-300):** Establish participant context: business type, role, tools used,
   tenure, staff count, accountant/bookkeeper setup.
2. **Middle passes:** Capture workflow detail, pain points, monitoring habits, and concept reactions.
   Read in 600-900 line chunks. Prioritise direct quotes that crystallise a key point.
3. **Final pass (last 300 lines):** Capture ranking, wrap-up, and any closing signals.

For VTT files, strip timestamps and speaker tags mentally. Focus on content.

---

## Output structure

Produce notes in this order. Use tables throughout for scannability. Never use bullet
lists where a table would work better.

### 1. Interview Details table

A single table with key metadata fields:

| Field | Detail |
|---|---|
| **Participant** | Codename or first name |
| **Study** | Study name / code |
| **Business** | Business type, size, age, location |
| **Location** | City / state |
| **Employees** | Headcount and FTE if relevant |
| **Accounting software** | Platform(s) used |
| **Expense tools** | Any dedicated expense tools, platforms, integrations |
| **Accountant / bookkeeper** | Relationship and cadence |
| **Session format** | e.g. Part 1 (foundational) + Part 2 (concept testing) |

Add or remove rows as relevant to the study.

---

### 2. Part 1: Foundational Behaviour

#### End-to-end workflow table

Three-column table: **Theme | Key points | Quotes**

Cover: how they currently manage the task being studied, who does what, tools used,
handoffs, and any workarounds. Include one direct quote per row where possible.
Quotes should be verbatim (or near-verbatim) and in quote marks.

#### Cadence table

Two-column table: **Theme | Key points**

Frequency of key activities: daily, weekly, monthly, quarterly, annual. Keep concise.

#### Pain points table

Three-column table: **Theme | Key points | Quotes**

Name each pain point clearly as a theme. Include quotes that crystallise the pain.

#### Monitoring table

Two-column table: **Theme | Key points**

How they currently track performance, spending, or the domain being studied.

#### Future / What if table

Three-column table: **Theme | Key points | Quotes**

What they'd change, what they wish existed, unprompted signals about unmet needs.

---

### 3. Part 2: Concept Reactions

*(Only include if the session involved concept or prototype testing)*

#### Quick Comparison Matrix

One row per concept. Columns:

| Concept | First reaction | Solves a real problem? (H/M/L) | Reduces thinking / micro-decisions? (H/M/L) | Trust level (H/M/L) | Would use regularly? | vs current tool | Final Reaction |

Keep each cell concise (1-2 sentences max). The "Final Reaction" column is where you add
nuance and any conditions on adoption.

After the matrix, add:
- **Participant ranking** (if given, or derived from session signals)
- **Top pick** with reasoning
- Any hard nos, with reasoning

#### Cross-concept synthesis table

Two-column table with rows for:
- Most time saved
- Most trusted / appealing
- Biggest gap vs current tool
- Would switch / pay for
- Biggest blocker (all concepts)
- Fully autonomous or human in loop

#### Concept detail notes (one sub-section per concept)

For each concept, a two-column table: **Capture | Notes**

Rows: Immediate reaction, use case(s), key concern(s), current workaround, conditions for
adoption, direct quotes. Tailor rows to what emerged in the session.

---

### 4. Post-session rapid synthesis

Two-column table (no header):

| | |
|---|---|
| **Primary problem being solved** | ... |
| **Most compelling value** | ... |
| **Biggest trust barrier** | ... |
| **Conditions for adoption** | ... |
| **Conditions for switching / expanding** | ... |

Follow the table with 2-4 **Notable signal** paragraphs. These are the researcher's voice:
observations that aren't obvious from the tables but carry design or strategy weight.
Each should be named and bolded (e.g. **Notable signal: the audit requirement drives adoption.**).

---

## Quote rules

Quotes must meet all three conditions:

1. **Verbatim only.** Reproduce the participant's exact words. Do not paraphrase, tighten,
   or clean up for readability. If the quote contains a filler word, incomplete sentence,
   or colloquialism, keep it.

2. **No injected context.** Do not insert explanatory words inside the quote (e.g. do not
   write "I just [use it to] check" if the participant said "I just check"). If the quote
   requires context to be understood on its own, add a plain-text note *before or after*
   the quote cell, not inside the quote marks.

3. **Add a timestamp.** After every quote, add the timestamp from the VTT source in
   parentheses. Use the start time of the first line of that quote.
   Format: `(00:12:34)`

   Example:
   > "I just chuck it in general ledger." (00:13:59)

   If the transcript is plain text with no timestamps, omit the timestamp and add
   *(timestamp unavailable)* once at the top of the notes as a disclaimer.

4. **Add a disclaimer when a quote needs context.** If a quote could be misread without
   knowing what question prompted it or what was on screen at the time, add a one-sentence
   plain-text note in the same table cell, outside the quote marks, prefixed with
   **Context:** For example:
   > "That would be awesome." (00:22:14)
   > *Context: said in response to the buy button concept, not the session overall.*

---

## Formatting rules

- No em dashes (use colons, commas, or restructure the sentence)
- No tildes
- No bullet lists in the body of notes (tables only, except for the Notable signals section
  which uses prose paragraphs)
- Quote marks for direct participant quotes; see Quote rules above for full requirements
- Bold key terms in table cells where it aids scanning
- Use H/M/L ratings (High/Medium/Low) in concept matrix columns, not percentages or scores
  unless the participant gave a numeric rating
- Preserve participant language and terminology (don't translate their words into product language)

---

## Length and depth calibration

- Short sessions (under 30 min, few concepts): produce a condensed version; collapse
  workflow and cadence into one table; skip empty sections
- Full generative + concept sessions (45-60 min): use the full structure above
- Expert participants with dense, fast-moving sessions: expand the Notable signals section;
  compress tables where content is thin

---

### 5. So what / Unresolved questions

This section sits at the very end of the notes. It is the bridge between raw participant
data and the work that comes next. It is not a summary; it is a set of open questions
that the notes raise but cannot answer on their own.

Produce three named sub-sections, one per discipline. Each sub-section is a two-column
table: **Question | Why it matters from this session**

Keep each question concise and answerable in principle (i.e. something a team could
actually go investigate). Do not restate findings; link questions back to specific signals
from this participant where helpful.

---

#### Design: So what?

Questions about how the experience should be shaped. Focus on: interaction model choices
the session raised, information hierarchy and layout decisions, permission and access
models, flow and trigger points, and any tension between what the participant said they
want and what they actually did.

Examples of the kind of question to ask:
- Where in the existing workflow does the new feature need to appear to require zero
  behaviour change?
- What is the minimum viable review step that preserves trust without adding friction?
- How should the UI handle the split between autonomous action and human approval?

---

#### Product: So what?

Questions about scope, prioritisation, segmentation, and go-to-market. Focus on: which
participant signals generalise to a segment vs this individual, pricing and packaging
implications, adoption triggers and timing, competitive positioning, and what would need
to be true for this participant to switch or expand.

Examples of the kind of question to ask:
- Is this use case a wedge into a new segment or an expansion of an existing one?
- What external dependency (accountant endorsement, supplier partnership, compliance
  change) would unlock adoption faster than any product change?
- Does the participant's top pick align with the concept we are prioritising, and if not,
  what does that mean for the roadmap?

---

#### Engineering / Dev: So what?

Questions about technical feasibility, integration complexity, data requirements, and
reliability constraints. Focus on: third-party integrations named by the participant,
data accuracy and deduplication requirements, volume and frequency of data flows, and
any trust conditions that imply specific technical guarantees.

Examples of the kind of question to ask:
- What does a reliable deduplication guarantee actually require technically, and how do
  we communicate that guarantee to users in a way they trust?
- What level of OCR accuracy is required before this participant would stop checking
  manually?
- Does the participant's preferred integration partner have a public API, and what does
  their data model look like?

---

**Calibration note:** Generate 3-5 questions per discipline. Fewer if the session was
short or the participant's relevance to a concept was low. Do not pad with generic
questions that could apply to any session; every question should be traceable to
something specific this participant said or did.

---

## What to avoid

- Do not editorialize in tables; save interpretation for Notable signals
- Do not paraphrase quotes into product-speak (e.g. don't change "I just chuck it all in
  general ledger" into "participant uses general ledger as a catch-all")
- Do not invent detail not in the transcript; if something is unclear, note it as
  "(not confirmed in transcript)"
- Do not reproduce the study guide questions verbatim; synthesise what was learned, not
  what was asked
