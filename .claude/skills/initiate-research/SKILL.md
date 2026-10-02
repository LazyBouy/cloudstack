---
name: initiate-research
description: "Research stage only, for one post of the CloudStack course in 00.Learn/: launches the researcher agent, which writes (or updates) a verified dossier, research.md, for the article's in-scope concepts (its approved strategy entry), from the pinned CloudStack code and approved sources. Use when the user asks to research a post or article, e.g. '/initiate-research 01.General/03'."
argument-hint: "<post, e.g. 03 or 01.General/03.Some-Topic> [notes for the researcher]"
allowed-tools: Agent, Read, Glob, Grep, AskUserQuestion, Bash(.github/scripts/*), Bash(git status *), Bash(git diff *), Bash(git merge-base *), Bash(git show *), Bash(git cat-file *), Bash(git branch --show-current)
---

# Initiate research for an article

Arguments: `$ARGUMENTS`

First read `.claude/skills/initiate-article/PIPELINE.md` in full: it's the procedure. Then:

1. **Resolve** the target, its strategy entry and the working folder (PIPELINE §1). If the entry isn't approved, stop and offer `/initiate-strategy <Module>`. Tell the user in one line what will run.
2. **Launch** the `researcher` (PIPELINE §3, mode `research`). If `research.md` already exists, the researcher updates it, so say so in the prompt.
3. **After research** (PIPELINE §4): handle BLOCKING questions, amendment requests and proposed new sources with the user.
4. **Report**, briefly:
   - the dossier's path, the number of findings, and the insights that should shape the post,
   - any docs-vs-code disagreements,
   - open questions,
   - the next step: `/initiate-authoring <target>` (or `/initiate-article` to run everything).

Don't start authoring unless the user asks. Nothing is committed.
