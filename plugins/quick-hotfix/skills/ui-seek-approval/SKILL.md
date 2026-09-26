---
name: ui-seek-approval
description: Quick FRONTEND-ONLY hotfix like /quick-hotfix:ui, but runs the seek-approval skill on the instructions first and applies only the approved reading. Fails with an error, before editing anything, if the approved fix needs any change outside the frontend. Use only when the user types /quick-hotfix:ui-seek-approval before a prompt. Usage /quick-hotfix:ui-seek-approval [test-budget] [none|touched|project] [--commit] <issue>; test-budget defaults to 50 (0 = no tests), static-check level defaults to touched.
---

Apply ONE frontend-only quick hotfix for: $ARGUMENTS, after its instructions are approved.

Arguments are parsed exactly as in the `run` skill (argument 1 = test budget, default 50,
`0` = no tests; argument 2 = static-check level `none` / `touched` / `project`, default
`touched`; `--commit` flag). Strip them; the rest is the issue.

This is the `run-seek-approval` skill with the frontend boundary of the `ui` skill. Read
`../run-seek-approval/SKILL.md` and `../ui/SKILL.md`
if they are not already loaded (relative to this skill's base directory; both build on `../run/SKILL.md`).

## Step 1 — approval, BEFORE any edit

Exactly step 1 of the `run-seek-approval` skill (run `seek-approval` on the issue text), plus:

1. **Find the frontend root first** (`ui` skill boundary item 1), so the options can be
   framed against it.
2. **Offer frontend-only readings.** A reading that needs any change outside the frontend root, or
   that hides a backend bug in the client (boundary item 4), is not offered as an option. If the
   only honest readings are outside the frontend, stop before asking anything and return the
   `ui` skill `ERROR: not a UI-only fix.` reply.

## Step 2 — the hotfix, on the approved readings only

1. **Boundary check on the approved readings** — `ui` skill boundary items 2–4, still before
   any edit. If the approved fix turns out to need anything outside the frontend, edit nothing and
   return the `ERROR: not a UI-only fix.` reply.
2. Then run the `ui` skill (its checks, UI rules and reply) with the rule overrides from step 2
   of the `run-seek-approval` skill.

## Reply

The the `ui` skill reply, with the `Approved: <reading>` first line. The `Next:` line is always
"hot-reloads" plus where to look.
