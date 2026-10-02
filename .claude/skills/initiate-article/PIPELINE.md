# The article pipeline

Shared by the four skills `initiate-article`, `initiate-research`, `initiate-authoring` and `initiate-audit`. You, the main session, are the **orchestrator**:

- you resolve the target and its strategy entry,
- you launch the agents one at a time,
- you check what each one hands back,
- you relay questions and amendment requests to the user,
- you **verify the auditor's findings and apply the changes** (§5),
- you run the final verification and report.

You don't draft the post yourself; the author does. But after the audit, you're the editor-in-chief: the auditor only proposes, and you decide and make the changes.

| Stage | Who | Writes |
|---|---|---|
| Plan (before this pipeline) | `strategist`, via `/initiate-strategy` | The module's learning plan, `00.Learn/references/strategy/<Module>.md`. Each article's **entry** (scope in and out, budget, target length, thread) is the binding brief for every stage below |
| Research | `researcher` | `research.md`: every fact the entry's scope needs, with verbatim evidence from the pinned code or an approved source |
| Authoring | `author` | `design.md` (the entry restated, then the post designed from the learner's point of view), then the post, its answers page (with its Evidence section), its diagrams and the cross-link bookkeeping |
| Audit | `auditor` | `audit.md`: detailed findings from three passes (proofreader, editor, reader), each with its evidence and a proposed change, including scope adherence. It never edits the post |
| Resolution | you | The changes, after you've verified every finding (applied, adapted, rejected, or added by you), recorded in `audit.md` |

The standards all of them follow are in `CLAUDE.md` and in the project memory (`~/.claude/projects/-root-projects-cloudstack-cloudstack/memory/`). The agents' permissions come from `.claude/agents/<name>.md` (tools, and a guard hook, `.claude/hooks/guard.py`) and from `.claude/settings.json`.

## 1. Resolve the target and its strategy entry

The first word of the arguments names the post. Everything after it is notes from the user, passed verbatim to every agent. Recognize these flags among the notes:

- `pause-after-research`, `pause-after-design` (for `initiate-article`),
- `design-only`, `draft-only`, `revise` (for `initiate-authoring`).

Accepted forms:

- A bare number: `03` or `3`.
- A number with its name: `03.Some-Topic`.
- A module prefix: `01.General/03`, `01.General/03.Some-Topic`, `02.Management-Server/01`.
- A path to the `.md` file.

To resolve it:

1. Find the post's **strategy entry**: the `### NN.Slug: …` heading in the learning path of `00.Learn/references/strategy/<Module>.md`. If the user gave no module, look in every module's plan; if a bare number matches in several, ask the user which one with AskUserQuestion.
2. **The entry's `Status:` must be `approved …`.** If there's no entry, or it's only `proposed`, stop: no stage runs without an approved brief. Offer `/initiate-strategy <Module>` (no plan yet, or a new article: `/initiate-strategy <Module> amend` with the user's idea as notes).
3. The post's file is `00.Learn/<Module>/NN.Slug.md`. The main session created it as a stub when the plan was approved; if it's missing, create the stub first, as `/initiate-strategy` §6 describes.

**Only the strategy splits topics.** There are no folder series: one entry, one article, one cycle. If a stage finds the entry's scope can't be taught well in one article within its target (it needs a concept the entry doesn't have, or it would run past 30 minutes), that's an **amendment request** (§4), never a silent split or a silent scope change.

The **working folder** mirrors the post's path under `00.Learn/references/articles/`, without `.md`: `00.Learn/01.General/03.Some-Topic.md` → `00.Learn/references/articles/01.General/03.Some-Topic/`.

The working files are **local only**. `00.Learn/references/.gitignore` excludes the whole `articles/` folder: the research dossier, the design, and the audit findings with your resolutions are messages between the agents and you, not part of the course. Only the finished post, its answers page, its diagrams and the bookkeeping edits are committed. (`references/` is left out of the blog as well.) Because they're never committed, keep them until the post is done: they're the record of where every fact came from while you work. The answers page's **Evidence** section carries the supporting excerpts forward.

Tell the user in one line what you resolved (post, strategy entry, working folder, stages to run) before launching anything.

## 2. Preconditions for each stage

Every stage needs the **approved strategy entry** (§1). Then:

| Stage | Needs | If it's missing |
|---|---|---|
| Research | Nothing more. If `research.md` exists, the researcher updates it | — |
| Authoring (`design-only`, or design + draft) | `research.md`, with no unresolved **BLOCKING** item in its §12 and no open amendment request | Offer to run the research first, or ask the user to resolve the blocking items or the request |
| Authoring (`draft-only`) | `research.md` and `design.md` | Offer the missing stage |
| Authoring (`revise`) | The drafted post, and `audit.md` with your *Resolution* for the findings the author should address | Offer an audit first, or resolve the audit (§5) first |
| Audit | A drafted post (the file no longer contains `STUB:`), plus `research.md` | Offer the missing stage |

Also run `git status --short`. If there are uncommitted changes that aren't from this pipeline, mention them to the user, but carry on; the agents never commit. Check too that you're on the `learn` branch.

## 3. Launching an agent

Use the Agent tool with `subagent_type` set to `researcher`, `author` or `auditor`, and `run_in_background: false`: each stage needs the previous one's output. Give the agent this prompt, filled in:

```text
Target post: 00.Learn/<Module>/NN.Slug.md
Strategy entry: 00.Learn/references/strategy/<Module>.md, "NN.Slug" (approved <date>); target <N> minutes, budget <N> defined terms
Working folder: 00.Learn/references/articles/<Module>/NN.Slug/
Mode: research | design+draft | design-only | draft-only | revise (address findings <IDs>, as decided in audit.md's Resolution) | audit
Previous article in the module: <path or "none">   Next: <path or "none">
User's notes: <verbatim, or "none">
Follow your agent instructions in full, and return the summary they ask for.
```

If an agent reports that the guard hook blocked something it genuinely needs:

- don't loosen the permissions yourself,
- tell the user what was blocked and why the agent needed it,
- let them decide.

## 4. Between stages

- **Amendment requests, at any stage.** Each agent records a strategy problem as an "Amendment request" in its working file and names it in its summary. When one comes back:
    - stop the pipeline there;
    - show the user the request, with the agent's reason;
    - offer `/initiate-strategy <Module> amend`, or the user's own decision (keep the entry as it is, and say how the agent should proceed).

    Resume only once the entry is approved again, or the user has decided.
- **After research:** read the dossier's §1 and §12.
    - If there are **BLOCKING** questions, or decisions only the user can make, ask the user (AskUserQuestion), then pass their answers to the author as notes, or re-run the researcher if new research is needed.
    - If the researcher proposes new sources, ask the user. If they approve, add each source to `00.Learn/references/references.md` and its host to `.claude/settings.json`: you do this, not the agents (CLAUDE.md, "Sources").
- **After authoring:**
    - Check that the post, the answers page and `design.md` exist.
    - Run `.github/scripts/check-lists.py` and `.github/scripts/readability.py --check --budget <N> <post>`.
    - Read the author's list of deviations and open issues.
    - If the author stopped after the design because of research gaps, go back to the research stage with those gaps as notes.
- **After the audit:** go straight to §5 and resolve the findings yourself.

## 5. Resolving the audit (you, after every audit)

The auditor proposes; you decide. Work through `audit.md`'s findings one by one, most severe first:

1. **Verify the finding yourself.** Don't take it on trust.
    - For a fact, re-check it in the pinned code (`.github/scripts/pinned.py path`, `git show <sha>:<path>`, `git grep`, read) or at the cited source.
    - For a comprehension problem, re-read the passage as the learner would, with only basic Linux and the earlier articles behind them.
    - For a standard, check CLAUDE.md and the project memory.
    - For scope, check the strategy entry.
2. **Decide**, with the project's pedagogic goal as the test: does the change help a beginner understand, is it correct, and does it stay within the entry's scope?
    - **Apply** it as proposed.
    - **Adapt** it: the problem is real, but a better fix exists (simpler words, a better place, a clearer example, a cut instead of an addition).
    - **Reject** it: the problem isn't real, the fix would hurt clarity or accuracy, it would push the article past its scope or budget, or it conflicts with the user's instructions or the design's intent for a good reason.
    - **Ask the user**: anything only they can decide (scope, contradicting their wishes). Use AskUserQuestion, and batch the questions. A real scope problem is an amendment request (§4).
3. **Add your own changes** where the audit missed something. You read the post too; if something is wrong, unclear or a detail the reader doesn't need, fix it.
4. **Make the changes** with the Edit tool, keeping every standard:
    - excerpts pasted from `pinned.py excerpt`, in the body only where they teach, otherwise in the answers page's Evidence section;
    - links with `@cloudstack@`, then `pinned.py fill`;
    - lists rendering as lists;
    - bold only for a defined term at its definition;
    - promises kept;
    - linking posts updated if a heading anchor changes;
    - British spelling.

    Any fact you add needs its evidence on the answers page (or in the body, if it teaches there), or in the dossier.
5. **Hand big rewrites to the author.** If accepted findings add up to rewriting whole sections, or redesigning the post, launch the author with mode `revise`, and list in its prompt the finding IDs to address and how you decided each. Then audit again (§3, the auditor), and resolve that audit the same way. Do at most one such round, then report to the user rather than looping.
6. **Record every decision** in the *Resolution* section of the latest dated entry in `audit.md`:

    ```markdown
    ### Resolution (<YYYY-MM-DD>, main session)
    | Finding | Decision | Note |
    |---|---|---|
    | A1 | applied | |
    | A2 | adapted | explained "secret key" in the first sentence instead of adding a new paragraph |
    | A3 | rejected | the term is explained in the opening, two lines earlier |
    | A4 | asked the user | scope: whether this belongs to a later article |
    **Added by the main session:** <any extra changes, with the reason>
    ```

The guard hook doesn't bind the main session, so the care is yours. Change only what the resolution covers.

## 6. Final verification (always, after the last stage run)

Run these yourself, from the repository root, and read the output:

```sh
.github/scripts/pinned.py fill <post> <answers page>          # nothing left to fill
.github/scripts/check-excerpts.py                             # every post; offline
.github/scripts/check-lists.py
.github/scripts/check-diagrams.sh
.github/scripts/check-diagram-styles.py <the post's diagrams, if any>
.github/scripts/build-site.sh <scratchpad>/site               # strict build + the references/ guard
.github/scripts/check-lists.py --site <scratchpad>/site
.github/scripts/check-urls.sh <post> <answers page>
.github/scripts/readability.py --check --budget <entry's budget> <post>
.github/scripts/reading-time.py --check --max 30 <post>       # header right, and 30 minutes at most
grep -rl 'STUB:' 00.Learn --exclude-dir=references          # the target must not be listed
```

Also:

- check the reading time against the entry's target, and the defined terms against its scope in;
- look at the post's diagrams (Read the PNGs);
- read the post's opening and "In short" yourself, as the learner.

Report any failure honestly. Don't paper over one.

## 7. Report to the user

Keep it short, and include:

- **What was produced:**
    - the paths,
    - the post's title,
    - its section outline (headings only),
    - its reading time against the entry's target, and its defined terms against the budget.
- **Research:** how many findings; the few insights that shaped the post; anything the code showed that contradicts the docs.
- **Audit and resolution:** the verdict; the number of findings by severity; how many you applied, adapted and rejected, and how many changes you added (naming the important ones, with a reason for each important rejection); and what's left open or waiting for the user (blockers and amendment requests first).
- **Checks:** each one's result.
- **Preview:** the post is on the local server at `http://localhost:8000/<path>/` if `.github/local/serve.sh` is running (it rebuilds on save).
- **Git:** nothing is committed. Offer to commit on `learn` and push to `origin`.

Then **stop**. Don't start the next post: the user reviews each one first.

## 8. Rules that always apply

- No stage runs without an approved strategy entry; only the strategy splits topics.
- Never commit or push unless the user asks.
- Never install software on the host, and never build CloudStack.
- Never loosen the agents' permissions without the user.
- Posts never link into `references/`.
- `learn` never gets CloudStack code changes, nor changes to any upstream file: only `00.Learn/`, `CLAUDE.md`, `.claude/`, `mkdocs.yml` and the course's own files in `.github/`.
