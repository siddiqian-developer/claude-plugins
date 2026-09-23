---
name: run
description: Very quick hotfix with minimal testing — the user verifies live in the UI. Use only when the user types /quick-hotfix:run before a prompt. Optional leading flags --no-tests (typecheck/import check only) and --commit (local WIP commit after the fix).
---

Apply ONE quick hotfix for: $ARGUMENTS

The user is testing live in the UI and will verify the fix there. Speed matters more than
ceremony, but the security floor below never moves.

## Flags (leading words of $ARGUMENTS, then strip them)

| Flag | Effect |
|---|---|
| (none) | Default mode: focused tests, at most 50 |
| `--no-tests` | No tests at all — static checks only (row 2 below) |
| `--commit` | After the fix passes its checks, make a local WIP commit on the current feature branch (never push, never on a protected branch) |

## Rules

| # | Rule |
|---|---|
| 1 | **Test budget.** Only the tests that cover the files you changed, **at most 50** per run (check the collected count before running; narrow with `-k` if over). `--no-tests`: none. Never the full suite. |
| 2 | **Static checks, touched files only.** Backend: an import check of the app (`python -c "import app.main"` or the project's equivalent). Frontend: typecheck plus lint of the touched files. Pre-existing warnings are not yours to fix. |
| 3 | **Skip** the full suite, reviewer agents, seek-approval flows, plan mode and graph planning. |
| 4 | **No questions.** Choose the obvious default and state the assumption in one line. Ask only when blocked with no reasonable guess. |
| 5 | **Scope lock.** Change only what the fix needs: no refactors, no renames, no comment rewrites, no drive-by cleanups, no new abstractions. |
| 6 | **Security floor — never relaxed.** Do not loosen a fail-closed path, an auth or role check, an egress / anonymization / data-leak control, or a secret's handling, even if that is the quick fix. If the fix would need it, stop and say so in one line instead. |
| 7 | **No commit** unless `--commit`. Never push. Respect the repo's branch rules and worktree isolation. |
| 8 | **Record keeping.** Append one line to the session's hotfix log (a `HOTFIXES.md` note in the job/scratch dir, never committed): date, what changed, files. Decision logs are updated later, in one go, when the user asks. |
| 9 | **Live rig.** Never start, stop or restart the user's services. Tell them what to restart: backend changes need the backend terminal restarted (unless it runs with reload); frontend changes hot-reload. |
| 10 | **One fix per invocation.** If $ARGUMENTS holds several issues, fix them in order but keep each one's diff separable so any can be reverted alone. |
| 11 | **Failures.** If the focused tests or checks fail because of your change, fix it within the budget. If they fail for a reason that predates the change, say so and do not chase it. |

## Reply — exactly this shape, nothing more

```
Fixed: <one line> — <file:line>[, <file:line>]
Checked: <tests run: N passed / M failed | static only> 
Next: <restart backend terminal? | hot-reloads> → <where to click / what to look at in the UI>
```

Add a fourth line `Assumed: …` only when rule 4 applied, and `Blocked: …` only when rule 6 stopped you.
