# ux-interview-notes (Claude.ai skill)

**UX interview notes** — structured, researcher-ready notes from raw interview transcripts for **reproducibility**: participant context, workflow detail, concept reactions, synthesis signals, and multidimensional open questions — not a transcript summary.

Documents what a participant said, how they said it, and what it means for design, product, and engineering — so the next round does not start from scratch.

Part of [Research-Skills](https://github.com/c44-ux/Research-Skills).

---

## Install

**From this repo (recommended):**

Go to **Claude.ai → Settings → Skills → Install from file**, then upload `ux-interview-notes.skill`.

Or clone and install manually:

```bash
git clone https://github.com/c44-ux/Research-Skills.git
```

Upload `Research-Skills/ux-interview-notes/` as a skill folder, or package the `.skill` file yourself (see [Layout](#layout)).

**To package locally:**

```bash
cd Research-Skills
zip -r ux-interview-notes.skill ux-interview-notes/
```

Then upload the `.skill` file to Claude.ai.

---

## Use

**In any Claude.ai conversation where a transcript file is uploaded.**

**General triggers:**
- Upload a `.vtt` or `.txt` transcript and ask: `write up these notes`
- `turn this into interview notes` · `participant notes` · `summarise this session`
- `now [participant name]` (when continuing a series of interviews)

**With study context:**
- `write up notes for [Participant], [Study name], concepts: [list]`
- `use the CXR-EP05 study guide at [URL] for context`

**Supported session types:**

| Type | When to use |
|------|-------------|
| **Generative / contextual inquiry** | Foundational behaviour, pain points, workflow mapping |
| **Concept testing** | Prototype or feature reactions, ranking, adoption signals |
| **Usability testing** | Task performance, friction points, comprehension |
| **Mixed** | Both foundational and concept sections in one session |

### Not triggering?

| Symptom | Fix |
|---------|-----|
| Skill ignores the transcript | Explicitly say "write up interview notes" in the message |
| Missing concept reactions section | Confirm the session included prototype/concept testing |
| Quotes without timestamps | Source file may be plain text; skill adds a disclaimer automatically |
| Notes too brief | Specify "full notes" or "detailed write-up" |

---

## Output structure

Each set of notes contains five sections:

1. **Interview details** — participant metadata, tools, business context
2. **Foundational behaviour** — workflow, cadence, pain points, monitoring, future wants
3. **Concept reactions** — comparison matrix, cross-concept synthesis, per-concept detail *(concept sessions only)*
4. **Post-session synthesis** — rapid summary table + Notable signal paragraphs
5. **So what / Unresolved questions** — open questions by discipline (Design, Product, Engineering)

---

## Quote policy

All quotes are:
- **Verbatim** — no paraphrasing, no cleanup, no injected context inside quote marks
- **Timestamped** — VTT start time appended in `(HH:MM:SS)` format
- **Contextualised where needed** — a plain-text *Context:* note is added outside the quote when the prompt or screen state affects meaning

See [references/quote-policy.md](references/quote-policy.md) for full rules.

---

## Layout

```text
ux-interview-notes/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── commands/
│   └── ux-interview-notes.md
└── references/
    ├── quote-policy.md
    ├── output-example.md
    └── so-what-guide.md
```

---

## Credits

Created by [Clare Reddan](https://github.com/c44-ux) for Claude.ai.

- **v0.1.0** — initial skill: five-section structure, VTT reading strategy, concept matrix
- **v0.2.0** — quote policy: verbatim-only, timestamps, context disclaimers
- **v0.3.0** — multidimensional So what section: Design, Product, Engineering open questions

Full change list: [CHANGELOG.md](CHANGELOG.md).
