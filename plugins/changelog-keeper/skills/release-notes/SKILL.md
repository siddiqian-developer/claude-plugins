---
description: Assemble release notes from the changelog or the commit range, and promote Unreleased to a version heading. Use when the user is cutting a release, wants release notes, or asks what changed since the last version.
---

Turn what has accumulated into release notes. `$ARGUMENTS` may name a version or
a commit range.

## 1. Find the range

Prefer, in order:

1. An explicit range in `$ARGUMENTS`
2. `origin/<main>..origin/<dev>` if `.gitflow.toml` exists
3. The last tag to `HEAD`: `git describe --tags --abbrev=0`

Say which one you used — a reader cannot check the notes without knowing the
range they came from.

## 2. Prefer the changelog over the commits

If `CHANGELOG.md` has an `## [Unreleased]` section with content, **that is the
source**. It is curated prose someone wrote deliberately; commit subjects are
not. Use the commit range only to check for anything notable that never made it
into the changelog, and list those gaps separately rather than silently folding
them in.

If there is no changelog, derive from commits and group by Conventional type:

| Section | Types |
|---|---|
| Added | `feat` |
| Fixed | `fix` |
| Changed | `perf`, `refactor` |
| Removed | `revert` |

Anything with `!` or a `BREAKING CHANGE` footer goes at the top under
**Breaking changes**, never buried in a list.

## 3. Promoting Unreleased

If the user is cutting a version, offer to rewrite the heading:

```markdown
## [Unreleased]

## [1.4.0] - 2026-08-20
```

Keep the empty `## [Unreleased]` above it so the next change has somewhere to
go. Use the real current date — do not guess it; read it from the environment.

Update the link definitions at the foot of the file if the changelog uses them.

## 4. Report honestly

Alongside the notes, state:

- The range the notes cover
- Notable commits that have no changelog entry, if any
- Anything shipping that is known to be incomplete or untested

A release note that omits a known caveat is worse than one that never existed,
because it converts an open question into a false assurance.
