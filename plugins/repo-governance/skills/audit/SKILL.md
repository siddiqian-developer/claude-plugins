---
description: Report what governance is actually in force on this repository versus what the files claim — branch protection, CODEOWNERS, required checks, and who holds write access. Use when the user asks whether the repo is protected, who can merge, or whether CODEOWNERS is working.
---

Answer one question honestly: **is any of this actually enforced?**

A repository can carry a CODEOWNERS file, a protection policy in its docs and a
CI workflow, and still have nothing standing between a developer and `main`.
That gap is the failure this skill exists to expose. Report what is true, not
what the files imply.

## 1. Identify the repository and plan

```bash
gh repo view --json nameWithOwner,visibility,isPrivate
gh api repos/{owner}/{repo} -q '.permissions'
```

## 2. Probe each control

Test them; do not infer from the presence of a file.

| Control | Probe | Read the result as |
|---|---|---|
| Branch protection | `gh api repos/{o}/{r}/branches/{branch}/protection` | 403 `Upgrade to GitHub Pro` → **unavailable on this plan**. 404 → available but not configured. 200 → configured; report the actual rules |
| Rulesets | `gh api repos/{o}/{r}/rulesets` | Same reading |
| CODEOWNERS | File exists? Repo private? Plan? | Present but **inert** on a private Free repo — GitHub ignores it entirely |
| Required checks | From the protection payload | Cannot be required without protection |
| Substitute workflows | `.github/workflows/codeowners-review.yml`, `direct-push-alert.yml` present and passing? | These are `repo-governance`'s replacements. Report whether they exist and whether recent runs succeeded (`gh run list`) |
| Write access | `gh api repos/{o}/{r}/collaborators` | Everyone listed with `push` can commit straight to any branch when protection is unavailable |

## 3. Check CODEOWNERS for the traps

If a CODEOWNERS file exists, read it and check each:

| Trap | Why it matters |
|---|---|
| A handle that does not exist | GitHub ignores it silently — the path is unowned and looks owned |
| A handle without write access | Same silent failure |
| A path with a single owner | Its owner cannot approve their own pull request, so the requirement can never be met |
| A path listed that does not exist in the repo | Usually a typo or a rename; the rule protects nothing |

Verify handles for real:

```bash
gh api users/<handle> -q .login
gh api repos/{o}/{r}/collaborators/<handle>/permission -q .permission
```

## 4. Report

Lead with a verdict line, then the detail. Format it like this:

```
repo-governance audit   <owner>/<repo>   (private, Free plan)

  branch protection    UNAVAILABLE — 403 Upgrade to GitHub Pro
  rulesets             UNAVAILABLE — 403
  CODEOWNERS           present · 14 paths · 2 owners each · INERT on this plan
  required checks      none can be required on this plan
  substitute workflows codeowners-review ✓   direct-push-alert ✓
  write access         alice (admin) · bob (write)

  VERDICT: nothing mechanically prevents a push or merge to main or dev.
           The workflows report violations; they cannot block them.
```

Then state the options plainly, with their real costs:

| Option | Effect | Cost |
|---|---|---|
| GitHub Pro, or an org on Team | Real branch protection, working CODEOWNERS, required checks | A subscription |
| Reduce write access; contributors work in forks | Genuine prevention — they cannot push at all | Fork workflow friction; the maintainer becomes the merge bottleneck |
| Keep as is | Convention plus loud detection | A determined or careless push still lands |

Do not soften the verdict. If the answer is "this repository is not protected",
say exactly that. The reason this skill exists is that the opposite impression
is easy to form and expensive to discover later.
