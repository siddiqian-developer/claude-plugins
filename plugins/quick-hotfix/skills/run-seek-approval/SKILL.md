---
name: run-seek-approval
description: Quick hotfix like /quick-hotfix:run, but runs the seek-approval skill on the instructions first and applies only the approved reading. Use only when the user types /quick-hotfix:run-seek-approval before a prompt. Usage /quick-hotfix:run-seek-approval [test-budget] [none|touched|project] [--commit] <issue>; test-budget defaults to 50 (0 = no tests), static-check level defaults to touched.
---

Apply ONE quick hotfix for: $ARGUMENTS, after its instructions are approved.

Arguments are parsed exactly as in the `run` skill (argument 1 = test budget, default 50,
`0` = no tests; argument 2 = static-check level `none` / `touched` / `project`, default
`touched`; `--commit` flag). Strip them; the rest is the issue.

Everything in the `run` skill applies (rules 1–11 and its reply shape) — read
`../run/SKILL.md` (relative to this skill's base directory) if it is not already loaded — except as changed below.

## Step 1 — approval, BEFORE any edit

1. Invoke the Skill tool with `skill: "seek-approval"`, `args:` the issue text (the arguments
   stripped). If the Skill tool can't load it, Read `~/.claude/skills/seek-approval/SKILL.md`.
2. Follow it fully: understanding, then build-decisions, with its grilling and 4-option
   questions. Read-only investigation (reading code, grepping) to frame the options is allowed;
   editing is not.
3. Every option must stay inside the security floor (`run` rule 6). A reading that would
   need to loosen it is not offered as an option; name it in one line as ruled out.
4. Do not ask about the test budget, static-check level or `--commit`: those are set by the
   arguments.

## Step 2 — the hotfix, on the approved readings only

Run the `run` skill on the approved readings and decisions, with these overrides:

| `run` rule | Override |
|---|---|
| 3 (skip seek-approval flows) | Seek-approval has already run in step 1. Still skip everything else rule 3 lists. |
| 4 (no questions) | Applies from here on. If a new consequential decision appears mid-fix, ask it seek-approval style (4 options, recommended first) instead of assuming. |
| 5 (scope lock) | The scope is exactly what was approved, nothing more. |
| 8 (record keeping) | The hotfix log line also carries the approved reading in a few words. |

## Reply

The the `run` skill reply shape, plus a first line:

```
Approved: <the approved reading, one line>
```
