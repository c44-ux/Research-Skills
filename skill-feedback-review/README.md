# Skill feedback review

Reviews your recent chats for feedback on your skills and proposes concrete `SKILL.md` edits you can commit to git. Works in Claude Code (reads session history on disk) and claude.ai (searches past chats).

Part of [Research-Skills](https://github.com/c44-ux/Research-Skills).

## What it does

1. Looks at the last 7 days of chats (or a window you give it).
2. Finds moments where you commented on a skill, corrected it, repeated the same habit around it, or praised it.
3. Gives each moment a recommendation: **update going forward**, **once-off**, or **unclear**. These are recommendations only. You decide.
4. Drafts before and after edits for the "update going forward" items, and flags the rest for your review.
5. On your approval, Claude Code edits the skill and commits on a branch. Claude.ai gives you the updated file and the git commands.

Nothing is changed or pushed without your approval.

## Install

**Claude Code (personal):**

```
git clone https://github.com/c44-ux/Research-Skills.git `
  "$env:USERPROFILE\.claude\skills\Research-Skills"
Copy-Item -Recurse -Force `
  "$env:USERPROFILE\.claude\skills\Research-Skills\skill-feedback-review" `
  "$env:USERPROFILE\.claude\skills\skill-feedback-review"
```

**Claude.ai:** zip the `skill-feedback-review` folder (root of the zip must contain `SKILL.md`) and upload it under Customize, then Skills.

## Use

Type `/skill-feedback-review`, or ask something like "what should I fix in my skills based on recent chats".

## Limits to know

- **Claude.ai only reads the area you start from.** Run from a regular chat and it reads regular chats. Run from inside a Project and it reads that Project's chats. Run it once per place you use skills.
- **Claude Code reads every working folder** under your Claude Code session history by default.
- In claude.ai it needs your skills repo URL (if public) or a paste of the skill text, so it never proposes edits against text it has not seen.
