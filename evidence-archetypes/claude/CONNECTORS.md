# Connectors (Evidence Archetypes)

## Miro MCP (Miro delivery)

| Tool | Used for |
|------|----------|
| `context_explore` | Understand existing board layout before adding docs |
| `board_create` | New board — **only after user approves** |
| `doc_create` / `doc_update` | Summary + one doc per segment |
| `board_list_items` | Verify what was published |

**Always read MCP tool schemas** in your environment before calling — parameter names vary by connector version.

See `docs/miro_delivery_guide.md` for doc templates and layout rules (bullet lists only — no markdown tables in Miro docs).

---

## Board rules (non-negotiable)

| Rule | Detail |
|------|--------|
| **No default board** | Only URLs the **current user** provides this session, or from `board_create` after approval |
| **No cross-project reuse** | Never use board URLs from prior chats, wikis, or other researchers |
| **User approval** | Ask before `board_create`; present existing vs new board as numbered options |
| **Tenancy** | Publish only to boards the user owns or explicitly pastes |

---

## Claude environment matrix

| Environment | Qual / mixed synthesis | Survey Phase 3 scripts | Miro delivery |
|-------------|------------------------|------------------------|---------------|
| **Claude Code** + bash | Yes | Yes (Python + cs-ux-personas) | Yes (if Miro MCP connected) |
| **Claude Desktop / CoWork** + code execution | Yes | Yes (if Python available) | Yes (if Miro connected) |
| **Chat-only** (no tools) | Yes (in chat) | No — ask user to run scripts locally | No — deliver markdown only |

When Miro MCP is missing, complete synthesis and stop with local `.md` files as source of truth. Do not invent board URLs.

---

## If a connector fails

- **Miro auth error:** tell the user once; local markdown remains valid deliverable.
- **Partial publish:** report what succeeded; offer retry with same board URL.
- **Script failure:** show exact command and error; do not fabricate segment counts.

Do not fabricate quotes, segment labels, or n values.
