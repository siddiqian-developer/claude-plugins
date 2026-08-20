---
description: Set up or enforce the project's own naming list across code, comments, PRs and standups — not just client documents. Use when the user wants consistent terminology, has a glossary to enforce, or asks to check naming.
---

Enforce the project's naming list. `$ARGUMENTS` may name a term or a path to
check.

A vocabulary that binds only client documents does not hold. The term drifts in
the code first — a variable, a log line, a PR title — and then leaks back into
the documents through the people who read the code every day.

## 1. Find the list

Look for an existing one: a glossary in the docs, a naming section in a
blueprint or spec, a `terminology.md`. Read it rather than inventing one.

If none exists, offer to create `.vocabulary.md` at the project root:

```markdown
# Vocabulary

| Say | Not | Why |
|---|---|---|
| allowlist | whitelist | — |
| <term> | <what people say instead> | <what the distinction protects> |

## Reserved
<term> — not in use yet; do not repurpose it.
```

The **Why** column matters more than it looks. A rule with no reason gets
treated as taste and quietly dropped; a rule that says *"these are two different
tenancy planes and mixing them hides a security boundary"* survives.

## 2. Where it binds

**Code, comments, PRs and standups** — not just documents. Specifically:

| Surface | Why it matters |
|---|---|
| Identifiers | The wrong noun in a type name propagates to every call site |
| Log lines and errors | Read by support and by customers |
| PR titles and commits | Become the changelog |
| UI copy | The user-facing consequence of an internal muddle |
| Comments | Where a retired term survives longest |

## 3. Check

Grep each retired term across the source, not only the docs. Report `file:line`
with the surrounding line, so a decision can be made without opening each one.

Distinguish three cases rather than lumping them:

- **A genuine violation** — rename it.
- **A quotation or an external name** — a third-party API field really is called
  `whitelist`; renaming it breaks the integration. Leave it, and say why.
- **A historical record** — a changelog entry or an ADR describing what was true
  then. Do not rewrite history to match current vocabulary.

## 4. Adding a term

**Suggest it explicitly and get approval before adopting it. Never rename
silently.** A term introduced quietly in one PR and spread by copy-paste is how
a project ends up with two words for the same thing and an argument about which
is correct.

Prefer industry-standard terms over invented ones. If the standard term is
genuinely wrong for the domain, say what it fails to capture — that reasoning is
what belongs in the **Why** column.

## 5. A note on names in documents

If the project restricts personal names — role labels rather than individuals —
apply it to code and commits too: comments, PR descriptions and commit trailers
all carry names people forget about, and they outlive the person's involvement.
