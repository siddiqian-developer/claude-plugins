#!/usr/bin/env python3
"""helper-text-approval — UserPromptSubmit hook.

When the switch is on, Claude must propose UI helper text as a multiple-choice
question (AskUserQuestion) and write only the option the user approves. The
switch is a file holding the number of suggestions per question, so toggling
applies to the next prompt with no restart:

    ~/.claude/helper-text-approval.on   present -> on (contents: count), absent -> off (the default)

stdout must be one JSON object or nothing — a stray print disables the hook.
"""

from __future__ import annotations

import json
import os

ON_FLAG = os.path.expanduser("~/.claude/helper-text-approval.on")
DEFAULT_COUNT = 3
# AskUserQuestion takes 2-4 options per question ("Other" is added automatically).
MIN_COUNT, MAX_COUNT = 2, 4

RULE = """helper-text-approval is on. Before writing or changing any UI helper text \
(field hints and descriptions, placeholder text, tooltips, empty-state notes, inline \
help, confirmation and error wording shown to users), do not write it yourself. First \
ask with AskUserQuestion: one question per piece of helper text, naming where it \
appears (file and component), with exactly {n} suggested wordings as the options, the \
recommended one first and labelled "(Recommended)", each option's description saying \
why. Batch up to 4 questions per call. Write only the wording the user picks, or their \
own text if they choose Other. Suggestions follow the project's UI copy rules. Code \
comments, docs and log messages are not helper text."""


def count() -> int:
    try:
        with open(ON_FLAG) as f:
            n = int(f.read().strip() or DEFAULT_COUNT)
    except ValueError:
        n = DEFAULT_COUNT
    return max(MIN_COUNT, min(MAX_COUNT, n))


def main() -> None:
    if not os.path.exists(ON_FLAG):
        return
    try:
        text = RULE.format(n=count())
    except Exception:
        return
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": text,
    }}))


if __name__ == "__main__":
    main()
