---
description: Start a new feature — cut a correctly named branch from the integration branch so its ancestry is right by construction. Use when the user says start a feature, start work, begin a task, or names something new to build.
---

Start a piece of work on its own branch. `$ARGUMENTS` is the short name or the
task the user named; if it is empty, work out what they mean from the
conversation, or ask.

## 1. Read the configuration

Read `.gitflow.toml` at the repository root for `dev`, `feature_prefix` and
`plan_source`. If the file does not exist, tell the user to run
`/gitflow-guard:setup` first, and use the defaults `dev` / `feature/` for now.

## 2. Pick the task

**If a plan is configured**, read it and find the task. Match `$ARGUMENTS`
against task IDs and titles. If the user gave nothing, offer the next unstarted
task and ask them to confirm. Derive the branch name from the task ID and title:

    T01 · PK entity recognizers   ->   feature/t01-pk-recognizers

**If no plan is configured**, derive the slug from `$ARGUMENTS` or from what the
user described. Lowercase, hyphens, no spaces, and name it after the work rather
than the action — `feature/expired-token-redirect`, not `feature/fix`.

Show the branch name and get confirmation before creating it.

## 3. Check the working tree

If there are uncommitted changes, ask what to do. Do **not** decide alone:

| Option | When it fits |
|---|---|
| Carry them onto the new branch | The usual case — `git checkout -b` moves them across untouched |
| Commit them first | They belong to the branch you are on |
| Leave and abort | They are someone else's in-progress work |

Never use bare `git stash`. The stash stack is shared across worktrees and other
sessions of the same repository, so an untagged entry can be popped by someone
else. If stashing is genuinely wanted, use `git stash push -u -m "<unique-tag>"`,
capture the SHA from `git stash list --format='%H %gs'`, and recover it later
with `git stash apply <sha>` rather than `pop`.

## 4. Cut the branch from the integration branch

```bash
git fetch origin <dev>
git checkout -b <feature_prefix><slug> origin/<dev>
```

Branch from `origin/<dev>` **explicitly**. This is the point of the skill:
ancestry is correct by construction, so it never has to be detected and
corrected later. Do not branch from whatever happens to be checked out.

If `origin/<dev>` does not exist, say so and ask whether to branch from the
local `<dev>` instead — do not silently fall back.

## 5. Record and report

Write the active feature to `.git/gitflow-state.json` (inside `.git`, so it is
per-clone and never committed):

```json
{ "feature": "t01-pk-recognizers", "branch": "feature/t01-pk-recognizers", "task_id": "T01" }
```

If the file already names a *different* active feature, tell the user they are
starting a second feature in one session, and recommend a fresh session so the
context stays clean. This is advice, not a block — if they want to continue,
continue.

Report the branch created, what it was cut from, and the task it maps to.

## 6. When more than one person works the plan

If the plan assigns work to more than one person, say this once when starting a
slice — it is the difference between a clean Friday and a merge weekend:

> **One slice = one branch = one merge, and merge frequently.** Do not batch
> three slices to the end of the week; that is what turns append-only edits into
> a conflict. Do not start the next slice until the current one is merged and
> green — batching also makes a failing gate impossible to attribute to a
> change.

Where the plan allows it, keep each slice in its own module so the only shared
lines touched are append-only ones.
