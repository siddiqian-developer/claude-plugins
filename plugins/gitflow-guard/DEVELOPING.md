# Developing gitflow-guard

For anyone changing this plugin. The user-facing guide is [README.md](README.md).

## Layout

```
gitflow-guard/
├── .claude-plugin/plugin.json   manifest — ONLY this file may live here
├── hooks/hooks.json             hook registrations
├── scripts/hook.py              all three hooks, one file, dispatched by argv[1]
├── skills/<name>/SKILL.md       six skills
└── templates/
    ├── githooks/                pure POSIX sh — the terminal layer
    └── workflows/gitflow.yml    the CI layer
```

Component directories must sit at the plugin **root**. Anything placed inside
`.claude-plugin/` other than `plugin.json` is silently ignored — no error, it
just never loads.

## The two languages, and why

| Layer | Language | Reason |
|---|---|---|
| Git hooks | POSIX `sh` | They run on every commit, in any repo, on anyone's machine. A hook that needs a toolchain is a hook someone disables |
| Claude hooks | Python 3 | Hook stdout must be **exactly one JSON object**. Hand-rolling JSON escaping in `sh` breaks on the first bash command containing a quote |

Do not "simplify" the Claude hooks into shell. That was considered and rejected.

## The hook contract

Getting this wrong fails **silently** — the hook runs, has no effect, and
reports nothing.

**Deny a tool call** (`PreToolUse`), exit 0 with:

```json
{"hookSpecificOutput":{"hookEventName":"PreToolUse",
 "permissionDecision":"deny","permissionDecisionReason":"..."}}
```

**Inject context** (any event), exit 0 with:

```json
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"..."}}
```

**No opinion**: exit 0, print nothing.

Rules that bite:

- **stdout must be the JSON and nothing else.** A stray `print()` breaks parsing.
  If a shell profile echoes a banner on startup it breaks parsing too.
- `hook_event_name` in the output must match the event that fired.
- The Bash command arrives at `.tool_input.command`; the working directory at
  `.cwd`.
- Matchers: `"Bash"` is an exact tool-name match. Anything containing a
  regex metacharacter is treated as an unanchored regex.

## Fail open, always

Every path in `hook.py` that cannot proceed calls `silent()` — exit 0, no
output. The `main()` wrapper catches `BaseException` and exits 0.

This is deliberate and must not be "fixed". A guard that crashes and blocks a
developer's commit is worse than a guard that occasionally misses one. If you
add a code path, make sure its failure mode is *allow*.

## Testing

There is no test runner; the hooks are exercised by feeding them JSON.

```bash
# a scratch repo on a protected branch
mkdir /tmp/t && cd /tmp/t && git init -b main
printf 'main = "main"\ndev = "dev"\nprotected = "main dev"\n' > .gitflow.toml

echo '{"cwd":"/tmp/t","tool_input":{"command":"git commit -m x"}}' \
  | python3 scripts/hook.py guard-bash
# expect: {"hookSpecificOutput":{...,"permissionDecision":"deny",...}}

echo '{"cwd":"/tmp/t"}' | python3 scripts/hook.py session-start
```

Cases worth keeping green when you change the command parser:

| Command | Expected |
|---|---|
| `git commit -m x` on protected | deny |
| `cd /tmp && git commit -m x` | deny — compound commands are split |
| `echo 'git commit -m x'` | **allow** — quoted, not an invocation |
| `git push origin HEAD:dev` | deny — refspec destination is parsed |
| `git push origin feature/x` | allow |
| `git stash` | warn |
| `git stash push -u -m "tag"` | allow — tagged stashes are safe |
| malformed JSON on stdin | allow, exit 0 |

The git hooks are tested by running real commits in a scratch repo with
`core.hooksPath` pointed at `templates/githooks/`.

## Command parsing

`git_invocations()` splits on `|| && ; |` and newline, then `shlex.split()`s
each segment. It strips leading `VAR=value` assignments and `sudo`/`command`/
`nohup`, then checks whether the executable basename is `git`.

It is not a shell parser and does not need to be. It errs toward *allow*: an
exotic construction it cannot parse is one it does not block.

## Config

`.gitflow.toml` in the consuming repo is a **flat** `key = "value"` subset of
TOML, deliberately. Both the Python hooks and the POSIX `sh` git hooks read it,
and `sh` has no TOML parser. Do not add sections or arrays — `gitflow-lib.sh`
parses it with `sed`.

## Adding a check

1. Decide severity. **Hard-deny only for protected-branch violations.** Anything
   else warns — that boundary was an explicit product decision.
2. Add the logic to `mode_guard_bash()`, appending to `warnings` or calling
   `deny()`.
3. Write a denial reason that tells Claude what to do instead, and says not to
   work around it. Claude reads the reason and self-corrects; a bare "denied"
   causes thrashing.
4. Add the case to the table above and check it by hand.

## Versioning

`plugin.json` has **no `version`** on purpose. A pinned version means users keep
a cached copy until it is bumped; without one, the resolved commit SHA drives
updates. `claude plugin validate` warns about this — the warning is expected.

Add a version only when cutting a deliberate release, and bump it every time
after that.
