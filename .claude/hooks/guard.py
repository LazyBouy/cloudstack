#!/usr/bin/env python3
"""PreToolUse guard for the CloudStack-course agents (strategist, researcher, author, auditor).

Registered twice, so that it runs even where one mechanism isn't honoured:
- in each agent's frontmatter (.claude/agents/<role>.md), with the role as argument:
      python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard.py" <role>
- in .claude/settings.json, for every tool call, without an argument. It then takes
  the role from the hook input's `agent_type`, and lets everything through for the
  main session and for other agents.
Both registrations skip the guard when this file is missing (a checkout without
.claude/), because python3 exits with code 2 on a missing script, and code 2 would
block every tool call, the main session's included.

It reads the hook's JSON from stdin and blocks a tool call by exiting with code 2
(the message on stderr goes back to the agent). Exit 0 lets the normal permission
flow decide. If the guard itself fails while checking one of our agents, it blocks
(fails closed). Every call is logged to $CLOUDSTACK_LEARN_GUARD_LOG
(default /tmp/cloudstack-learn-guard.log), so you can see that it runs.
This is a guardrail against mistakes, not a sandbox.

Rules
- Only inside the CloudStack learning project (a repo with 00.Learn/references/base_instruction_v0.md).
- Never read or touch credentials (.github/.env, ~/.claude/.credentials.json).
- Writes (Write/Edit/NotebookEdit, and shell redirections, cp, mv, tee):
    strategist           00.Learn/references/strategy/** only (the course map and the
                         modules' learning plans). The main session turns an approved
                         plan into the module skeleton (README, .nav.yml, stubs).
    researcher, auditor  00.Learn/references/articles/** only (the dossier; the audit
                         report). The auditor never edits posts: it hands findings to
                         the main session, which verifies them and applies the changes.
    author               00.Learn/**, except references/ other than references/articles/**
                         and references/in_progress_checks.md
  plus, for every role, the session scratchpad and the pinned-source cache.
- Shell: no git commands that change the repository, its refs or its index (tag and
  branch only to list), no package installs, no Maven (the agents read CloudStack's
  code, they never build it), no sudo, no piping downloads into a shell, no uploads
  with curl, no GitHub tools, docker only for the blog and Mermaid images, no
  in-place sed/perl, and rm only inside the scratchpad, the cache or /tmp. The
  strategist, the researcher and the auditor may not run the scripts that change
  posts (pinned.py fill, render-diagrams.sh).
"""
import datetime
import json
import os
import re
import shlex
import sys

ROLES = ("strategist", "researcher", "author", "auditor")
LOG = os.environ.get("CLOUDSTACK_LEARN_GUARD_LOG", "/tmp/cloudstack-learn-guard.log")
SECRETS = re.compile(r"\.github/\.env\b|\.credentials\.json")


class Deny(Exception):
    pass


def log(line):
    try:
        with open(LOG, "a") as f:
            f.write(f"{datetime.datetime.now().isoformat(timespec='seconds')} {line}\n")
    except OSError:
        pass


def check(role, data):
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    cwd = data.get("cwd") or os.getcwd()
    project = os.environ.get("CLAUDE_PROJECT_DIR") or cwd
    scratch = data.get("scratchpad_dir") or ""
    cache = os.path.join(os.environ.get("CLOUDSTACK_LEARN_CACHE",
                                        os.path.expanduser("~/.cache/cloudstack-learn")), "")
    learn = os.path.join(project, "00.Learn")
    refs = os.path.join(learn, "references")
    articles = os.path.join(refs, "articles")
    strategy = os.path.join(refs, "strategy")
    checks = os.path.join(refs, "in_progress_checks.md")
    safe_roots = [r for r in (scratch, cache, "/tmp/claude-") if r]

    def real(p):
        p = os.path.expanduser(p)
        return os.path.realpath(p if os.path.isabs(p) else os.path.join(cwd, p))

    def under(path, root):
        root = os.path.realpath(root)
        return path == root or path.startswith(root.rstrip("/") + "/")

    def writable(path):
        if any(under(path, r) for r in (scratch, cache) if r) or path.startswith("/tmp/claude-") \
                or path == "/dev/null":
            return True
        if role == "strategist":
            return under(path, strategy)
        if role in ("researcher", "auditor"):
            return under(path, articles)
        if role == "author":
            if under(path, refs):
                return under(path, articles) or path == os.path.realpath(checks)
            return under(path, learn)
        return False

    def where_allowed():
        if role == "strategist":
            return ("00.Learn/references/strategy/ (course.md, <Module>.md) and the scratchpad; "
                    "the main session creates the module skeleton once the user approves the plan")
        if role == "researcher":
            return "00.Learn/references/articles/<Module>/<NN.Slug>/ (and the scratchpad)"
        if role == "auditor":
            return ("00.Learn/references/articles/<Module>/<NN.Slug>/audit.md (and the scratchpad); "
                    "put proposed changes in audit.md as findings: the main session applies them")
        return ("00.Learn/ (posts, answers, diagrams, stubs, READMEs), "
                "00.Learn/references/articles/ and 00.Learn/references/in_progress_checks.md")

    # 0. Only this project.
    if not os.path.exists(os.path.join(project, "00.Learn", "references", "base_instruction_v0.md")):
        if tool in ("Write", "Edit", "NotebookEdit", "MultiEdit", "Bash"):
            raise Deny(f"the {role} agent only works in the CloudStack learning project (00.Learn/); "
                       "stop and tell the caller.")
        return

    # 1. Credentials.
    if SECRETS.search(json.dumps(ti)):
        raise Deny("credentials (.github/.env, .credentials.json) are off limits: "
                   "never read, print, copy or edit them.")

    # 2. File-writing tools.
    if tool in ("Write", "Edit", "NotebookEdit", "MultiEdit"):
        target = ti.get("file_path") or ti.get("notebook_path") or ""
        if not target or not writable(real(target)):
            raise Deny(f"{role} may not write {target!r}. Allowed: {where_allowed()}.")
        return

    # 3. Shell commands, read the way the shell reads them: quoted text and heredoc
    # bodies are data, not commands or redirections.
    if tool != "Bash":
        return
    previous = (None, None)
    for words, redirects, cwd_now, env, sep in simple_commands(ti.get("command", ""), cwd):
        prog = os.path.basename(words[0]) if words else None
        if previous[1] in ("|", "|&") and previous[0] in ("curl", "wget") \
                and prog in ("sh", "bash", "zsh", "dash", "ksh"):
            raise Deny("never pipe a download into a shell")
        check_command(role, words, redirects, cwd_now, env, writable, where_allowed, safe_roots)
        previous = (prog, sep)


GIT_WRITES = {"commit", "push", "pull", "fetch", "clone", "init", "reset", "rebase", "merge",
              "switch", "checkout", "restore", "stash", "clean", "cherry-pick", "revert",
              "am", "apply", "submodule", "add", "rm", "mv", "gc", "prune", "worktree",
              "filter-branch", "update-ref", "config", "notes", "replace", "bisect", "remote",
              "sparse-checkout", "read-tree", "checkout-index", "update-index", "symbolic-ref",
              "write-tree", "commit-tree", "pack-refs", "reflog", "lfs", "maintenance"}
LIST_MODE = {"-l", "--list", "--contains", "--no-contains", "--points-at", "--merged", "--no-merged",
             "-a", "--all", "-r", "--remotes"}
CHANGES_REFS = {"-d", "-D", "--delete", "-a", "-s", "-u", "-f", "--force", "-m", "-M", "--move", "-c", "-C",
                "--copy", "--annotate", "--sign", "--local-user", "--message", "--file", "-F", "-e", "--edit",
                "--set-upstream-to", "--unset-upstream", "--edit-description", "--track", "--no-track"}
BUILDERS = {"mvn", "mvnw", "ant", "gradle", "gradlew"}
DOCKER_IMAGES = {"cloudstack-blog", "minlag/mermaid-cli:12.0.0"}
INSTALLERS = {"pip", "pip3", "pipx", "uv", "npm", "yarn", "pnpm", "apt", "apt-get", "dnf", "yum",
              "apk", "brew", "snap", "gem", "cargo", "go"}
KEYWORDS = {"do", "then", "else", "elif", "if", "while", "until", "!", "{", "}", "done", "fi"}
WRAPPERS = {"time", "nohup", "nice", "env", "xargs", "command", "exec"}
SEPARATORS = {";", "&&", "||", "|", "&", "(", ")", "|&", ";;"}
REDIRECTS = {">", ">>", ">|", "&>", "&>>"}


def lists_only(sub, rest):
    """True if `git tag …` or `git branch …` only lists. With no arguments both list; a bare
    name creates a tag or branch unless a list-mode option (--list, --contains…) is given."""
    flags = {a.split("=", 1)[0] for a in rest if a.startswith("-")}
    changing = CHANGES_REFS - ({"-a"} if sub == "branch" else set())   # branch -a lists all
    if flags & changing or any(a.startswith("-") and not a.startswith("--") and len(a) > 2
                               and set(a[1:]) & {"d", "D", "m", "M", "c", "C", "f", "u"} for a in rest):
        return False
    names = [a for a in rest if not a.startswith("-")]
    return not names or bool(flags & LIST_MODE)


DOCKER_VALUE_FLAGS = {"-v", "--volume", "-e", "--env", "-p", "--publish", "-u", "--user", "-w", "--workdir",
                      "--name", "--entrypoint", "--mount", "--network", "--env-file", "-l", "--label",
                      "--platform", "--add-host", "--cpus", "-m", "--memory", "--tmpfs", "--init-path",
                      "-h", "--hostname", "--stop-signal", "--pull", "--cidfile", "--log-driver",
                      "--log-opt", "--device", "--cap-add", "--cap-drop", "--ulimit", "--security-opt"}


def docker_image(args):
    """The image named in `docker run|create [options] IMAGE [command…]`."""
    i = next((k for k, a in enumerate(args) if a in ("run", "create")), len(args)) + 1
    while i < len(args):
        a = args[i]
        if a in DOCKER_VALUE_FLAGS:
            i += 2
        elif a.startswith("-"):
            i += 1
        else:
            return a
    return ""


def unquoted_newlines_to_semicolons(cmd):
    """Replace newlines outside quotes with ';', so each line is a command of its own."""
    out, quote, i = [], None, 0
    while i < len(cmd):
        c = cmd[i]
        if c == "\\" and quote != "'" and i + 1 < len(cmd):
            out.append(cmd[i:i + 2]); i += 2; continue
        if quote:
            if c == quote:
                quote = None
        elif c in "'\"":
            quote = c
        elif c == "\n":
            c = " ; "
        out.append(c); i += 1
    return "".join(out)


def expand(word, env):
    """Expand $NAME and ${NAME}; None if a variable is unknown."""
    def sub(m):
        name = m.group(1) or m.group(2)
        if name not in env:
            raise KeyError(name)
        return env[name]
    try:
        return re.sub(r"\$\{(\w+)\}|\$(\w+)", sub, os.path.expanduser(word))
    except KeyError:
        return None


def simple_commands(cmd, cwd):
    """Yield (argv, redirect targets, cwd, env) for each simple command in a shell line."""
    # Heredoc bodies are data: keep the line that starts them, drop the body.
    cmd = re.sub(r"(<<-?\s*(['\"]?)(\w+)\2)([^\n]*)\n.*?\n[ \t]*\3[ \t]*(?=\n|$)", r"\1\4",
                 cmd, flags=re.S)
    cmd = unquoted_newlines_to_semicolons(cmd)
    lex = shlex.shlex(cmd, posix=True, punctuation_chars=";&|<>()")
    lex.whitespace_split = True
    try:
        tokens = list(lex)
    except ValueError:                      # unbalanced quotes: fall back to plain splitting
        tokens = cmd.split()
    env = dict(os.environ)
    words, redirects, pending = [], [], None
    here = cwd

    def flush(sep=None):
        nonlocal words, redirects, here
        argv = list(words)
        while argv and (argv[0] in KEYWORDS or re.fullmatch(r"[A-Za-z_]\w*=.*", argv[0])):
            m = re.fullmatch(r"([A-Za-z_]\w*)=(.*)", argv[0])
            if m:
                value = expand(m.group(2), env)
                if value is not None:
                    env[m.group(1)] = value
            argv.pop(0)
        if argv and argv[0] == "export":
            for a in argv[1:]:
                m = re.fullmatch(r"([A-Za-z_]\w*)=(.*)", a)
                if m and expand(m.group(2), env) is not None:
                    env[m.group(1)] = expand(m.group(2), env)
            argv = []
        result = (argv, redirects, here, dict(env), sep)
        if argv and argv[0] == "cd" and len(argv) > 1:
            target = expand(argv[1], env)
            if target is not None:
                here = os.path.realpath(target if os.path.isabs(target) else os.path.join(here, target))
        words, redirects = [], []
        return result

    for tok in tokens:
        if pending:
            redirects.append(tok)
            pending = None
        elif tok in REDIRECTS:
            pending = tok
        elif tok in SEPARATORS:
            yield flush(tok)
        elif tok in ("<", "<<", "<<<", ">&", "<&", "<<-", "2", "1") and not words:
            words.append(tok)
        else:
            words.append(tok)
    yield flush()


def check_command(role, argv, redirects, here, env, writable, where_allowed, safe_roots):
    def real_at(p):
        return os.path.realpath(p if os.path.isabs(p) else os.path.join(here, p))

    def target_ok(t):
        if t.startswith("&") or t in ("/dev/null", "/dev/stderr", "/dev/stdout"):
            return True
        e = expand(t, env)
        return e is not None and writable(real_at(e))

    for t in redirects:
        if not target_ok(t):
            raise Deny(f"writing to {t!r} is outside where {role} may write ({where_allowed()})")
    while argv and (argv[0] in WRAPPERS or argv[0] == "timeout"):
        name = argv.pop(0)
        while argv and (argv[0].startswith("-") or (name == "timeout" and re.fullmatch(r"[\d.]+[smhd]?", argv[0]))
                        or re.fullmatch(r"[A-Za-z_]\w*=.*", argv[0])):
            argv.pop(0)
    if not argv:
        return
    prog = os.path.basename(argv[0])
    args = argv[1:]

    if prog == "git":
        i = 0
        while i < len(args) and args[i].startswith("-"):
            i += 2 if args[i] in ("-C", "-c", "--git-dir", "--work-tree", "--namespace") else 1
        sub = args[i] if i < len(args) else ""
        rest = args[i + 1:]
        if sub in GIT_WRITES:
            raise Deny("git commands that change the repository are not allowed (read-only git is fine; "
                       "pinned sources come from .github/scripts/pinned.py, or git show/grep at the pin; "
                       "the main session commits when the user asks)")
        if sub in ("tag", "branch") and not lists_only(sub, rest):
            raise Deny(f"git {sub} may only list (for example git {sub} --contains <commit>); "
                       "creating, moving or deleting is not allowed")
        if sub == "archive" and any(a in ("-o", "--output") or a.startswith("--output=") for a in rest):
            raise Deny("git archive may not write files; .github/scripts/pinned.py path exports the pinned code")
    if (prog in INSTALLERS and any(a in ("install", "add", "get", "i", "ci") for a in args[:2])) \
            or (prog.startswith("python") and args[:2] == ["-m", "pip"]) or prog in ("npx", "uvx") \
            or (prog.startswith("python") and "setup.py" in args and "install" in args):
        raise Deny("never install software on the host; run tools in Docker "
                   "(CLAUDE.md, 'Tooling: containers only')")
    if prog in BUILDERS:
        raise Deny("never build CloudStack on the host (Maven would download hundreds of MB); read the code "
                   "at the pin instead (.github/scripts/pinned.py, git show, git grep)")
    if prog in ("sudo", "su", "doas"):
        raise Deny("no sudo")
    methods = {args[k + 1].upper() for k, a in enumerate(args[:-1]) if a in ("-X", "--request")} | \
              {a[2:].upper() for a in args if a.startswith("-X") and len(a) > 2}
    if prog == "curl" and (methods & {"POST", "PUT", "PATCH", "DELETE"} or any(
            a in ("-d", "-F", "-T", "--form", "--upload-file") or a.startswith("--data") for a in args)):
        raise Deny("curl may only read (no uploads or POST/PUT/PATCH/DELETE)")
    # Scripts are matched wherever they appear (bash x.sh, python3 x.py), not only as the program.
    names = {os.path.basename(a) for a in argv}
    if "publish-pages.sh" in names:
        raise Deny("publishing the site is the main session's job, on the user's request only")
    if prog in ("gh", "wrangler"):
        raise Deny("GitHub and Cloudflare tools are off limits for this agent (read PRs with WebFetch "
                   "on api.github.com instead)")
    if prog == "docker":
        sub = next((a for a in args if not a.startswith("-")), "")
        mounts = [args[k + 1] for k, a in enumerate(args[:-1]) if a in ("-v", "--volume")] + \
                 [a.split("=", 1)[1] for a in args if a.startswith("--volume=")]
        if sub in ("exec", "rm", "rmi", "system", "volume", "network", "push", "login", "kill", "stop",
                   "pull", "build", "buildx", "compose", "cp", "commit", "save", "load", "import", "tag") \
                or "--privileged" in args or "--pid=host" in args or "--network=host" in args \
                or any(m.startswith("/:") for m in mounts):
            raise Deny("that docker usage is not allowed; use the repo scripts (build-site.sh, "
                       "render-diagrams.sh, check-diagram-styles.py)")
        if sub in ("run", "create"):
            image = docker_image(args)
            if image not in DOCKER_IMAGES:
                raise Deny(f"docker may only run the course's images ({', '.join(sorted(DOCKER_IMAGES))}), "
                           f"not {image!r}; never run CloudStack, Maven or other tools in containers here")
    if (prog == "sed" and any(a == "--in-place" or a.startswith("--in-place=")
                              or (re.fullmatch(r"-[A-Za-z]+.*", a) and "i" in a[1:].split(".")[0]
                                  and not a.startswith("--")) for a in args)) \
            or (prog == "perl" and any(re.fullmatch(r"-[A-Za-z]*i.*", a) for a in args)):
        raise Deny("no in-place sed/perl edits; use the Edit tool so every change is visible")
    if role in ("strategist", "researcher", "auditor") and (
            ("pinned.py" in names and "fill" in args) or "render-diagrams.sh" in names):
        raise Deny(f"the {role} doesn't edit posts or diagrams; record what's needed in "
                   + {"strategist": "the strategy document", "researcher": "research.md",
                      "auditor": "audit.md as a finding"}[role])
    if prog == "rm":
        paths = [a for a in args if not a.startswith("-")]
        expanded = [expand(p, env) for p in paths]
        if not paths or any(e is None for e in expanded) or not all(
                e.startswith("/tmp/") or any(real_at(e).startswith(r) for r in safe_roots) for e in expanded):
            raise Deny("rm is only allowed inside the scratchpad, the pinned-source cache or /tmp")
    if prog in ("cp", "mv") and len([a for a in args if not a.startswith("-")]) >= 2:
        dest = [a for a in args if not a.startswith("-")][-1]
        if not target_ok(dest):
            raise Deny(f"{prog} to {dest!r} is outside where {role} may write ({where_allowed()})")
    if prog == "tee":
        for t in (a for a in args if not a.startswith("-")):
            if not target_ok(t):
                raise Deny(f"writing to {t!r} is outside where {role} may write ({where_allowed()})")


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except ValueError:
        data = {}
    agent = data.get("agent_type") or ""
    role = (sys.argv[1] if len(sys.argv) > 1 else "") or (agent if agent in ROLES else "")
    tool = data.get("tool_name", "?")
    ti = data.get("tool_input") or {}
    what = ti.get("file_path") or ti.get("command") or ti.get("pattern") or ti.get("url") or ""
    via = "frontmatter" if len(sys.argv) > 1 else "settings"
    if not role:
        log(f"pass  via={via} agent_type={agent or '-'} tool={tool} {str(what)[:120]!r}")
        return 0                  # the main session, or an agent that isn't ours
    try:
        check(role, data)
    except Deny as d:
        log(f"BLOCK via={via} role={role} tool={tool} {str(what)[:120]!r}: {d}")
        print(f"[{role} guard] Blocked: {d}", file=sys.stderr)
        return 2
    except Exception as e:        # fail closed: an error must never let a call through
        log(f"ERROR via={via} role={role} tool={tool} {str(what)[:120]!r}: {e!r}")
        print(f"[{role} guard] Blocked: the guard hit an internal error ({e!r}); "
              "tell the main session.", file=sys.stderr)
        return 2
    log(f"allow via={via} role={role} tool={tool} {str(what)[:120]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
