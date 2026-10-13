---
name: onboard
description: Set up this clone for the person using it, the way the project's own instructions say - find the project's onboarding declaration, run its setup in report mode, explain each gap in plain words, fix what can be fixed with the person's go, and say what still needs another person (access, credentials). Use when the user says onboard me, set me up, set up this clone, first time in this repo, or why does the workflow not work for me.
---

# onboard - this clone, set up the way the project says

A project's setup lives in the project, not in this skill. This skill finds it,
runs it, and turns its output into a short list of what is done, what was fixed
and what the person still has to get from someone else.

## 1. Find the declaration, in this order

| Look for | Use it as |
|---|---|
| `.claude/onboarding.md` | The authority: it names the setup command, its report-only and apply forms, the arguments to ask for, and anything else the person must do |
| A "Setup" or "Getting started" section in `CONTRIBUTING.md`, then `README.md` | The steps, when no onboarding file exists |
| `scripts/setup*.sh`, `bin/setup`, `Makefile` target `setup` | The command, when the docs name none |

Nothing found: say so, list what you looked for, and stop. Never invent setup
steps for a project that has none.

## 2. Report first, change nothing

Run the declared **report-only** form (`--check`, `--dry-run`, or whatever the
declaration names). If there is none, read the steps and check each one by
reading state (`git config --get ...`, `test -f ...`), not by doing it.

Present one table: item, state (ok, missing, wrong), and what fixing it does.
Separate **things this clone can fix** from **things only another person can
give** (repository access, host access, keys, credentials, tokens). For the
second kind, say who to ask and how the project says to receive it; never ask
the person to paste a credential into this conversation.

## 3. Fix, with the person's go

Ask for any argument the declaration requires (a role, a name for local config)
with a short question. Then run the apply form once, and re-run the report to
show the result. Never write a secret, a key or an address into a tracked file.

## 4. Point at the next step

End with the project's tutorial or first-task pointer if the declaration names
one, and the first thing to say to Claude to start real work.
