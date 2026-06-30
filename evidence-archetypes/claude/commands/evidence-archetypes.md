# evidence-archetypes command

Copy this into `.claude/commands/evidence-archetypes.md` in your project repo to use as a slash command in Claude Code or CoWork.

---

```markdown
Build evidence-based behaviour archetypes from the study materials I provide.

Instructions:
1. Read and follow `.claude/skills/evidence-archetypes/SKILL.md` end to end.
2. Read required docs first:
   - `docs/Evidence based behaviour_archetype_principles.md`
   - `docs/behaviour_archetype_methodology_guide.md`
3. Determine input path:
   - **Qual** — transcripts/notes: synthesise in markdown; no Phase 3 scripts.
   - **Quant** — survey `.xlsx`/`.csv`: run Phase 3 scripts after column mapping (requires cs-ux-personas).
   - **Mixed** — keep qual and quant claims separate unless I explicitly triangulate.
4. Output markdown with: Evidence scope, Observed patterns, Behaviour archetype profile, Design implications, Limitations and confidence.
5. If I ask for Miro delivery: read `docs/miro_delivery_guide.md` and CONNECTORS.md; ask existing vs new board; use bullet lists in Miro docs only.
6. Never invent quotes, names, or segment labels — use data only.

Study context (fill in before running):
- Study ID / name: [e.g. CXR004]
- Input type: [qual | quant | mixed]
- Files: [paths or upload]
- Miro: [none | paste board URL | create new board]
```
