#!/usr/bin/env python3
"""gitflow-guard — Claude Code hook entry point.

One script, three modes, dispatched by argv[1]:

    guard-bash      PreToolUse on Bash      hard-denies work on protected branches
    session-start   SessionStart            reports git posture into the session
    prompt-check    UserPromptSubmit        nudges when new work starts on a protected branch

Contract notes that matter, because getting them wrong fails *silently*:

  * stdout must contain the JSON object and nothing else. Any stray print
    breaks parsing and the hook has no effect, with no error shown.
  * exit 0 with no stdout means "no opinion" — the tool proceeds normally.
  * A deny is exit 0 plus permissionDecision: "deny".

Everything here fails open. If this script cannot parse the input, cannot find
git, or hits an unexpected error, it prints nothing and exits 0. A guard that
bricks someone's commit is worse than a guard that occasionally misses one.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys

TIMEOUT = 5

# --------------------------------------------------------------------------
# Output helpers. Exactly one JSON object, or nothing at all.
# --------------------------------------------------------------------------


def emit(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj))
    sys.exit(0)


def silent() -> None:
    sys.exit(0)


def deny(reason: str) -> None:
    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    )


def note(event: str, context: str) -> None:
    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": event,
                "additionalContext": context,
            }
        }
    )


# --------------------------------------------------------------------------
# git and config
# --------------------------------------------------------------------------


def git(cwd: str, *args: str) -> str | None:
    """Run a git command, returning stripped stdout, or None on any failure."""
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def repo_root(cwd: str) -> str | None:
    return git(cwd, "rev-parse", "--show-toplevel")


def current_branch(cwd: str) -> str | None:
    """Branch name, or None on a detached HEAD."""
    return git(cwd, "symbolic-ref", "--quiet", "--short", "HEAD") or None


_CFG_LINE = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$')


def read_config(root: str) -> dict[str, str]:
    """Parse the flat subset of .gitflow.toml we use.

    Deliberately not a TOML parser. The file is written by this plugin and only
    ever holds `key = "value"` lines, which keeps it readable by the POSIX sh
    git hooks as well as from here.
    """
    cfg = {"main": "main", "dev": "dev", "feature_prefix": "feature/",
           "protected": "main dev", "remote": ""}
    path = os.path.join(root, ".gitflow.toml")
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if line.lstrip().startswith("#"):
                    continue
                m = _CFG_LINE.match(line)
                if not m:
                    continue
                key, val = m.group(1), m.group(2)
                val = re.sub(r"\s*#.*$", "", val).strip().strip('"')
                if val:
                    cfg[key] = val
    except OSError:
        pass
    return cfg


def remote_name(cwd: str, cfg: dict[str, str]) -> str | None:
    """Which remote to compare against.

    Not every repository calls it `origin` — assuming so meant the ancestry
    check silently skipped, which is the worst outcome for a check: it looked
    like it ran and it had not. Order: the config, then the branch's upstream,
    then `origin`, then the only remote if there is exactly one.
    """
    if cfg.get("remote"):
        return cfg["remote"]

    upstream = git(cwd, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if upstream and "/" in upstream:
        return upstream.split("/", 1)[0]

    remotes = (git(cwd, "remote") or "").split()
    if "origin" in remotes:
        return "origin"
    return remotes[0] if len(remotes) == 1 else None


def protected_branches(cfg: dict[str, str]) -> list[str]:
    return [b for b in cfg.get("protected", "").split() if b]


# --------------------------------------------------------------------------
# Command analysis
# --------------------------------------------------------------------------

# Splits a compound shell command into its separate invocations. Not a shell
# parser — it does not understand quoting around the separators themselves —
# but it is accurate for the shapes that matter here.
_SPLIT = re.compile(r"(?:\|\||&&|;|\||\n)")


def git_invocations(command: str) -> list[list[str]]:
    """Every `git ...` invocation in a possibly-compound command."""
    found: list[list[str]] = []
    for segment in _SPLIT.split(command):
        segment = segment.strip()
        if not segment:
            continue
        try:
            tokens = shlex.split(segment)
        except ValueError:
            # Unbalanced quotes. Fall back to a crude split so an obvious
            # `git commit` is still caught rather than silently allowed.
            tokens = segment.split()
        # Skip leading VAR=value assignments and a `sudo`/`command` prefix.
        while tokens and ("=" in tokens[0].split(" ")[0] and not tokens[0].startswith("-")):
            tokens = tokens[1:]
        while tokens and tokens[0] in ("sudo", "command", "nohup"):
            tokens = tokens[1:]
        if tokens and os.path.basename(tokens[0]) == "git":
            found.append(tokens[1:])
    return found


def strip_global_flags(args: list[str]) -> tuple[list[str], str | None]:
    """Remove git's own options, returning (remaining, -C directory if given)."""
    cdir = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-C" and i + 1 < len(args):
            cdir = args[i + 1]
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        break
    return args[i:], cdir


def push_targets(args: list[str], branch: str | None) -> tuple[list[str], bool]:
    """Branches a `git push` would write to, and whether it forces.

    `git push` with no refspec pushes the current branch. `git push origin dev`
    and `git push origin HEAD:dev` both target dev.
    """
    force = any(
        a in ("-f", "--force") or a.startswith("--force-with-lease") or a.startswith("--force-if-includes")
        for a in args
    )
    positionals = [a for a in args[1:] if not a.startswith("-")]

    if len(positionals) <= 1:
        # `git push` or `git push <remote>`: the current branch.
        return ([branch] if branch else [], force)

    targets = []
    for ref in positionals[1:]:
        ref = ref.lstrip("+")
        if ref.startswith("--"):
            continue
        # src:dst -> dst is what gets written
        dst = ref.split(":", 1)[1] if ":" in ref else ref
        dst = dst.replace("refs/heads/", "")
        if dst:
            targets.append(dst)
    if any(a.startswith("+") for a in positionals[1:]):
        force = True
    return (targets, force)


# --------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------


def mode_guard_bash(payload: dict) -> None:
    command = (payload.get("tool_input") or {}).get("command") or ""
    if not command.strip():
        silent()

    cwd = payload.get("cwd") or os.getcwd()
    invocations = git_invocations(command)
    if not invocations:
        silent()

    root = repo_root(cwd)
    if not root:
        silent()

    cfg = read_config(root)
    protected = protected_branches(cfg)
    branch = current_branch(cwd)
    dev = cfg["dev"]
    prefix = cfg["feature_prefix"]

    warnings: list[str] = []

    for raw in invocations:
        args, cdir = strip_global_flags(raw)
        if not args:
            continue
        sub = args[0]

        # -- commit on a protected branch: HARD DENY --------------------------
        if sub == "commit":
            if branch and branch in protected:
                deny(
                    f"Refusing to commit directly to '{branch}', which is a protected "
                    f"branch in this repository's .gitflow.toml.\n\n"
                    f"Put the work on its own branch first:\n"
                    f"    /gitflow-guard:start <short-name>\n\n"
                    f"which cuts {prefix}<short-name> from origin/{dev} so its ancestry "
                    f"is correct, then commit there and open a pull request into {dev}.\n\n"
                    f"Do not work around this by passing --no-verify or by editing "
                    f".gitflow.toml. If the commit genuinely belongs on {branch}, say so "
                    f"and let the user make that call."
                )

        # -- push to a protected branch: HARD DENY ---------------------------
        elif sub == "push":
            targets, force = push_targets(args, branch)
            hit = [t for t in targets if t in protected]
            if hit:
                which = ", ".join(sorted(set(hit)))
                verb = "force-push to" if force else "push directly to"
                deny(
                    f"Refusing to {verb} '{which}', which is protected in this "
                    f"repository's .gitflow.toml.\n\n"
                    f"Protected branches take work by pull request so the change is "
                    f"reviewed and the checks run before it lands:\n"
                    f"    /gitflow-guard:ship\n\n"
                    f"Do not work around this by editing .gitflow.toml or renaming the "
                    f"branch. If this push is genuinely necessary, ask the user."
                )
            if force and targets:
                warnings.append(
                    f"force-push to {', '.join(targets)} — this rewrites published "
                    f"history and anyone who has pulled it will need to recover."
                )

        # -- bare stash: WARN -------------------------------------------------
        elif sub == "stash":
            rest = args[1:]
            action = next((a for a in rest if not a.startswith("-")), None)
            tagged = any(a in ("-m", "--message") for a in rest)
            if action in (None, "push", "save") and not tagged:
                warnings.append(
                    "bare `git stash` — the stash stack is shared across all worktrees "
                    "and other sessions of this repository, so an untagged entry can be "
                    "popped by someone else. Prefer a temporary WIP commit, or "
                    "`git stash push -u -m \"<unique-tag>\"` and recover it later with "
                    "`git stash apply <sha>` rather than `pop`."
                )
            elif action == "pop":
                warnings.append(
                    "`git stash pop` — the stash stack is shared across worktrees, so "
                    "this can pop an entry another session pushed. Find your own entry "
                    "by tag in `git stash list` and use `git stash apply <sha>`."
                )

    if warnings:
        note("PreToolUse", "gitflow-guard warnings:\n- " + "\n- ".join(warnings))

    silent()


def mode_session_start(payload: dict) -> None:
    cwd = payload.get("cwd") or os.getcwd()
    root = repo_root(cwd)
    if not root:
        silent()

    cfg = read_config(root)
    protected = protected_branches(cfg)
    branch = current_branch(cwd)
    dev, main = cfg["dev"], cfg["main"]

    lines: list[str] = []
    configured = os.path.exists(os.path.join(root, ".gitflow.toml"))

    if not configured:
        lines.append(
            "This repository has no .gitflow.toml. gitflow-guard is running with "
            f"defaults (main={main}, dev={dev}, protected='{' '.join(protected)}'). "
            "Run /gitflow-guard:setup to configure it."
        )

    if branch is None:
        lines.append("HEAD is detached — not on a branch.")
    elif branch in protected:
        lines.append(
            f"On '{branch}', which is PROTECTED. Commits and pushes here will be "
            f"denied. Start work with /gitflow-guard:start <short-name> before editing."
        )
    else:
        lines.append(f"On '{branch}'.")
        rem = remote_name(cwd, cfg)
        base = f"{rem}/{dev}" if rem else None
        if base is None:
            lines.append(
                "No remote to compare against, so the ancestry of this branch was not "
                "checked. Set `remote` in .gitflow.toml if this repository's remote is "
                "not called origin."
            )
        elif git(cwd, "rev-parse", "--quiet", "--verify", base) is not None:
            merged = subprocess.run(
                ["git", "merge-base", "--is-ancestor", base, "HEAD"],
                cwd=cwd,
                capture_output=True,
                timeout=TIMEOUT,
            )
            if merged.returncode != 0:
                lines.append(
                    f"This branch is NOT descended from {base}. It was probably cut "
                    f"from the wrong branch, which drags unrelated history into {dev} "
                    f"at merge time."
                )

    # The failure mode the whole plugin exists to prevent: a repository that
    # looks protected and is not.
    hooks_path = git(cwd, "config", "--get", "core.hooksPath")
    if hooks_path is None:
        lines.append(
            "Terminal git hooks are NOT installed (core.hooksPath is unset), so work "
            "done outside Claude Code is unguarded. /gitflow-guard:setup installs them."
        )
    elif os.path.isabs(hooks_path):
        lines.append(
            f"core.hooksPath is an absolute path ({hooks_path}). That breaks for "
            "everyone else who clones this repository; it should be relative."
        )

    dirty = git(cwd, "status", "--porcelain")
    if dirty:
        lines.append(f"{len(dirty.splitlines())} uncommitted change(s) in the working tree.")

    if not lines:
        silent()

    note("SessionStart", "gitflow-guard:\n- " + "\n- ".join(lines))


# Phrases that read as "begin new work" rather than "answer a question".
_NEW_WORK = re.compile(
    r"\b(let'?s\s+(start|build|add|implement|do|work)|"
    r"start\s+(work|working|on|a\s+new)|"
    r"implement\s|add\s+(a\s+)?(new\s+)?(feature|endpoint|page|command)|"
    r"build\s+(a|the)\s|"
    r"work\s+on\s|next\s+task|pick\s+up\s+)",
    re.IGNORECASE,
)


def mode_prompt_check(payload: dict) -> None:
    prompt = payload.get("prompt") or ""
    if not prompt.strip() or not _NEW_WORK.search(prompt):
        silent()

    cwd = payload.get("cwd") or os.getcwd()
    root = repo_root(cwd)
    if not root:
        silent()

    cfg = read_config(root)
    branch = current_branch(cwd)
    if not branch or branch not in protected_branches(cfg):
        silent()

    note(
        "UserPromptSubmit",
        f"gitflow-guard: this reads as the start of new work, and the repository is "
        f"on the protected branch '{branch}'. Commits here will be denied. Run "
        f"/gitflow-guard:start <short-name> to cut a branch from origin/{cfg['dev']} "
        f"before making any edits. If the user is only asking a question, ignore this.",
    )


MODES = {
    "guard-bash": mode_guard_bash,
    "session-start": mode_session_start,
    "prompt-check": mode_prompt_check,
}


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in MODES:
        silent()
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        silent()
    if not isinstance(payload, dict):
        silent()
    MODES[sys.argv[1]](payload)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException:
        # Fail open, always. A guard that breaks git is worse than one that misses.
        sys.exit(0)
