# helper-text-approval

A global switch: while it is on, Claude never writes UI helper text on its own. It proposes
wordings as a multiple-choice question and writes only the one you pick.

| You do | Effect |
|---|---|
| `/helper-text-approval:on [count]` | On, starting with the next prompt. `count` = suggestions per question, 2 to 4, default 3 |
| `/helper-text-approval:off` | Off (the default after install) |
| `/helper-text-approval:status` | Shows on or off, and the count |

```
/plugin marketplace add siddiqian-developer/claude-plugins
/plugin install helper-text-approval@siddiqian-plugins
```

Install at **user scope** so it works in every project.

## What counts as helper text

Field hints and descriptions, placeholders, tooltips, empty-state notes, inline help, and
confirmation or error wording shown to users. Code comments, docs and log messages do not.

## How it works

A `UserPromptSubmit` hook adds the rule as context next to your prompt while the switch is on.
Each piece of helper text becomes one question naming where it appears, with `count` wordings,
the recommended one first. You can always choose **Other** to type your own. Up to 4 questions
are asked at once.

The switch is the file `~/.claude/helper-text-approval.on`, which holds the count. The question
UI takes 2 to 4 options, so counts outside that range are clamped.

Requires `python3` on `PATH`. If it is missing, the hook fails open and does nothing.
