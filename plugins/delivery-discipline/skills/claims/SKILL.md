---
description: Check that capability, coverage, security or readiness claims in the repository are traceable to code or to an audit finding, and that every number carries its dataset label. Use before a release, a client deliverable, or when reviewing README and docs claims.
---

Check what this repository *claims* against what it can *show*. `$ARGUMENTS` may
scope it to a file or a directory.

## The rule

**Do not write a capability, test-coverage, security or readiness claim unless it
is traceable to code or to an audit finding.** Cite the file, or cite the
finding.

This is a liability control, not a style preference. Claims recorded in a
repository become delivery obligations — in enterprise and telco procurement,
acceptance testing gates payment against exactly these sentences. Where the
honest statement is *"bounded, with these limits"*, write that.

**Where code and documents disagree, trust the code.**

## 1. Find the claims

Look where claims accumulate: `README.md`, `docs/`, marketing or positioning
copy, PR descriptions, changelog entries, and any client-facing deliverable.

Claim shapes worth grepping for:

| Shape | Example |
|---|---|
| Capability | "supports", "handles", "works with", "compatible with" |
| Coverage | "fully tested", "100%", "comprehensive" |
| Security | "encrypted", "secure", "isolated", "tamper-proof", "compliant" |
| Readiness | "production-ready", "enterprise-grade", "battle-tested" |
| Performance | any latency or throughput number |
| Autonomy | "automatic", "self-healing", "zero-touch" |

## 2. Trace each one

For every claim found, one of three outcomes — no fourth:

| Outcome | Means |
|---|---|
| **Traceable** | Cite the file, the test, or the audit finding that shows it |
| **Overstated** | The code does less than the sentence. Propose the bounded version |
| **Unsupported** | Nothing shows it. Propose removal, or a statement of intent clearly marked as such |

Do not accept a claim because it is probably true, or because someone would
have noticed. "Probably true" is how an obligation gets signed.

## 3. Numbers carry their dataset label

**Every figure quoted from a dataset carries `name@version`.** `recall 0.981 on
entities@2.1.0 validation`, never a bare `0.981`.

A number without provenance cannot be checked, cannot be reproduced, and invites
the one question nobody can answer in the room. It also silently survives the
dataset changing underneath it, which is worse — the number stays, the thing it
measured is gone.

Check too that the split is named. A number from the tuning split quoted as
though it were validation is not a rounding difference; it is the wrong claim.

## 4. Report

A table of claim, location, verdict, and the citation or the proposed rewrite.
Lead with anything client-facing — that is where a claim converts into an
obligation fastest.

If nothing is overstated, say so plainly. This check passing is a real result,
not an anticlimax.
