# In-progress checks

Internal tracking of links that point at posts not written yet, so none of them fall through the cracks. Like everything in `references/`, this file is not published on the blog.

## The rule

Whenever a post refers to another post, it **links** to it. It never just says "post 05 covers this" in plain text.

If the target post doesn't exist yet:

1. **Link to its placeholder page ("stub")**, which sits at the post's final path (for example `01.General/NN.Some-Topic.md`). The link works today and keeps working once the real post replaces the stub under the same file name. Create the stub if it doesn't exist yet; every stub contains the marker `STUB:` in an HTML comment.
2. **Add a row to the table below** saying where the link is and what the linking text promises the target will contain.

## When a stub becomes a real post

1. Replace the stub with the post, keeping the same file name.
2. Go through every row for that stub:
   - Make sure the post keeps each promise.
   - Where a promise is about one particular section, point the link at that section's anchor (for example `NN.Some-Topic.md#the-section-heading`).
   - Remove *(coming soon)* from the linking text.
3. Delete the rows, and run `mkdocs build --strict` to confirm every link and anchor resolves.

List the stubs still waiting to be written:

```sh
grep -rl 'STUB:' 00.Learn --include='*.md' --exclude-dir=references
```

## Pending

Paths are relative to `00.Learn/01.General/`.

Rows come from links in written pages, not from stubs: a module's reading order needs no rows. The first attempt's rows are kept in `archive/v1/in_progress_checks.md`.

| Stub (target) | Linked from | What the link promises / what to fix |
|---|---|---|
| `04.API-And-Database.md` | `03.What-A-Cloud-Adds.md`, section "One program decides: the management server": "It's one program, though several identical copies of it can run at once, as [How Do You Ask CloudStack for Something?] shows." | 04 shows that several identical copies of the management server can run at once, sharing one database (GEN-15). Point the link at that section, and remove *(coming soon)* |
| `04.API-And-Database.md` | `03.What-A-Cloud-Adds.md`, the "Next up" line: "The management server decides. How do you ask it for anything, and where does it keep what it knows?" | 04 explains how every request reaches the management server (its API) and where it keeps its records (one database). Remove *(coming soon)* from the line |
| `05.Accounts-And-Roles.md` | `03.What-A-Cloud-Adds.md`, section "Tenants share the pool": "CloudStack has its own names for a tenant and for those logins, which [Who May Ask the Cloud for What?] explains." | 05 explains CloudStack's record for a tenant (the account) and the logins of its people (users). Point the link at that section, and remove *(coming soon)* |
| `06.Talking-To-Hosts.md` | `02.Hypervisors.md`, section "libvirt starts and stops the VMs": "CloudStack talks to libvirt through a program of its own on each KVM host, which [How Does CloudStack Talk to a Host?] introduces" | 06 introduces CloudStack's own program on a KVM host (the agent), which carries out the management server's instructions through libvirt. Point the link at that section, and remove *(coming soon)* |
| `06.Talking-To-Hosts.md` | `03.What-A-Cloud-Adds.md`, section "Follow one request through the cloud", step 4: "On a KVM host, a CloudStack program there hands the instruction to libvirt … [How Does CloudStack Talk to a Host?] introduces that program." | 06 introduces CloudStack's own program on a KVM host (the agent), which carries out the management server's instructions through libvirt. Point the link at that section, and remove *(coming soon)* |
| `06.Talking-To-Hosts.md` | `03.What-A-Cloud-Adds.md`, section "When the management server stops, the VMs carry on": "If a host fails meanwhile, the automatic restarts that CloudStack can do for its VMs don't happen while the management server is down. [How Does CloudStack Talk to a Host?] explains those restarts." | 06 explains HA, role only: CloudStack restarting a failed host's HA-enabled VMs on another host. Point the link at that section, and remove *(coming soon)* |
| `07.Where-Disks-Live.md` | `02.Hypervisors.md`, section "Follow one VM: a start and a disk write", step 3 of the disk write: "QEMU writes the data to the VM's disk on the host: a file, a device or storage reached over the network, wherever the host keeps it. That's the subject of [Where Does a VM's Disk Live?]" | 07 explains what a VM's disk physically is (a file or a block device) and where it can live (the host's own disk, or a storage server reached over the network). Point the link at that section, and remove *(coming soon)* |
| `08.Clusters.md` | `02.Hypervisors.md`, section "Where KVM fits": "CloudStack's own phrase "hypervisor type" means something else: which hypervisor a host runs (KVM, VMware, XenServer and so on), not type 1 or type 2. [Which Hosts Can a VM Move Between?] teaches it." | 08 teaches CloudStack's "hypervisor type" (which hypervisor a host runs) and says it isn't type 1 or type 2 (GEN-36's misconception). Point the link at that section, and remove *(coming soon)* |
| `09.Zones-And-Pods.md` | `01.Virtual-Machines.md`, section "CloudStack's words: host and Instance": "The people who use a cloud never see its hosts; the team that runs it does … The reason comes [later in this module]" | 09 explains why the people who use a cloud (end users) never see its hosts (they choose a zone and never see what's inside it). Point the link at the section that gives the reason, and remove *(coming soon)* |
| `15.Lab-Preparing-A-Machine.md` | `01.Virtual-Machines.md`, section "Try it in your lab (optional)": "if your machine is itself a VM, [What Does One Machine Need to Run CloudStack?] shows what it needs" | 15 says what a lab machine that is itself a VM needs (nested virtualisation, step 1 of its thread). Point the link at that section, and remove *(coming soon)* |
| `04.API-And-Database.md` | `99.Check-Yourself-Answers/03.What-A-Cloud-Adds.md`, Evidence, "The VMs keep running when the management server stops": "each running copy also holds live connections to some of the hosts, as [How Do You Ask CloudStack for Something?] shows" | 04 shows that each copy of the management server holds live connections of its own, while the records are shared (GEN-15). Point the link at that section, and remove *(coming soon)* |
