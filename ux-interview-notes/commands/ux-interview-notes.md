# ux-interview-notes command

Copy this into `.claude/commands/ux-interview-notes.md` in your project repo to use as a slash command in Claude.ai.

---

```markdown
Write up structured interview notes from the uploaded transcript.

Context (fill in before running):
- Study: [study name / code]
- Participant: [codename or first name]
- Concepts tested: [list concepts, or "none — generative session only"]
- Study guide: [URL or "not available"]

Produce the full five-section format:
1. Interview details
2. Foundational behaviour (workflow, cadence, pain points, monitoring, future wants)
3. Concept reactions (matrix + per-concept detail) — skip if generative only
4. Post-session synthesis (rapid summary + Notable signals)
5. So what / Unresolved questions (Design, Product, Engineering)

Quote rules:
- Verbatim only — no paraphrasing, no injected context inside quote marks
- Timestamp every quote from the VTT source: (HH:MM:SS)
- Add a Context: note outside quote marks if meaning depends on what was on screen

Formatting:
- Tables throughout (no bullet lists in note body)
- No em dashes, no tildes
- H/M/L ratings in concept matrix
- Preserve participant language exactly
```
