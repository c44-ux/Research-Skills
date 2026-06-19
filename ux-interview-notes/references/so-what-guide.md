# So what / Unresolved questions — guide

The So what section is Section 5 of every set of notes. It is not a summary. It is a set of open questions that the notes raise but cannot answer on their own — the bridge between raw participant data and the work that comes next.

---

## What makes a good So what question

**Traceable.** Every question should connect to something specific this participant said or did. Generic questions that could appear in any set of notes add no value.

**Answerable in principle.** Frame questions as something a team could actually investigate — a design experiment, a technical spike, a product decision, a follow-up interview.

**Discipline-specific.** Design, Product, and Engineering each have different jobs. Questions in each section should reflect what that discipline would actually need to decide next.

**Not a restatement.** Do not rephrase a finding as a question (e.g. "Should we build the feature the participant wanted?" is not a useful question). Push one step further: what does that signal imply that we don't yet know?

---

## Design: So what?

Questions about how the experience should be shaped.

Focus areas:
- Where in an existing workflow does a new feature need to land to require zero behaviour change?
- What is the minimum review step that maintains trust without adding friction?
- How should the UI handle the split between autonomous action and human approval?
- What permission or access model does the session imply (e.g. staff sub-accounts with limited access)?
- Is there a tension between what the participant said they want and what they actually did?

**Example from a concept testing session:**

| Question | Why it matters from this session |
|---|---|
| Where should the receipt upload entry point live to fit the participant's existing 5-minute daily reconciliation habit? | Participant reconciles every morning as their first task. A feature that requires a separate workflow step will be skipped. |
| What does the approve/decline pop-up need to show for the participant to trust it without checking Xero separately? | Participant said they'd prefer auto-push with a confirmation step, but also said they'd parallel-run for a month — suggesting the pop-up needs to be informative, not just a yes/no. |

---

## Product: So what?

Questions about scope, prioritisation, segmentation, and go-to-market.

Focus areas:
- Does this participant's top pick align with the concept being prioritised? If not, what does that mean?
- Which signals from this session generalise to a segment vs this individual only?
- What external dependency (accountant endorsement, supplier partnership, compliance change) would unlock adoption faster than any product change?
- What is the adoption trigger or timing constraint (e.g. start of financial year)?
- Is this a wedge into a new segment or an expansion of an existing one?

**Example from a concept testing session:**

| Question | Why it matters from this session |
|---|---|
| Is the "start at the new financial year" adoption timing a constraint we need to support with onboarding flow, or just a preference? | Two participants independently said they would not activate mid-cycle. If this is common, a "start fresh July 1" prompt in onboarding could materially improve activation rates. |
| Does the NFP segment need a separate positioning for the claims optimiser — grant discovery rather than deductions? | Participant dismissed the deductions framing immediately but lit up at grant surfacing. Same feature, different frame, different segment. |

---

## Engineering / Dev: So what?

Questions about technical feasibility, integration complexity, data requirements, and reliability constraints.

Focus areas:
- What does a reliable deduplication guarantee require technically, and how do we surface that guarantee in a way users trust?
- What accuracy threshold does OCR need to reach before this participant would stop manually verifying?
- Does the participant's named integration partner have a public API? What does their data model look like?
- What data volume and frequency does the integration need to handle (e.g. daily vs monthly batches)?
- Are there credit, returns, or adjustment flows that a buy button integration would need to support?

**Example from a concept testing session:**

| Question | Why it matters from this session |
|---|---|
| Does Ordermentum have a public API, and does it expose individual supplier names per line item or only the platform-level merchant name? | Participant's top condition for buy button adoption was supplier-level detail (not just "Ordermentum"). If the API only returns platform-level data, the feature as described is not deliverable without a different architecture. |
| What would a watertight deduplication guarantee look like technically for the email connection feature, given a participant had a $2,500 duplicate in 2019 and has not re-enabled auto-forwarding since? | Trust, once broken, requires a demonstrated technical guarantee — not just a UI assurance. The question is what the guarantee actually consists of and how to make it visible. |

---

## Calibration

- **3-5 questions per discipline** per session
- Fewer for short or low-relevance sessions
- More for expert participants with dense, multi-domain signals
- Never pad with questions that could appear in any set of notes
