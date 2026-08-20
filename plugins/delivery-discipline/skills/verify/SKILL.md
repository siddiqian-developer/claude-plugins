---
description: Close out a task with a manual verification section — the exact steps to confirm the work, separating what was already run from what the reader still needs to run. Use when finishing a piece of work, handing it over, or when the user asks how to verify something.
---

End the task with a **Manual verification** section. `$ARGUMENTS` may name the
work being closed out.

## The shape

Concrete steps, in order, that someone else can follow:

- **Exact commands**, with the environment variables and the directory they need.
  `pytest -q` is not a step if it only works from `backend/` with a venv active.
- **What to click or look at**, for anything with a UI.
- **What a passing result looks like.** "It should work" is not a result. "Prints
  `755 passed`" is.

Then split the list in two, explicitly:

| | |
|---|---|
| **Already run** | What you ran, and **what it returned** — the real output, including failures |
| **Still to run** | What the reader has to do themselves, and why you could not |

Keeping those separate is the whole point. A merged list reads as "all verified",
and the reader discovers otherwise at the worst moment.

## This does not replace running things

Run the gates yourself first, then say how to re-run them. A verification
section written instead of testing is worse than none, because it looks like
evidence.

If you could not run something — no credentials, no device, no environment — say
so plainly and put it under **Still to run** with the reason. "Not verified" is a
useful sentence. An unqualified list is not.

## UI is verified in a real browser

**Never by reading component source.** Reading the component and concluding it
works is precisely the failure this exists to prevent: the source can be correct
while the rendered result is wrong — the wrong element mounted, a style not
applied, a state never reached, a build not rebuilt.

Drive the running application and assert on what is rendered. If there is a
headless-browser harness, use it and say which spec ran. If you genuinely cannot
open a browser, that step belongs under **Still to run**, not under **Already
run** with a caveat attached.

The same principle applies to anything with a runtime: look at the running
thing, not at the code that should produce it.

## Honesty rules for the section

- Report what the command actually returned, not what it should return.
- If a test fails, show the failure. A green summary over a red run is the
  single most expensive thing this section can contain.
- If a step is flaky, say so and say how often.
- Do not list steps you invented and never tried — mark them **Still to run**.
