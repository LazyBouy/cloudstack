#!/usr/bin/env python3
"""Estimate each post's reading time, the same way for every post.

    reading-time.py [--check] [--max MINUTES] [FILE.md ...]

The rule: prose at 200 words a minute (a beginner reading technical text), plus
2 seconds for every non-blank line of code (skimmed: the sentence after each
block says what it shows), rounded to the nearest 5 minutes. Front matter, link
targets and image alt text don't count as prose; tables do.

Without files, it looks at every post under 00.Learn/ (not references/, not the
check-yourself answers). For each post it prints the counts, the estimate and
what the header says. With --check, it exits 1 if any header differs from the
estimate. With --max, it also exits 1 if any post's estimate (before rounding) is
longer than MINUTES: the course's rule is 30 minutes at most per post.
"""
import pathlib
import re
import subprocess
import sys

WORDS_PER_MINUTE = 200
SECONDS_PER_CODE_LINE = 2
FENCE = re.compile(r"^\s*(```|~~~)[^\n]*\n(.*?)^\s*\1\s*$", re.S | re.M)
HEADER = re.compile(r"\*\*Reading time:\*\* about (\d+) minutes")


def estimate(text):
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    code_lines = sum(len([l for l in m.group(2).splitlines() if l.strip()])
                     for m in FENCE.finditer(text))
    prose = FENCE.sub("", text)
    prose = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", prose)
    prose = re.sub(r"\]\([^)]*\)", "]", prose)
    words = len(prose.split())
    minutes = words / WORDS_PER_MINUTE + code_lines * SECONDS_PER_CODE_LINE / 60
    return words, code_lines, max(5, 5 * round(minutes / 5)), minutes


def main(argv):
    check = "--check" in argv
    limit = None
    if "--max" in argv:
        i = argv.index("--max")
        limit = float(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    files = [pathlib.Path(a) for a in argv if a != "--check"]
    if not files:
        root = pathlib.Path(subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True).strip())
        files = sorted(p for p in (root / "00.Learn").rglob("*.md")
                       if "references" not in p.parts
                       and "Check-Yourself-Answers" not in str(p))
    wrong = too_long = 0
    for f in files:
        text = f.read_text()
        header = HEADER.search(text)
        if not header:
            continue                    # stubs, READMEs and pages without a header
        words, code, rounded, exact = estimate(text)
        said = int(header.group(1))
        mark = "ok " if said == rounded else "FIX"
        wrong += said != rounded
        print(f"{mark} {f.name:34} prose {words:5} words, code {code:4} lines"
              f" -> {exact:4.1f} min, about {rounded:2}; header says {said}"
              + (f"  TOO LONG (max {limit:g})" if limit is not None and exact > limit else ""))
        too_long += limit is not None and exact > limit
    if check and wrong:
        print(f"{wrong} header(s) differ from the estimate.")
    if too_long:
        print(f"{too_long} post(s) longer than {limit:g} minutes: split or cut them.")
    return 1 if (check and wrong) or too_long else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
