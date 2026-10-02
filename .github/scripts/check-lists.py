#!/usr/bin/env python3
"""Check that every list in the posts will render as a list on the blog.

GitHub's Markdown is forgiving, but MkDocs' (Python-Markdown) is not, so a list
that looks fine on GitHub can come out on the blog as one run-on paragraph with
the "- " markers in the text. This fails on the four patterns that cause it:

  1. a list that starts on the line right after a paragraph (leave a blank line;
     inside a callout, a line holding just ">"),
  2. a code block or a nested list inside a "- " item indented by 2 or 3 spaces
     (indent it by 4),
  3. a list item right after a code block inside the previous item,
  4. a list item right after an indented paragraph inside the previous item
     (leave a blank line before the item in both cases),
  5. text right after a closing code fence: MkDocs then renders it as bare text
     outside any paragraph (leave a blank line after every closing fence).

Usage: .github/scripts/check-lists.py [FILE.md ...]   (default: every post)
       .github/scripts/check-lists.py --site DIR       (a site built by build-site.sh)

With --site it checks the rendered pages instead: any list marker left inside a
paragraph, list item or table cell means a list didn't render, and a literal
``` means a code block didn't either.
Standard library only; no network needed.
"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True).strip())
ITEM = re.compile(r"^(?:>\s?)*(?P<ind>[ ]*)(?:[-*+]|\d+\.)\s+\S")
FENCE = re.compile(r"^(?:>\s?)*(?P<ind>\s*)(```|~~~)")
QUOTE = re.compile(r"^(?:>\s?)*")


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


def body(line):
    """The line without any callout ("> ") prefix."""
    return line[QUOTE.match(line).end():]


def indent(text):
    return len(text) - len(text.lstrip(" "))


def problems(lines):
    in_fence = in_list = fence_in_list = False
    delims = fence_delimiters(lines)
    for i, line in enumerate(lines):
        prev = lines[i - 1] if i else ""
        prev_blank = not body(prev).strip()
        fence = FENCE.match(line) if i in delims else None
        if fence:
            ind = len(fence.group("ind"))
            if not in_fence:
                fence_in_list = in_list and ind > 0
                if fence_in_list and ind % 4:
                    yield i, f"code block inside a list item is indented {ind} spaces; use 4"
            else:
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                if body(nxt).strip() and not ITEM.match(nxt) and (i + 1) not in delims:
                    yield i + 1, "text right after a closing code fence; leave a blank line"
            in_fence = not in_fence
            continue
        if in_fence or not body(line).strip():
            continue
        item = ITEM.match(line)
        if item:
            ind = len(item.group("ind"))
            if ind % 4:
                yield i, f"nested list item is indented {ind} spaces; use a multiple of 4"
            if not prev_blank and not ITEM.match(prev):
                if (i - 1) in delims and fence_in_list:
                    yield i, "list item right after a code block; leave a blank line"
                elif in_list and body(prev).startswith("  ") and ind == 0:
                    yield i, "list item right after an indented paragraph; leave a blank line"
                elif not in_list and not body(prev).startswith("|"):
                    yield i, "list starts right after a paragraph; leave a blank line"
            in_list = True
        elif in_list and prev_blank and indent(body(line)) == 0:
            in_list = False     # a new block at column 0 after a blank line ends the list


def check_site(site):
    """Scan built pages for list markers inside rendered text, and for unrendered fences."""
    marker = re.compile(r"\n\s*(?:[-*+]|\d+\.)\s+\S")
    count = 0
    for page in sorted(pathlib.Path(site).rglob("index.html")):
        text = page.read_text()
        m = re.search(r"<article[^>]*>(.*)</article>", text, re.S)
        body_html = re.sub(r"<pre.*?</pre>", "", m.group(1) if m else text, flags=re.S)
        for tag in ("p", "li", "td"):
            for chunk in re.findall(rf"<{tag}\b[^>]*>(.*?)</{tag}>", body_html, re.S):
                plain = html.unescape(re.sub(r"<[^>]+>", "", chunk))
                if marker.search(plain):
                    count += 1
                    print(f"{page}: list marker inside <{tag}>: "
                          + plain.strip().replace("\n", " / ")[:120])
        if "```" in body_html:
            count += 1
            print(f"{page}: a code block didn't render (literal ``` in the page)")
        empty = body_html.count("<p></p>")
        if empty:
            count += 1
            print(f"{page}: {empty} empty <p></p>: text probably glued to a code fence, "
                  "rendered outside any paragraph")
    print(f"{count} rendering problems found.")
    return 1 if count else 0


def main(paths):
    count = 0
    for md in paths:
        for i, message in problems(md.read_text().split("\n")):
            count += 1
            print(f"{md}:{i + 1}: {message}")
    print(f"{len(paths)} files checked, {count} list problems found.")
    return 1 if count else 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--site"] and len(sys.argv) == 3:
        sys.exit(check_site(sys.argv[2]))
    args = [pathlib.Path(a) for a in sys.argv[1:]] or sorted(
        p for p in (ROOT / "00.Learn").rglob("*.md") if "references" not in p.parts)
    sys.exit(main(args))
