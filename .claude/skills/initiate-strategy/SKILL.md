---
name: initiate-strategy
description: "Plan the CloudStack course before anything is researched or written: launches the strategist agent, which proposes either the course strategy (module map, 2–3 running-analogy candidates mapped and stress-tested) or one module's learning plan (concept ledger and a path of tightly scoped articles). You present it, the user decides, you record the approval, and for a module you build its skeleton (README, .nav.yml, stubs). Use when the user asks to plan, strategise or restructure the course or a module, or to amend a plan, e.g. '/initiate-strategy course', '/initiate-strategy 01.General', '/initiate-strategy 01.General amend'."
argument-hint: "<course | module, e.g. 01.General or 02.Management-Server> [amend] [notes]"
allowed-tools: Agent, Read, Glob, Grep, Edit, Write, AskUserQuestion, Bash(.github/scripts/*), Bash(git status *), Bash(git diff *), Bash(git show *), Bash(git branch --show-current)
---

# Initiate a strategy: plan before research

Arguments: `$ARGUMENTS`

The strategist proposes; the user decides; you record and build. Strategy documents live in `00.Learn/references/strategy/`. They're committed with the course (they're its blueprint), but they're not on the site.

## 1. Resolve the scope

The first word is the scope; `amend` among the rest is a flag; everything else is the user's notes, passed verbatim.

- `course` → `00.Learn/references/strategy/course.md`.
- A module, `01`, `01.General` or `02.Management-Server` → `00.Learn/references/strategy/<Module>.md`. Take the module's full name from the module map in `course.md`.
    - **Precondition:** `course.md` exists and its status is `approved`. If not, stop and offer `/initiate-strategy course`.
    - The module's number and name must match the map. If the user wants a module the map doesn't have, it's a course amendment first.
- `amend` → the strategy file must exist. Collect the open amendment requests:
    - from the user's notes;
    - from the working files: `grep -rn -A6 -i "amendment request" 00.Learn/references/articles/<Module>/` (for `course`, every module);
    - from the plan's own §6 rows with no decision.

    Pass every request to the strategist, quoted, with where it came from.

Tell the user in one line what will run. Check `git branch --show-current` is `learn`.

## 2. Launch the strategist

Use the Agent tool with `subagent_type: strategist` and `run_in_background: false`, with this prompt, filled in:

```text
Scope: course | <Module>
Mode: new | amend
Strategy file: 00.Learn/references/strategy/<course | Module>.md
Amendment requests: <each, quoted, with its source; or "none">
User's notes: <verbatim, or "none">
Follow your agent instructions in full, and return the summary they ask for.
```

If it reports a guard block it genuinely needs, don't loosen the permissions: tell the user and let them decide.

## 3. Check the plan yourself

Read the whole strategy file. The strategist proposes; you check before the user spends time on it.

- **Course:**
    - 2–3 genuinely different analogy candidates, each with its mapping, stress test, breaks, vocabulary cost and risks;
    - a module map with a question per module;
    - nothing borrowed from the OpenStack course's structure.
- **Module:**
    - every article has one question, one idea, at most about 3–5 new concepts, a target of 10–20 minutes, and a budget;
    - every ledger concept has its "taught in", and the order check holds (no concept used before it's taught);
    - each chain goes problem before options;
    - the analogy is the approved one.
- **Evidence:** spot-check three to five of its evidence pointers against the code (`git show <sha>:<path>`, `git grep`) or the source. Check claims about counts and scope especially.

Small slips (a missing pointer, a typo) you may fix yourself; say so in the changelog. Anything bigger goes back to the strategist once, with your notes, in mode `amend`.

## 4. Present it and ask the user

Give the user a short summary, and the path to the file as a link, so they can read it in full.

- **Course:**
    - the module map, one line per module;
    - the analogy candidates side by side: each one's picture in a sentence, its best fit, its worst break, its vocabulary cost;
    - the recommendation.

    Ask with AskUserQuestion, in one call: which analogy (each candidate an option, the recommended one first and marked; give each a `preview` with its mapping table), and whether the module map is right (approve, or adjust).
- **Module:**
    - the learner's outcomes;
    - the article list: `NN.Slug`, title, the one idea, target minutes.

    Ask with AskUserQuestion: approve the whole list, or approve it with changes (the user says which), or send it back to the strategist with notes.

## 5. Record the decision

- **Changes requested:** relaunch the strategist in mode `amend` with the user's words, then repeat §3 and §4.
- **Approved:**
    - set the file's `Status:` to `approved <YYYY-MM-DD>`, and each approved article entry's `Status:` too;
    - for `course`, mark the chosen candidate "**Chosen**", and the others "Not chosen", with the user's reason if they gave one;
    - add a changelog line: "<YYYY-MM-DD>: approved by the user: <what, and any wording they used>".

## 6. Build what the approval unlocks

- **Course approved:** update the home page, `00.Learn/README.md`: its module table lists every module of the map, with the question it answers, each *(coming soon)* until its first article is written. If the voice or template changed, update `CLAUDE.md`'s "Writing rules" to match.
- **Module approved:** create the module's skeleton from the plan:
    - `00.Learn/<Module>/README.md`: what the module is for, in two or three plain sentences; the learner's outcomes; and the reading order, a table of every article with its title (a link to the stub), level and target minutes, each *(coming soon)*. Remove the module README's own `STUB:` marker if it has one.
    - `00.Learn/<Module>/.nav.yml`: `title: "NN · Title"` (no *(coming soon)* once the module has a plan).
    - One stub per article, `00.Learn/<Module>/NN.Slug.md`: the title with *(coming soon)*; the comment `<!-- STUB: placeholder so links work. The brief is the entry "NN.Slug" in 00.Learn/references/strategy/<Module>.md. -->`; a `> [!NOTE]` saying the post isn't written yet; and one or two plain sentences, in the learner's words, on the question it will answer. No technical detail the learner can't read yet.
    - `00.Learn/<Module>/99.Check-Yourself-Answers/README.md`: one short paragraph ("Every article in this module ends with a few questions…"), and the sentence "No answers yet: the first appear with the first article." Plus its `.nav.yml`: `title: "Check-yourself answers"`.
    - The home page's row for the module: link it, keep *(coming soon)*.
- **Module amended:** add, rename or remove stubs to match, never renumbering a written article, and fix every link and `in_progress_checks.md` row that pointed at a changed stub.

Stubs never link into `references/`. The strategy file is named only inside the HTML comment, which isn't rendered.

## 7. Verify and report

Run:

```sh
.github/scripts/build-site.sh <scratchpad>/site
.github/scripts/check-lists.py --site <scratchpad>/site
.github/scripts/check-lists.py
```

Report in a few lines: what was decided, the files written or changed, the check results, and the next step: for `course`, `/initiate-strategy 01.General`; for a module, `/initiate-article <Module>/01`. Nothing is committed: offer to commit on `learn`.

Then stop. Plans and articles go one at a time, each reviewed by the user.
