#!/usr/bin/env python3
"""changelog-keeper — PostToolUse nudge after a commit.

Watches for a `git commit` that succeeded, reads the commit it produced, and —
when the change is notable — suggests the Keep a Changelog entry for it.

It suggests. It does not write.

The entries in a good CHANGELOG are curated prose: they cite files, they state
caveats honestly, and they are written for someone who was not there. A line
generated from a commit subject is none of those things. Producing the draft and
letting a person edit it is the useful division of labour; producing the final
text is not.

stdout must be one JSON object or nothing at all — a stray print makes the hook
silently do nothing.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

TIMEOUT = 5

# Conventional Commits type -> Keep a Changelog section.
SECTION = {
    "feat": "Added",
    "fix": "Fixed",
    "perf": "Changed",
    "refactor": "Changed",
    "revert": "Removed",
}

# Types that do not earn a changelog line unless they break something.
QUIET = {"docs", "chore", "style", "ci", "build", "test"}

HEADER = re.compile(r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?:\s*(?P<desc>.+)$")


def emit(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj))
    sys.exit(0)


def silent() -> None:
    sys.exit(0)


def git(cwd: str, *args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def looks_like_commit(command: str) -> bool:
    """Did this command contain a real `git commit`?"""
    for segment in re.split(r"(?:\|\||&&|;|\||\n)", command):
        tokens = segment.strip().split()
        while tokens and tokens[0] in ("sudo", "command", "nohup"):
            tokens = tokens[1:]
        if not tokens or os.path.basename(tokens[0]) != "git":
            continue
        rest = [t for t in tokens[1:] if not t.startswith("-")]
        # Skip `git -C <dir>` style options when looking for the subcommand.
        if rest and rest[0] == "commit":
            return True
        if "commit" in tokens[1:3]:
            return True
    return False


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        silent()
    if not isinstance(payload, dict):
        silent()

    command = (payload.get("tool_input") or {}).get("command") or ""
    if not looks_like_commit(command):
        silent()

    cwd = payload.get("cwd") or os.getcwd()
    root = git(cwd, "rev-parse", "--show-toplevel")
    if not root:
        silent()

    # A merge commit has two parents. Merges are how work reaches the
    # integration branch; the entries were written on the feature branch.
    parents = git(cwd, "rev-list", "--parents", "-n", "1", "HEAD")
    if parents and len(parents.split()) > 2:
        silent()

    subject = git(cwd, "log", "-1", "--format=%s")
    body = git(cwd, "log", "-1", "--format=%b") or ""
    if not subject:
        silent()

    m = HEADER.match(subject)
    if not m:
        silent()

    ctype = m.group("type")
    scope = m.group("scope")
    desc = m.group("desc")
    breaking = bool(m.group("bang")) or "BREAKING CHANGE" in body

    if ctype in QUIET and not breaking:
        silent()

    section = "Changed" if breaking else SECTION.get(ctype)
    if not section:
        silent()

    # Already handled in this very commit? Then there is nothing to nudge about.
    touched = git(cwd, "show", "--name-only", "--format=", "HEAD") or ""
    if any(line.strip().lower().endswith("changelog.md") for line in touched.splitlines()):
        silent()

    changelog = next(
        (p for p in ("CHANGELOG.md", "docs/CHANGELOG.md") if os.path.exists(os.path.join(root, p))),
        None,
    )

    bullet = f"- {desc}" if not scope else f"- **{scope}**: {desc}"
    if breaking:
        bullet += "  _(breaking)_"

    lines = [
        f"changelog-keeper: this commit is notable ({ctype}"
        + (f"({scope})" if scope else "")
        + (", BREAKING" if breaking else "")
        + f") and {'CHANGELOG.md has not been updated' if changelog else 'this repository has no CHANGELOG.md'}.",
        "",
        f"Suggested entry under ## [Unreleased] -> ### {section}:",
        f"    {bullet}",
        "",
        "Rewrite it before using it — the suggestion is derived from the commit",
        "subject, and a changelog entry should say what changed for a reader who",
        "was not here, cite the files that matter, and state any caveat honestly.",
    ]
    if changelog:
        lines += ["", "Then:", "    git add " + changelog + " && git commit --amend --no-edit"]

    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": "\n".join(lines),
            }
        }
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException:
        sys.exit(0)
