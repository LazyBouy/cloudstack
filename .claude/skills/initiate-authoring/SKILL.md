---
name: initiate-authoring
description: "Authoring stage only, for one post of the CloudStack course in 00.Learn/: launches the author agent, which restates the approved strategy entry and designs the post from the learner's point of view (design.md) and then drafts the post, its answers page with its Evidence section, diagrams and cross-link bookkeeping from the research dossier. Modes design-only, draft-only and revise (a rewrite after an audit, driven by the findings you accepted). Use when the user asks to write, design or draft a post whose research is done, e.g. '/initiate-authoring 01.General/03'."
argument-hint: "<post, e.g. 03 or 01.General/03.Some-Topic> [design-only | draft-only | revise] [notes for the author]"
allowed-tools: Agent, Read, Glob, Grep, AskUserQuestion, Bash(.github/scripts/*), Bash(git status *), Bash(git diff *), Bash(git merge-base *), Bash(git show *), Bash(git cat-file *), Bash(git branch --show-current)
---

# Initiate authoring for an article

Arguments: `$ARGUMENTS`

First read `.claude/skills/initiate-article/PIPELINE.md` in full: it's the procedure. Then:

1. **Resolve** the target, its strategy entry, the working folder and the mode (PIPELINE §1). If the entry isn't approved, stop and offer `/initiate-strategy <Module>`. With no mode flag, the mode is `design+draft`.
2. **Check the preconditions** for that mode (PIPELINE §2). If `research.md` is missing, offer `/initiate-research` instead; never let the author write without a dossier.
3. **Launch** the `author` (PIPELINE §3) with the mode and the user's notes. For `revise`, list the audit findings to address (by ID) and your decision on each, from `audit.md`'s *Resolution* section.
4. **After authoring** (PIPELINE §4). In `design-only` mode, instead show the user the design's brief, learning objectives, outline and picture plan, and stop so they can review it. Bring any amendment request to the user (PIPELINE §4).
5. **Run a quick verification.** The same checks as PIPELINE §6, minus the external-URL check if time is short. **Report** what was written, the check results, and the author's open issues.

Then suggest `/initiate-audit <target>`: every draft must be audited before it's considered done. Nothing is committed.
