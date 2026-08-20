# gitflow-guard

Enforces gitflow where the work actually happens.

## What it does

| Component | Type | Severity |
|---|---|---|
| Commit or push on a protected branch | `PreToolUse` hook | **Hard deny** — the Bash call never runs |
| Force-push to a protected branch | `PreToolUse` hook | **Hard deny** |
| Force-push anywhere else | `PreToolUse` hook | Warn |
| Bare `git stash` / `git stash pop` | `PreToolUse` hook | Warn |
| Branch not descended from the integration branch | `SessionStart`, CI | Warn |
| Git posture at session start | `SessionStart` hook | Report |
| A prompt that reads as new work while on a protected branch | `UserPromptSubmit` hook | Warn |

## Skills

| Skill | Does |
|---|---|
| `/gitflow-guard:setup` | Prompts for branch names, finds or asks for the plan, installs git hooks and CI, wires the plugin globally or per project |
| `/gitflow-guard:config` | Changes branch names, prefix, protected list, gates — with a checklist for a real rename |
| `/gitflow-guard:plan` | Re-scans the plan, reports which tasks are done, in flight or unstarted |
| `/gitflow-guard:start` | Cuts `feature/<slug>` from `origin/<dev>` |
| `/gitflow-guard:ship` | Runs the gates, pushes, opens the pull request into `<dev>` |
| `/gitflow-guard:release` | Opens `<dev>` into `<main>` with the changes summarised |

## Configuration

`.gitflow.toml` at the repository root. A flat `key = "value"` subset of TOML —
deliberately, so both the Python hooks and the POSIX `sh` git hooks can read it
without a parser.

```toml
main           = "main"
dev            = "dev"
feature_prefix = "feature/"
protected      = "main dev"
plan_source    = "plans/roadmap.md"   # or "none"
gates          = "pytest -q"          # optional; run by ship
```

Every name is configurable. If your repository uses `master` and `develop`,
`setup` reads what is there and offers those as the defaults.

## Why `start` matters more than the ancestry check

`start` cuts the branch from `origin/<dev>` explicitly, which makes wrong
ancestry impossible rather than detectable. The ancestry warnings elsewhere are
a safety net for branches created some other way — they are not the mechanism.

The failure they catch: branching off `main` by accident, then dragging
unrelated history into `<dev>` at merge time.

## The stash warning

The stash stack is shared across **all worktrees and all sessions** of a
repository. A bare `git stash` puts an untagged entry on a stack another session
can pop. If you must stash:

```bash
git stash push -u -m "unique-tag"
git stash list --format='%H %gs'     # capture your entry's SHA
git stash apply <sha>                # apply, never pop
```

A temporary WIP commit is usually better.

## Limits

- The Claude hooks only bind work done **through Claude Code**. The git hooks
  cover the terminal, and `--no-verify` bypasses those by design.
- CI checks cannot be marked required on a private repository on the GitHub Free
  plan, so a red pull request can still be merged. `/repo-governance:audit`
  reports the real position.
- Everything fails open. If `python3` is missing or a hook errors, the tool call
  proceeds.

## Changing this plugin

See [DEVELOPING.md](DEVELOPING.md) — architecture, the contracts that fail silently when broken, the cases to keep green, and how to test locally.
