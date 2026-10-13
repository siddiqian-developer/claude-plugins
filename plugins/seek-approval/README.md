# seek-approval

Get an instruction understood and every consequential decision approved **before**
anything is built. For people who want Claude to ask instead of guess.

| Skill | Invoke | Does |
|---|---|---|
| `seek-approval` | `/seek-approval:seek-approval <instruction>` | Classifies the input, then runs understanding, decisions, or both |
| `seek-approval-understanding` | loaded by the entry skill | Splits the instruction into atomic points; one question per point with four readings that differ in what would be done |
| `seek-approval-build-decisions` | loaded by the entry skill | Splits the build into decisions; asks the consequential ones in batches of four |
| `grill-me` | `/seek-approval:grill-me <idea>` | Adversarial review: steelman, hidden assumptions, counter-arguments, failure modes, the cheaper alternative |

Every question has exactly four genuine options, the recommended one first with
its reason. Both flows grill their own options before asking and the approved set
after, and put each finding to you as another four-option question.

## Install

```
/plugin marketplace add siddiqian-developer/claude-plugins
/plugin install seek-approval@siddiqian-plugins
```
