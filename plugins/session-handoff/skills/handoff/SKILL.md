---
name: handoff
description: Session handoff pattern. Use at the end of a feature session to wrap up (commit, push, save memory), write a handoff file and print the opening prompt for the next session; or at the start of a session with 'resume <path>' to absorb a handoff, verify it against reality and delete it. Use whenever the user says handoff, hand over, wrap up the session, next session, or pastes a '/handoff resume' line.
---

# /handoff — the session handoff pattern

One session per feature. A session ends by writing what the **next** one needs to know that is
not visible in the code, the git log, or memory; the next session reads it, absorbs it, and
deletes it. This command does both halves.

Arguments: `$ARGUMENTS`

- Starts with `resume ` → **RESUME mode** (section B). The rest is the handoff path.
- Anything else → **CREATE mode** (section A). The text, if any, is the purpose of the next session.

Work through the Bash tool where it can do the job. Never put personal names, credentials,
provider keys or real phone numbers in a handoff — role labels (Eng A / Eng B) only.

---

## A · CREATE mode

### A1 · Purpose of the next session — ask first, always

If `$ARGUMENTS` is empty, ask with AskUserQuestion (one question, free text via "Other" is fine):
**"What is the next session for?"** Offer 3 options derived from the current conversation —
e.g. "continue this feature", "next item in the plan", "review / ship what was built" — so the
user can pick or type. Do not proceed until you have a purpose in one sentence; it becomes the
handoff's title and first paragraph.

If `$ARGUMENTS` has text, that is the purpose. Restate it in one line and continue.

### A2 · Resolve where the handoff lives

In this order, stop at the first hit:

1. The project's `CLAUDE.md` / `CLAUDE.local.md` names a handoff location (grep them for
   `handoff`). Use it — e.g. this may be a docs directory **outside** the repo because the
   integration branch is protected and a transient file would cost two pull requests.
2. Inside a git repo → `HANDOFF.md` at the repo root (`git rev-parse --show-toplevel`).
3. Otherwise → the current directory.

Filename when a directory is used: `<slug>-handoff.md`, slug from the purpose
(lowercase, hyphens, ≤5 words). If a file of that name exists, append `-2`, `-3`… — never
overwrite a handoff you did not write this session; other `*-handoff.md` files beside it belong
to other sessions.

### A3 · Do whatever is necessary before writing

Leave the checkout in a state the next session can start from without archaeology:

| Check | Action |
|---|---|
| `git status --porcelain` non-empty | Show the user the list. Commit it on the current feature branch with a descriptive message **unless** the branch is protected (integration/release) — then say so and record the uncommitted paths in the handoff instead |
| Branch has an upstream (`git rev-parse --abbrev-ref @{u}`) and commits ahead | Push |
| Open PR for this branch (`gh pr view --json number,state,mergeable,url` — pass `--repo` if the project notes say `gh` resolves the wrong remote) | Record number, state, CI/mergeable, what blocks it |
| Facts learned this session that outlive it (decisions, gotchas, external state) and are not in code/git | Save them to memory now (one file per fact, index line in `MEMORY.md`); the handoff *points* at memory, it does not duplicate it |
| Gates / tests | Record the last result you actually saw and the exact command to re-run — never "tests pass" without the command |
| Background processes, worktrees, stray files | Note them; leave nothing running that the next session would not expect |

### A4 · Write the handoff file

Markdown, this structure, tables wherever content repeats:

```
# HANDOFF — <purpose, one line>

**Consume this first.** Read, absorb, then delete it (`/handoff resume <this path>` does both).
Other `*-handoff.md` files beside it belong to other sessions — leave them.

## The task
<2–5 sentences: what the next session does, what "done" looks like, what it must NOT do>

## Where things are
| | |
|---|---|
| Branch | `<name>` @ `<short sha>`, tracks `<remote/branch>`, <ahead/behind> |
| PR | #<n> — <state, CI, mergeable, what blocks> — or "none" |
| Uncommitted | <paths> — or "nothing" |
| Plan / spec | <path + section that names the work> |
| Last gate result | `<command>` → <what it returned, when> |

## Decisions taken this session (not visible in code or git)
| Decision | Why | Revisit when |
|---|---|---|

## Traps
<Things that look fine and are not. Each: symptom → cause → what to do. Omit section if none.>

## Standing rules still binding
<Only the ones this task will actually touch, each pointing at its source file/section — not a re-paste of CLAUDE.md>

## Memory to read
<memory file names, one line each with why>

## Suggested opening
1. <first concrete action>
2. <second>
```

Everything in it must be traceable — cite the file, the PR, the command. Where the honest
statement is "unknown", write that. Do not bump any document's version.

### A5 · Mark the handoff active

Insert at the very top of the memory index `MEMORY.md` (path is in the Memory section of your
system prompt), above the heading:

```
- ACTIVE HANDOFF: <absolute path> — <purpose>; read it first, then delete it
```

If an older `ACTIVE HANDOFF:` line for a *different* file is still there, leave it and tell the
user it exists — it is another session's, not yours to remove.

### A6 · Print the initial prompt for the next session

End with this block, verbatim shape, so the user can copy it in one motion:

````
Paste this as the first prompt of the next session:

```
/handoff resume <absolute path to the handoff file>
```
````

Then one line of what the next session will do, and one line confirming the file path and
whatever was committed/pushed. Nothing else after the block.

Example ending:

````
Paste this as the first prompt of the next session:

```
/handoff resume ~/project-docs/payment-retry-handoff.md
```
````

Next session: add retry with backoff to the payment webhook (plan §3.2).
Handoff at `~/project-docs/payment-retry-handoff.md`; branch `feature/payment-retry` pushed, nothing uncommitted.

---

## B · RESUME mode

`$ARGUMENTS` after `resume ` is the handoff path (expand `~`). The purpose is to absorb it
and remove it so it cannot go stale and mislead a later session.

### B1 · Read

If the file does not exist: say so, check `MEMORY.md` for an `ACTIVE HANDOFF:` line that names
the intended file, and stop — do not guess at a different handoff.

Read the whole file. Restate, in your own words and in a short table: the task, the branch/PR
state it claims, the first action.

### B2 · Verify before trusting

The handoff is a snapshot; the world may have moved. Check the claims that are cheap to check:

- branch exists and its head/upstream match; uncommitted paths listed are (or are not) still there
- PR state (`gh pr view`, with `--repo` if the project notes require it)
- every path it cites exists

Report any drift plainly ("handoff says PR #27 open; it merged since"). Drift changes the
opening steps, not the task.

### B3 · Delete the handoff — this is not optional

| Where the file is | How to delete |
|---|---|
| Tracked in a git repo, on a branch that is **not** protected | `git rm <file>` and commit: `chore: consume handoff — <purpose>` ; push if the branch has an upstream |
| Tracked, but the current branch is protected | Do not commit here. `rm` the working copy is **wrong** too (it would show as a deletion on a protected branch). Tell the user the deletion must ride the next feature branch, and delete it as the first commit once that branch exists |
| Untracked, or outside any repo | `rm <file>` |

Then remove the matching `ACTIVE HANDOFF:` line from `MEMORY.md` (only the line naming this
file). Do not add a "consumed" line — memory holds facts, not receipts; anything durable from
the handoff was already saved as a memory fact when it was written (if you find something
durable that was not, save it now as its own memory file).

Confirm in one line: file deleted (how), memory line removed.

### B4 · Start the work

Read the memory files the handoff named. Then begin at "Suggested opening", step 1, adjusted
for any drift found in B2. If the task needs a feature branch and the project has a
branch-start command (e.g. `/gitflow-guard:start`), use it before the first edit.
