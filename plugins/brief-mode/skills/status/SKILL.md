---
name: status
description: Report whether brief mode is on or off. Use when the user says /brief-mode:status.
disable-model-invocation: true
---

Run `test -f ~/.claude/brief-mode.off && echo off || echo on` and reply with one line: "Brief mode is <on|off>."
