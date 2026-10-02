#!/usr/bin/env python3
"""Work with the CloudStack code the course is pinned to, without changing the repository.

The `learn` branch is `main` (a mirror of apache/cloudstack) plus the course files, and it
never changes CloudStack's own files. The *pin* is the last upstream commit merged into
`learn`: the newest of `git merge-base HEAD <ref>` for main, upstream/main and origin/main
(whichever exist).

  pinned.py sha                                  full SHA of the pin
  pinned.py path                                 a folder holding the code at the pin
  pinned.py excerpt [cloudstack:]PATH:N[-M]...   paste-ready excerpt blocks: header, verbatim lines (dedented), link
  pinned.py link [cloudstack:]PATH:N[-M]...      the GitHub permalink for those lines
  pinned.py fill FILE...                         replace @cloudstack@ in links with the commit each post is written against
  pinned.py written-against                      the commit a new post names in its header
  pinned.py prune                                remove cached code trees that no post and no pin needs any more

Options (before the subcommand's arguments):
  --at REF      use this commit, tag or branch instead of the pin; install posts use the
                release they install, e.g. --at 4.22.1.1
  --lang LANG   code-fence language for `excerpt` (default: guessed from the file name)

Never type a SHA by hand: write links as
  https://github.com/apache/cloudstack/blob/@cloudstack@/api/src/main/java/org/apache/cloudstack/api/APICommand.java#L28
and run `pinned.py fill` on the post. A post's links use the commit in its own
"**Written against:** commit `…`" header; an answers page uses its post's.

Reading code needs no copy at all: `git show <sha>:<path>` prints a file, and
`git grep -n <pattern> <sha> -- <path>` searches one. `path` is for tools that need real
files (Grep, Read): it prints the repository itself when its code is exactly the pin's
(learn only ever adds files), and otherwise a read-only export made with `git archive` in
${CLOUDSTACK_LEARN_CACHE:-~/.cache/cloudstack-learn}/src/cloudstack@<sha12> (about 200 MB).
Needs only git; tags and release branches need `git fetch upstream --tags` once.
"""
import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import textwrap

ROOT = pathlib.Path(subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True).strip())
CACHE = pathlib.Path(os.environ.get("CLOUDSTACK_LEARN_CACHE",
                                    pathlib.Path.home() / ".cache" / "cloudstack-learn")) / "src"
BASE_REFS = ("main", "upstream/main", "origin/main")
GITHUB = "https://github.com/apache/cloudstack"
WRITTEN_AGAINST = re.compile(r"\*\*Written against:\*\* commit `([0-9a-f]{7,40})`")
PLACEHOLDER = re.compile(r"(https://github\.com/apache/cloudstack/(?:blob|tree)/)@cloudstack@")
LANGS = {".java": "java", ".js": "javascript", ".ts": "typescript", ".vue": "html",
         ".html": "html", ".sql": "sql", ".xml": "xml", ".xsd": "xml", ".groovy": "groovy",
         ".properties": "properties", ".py": "python", ".sh": "bash", ".yaml": "yaml",
         ".yml": "yaml", ".ini": "ini", ".conf": "ini", ".cfg": "ini", ".json": "text",
         ".rst": "text", ".txt": "text", ".j2": "text", ".md": "text", ".in": "text"}
SLASHES = {".java", ".js", ".ts", ".groovy", ".c", ".h", ".go", ".cs", ".scala", ".kt"}
DASHES = {".sql"}
ANGLES = {".xml", ".xsd", ".vue", ".html"}


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True)


def commit(ref):
    """The full SHA of a commit, tag or branch."""
    try:
        return git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").strip()
    except subprocess.CalledProcessError:
        sys.exit(f"{ref!r} is not a commit here. For a tag or release branch, run "
                 "`git fetch upstream --tags` first.")


def pin(at=None):
    """The commit the course reads: --at if given, else the last upstream commit in HEAD."""
    if at:
        return commit(at)
    bases = []
    for ref in BASE_REFS:
        if subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--verify", "--quiet", ref],
                          capture_output=True).returncode == 0:
            bases.append(git("merge-base", "HEAD", ref).strip())
    if not bases:
        sys.exit(f"none of {', '.join(BASE_REFS)} exists; cannot tell which upstream commit is pinned")
    newest = bases[0]
    for b in bases[1:]:
        if subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", newest, b]).returncode == 0:
            newest = b
    return newest


def parse_spec(spec):
    s = spec[len("cloudstack:"):] if spec.startswith("cloudstack:") else spec
    try:
        path, rng = s.rsplit(":", 1)
        first, _, last = rng.partition("-")
        first, last = int(first), int(last or first)
    except ValueError:
        sys.exit(f"bad spec {spec!r}; expected [cloudstack:]PATH:N or [cloudstack:]PATH:N-M")
    if last < first:
        sys.exit(f"bad spec {spec!r}: the range runs backwards")
    return path, first, last


def link(sha, path, first, last=None):
    plain = "?plain=1" if path.endswith(".md") else ""
    anchor = f"#L{first}" if not last or last == first else f"#L{first}-L{last}"
    return f"{GITHUB}/blob/{sha}/{path}{plain}{anchor}"


def read(sha, path):
    try:
        data = subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", f"{sha}:{path}"],
                              check=True, capture_output=True).stdout
    except subprocess.CalledProcessError:
        sys.exit(f"{path} does not exist at {sha[:10]}")
    return data.decode("utf-8", errors="replace").split("\n")


def comment(path, text):
    ext = pathlib.Path(path).suffix
    if ext in SLASHES:
        return f"// {text}"
    if ext in DASHES:
        return f"-- {text}"
    if ext in ANGLES:
        return f"<!-- {text} -->"
    return f"# {text}"


def cmd_excerpt(specs, at, lang):
    sha = pin(at)
    for spec in specs:
        path, first, last = parse_spec(spec)
        src = read(sha, path)
        if last > len(src):
            sys.exit(f"{spec}: the file has only {len(src)} lines")
        body = textwrap.dedent("\n".join(src[first - 1:last]))
        where = f"line {first}" if first == last else f"lines {first}–{last}"
        fence = lang or LANGS.get(pathlib.Path(path).suffix, "text")
        print(f"```{fence}\n{comment(path, f'cloudstack: {path}, {where}')}\n{body}\n```")
        print(f"link: {link(sha, path, first, last)}\n")


def post_commit(md):
    """The commit a post (or, for an answers page, its post) is written against, or None."""
    m = WRITTEN_AGAINST.search(md.read_text())
    if m:
        return commit(m.group(1))
    answers = next((a for a in md.resolve().parents if a.name.endswith("Check-Yourself-Answers")), None)
    if answers is not None:
        # The answers page sits at the same path as its post, under <Module>/99.Check-Yourself-Answers/.
        post = answers.parent / md.resolve().relative_to(answers)
        if post.exists():
            m = WRITTEN_AGAINST.search(post.read_text())
            if m:
                return commit(m.group(1))
    return None


def cmd_fill(files, at):
    for f in files:
        p = pathlib.Path(f)
        text = p.read_text()
        sha = post_commit(p)
        note = ""
        if sha is None:
            sha = pin(at)
            note = " (no 'Written against' header found; used the pin)"
        new = PLACEHOLDER.sub(lambda m: m.group(1) + sha, text)
        left = sorted(set(re.findall(r"/(?:blob|tree)/@[^@/]+@", new)))
        p.write_text(new)
        print(f"{f}: filled {len(PLACEHOLDER.findall(text))} links with {sha[:10]}{note}"
              + (f"; not filled: {left}" if left else ""))


def same_code_as_worktree(sha):
    """True if every tracked file that differs from `sha` in the working tree is one learn added."""
    out = git("diff", "--name-status", "--no-renames", sha)
    return all(line.split("\t", 1)[0] == "A" for line in out.splitlines() if line.strip())


def cmd_path(at):
    sha = pin(at)
    if same_code_as_worktree(sha):
        print(ROOT)
        print("(the repository's code is exactly the pin's; no copy needed)", file=sys.stderr)
        return
    dest = CACHE / f"cloudstack@{sha[:12]}"
    if not dest.is_dir():
        CACHE.mkdir(parents=True, exist_ok=True)
        tmp = pathlib.Path(tempfile.mkdtemp(prefix=".export-", dir=CACHE))
        try:
            proc = subprocess.Popen(["git", "-C", str(ROOT), "archive", "--format=tar", sha],
                                    stdout=subprocess.PIPE)
            with tarfile.open(fileobj=proc.stdout, mode="r|") as tar:
                tar.extractall(tmp, filter="data")
            if proc.wait() != 0:
                sys.exit("git archive failed")
            tmp.rename(dest)
        finally:
            if tmp.exists():
                shutil.rmtree(tmp)
    print(dest)


def cmd_prune(at):
    keep = {pin(at)[:12]}
    for md in (ROOT / "00.Learn").rglob("*.md"):
        if "references" not in md.parts:
            keep.update(commit(c)[:12] for c in WRITTEN_AGAINST.findall(md.read_text()))
    if not CACHE.is_dir():
        print("nothing cached")
        return
    for d in sorted(CACHE.iterdir()):
        if d.name.startswith(".export-") or (d.name.startswith("cloudstack@")
                                              and d.name.split("@", 1)[1] not in keep):
            shutil.rmtree(d)
            print(f"removed {d}")
        else:
            print(f"kept    {d}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--at")
    ap.add_argument("--lang")
    ap.add_argument("command", choices=["sha", "path", "excerpt", "link", "fill", "written-against", "prune"])
    ap.add_argument("args", nargs="*")
    a = ap.parse_args()
    if a.command == "sha":
        print(pin(a.at))
    elif a.command == "path":
        cmd_path(a.at)
    elif a.command == "excerpt":
        cmd_excerpt(a.args, a.at, a.lang)
    elif a.command == "link":
        sha = pin(a.at)
        for s in a.args:
            path, first, last = parse_spec(s)
            print(link(sha, path, first, last))
    elif a.command == "fill":
        cmd_fill(a.args, a.at)
    elif a.command == "written-against":
        print(git("rev-parse", "--short=10", pin(a.at)).strip())
    else:
        cmd_prune(a.at)


if __name__ == "__main__":
    main()
