# Examples — Arc, Attribution, Artifact

Load-bearing positive/negative pairs. Prefer the positive patterns in synopses.

---

## Arc — What Happened

**Bad (event list, no through-line):**

> User asked about scatter charts. Assistant added a legend. User asked for colours. Assistant changed colours. User said thanks.

**Good (arc):**

> User opened wanting a calendar scatter for high-volume users. Mid-thread they reframed the goal from "more chart types" to "one view that shows span vs density." The thread landed on a single HTML prototype with toggles for archetype filters, shipped as `high-volume-user-calendar-scatter.html`.

---

## Attribution

**Bad (collapsed "we", passive):**

> We decided to use Feelix Table. The empty state was improved. Claude fixed the bug.

**Good:**

> User decided to standardise on Feelix `Table` for the span listing. Assistant proposed an empty state with guided copy; user rejected the illustration and chose text-only. Assistant fixed the sort handler after user caught reversed default order.

**Joint credit:**

> User proposed grouping by archetype; assistant drafted card layout options; user chose the compact variant without avatars.

---

## Artifact (standalone)

**Bad (chat-dependent):**

> As discussed above, the MCP gate applies here too.

**Good:**

> The team treats `.cursor/rules/mcp-gate.mdc` as mandatory for Figma and Feelix work before UI edits.

---

## Zero-anchor honesty

**Good (before generating):**

> This looks like a single-topic lookup (npm script name) with no reframe or decision. A synopsis would mostly repeat the chat. Want me to run it anyway?

---

## Section omission

If there were no quotable user phrases, omit **Quotable Moments**. If nothing is unresolved, omit **Open Threads**.
