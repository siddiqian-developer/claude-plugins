---
description: Open a release pull request from the integration branch into the release branch, with the accumulated changes summarised. Use when the user says cut a release, release to main, or ship dev to main.
---

Open the release pull request: `<dev>` into `<main>`.

## 1. Preflight

Read `.gitflow.toml` for `main` and `dev`. Then:

```bash
git fetch origin
git log --oneline origin/<main>..origin/<dev>
```

If there is nothing between them, say so and stop — there is no release to cut.

Check for an already-open release PR before creating another one:

```bash
gh pr list --base <main> --head <dev> --state open
```

## 2. Assemble what is being released

Summarise `origin/<main>..origin/<dev>` for a reader who has not followed the
work. Group by Conventional Commit type when the repository uses it:

| Section | From |
|---|---|
| Added | `feat` |
| Fixed | `fix` |
| Changed | `perf`, `refactor` |
| Removed | `revert` |
| Breaking | anything with `!` or a `BREAKING CHANGE` footer |

Call out breaking changes at the top, not buried in a list.

If `changelog-keeper` is installed and `CHANGELOG.md` has an `Unreleased`
section, use that as the source instead — it is curated prose and better than
anything derived from commit subjects. Offer to promote `Unreleased` to a
version heading as part of the release.

## 3. Open it

```bash
gh pr create --base <main> --head <dev> --title "Release: ..." --body "..."
```

The body should carry the grouped summary, the commit range, and an honest note
on what was verified versus what was not.

## 4. Report

Give the PR URL and the count of commits being released. State plainly whether
the merge is gated: on a private repository on the GitHub Free plan it is not,
so a release can be merged with checks red. If that matters here, say so.
