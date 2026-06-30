# Evidence Archetypes (UX)

Build **evidence-grounded behaviour archetypes** from **your** surveys and/or interviews — any product domain.

Part of [Research-Skills](https://github.com/c44-ux/Research-Skills). Synthesis stays local; optional publish to **your** Miro via MCP.

---

## Choose your platform

| Variant | Folder | Runtime | Install target |
|---------|--------|---------|----------------|
| **Cursor** | [`cursor/`](cursor/) | Cursor Agent mode + Miro MCP | `%USERPROFILE%\.cursor\skills\evidence-archetypes\` |
| **Claude** | [`claude/`](claude/) | Claude Code, Desktop, CoWork + Miro connector | `%USERPROFILE%\.claude\skills\evidence-archetypes\` |

Both variants include the same `docs/` and `scripts/` (self-contained install packages).

---

## Quick install

**Cursor:**

```powershell
git clone https://github.com/c44-ux/Research-Skills.git "$env:USERPROFILE\.cursor\skills\Research-Skills"
Copy-Item -Recurse -Force `
  "$env:USERPROFILE\.cursor\skills\Research-Skills\evidence-archetypes\cursor" `
  "$env:USERPROFILE\.cursor\skills\evidence-archetypes"
```

**Claude Code (personal):**

```powershell
git clone https://github.com/c44-ux/Research-Skills.git "$env:USERPROFILE\.claude\skills\Research-Skills"
Copy-Item -Recurse -Force `
  "$env:USERPROFILE\.claude\skills\Research-Skills\evidence-archetypes\claude" `
  "$env:USERPROFILE\.claude\skills\evidence-archetypes"
```

**Claude Desktop / CoWork:** zip the [`claude/`](claude/) folder — see [claude/README.md](claude/README.md).

---

## End-to-end flow

```text
Survey / interviews  →  Synthesis (local .md / .json)  →  Miro board (Miro MCP / connector)
```

Survey path also requires sibling skill **`cs-ux-personas`** for Phase 3 scripts.
