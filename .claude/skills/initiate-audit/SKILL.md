---
name: initiate-audit
description: "Audit stage only, for one drafted post of the CloudStack course in 00.Learn/: launches the auditor agent, which reads the post as proofreader, then editor (including scope adherence against the post's strategy entry), then a first-time learner, and writes detailed findings with proposed changes (audit.md) without touching the post. You then verify every finding, apply, adapt or reject it, add your own fixes, and record each decision. Use when the user asks to audit, review, proofread or edit a post, e.g. '/initiate-audit 01.General/03'."
argument-hint: "<post, e.g. 03 or 01.General/03.Some-Topic> [notes for the auditor]"
allowed-tools: Agent, Read, Glob, Grep, AskUserQuestion, Bash(.github/scripts/*), Bash(git status *), Bash(git diff *), Bash(git merge-base *), Bash(git show *), Bash(git cat-file *), Bash(git branch --show-current)
---

# Initiate an audit for an article

Arguments: `$ARGUMENTS`

First read `.claude/skills/initiate-article/PIPELINE.md` in full: it's the procedure. Then:

1. **Resolve** the target, its strategy entry and the working folder (PIPELINE §1). If the entry isn't approved, stop and offer `/initiate-strategy <Module>`: the audit checks the article against its entry.
2. **Check the preconditions** (PIPELINE §2). The post must be drafted (no `STUB:` marker).
   - For a post written outside the pipeline, there's no `research.md`. Tell the auditor so: it must verify facts directly against the pinned code, and still write `audit.md`. Its working folder is created on first use.
3. **Launch** the `auditor` (PIPELINE §3, mode `audit`) with the user's notes. It writes findings only; it can't edit the post.
4. **Resolve the audit yourself** (PIPELINE §5):
   - verify every finding against the code, the dossier, the strategy entry and the learner's point of view,
   - apply, adapt or reject each one, and add your own fixes,
   - record every decision in `audit.md`'s *Resolution* section,
   - ask the user about anything only they can decide, amendment requests included.

   If the accepted findings amount to rewriting whole sections, and the post came through the pipeline (it has a `design.md`), offer `/initiate-authoring <target> revise` instead of rewriting it yourself.
5. **Verify** (PIPELINE §6) and **report** (PIPELINE §7):
   - the verdict and the number of findings by severity,
   - how many you applied, adapted and rejected, and what you added, naming the important ones and why,
   - what's left open,
   - the check results.

Nothing is committed.
