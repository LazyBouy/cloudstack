#!/usr/bin/env bash
# Fail if any diagram source (00.Learn/**/diagrams/*.mmd) has no PNG, or has
# changed since its PNG was rendered by render-diagrams.sh. Run it before
# committing, and before publishing.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

status=0
while read -r src; do
  dir=$(dirname "$src")
  file=$(basename "$src")
  if [ ! -f "$dir/${file%.mmd}.png" ]; then
    echo "ERROR $src: No PNG for this diagram. Run: .github/scripts/render-diagrams.sh $src"
    status=1
  elif ! (cd "$dir" && grep "  $file\$" manifest.sha256 2>/dev/null | sha256sum --quiet --strict -c - 2>/dev/null); then
    echo "ERROR $src: This diagram changed since its PNG was rendered. Run: .github/scripts/render-diagrams.sh $src"
    status=1
  fi
done < <(find 00.Learn -path '*/diagrams/*.mmd' -not -path '*/references/*' | sort)

[ "$status" -eq 0 ] && echo "All diagrams are up to date."
exit "$status"
