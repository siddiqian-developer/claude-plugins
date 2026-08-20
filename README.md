# claude-plugins

Git workflow discipline for teams working in Claude Code.

Three plugins, installable independently:

| Plugin | Does |
|---|---|
| [`gitflow-guard`](plugins/gitflow-guard) | Enforces gitflow. Denies commits and pushes on protected branches *before git runs*, cuts feature branches from the integration branch so ancestry is right by construction, and tracks features against your plan |
| [`repo-governance`](plugins/repo-governance) | Code-owner review and direct-push alerting for repositories that cannot use branch protection, plus an audit of what is actually in force |
| [`changelog-keeper`](plugins/changelog-keeper) | Conventional Commits into Keep a Changelog. Reminds rather than generates, and gates the pull request when a notable change lands with no entry |

## Install

```
/plugin marketplace add siddiqian-developer/claude-plugins
/plugin install gitflow-guard@siddiqian-plugins
```

Install to **user scope** for every repository you open, or to **project scope**
so everyone who clones gets it. For a whole team, commit this to the repo's
`.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "siddiqian-plugins": {
      "source": { "source": "github", "repo": "siddiqian-developer/claude-plugins" }
    }
  },
  "enabledPlugins": {
    "gitflow-guard@siddiqian-plugins": true,
    "changelog-keeper@siddiqian-plugins": true
  }
}
```

A teammate then clones, opens Claude Code, trusts the folder, and has it. No
install step.

Then, once per repository:

```
/gitflow-guard:setup
```

## What these can and cannot enforce

Read this before relying on any of it.

| Layer | Where it binds | Bypassable |
|---|---|---|
| Claude Code hooks | Inside Claude Code | No — the tool call is denied before git runs |
| Git hooks | Any terminal in that clone | `--no-verify`, or never installing them |
| CI workflows | On GitHub, per pull request | Cannot block a merge unless checks can be marked *required* |
| Branch protection | Server side | Not bypassable — **and not available on a private repo on the GitHub Free plan** |

That last row is the one that matters. On a private repository on the Free plan,
branch protection, rulesets and CODEOWNERS are all unavailable — the API returns
`403 Upgrade to GitHub Pro`. These plugins are built for that reality: they make
the right path easy and the wrong path loud, and `repo-governance`'s
`codeowners-review` workflow re-implements code-owner review in an Action that
goes red without the right approval.

**Nothing here makes a merge impossible on that plan.** The only free mechanism
that genuinely prevents a push is reducing write access so contributors work
through forks. `/repo-governance:audit` will tell you exactly where you stand,
and will not flatter the answer.

## Requirements

| | |
|---|---|
| `git` | Any recent version |
| `python3` | For the Claude Code hooks — needed because hook stdout must be exactly one JSON object, and hand-rolling JSON escaping in `sh` breaks on the first command containing a quote |
| `gh` | For the skills that open pull requests and query GitHub |

The **git** hooks are pure POSIX `sh` — no bash, no jq, no Python — so they run
anywhere, on every commit, in a mixed-language team.

## Design notes

- **Hooks enforce, skills assist.** The hooks are the load-bearing part; the
  skills make the correct path faster than the incorrect one.
- **Everything fails open.** A hook that cannot parse its input, or hits an
  unexpected error, prints nothing and exits 0. A guard that breaks someone's
  commit is worse than one that occasionally misses.
- **Escape hatches are deliberate.** `git commit --no-verify` works, and is meant
  to: it makes the exception explicit and visible in the reflog rather than
  silent.
- **Alert, don't auto-revert.** `direct-push-alert` opens an issue and changes
  nothing. An automatic revert would eventually undo a deliberate push, noisily
  and in shared history.
- **Say what is true.** Every skill that reports on enforcement is instructed to
  state plainly when something is not enforced. The failure this whole
  repository exists to prevent is a repo that looks protected and is not.

## Licence

MIT — see [LICENSE](LICENSE).
