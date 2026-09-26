---
name: on
description: Turn helper-text approval on globally. Claude proposes UI helper text as a multiple-choice question and writes only the approved wording. Use when the user says /helper-text-approval:on [count]. count = suggestions per question, 2 to 4, default 3.
disable-model-invocation: true
---

Count: the first whole number in "$ARGUMENTS", or 3 if there is none. Clamp it to 2..4
(the question UI takes 2 to 4 options; "Other" is always added for your own wording) and
say so in the reply if you clamped.

Run `mkdir -p ~/.claude && echo <count> > ~/.claude/helper-text-approval.on`, then reply with
one line: "Helper-text approval on: <count> suggestions per question."
