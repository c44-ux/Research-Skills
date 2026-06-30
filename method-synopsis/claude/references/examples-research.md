# Examples — Research playbook (quant & qual)

Load-bearing positive/negative pairs for **research mode**. Use alongside [examples.md](examples.md) (general AAA).

---

## When to use research mode

**Good trigger timing:**
> Analysis session complete; user says "method synopsis this research" before closing the session.

**Bad timing:**
> Mid-exploration, no decisions locked yet — playbook would be premature.

---

## Quant — Research decisions

**Bad (vague, not rerunnable):**
> We used timestamps for the analysis and filtered high-volume users.

**Good (precise rules):**
> - **Span metric:** Calendar days between min and max `timestamp` per business (not session count).
> - **High-volume cohort:** Businesses with ≥5 queries in extract.
> - **Denominator:** All percentages use n=3,211 chat-active businesses unless labelled HV-only (n=218).

---

## Quant — Method steps (rerun checklist)

**Bad (findings restated, no procedure):**
> 1. Look at the spreadsheet.
> 2. Build charts.
> 3. Write up results.

**Good (ordered, rerunnable):**
> 1. Export Langfuse extract for new date range → save as `{study-id}-langfuse-{YYYYMMDD}.xlsx` beside prior wave.
> 2. Confirm n and wave labels in workbook before any % table.
> 3. Recompute span from timestamps only; keep 2+ sessions as separate metric.
> 4. Regenerate archetype intent breakdown; add column comparing to prior playbook.
> 5. Update adoption table; footnote if denominator or W3 cap changed.

---

## Qual — Research decisions

**Bad:**
> We themed the interviews and pulled good quotes.

**Good:**
> - **Scope:** n=12 completed SME interviews (Wave 3 recruitment); excluded 2 pilot sessions.
> - **Theme rule:** Behaviour pattern must appear in ≥3 participants to become a theme; edge cases noted in appendix.
> - **Quote policy:** Real quotes only; anonymise as Participant A/B; no invented "representative" quotes.
> - **Codebook:** Merged "payroll deadline stress" and "payday cash-flow anxiety" into **Payday pressure** after user review.

---

## Qual — Method steps (rerun checklist)

**Bad:**
> Read new transcripts and update themes.

**Good:**
> 1. Save new transcripts to `{study-id}/interviews/round-{N}/` with filename `{participant-id}-{YYYYMMDD}.md`.
> 2. Confirm exclusion rules (pilots, incomplete sessions) before synthesis.
> 3. Load prior codebook from last playbook or `{study-id}-codebook.md`; log theme merges/splits in Research decisions.
> 4. Synthesise themes using evidence-archetypes qual path; mark segments where saturation is unclear.
> 5. Route deliverables: themes → Confluence page; supporting quotes → appendix; stakeholder readout → Miro.
> 6. Do not triangulate with survey counts unless user explicitly directs merge.

---

## Qual — What changed vs last wave

**Bad:**
> More interviews this time.

**Good:**
> - **n:** 12 → 18 interviews; enterprise segment added (n=6).
> - **Themes:** **Payday pressure** unchanged; new theme **Multi-entity bookkeeping** (4/6 enterprise participants).
> - **Saturation:** Retail segment saturated; enterprise still thin — user flagged 3 more interviews before locking enterprise themes.

---

## Mixed-methods — triangulation discipline

**Bad (collapsed claims):**
> Survey shows 16% multi-day span and interviews confirm users return over multiple days.

**Good (separate evidence, user-directed merge):**
> - **Quant (workbook):** 16.0% of Wave 3 users show multi-day span (timestamp rule).
> - **Qual (n=12):** 5/12 described returning "when the task wasn't finished" — behavioural retry, not habit.
> - **Triangulation:** User chose to present quant adoption row and qual retry narrative separately in Confluence; no merged % claim.

---

## Worked example — quant playbook excerpt (CXR004-style)

Based on a real analysis session pattern (synthetic paths):

```markdown
---
title: "CXR004 — high-volume span and adoption metrics"
study_id: CXR004
research_type: survey-analysis
wave: Wave 3
prior_playbook: null
---

## Research decisions (reproducibility)
- **Span metric:** min/max `timestamp` calendar days; not session count.
- **HV cohort:** ≥5 queries; n=218 of 3,211 chat-active (6.8%).
- **W3 HV share:** 93/1,056 (8.8%) — not 218/1,056.

## Method steps (rerun checklist)
1. Export new Langfuse cohort → `{study-id}-langfuse-{date}.xlsx`.
2. Validate n before % tables.
3. Recompute span, HV, W3 splits with locked definitions.
4. Regenerate intent breakdown; compare to this playbook.
5. Paste adoption table to Confluence; footnote denominator.
```

---

## Worked example — qual playbook excerpt

```markdown
---
title: "CXR004 — SME depth interview synthesis"
study_id: CXR004
research_type: qual-analysis
wave: Round 1
skills_used:
  - evidence-archetypes
---

## Research decisions (reproducibility)
- **Scope:** n=8 HV SMEs (10+ queries); 45-min sessions; pilots excluded.
- **Synthesis:** Behaviour archetypes from transcripts only — no survey triangulation in this round.
- **Quote policy:** Real quotes; Participant A–H labels; business names removed.

## Method steps (rerun checklist)
1. Add Round 2 transcripts to `cxr004/interviews/round-2/`.
2. Re-read prior themes; extend or split only with ≥3 participant evidence.
3. Update local synthesis `.md`; publish revised Miro board after user approves URL.
4. Flag saturation gaps before stakeholder readout.
```

---

## Zero-anchor honesty (research)

**Good (procedure-only wrap-up still valid):**
> Found 4 research anchors (metric definitions, denominator rules, delivery mode) but no new insights — proceeding with playbook-focused synopsis.

**Bad (inflated insight section):**
> Listing every table cell as an "insight" when the user only locked procedural rules.
