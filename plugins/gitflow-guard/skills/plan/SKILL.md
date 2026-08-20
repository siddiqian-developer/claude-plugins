---
description: Find, re-read or change the plan that drives feature detection, and show which tasks are done, in flight or unstarted. Use when the user asks what is next, wants to re-scan the plan, or points at a different plan file.
---

Read the plan and report task state. `$ARGUMENTS` may be a path to a plan file.

## 1. Locate the plan

If `$ARGUMENTS` names a file, use it. Otherwise read `plan_source` from
`.gitflow.toml`. If that is unset or `none`, scan for one:

`plans/*.md` · `plans/*.html` · `docs/plans/*` · `PLAN.md` · `ROADMAP.md` ·
`TASKS.md` · `_bmad-output/**/*.md`

Found exactly one → use it. Several → list them and ask. None → say so, and
offer to proceed without a plan, in which case feature detection falls back to
reading intent from the conversation.

## 2. Extract the tasks

Handle whichever shape the file uses:

| Shape | Example |
|---|---|
| Table row with an ID column | `\| T01 \| PK entity recognizers \| Eng B \|` |
| Heading | `## T01 · PK entity recognizers` |
| Checklist | `- [ ] T01 PK entity recognizers` |
| HTML anchor | `<div id="det-t01">` with a heading inside |

Take an ID and a title from each. If nothing parses, say so honestly rather than
inventing tasks — an empty result means the plan needs a bit of structure, and
that is worth telling the user directly.

## 3. Work out task state

For each task, decide from evidence rather than assumption:

| State | Evidence |
|---|---|
| **done** | Its branch merged into `<dev>`, or the plan marks it complete |
| **in flight** | A branch matching its slug exists, or `.git/gitflow-state.json` names it |
| **unstarted** | Neither |

Useful checks:

```bash
git branch -a --list "*<slug>*"
gh pr list --state merged --search "<task-id>"
```

If a task looks done in the plan but its branch never merged — or the reverse —
say so. A disagreement between the plan and the repository is worth surfacing,
not smoothing over.

## 4. Report

A table of ID, title, state, and branch where one exists. Then name the next
unstarted task and show the command:

```
/gitflow-guard:start <task-id>
```

If `plan_source` was empty or pointed somewhere stale, offer to update
`.gitflow.toml` to what you actually used.
