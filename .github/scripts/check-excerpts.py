#!/usr/bin/env python3
"""Check that every code excerpt in the posts matches the code it quotes.

Posts quote CloudStack code in fenced blocks, one contiguous excerpt per block.
Each excerpt starts with a header comment naming the file and line(s), in the
comment style of the file's language, followed by the lines themselves:

    // cloudstack: api/src/main/java/org/apache/cloudstack/api/APICommand.java, lines 28-31
    -- cloudstack: engine/schema/src/main/resources/META-INF/db/schema-42300to2400.sql, line 19
    <!-- cloudstack: core/src/main/resources/META-INF/cloudstack/core/module.properties, line 17 -->
    # cloudstack: systemvm/debian/opt/cloud/bin/cs_dhcp.py, lines 20-25

Lines that aren't adjacent (another range of the same file, or another file)
go in a separate block; a block with more than one header fails the check.

Inside tables, a line may be quoted inline right before its link instead:

    `public @interface APICommand {` ([APICommand.java, line 30](https://github.com/apache/cloudstack/blob/<sha>/...#L30))

Which commit is checked: the commit in the post's own header ("Written against:
commit `abc1234567`"); for a page without one (an answers page), the commit its
links use, or else the current pin. Each excerpt line must equal the source
line, ignoring leading/trailing whitespace; for "lines N-M" the excerpt must
cover the whole range.

It also checks the links into apache/cloudstack themselves: each must name a
full 40-character commit, the file must exist there, and in a post with a
"Written against" header every link must use exactly that commit, so a
mistyped SHA is caught even where no excerpt quotes that file.

Everything is read from this repository with git, so it needs no network.
If a commit is missing, run `git fetch upstream --tags`.

Usage: .github/scripts/check-excerpts.py [FILE.md ...]   (default: every post)
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True).strip())
HEADER = re.compile(
    r"^\s*(?:#|//|--|<!--)\s*cloudstack:\s*(\S+), lines? (\d+)(?:\s*[-–]\s*(\d+))?\s*(?:-->)?\s*$")
LINK = re.compile(
    r"https://github\.com/apache/cloudstack/(blob|tree)/([^/\s)#?]+)/([^)#?\s]*)(?:\?plain=1)?(?:#L(\d+)(?:-L(\d+))?)?")
WRITTEN_AGAINST = re.compile(r"\*\*Written against:\*\* commit `([0-9a-f]{7,40})`")
INLINE = re.compile(
    r"`([^`]+)` \(\[[^\]]*\]\(https://github\.com/apache/cloudstack/blob/"
    r"([0-9a-f]{40})/([^)#?\s]+)(?:\?plain=1)?#L(\d+)\)\)")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")

_files, _commits = {}, {}


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True)


def resolve(ref):
    """The full SHA of a commit, or None if this repository doesn't have it."""
    if ref not in _commits:
        r = git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
        _commits[ref] = r.stdout.decode().strip() if r.returncode == 0 else None
    return _commits[ref]


def current_pin():
    out = subprocess.run([str(ROOT / ".github/scripts/pinned.py"), "sha"],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def source(sha, path):
    """The file's lines at that commit, or None if it isn't there."""
    key = (sha, path)
    if key not in _files:
        r = git("cat-file", "blob", f"{sha}:{path}")
        _files[key] = r.stdout.decode("utf-8", errors="replace").split("\n") if r.returncode == 0 else None
    return _files[key]


def fence_delimiters(lines):
    """Indexes of the lines that open or close a fenced block, paired the way Markdown
    pairs them: a fence closes only with the same character (` or ~), at least as long,
    and nothing else on the line. So an RST underline like ~~~~ inside a ``` block
    isn't mistaken for a fence."""
    marks, opener = set(), None
    for i, line in enumerate(lines):
        stripped = re.sub(r"^(?:>\s?)*\s*", "", line)
        m = re.match(r"(`{3,}|~{3,})(.*)$", stripped)
        if not m:
            continue
        run, rest = m.group(1), m.group(2)
        if opener is None:
            opener = run
            marks.add(i)
        elif run[0] == opener[0] and len(run) >= len(opener) and not rest.strip():
            opener = None
            marks.add(i)
    return marks


def fenced_excerpts(lines):
    """Yield (md line number, path, first, last, [excerpt lines])."""
    in_fence, current = False, None
    delims = fence_delimiters(lines)
    for i, line in enumerate(lines, 1):
        if i - 1 in delims:
            if in_fence and current:
                yield current
            in_fence, current = not in_fence, None
            continue
        if not in_fence:
            continue
        m = HEADER.match(line)
        if m:
            if current:
                yield current
            first = int(m.group(2))
            current = (i, m.group(1), first, int(m.group(3) or first), [])
        elif current is not None:
            current[4].append(line)


def crowded_blocks(lines):
    """Yield the md line number of every fenced block holding more than one excerpt."""
    in_fence, start, heads = False, 0, 0
    delims = fence_delimiters(lines)
    for i, line in enumerate(lines, 1):
        if i - 1 in delims:
            if in_fence and heads > 1:
                yield start
            in_fence, start, heads = not in_fence, i, 0
        elif in_fence and HEADER.match(line):
            heads += 1


def compare(label, src, first, last, body):
    if src is None:
        print(f"{label}: file not found at that commit (wrong SHA or path?)")
        return False
    want = [s.strip() for s in src[first - 1:last]]
    while want and not want[-1]:
        want.pop()                  # a range may end on blank lines; the post drops them
    got = [s.strip() for s in body]
    if got == want:
        return True
    print(f"{label} does not match")
    if len(got) != len(want):
        print(f"    the range has {len(want)} lines, the excerpt has {len(got)}")
    for n, (w, g) in enumerate(zip(want, got), first):
        if w != g:
            print(f"    first difference, line {n}:\n      code: {w!r}\n      post: {g!r}")
            break
    return False


def main(paths):
    failures = checked = 0
    pin = None
    for md in paths:
        text = md.read_text()
        lines = text.split("\n")

        # Which commit this page is checked against.
        m = WRITTEN_AGAINST.search(text)
        header = None
        if m:
            header = resolve(m.group(1))
            if header is None:
                failures += 1
                print(f"{md}: 'Written against' commit {m.group(1)} isn't in this repository "
                      "(run `git fetch upstream --tags`, or fix the header)")

        # Every link into apache/cloudstack: a full SHA, the right one, an existing file.
        first_link = None
        for lineno, line in enumerate(lines, 1):
            for kind, ref, path, start, _ in LINK.findall(line):
                where = f"{md}:{lineno}: link to {path or '/'}"
                if not FULL_SHA.match(ref):
                    failures += 1
                    print(f"{where} uses {ref!r}; use a full 40-character commit "
                          "(write @cloudstack@ and run pinned.py fill)")
                    continue
                if resolve(ref) is None:
                    failures += 1
                    print(f"{where} uses {ref}, which isn't in this repository "
                          "(run `git fetch upstream --tags`, or fix the SHA)")
                    continue
                first_link = first_link or ref
                if header and ref != header:
                    failures += 1
                    print(f"{where} uses {ref},\n    but the post is written against {header}")
                if kind == "blob" and path:
                    src = source(ref, path)
                    if src is None:
                        failures += 1
                        print(f"{where}: no such file at {ref[:10]}")
                    elif start and int(start) > len(src):
                        failures += 1
                        print(f"{where}: line {start} is past the end of the file ({len(src)} lines)")

        sha = header or first_link
        if sha is None:
            pin = pin or current_pin()
            sha = pin

        for lineno in crowded_blocks(lines):
            failures += 1
            print(f"{md}:{lineno}: this code block holds several excerpts; "
                  "put each contiguous excerpt in its own block")

        for lineno, path, first, last, body in fenced_excerpts(lines):
            while body and not body[-1].strip():
                body.pop()          # trailing blank lines are just spacing
            checked += 1
            ok = compare(f"{md}:{lineno}: excerpt of {path}, lines {first}-{last} @ {sha[:10]}",
                         source(sha, path), first, last, body)
            failures += not ok

        for lineno, line in enumerate(lines, 1):
            if not line.lstrip().startswith("|"):
                continue            # inline quotes are checked in tables only
            for code, ref, path, n in INLINE.findall(line):
                n = int(n)
                checked += 1
                ok = compare(f"{md}:{lineno}: inline quote of {path}, line {n} @ {ref[:10]}",
                             source(ref, path), n, n, [code])
                failures += not ok
    print(f"{checked} excerpts checked, {failures} problems found.")
    return 1 if failures else 0


if __name__ == "__main__":
    args = [pathlib.Path(a) for a in sys.argv[1:]] or sorted(
        p for p in (ROOT / "00.Learn").rglob("*.md") if "references" not in p.parts)
    sys.exit(main(args))
