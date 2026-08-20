---
description: Install the governance workflows that stand in for branch protection when it is unavailable — code-owner review and direct-push alerting. Use when the user wants to enforce review policy on a repository that cannot use branch protection.
---

Install the substitutes for the GitHub features this repository cannot use.

## 1. Find out what is actually available first

Do not install substitutes for features that already work. Probe:

```bash
gh repo view --json nameWithOwner,isPrivate
gh api repos/{owner}/{repo}/branches/{branch}/protection
gh api repos/{owner}/{repo}/rulesets
```

| Result | What to do |
|---|---|
| 403 `Upgrade to GitHub Pro` | Native protection is unavailable. Install the substitutes — this is what they are for |
| 404 | Protection is *available* but unconfigured. Offer to configure it natively; that is strictly better than the substitutes |
| 200 | Already configured. Report the rules and ask whether the substitutes are still wanted |

If protection is available, prefer it. The configuration that matches a
self-merge-plus-cross-review policy is:

```json
{
  "required_status_checks": { "strict": true, "contexts": ["<your check>"] },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0,
    "require_code_owner_reviews": true,
    "dismiss_stale_reviews": true
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

`required_approving_review_count: 0` with `require_code_owner_reviews: true` is
the combination that lets an author self-merge ordinary changes while still
forcing cross-review on owned paths. `enforce_admins: false` keeps an admin from
deadlocking themselves before a second owner exists.

## 2. Ask which branches are protected

Read `.gitflow.toml` if `gitflow-guard` is set up in this repository — reuse its
`protected` list rather than asking again. Otherwise ask, defaulting to `main`
and `dev`.

## 3. Install the workflows

Copy from the plugin's `templates/workflows/` into `.github/workflows/`:

| File | Does |
|---|---|
| `codeowners-review.yml` | Parses CODEOWNERS itself, requests review from the owner who is not the author, and fails until one of them approves |
| `direct-push-alert.yml` | On a push to a protected branch, checks whether the commit arrived via a merged pull request; opens an issue if not |

Edit the `on.push.branches` list in `direct-push-alert.yml` to match the actual
protected branch names — the template ships with `main` and `dev`.

Locate the plugin via `$CLAUDE_PLUGIN_ROOT` if set, otherwise under
`~/.claude/plugins/**/repo-governance`.

**Alert only.** `direct-push-alert.yml` does not revert anything, deliberately:
an automatic revert would eventually undo a deliberate push, noisily and in
shared history. If the user asks for auto-revert, explain that cost before
building it.

## 4. Make sure CODEOWNERS exists and is sound

`codeowners-review.yml` is useless without a valid CODEOWNERS file. If there
isn't one, or it has single-owner paths or unverified handles, run
`/repo-governance:codeowners` before finishing here.

## 5. Report — and do not overstate it

Summarise what was installed, then state the ceiling plainly:

> These workflows report violations. They cannot block a merge, because required
> status checks need branch protection, which this plan does not include. A red
> pull request can still be merged by anyone with write access.

List who currently has write access, since on this plan that is the only thing
that actually limits who can push:

```bash
gh api repos/{owner}/{repo}/collaborators -q '.[] | "\(.login) \(.permissions.push)"'
```

Finish by pointing at `/repo-governance:audit` for the full picture at any time.
