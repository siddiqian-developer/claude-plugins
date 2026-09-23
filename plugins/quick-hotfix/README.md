# quick-hotfix

Very quick hotfixes with minimal testing, for the loop where **you verify live in the UI**.
Nothing here is automatic: type the command in front of the prompt, every time.

| Command | Does |
|---|---|
| `/quick-hotfix:run <issue>` | One fix. Focused tests on the changed files only (**at most 50**), an import check and a typecheck/lint of the touched files. No full suite, no reviewer, no approval flows, no questions (it states its assumption instead). Nothing is committed. |
| `/quick-hotfix:run --no-tests <issue>` | The same, static checks only |
| `/quick-hotfix:run --commit <issue>` | The same, then a local WIP commit on the current feature branch (never pushed, never on a protected branch) |
| `/quick-hotfix:ui [--commit] <issue>` | **Frontend only.** Diagnoses first; if any part of the fix needs a change outside the frontend (backend, API contract, database, config, env, infrastructure) it edits nothing and returns `ERROR: not a UI-only fix` with what is needed. Frontend tests only, at most 50 |

## What it never skips

A security floor: no hotfix loosens a fail-closed path, an auth or role check, an egress,
anonymization or data-leak control, or the handling of a secret. If the quick fix would need
that, it stops and says so.

## The reply

Three lines, every time:

```
Fixed: <one line> — <file:line>
Checked: <tests run: N passed / M failed | static only>
Next: <restart backend terminal? | hot-reloads> → <where to look in the UI>
```

It never starts or restarts your services; it tells you which terminal to restart.

## Install

```
/plugin marketplace add siddiqian-developer/claude-plugins
/plugin install quick-hotfix@siddiqian-plugins
```
