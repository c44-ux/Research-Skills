# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.3.0] — 2026-06-19

Multidimensional So what section. Extension by [Clare Reddan](https://github.com/c44-ux).

### Added

- **Section 5: So what / Unresolved questions** — three discipline-specific sub-sections at the end of every set of notes.
- **Design: So what?** — interaction model choices, permission models, friction vs trust tradeoffs, gaps between stated preferences and observed behaviour.
- **Product: So what?** — segmentation signals, adoption triggers, external dependencies, roadmap alignment.
- **Engineering / Dev: So what?** — integration complexity, named third-party platforms, deduplication and accuracy requirements, data volume, API feasibility.
- Calibration note: 3-5 questions per discipline, all traceable to specific participant signals (no generic padding).

---

## [0.2.0] — 2026-06-19

Quote integrity and timestamp rules. Extension by [Clare Reddan](https://github.com/c44-ux).

### Added

- **Quote policy** — verbatim-only rule: no paraphrasing, no injected context inside quote marks.
- **Timestamps** — VTT start time appended to every quote in `(HH:MM:SS)` format.
- **Context disclaimers** — plain-text *Context:* note added outside quote marks when prompt or screen state affects meaning.
- **Plain text fallback** — *(timestamp unavailable)* disclaimer added once at top of notes when source has no timestamps.
- `references/quote-policy.md` — standalone reference for the full quote rules.

---

## [0.1.0] — 2026-06-19

Initial release by [Clare Reddan](https://github.com/c44-ux).

### Added

- **Five-section output structure**: Interview details, Foundational behaviour, Concept reactions, Post-session synthesis, So what.
- **VTT reading strategy** — chunked pass system for long transcripts (1500-4000+ lines).
- **Concept comparison matrix** — H/M/L ratings, first reaction, final reaction, conditions on adoption.
- **Cross-concept synthesis table** and per-concept detail sub-sections.
- **Notable signal paragraphs** — researcher-voice interpretation, separate from tables.
- **Formatting rules** — no em dashes, no tildes, no bullet lists in note body, tables throughout.
- **Length calibration** — short session (condensed) vs full generative + concept session (full structure).
- `references/output-example.md` — worked example showing all five sections.
- `references/so-what-guide.md` — guidance on writing strong open questions per discipline.
