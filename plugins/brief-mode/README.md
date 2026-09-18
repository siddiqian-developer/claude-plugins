# brief-mode

A global switch that answers every prompt as if you had typed `be brief:` at the start.

| You do | Effect |
|---|---|
| Type any prompt | Answer is brief: result first, no narration, short by default |
| Start a prompt with `exp:` | That one message gets a full, detailed answer |
| `/brief-mode:off` | Off, starting with the next prompt. No restart needed |
| `/brief-mode:on` | On again (the default after install) |
| `/brief-mode:status` | Shows on or off |

```
/plugin marketplace add siddiqian-developer/claude-plugins
/plugin install brief-mode@siddiqian-plugins
```

Install at **user scope** so it works in every project.

## How it works

A `UserPromptSubmit` hook adds the brief instruction as context next to your prompt. It
cannot rewrite the prompt text itself. The instruction includes the rules of Claude Code's
built-in *Concise* output style, so you get the same behaviour without selecting that style.
The switch is the file `~/.claude/brief-mode.off`: if it exists, the hook does nothing.

`exp:` is matched only at the start of a prompt (leading spaces allowed), case-sensitive and
with the colon, so `regexp:` in the middle of a message does not trigger it.

Requires `python3` on `PATH`. If it is missing, the hook fails open and brief mode simply
does nothing.
