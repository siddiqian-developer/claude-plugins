# Developing changelog-keeper

For anyone changing this plugin. The user-facing guide is [README.md](README.md).

## The design constraint

**It suggests; it never writes.** Everything here follows from that.

A changelog entry is curated prose: it says what changed for someone who was not
there, cites the files that matter, and states caveats honestly. A line derived
from a commit subject is none of those. A changelog full of generated lines is
one nobody reads, which makes it worse than no changelog.

So the tooling drafts and a person edits. If you are tempted to add an
auto-append, that is the thing this plugin deliberately does not do.

## Layout

```
changelog-keeper/
├── .claude-plugin/plugin.json
├── hooks/hooks.json              PostToolUse on Bash
├── scripts/hook.py               the in-session nudge
├── skills/release-notes/SKILL.md
└── templates/
    ├── githooks/post-commit      the terminal nudge (POSIX sh)
    └── workflows/changelog.yml    the enforcing half
```

Three surfaces, one rule set. The Python hook and the `sh` hook implement the
same mapping — **if you change one, change the other**, or the two paths start
disagreeing about what counts as notable.

## The mapping

| Type | Section |
|---|---|
| `feat` | Added |
| `fix` | Fixed |
| `perf`, `refactor` | Changed |
| `revert` | Removed |
| `!` or `BREAKING CHANGE` footer | Changed, marked breaking |

Silent when:

- the type is `docs`, `chore`, `style`, `ci`, `build` or `test` **and** not breaking
- the commit is a merge — its entries were written on the branch being merged
- the commit already touched `CHANGELOG.md`
- the subject is not a Conventional Commit at all

Each of those silences is a real case someone hit. Do not remove one without
knowing which.

## The hook contract

`PostToolUse`, exit 0, stdout is exactly one JSON object or nothing:

```json
{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"..."}}
```

`PostToolUse` **cannot block** — the tool already ran. `decision: "block"` only
adds a message. If you want to stop something, that is `PreToolUse`, and it
belongs in a different plugin.

Fails open: any exception exits 0 silently.

## Detecting "was that a commit?"

`looks_like_commit()` splits compound commands and checks whether a `git`
invocation's subcommand is `commit`. It runs *after* the fact, so it then reads
`HEAD` for the real subject rather than parsing `-m` out of the command — which
is why `git commit` with an editor, or with `-F`, still works.

It does not verify the commit succeeded. If a commit fails, `HEAD` is unchanged
and the nudge either repeats the previous commit or stays silent because the
changelog was already touched. Harmless, but that is why you may see a repeat.

## The CI job

`changelog.yml` is the only part that can fail. It is `pull_request`-only, so it
never blocks a hotfix pushed straight to a branch.

It needs `fetch-depth: 0` — the commit range `origin/<base>...HEAD` is
unavailable in a shallow clone, and the job silently counts zero notable commits
instead of failing. That is the bug to look for if it stops catching things.

On a private repo on the GitHub Free plan the check **cannot be marked
required**, so red does not prevent a merge. The workflow header says so; keep
that accurate if the plan changes.

## Testing

```bash
# in a scratch repo
git commit --allow-empty -m "feat(auth): add a thing"
echo '{"cwd":"'"$PWD"'","tool_input":{"command":"git commit -m x"}}' \
  | python3 scripts/hook.py
```

Cases to keep green:

| Subject | Expected |
|---|---|
| `feat(auth): x` | Added, scope bolded |
| `fix: x` | Fixed |
| `docs: x` | silent |
| `feat!: x` | Changed, marked breaking |
| `fix: x` + `BREAKING CHANGE:` body | Changed, breaking |
| not conventional | silent |
| commit that touched CHANGELOG.md | silent |
| merge commit | silent |

The `sh` hook is tested by making real commits with `core.hooksPath` pointed at
`templates/githooks/`.

## Versioning

No `version` in `plugin.json`; the resolved commit SHA drives updates. The
validator warning is expected.
