#!/usr/bin/env bash
# Install (or update) the EPCV agents, commands, skills, and plugins for OpenCode.
#
# Copies the portable parts of this repo's .opencode/ directory into either
# the global OpenCode config directory or a project's .opencode/ directory.
# Re-running the script updates a previous install: every item this repo
# provides is replaced with the current version; anything else in the
# destination (your own agents, commands, skills) is left alone.
#
# Repo-specific files (opencode.json, tui.json, docs) are never installed —
# opencode.json contains machine-local provider and MCP configuration.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./install.sh --global [--symlink]
  ./install.sh --project <path> [--symlink]

Targets:
  --global          Install for all projects, into $XDG_CONFIG_HOME/opencode
                    (default ~/.config/opencode)
  --project <path>  Install into <path>/.opencode for a single project

Options:
  --symlink         Symlink items into place instead of copying, so a
                    `git pull` in this repo updates every install
  -h, --help        Show this help

What gets installed:
  agent/    -> agents/     EPCV agents (explorer, planner, coder, verifier,
                           GeneralCoder) and their subagents
  command/  -> commands/   /explore, /plan, /code, /verify, /epcv, /commit-task
  skills/   -> skills/     the workflow rules each agent loads
  plugins/  -> plugins/    the context-cache plugin

Re-run the same command at any time to update an existing install.
EOF
}

fail() {
  echo "error: $1" >&2
  exit 1
}

target=""
project_path=""
symlink=false

while [ $# -gt 0 ]; do
  case "$1" in
    --global)
      [ -z "$target" ] || fail "specify only one of --global or --project"
      target="global"
      ;;
    --project)
      [ -z "$target" ] || fail "specify only one of --global or --project"
      target="project"
      [ $# -ge 2 ] || fail "--project requires a path"
      project_path="$2"
      shift
      ;;
    --symlink)
      symlink=true
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      usage >&2
      fail "unknown argument: $1"
      ;;
  esac
  shift
done

[ -n "$target" ] || {
  usage >&2
  fail "specify --global or --project <path>"
}

# Resolve the repo's .opencode directory relative to this script.
script_dir="$(cd "$(dirname "$0")" && pwd)"
source_dir="$script_dir/.opencode"
[ -d "$source_dir" ] || fail "source directory not found: $source_dir"

if [ "$target" = "global" ]; then
  dest_root="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
else
  [ -d "$project_path" ] || fail "project path is not a directory: $project_path"
  dest_root="$(cd "$project_path" && pwd)/.opencode"
fi

# Map repo directories (singular) to the destination names the current
# OpenCode docs use (plural). Each entry is "<source subdir>:<dest subdir>".
mappings="agent:agents command:commands skills:skills plugins:plugins"

installed=0
for mapping in $mappings; do
  src_name="${mapping%%:*}"
  dest_name="${mapping##*:}"
  src="$source_dir/$src_name"
  dest="$dest_root/$dest_name"
  [ -d "$src" ] || continue
  mkdir -p "$dest"

  for item in "$src"/*; do
    [ -e "$item" ] || continue
    base="$(basename "$item")"
    rm -rf "${dest:?}/$base"
    if [ "$symlink" = true ]; then
      ln -s "$item" "$dest/$base"
    else
      cp -R "$item" "$dest/$base"
    fi
    installed=$((installed + 1))
    echo "  $dest_name/$base"
  done
done

[ "$installed" -gt 0 ] || fail "nothing to install — is this a complete checkout?"

mode="copied"
[ "$symlink" = true ] && mode="symlinked"
echo
echo "Done: $installed items $mode into $dest_root"
if [ "$symlink" = true ]; then
  echo "Symlinked installs update automatically when you git pull this repo."
else
  echo "To update later, git pull this repo and re-run the same command."
fi
