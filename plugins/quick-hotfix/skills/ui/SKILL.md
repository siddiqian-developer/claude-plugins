---
name: ui
description: Very quick FRONTEND-ONLY hotfix with minimal testing — the user verifies live in the UI. Fails with an error, before editing anything, if the fix needs any change outside the frontend. Use only when the user types /quick-hotfix:ui before a prompt. Usage /quick-hotfix:ui [test-budget] [none|touched|project] [--commit] <issue>; test-budget defaults to 50 (0 = no tests), static-check level defaults to touched.
---

Apply ONE frontend-only quick hotfix for: $ARGUMENTS

Arguments are parsed exactly as in this plugin's `run` skill (argument 1 = test budget, default 50,
`0` = no tests; argument 2 = static-check level `none` / `touched` / `project`, default
`touched`; `--commit` flag).

Everything in this plugin's `run` skill applies (rules 1–11 and its reply shape) — read
`../run/SKILL.md` (relative to this skill's base directory) if it is not already loaded — with these additions.

## The frontend boundary — decided BEFORE any edit

1. **Find the frontend root**: the web-app package the UI is built from (e.g. `frontend/`, or the
   directory with the Next/Vite/React `package.json`). Everything outside it is off-limits.
2. **Diagnose first, edit second.** Work out the whole fix. If ANY part of it needs a change outside
   the frontend root — backend or API code, an API contract or response shape, a database or
   migration, server config, env vars, infrastructure, shared schemas, backend tests — **edit
   nothing** and reply only:

   ```
   ERROR: not a UI-only fix.
   Needs outside the frontend: <file or area> — <why, one line each>
   Use /quick-hotfix:run instead (or split the fix).
   ```

3. Inside the frontend root, also off-limits without saying so first: generated files, lockfiles,
   build config, and environment files (`.env*`, anything inlined at build time such as
   `NEXT_PUBLIC_*`).
4. **Fixing the UI to hide a backend bug is not a UI fix.** If the real defect is server-side,
   return the ERROR above rather than papering over it in the client.

## Checks (instead of rules 1–2 of the `run` skill)

| Check | Scope |
|---|---|
| Typecheck | Per argument 2: `touched` = the frontend project, errors in touched files only count; `project` = every error reported; `none` = skipped |
| Lint | Per argument 2: touched files, the whole frontend, or skipped |
| Tests | Frontend unit/component tests covering the touched files, **at most the test budget** (default 50; `0` = none); none if the project has none. No backend tests, no e2e. |

Follow the project's UI rules (existing primitives, design tokens, no hex colours, the house focus
ring) — a hotfix does not get to invent a style.

## Reply

The `run` skill's three-line reply; the `Next:` line is always "hot-reloads" (no restart) plus
where to look.
