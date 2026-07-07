#!/usr/bin/env bash
set -euo pipefail

TARGET_PROJECT="${1:-}"
if [[ -z "$TARGET_PROJECT" ]]; then
  echo "usage: bash ai_quant_trader/install.sh /path/to/ai_quant_trader" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_TARGET="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$SKILL_TARGET"
mkdir -p "$TARGET_PROJECT"

cp "$SCRIPT_DIR/AGENTS.md" "$TARGET_PROJECT/AGENTS.md"

find "$SCRIPT_DIR/skills" -mindepth 2 -maxdepth 3 -name SKILL.md -print0 | while IFS= read -r -d "" skill_file; do
  skill_dir="$(dirname "$skill_file")"
  skill_name="$(basename "$skill_dir")"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete "$skill_dir/" "$SKILL_TARGET/$skill_name/"
  else
    rm -rf "$SKILL_TARGET/$skill_name"
    mkdir -p "$SKILL_TARGET/$skill_name"
    cp -R "$skill_dir/." "$SKILL_TARGET/$skill_name/"
  fi
  echo "installed $skill_name"
done

echo "installed AGENTS.md -> $TARGET_PROJECT/AGENTS.md"
echo "installed skills -> $SKILL_TARGET"
