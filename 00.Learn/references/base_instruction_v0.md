# Base instruction v0

The founding instruction for this project, recorded verbatim on 2026-10-01 (typos included).

---

/root/projects/openstack/openstack/CLAUDE.md

/root/projects/openstack/openstack/00.Learn

/root/projects/openstack/openstack/.claude

Please refer to the files & directories in the above project folders for OpenStack and replicate exactly the same structure (of course adapted for this project). The goal is exactly the same, pedagogical - to enable learning of CLoudStack from stratch for beginners and enable them step by step to become super-advance. Please update the repo with necessary strucutres, for now the publishing will be just through the localhost server, which can be gitignored. Please let me know in case of any questions

---

## The answers given when the project was set up (2026-10-01)

Asked before the structure was built, and answered by the user:

| Question | Answer |
|---|---|
| Keep the OpenStack blog's per-post access control, with publishing on localhost only? | Drop it for now. Every post is visible on the local server; access control can be added later without changing any post |
| Which comparison callouts? | Kubernetes lens **and** OpenStack lens, both optional |
| How to set up the branches? | A `learn` branch for all course work, and an `upstream` remote for apache/cloudstack; `main` stays an untouched mirror |
| Which running metaphor? | The hotel from the OpenStack course, CloudStack edition: one head office instead of many departments |

## Inherited goal: the OpenStack project's base instruction

The instruction above says the goal is "exactly the same" as the OpenStack project's. That project's founding instruction is quoted here verbatim, so its rules (three kinds of material, the five writing rules, sources whitelisted per project) can be read in full. Where it names OpenStack, read CloudStack; where it names OpenStack's docs, blog or repository, this project's own list in `references.md` applies.

> The goal of this project is purely pedagogical, i.e., to understand Openstack as best as possible from ground up with the code being the source of truth. We will NEVER change any code in the learn branch. What we may do however is to update the branch as and when new chnages are pushed to https://opendev.org/openstack/openstack. There are lot of materials out there in the internet on OpenStack that dumps the some code of openstack from installation to intergrating/bringing up various services without ever answering the question why, or how something could be done differently or what is purpose of doing something, etc. This project would like to address that from ground up, so that any beginner can actually understand the basics, the core architecture design, how each modules are designed, how they fit with each other, what are the pre-requiste services in OpenStack and can learn the tool. I would also like to eventually design tasks and sub-task to test the understanding of the student. 
> We will be producing three kinds of items - 
> 1. Overall big picture of the architecture (of a module or general) in great depth addressing especially the why questions.
> 2. Deep dives into specific part of the architecture on demand
> 3. Questions and Exercises for students to work on.
>
> Each of this will be placed inside a new folder called 00.Learn. We will be creating sub-folders within 00.Learn for specific modules and/or general architecture. As the ultimate goal is to help a beginner grow in journey in understanding OpenStack, we must always
> 1. think from the students standpoint.
> 2. Label the material as Beginner, Intermediate, Advanced
> 3. Irrespective of the level, always use as simple and intuitive language as possible 
> 4. Use methapors, analogies to make the Ideas as clear as possible
> 5. Refer to the achitectural design of Kubernetes as simpler references to complex OpenStack ideas (as a students might be more familiar with Kubernetes than OpenStack)
>
> Finally, you may refer the Official Docs and other blogs as mentioned below to create the pedagogical materials as discussed earlier
> -  https://docs.openstack.org/2026.1/
> as well as blogs (more which will be added as we move forward)
>  - https://openstackblog.com/
>
> Please create a folder under 00.Learn called "references" and then create a .md file with all the references. These references must be whitelisted for you to do web-search / web-fetch on as you see fit. So please update the settings.json in ~/.claude/ , i.e., just for the scope of this current project.
> Also create another .md doc in the "references" folder called base_instruction_v0, and keep this whole instruction verbatim for future reference. Also update you memory as well Cluade.md files to reflect the goal of this project as mentioned here.
