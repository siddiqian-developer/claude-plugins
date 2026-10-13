# session-handoff

One session per feature. A session ends by writing a handoff (what the next
session needs that is not visible in the code, the git log or memory); the next
session reads it, checks it against the world, deletes it and starts work.

| Invoke | Does |
|---|---|
| `/session-handoff:handoff <purpose of the next session>` | Commits or records loose work, pushes, saves durable facts to memory, writes the handoff, marks it active in the memory index, prints the one line to paste into the next session |
| `/session-handoff:handoff resume <path>` | Reads it, reports any drift (branch moved, PR merged), deletes it, starts at its first step |

Where the file lives: the location the project's `CLAUDE.md` names, else
`HANDOFF.md` at the repository root.

## Install

```
/plugin marketplace add siddiqian-developer/claude-plugins
/plugin install session-handoff@siddiqian-plugins
```
