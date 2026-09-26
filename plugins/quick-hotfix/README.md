# quick-hotfix

Very quick hotfixes with minimal testing, for the loop where **you verify live in the UI**.
Nothing here is automatic: type the command in front of the prompt, every time.

| Command | Does |
|---|---|
| `/quick-hotfix:run [budget] [level] [--commit] <issue>` | One fix. Focused tests on the changed files only, an import check and a typecheck/lint. No full suite, no reviewer, no approval flows, no questions (it states its assumption instead). Nothing is committed unless `--commit`. |
| `/quick-hotfix:ui [budget] [level] [--commit] <issue>` | **Frontend only.** Diagnoses first; if any part of the fix needs a change outside the frontend (backend, API contract, database, config, env, infrastructure) it edits nothing and returns `ERROR: not a UI-only fix` with what is needed. Frontend tests only |
| `/quick-hotfix:run-seek-approval [budget] [level] [--commit] <issue>` | `run`, but first runs the `seek-approval` skill on the issue and applies only the reading you approve |
| `/quick-hotfix:ui-seek-approval [budget] [level] [--commit] <issue>` | `ui`, but first runs `seek-approval`, offering only frontend-only readings, and applies only the one you approve |

## Arguments

| # | Argument | Values | Default |
|---|---|---|---|
| 1 | Test budget: the maximum tests to run | a whole number; `0` = no tests | `50` |
| 2 | Static-check level | `none` · `touched` (files changed) · `project` (whole typecheck and lint) | `touched` |
| — | `--commit` | a local WIP commit on the current feature branch; never pushed, never on a protected branch | off |

```
/quick-hotfix:run 0 none fix the Save label          # no tests, no checks
/quick-hotfix:run 10 project --commit fix the 409    # 10 tests, full checks, commit
/quick-hotfix:ui fix the chip spacing                 # 50 tests, touched files
```

The two `-seek-approval` commands need the `seek-approval` skill (with `seek-approval-understanding`
and `seek-approval-build-decisions`) installed in `~/.claude/skills/`; this plugin does not ship it.

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
