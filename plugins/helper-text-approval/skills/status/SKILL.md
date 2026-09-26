---
name: status
description: Report whether helper-text approval is on, and with how many suggestions. Use when the user says /helper-text-approval:status.
disable-model-invocation: true
---

Run `cat ~/.claude/helper-text-approval.on 2>/dev/null || echo off` and reply with one line:
"Helper-text approval is on: <count> suggestions per question." or "Helper-text approval is off."
