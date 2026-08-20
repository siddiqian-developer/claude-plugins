# Developing delivery-discipline

For anyone changing this plugin. The user-facing guide is [README.md](README.md).

## Why there are no hooks here

Every other plugin in this marketplace enforces something mechanically. This one
does not, deliberately.

All three skills turn on judgement that a grep cannot make: whether a sentence
overstates what the code does, whether a verification step was really run,
whether a term is a violation or a third-party field name. A hook that tried to
decide those would be wrong often enough to be switched off — and a check that
gets switched off is worse than one that never existed, because the repository
still looks like it has one.

So these are skills, invoked at the moments that matter, and the plugin is
honest about being advisory.

If you find yourself adding a hook, check first whether what you are enforcing is
actually mechanical. `no bare number without an @version` is nearly grep-able and
might belong in a CI job; `this claim overstates the code` is not.

## Layout

```
delivery-discipline/
├── .claude-plugin/plugin.json
└── skills/{verify,claims,vocabulary}/SKILL.md
```

Skills only. No scripts, no templates, no assets — which also means nothing to
keep in sync and nothing that can fail silently.

## Provenance

The rules were extracted from two working repositories where they had already
earned their place:

| Rule | Origin |
|---|---|
| Manual verification section | A personal `CLAUDE.local.md` |
| UI verified in a real browser | A project `CLAUDE.md`, alongside a headless-browser harness |
| Claim discipline | A shared governance document written for telco procurement |
| Dataset labelling | An evals document where a mislabelled split had caused real confusion |

Everything client-specific was left behind: no product names, no host names, no
project-specific commands, no client references. If you extend these, keep that
line — the value is that they transfer, and they stop transferring the moment
they name somebody's stack.

## Editing the skills

**Keep the reasoning, not just the rule.** Each skill states *why* — claims are a
liability control because acceptance testing gates payment; the verification
split matters because a merged list reads as "all verified"; the Why column in a
vocabulary survives where a bare rule gets dropped as taste.

A rule with its reason attached gets followed when it is inconvenient. Without
it, it gets followed only when it is easy, which is when it does not matter.

**Do not soften the honesty clauses.** These are the load-bearing sentences:

- "Report what the command actually returned, not what it should return."
- "If a test fails, show the failure."
- "Do not accept a claim because it is probably true."
- "Never rename silently."

They exist because the failure mode in every case is a confident, plausible,
wrong statement — which is exactly what a language model produces most easily.

**Three outcomes, not four.** The `claims` skill forces traceable / overstated /
unsupported. Adding a fourth ("probably fine", "minor") reopens the gap the skill
closes.

## Testing

There is nothing to execute. Validate the manifest and frontmatter:

```bash
claude plugin validate ./delivery-discipline
```

Beyond that, the test is use: run `verify` on a real task and check whether the
already-run and still-to-run lists are genuinely separated, and run `claims`
against a README you know overstates something and check it catches it.

## Versioning

No `version` in `plugin.json`; the resolved commit SHA drives updates. The
validator warning is expected.
