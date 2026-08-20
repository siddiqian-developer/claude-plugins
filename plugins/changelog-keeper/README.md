# changelog-keeper

Conventional Commits into Keep a Changelog. Reminds; does not generate.

## Why a reminder and not a generator

A changelog entry is curated prose. It says what changed for a reader who was
not there, it cites the files that matter, and it states caveats honestly. A
line derived from a commit subject is none of those, and a changelog full of
generated lines is one nobody reads.

So the tooling drafts the entry and puts it in front of a person. The person
writes the words.

## What it does

| Component | When |
|---|---|
| `PostToolUse` hook | After a `git commit` inside Claude Code |
| `post-commit` git hook | After a `git commit` in any terminal |
| `changelog.yml` CI job | On every pull request |
| `/changelog-keeper:release-notes` | When cutting a release |

The two hooks suggest an entry. The CI job is the half that fails.

## Mapping

| Commit type | Section |
|---|---|
| `feat` | Added |
| `fix` | Fixed |
| `perf`, `refactor` | Changed |
| `revert` | Removed |
| Anything with `!` or a `BREAKING CHANGE` footer | Changed, marked breaking |

Silent for `docs`, `chore`, `style`, `ci`, `build` and `test` unless the commit
is breaking. Silent for merge commits — their entries were written on the branch
being merged. Silent when the commit already touched the changelog.

## The CI job

Runs on pull requests only, so it never blocks a hotfix pushed straight to a
branch. It counts notable commits in `origin/<base>...HEAD` and fails when there
are some but `CHANGELOG.md` is untouched, listing the commits it counted.

On a private repository on the GitHub Free plan this check **cannot be marked
required**, so a red result does not prevent a merge. It makes the omission
visible; merging anyway remains a human decision.

## Independent

No dependency on `gitflow-guard`. Conventional Commits and a changelog are
useful in repositories with no branching policy at all.

## Changing this plugin

See [DEVELOPING.md](DEVELOPING.md) — architecture, the contracts that fail silently when broken, the cases to keep green, and how to test locally.
