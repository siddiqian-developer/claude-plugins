---
description: Set up gitflow in this repository — choose the branch names and feature prefix, install the git hooks and CI, and wire the plugin in globally or for this project. Use when the user says set up gitflow, configure gitflow-guard, or asks to enforce a branching workflow in a repo.
---

Set this repository up for gitflow. Work through the steps in order and **ask
before writing anything** — this touches branches, git config and committed
files.

## Step 1 — Where should the plugin be active?

Ask the user, and say what each choice means:

| Choice | Writes | Effect |
|---|---|---|
| **Global** | `~/.claude/settings.json` | Active in every repository you open |
| **This project, for everyone** | `.claude/settings.json` (committed) | Anyone who clones and trusts the folder gets it automatically |
| **This project, just me** | `.claude/settings.local.json` (gitignored) | Local only, nothing committed |

For the project choices, the file needs both keys:

```json
{
  "extraKnownMarketplaces": {
    "siddiqian-plugins": {
      "source": { "source": "github", "repo": "siddiqian-developer/claude-plugins" }
    }
  },
  "enabledPlugins": { "gitflow-guard@siddiqian-plugins": true }
}
```

Merge into any existing settings file rather than overwriting it.

## Step 2 — Branch names

Ask for each, showing the default. Do not assume — the whole point is that these
are configurable.

| Setting | Default | Meaning |
|---|---|---|
| `main` | `main` | Release branch |
| `dev` | `dev` | Integration branch; features are cut from it and merge back into it |
| `feature_prefix` | `feature/` | Prefix for work branches |
| `protected` | `main dev` | Branches where commits and pushes are denied |

Check which of these branches already exist (`git branch -a`). If `main` or `dev`
is missing, ask whether to create it. If the repository uses different names
already (say `master` or `develop`), offer those as the defaults instead — read
what is there rather than imposing.

Write `.gitflow.toml` at the repository root:

```toml
# gitflow-guard configuration.
# Flat key = "value" only: this file is read both by the Python hooks and by
# the POSIX sh git hooks, which have no TOML parser.
main           = "main"
dev            = "dev"
feature_prefix = "feature/"
protected      = "main dev"
```

## Step 3 — The plan

**If the repository already contains a plan, read it automatically** — do not
ask the user to point at a file that is sitting there. Look in this order:

`plans/*.md` · `plans/*.html` · `docs/plans/*` · `PLAN.md` · `ROADMAP.md` ·
`TASKS.md` · `_bmad-output/**/*.md`

Extract tasks from whichever shape the file uses: markdown table rows with an ID
column, `## T01 · Title` headings, `- [ ] T01 Title` checklists, or HTML anchors
like `id="det-t01"`. Show the user the tasks you found and ask them to confirm
it is the right plan.

If several candidates exist, list them and ask which is authoritative.

**If nothing is found, ask explicitly**: point me at a plan file, paste one, or
proceed without. If they proceed without, record `plan_source = "none"` and say
that feature detection will fall back to reading intent from the conversation.

Record in `.gitflow.toml`:

```toml
plan_source = "plans/roadmap.md"
```

## Step 4 — Terminal git hooks

These cover work done outside Claude Code. Copy from the plugin's
`templates/githooks/` into `.githooks/` in the repository:

`gitflow-lib.sh` · `pre-commit` · `pre-push`

To find the plugin directory, use `$CLAUDE_PLUGIN_ROOT` if it is set in the
environment; otherwise locate the installed plugin under
`~/.claude/plugins/**/gitflow-guard`.

Then make them executable and point git at them **relatively**:

```bash
chmod +x .githooks/pre-commit .githooks/pre-push
git config core.hooksPath .githooks
```

The relative path matters. An absolute path works on this machine and breaks for
everyone else who clones. Verify with `git config --get core.hooksPath` and
confirm the output is `.githooks`, not a path starting with `/`.

## Step 5 — CI

Copy `templates/workflows/gitflow.yml` to `.github/workflows/gitflow.yml`.

Then check what the checks can actually do:

```bash
gh api repos/{owner}/{repo} -q .private
gh api repos/{owner}/{repo}/branches/{main}/protection >/dev/null 2>&1
```

If the repository is private and the protection call returns 403 (`Upgrade to
GitHub Pro`), **tell the user plainly**: the workflow will run and a violation
will be red on the pull request, but the check cannot be marked required, so
nothing mechanically prevents a merge. Do not describe the repository as
protected when it is not. Point them at `/repo-governance:audit` for the full
picture.

## Step 6 — Report

Summarise as a table: what was written, the branch names in force, whether the
plan was found or declined, whether `core.hooksPath` is relative, and what CI
can and cannot enforce on this plan. Then show the user the first command they
will actually use:

```
/gitflow-guard:start <short-name>
```

Do not commit anything yourself unless the user asks. Show them what changed and
let them commit it.
