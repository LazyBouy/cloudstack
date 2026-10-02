#!/usr/bin/env python3
"""Check that every styled edge in a Mermaid diagram keeps its style when rendered.

Mermaid drops an edge's `linkStyle` when that edge crosses another one (it draws
a little bridge instead), so a dotted line can come out solid. This renders each
diagram to SVG with the same pinned Mermaid CLI as render-diagrams.sh (in
Docker), then compares every edge that has a `stroke-dasharray` in a `linkStyle`
line with the last `stroke-dasharray` the SVG gives that edge. If one differs,
reorder the nodes until nothing crosses; defining the shared node first, with
edges drawn *from* it, often helps.

Usage: .github/scripts/check-diagram-styles.py FILE.mmd...
"""
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

IMAGE = "minlag/mermaid-cli:12.0.0"
LINKSTYLE = re.compile(r"^\s*linkStyle\s+([\d,\s]+?)\s+(.*)$", re.M)
DASH = re.compile(r"stroke-dasharray:\s*([^;,\"]+)")


def expected(src):
    want = {}
    for idxs, style in LINKSTYLE.findall(src):
        m = DASH.search(style)
        if m:
            for i in idxs.replace(" ", "").split(","):
                want[int(i)] = " ".join(m.group(1).split())
    return want


def rendered(mmd):
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(mmd, pathlib.Path(tmp) / "d.mmd")
        subprocess.run(["docker", "run", "--rm", "-u", f"{os.getuid()}:{os.getgid()}",
                        "-v", f"{tmp}:/data", IMAGE, "-i", "d.mmd", "-o", "d.svg"],
                       check=True, capture_output=True)
        svg = (pathlib.Path(tmp) / "d.svg").read_text()
    edges = []
    for tag in re.findall(r"<path[^>]*\bid=\"L_[^\"]*\"[^>]*>", svg):
        dashes = DASH.findall(tag)
        edges.append(" ".join(dashes[-1].split()) if dashes else None)
    return edges


def main(files):
    bad = 0
    for f in files:
        want = expected(pathlib.Path(f).read_text())
        if not want:
            print(f"{f}: no dashed linkStyle to check")
            continue
        got = rendered(f)
        for i, style in sorted(want.items()):
            actual = got[i] if i < len(got) else None
            if actual != style:
                bad += 1
                print(f"{f}: edge {i} should be dashed '{style}' but renders as {actual!r} "
                      "(probably crosses another edge)")
        if not any(got[i] != s for i, s in want.items() if i < len(got)):
            print(f"{f}: all {len(want)} styled edges keep their style")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
