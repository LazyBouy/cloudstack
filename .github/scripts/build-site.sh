#!/usr/bin/env bash
# Build the blog the way it is published (mkdocs build --strict, in the pinned
# Docker image), then run the guard against links into references/.
# Usage: .github/scripts/build-site.sh [OUTDIR]   (default: a new temp dir)
# Never add --quiet: it silently turns --strict off.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
out="${1:-$(mktemp -d)}"
mkdir -p "$out"
out="$(cd "$out" && pwd)"

docker build -q -t cloudstack-blog -f .github/docker/blog.Dockerfile .github >/dev/null
docker run --rm -v "$PWD":/docs -v "$out":/site cloudstack-blog build --strict -d /site

if grep -rnE --include='*.md' --exclude-dir=references '\]\([^)]*references/' 00.Learn; then
    echo "Fix the links above: posts must never link into references/." >&2
    exit 1
fi
echo "Built in $out (strict). No links into references/."
