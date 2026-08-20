#!/bin/sh
# gitflow-guard — shared helpers for the git hooks.
#
# Sourced by the hooks in this directory. Pure POSIX sh: no bash, no jq, no
# Python. That is deliberate — these hooks run on every commit in a mixed
# language team, and a hook that needs a toolchain is a hook somebody disables.
#
# Configuration lives in .gitflow.toml at the repository root. Only a flat
# subset of TOML is used (key = "value"), which is both valid TOML for the
# skills that read it and parseable here with sed.

# Repository root. Works inside worktrees.
gf_root() {
  git rev-parse --show-toplevel 2>/dev/null
}

# Read one config key. $1 = key, $2 = default when unset or file missing.
gf_cfg() {
  _gf_key=$1
  _gf_def=$2
  _gf_file="$(gf_root)/.gitflow.toml"

  if [ ! -f "$_gf_file" ]; then
    printf '%s' "$_gf_def"
    return 0
  fi

  # key = "value"  ->  value   (first match wins; trailing space and quotes stripped)
  _gf_val=$(
    sed -n "s/^[[:space:]]*${_gf_key}[[:space:]]*=[[:space:]]*//p" "$_gf_file" \
      | head -n 1 \
      | sed 's/[[:space:]]*#.*$//; s/[[:space:]]*$//; s/^"//; s/"$//'
  )

  if [ -n "$_gf_val" ]; then
    printf '%s' "$_gf_val"
  else
    printf '%s' "$_gf_def"
  fi
}

# The current branch name, or empty on a detached HEAD.
gf_branch() {
  git symbolic-ref --quiet --short HEAD 2>/dev/null
}

# Is $1 one of the protected branches?
gf_is_protected() {
  _gf_b=$1
  [ -n "$_gf_b" ] || return 1
  for _gf_p in $(gf_cfg protected "main dev"); do
    [ "$_gf_b" = "$_gf_p" ] && return 0
  done
  return 1
}

# Colour, but only when stderr is a terminal.
if [ -t 2 ]; then
  GF_RED=$(printf '\033[31m'); GF_YLW=$(printf '\033[33m')
  GF_BLD=$(printf '\033[1m');  GF_OFF=$(printf '\033[0m')
else
  GF_RED=''; GF_YLW=''; GF_BLD=''; GF_OFF=''
fi

gf_die() {
  printf '%s\n' "${GF_RED}${GF_BLD}gitflow-guard: blocked${GF_OFF}" >&2
  printf '%s\n' "$@" >&2
  exit 1
}

gf_warn() {
  printf '%s\n' "${GF_YLW}gitflow-guard:${GF_OFF} $*" >&2
}
