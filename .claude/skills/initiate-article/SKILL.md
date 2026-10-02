---
name: initiate-article
description: "Run the full pipeline for one post of the CloudStack course in 00.Learn/ that has an approved strategy entry: research (researcher agent), then design and draft (author agent), then a three-pass audit (auditor agent, findings only), then your verification and application of the findings, then a final verification and a report, pausing for the user afterwards. Use when the user asks to write, create or produce a post or article end to end, e.g. '/initiate-article 01.General/03'. Without an approved entry it stops and offers /initiate-strategy."
argument-hint: "<post, e.g. 03 or 01.General/03.Some-Topic> [notes] [pause-after-research] [pause-after-design]"
allowed-tools: Agent, Read, Glob, Grep, AskUserQuestion, Bash(.github/scripts/*), Bash(git status *), Bash(git diff *), Bash(git merge-base *), Bash(git show *), Bash(git cat-file *), Bash(git branch --show-current)
---

# Initiate an article: research → authoring → audit

Arguments: `$ARGUMENTS`

First read `.claude/skills/initiate-article/PIPELINE.md` in full: it's the procedure. Then:

1. **Resolve** the target, its strategy entry, the working folder and the flags (PIPELINE §1). **If the entry isn't approved, stop** and offer `/initiate-strategy <Module>` (or `amend`): no stage runs without an approved brief. Tell the user in one line what will run.
2. **Research.** Check the preconditions (PIPELINE §2), then launch the `researcher` (PIPELINE §3, mode `research`). When it returns, do PIPELINE §4 "After research". If the flags include `pause-after-research`, report the dossier's highlights and stop here. An amendment request from any stage stops the pipeline until the user decides (PIPELINE §4).
3. **Authoring.** Launch the `author` with mode `design+draft`. The exception is `pause-after-design`: then use mode `design-only`, show the user the design's outline, learning objectives and diagram plan, and stop. When the author returns, do PIPELINE §4 "After authoring".
4. **Audit.** Launch the `auditor` (mode `audit`). It writes findings to `audit.md` and never edits the post.
5. **Resolve the audit** (PIPELINE §5):
   - verify every finding yourself,
   - apply, adapt or reject it, with the pedagogic goal as the test,
   - add your own fixes,
   - record each decision in `audit.md`.

   Big rewrites go back to the author (mode `revise`), followed by one more audit, at most once.
6. **Verify** (PIPELINE §6) and **report** (PIPELINE §7). Then stop: don't start another post.

Run the stages one at a time, in the foreground: each needs the previous one's output. One article per run: only the strategy splits topics. Never skip the audit, its resolution or the final verification, even if the draft looks fine.
