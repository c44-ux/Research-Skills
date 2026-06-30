# Method synopsis

Capture this Cursor session as a **method synopsis** — durable, rerunnable documentation for reproducible research.

**Instructions for the agent**

1. Read and follow [`.cursor/skills/method-synopsis/SKILL.md`](../SKILL.md) in **reproducibility mode** end to end.
2. Load [`.cursor/skills/method-synopsis/references/examples-research.md`](../references/examples-research.md) for quant and qual worked examples.
3. Infer `research_type`: `survey-analysis`, `qual-analysis`, or `mixed-methods`. If unclear, ask once before rendering.
4. Run the salience check including **method / research anchors** (definitions, scope, codebook, quote policy, tool chain, deliverable routing).
5. Apply the privacy pass — anonymise participant/business identifiers in qual work.
6. Use the **reproducibility output structure** (Research decisions, Inputs & artefacts, Method steps with quant and/or qual rerun sections, Next wave playbook).
7. If a prior playbook for the same `study_id` exists in `.cursor/method-playbooks/`, read it and populate **What changed vs last wave**.
8. **Mandatory preview** — show full markdown; wait for Accept, Edit, or Cancel before saving.
9. Save to `method_playbook_folder` from [`references/destinations.md`](../references/destinations.md) (default: `.cursor/method-playbooks/`) unless the user specified a per-run override.

Do not activate unless the user ran this command or used an explicit method synopsis trigger phrase.
