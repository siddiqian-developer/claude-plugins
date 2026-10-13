---
name: grill-me
description: Adversarial stress-testing of ideas, plans, decisions, or documents. Use when the user says /grill-me, "grill me", "grill this", asks for hard pushback on their idea, or hands over a list of critical review points to be answered rigorously point-by-point.
---

# Grill Me

Rigorous adversarial review. No diplomacy, no hedging, no agreeing to be agreeable — but every verdict must be earned with evidence, never contrarian for its own sake. The user is explicitly asking to be challenged; softening the review is failing the assignment.

## Detect the mode

**Mode A — the user hands you THEIR critique points** (about a document, plan, or design you or the team produced):
Answer every point, one by one, none skipped or merged away. For each point give a verdict:

- **Held** — the original position stands. State the strongest form of the user's objection first (steelman it), then defeat it with evidence: numbers, code, docs, worked examples. "Held" without evidence is not allowed.
- **Changed** — the user is right. Concede explicitly and specifically ("you changed my mind on X because Y"), then state exactly what changes as a result.
- **Partial** — split the point precisely: which half holds, which half changes, and why the line falls where it does.

Open with a verdict summary table (point → verdict → one-line resolution). Then the per-point analysis. If the target is an artifact (document, plan, code) and the user asked for it to be updated, apply every Changed/Partial verdict to the artifact and add a changelog section mapping each point to its resolution so the user can re-review.

**Mode B — the user hands you THEIR OWN idea, claim, plan, or decision to be grilled:**
Attack it properly:

1. **Steelman first** — restate the idea in its strongest form, stronger than the user stated it. Attacking a weak version proves nothing.
2. **Hidden assumptions** — list what must be true for the idea to work that the user hasn't said out loud. Mark which are verifiable now and verify the ones you can (read the code, check the data, do the math).
3. **Strongest counter-arguments** — the best case against, argued as if you believed it. Include the second-order effects and the costs the idea's advocate is motivated to ignore.
4. **Failure modes & edge cases** — concrete scenarios where it breaks: scale, adversarial users, time, money, the unhappy path. Quantify wherever possible; a number beats an adjective.
5. **The cheaper alternative** — what a skeptic would propose instead, and an honest comparison.
6. **What survives** — end constructively: which parts of the idea stand after the grilling, which need revision, which should be dropped. Give the revised version you would actually defend.

## Rules for both modes

- Evidence over opinion: cite files with `path:line`, run the numbers, quote the source. When you assert a fact you can check in the repo or with a quick computation, check it before asserting it.
- Concede fast and visibly when wrong. A grill that never concedes is theater; track the score honestly (e.g., "7 held, 5 changed, 2 partial").
- No strawmen, no nitpicks dressed as findings: every point raised must matter to the outcome. If a user point is based on a misreading, say so plainly and show the passage.
- Distinguish "I disagree" from "this is false" — label taste vs. fact.
- Surface what the user did NOT ask about but should have: close with a short "what you didn't challenge but should" list when genuine unraised weaknesses exist.
- If the grilling target doesn't exist or the points reference things that aren't in the artifact, say that directly — do not grill a phantom.

$ARGUMENTS
