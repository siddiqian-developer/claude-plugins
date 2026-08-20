# Developing repo-governance

For anyone changing this plugin. The user-facing guide is [README.md](README.md).

## What this plugin actually is

A re-implementation of three GitHub features that are **unavailable on a private
repository on the Free plan**: branch protection, rulesets, and CODEOWNERS. All
three return `403 Upgrade to GitHub Pro`, and CODEOWNERS additionally fails
*silently* — the file sits there doing nothing.

So the plugin has no skill that calls the protection API and expects it to work.
It probes, reports honestly, and installs Actions that do the job instead.

**If you are extending this, keep that honesty.** The temptation is to write
something that looks like it protects a branch. The whole value here is telling
someone plainly when nothing does.

## Layout

```
repo-governance/
├── .claude-plugin/plugin.json
├── skills/{setup,codeowners,audit}/SKILL.md
└── templates/workflows/
    ├── codeowners-review.yml    replaces code-owner review
    └── direct-push-alert.yml    replaces branch protection (detects, never prevents)
```

No hooks. Everything happens in skills and in GitHub Actions.

## The CODEOWNERS matcher

`codeowners-review.yml` embeds a Python implementation of gitignore-style
matching, because the workflow runs in the user's repo where the plugin is not
present. It cannot import a shared module — inline is the constraint, not a
style choice.

`to_regex()` semantics, which are worth knowing before you touch it:

| Pattern | Matches |
|---|---|
| `/backend/app/x.py` | anchored — that exact path |
| `docs/` | **unanchored** — `docs/a.md` and `backend/docs/a.md` |
| `/docs/` | anchored — root `docs/` only |
| `*.js` | any depth |
| `/src/**/*.ts` | requires an intermediate segment |

**Last matching rule wins**, as GitHub does it — so a broad `*` default must be
listed first and specific paths after.

If you change the matcher, re-run these cases. They are the ones that were wrong
in early drafts:

```python
("/backend/app/recognizers/", "backend/app/recognizersX.py", False)  # prefix, not substring
("docs/",  "backend/docs/a.md", True)   # unanchored
("/docs/", "backend/docs/a.md", False)  # anchored
("/src/**/*.ts", "src/c.ts", False)     # ** needs a segment
```

## The two traps the codeowners skill exists to prevent

Both are silent failures in GitHub itself, which is why the skill checks for
them explicitly:

1. **A handle without write access is ignored.** No error — the path simply
   stops being owned while continuing to look owned. The skill verifies each
   handle against `/users/<h>` *and* `/collaborators/<h>/permission`.
2. **A single-owner path can never be satisfied.** GitHub never lets a PR author
   approve their own PR, so a path owned only by its usual author deadlocks. The
   workflow detects this and fails with a distinct message rather than reporting
   "awaiting review" forever.

That second point is also *why* dual ownership is the mechanism for
"cross-review in both directions" — there is no way to express "the other
person" directly.

## Alert, never revert

`direct-push-alert.yml` opens an issue and changes nothing. Auto-revert was
considered and rejected: it would eventually undo a deliberate push, noisily,
in shared history.

If someone asks for auto-revert, explain that cost before building it. If it is
built, it must be opt-in and off by default.

## Testing the workflows

They only run on GitHub, so local testing is limited to:

```bash
python3 -c "import yaml; yaml.safe_load(open('templates/workflows/codeowners-review.yml'))"
```

For the matcher, extract the `to_regex` function into a scratch file and run the
cases above. For end-to-end, push to a throwaway repo and open a PR touching an
owned path.

Note `codeowners-review.yml` triggers on both `pull_request` and
`pull_request_review` — without the second, the check never re-runs after
someone approves, and stays red forever.

## Required permissions

| Workflow | Needs |
|---|---|
| `codeowners-review` | `contents: read`, `pull-requests: write` (to request reviewers) |
| `direct-push-alert` | `contents: read`, `pull-requests: read`, `issues: write` |

`pull-requests: write` is the one people trim by mistake; without it, review
requests fail while the approval check still runs, which looks like the workflow
half-works.

## Versioning

No `version` in `plugin.json` — the resolved commit SHA drives updates. The
validator warning is expected.
