#!/usr/bin/env bash
# Render diagram sources (00.Learn/**/diagrams/*.mmd) to PNGs beside them, using
# the Mermaid CLI in Docker (nothing is installed on the host). Each rendered
# source's checksum goes into its folder's manifest.sha256, which is how
# check-diagrams.sh knows a PNG is up to date.
#
#   .github/scripts/render-diagrams.sh                    # every diagram
#   .github/scripts/render-diagrams.sh path/to/x.mmd ...  # just these
#
# Pictures render at three times their natural size, so they stay sharp when
# enlarged. A tall picture (a vertical step sequence) would then fill the page
# on the site and on GitHub, so its source may ask for a smaller scale with a
# line of its own:   %% render-scale: 1.5
# (the PNG then shows at a modest size everywhere, with no MkDocs-only width).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

MERMAID_IMAGE=minlag/mermaid-cli:12.0.0

if [ $# -gt 0 ]; then
  sources=("$@")
else
  mapfile -t sources < <(find 00.Learn -path '*/diagrams/*.mmd' -not -path '*/references/*' | sort)
fi

for src in "${sources[@]}"; do
  dir=$(dirname "$src")
  file=$(basename "$src")
  scale=$(sed -n 's/^%% render-scale: *\([0-9.]*\) *$/\1/p' "$src" | head -n 1)
  scale=${scale:-3}
  echo "rendering $src (scale $scale)"
  docker run --rm -u "$(id -u):$(id -g)" -v "$PWD/$dir":/data "$MERMAID_IMAGE" \
    -q -i "$file" -o "${file%.mmd}.png" -s "$scale" -b white

  # Record this source's checksum, replacing any older entry for it.
  manifest="$dir/manifest.sha256"
  touch "$manifest"
  { grep -v "  $file\$" "$manifest" || true; (cd "$dir" && sha256sum "$file"); } \
    | sort -k2 > "$manifest.tmp"
  mv "$manifest.tmp" "$manifest"
done
