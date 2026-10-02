# The course strategy

This folder is the course's blueprint. Nothing is researched or written until it's planned here and the user has approved the plan.

| File | What it decides | Written by |
|---|---|---|
| `course.md` | The module map, the running analogy (chosen by the user from the strategist's candidates), the voice and the template | the `strategist` agent, via `/initiate-strategy course` |
| `<Module>.md` (for example `01.General.md`) | One module's learning plan: the learner's outcomes, the concept ledger, and the learning path, one entry per article with its scope, budget and target length | the `strategist` agent, via `/initiate-strategy <Module>` |

- The strategist proposes (`Status: proposed`). Only the user approves; the main session records it (`Status: approved <date>`) and then builds what the approval unlocks: the home page's module list, or a module's skeleton (README, `.nav.yml`, one stub per article).
- Each article's approved entry is the binding brief for the researcher, the author and the auditor. A problem with it is raised as an amendment request and settled with `/initiate-strategy <Module> amend`.
- These files are committed with the course, but they're under `references/`, so they're not on the site, and posts never link here.

CLAUDE.md ("How the course is planned: strategy first") and `.claude/agents/strategist.md` describe the process in full.
