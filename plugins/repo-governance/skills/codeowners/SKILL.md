---
description: Write or update CODEOWNERS so security-sensitive paths get cross-review, verifying every handle exists and holds write access. Use when the user wants code owners, cross-review on certain paths, or to add a reviewer to CODEOWNERS.
---

Write `.github/CODEOWNERS` so the paths that matter get reviewed by someone
other than their author.

## The mechanism, because it is not obvious

There is no way to write "the other person must review this". What works is
listing **both** people as owners of the path: GitHub never lets a pull request
author satisfy their own code-owner requirement, so whoever opens the PR, the
other owner has to approve it. Cross-review in both directions falls out of
dual ownership.

This has a hard consequence: **a path with one owner is broken**. Its sole owner
can never approve their own pull request, so the requirement can never be met.
Never write a single-owner rule for a path you intend to protect.

## 1. Establish who the owners are

Ask for the handles. For each one, verify before writing it:

```bash
gh api users/<handle> -q .login
gh api repos/{owner}/{repo}/collaborators/<handle>/permission -q .permission
```

A handle that does not exist, or that lacks write access, is **silently ignored
by GitHub** — the rule does not fail loudly, it just stops protecting the path.
Refuse to write an unverified handle. If someone lacks access, say so and offer
to add them:

```bash
gh api -X PUT repos/{owner}/{repo}/collaborators/<handle> -f permission=push
```

Adding a collaborator changes who can write to the repository. Confirm with the
user first.

## 2. Establish which paths need cross-review

Ask, and suggest from what is actually in the repository. Look for the areas
where a mistake is expensive and hard to see in review:

| Area | Typical paths |
|---|---|
| Authentication and secrets | vault, key management, token handling |
| Data protection | DLP, anonymization, redaction, PII detection |
| Routing and policy | which data may reach which destination |
| Audit | append-only logs, tamper-evident records |
| Admin overrides | config stores that can weaken a control without touching it |
| The tests that prove the above | a quietly relaxed assertion is the failure mode |
| CI and this file | `/.github/` |

Include paths that do not exist yet if they are planned — the rule is then in
place on the commit that creates the file, not bolted on afterwards.

## 3. Write the file

```
# Default owner for everything not matched below.
*                             @owner-a

# Security paths — owned by both, so each one's PR needs the other's review.
/backend/app/guardrails.py    @owner-a @owner-b
/backend/app/vault/           @owner-a @owner-b
/.github/                     @owner-a @owner-b
```

Order matters: **the last matching rule wins**, so the broad `*` default goes
first and specific paths follow.

Group the entries with comments explaining *why* each path is owned. A future
reader needs to know whether a rule is load-bearing or leftover.

## 4. Say whether it will actually do anything

Check the plan before claiming the file works:

```bash
gh repo view --json isPrivate -q .isPrivate
gh api repos/{owner}/{repo}/branches/{branch}/protection >/dev/null 2>&1
```

On a **private repository on the GitHub Free plan, CODEOWNERS is inert** —
GitHub neither requests reviewers from it nor requires their approval. Say so
directly rather than leaving the user believing the file protects something.

Two honest options in that case:

1. Install `repo-governance`'s `codeowners-review` workflow, which reads this
   same file and does the requesting and the checking itself. It goes red
   without an owner approval, but it cannot block the merge.
2. Move to GitHub Pro or an org on Team, where the file works natively.

Offer the first — `/repo-governance:setup` installs it.

## 5. Report

A table of path, owners, and whether every handle verified. State plainly
whether the file is currently enforced, advisory via the workflow, or inert.
