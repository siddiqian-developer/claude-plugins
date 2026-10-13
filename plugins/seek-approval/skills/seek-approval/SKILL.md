---
name: seek-approval
description: Seek approval for whatever the moment calls for — understanding first when it is an instruction, decisions when it is a build
---

Classify $ARGUMENTS, then run the matching flow.

| $ARGUMENTS is… | Flow |
|---|---|
| An instruction to DO or BUILD | UNDERSTANDING, then BUILD-DECISIONS on the approved readings |
| A decision or build proposal | BUILD-DECISIONS |
| A question about code, a doc, or a fact | UNDERSTANDING, then answer — no build flow |
| An idea/plan leading to a build | BUILD-DECISIONS on the consequential parts |
| Ambiguous between two of these | Ask which flow, as a 4-option question |

**UNDERSTANDING** — split the instruction into atomic points (verbatim quote
each, mark implied ones); ask one question per point, up to 4 per call, each
with 4 readings that differ in what you'd actually DO (scope, deliverable,
depth, target, output form); proceed with exactly the approved readings. **When this flow starts** (and not
before), invoke the Skill tool with `skill: "seek-approval:seek-approval-understanding"`,
`args: $ARGUMENTS`, and follow it.

**BUILD-DECISIONS** — split into atomic decisions (one choice each), forced ones
named in one line and not asked; ask the rest in batches of up to 4 questions;
stop and ask again when a new
consequential decision appears. **Load it only when this flow starts** —
after every understanding point is approved (grill questions included), never
alongside understanding. Then invoke the Skill tool with
`skill: "seek-approval:seek-approval-build-decisions"`, `args:` all approved point readings,
one line each as `Point N: <reading>` (or $ARGUMENTS if understanding was
skipped), and follow it.

If the Skill tool can't load one, Read `../<name>/SKILL.md` relative to this
skill's base directory instead. The summaries here are a fallback, not a substitute.

**Grilling, both flows:** each sub-skill runs `grill-me`'s checks on its options
before asking and on the approved set after, and puts every finding to you as a
4-option question in this style — never as a grill-me report.

**Every question, both flows:** exactly 4 real options, recommended first and
labelled `(Recommended)`, its `description` giving the why — what it buys,
costs, rules out. `multiSelect: false` unless parallel choices apply.

**Ordering:** understanding is settled before any build-decision question. Keep
working on what the answers already permit; execute nothing that depends on an
un-asked decision. Never substitute "is this OK?" for options, never summarise
this prompt.
