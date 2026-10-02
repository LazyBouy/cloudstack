# In-progress checks

Internal tracking of links that point at posts not written yet, so none of them fall through the cracks. Like everything in `references/`, this file is not published on the blog.

## The rule

Whenever a post refers to another post, it **links** to it. It never just says "post 05 covers this" in plain text.

If the target post doesn't exist yet:

1. **Link to its placeholder page ("stub")**, which sits at the post's final path (for example `01.General/05.Foundation-Services.md`). The link works today and keeps working once the real post replaces the stub under the same file name. Create the stub if it doesn't exist yet; every stub contains the marker `STUB:` in an HTML comment.
2. **Add a row to the table below** saying where the link is and what the linking text promises the target will contain.

## When a stub becomes a real post

1. Replace the stub with the post, keeping the same file name.
2. Go through every row for that stub:
   - Make sure the post keeps each promise.
   - Where a promise is about one particular section, point the link at that section's anchor (for example `06.Control-Plane-Building-Blocks.md#signing-a-request`).
   - Remove *(coming soon)* from the linking text.
3. Delete the rows, and run `mkdocs build --strict` to confirm every link and anchor resolves.

List the stubs still waiting to be written:

```sh
grep -rl 'STUB:' 00.Learn --include='*.md' --exclude-dir=references
```

## Pending

Paths are relative to `00.Learn/01.General/`.

Module 01's reading order (`README.md`) links to every post, and its rows are updated as each post is written, so it has no rows here. Every other link from a written page to a stub has a row below.

| Stub (target) | Linked from | What the link promises / what to fix |
|---|---|---|
| `03.Inside-The-Management-Server.md` | `01.Overview.md`, section "So what is CloudStack?" ("answers it") | Answers **why CloudStack builds a whole cloud as one program** instead of separate services (OpenStack-style), with what that design gains and costs. Point the link at that section's anchor. Remove *(coming soon)* |
| `03.Inside-The-Management-Server.md` | `01.Overview.md`, section "One head office decides everything" ("opens their doors") | Shows the sections inside the one program: the front desk (API), the guest registry (accounts), the work-order board (async jobs) and the managers who decide and instruct (orchestration), as modules of one program, not separate services. Remove *(coming soon)* |
| `03.Inside-The-Management-Server.md` | `02.Architecture/02.Who-Calls-Whom.md`, section "Growing: more head offices" ("How they share the work") | How several management servers share one ledger and the floors: each host's line is held by one of them at a time, and work for a host is passed to the management server that holds its line (they talk on ports 8250 and 9090). Point the link at that part's anchor. Remove *(coming soon)* |
| `03.Inside-The-Management-Server.md` | `02.Architecture/02.Who-Calls-Whom.md`, "Next up" | Why CloudStack builds the whole cloud as one program, and the sections inside it, **including the one that keeps every attendant's line** (the agent manager). Remove *(coming soon)* |
| `03.Inside-The-Management-Server.md` | `02.Architecture/README.md`, "The two parts" ("after them, Inside the Management Server") | General link to the post, as the series' next stop. Remove *(coming soon)* |
| `04.How-It-Unfolds.md` | `01.Overview.md`, section "Why your users pick a hotel site, never a floor" ("Who picks the host, and how") | Explains **who picks the host for a new VM, and how** (the deployment planner). Point the link at that section's anchor. Remove *(coming soon)* |
| `04.How-It-Unfolds.md` | `01.Overview.md`, section "A ticket, not a wait" ("follows it step by step") | Follows one `deployVirtualMachine` request step by step: the async job and the chain of decisions and instructions down to the floor attendant (agent). Point the link at that part's anchor. Remove *(coming soon)* |
| `04.How-It-Unfolds.md` | `02.Architecture/01.Where-Everything-Lives.md`, section "Zones: the sites your users choose" ("Who picks the floor within a site") | Same promise as post 01's: who picks the host for a new VM, and how (the deployment planner). Point the link at that section's anchor. Remove *(coming soon)* |
| `04.How-It-Unfolds.md` | `02.Architecture/02.Who-Calls-Whom.md`, section "The attendant phones in" ("tells it as a story: a whole cloud waking up") | The start-up in time order, as a story: a cloud waking up, with the hosts' agents phoning in on port 8250 (post 02's part 2 gives only the anatomy of the line). Point the link at that part's anchor. Remove *(coming soon)* |
| `04.How-It-Unfolds.md` | `02.Architecture/02.Who-Calls-Whom.md`, section "What a staff room needs before it opens" ("tells this chain in time order") | The system VMs starting once a host is Up, primary storage exists and the system VM template is ready in secondary storage, told in time order. Point the link at that part's anchor. Remove *(coming soon)* |
| `../04.How-It-Unfolds.md` | `08.Check-Yourself-Answers/01.Overview.md`, answer 4 ("Who picks the host, and how") | Same promise as the "Why your users pick a hotel site" row: who picks the host, and how. Point the link at that section's anchor. Remove *(coming soon)* |
| `05.Foundation-Services.md` | `01.Overview.md`, section "The magic trick: virtualization" ("explains all three") | Explains **KVM, QEMU and libvirt**, all three. Point the link at that section's anchor. Remove *(coming soon)* |
| `05.Foundation-Services.md` | `01.Overview.md`, section 'Behind the "staff only" door' ("covers each") | Covers the **ledger (database) and the synchronized clocks (NTP)**: why each is needed and what could replace it, with **MySQL and MariaDB side by side** (config lines). Remove *(coming soon)* |
| `05.Foundation-Services.md` | `02.Architecture/01.Where-Everything-Lives.md`, section "The head office's machine" ("MySQL next to MariaDB is for") | Same promise as post 01's: **MySQL and MariaDB side by side**. Remove *(coming soon)* |
| `05.Foundation-Services.md` | `02.Architecture/01.Where-Everything-Lives.md`, section "Secondary storage: one warehouse per site" ("Why NFS, and what else could serve") | **Why NFS** serves secondary storage (and, in the lab, primary storage), and **what else could** do the job. Point the link at that section's anchor. Remove *(coming soon)* |
| `06.Control-Plane-Building-Blocks.md` | `01.Overview.md`, section "Guests only ever talk to the front desk" (key cards: "shows how") | Shows **how a program signs a request with its API key and secret key**. Point the link at that section's anchor. Remove *(coming soon)* |
| `06.Control-Plane-Building-Blocks.md` | `01.Overview.md`, section "Checking in" ("The same request, three ways": "The `signature` is computed from the secret key; … shows how") | Same promise: how the `signature` parameter of a raw API request is computed from the secret key. Remove *(coming soon)* |
| `06.Control-Plane-Building-Blocks.md` | `02.Architecture/02.Who-Calls-Whom.md`, section "Instructions come back on the same call" ("How commands and answers are packed and matched") | The **commands and answers on the agent's line**: how they're packed (serialized), sent and matched to each other. Point the link at that section's anchor. Remove *(coming soon)* |
| `07.Core-Subsystems.md` | `01.Overview.md`, section "So what is CloudStack?" ("compares them") | **Compares the hypervisors** CloudStack can drive (KVM, XenServer/XCP-ng, VMware). Point the link at that section's anchor. Remove *(coming soon)* |
| `07.Core-Subsystems.md` | `02.Architecture/01.Where-Everything-Lives.md`, section "Zones: the sites your users choose" ("compares the two") | **Compares basic and advanced zones.** Point the link at that section's anchor. Remove *(coming soon)* |
| `07.Core-Subsystems.md` | `02.Architecture/01.Where-Everything-Lives.md`, section "The wiring: five kinds of traffic" ("this can wait for") | Sorts out the **"storage" traffic type**: the Concepts page says it carries only secondary-storage traffic, Network Setup says primary-storage traffic uses it too. Point the link at that part's anchor. Remove *(coming soon)* |
| `07.Core-Subsystems.md` | `02.Architecture/02.Who-Calls-Whom.md`, section "Floors without an attendant: VMware and XenServer" ("compares the hypervisors") | Same promise as post 01's: **compares the hypervisors** (KVM, XenServer/XCP-ng, VMware). Remove *(coming soon)* |
| `07.Core-Subsystems.md` | `02.Architecture/02.Who-Calls-Whom.md`, section "The switchboard, reached through the intercom" ("goes deeper") | **The virtual router in depth.** Point the link at that section's anchor. Remove *(coming soon)* |
| `11.Install-By-Hand/README.md` | `01.Overview.md`, section "The magic trick: virtualization" ("the install posts say how to switch it on") | Say **how to switch on nested virtualization** for the lab's KVM host VM. Point the link at the part that does. Remove *(coming soon)* |
| `11.Install-By-Hand/README.md` | `01.Overview.md`, section "Who sets the rules" ("the lab you'll build … you're both operator and user") | The lab where the reader is both operator (root admin) and user. Post 01 also says the lab runs **one management server** and uses **KVM**. Remove *(coming soon)* |
| `11.Install-By-Hand/README.md` | `02.Architecture/01.Where-Everything-Lives.md`, section "Two machines: a head office and a floor" ("The lab we'll build") | The **two-machine lab**: one machine for the management server with its MySQL database and NFS storage (both primary and secondary, NFS), one KVM host; one management server, no separate storage network. Part 1's `02-lab` picture shows what's installed on each machine, and part 2's `02-machines` picture draws every connection between them, labelled "the lab we'll build". Remove *(coming soon)* |
| `11.Install-By-Hand/README.md` | `02.Architecture/README.md`, "The big picture" ("the install posts") | Same promise: the two-machine lab, one machine for the head office and its ledger, and one KVM host. Remove *(coming soon)* |
| `11.Install-By-Hand/README.md` | `02.Architecture/01.Where-Everything-Lives.md`, section "The wiring: five kinds of traffic" ("your lab's layout is for the install posts to settle") | Settles the lab's **bridge layout** on the KVM host, and explains both layouts post 02 now only names (its comparison table was cut for length): one bridge, `cloudbr0`, as in the QIG ("something your would NEVER do in a production"), or two, `cloudbr0` for management and `cloudbr1` for public and guest, as in the KVM guide. Point the link at the part that does. Remove *(coming soon)* |
