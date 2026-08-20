---
description: Finish a feature — run the checks, push the branch, and open a pull request into the integration branch. Use when the user says ship it, open a PR, finish the feature, or the work on a feature branch is done.
---

Push the current feature branch and open its pull request. `$ARGUMENTS` may
carry a title or extra context for the PR body.

## 1. Preflight

Read `.gitflow.toml` for `dev` and `protected`.

Refuse to proceed and say why if any of these hold:

| Condition | Why it stops here |
|---|---|
| On a protected branch | There is no feature to ship. Run `/gitflow-guard:start` |
| Detached HEAD | Not on a branch |
| No commits ahead of `origin/<dev>` | Nothing to review |

If the working tree is dirty, list the files and ask whether to commit them
first. Do not commit silently.

## 2. Check ancestry

```bash
git merge-base --is-ancestor origin/<dev> HEAD
```

If this fails, the branch was cut from the wrong place and merging it will drag
unrelated history into `<dev>`. Tell the user, show the fix, and ask before
doing it:

```bash
git rebase --onto origin/<dev> $(git merge-base HEAD origin/<dev>)
```

## 3. Run the gates

Run whatever the repository actually uses, in this order of preference:

1. The `gates` key in `.gitflow.toml`, if set
2. The repository's own documented test command (check `CLAUDE.md`, `Makefile`, `package.json` scripts, `pytest.ini`)
3. Nothing — and say so rather than pretending checks ran

Report the real result. If the gates fail, stop and show the output. Do not open
a pull request on a red branch unless the user explicitly asks, and if they do,
say in the PR body that the checks are failing.

## 4. Push and open the PR

```bash
git push -u origin <branch>
gh pr create --base <dev> --head <branch> --title "..." --body "..."
```

Write a body that is worth reading:

- What changed and why, in a sentence or two
- A table of the significant files or areas when there are several
- The task ID from `.git/gitflow-state.json` if there is one
- The gate results, honestly — including failures
- Anything deliberately left out of scope

Use the repository's commit and PR conventions if it has them. If the repository
uses Conventional Commits, match that style in the title.

## 5. Clear the session state

Update `.git/gitflow-state.json` to mark this feature's session work done, and
record the PR number. The task itself is not finished until the PR merges —
that is checked lazily on a later session start, not polled for now.

Report the PR URL, and what CI will and will not be able to enforce. On a
private repository on the GitHub Free plan the checks run but cannot be
required, so a red pull request can still be merged by anyone with write access.
Say that plainly rather than implying the PR is gated.
