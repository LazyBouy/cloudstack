#!/usr/bin/env python3
"""Measure how dense a post is: new concepts, code and jargon per 1,000 words.

    readability.py [--check] [--budget N] [--max-bold D] [--max-code D]
                   [--max-inline D] [FILE.md ...]

A post that piles up new terms, code and inline jargon makes the reader carry
too much at once. The course marks each defined term in bold at its definition,
and only there, so bold counts the concepts a post asks the reader to learn.

Measured on the prose (not front matter, fenced code, tables, headings, images,
link targets, HTML comments or the template's labels such as **Level:**):

  gated with --check (exit 1 if any is over):
    defined terms   distinct bold terms; at most --budget N, the article's budget
                    from its strategy entry (no limit without --budget)
    bold density    bold terms per 1,000 words           (default max 6)
    code density    lines of fenced code per 1,000 words  (default max 10)
    inline density  `inline code` spans per 1,000 words   (default max 6)

  reported only:
    average sentence length, sentences over 25 words, paragraphs over 3 sentences,
    and the densest paragraphs, so you know where to start cutting.

Densities are per 1,000 words, and a post shorter than 1,000 words counts as
1,000, so a short post is judged by its absolute counts.

Without files, it looks at every post under 00.Learn/ (not references/, not the
check-yourself answers, not READMEs or stubs). Answers pages carry the evidence
excerpts on purpose, so they're always skipped. The defaults were set so that
every post of the archived first attempt fails; the first posts the user approves
set the final values.
"""
import pathlib
import re
import subprocess
import sys

DEFAULTS = {"--max-bold": 6.0, "--max-code": 10.0, "--max-inline": 6.0}
LABELS = {"level:", "type:", "written against:", "reading time:", "next up:",
          "kubernetes lens:", "openstack lens:", "what you'll learn:", "what you'll learn",
          "in short:", "tl;dr", "tl;dr:"}
FENCE_OPEN = re.compile(r"^\s*(```|~~~)")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
BOLD = re.compile(r"\*\*(.+?)\*\*")
INLINE = re.compile(r"`[^`\n]+`")
SENTENCE_END = re.compile(r"(?<=[.!?])[\"”’)]*\s+(?=[A-Z0-9\"“(\[*_`])")


def units(text):
    """Split a post into (line number, paragraph text) units and count code lines."""
    text = re.sub(r"\A---\n.*?\n---\n", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    out, current, start, code, fence = [], [], 0, 0, None

    def flush():
        nonlocal current
        if current:
            out.append((start, " ".join(current)))
        current = []

    for n, line in enumerate(text.splitlines(), 1):
        if fence:
            if re.match(r"^\s*" + re.escape(fence) + r"\s*$", line):
                fence = None
            elif line.strip():
                code += 1
            continue
        m = FENCE_OPEN.match(line)
        if m:
            flush()
            fence = m.group(1)
            continue
        s = line.strip()
        s = re.sub(r"^(>\s*)+", "", s)                  # callouts
        if not s or s.startswith(("#", "|", "![", "[!", "???", "!!!")) or re.fullmatch(r"[-*_]{3,}", s) \
                or s.startswith("**Level:**") or s.startswith("*Click the picture"):
            flush()
            continue
        if LIST_ITEM.match(s):
            flush()
            s = LIST_ITEM.sub("", s)
        if not current:
            start = n
        current.append(s)
    flush()
    return out, code


def clean(unit):
    unit = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", unit)
    unit = re.sub(r"\]\([^)]*\)", "]", unit)
    return unit


def words_in(s):
    return [w for w in s.split() if re.search(r"\w", w)]


def measure(text):
    paras, code = units(text)
    total = 0
    bold_terms, inline, sentences, long_sentences, long_paras, scored = [], 0, 0, 0, 0, []
    sentence_words = 0
    for line, raw in paras:
        unit = clean(raw)
        bolds = [b.strip() for b in BOLD.findall(unit) if b.strip().lower() not in LABELS]
        spans = INLINE.findall(unit)
        flat = INLINE.sub("X", unit)
        flat = re.sub(r"[*_\[\]]", "", flat)
        n_words = len(words_in(unit.replace("`", " ")))
        total += n_words
        bold_terms += bolds
        inline += len(spans)
        sents = [s for s in SENTENCE_END.split(flat) if words_in(s)]
        sentences += len(sents)
        for s in sents:
            k = len(words_in(s))
            sentence_words += k
            long_sentences += k > 25
        long_paras += len(sents) > 3
        scored.append((len(bolds) + len(spans), len(sents), line, raw, len(bolds), len(spans)))
    distinct = []
    for b in bold_terms:
        if b.lower().rstrip(":.") not in [d.lower().rstrip(":.") for d in distinct]:
            distinct.append(b)
    per_k = lambda x: 1000 * x / max(total, 1000)     # a short post is counted as 1,000 words
    return {
        "words": total, "code": code, "bold": len(bold_terms), "terms": distinct,
        "inline": inline, "bold_d": per_k(len(bold_terms)), "code_d": per_k(code),
        "inline_d": per_k(inline), "avg_sentence": sentence_words / sentences if sentences else 0,
        "long_sentences": long_sentences, "long_paras": long_paras,
        "densest": sorted((s for s in scored if s[0] > 1), key=lambda s: (-s[0], -s[1]))[:3],
    }


def main(argv):
    opts = dict(DEFAULTS)
    budget, files, check = None, [], False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--check":
            check = True
        elif a == "--budget":
            budget = int(argv[i + 1]); i += 1
        elif a in opts:
            opts[a] = float(argv[i + 1]); i += 1
        elif a in ("-h", "--help"):
            print(__doc__); return 0
        else:
            files.append(pathlib.Path(a))
        i += 1
    if not files:
        root = pathlib.Path(subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True).strip())
        files = sorted(p for p in (root / "00.Learn").rglob("*.md")
                       if "references" not in p.parts and p.name != "README.md")
    failed = 0
    for f in files:
        text = f.read_text()
        if "Check-Yourself-Answers" in str(f) or "STUB:" in text:
            print(f"skip {f}  ({'answers page' if 'Check-Yourself-Answers' in str(f) else 'stub'})")
            continue
        m = measure(text)
        over = []
        if budget is not None and len(m["terms"]) > budget:
            over.append(f"{len(m['terms'])} defined terms > budget {budget}")
        for key, flag, name in (("bold_d", "--max-bold", "bold"), ("code_d", "--max-code", "code"),
                                ("inline_d", "--max-inline", "inline code")):
            if m[key] > opts[flag]:
                over.append(f"{name} {m[key]:.1f}/1k > {opts[flag]:g}")
        failed += bool(over)
        print(f"{'FAIL' if over else 'ok  '} {f}")
        print(f"     {m['words']} words · {len(m['terms'])} defined terms"
              f"{'' if budget is None else f' (budget {budget})'} · bold {m['bold_d']:.1f}/1k"
              f" · code {m['code']} lines, {m['code_d']:.1f}/1k · inline code {m['inline']}, {m['inline_d']:.1f}/1k")
        print(f"     sentences: average {m['avg_sentence']:.1f} words, {m['long_sentences']} over 25"
              f" · paragraphs over 3 sentences: {m['long_paras']}")
        if over:
            print("     over: " + "; ".join(over))
        if m["terms"]:
            print("     terms: " + ", ".join(m["terms"]))
        for score, n_sent, line, raw, nb, ni in (m["densest"] if over else []):
            print(f"     dense L{line}: {nb} bold, {ni} inline code, {n_sent} sentences: {raw[:70]!r}")
    if check and failed:
        print(f"{failed} post(s) too dense: cut details, defer concepts to their own article, "
              "or move evidence to the answers page.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
