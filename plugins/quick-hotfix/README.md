# quick-hotfix

One small fix while you are testing live in the UI. Speed over ceremony, with a
floor that never moves: no fail-closed path, auth check, egress or data-leak
control and no secret's handling is loosened to make a fix quick.

| Skill | Invoke | Does |
|---|---|---|
| `quick-hotfix` | `/quick-hotfix:quick-hotfix [budget] [none\|touched\|project] [--commit] <issue>` | The fix, focused tests within the budget, the static checks at the chosen level, a three-line reply |
| `quick-hotfix-ui` | `/quick-hotfix:quick-hotfix-ui ...` | The same, frontend only: refuses before editing if any part of the fix is outside the frontend root |
| `quick-hotfix-seek-approval` | `/quick-hotfix:quick-hotfix-seek-approval ...` | Approves the reading first (needs the `seek-approval` plugin) |
| `quick-hotfix-ui-seek-approval` | `/quick-hotfix:quick-hotfix-ui-seek-approval ...` | Both of the above |

Test budget defaults to 50 (`0` = none); static checks default to `touched`. It
never commits unless `--commit`, never pushes, and never restarts your services:
it tells you what to restart.

## Install

```
/plugin marketplace add siddiqian-developer/claude-plugins
/plugin install quick-hotfix@siddiqian-plugins
/plugin install seek-approval@siddiqian-plugins     # only for the -seek-approval variants
```
