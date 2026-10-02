#!/usr/bin/env bash
# Check that every external link in the given posts answers with a 2xx status
# (following redirects). Only real Markdown links count: [text](url) and <url>.
# Addresses inside code and config examples (http://localhost:8080/client,
# 192.168.1.10) aren't links. Code permalinks into apache/cloudstack are skipped
# too: their SHA and the quoted lines are check-excerpts.py's job.
# Usage: .github/scripts/check-urls.sh FILE.md...
set -uo pipefail
[ $# -gt 0 ] || { echo "usage: $0 FILE.md..." >&2; exit 2; }
fail=0
while read -r url; do
    [ -n "$url" ] || continue
    code=$(curl -s -o /dev/null -L --max-time 30 -w '%{http_code}' "$url")
    if [[ "$code" =~ ^2 ]]; then
        echo "ok   $code $url"
    else
        echo "FAIL $code $url"
        fail=1
    fi
done < <(grep -ohE '\]\(https?://[^) ]+\)|<https?://[^> ]+>' "$@" \
           | sed -E 's/^\]\(//; s/\)$//; s/^<//; s/>$//' \
           | grep -vE '^https://github\.com/apache/cloudstack/(blob|tree)/[0-9a-f]{40}/' \
           | sort -u)
exit $fail
