---
name: skill-feedback-review
description: >-
  Mines recent chats for feedback on skills and proposes concrete SKILL.md edits
  the user can commit to git. Works in Claude Code (reads session history) and
  claude.ai (searches past chats). Use whenever the user invokes
  /skill-feedback-review, or asks to review, improve, tune or audit their skills
  based on how recent chats went, e.g. "what should I fix in my skills", "which
  skills are annoying me", "weekly skill review", "update my skills from
  feedback". Trigger even if they do not say "feedback" or "git".
---

# Skill feedback review

Goal: find where the user corrected, re-prompted or fought a skill in recent chats, then propose small, evidence-backed edits to those skills. The user applies and pushes the edits to git (Claude Code can apply and commit for them).

## Step 0: Detect environment

- **Claude Code** (bash and local files available, skills on disk): chats come from session history, skills are read and edited in place.
- **Claude.ai** (past chat tools available, no local repo): chats come from `recent_chats` and `conversation_search`, current skill text comes from the repo or a paste, edits are output as diffs.

## Step 1: Scope (ask at most one question)

Default window: last 7 days. Default skills: all that appear in the evidence.
Only ask if the user gave neither a window nor a skill name, and then ask one combined question. If they gave either, proceed.

## Step 2: Gather evidence

### Claude Code
1. Session transcripts live as `.jsonl` files under `$HOME/.claude/projects/`. List files modified inside the window.
2. Use grep or jq to pull user turns near skill use. Cues: slash command invocations, the skill name, "Skill" tool calls.
3. Read only the surrounding turns, not whole sessions.
4. Each subfolder of `$HOME/.claude/projects/` is one working directory. Scan all of them by default so the review covers every repo, and say which folders were covered. Narrow to one only if the user asks.

### Claude.ai
1. Call `recent_chats` for the window (paginate with `before`, stop after about 5 calls).
2. Call `conversation_search` with skill names and slash commands as the query (content words only).
3. Use `read_conversation` once per chat at most, at the hit. Do not page on.
4. Scope limit: the chat tools only see one scope at a time. Run from a regular chat and you only see regular chats. Run from inside a Project and you only see that Project's chats. State which scope was covered at the top of the report, and tell the user to run the skill again from a Project (or a regular chat) to cover the others. Never imply the review was complete across scopes.

### Optional extra source
If `skill-feedback/feedback-log.md` exists or the user pastes one, treat its open entries as additional evidence.

## Step 3: Extract signals and classify each as "update going forward" or "once-off"

Only the user's own turns count as evidence. Claude's turns are context, never evidence of what the user wanted.

Corrections are often the user steering toward their goal, not a sign the skill is wrong. Always record them, but never assume one needs a skill update. Flag it and give a verdict (see below). The default verdict for a correction seen in only one chat is "once-off".

Not a signal on its own: a skill that has not been used for a while. That says nothing about its quality.

Signals to record:
1. **Direct comment on the skill itself** ("this skill is too long", "it should also do X").
2. **Corrections:** any time the user corrects or redirects a skill's output. Note whether the same correction appears in other chats.
3. **Usage pattern:** the user does the same thing around the skill every time (supplies the same context first, overrides the same default, sends the same follow-up prompt).
4. **Praise or approval** of how a skill behaved. Record it so edits do not remove what works.

For each signal record: skill name, chats or dates, short paraphrase of what the user said or did. Quote user wording only when exact phrasing matters, and keep quotes short.

Then label every signal with one verdict:
- **Update going forward:** the user stated it as a standing rule ("always", "from now on", "this skill should"), OR it recurs across two or more separate chats, OR it is a repeated usage pattern.
- **Once-off:** appears in one chat only and is tied to that task's specifics (the default for a single correction). Flag it for the user's review. Do not draft an edit unless the user says to update the skill.
- **Unclear:** evidence is split or thin. List it and ask the user.

Every verdict is a recommendation only. The user decides. Say why for each in one line, so they can overrule it.

Attribute carefully. If it is unclear which skill produced the output, label it "unattributed" and do not propose an edit for it.

## Step 4: Read the current skill text before proposing anything

- Claude Code: read the `SKILL.md` from disk. Locations: `.claude/skills/<name>/` in the repo, `$HOME/.claude/skills/<name>/`, or the user's skills repo.
- Claude.ai: ask once for the repo URL or a paste. If the repo is public, fetch the raw `SKILL.md` with bash (github.com and raw.githubusercontent.com are reachable). If private or unreachable, ask the user to paste it.

Never propose a diff against text you have not seen. Skip feedback the current text already addresses.

## Step 5: Report

Telegraphic. Australian English. No preamble. Scannable in under 2 minutes.

1. **Evidence table:** skill | signals found | verdict (update going forward, once-off, unclear) | one-line reason
2. **Patterns:** max 3 bullets (triggering, tone, length, missing steps, wrong defaults)
3. **Proposed edits:** for each of at most 3 skills, ordered by impact:
   - Evidence: 1 to 3 lines with chat references
   - Change: before and after, as a small diff
   - Why it should help, and any risk of regressing something that worked (use the praise signals)
4. **Quick wins:** edits that take under 15 minutes
5. **Flagged for your review:** every once-off and unclear item, each with the recommendation and reason. For each, ask the user: update the skill, or leave it? Draft the edit only if they say update. Unattributed items are listed with no edit.

If zero signals are found, say so in one line and stop.

## Step 6: Apply (on approval only)

Ask which edits to action unless the user said "just do quick wins" or similar.

### Claude Code
1. Edit the canonical `SKILL.md`. Keep edits small and focused.
2. Create a branch named `skill-feedback/YYYY-MM-DD` and commit with a message listing the skills touched.
3. Show the diff and the push command. Never push without explicit confirmation.

### Claude.ai
1. Output each updated `SKILL.md` as a file (or a unified diff if the change is small).
2. Give the git commands and a ready-made commit message for the user to run.
3. Do not claim anything was saved or pushed.

## Rules

- Prefer small edits over rewrites. Preserve the skill's name and structure.
- Draft edits up front only for "update going forward" items. Once-off and unclear items are flagged for the user to decide, never silently dropped. Do not remove behaviour that earned praise.
- Conflicting feedback on one skill: show both sides and ask, do not pick.
- Multiple copies of a skill (Cursor, Claude, repo): edit the canonical one and list the others as needing a sync.
- Chats can hold sensitive content. Extract only what concerns skill behaviour and keep other detail out of the report.
- Never use em dashes or tildes in output.
