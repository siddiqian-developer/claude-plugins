# repo-governance

Code-owner review and push detection for repositories that cannot use branch
protection.

## The problem it solves

On a **private repository on the GitHub Free plan**, three things you might
assume are working are not:

| Feature | Reality |
|---|---|
| Branch protection | `403 Upgrade to GitHub Pro` |
| Rulesets | `403 Upgrade to GitHub Pro` |
| CODEOWNERS | The file is **inert**. GitHub neither requests reviewers from it nor requires their approval |

None of these fail loudly. You get a repository carrying a CODEOWNERS file, a
policy in its docs and a green CI badge, with nothing standing between anyone
and `main`.

## Skills

| Skill | Does |
|---|---|
| `/repo-governance:setup` | Probes what is available, then installs the substitute workflows (or configures native protection if the plan allows it) |
| `/repo-governance:codeowners` | Writes CODEOWNERS with verified handles and dual ownership |
| `/repo-governance:audit` | Reports what is **actually** in force, and who currently has write access |

## The substitutes

| Workflow | Replaces | Can it block? |
|---|---|---|
| `codeowners-review.yml` | Code-owner auto-request and required review | No. It requests the right reviewer and goes red until one approves |
| `direct-push-alert.yml` | Branch protection | No. It notices after the fact and opens an issue |

`codeowners-review.yml` parses CODEOWNERS itself with gitignore-style matching
and last-match-wins ordering, computes which owned paths a pull request touches,
requests review from the owner who is **not** the author, and fails until one of
them approves.

`direct-push-alert.yml` **alerts only**. It never reverts. An automatic revert
would eventually undo a deliberate push, noisily and in shared history.

## Two CODEOWNERS traps

**A single-owner path is broken.** Its owner cannot approve their own pull
request, so the requirement can never be satisfied. Always give a protected path
two owners — that is also how "cross-review in both directions" is expressed,
since GitHub never lets an author satisfy their own code-owner requirement.

**An invalid handle is ignored silently.** A handle that does not exist, or that
lacks write access, does not raise an error; the path simply stops being
protected while continuing to look protected. `codeowners` verifies every handle
against the API before writing it.

## What actually enforces anything on this plan

Only one thing: **access level**. Contributors with `read` access working through
forks genuinely cannot push to your branches. Everything else here is detection.

`audit` reports this without softening it. If the answer is "nothing prevents a
push to main", it says exactly that.

## Changing this plugin

See [DEVELOPING.md](DEVELOPING.md) — architecture, the contracts that fail silently when broken, the cases to keep green, and how to test locally.
