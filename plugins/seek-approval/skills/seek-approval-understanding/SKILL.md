---
name: seek-approval-understanding
description: Before doing what you were told, split the instruction into atomic points and get your reading of each point approved — 4 readings per point, recommended first with why
---

Settle what $ARGUMENTS means, point by point, before acting on any of it.
If $ARGUMENTS is empty, use the instruction currently under discussion; if
there is none, ask what to settle.

1. **Split into atomic points.** Break the payload into the smallest separately
   actionable points — one verb, one target each. Split compound sentences
   ("merge X, then delete Y" is two points), and surface implied points too
   (an ordering, a constraint, a "use the same pattern as"), marked *implied*.
2. If a boundary is doubtful (one point or two?), ask about it before
   interpreting it. Don't output the split itself — it shows up as the
   questions.
3. **One question per point.** AskUserQuestion, up to 4 points per call, in
   point order; `header` = `Point N`. Each question: exactly 4 readings,
   `multiSelect: false`. Readings must differ in what you'd actually DO —
   scope, deliverable, depth, target, or output form — not in wording. If a
   point is unambiguous, fill slots with honest variants (broader, narrower,
   "just answer, change nothing"). Never pad with fake options. Don't mention
   the free-text "Other".
4. Recommended first, labelled `(Recommended)`. Its `description` (1–2
   sentences) says why, and what the rival readings would mean in practice.
5. Readings that interact (one point's choice changes another's meaning) get
   re-asked before proceeding.
6. Sub-choices inside a chosen reading (where the result goes, how far to go,
   which files) get the same treatment. Understanding is done when every point
   has an approved one-sentence reading. Then do exactly those points and
   nothing more.

**Grill with `grill-me`** — load it via the Skill tool (`seek-approval:grill-me`; fallback: Read `../grill-me/SKILL.md`
relative to this skill's base directory) and apply its Mode B checks (hidden
assumptions, strongest counter-arguments, failure modes, cheaper alternative) —
but **not its output format**. Every finding reaches the user only as an
AskUserQuestion question in this skill's style: tied to its point
(`header` = `Grill PN`, e.g. `Grill P3`), the finding stated in the question, exactly 4
genuine ways to resolve it, recommended first with the why in its
`description`. No steelman prose, no verdict tables, no score.

- **Before asking a point**: grill its 4 readings and the recommendation.
  Readings that don't survive are replaced silently. Findings that need the
  user's call are held until the point is answered; drop any that no longer
  apply to the chosen reading, and ask the rest in the next batch.
- **After all points are approved**: grill the approved set once as a whole —
  clashes between readings, hidden assumptions, failure modes. Each finding
  becomes a grill question, batched up to 4 per call. Nothing found → one line
  saying so, then proceed.
- **Grilling terminates.** Each point is grilled once before asking, and the
  set once after. A point changed by a grill answer is not grilled again; the
  after-set grill does not repeat.

New ambiguity mid-task: stop and re-ask the same way, for that point only.
Never merge points to save questions, never guess, never proceed silently
after the first answer, never summarise this prompt.
