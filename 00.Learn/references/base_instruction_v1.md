# Base instruction v1

The user's new direction for the course, recorded verbatim on 2026-10-01 (typos included). It follows the first attempt at module 01 (archived in `archive/v1/`), and supersedes these parts of [v0](base_instruction_v0.md)'s set-up answers: **the hotel metaphor**, **replicating the OpenStack course's structure**, and (from the feedback of the same day) **the operator voice**. v0's goal stands: a purely pedagogical course, with the code as the source of truth.

---

## The direction

> These articles are really not good quality. The articles should be written from the readers perspective. This does not clarify the architecture rather confuses the readers more. If you need to break it in more granualr chunk to make the dense architecture accessible please do so. The two part break was arbitrary in my view. There can be multiple break if required. Let's enter plan mode to figure the chunks out. Something that worked for OpenStack need not work for Cloudstack, that project was just an example not a replication template

> We need to create a article strategy that fits the CloudStack project specifically and cannot use Openstack writeup as template. The Hotel analogy may not be the right one for CloudStack. We need to think of the a different analogy. It seems to me we are trying to fit the OpenStack model to CloudStack. That is not the goal. Let's archive the Overview and Architecture articles written so far and enter plan mode to structure the writing. May be it would be a good idea to create Strategy Agent before the researcher that can strategize the way a topic (here first 00.General CloudStack Overview, then may be 01.ManageServer DeepDives ect.) into group of article header that maxmizes understanding and learning the CloudStack Application. Also the writing has to be humanized, with a better readbility and more intuitive and simpler flow with precision, and well defined scope. For that if we need break certain topics let's do that. Details are important only if used properly else it becomes a burden the reader carries (hence eventually leaves) throughout the articles

> Keep the module numbering

> i.e., 01.General; 02.Management Server

## The answers given in plan mode

| Question | Answer |
|---|---|
| What replaces the hotel analogy? | The strategist proposes 2–3 CloudStack-specific central analogies, mapped and stress-tested; the user picks one |
| Who is "you" in the articles? | The learner: a reader with basic Linux learning CloudStack step by step. Operators and cloud users are roles, described in the third person when they matter |
| How are modules numbered? | As before: `01.General`, then `02.Management-Server`, … (the user's correction of the option first chosen) |
| Where do the archived articles go? | In the repository, off the site: `00.Learn/references/archive/v1/` |

## Earlier feedback the same day, which this direction builds on

> the Cloudstack posts feel very dry with flow getting bogged down by minute details. The details are important, but putting it before giving the big picture idea defeats the pedagogical purpose of the project. Also the posts are written from two different perspective which switches in a confusing way. Let's build the posts from the 'operator' perspective and name the user perspective explicitly if something needs to be shared from that perspective. Let keep each posts 30 mins read max, and split it into meaningful topics if you think it exceeds based on current topic selection. However if broken finish both the subtopic in a single cycle, i.e., author and auditor

> "A cluster runs exactly one hypervisor." - a sentence like this is not only confusing but down right wrong. It makes no sense to claim that cluster which is ultimately a set of hosts (physical machine) runs one hypervisor. This is absurd as each physical machine has its own Os and its own hypervisor. What the documentation and the code mean is same "type" of Hypervisor. Please make sure sure basic mistakes should not be there in the writing. The articles' first draft should be factually correct

> This part is so confusing.... Why single storage, how VMs can have private storage? Why VMs always need to share storages? What are these Storage hosts etc. are totally unexplaind and dumped on the reader

(The operator-voice rule and the "series in one cycle" rule in the first of these were superseded by the direction above: the learner voice, and splits decided by the strategy, articles one at a time.)
