# Quote policy

All quotes in ux-interview-notes output must meet these four conditions.

---

## 1. Verbatim only

Reproduce the participant's exact words. Do not paraphrase, tighten, or clean up for readability.

If the quote contains a filler word, incomplete sentence, false start, or colloquialism — keep it. That is the data.

**Correct:**
> "I just, um, chuck it in general ledger." (00:13:59)

**Incorrect:**
> "I just put it in general ledger."

---

## 2. No injected context inside quote marks

Do not add explanatory words inside the quote to make it read more clearly.

**Correct:**
> "That would be awesome." (00:22:14)
> *Context: said in response to the Ordermentum buy button concept.*

**Incorrect:**
> "That [Ordermentum integration] would be awesome."

If the quote needs context to be understood, add it as a plain-text note outside the quote marks — never inside.

---

## 3. Timestamps

After every quote, add the VTT start time of the first line of that utterance in parentheses.

Format: `(HH:MM:SS)`

Example:
> "I just chuck it in general ledger." (00:13:59)

**If the source has no timestamps** (plain text transcript): omit timestamps and add this disclaimer once at the top of the notes:

> *(Timestamp unavailable — source transcript contains no time codes.)*

---

## 4. Context disclaimers

Add a *Context:* note when:
- The quote is a reaction to something on screen (prototype, concept card) that isn't named in the quote itself
- The quote uses a pronoun whose referent is unclear without knowing what was being discussed
- The quote is a superlative ("that's the most useful thing") and the referent needs to be named

Format — add as a new line in the same table cell, outside quote marks, italicised:

> "That would be awesome." (00:22:14)
> *Context: said in response to the buy button concept, not the session overall.*

---

## What these rules are for

Downstream consumers of interview notes — designers, PMs, engineers, stakeholders — often read quotes out of context. These rules ensure:

- Quotes can be trusted as evidence (verbatim, timestamped, traceable)
- Quotes are not accidentally misleading (no injected framing, context added where needed)
- Anyone can go back to the source recording to verify (timestamps make this fast)
