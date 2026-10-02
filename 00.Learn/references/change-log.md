# Change log

Where the learning material and its tooling were changed, and why. Newest entries first. Like everything in `references/`, this file isn't published on the blog.

How to read an entry:

- **Line numbers** are those of each file *after* the change, as committed. To see the exact before-and-after text of a file, run `git diff <commit before> <commit after> -- <file>` (the commits are named in each entry).
- **Finding IDs** (A1, A2, …) are the auditor's findings for a post. The full findings, with their evidence and the resolution of each, are in `articles/<Module>/<post>/audit.md`. The `articles/` folder is git-ignored, so those files exist only on the author's machine.

---

## 2026-10-01: module 01's learning plan approved; its skeleton built

**Commits:** the first commits of the course on `learn`, 2026-10-02 (see `git log`).

**What happened:** the strategist proposed module 01's plan ([`strategy/01.General.md`](strategy/01.General.md)): six outcomes, a ledger of 63 concepts, sixteen articles and seven first-principles chains. The user approved it with the university running example and the module palette, and decided:

- twelve analogy words counted in the budgets, six descriptions glossed;
- the KVM lab on Ubuntu 24.04 LTS, not EL8. The strategist re-planned 14 and 15 from the 4.22.1.1 docs, with a route table naming every gap from the EL8 quick guide;
- the simulator image `4.22.1.0` (Docker Hub has no `4.22.1.1`);
- two lab articles, with the system VM template seeded automatically;
- new sources: hub.docker.com, for the simulator's tags only, and the Ubuntu Server docs, Ubuntu manpages and the MySQL manual, for the lab's facts only.

| Changed | How |
|---|---|
| `strategy/01.General.md` | Approved; entry 10's "15 installs" corrected to "15 shows CloudStack seeding it" (wording only) |
| `01.General/README.md`, `.nav.yml` | The module's landing page: outcomes and the reading order in six parts; sidebar title "01 · General" |
| `01.General/01…16.*.md` | Sixteen stubs, each pointing at its strategy entry in an HTML comment |
| `01.General/99.Check-Yourself-Answers/` | The answers folder, empty until the first article |
| `references.md`, `.claude/settings.json` | The four new sources, each limited to its purpose |

---

## 2026-10-01: the course strategy approved

**Commits:** the first commits of the course on `learn`, 2026-10-02 (see `git log`).

**What happened:** the strategist proposed the course strategy ([`strategy/course.md`](strategy/course.md)): eleven traits of CloudStack with evidence, a module map, and two analogy candidates with five dropped pictures. The user chose:

- the cloud kitchen as the running analogy;
- the module map as proposed (01–10, with 11.Beyond-VMs optional);
- the hands-on lab at the end of 01.General;
- one exercises article per module;
- all the template changes (the "Type" values, optional "Try it in your lab" sections, the exercises article, an opening picture for each deep-dive module).

| Changed | How |
|---|---|
| `strategy/course.md` | Approved; Candidate A marked chosen; the decisions recorded |
| `00.Learn/README.md` | Every module of the map, with the question it answers |
| `CLAUDE.md` | "The running analogy: the cloud kitchen" with its five rules; the template's "Type" values, "Try it in your lab", the exercises article and the module opening picture; diagram labels "kitchen (host)" |

---

## 2026-10-01: the first attempt archived; strategy first

**Commits:** the first commits of the course on `learn`, 2026-10-02 (see `git log`).

**What happened:** the user judged the first articles (post 01, Overview; post 02, Architecture, in two parts) low quality. They confused instead of clarifying, they were dense and dry, and concepts and details were "dumped on the reader". The course had been built as a replica of the OpenStack course: its module shape, hotel metaphor, post sequence and template, with CloudStack fitted into them. The user's direction, verbatim, is in [`base_instruction_v1.md`](base_instruction_v1.md). The approved plan:
- archive the first attempt;
- add a **strategist** stage before the researcher, which plans each module as a series of short articles with explicit scopes and proposes a CloudStack-specific analogy;
- rewrite the writing standards for CloudStack: the learner voice, first principles, details only when they serve, code shown only where it teaches, and evidence on the answers pages.

**Feedback from the user that the first attempt failed** (each one now a standing rule):
1. Big picture first, then details: the posts were dry and bogged down by minute details.
2. Perspectives switched confusingly. The fix: one voice, now the learner's.
3. Technically wrong shorthand: "a cluster runs exactly one hypervisor" (the hosts share a hypervisor *type*), and "one storage room per wing" (a cluster has one or more primary storage pools).
4. Concepts were dumped, not explained: the storage section named three storage scopes before saying what a VM's disk is or why other hosts must reach it.
5. The split into two parts was arbitrary, and the course was an OpenStack template.

| Moved | To |
|---|---|
| `01.General/` (posts 01–02, answers, 11 stubs, diagrams) | [`archive/v1/01.General/`](archive/v1/01.General/README.md) |
| `references/articles/01.General/` (dossiers, designs, audits) | `archive/v1/working/01.General/`: local only (git-ignored) |
| The home page and the tracker's rows | copies in `archive/v1/`. The home page is now minimal, and module 01 is a stub until its strategy is approved |

| Changed | How |
|---|---|
| `CLAUDE.md` | The course section rewritten for CloudStack: the OpenStack course is an example of process and tooling only; "How the course is planned: strategy first"; the learner voice; first principles; one concept at a time; details only when they serve; bold only for defined terms; code shown only where it teaches, with no bare code links, and supporting excerpts in the answers page's Evidence section; lenses sparing; the slimmed template ("In short" replaces the one-paragraph version; answers in `99.Check-Yourself-Answers/`); the hotel mapping removed. "Branches and remotes" and "How the codebase works" unchanged |
| `.claude/agents/strategist.md`, `.claude/skills/initiate-strategy/` | New: the strategist agent and its skill. It writes `references/strategy/course.md` (module map, 2–3 analogy candidates with mappings and stress tests) and `references/strategy/<Module>.md` (concept ledger, learning path); the user approves; the main session builds the module skeleton |
| `.claude/hooks/guard.py` | New role `strategist`: writes only `references/strategy/`; may not run `pinned.py fill` or `render-diagrams.sh`. 64 cases pass on both the `agent_type` and the role-argument paths |
| `.claude/skills/initiate-article/PIPELINE.md`, the other three `initiate-*` skills | No stage runs without an approved strategy entry; the entry goes into every agent's prompt; amendment requests stop the pipeline for the user; no more folder series; `readability.py` in the checks |
| `.claude/agents/{researcher,author,auditor}.md` | Each reads the strategy entry as its brief. The researcher goes deep on the scope only and explains each concept from first principles; the author restates the entry in `design.md` and keeps to its budget and target; the auditor checks scope adherence |
| `.github/scripts/readability.py` | New: defined terms against a budget, and bold, code and inline-code density per 1,000 words (gated); sentence and paragraph length (reported). Every archived v1 post fails it |
| `references/strategy/README.md`, `references/publishing.md`, `.claude/settings.json` | The strategy folder explained; the checks list updated; `readability.py` pre-approved |
| Project memory | The hotel and the operator voice removed; new `openstack-not-a-template`; the strategist in `article-pipeline`, `cross-post-links` and `cloudstack-learning-project` |

---

## 2026-10-01: post 02 split into a two-part series, after the user's feedback

**Commits:** the first commits of the course on `learn`, 2026-10-02 (see `git log`).

**What happened:** the user found posts 01–02 "very dry with flow getting bogged down by minute details", and confusing in perspective. The new rules: big picture first, then details; one operator perspective, with the user's side named explicitly; 30 minutes at most per post, with a split into parts written and audited in one cycle. They're in `CLAUDE.md` ("Writing rules"), the project memory (`post-shape-feedback`), the pipeline and the agents. `reading-time.py` gained `--max 30`, and `pinned.py` now finds a series part's answers page. Post 02 (42 min) became a series in one cycle: the author's rework (design R0–R9), one audit (25 findings: 11 should-fix, 14 nice-to-have, no blocker), one resolution. Details are in `articles/01.General/02.Architecture/audit.md`; the previous single post is kept there as `v1-post.md` and `v1-answers.md`.

| File | Change |
|---|---|
| [`01.General/02.Architecture/`](archive/v1/01.General/02.Architecture/README.md) | `README.md` (the series' big picture), [part 1: Where Does Everything Live?](archive/v1/01.General/02.Architecture/01.Where-Everything-Lives.md) (26.7 min), [part 2: Who Calls Whom?](archive/v1/01.General/02.Architecture/02.Who-Calls-Whom.md) (29.0 min), `.nav.yml` |
| `08.Check-Yourself-Answers/02.Architecture/` | One answers page per part; part 1's answer 4 corrected (two databases, two settings) |
| `01.General/diagrams/` | New `02-series`, `02-lab`, `02-lab-plan`, `02-storage`; operator wording in `02-lab` and `02-machines` |
| `01.Overview.md`, module and answers READMEs, `in_progress_checks.md` | Links and rows moved to the parts |
| `CLAUDE.md`, `.claude/` (pipeline, author, auditor), `.github/scripts/reading-time.py`, `pinned.py` | The three rules, series handling, `--max 30`, answers pages at the post's path |

**Worth knowing for later posts:** a check-yourself question must be answerable from the visible post, not only from under the hood; operator perspective covers pictures and alt text; a part that readers can land on directly re-glosses the series' own metaphors; say what a one-host lab can't show (live migration, the neighbour check, HA).

---

## 2026-10-01: post 02, "Architecture: One Head Office, Many Floors", and the style model

**Commits:** the first commits of the course on `learn`, 2026-10-02 (see `git log`).

**What happened:**
- The user named LearnKube's Kubernetes series as the style model for the whole course. The style was analysed from the six articles and recorded in the project memory (`learnkube-style`), [`references.md`](references.md) ("Style model") and `CLAUDE.md` (writing rules, diagrams). The author and auditor prompts were aligned with it.
- Post 02 went through the pipeline: research (86 findings), design (approved, about 40 minutes), a draft in the new style (one host's journey, 15 small pictures), and an audit (40 findings: 1 blocker, 17 should-fix, 22 nice-to-have). The resolution applied, adapted or rejected each one; details in `articles/01.General/02.Architecture/audit.md`.

| File | Change |
|---|---|
| `01.General/02.Architecture.md` (since split into [`02.Architecture/`](archive/v1/01.General/02.Architecture/README.md)) | The post, replacing its stub: 7,176 words, 192 code lines, about 40 minutes |
| `01.General/08.Check-Yourself-Answers/02.Architecture.md` and its `README.md` | The answers page; answer 2 corrected after the audit (a crash is noticed at once, a hang after 150 s) |
| `01.General/diagrams/02-*.{mmd,png}`, `manifest.sha256` | 15 pictures: the building plan, the lab map, and step sequences (the staff line, phone and hands, staff rooms, the intercom) |
| `01.General/01.Overview.md` | Links to 02 without *(coming soon)*, one pointing at `#the-attendant-phones-in`; the hotel table's guest-network row now "Guest corridors" |
| `in_progress_checks.md` | Post 02's rows resolved; new rows for its links to 03–07 and 11 (the 11 row now also carries the bridge-layout comparison cut from 02) |
| `CLAUDE.md` | The style model; small step pictures; mapping additions (the staff line, the engineer's one visit, the intercom, the traffic types' routes, the phone and the hands); "one lift" dropped from the cluster mapping |
| `.claude/agents/author.md`, `auditor.md` | The style model in their language, form and diagram rules (they load in a new session) |
| [`references.md`](references.md), `.claude/settings.json` | The six style-model articles; WebFetch for learnkube.com |

**Worth knowing for later posts** (the audit's "For future posts"): a JPA `nullable` annotation isn't the database constraint; "how long until CloudStack notices" has two paths, silence and a closed connection; HA restarts only HA-enabled VMs and skips local storage; a design-note quote must fit the sentence it supports; gloss every first-use acronym and Java construct whose meaning is the point; leave about a minute of reading-time headroom for the audit.

---

## 2026-10-01: post 01, "What Is CloudStack? A Hotel for Computers"

**Commits:** the first commits of the course on `learn`, 2026-10-02 (see `git log`).

**What happened:** the first post went through the full pipeline: research (73 findings), design (paused for the user, approved with all nine defaults), draft, audit (28 findings: 10 should-fix, 18 nice-to-have, no blockers) and resolution (19 applied, 9 adapted, 0 rejected outright; one optional sub-change rejected). Details: `articles/01.General/01.Overview/` (research.md, design.md, audit.md with its *Resolution*).

| File | Change |
|---|---|
| [`01.General/01.Overview.md`](archive/v1/01.General/01.Overview.md) | The post, replacing its stub: 5,571 words, 133 code lines, 39 excerpts (with the answers page), about 30 minutes |
| `01.General/08.Check-Yourself-Answers/01.Overview.md` and its `README.md` | The answers page, listed |
| `01.General/diagrams/01-hotel.{mmd,png}`, `manifest.sha256` | The hotel at a glance; after the audit (A7), the head office's boxes are joined: desk → work-order board → managers, desk → guest registry |
| `01.General/README.md` | Row 01 without *(coming soon)* |
| `in_progress_checks.md` | 23 rows for the post's links to unwritten posts |
| `00.Learn/README.md` | LTS: "two years (all fixes for 18 months, then blocker and security fixes for six more)", per the LTS page (the downloads page still says 18 months) |
| `CLAUDE.md` | The hotel mapping refined (design §13, user-approved): offerings are room types (sizes, not prices); a cupboard on the floor (host-local storage); attendants only on KVM floors; the hypervisor is the floor's machinery; a VPC is a private annexe; the console proxy is a remote-control window; the head office's four inner parts (audit A28) |
| `.claude/agents/author.md` | Answers pages start with their title, then the back link (audit A24) |

**Worth knowing for later posts** (from the audit's "For future posts"): check wiki authorship from the page metadata, not its title; check sister-course anchors on the live site; test borrowed analogies for direction (the OpenStack course's take-and-bake pizza maps IaaS the wrong way round); join the boxes inside a diagram's container so a request's path reads end to end.

---

## 2026-10-01: sources from the user's resource list

**Commits:** the first commits of the course on `learn`, 2026-10-02 (see `git log`).

**What happened:** the user gave a list of CloudStack resources (main docs, Usage/Admin Guide, Developers Guide, Programmer Guide, API reference, wiki, mailing lists, documentation repository, downloads) to add as approved sources, with WebSearch and WebFetch for the agents and the main session. Every resource was looked up on the project's website and docs, and every claim in the list checked against its page: the docs' `latest` is 4.23.0.0; the Usage Guide has a "Provisioning and Authentication API" chapter; the Programmer Guide covers API keys, the request format and signing, event types and time zones; API references back to 4.11 and 4.14 are still online; the downloads page links the signed source releases and the community-built CloudMonkey binaries. Every URL answered 200.

| File | Change |
|---|---|
| [`references.md`](references.md) | The wiki home, the mailing lists page and the docs repository under "Design rationale"; the Usage, Developers and Programmer guides and the per-version API reference under "Official documentation", with a note on 4.22.1.1 vs `latest`; a new "Releases and packages" table (`dlcdn.apache.org`, `archive.apache.org`, CloudMonkey releases, `download.cloudstack.org`) |
| `.claude/settings.json` | WebFetch allowed for `dlcdn.apache.org`, `archive.apache.org`, `download.cloudstack.org` and `gitbox.apache.org` (the other resources were on hosts already allowed). WebSearch was already allowed |
| `.claude/agents/auditor.md` | The auditor gets WebSearch too, limited to approved hosts. The researcher already had both tools; the author has neither, on purpose: it writes only from the researcher's dossier |

---

## 2026-10-01: project set up

**Commits:** on top of upstream `1a48a87587` ("Add the ASF Allowlist check workflow (#14113)"), on the new `learn` branch, not yet committed.

**What happened:** the user asked for the structure of their OpenStack course (`/root/projects/openstack/openstack`: `CLAUDE.md`, `00.Learn/`, `.claude/`) to be replicated for CloudStack, with the same pedagogic goal, and with publishing only on a git-ignored local server for now. The request is kept verbatim in [`base_instruction_v0.md`](base_instruction_v0.md).

### Decisions taken with the user

- **D1 · No access control for now.** Every post is visible on the local server. Adding OpenStack's per-post access later changes no post, because unmarked posts default to restricted there (see [`publishing.md`](publishing.md#publishing-somewhere-public-later)).
- **D2 · Two lenses.** Optional "Kubernetes lens" and "OpenStack lens" callouts.
- **D3 · Branches.** `learn` for all course work, `main` an untouched mirror of upstream, and a new `upstream` remote (apache/cloudstack, fetch only).
- **D4 · Metaphor.** The hotel from the OpenStack course, CloudStack edition: one head office (the management server) instead of many departments. The mapping is in `CLAUDE.md`.

### What was adapted from the OpenStack project

| OpenStack | CloudStack | Why |
|---|---|---|
| One pin per submodule (`git ls-tree`) | One pin: the last upstream commit merged into `learn` | CloudStack is one repository |
| `opendev.org` links, `@repo@` placeholders | `github.com/apache/cloudstack/blob/<sha>/…` links, `@cloudstack@`, filled with the post's own "Written against" commit | GitHub is CloudStack's public mirror; a revised post keeps one commit |
| Header "Written against: superproject `…`" | "Written against: commit `…`" | No superproject |
| `# repo: path, lines N–M` excerpt headers | `// cloudstack: …` (Java, JS), `-- cloudstack: …` (SQL), `<!-- cloudstack: … -->` (XML, Vue), `# cloudstack: …` (other) | Comment style of each language |
| `check-excerpts.py` fetches from opendev | Reads the code from local git: offline | All upstream commits are in this repository |
| Install target: OpenStack 2026.1 | CloudStack 4.22 LTS (4.22.1.1) | The current long-term-support release |
| Cloudflare Worker, access hook, publish workflow | Not copied (D1); a git-ignored local server on port 8000 instead | Localhost only for now; 8080 is the management server's port |
| Root `.gitignore` edits | Nested `.github/.gitignore` and `00.Learn/references/.gitignore` | `learn` touches no upstream file, so merges stay conflict-free |
| Sync recipe switches to `master` | Sync recipe never leaves `learn` (`git fetch . upstream/main:main`); the guard's hook command tolerates a missing guard file | Leaving `learn` removes `.claude/`, and a missing guard script exits with code 2, which blocks every tool call |
| Guard | Also blocks `mvn`, more git subcommands (`bisect`, `remote`, `tag` except listing, …), `npm ci`, and `docker run` with any image but the blog and Mermaid ones | CloudStack is a Maven project; the agents read code, they don't build it |

### Files created

| Area | Files |
|---|---|
| Course | `00.Learn/README.md`, `00.Learn/.nav.yml`, `01.General/{README.md,.nav.yml}`, 12 stubs (posts 01–07, 09–13; 11 is a folder), `08.Check-Yourself-Answers/{README.md,.nav.yml}` |
| References | `base_instruction_v0.md`, `references.md`, `in_progress_checks.md`, `publishing.md`, this file, `.gitignore`; `handoff/README.md` (git-ignored) |
| Pipeline | `.claude/agents/{researcher,author,auditor}.md`, `.claude/skills/initiate-{article,research,authoring,audit}/SKILL.md`, `.claude/skills/initiate-article/PIPELINE.md`, `.claude/hooks/guard.py`, `.claude/settings.json` |
| Tooling | `mkdocs.yml`, `.github/{README.md,blog-requirements.txt,.dockerignore,.gitignore}`, `.github/docker/blog.Dockerfile`, `.github/scripts/{pinned.py,check-excerpts.py,check-lists.py,check-diagrams.sh,render-diagrams.sh,check-diagram-styles.py,check-urls.sh,reading-time.py,build-site.sh}`; `.github/local/` (git-ignored) |
| Guide | `CLAUDE.md`: course conventions, plus the codebase guide written by `/init` |
