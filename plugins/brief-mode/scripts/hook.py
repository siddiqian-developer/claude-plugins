#!/usr/bin/env python3
"""brief-mode — UserPromptSubmit hook.

When the switch is on, every prompt is answered as if it began with "be brief:".
A prompt that starts with "exp:" (exact, case-sensitive, colon included) is
exempt for that one message. The switch is a file, so toggling applies to the
next prompt with no restart:

    ~/.claude/brief-mode.off   present -> off, absent -> on (the default)

A hook cannot rewrite the prompt; it adds the instruction as context next to it.
stdout must be one JSON object or nothing — a stray print disables the hook.
"""

from __future__ import annotations

import json
import os
import sys

OFF_FLAG = os.path.expanduser("~/.claude/brief-mode.off")
ESCAPE = "exp:"

# The "be brief:" prefix plus the Concise output-style rules it was used with.
BRIEF = """be brief: — Brief mode is on for this message. Keep responses short and \
direct while doing the work just as thoroughly:
1. Lead with the result — the first sentence answers "what happened" or "what's \
the answer". No preamble ("Let me...") and no closing recap.
2. Cut narration, keep substance — don't restate the request, the plan, or each \
step. Report outcomes, decisions, and anything the user must act on.
3. Short by default — simple questions get 1-3 sentences of plain prose. Use \
headers, tables and lists only when they carry real structure.
4. State things plainly — mention a caveat only when it changes what the user \
should do next.
5. Never trade correctness for brevity — errors, failing output, security \
warnings and destructive-action confirmations keep their full content.
The user can start a message with "exp:" to get a full, detailed answer."""

EXPAND = """exp: — the user asked for a full, detailed explanation of this \
message. Brief mode does not apply to it; answer completely."""


def main() -> None:
    if os.path.exists(OFF_FLAG):
        return
    try:
        prompt = json.load(sys.stdin).get("prompt", "") or ""
    except Exception:
        return
    text = EXPAND if prompt.lstrip().startswith(ESCAPE) else BRIEF
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": text,
    }}))


if __name__ == "__main__":
    main()
