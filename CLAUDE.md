# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project goal

This fork (`LazyBouy/cloudstack`) is a teaching project, purely pedagogical. It helps a beginner understand Apache CloudStack from the ground up, step by step, until they're advanced, with the code as the source of truth. Most material online walks through installing a cloud without explaining *why*. This course answers the why: what each part is for, why it's designed this way, and how the parts fit together. CloudStack's code is only ever read here, never edited or executed.

The course is built **for CloudStack itself**. The user's OpenStack course (`/root/projects/openstack/openstack`) was an example of *process and tooling* (the pipeline, the checks, the blog), never a template for content, structure, metaphor or sequence. A first attempt that copied it was archived (`00.Learn/references/archive/v1/`).

The founding instruction is [base_instruction_v0.md](00.Learn/references/base_instruction_v0.md). The current direction, which supersedes parts of it, is [base_instruction_v1.md](00.Learn/references/base_instruction_v1.md). When in doubt about intent, read both.

## How the course is planned: strategy first

Nothing is written before it's planned. For each module, the **strategist** writes a learning plan (`00.Learn/references/strategy/<Module>.md`), and the user approves it. The plan holds:

- the learner's outcomes;
- a concept ledger: every concept, what it depends on, and which article teaches it;
- the articles in order, each keyed by `NN.Slug` with an explicit scope (the concepts in, the concepts deferred, a target length).

The course map, the voice, the template and the **running analogy** live in `00.Learn/references/strategy/course.md` (approved 2026-10-01). The user chose **the cloud kitchen** from the strategist's candidates; the hotel analogy of the first attempt is retired. Module 01 ends with the hands-on lab, and every module ends with an exercises article.

Each article's strategy entry is the **binding brief** for the researcher, the author and the auditor.

- **Only the strategy splits topics.** A draft that runs long is cut, or the author files an amendment request; it's never split on the fly.
- **A strategy problem is raised, never worked around.** Any agent that finds one records an amendment request in its working file, and the strategy is revised with `/initiate-strategy <Module> amend`.

Modules are numbered `01.General`, `02.Management-Server`, and so on, as the course map decides. Articles are numbered within their module (`01.General/03.Some-Topic.md`), and the module's answers live in `99.Check-Yourself-Answers/`.

## Writing rules

The reader is **the learner**: someone who knows basic Linux (shell, files, packages, services, SSH) and nothing else, learning CloudStack step by step. "You" is always that learner. Operators (who build and run a cloud) and users (who work in one) are roles, described in the third person when they matter. Articles start from the learner's own questions and what they already know.

1. **Big picture first, then details.** Every article, and every section, opens with the idea in plain words: what it is, why it exists. The mechanism and the evidence come after, to confirm an idea the reader already holds.
2. **Explain each concept from first principles before it's used.** Say what it physically is, where it lives, the problem it solves, the trade-off, and the beginner's likely misconception. Only then name its kinds or options, as answers to that problem. A one-line definition isn't an explanation. The reader never meets a word before it's explained.
3. **One new concept at a time,** within the article's budget (about 3–5 new concepts, the analogy's words included).
4. **Details only when they serve the article's one idea.** A detail the reader must carry without needing it is a burden: defer it to the article whose scope covers it, or leave it out. "Under the hood" blocks (`??? info "Under the hood"`) are rare, never a dumping ground. Compare alternatives side by side only when the choice itself is the article's subject.
5. **Precision, shorthand included.** A short phrase must still be literally true. "A cluster runs exactly one hypervisor" was wrong: each host runs its own, and the hosts share a hypervisor *type*. "One storage room per wing" was wrong: a cluster has one or more primary storage pools. Check every claim about counts, ownership and scope ("one", "a", "its", "only", "always", "each") against the code and docs, in tables, captions, pictures and recaps too.
6. **Humanised and readable.** Write in a conversational tone, with plain sentences and paragraphs of one to three. Questions move the reader on ("So who starts the VM? Not the API."). Bust misconceptions out loud. Local analogies are short and used once; the running analogy comes from the strategy.
7. **Honest.** Say when something isn't used in the lab, flag docs-vs-code disagreements, and never present an inference as a fact or as the reason for a design.
8. **Spelling is British** in prose ("catalogue", "centre", "behaviour"); code and product names stay verbatim.
9. **Label the level** Beginner, Intermediate or Advanced (a range is allowed). A post is never labelled lower than the posts it builds on.

**Bold marks a defined term, at its definition, and nothing else**: no bold lead-ins, no bold for emphasis. The defined terms are the new concepts in the article's scope, so `.github/scripts/readability.py --budget N` can count them against the entry's budget. A plain word glossed in passing ("a mount, which attaches…") isn't bold.

**The style model is LearnKube's Kubernetes series**: the six articles under "Style model" in [references.md](00.Learn/references/references.md), analysed in the project memory (`learnkube-style`). Its traits:

- headings that say what each part does;
- short paragraphs;
- one concrete thread followed through the system;
- small step-by-step pictures;
- focus.

**Two optional lenses**, used sparingly (at most one or two per article, and only where they really help), as callouts so the main text never depends on them:

```
> [!TIP]
> **Kubernetes lens:** …

> [!TIP]
> **OpenStack lens:** …
```

The Kubernetes lens has nothing to do with CloudStack's own Kubernetes Service (CKS); say so wherever a reader could mix them up. OpenStack-lens links go only to docs.openstack.org or to **public** posts of the OpenStack course (<https://openstack.techphistudio.de/>).

### The running analogy: the cloud kitchen

A delivery app's virtual restaurant brands are cooked in shared kitchens, and a head office decides which kitchen cooks each one. So a VM is a virtual brand, a host a kitchen, the hypervisor that kitchen's equipment, a cluster a row of kitchens with the same kind of equipment, a pod a kitchen hub, a zone a city, and the management server HQ. The full mapping, with its evidence and the places it breaks, is §4 of `00.Learn/references/strategy/course.md`; each module plan lists the words it uses.

1. **Analogy words count in the article's concept budget.**
2. **Each word arrives when its concept is taught**, never as a mapping table up front: the full table lives in the strategy, not in a post.
3. **Pictures name both**: "kitchen (host)".
4. **Where the picture breaks, say so** in one sentence and carry on with the real thing (for example, networking below the virtual router's role, and the management server's internals).
5. **Precision holds inside the analogy.** Each kitchen has its own equipment, and the kitchens of a row have the same *kind*; a row has one or more cold stores. Say the real scale whenever a zone or pod is defined (a zone is usually a data centre, not a city).

Linux parallels ("a background job, like `cmd &`") may serve as one-off local bridges, never as a second running analogy.

### The article template

- A header line: `**Level:** … · **Type:** … · **Written against:** commit `<short sha>` · **Reading time:** …`. The type is one of Concept (explains one idea), Journey (follows one request or event through the system), Hands-on (lab steps, from the docs) or Exercises. Install posts also name the CloudStack release, and are written against its tag. The reading time comes from `.github/scripts/reading-time.py` (prose at 200 words a minute, plus 2 seconds per line of code, rounded to 5 minutes), never from a guess. **Hard cap: 30 minutes** (`--max 30`). The strategy entry sets each article's target, usually 10–20.
- A short opening: a hook, and the question the article answers.
- "What you'll learn": 3–5 outcomes.
- The body. It may hold optional **"Try it in your lab"** sections: short, marked optional, never needed to follow the article, with commands from the docs, and output shown only when it's quoted from the docs or the code, labelled so (the course never runs CloudStack itself).
- **"In short"**: 3–5 bullets recapping the article.
- "Check yourself": 3–5 questions that test understanding, all answerable from the visible article. The answers go on the article's own page in the module's `99.Check-Yourself-Answers/` folder (same file name), listed in that folder's `README.md`. It starts with its title, then `[← Back to the post](../<file>)`, and ends with an **"Evidence"** section (below).
- "Further reading": direct external links.
- `---`, then "**Next up:**" with a link.

Each module's last article is an **exercises article** (Type: Exercises), with its solutions on its answers page. The first article of each deep-dive module (02 onwards) opens with one small picture placing that module's part in the whole cloud, in the analogy's names: big picture first, at module level too.

Lists are real lists. Whenever a sentence introduces several items, use a bullet or numbered list. MkDocs is stricter than GitHub:

- leave a blank line before every list (inside a callout, a line holding just `>`);
- indent anything nested in a `- ` item by **4** spaces;
- leave a blank line before the next item when the previous one ends with a code block or a follow-on paragraph.

`.github/scripts/check-lists.py` checks this.

### Code: the source of truth, shown where it teaches

Every fact is verified against the code at the pinned commit, in the research dossier. The article **shows** code only where seeing it teaches something: a few short excerpts, each explained in a sentence or two, because many readers don't know Java.

- **No bare code links in the body.** Every code link has its excerpt beside it.
- The excerpts that back facts the body states in plain words go in the **"Evidence" section of the answers page**: each fact, then its excerpt and link. The evidence outlives the dossier, which is git-ignored.

Code links point at the commit the post is written against: `https://github.com/apache/cloudstack/blob/<full-sha>/<path>#L<n>` (or `#L<n>-L<m>`; add `?plain=1` before the anchor for a `.md` file). Write `@cloudstack@` in place of the SHA, and run `.github/scripts/pinned.py fill`, which fills in the post's own "Written against" commit. An answers page gets its post's commit. Never type a SHA. Excerpts and pinned links come only from apache/cloudstack; other repositories are cited as ordinary links.

Each excerpt is one contiguous range in a fenced block. A header comment in the file's own comment style comes first, then the lines verbatim (indentation may be removed). Paste it from `.github/scripts/pinned.py excerpt cloudstack:PATH:N-M`:

```java
// cloudstack: api/src/main/java/org/apache/cloudstack/api/APICommand.java, lines 28–30
@Retention(RetentionPolicy.RUNTIME)
@Target({TYPE})
public @interface APICommand {
```

- The header uses `// cloudstack: …` for Java and JavaScript, `-- cloudstack: …` for SQL, `<!-- cloudstack: … -->` for XML and Vue, and `# cloudstack: …` for everything else.
- **One contiguous excerpt per code block.** Never stack two headers in one block.
- Inside a table, quote the line inline in backticks next to its link.

`.github/scripts/check-excerpts.py` compares every excerpt and inline quote with the code in this repository's git history (no network needed). It also checks every apache/cloudstack link: a full SHA, a file that exists at that commit, and, in a post with a header, exactly the header's commit. If a commit is missing, run `git fetch upstream --tags`.

### Publishing

`00.Learn/` is built into a website with MkDocs Material (`mkdocs.yml`), in two places:

- **On this machine**, by the git-ignored local server: `.github/local/serve.sh` serves it at <http://localhost:8000/>, on port 8000 because a management server run from source takes 8080. It rebuilds within a second or two of saving a post, and its `README.md` explains it.
- **Publicly, on GitHub Pages**, at <https://lazybouy.github.io/cloudstack/> (since 2026-10-02). `.github/scripts/publish-pages.sh` builds the committed `learn` branch strictly and force-pushes the built files to the fork's `gh-pages` branch. Run it **only when the user asks**; the guard blocks the agents from it.

There's no access control: every page of the site is public. `00.Learn/references/publishing.md` explains the build, the checks and both ways of serving it.

`00.Learn/references/` (strategy, working files, archive, notes) is excluded from the site, so **posts never link into `references/`**. Before committing content, run:

- `.github/scripts/build-site.sh`: `mkdocs build --strict` (broken links and anchors) plus a guard against links into `references/`;
- `.github/scripts/check-diagrams.sh`, `check-lists.py` and `check-excerpts.py`;
- `.github/scripts/readability.py --check`: concept and code density;
- `.github/scripts/reading-time.py --check --max 30`.

Each folder's `README.md` is its landing page. The navigation follows the numbered names, with pages and folders sorted together (`awesome-nav`, `00.Learn/.nav.yml`). Each module needs a `.nav.yml` with its sidebar title (`title: "01 · General"`).

### Cross-references between posts

**Every mention of another post is a link**, never plain text. If the target isn't written yet:

1. Link to its stub. A stub is a placeholder page at the post's final path, marked `STUB:` in an HTML comment, created from the approved strategy.
2. Record the link, and what the text promises, in `00.Learn/references/in_progress_checks.md`. Rows come from links in written pages, not from stubs. A promise must fit the target's scope in the strategy.

When a stub becomes a post, resolve its rows first: keep each promise, point links at section anchors, and remove *(coming soon)*. `grep -rl 'STUB:' 00.Learn --exclude-dir=references` lists the stubs still pending.

### Diagrams

Diagrams are written in Mermaid and **published as PNG images**, so readers can click to enlarge them. For each diagram:

1. Put the source in the module's `diagrams/` folder as `NN-name.mmd` (`NN` is the article number).
2. Render it with `.github/scripts/render-diagrams.sh [file.mmd…]`. It runs the pinned Mermaid CLI in Docker and records the source's checksum in `diagrams/manifest.sha256`.
3. Embed the PNG with descriptive alt text, followed by `*Click the picture to enlarge it.*`.
4. Look at the PNG, and commit the `.mmd`, the `.png` and the manifest together. `check-diagrams.sh` fails on a stale picture.

Prefer **several small step pictures to one big diagram**:

- 2–6 boxes each, with the same layout from frame to frame and one new element per frame;
- a short note pointing at what changed, and a one-sentence caption under each picture;
- one colour per CloudStack part, the same in every article;
- labels with the analogy's name and the technical name in brackets: "kitchen (host)".

A tall picture (a vertical step sequence) would fill the page at the default 3× scale; its source may ask for less with a line `%% render-scale: 1.5`. Never size pictures with MkDocs-only attributes (`{ width=… }`): GitHub's Markdown view prints them as text.

Pictures cost no reading time. Give different kinds of lines visibly different styles, and say in the text what each style means. Mermaid drops an edge's `linkStyle` where edges cross; `.github/scripts/check-diagram-styles.py` catches it. If a style drops, reorder the nodes.

### Tooling: containers only

**Never install software on the host**, not even in the scratchpad, and **never build CloudStack** for the course: it reads the code, it doesn't run it. Run tools in Docker, with output going to the scratchpad (`$SP` below):

```sh
docker build -t cloudstack-blog -f .github/docker/blog.Dockerfile .github   # the blog image
.github/scripts/build-site.sh "$SP/site"                            # strict build + the references/ guard
.github/scripts/render-diagrams.sh 00.Learn/01.General/diagrams/NN-name.mmd
.github/scripts/check-diagrams.sh
.github/scripts/check-diagram-styles.py 00.Learn/01.General/diagrams/NN-name.mmd
.github/scripts/pinned.py excerpt cloudstack:api/src/main/java/org/apache/cloudstack/api/APICommand.java:28-30
.github/scripts/pinned.py fill 00.Learn/01.General/NN-x.md          # @cloudstack@ → the post's commit
.github/scripts/pinned.py written-against                           # the commit for a new post's header
.github/scripts/pinned.py --at 4.22.1.1 written-against             # … for an install post, at its release
.github/scripts/pinned.py path                                      # a folder with the code at the pin
.github/scripts/check-excerpts.py                                   # excerpts and code links match the code
.github/scripts/check-lists.py --site "$SP/site"                    # lists rendered as intended
.github/scripts/check-urls.sh 00.Learn/01.General/NN-x.md           # external links answer 2xx
.github/scripts/readability.py --check --budget 5 00.Learn/01.General/NN-x.md   # concept and code density
.github/scripts/reading-time.py --check --max 30                    # reading time right, 30 minutes at most
.github/local/serve.sh                                              # the site at http://localhost:8000/ (git-ignored)
.github/scripts/publish-pages.sh [--dry-run]                        # publish to GitHub Pages: only when the user asks
```

Reading code at a commit needs no copy: `git show <sha>:<path>` prints a file, and `git grep -n <pattern> <sha> -- <path>` searches one.

### Writing a post: the pipeline

Four agents and five skills, all in this repository's `.claude/` folder:

| Skill | What it runs |
|---|---|
| `/initiate-strategy <course \| Module> [amend] [notes]` | The `strategist`: the course map and analogy study, or a module's learning plan. The user approves it, then the main session creates the module skeleton (README, `.nav.yml`, stubs) |
| `/initiate-article <post> [notes]` | The full cycle for one post with an approved strategy entry: research → design and draft → audit → resolution → final checks → report. Takes `pause-after-research` or `pause-after-design` |
| `/initiate-research <post> [notes]` | The `researcher` only: the verified dossier, for the entry's in-scope concepts |
| `/initiate-authoring <post> [design-only \| draft-only \| revise] [notes]` | The `author` only: the design (restating the entry), then the draft |
| `/initiate-audit <post> [notes]` | The `auditor` (proofreader, editor and reader passes, findings only); then the main session resolves its findings |

- **Articles go one at a time.** Finish one post, report, and wait for the user before starting the next.
- **The auditor never edits a post.** It writes findings with evidence and proposed changes to `audit.md`. The main session verifies each one, applies, adapts or rejects it, adds its own fixes, and records every decision in *Resolution*. Rewrites of whole sections go back to the author (`revise`).
- **Working folders**, `00.Learn/references/articles/<Module>/<NN.Slug>/`, hold `research.md`, `design.md` and `audit.md`. They're **git-ignored**, like `references/handoff/`. The strategy documents are committed: they're the course's blueprint.
- The shared procedure is `.claude/skills/initiate-article/PIPELINE.md`; the agents' prompts are in `.claude/agents/`. New or edited agents and skills load only in a new session.
- **Permissions:**
    - Each agent has a tool allowlist and a guard hook, `.claude/hooks/guard.py`, registered in `.claude/settings.json`; it recognizes the agents by the hook input's `agent_type`.
    - The guard limits where each agent writes: the strategist `references/strategy/`, the researcher and the auditor their working files, the author `00.Learn/`.
    - It also blocks git changes, installs, Maven, docker beyond the blog and Mermaid images, and credentials, and fails closed on its own errors.
    - The hook command skips the guard if its file is missing, because a missing Python script exits with code 2 and would block every tool call.
    - Decisions are logged to `/tmp/cloudstack-learn-guard.log`.
    - `00.Learn/references/base_instruction_v0.md` is the guard's project marker: never move it.
- The agents never commit.

### Sources

The code is the source of truth. Design pages, pull requests and mailing-list threads say why a design was chosen; the official docs say how things are meant to be used; blogs give context. Check any claim against the code, and say so in the material where the docs and the code disagree.

Approved sources are listed in [00.Learn/references/references.md](00.Learn/references/references.md), and each host is allowed for WebFetch in `.claude/settings.json`; to add a source, add it to both. WebSearch is allowed; narrow it with `allowed_domains` to the listed hosts.

Installation facts come from the docs of **CloudStack 4.22**, the current LTS release (4.22.1.1, <https://docs.cloudstack.apache.org/en/4.22.1.1/>), and its API reference (<https://cloudstack.apache.org/api/apidocs-4.22/>). The docs' `latest` is 4.23.0.0. Explanations follow the pinned development code on `main` (24.0.0-SNAPSHOT).

The strategist, the researcher and the auditor have WebFetch and WebSearch, limited to the approved hosts. The author has neither, on purpose: it writes only from the dossier.

## Branches and remotes

- `origin` is the fork (`git@github.com:LazyBouy/cloudstack.git`). `upstream` is Apache CloudStack (`https://github.com/apache/cloudstack.git`, the read-only GitHub mirror of the ASF repository); only fetch from it.
- `main` mirrors `upstream/main`. It gets no commits of its own.
- `learn` is the working branch. **Never change CloudStack's code, or any upstream file, on `learn`**: commits touch only `00.Learn/`, `CLAUDE.md`, `.claude/`, `mkdocs.yml` and the course's own files in `.github/` (`README.md`, `.gitignore`, `.dockerignore`, `blog-requirements.txt`, `docker/`, and the scripts listed in "Tooling" above). Upstream merges therefore never conflict. The one exception would be upstream adding a `CLAUDE.md` of its own; keep ours if it does.
- The **pin** is the last upstream commit merged into `learn` (`.github/scripts/pinned.py sha`).

To bring in new upstream changes, **stay on `learn`**:

```sh
git fetch upstream --tags            # new commits, release branches and tags
git fetch . upstream/main:main       # fast-forward main without checking it out
git push origin main                 # keep the fork's main a mirror
git merge main                       # into learn; merge, don't rebase
```

Never check out `main` (or any other upstream branch) in this working tree: that removes `.claude/` and `CLAUDE.md` until you switch back. Merge, don't rebase: `learn` is meant to be published, and our paths don't overlap upstream's, so the merge has no conflicts.

Two upstream tools must stay off on `learn`:

- **GitHub Actions** on the fork. Upstream's workflows (a full Maven build, RAT, CodeQL, scheduled and agentic workflows) would run on pushes to `main`, and on `learn` if it became the default branch. Keep Actions disabled in the fork's settings.
- **pre-commit.** Never run `pre-commit install`: upstream's `insert-license` hook would stamp ASF licence headers onto every new `.md`, `.sh` and `.yml` of the course.

## How the codebase works

This guide to CloudStack's code is the researcher's map: it's how a post can say exactly which lines do what. Its build, lint, licence and test rules are CloudStack's own, for changes to CloudStack's code upstream. The course's files on `learn` follow the course rules above instead: no licence headers, and no Maven builds for the course.

### Project facts

These describe CloudStack itself, and the rules for contributing to it upstream. They're background for the course: on `learn`, CloudStack's code is never changed.

- Apache CloudStack: a Java IaaS orchestration platform (management server, hypervisor agents, system VMs) with a Vue 3 UI in `ui/`.
- `main` is `24.0.0-SNAPSHOT`. The version scheme jumps from 4.23 to 24.0.0, so upgrade classes and SQL files use names like `Upgrade42300to2400` and `schema-42300to2400.sql`.
- Branching (from CONTRIBUTING.md): bug fixes target a maintained release branch (`4.20`, `4.22`) and are merged forward into `main`. New features go to `main` only and are never backported. Record user-visible feature changes in `PendingReleaseNotes`.
- Security: read `SECURITY.md` and `THREAT_MODEL.md` before reporting or "fixing" a security issue. §3 lists what is out of scope and §11a lists recurring false positives. Report vulnerabilities privately to security@apache.org, never in public issues or PRs.
- Toolchain: CI builds with JDK 17, but the compiler level is Java 11 (`cs.jdk.version` in `pom.xml`), so don't use language features newer than Java 11. Other versions: Maven 3.9, Node 16 for the UI, Python 3.10 for Marvin and the systemvm scripts.

### Build

```bash
# What CI runs. -Dsimulator adds the simulator hypervisor.
# -Dnoredist adds VMware and other non-redistributable plugins; it needs deps/install-non-oss.sh run first.
mvn -P developer,systemvm -Dsimulator clean install -T$(nproc)
mvn -P developer,systemvm -Dsimulator clean install -DskipTests -T$(nproc)

# Rebuild a single module. Sibling SNAPSHOT modules must already be in ~/.m2, or add -am.
mvn -pl server install -DskipTests
mvn -pl plugins/hypervisors/kvm -am install -DskipTests
```

Profiles:

- `developer` adds the `developer/` (DB deploy), `tools/` (Marvin, apidoc) and `test/` modules.
- `systemvm` adds `systemvm/`.
- `-Dsimulator` adds `plugins/hypervisors/simulator` and bundles it into the client.
- `-Dnoredist` enables `vmware-base` and the other non-OSS plugins.

### Lint and license checks

- **Checkstyle** runs in the `validate` phase of every leaf module, so a violation fails any Maven build. Rules are in `tools/checkstyle/src/main/resources/cloud-style.xml`. It rejects:
  - trailing whitespace and tabs
  - unused, redundant, or star imports
  - imports of `org.apache.commons.lang.StringUtils` or `com.google.common.base.Strings`; use `org.apache.commons.lang3.StringUtils`

  Skip locally with `-Dcheckstyle.skip`.
- **ASF license header** is required on essentially every file: Java, Python, shell, SQL, XML, YAML, `.properties`, `.vue`, `.md`. CI fails through Apache RAT otherwise:
  `mvn -P developer,systemvm -Dsimulator -Dnoredist -pl . org.apache.rat:apache-rat-plugin:0.18:check` (report in `target/rat.txt`).
- **pre-commit** (see PRE_COMMIT.md) runs in CI. Hooks include license insertion, codespell, flake8, markdownlint, yamllint, gitleaks, and whitespace and EOF fixers.
  - `pip install -r requirements-dev.txt && pre-commit install`
  - `pre-commit run --all-files` runs every hook, `pre-commit run --all-files codespell` runs one, and `pre-commit run --files <paths>` checks specific files.

### Tests

#### Java unit tests

Java unit tests use JUnit 4 with Mockito: `MockitoJUnitRunner`, plus `@InjectMocks` and `@Spy` on the `*Impl` class. Surefire is 2.22.2.

```bash
mvn -pl server test -Dtest=UserVmManagerImplTest
mvn -pl server test -Dtest='UserVmManagerImplTest#testMethodName'
# With an empty ~/.m2, build upstream modules too:
mvn -pl server -am test -Dtest=UserVmManagerImplTest -Dsurefire.failIfNoSpecifiedTests=false
```

Several modules exclude tests through surefire `<excludes>` in their `pom.xml`. `server` excludes `*To*Test` upgrade tests and some DAO and VPC packages. If a test silently doesn't run, check that list.

#### Integration tests (Marvin + simulator)

These are Python nose tests in `test/integration/{smoke,component}`. They mirror `.github/workflows/ci.yml` and need a local MySQL. DB credentials come from `utils/conf/db.properties`, or a local `db.properties.override` next to it.

```bash
mvn -Pdeveloper -pl developer -Ddeploydb             # drops and recreates the cloud + cloud_usage DBs
mvn -Pdeveloper -pl developer -Ddeploydb-simulator
mvn -Dsimulator -pl :cloud-client-ui jetty:run        # UI/API on :8080, unauthenticated integration API on :8096
pip install tools/marvin/dist/[mM]arvin-*.tar.gz      # built by the developer profile
python3 tools/marvin/marvin/deployDataCenter.py -i setup/dev/advdualzone.cfg
nosetests --with-marvin --marvin-config=setup/dev/advdualzone.cfg \
  test/integration/smoke/test_vm_life_cycle.py -s \
  -a tags=advanced,required_hardware=false --zone=zim1 --hypervisor=simulator
```

Shared test helpers are in `tools/marvin/marvin/lib/{base,common,utils}.py`. To debug the management server, set `MAVEN_OPTS="... -Xdebug -Xrunjdwp:transport=dt_socket,address=8787,server=y,suspend=n"`. The default login is admin / password.

#### System VM / virtual router Python

`cd systemvm/test && ./runtests.sh` runs pycodestyle (max line 179), pylint, and the nose tests against `systemvm/debian/opt/cloud/bin`.

#### UI (`ui/`)

```bash
npm install
npm run serve        # dev server on :5050; set CS_URL=http://localhost:8080 in ui/.env.local
npm run lint
npm run test:unit
npx vue-cli-service test:unit tests/unit/views/AutogenView.spec.js   # single spec
npm run build
```

### Architecture

#### Request path

An API request travels through these layers:

1. API command
2. service or manager
3. orchestrator
4. agent `Command`
5. hypervisor resource

What each top-level directory owns:

- **`api/`** holds the public API surface:
  - API commands live in `org.apache.cloudstack.api.command.{admin,user}`. They extend `BaseCmd`, `BaseAsyncCmd` or `BaseListCmd` and are annotated with `@APICommand(name, responseObject, authorized, since)`. Their `@Parameter` fields use names from `ApiConstants`.
  - Response classes and the `*Service` interfaces the commands call also live here.
  - So do the base agent `Command`/`Answer` types (`com.cloud.agent.api`).
- **`server/`** is the management server core. `ApiServer` and `ApiServlet` hand requests to `ApiDispatcher`, which runs the dispatch chain in `com.cloud.api.dispatch` (unpack, validate, and resolve parameters; `ParamProcessWorker` turns UUIDs into entities and enforces `@ACL` access checks on them). The command then calls the `*ManagerImpl` or `*ServiceImpl` business logic.
  - Responses are built in `ApiResponseHelper`.
  - `list*` APIs read denormalized MySQL views through `QueryManagerImpl` and `*JoinVO` (`com.cloud.api.query`).
- **`engine/`** holds:
  - `orchestration/`: `VirtualMachineManagerImpl`, `NetworkOrchestrator`, `VolumeOrchestrator`.
  - `storage/`: the pluggable storage subsystem (`DataStoreProvider`, `PrimaryDataStoreDriver`, `DataMotionStrategy`; interfaces in `engine/api`).
  - `schema/`: every `*VO` entity, every DAO, and the DB upgrade machinery.
  - `components-api/`: manager interfaces shared across modules, such as `AgentManager`.
- **`framework/`** is infrastructure:
  - `db`: `GenericDaoBase`, `SearchBuilder`/`SearchCriteria`, `Transaction`.
  - `config`: `ConfigKey`.
  - `jobs`: `AsyncJobManager`.
  - `spring/module`: plugin loading.
  - Also `events`, `cluster`, `managed-context`, `extensions`, `ca`, `kms`, `quota`.
- **`core/`** has `ServerResource` and the `@ResourceWrapper` command-dispatch base, plus the root Spring module definitions.
- **`agent/`** is the standalone agent JVM (`AgentShell`) that runs on KVM hosts. The KVM logic itself is in `plugins/hypervisors/kvm`: `LibvirtComputingResource`, plus one `Libvirt<X>CommandWrapper` per command in `resource/wrapper/`.
- **`plugins/`** holds everything pluggable: hypervisors, network elements, storage drivers (`plugins/storage/volume/*`), ACL, user authenticators, API plugins, integrations (Kubernetes and others), backup providers, and more.
- **`services/`** has the console-proxy and secondary-storage system VM services.
- **`systemvm/`** builds the system VM agent. Its `systemvm/debian/opt/cloud/bin/` holds the virtual router's Python and bash configuration (`configure.py`, `cs_*.py`), driven by JSON "databags" pushed from the management server.
- **`usage/`** is the separate usage-server process.
- **`client/`** assembles the management server webapp (`cloud-client-ui`). Its config templates are `client/conf/*.in`, and a plugin is bundled only if it is a dependency in `client/pom.xml`.
- **`extensions/`** has sample orchestrator scripts (Proxmox, HyperV, MaaS) for the Extensions framework, which is the "External" hypervisor type: `plugins/hypervisors/external` plus `framework/extensions`.
- **`scripts/`** holds shell and Python scripts that are installed on hosts or the management server and invoked by resources.
- **`tools/marvin/`** is the Python API client and test framework. **`tools/apidoc/`** generates the API docs.

#### Spring module system (how beans and plugins are wired)

There is no component scanning, so a new bean must be declared in a Spring XML context; annotations alone do nothing.

- **Module files.** Every module ships `src/main/resources/META-INF/cloudstack/<name>/module.properties` (`name=`, `parent=`) and `spring-<name>-context.xml`.
- **Hierarchy.** Module contexts form a hierarchy defined in `core/src/main/resources/META-INF/cloudstack/`: `bootstrap` → `system` → `core`. Under `core` sit `api` and `backend`, and `backend` is the parent of `compute`, `network` and `storage`. Planner, discoverer and similar parents also live there. A child context sees its parents' beans.
- **Registries.** The `*-context-inheritable.xml` files declare `RegistryLifecycle` beans that collect every bean implementing an extension interface (`HypervisorGuru`, `Investigator`, `NetworkElement`, user authenticators, …) into a registry. A plugin therefore only declares its bean in its own context under the right parent.
- **Ordering.** Some registries are ordered or filtered by global settings (`*.order`, `*.exclude`). Whole modules can be dropped with `modules.exclude`.
- **DAOs.** Core DAOs are declared in `engine/schema/src/main/resources/META-INF/cloudstack/core/spring-engine-schema-core-daos-context.xml`.

#### Adding an API command

1. Write the command class with `@APICommand` and `@Parameter` fields. Its `execute()` calls a service method and sets the response object.
2. Register the class in the owning service's `getCommands()`:
   - `ManagementServerImpl.getCommands()` for core APIs
   - the plugin's `PluggableService` implementation for plugin APIs
3. Set `authorized = {RoleType...}`. Root Admin can call every API. For other roles, `DynamicRoleBasedAPIAccessChecker` checks explicit `role_permissions` rules first and otherwise falls back to the annotation's `authorized` list. Only special roles, such as Read-Only, need explicit rules, added in the upgrade SQL with `IDEMPOTENT_UPDATE_API_PERMISSION`.
4. To expose the command in the UI, reference it from `ui/src/config/section/*.js`. Sections and actions name the API they call (`api:`, `permission:`), and the UI shows them only if `listApis` returns that API for the user's role. Add label strings to `ui/public/locales/en.json`.

#### Global settings

Declare a `ConfigKey<T>` constant on a class that implements `Configurable` and return it from `getConfigKeys()`. `ConfigDepot` registers the key in the `configuration` table at startup, so no SQL is needed. Scope (global, zone, cluster, account, domain, storage pool, …) is set on the key.

#### Database schema and upgrades

- **Fresh databases.** `setup/db/create-schema.sql` is the frozen 4.0.0 base, and `DatabaseUpgradeChecker` replays the whole upgrade chain on top of it, even for fresh installs. So never edit the base schema.
- **Schema changes.** Put them in the newest `engine/schema/src/main/resources/META-INF/db/schema-<from>to<to>.sql`, currently `schema-42300to2400.sql`, with a `-cleanup.sql` companion. Use the idempotent procedures from `db/procedures/`, for example `` CALL `cloud`.`IDEMPOTENT_ADD_COLUMN`(...) ``.
- **Java migrations.** Data migrations that need Java go in the matching `com.cloud.upgrade.dao.Upgrade<from>to<to>` class. A new version step must be chained in `DatabaseUpgradeChecker`.
- **Views.** Each view backing a `*JoinVO` is one file in `db/views/`, re-applied on every upgrade. Edit that file instead of redefining the view in an upgrade script.

#### Async jobs and agent communication

- **Async jobs.** Long-running APIs extend `BaseAsyncCmd` and run as async jobs (`framework/jobs`). VM operations are also serialized per VM through `VmWork*` work jobs handled by `VirtualMachineManagerImpl`.
- **Agent commands.** The management server sends `Command` subclasses to hosts through `AgentManager`. On the resource side, `@ResourceWrapper(handles = X.class)` classes are discovered by `RequestWrapper`. Adding a new host-side operation means three pieces:
  - a `Command`/`Answer` pair
  - a wrapper in each relevant hypervisor plugin
  - simulator handling (`plugins/hypervisors/simulator`, `SimulatorManagerImpl`), if Marvin simulator tests should exercise it
