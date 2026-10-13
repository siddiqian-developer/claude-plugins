---
name: seek-approval-build-decisions
description: Before building anything or making decisions, get each decision interactively approved — 4 options each, recommended first with why
---

Nothing in $ARGUMENTS gets built, edited, installed, deployed or decided
unilaterally. Every consequential decision goes to the user via AskUserQuestion.
If $ARGUMENTS is empty, use the task currently under discussion; if there is
none, ask what to decide.

1. **Split into atomic decisions.** Break the input into the smallest
   separately decidable choices — one choice each, never a bundle ("which
   library and where it lives" is two decisions). Cover approach, scope,
   tooling, sequencing, naming, where changes live, edge cases, failure
   behaviour.
2. **Filter to consequential.** A decision is consequential when a wrong choice
   costs real rework, is hard to reverse, or visibly changes the outcome. The
   rest are *forced* (by the codebase or the user's own words) or *defaulted*
   (the obvious choice). Don't output the split as a table — name the forced
   and defaulted ones in one line with their reasons, so the user can override.
3. **Ask in dependency order.** If a boundary is doubtful (one decision or
   two?), ask about it first. Ask the consequential ones in batches of up to 4
   per call, `header` = `Decision N`, grouped so each call reads as one
   coherent sheet. A decision whose options depend on an earlier answer goes
   in a later batch than that answer, never the same one.
4. Every question: exactly 4 options, `multiSelect: false` unless parallel
   choices genuinely apply. Recommended first, labelled `(Recommended)`. All
   options genuine — "defer this decision" or "decide after seeing X" are real
   choices; fake padding is not. Don't mention the free-text "Other".
5. The recommendation's `description` (1–2 sentences) carries the reason: what
   it buys, what it costs, what it rules out. No recommendation without one.
   Trade-offs go there, not in the label.
6. After each batch, continue — no restating of choices. Between batches only
   read-only or reversible work is allowed; nothing is written, installed or
   deployed until the after-set grill (below) is settled.

**Grill with `grill-me`** — load it via the Skill tool (`seek-approval:grill-me`; fallback: Read `../grill-me/SKILL.md`
relative to this skill's base directory) and apply its Mode B checks (hidden
assumptions, strongest counter-arguments, failure modes, cheaper alternative) —
but **not its output format**. Every finding reaches the user only as an
AskUserQuestion question in this skill's style: tied to its decision
(`header` = `Grill DN`, e.g. `Grill D3`), the finding stated in the question,
exactly 4 genuine ways to resolve it, recommended first with the why in its
`description`. No steelman prose, no verdict tables, no score.

- **Before asking a decision**: grill its 4 options and the recommendation.
  Options that don't survive are replaced silently. Findings that need the
  user's call are held until the decision is answered; drop any that no longer
  apply to the chosen option, and ask the rest in the next batch.
- **After all decisions are approved**: grill the approved set once as a
  whole — clashes between choices, hidden assumptions, failure modes. Each
  finding becomes a grill question, batched up to 4 per call. Nothing found →
  one line saying so, then proceed.
- **Grilling terminates.** Each decision is grilled once before asking, and
  the set once after. A decision changed by a grill answer is not grilled
  again; the after-set grill does not repeat.

A new consequential decision mid-work: give it the next number, then stop and
ask the same way. Never merge decisions to save questions. An approval covers
exactly what was asked. Never substitute "is this OK?" for options, never
summarise this prompt.
