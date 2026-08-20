---
description: Change the gitflow branch names, feature prefix or protected list after setup. Use when the user wants to rename main or dev, change the feature prefix, or adjust which branches are protected.
---

Change the gitflow configuration in `.gitflow.toml`. `$ARGUMENTS` may name what
to change.

## 1. Show what is in force now

Read `.gitflow.toml` and print the current values as a table. If the file is
missing, send the user to `/gitflow-guard:setup` instead.

## 2. Take the new values

Ask only about what they want to change; leave the rest alone.

| Setting | Meaning |
|---|---|
| `main` | Release branch |
| `dev` | Integration branch |
| `feature_prefix` | Prefix for work branches |
| `protected` | Space-separated branches where commits and pushes are denied |
| `plan_source` | Path to the plan, or `none` |
| `gates` | Command `/gitflow-guard:ship` runs before opening a PR |

Validate before writing: a branch named in `protected` that does not exist is
almost always a typo, so check `git branch -a` and query anything that does not
match.

## 3. Renaming a branch is more than a config edit

If the user is renaming `main` or `dev` rather than just pointing at a
differently-named existing branch, the rename has to happen in several places or
the repository ends up half-configured. Show this as a checklist and confirm
each before acting:

| Where | Action |
|---|---|
| `.gitflow.toml` | Update the key, and `protected` if it named the old branch |
| Local branch | `git branch -m <old> <new>` |
| Remote | `git push origin :<old> <new>` then reset the upstream |
| Default branch | `gh repo edit --default-branch <new>` if renaming `main` |
| Open PRs | PRs targeting the old branch need retargeting — list them with `gh pr list --base <old>` |
| CI workflows | `.github/workflows/*.yml` may name the branch in `on.push.branches` |
| `.githooks/` | No change needed; they read `.gitflow.toml` at runtime |

Renaming a branch other people have checked out will disrupt them. Say so, and
make sure the user wants it before touching the remote.

## 4. Report

Show a before/after table and note anything that still needs doing by hand —
retargeting PRs in particular.
