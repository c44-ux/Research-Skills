# Method playbook — integration guide

How **method-synopsis** reproducibility mode fits alongside other Research-Skills and a repeatable study workflow.

---

## Recommended ritual

```text
Plan study → Collect data → Analyse in Cursor → method-synopsis → Save playbook → Next wave reads prior playbook
```

Run **method-synopsis** (or "method synopsis this research") **after** analysis is complete — not mid-exploration.

---

## Folder layout (project repo)

```text
.cursor/
├── skills/
│   └── method-synopsis/
├── commands/
│   └── method-synopsis.md       # reproducibility mode command
├── method-synopses/             # general method synopses (optional)
└── method-playbooks/            # rerunnable study docs (recommended)
    ├── 2026-05-22-cxr004-high-volume-span-analysis.md
    └── 2026-08-15-cxr004-sme-interview-synthesis-round1.md
```

Configure in [destinations.md](destinations.md):

```markdown
| destination_type | project |
| path_or_id | .cursor/method-synopses |
| method_playbook_folder | .cursor/method-playbooks |
```

Reproducibility mode saves to `method_playbook_folder` when set.

---

## Integration with other Research-Skills

| Skill | When to run method-synopsis | Capture in playbook |
|-------|----------------------------|---------------------|
| **[evidence-archetypes](../../evidence-archetypes/)** — quant | After survey Phase 3 scripts and segment reports | Column mapping path, script commands, segment rules, output paths |
| **[evidence-archetypes](../../evidence-archetypes/)** — qual | After thematic/archetype synthesis from transcripts | Participant scope, codebook, quote policy, Miro board URL |
| **uxr-planner** (if installed) | After study plan published or analysis complete | Confluence page ID, research questions, method, study ID |

**Cross-link in frontmatter:**

```yaml
skills_used:
  - evidence-archetypes
prior_playbook: 2026-05-22-cxr004-high-volume-span-analysis.md
```

---

## Quant vs qual vs mixed

| Type | Trigger hint | Playbook emphasis |
|------|--------------|-------------------|
| **survey-analysis** | Spreadsheet, Langfuse, cohort metrics | Metric definitions, denominators, script chain, rerun export steps |
| **qual-analysis** | Transcripts, interviews, themes, quotes | Scope, codebook, anonymisation, saturation, Miro/Confluence routing |
| **mixed-methods** | Both in one study | Separate quant and qual rerun sections; triangulation rules explicit |

User can say **"method synopsis this qual analysis"** to force qual framing.

---

## Longitudinal studies (same topic, new data)

When a new survey wave or interview round arrives:

1. Open or @mention the **prior playbook** for the same `study_id`.
2. Run analysis in a new Cursor chat.
3. Trigger **method-synopsis** — agent populates **What changed vs last wave**.
4. Save with new date prefix; set `prior_playbook` to previous filename.

Filename pattern: `YYYY-MM-DD-{study-id}-{topic-slug}.md` or `…-wave4.md`, `…-round2.md`.

---

## Privacy (research)

- Anonymise participant and business identifiers in playbooks intended for shared repos.
- Keep raw transcripts outside git when they contain PII.
- Playbooks in `.cursor/method-playbooks/` may be committed for team reproducibility — use redaction and synthetic labels.

See [privacy.md](privacy.md).
