#!/usr/bin/env bash
# Publish the course site to GitHub Pages. Run it only when the user asks: it
# makes every page of 00.Learn/ (references/ excluded) public.
#
# It builds the site strictly (build-site.sh) for the Pages address, then commits
# the built files, and nothing else, to the fork's gh-pages branch and pushes it.
# The branch holds only the latest build, as one commit, so each publish replaces
# the last one (a force push). GitHub serves it once the repository's settings say
# Pages: "Deploy from a branch", gh-pages, / (root).
#
#   .github/scripts/publish-pages.sh             # build and publish
#   .github/scripts/publish-pages.sh --dry-run   # build only; nothing is pushed
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
SITE_URL="${SITE_URL:-https://lazybouy.github.io/cloudstack/}"
REMOTE="${REMOTE:-origin}"
dry=false
[ "${1:-}" = --dry-run ] && dry=true

[ "$(git branch --show-current)" = learn ] || { echo "Publish from the learn branch." >&2; exit 1; }
if [ -n "$(git status --porcelain -- 00.Learn mkdocs.yml)" ]; then
  echo "00.Learn/ or mkdocs.yml has uncommitted changes: commit them first, so the site matches a commit." >&2
  exit 1
fi
src="$(git rev-parse --short HEAD)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

SITE_URL="$SITE_URL" .github/scripts/build-site.sh "$work/site"
touch "$work/site/.nojekyll"     # serve the files as they are, without Jekyll

git -C "$work/site" init -q -b gh-pages
git -C "$work/site" add -A
git -C "$work/site" -c user.name="$(git config user.name)" -c user.email="$(git config user.email)" \
  commit -q -m "Publish the course site, built from learn at $src"
echo "Built from learn at $src: $(git -C "$work/site" ls-files | wc -l) files."
if $dry; then
  echo "Dry run: nothing pushed."
  exit 0
fi
git -C "$work/site" push -q -f "$(git remote get-url "$REMOTE")" gh-pages:gh-pages
echo "Published to $REMOTE's gh-pages branch. The site: $SITE_URL"
