# delivery-discipline

Three habits that keep delivered work honest. No hooks, no gates — these are
judgement, and a grep cannot hold them.

| Skill | When |
|---|---|
| `verify` | Closing out a task or handing work over |
| `claims` | Before a release or a client deliverable |
| `vocabulary` | Setting up or enforcing the project's naming list |

## `verify` — end with manual verification steps

Finish a task with the concrete steps to confirm it: exact commands with the env
vars and directory they need, what to click, and what a passing result looks
like — then split the list into **what you already ran and what it returned**
versus **what the reader still has to run**.

Keeping those apart is the point. A merged list reads as "all verified", and the
reader finds out otherwise at the worst possible moment.

It also carries the rule that catches the most confident mistakes: **UI is
verified in a real browser, never by reading component source.** The source can
be correct while the rendered result is wrong — wrong element mounted, style not
applied, state never reached, build not rebuilt.

## `claims` — do not write what you cannot show

> Do not write a capability, test-coverage, security or readiness claim unless it
> is traceable to code or to an audit finding. Cite the file, or cite the
> finding. Where code and documents disagree, trust the code.

A liability control, not a style preference: claims in a repository become
delivery obligations, and in enterprise procurement acceptance testing gates
payment against exactly these sentences.

Also enforces that **every number carries its dataset label** — `recall 0.981 on
entities@2.1.0 validation`, never a bare `0.981`. A figure without provenance
cannot be reproduced and silently survives the dataset changing underneath it.

## `vocabulary` — the naming list binds code too

A vocabulary that binds only client documents does not hold: the term drifts in
the code first — a variable, a log line, a PR title — then leaks back through
the people who read the code every day.

Sets up `.vocabulary.md` if there isn't one, and checks retired terms across
source rather than only docs. It distinguishes a genuine violation from a
third-party field really named `whitelist`, and from a changelog entry recording
what was true then — history does not get rewritten to match current usage.

## Install

```
/plugin marketplace add siddiqian-developer/claude-plugins
/plugin install delivery-discipline@siddiqian-plugins
```

Independent of the other plugins in this marketplace.

## Changing this plugin

See [DEVELOPING.md](DEVELOPING.md).
