# Architecture: One Head Office, Many Floors

How a CloudStack cloud is put together, in two parts: where everything lives, and who calls whom.

## The big picture

A CloudStack cloud has two kinds of machine. One runs the **head office**, the management server, which decides everything and writes it down in its ledger, a database. The others are **floors**, hypervisor hosts, where the VMs run.

Every floor has an address in a building plan: a hotel site (a zone), a building (a pod) and a wing (a cluster). Each level is a boundary where something stops, from the warehouse of room styles at the site to the shared storage room at the wing.

And one rule decides who calls whom: on a KVM floor, the attendant, CloudStack's agent, phones the head office and gets its instructions back on that same call. The head office only goes to a floor to set it up, or to repair it.

![The series in one picture. A floor (a KVM host) holds the floor attendant (cloudstack-agent) and the rooms and staff rooms (VMs and system VMs). The attendant dials the head office (management server) on the staff line, port 8250; the head office keeps its records in the ledger (MySQL), and both sit on the head office's machine. The rooms keep their disks in the storage rooms (primary storage); the warehouse (secondary storage) holds room styles. A note on the storage says part 1 covers where each box lives and how a site is divided; a note on the attendant says part 2 covers who calls whom, and why the floor dials.](../diagrams/02-series.png)

*Click the picture to enlarge it.*

Both parts follow the same example: the two-machine lab you'll build in [the install posts](../11.Install-By-Hand/README.md) *(coming soon)*, one machine for the head office and its ledger, and one KVM host. You're its operator throughout.

## The two parts

| Part | What it answers | Level |
|---|---|---|
| 1 · [Where Does Everything Live in a CloudStack Cloud?](01.Where-Everything-Lives.md) | Which machines a cloud runs on and what runs on each; how a cloud divides into regions, zones, pods, clusters and hosts; where disks and room styles are kept; which kinds of traffic the cables carry | Beginner → Intermediate |
| 2 · [Who Calls Whom in a CloudStack Cloud?](02.Who-Calls-Whom.md) | How a host's agent and the management server talk, and what happens when they stop; why VMware and XenServer hosts have no agent; how the system VMs get their jobs and reach the head office; every connection in the lab | Beginner → Intermediate |

Read them in order: [part 2](02.Who-Calls-Whom.md) builds on the building plan of [part 1](01.Where-Everything-Lives.md). Each takes under half an hour. Before them comes [What Is CloudStack? A Hotel for Computers](../01.Overview.md); after them, [Inside the Management Server](../03.Inside-The-Management-Server.md) *(coming soon)*.
