# Privacy pass — limitations

The Step 4 redaction pass in [SKILL.md](../SKILL.md) is **best-effort**, not security-grade.

## What it tries to catch

- Common API key prefixes and cloud access-key shapes
- JWT-shaped strings
- Obvious `password=` / `api_key:` style assignment lines

## What it does not guarantee

- Secrets in images, attachments, or pasted logs the model did not re-read
- Custom or internal token formats without matching patterns
- Redaction of personal data the user chose to include (names, emails) — synopses should already avoid secrets; synthetic examples in prototypes are fine
- Removal from git history if a synopsis was saved before the user noticed a leak

## User responsibilities

1. Review the **mandatory preview** before Accept.
2. Do not Accept if redaction looks incomplete — ask for Edit or Cancel.
3. Prefer configuring synopses folders outside public repos if content is sensitive.

If a secret was exposed in chat, rotating the credential matters more than redacting the synopsis file.
