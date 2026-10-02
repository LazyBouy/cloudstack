# Course strategy: CloudStack from the Ground Up

Status: approved 2026-10-01 · Written against: commit `1a48a87587` · Last changed: 2026-10-01

Code pointers are `path:line` at the pinned commit `1a48a87587c03472feefb081cfac71b2ebd0f407` (read them with `.github/scripts/pinned.py excerpt cloudstack:PATH:N-M`). Doc quotes are from the 4.22.1.1 docs unless marked otherwise. "v1 F<n>" points at a finding in the archived dossiers (`archive/v1/working/01.General/*/research.md`), to be re-verified before use.

## 1. The learner and the destination

**Who starts.** Someone who knows basic Linux: the shell, files and permissions, installing packages, starting services with systemd, SSH, editing a config file. They don't know virtualisation, clouds, networking beyond "a machine has an IP address", storage protocols, databases or Java. They learn one step at a time, in order.

**What they can do at the end.**

- **Understand.** Say what each part of a CloudStack cloud is for, why it's built that way, and what happens, step by step and down to the code, between a request and its result: for example, from `deployVirtualMachine` to a running VM.
- **Run.** Plan a small cloud for a stated need (zones, pods, clusters, hosts, storage, networks), build one from the 4.22 docs, and look after it: maintenance, upgrades, usage records.
- **Troubleshoot.** Start from a symptom (a VM stuck in Starting, "insufficient capacity", a host Disconnected, a template that never downloads), name the part involved, and find the evidence in the logs, the database and the code.
- **Extend.** Add an API command or a plugin, knowing where it's declared and wired, and test it with the simulator.
- **Explain the why.** Argue for or against one of CloudStack's design choices (one management server, agents that dial in, system VMs, storage scopes), with its trade-offs.

Module 01 is for everyone. Modules 02–09 go deep into one part each. Module 10 is for those who will change the code.

## 2. What makes CloudStack CloudStack

These traits come from CloudStack's own docs and code, before any other course was looked at. They decide the module map (§3) and the analogy test (§4). Each says what it is in plain words, its evidence with its exact scope, what a learner must grasp, and where it's taught.

### T1. One program decides; one database remembers

- **Plain words.** The management server is one Java program, run as one systemd service. It takes every request, decides what happens, and instructs the hosts. It can run as several identical copies behind a load balancer; the copies share one MySQL database, which holds the cloud's records. Each copy holds the live connections of some hosts, and passes on work for hosts held by another copy.
- **Evidence.**
    - `packaging/systemd/cloudstack-management.service:26,38`: one service, one `java` command.
    - "The Management Server itself may be deployed in a multi-node installation where the servers are load balanced." and "requires a MySQL database for persistence" ([Concepts](https://docs.cloudstack.apache.org/en/4.22.1.1/conceptsandterminology/concepts.html)).
    - `framework/cluster/src/main/java/com/cloud/cluster/ManagementServerHostVO.java:38`: the copies are listed in the `mshost` table.
    - `engine/schema/src/main/java/com/cloud/host/HostVO.java:416`: each host records the copy it's connected to (`mgmt_server_id`).
    - `engine/orchestration/src/main/java/com/cloud/agent/manager/ClusteredAgentManagerImpl.java:581-586` and `ClusteredAgentAttache.java:179`: a copy that doesn't hold a host's connection creates a forwarding attache and forwards the request to the peer that does.
- **Exact scope.** One or more copies; one shared database; each host's connection held by one copy at a time. Never "one management server" without "possibly several identical copies"; never "the program holds no state" (each copy holds live connections and in-flight work; the records are in the database).
- **The learner must grasp:** a single brain, not a federation of services; the database is the cloud's memory; scaling the brain means more identical copies.
- **Taught in:** 01 (role), 02 (inside), 09 (running several).

### T2. The physical data centre is modelled on purpose

- **Plain words.** The operator describes the real layout to CloudStack: zones (typically a data centre), pods (often a rack, whose hosts share a subnet), clusters (hosts of the same hypervisor type that share primary storage) and hosts (one computer each). Users see zones; pods, clusters and hosts are hidden from them.
- **Evidence.**
    - [Concepts](https://docs.cloudstack.apache.org/en/4.22.1.1/conceptsandterminology/concepts.html): "A zone typically corresponds to a single datacenter, although it is permissible to have multiple zones in a datacenter"; "A pod often represents a single rack. Hosts in the same pod are in the same subnet."; "A cluster consists of one or more hosts and one or more primary storage servers."; "A host is a single computer"; "Zones are visible to the end user."; "Pods are not visible to the end user."; "Hosts are not visible to the end user."
    - `engine/schema/src/main/java/com/cloud/dc/ClusterVO.java:56-64`: a cluster row names its zone, its pod and its hypervisor type.
    - `engine/schema/src/main/java/com/cloud/host/HostVO.java:131`: each host records its own hypervisor type.
    - `server/src/main/java/com/cloud/resource/ResourceManagerImpl.java:3781-3784`: a host whose hypervisor type differs from its cluster's is refused ("Can't add host whose hypervisor type is: … into cluster: … whose hypervisor type is: …"); `:3785-3790` does the same for the CPU architecture when both are known.
    - `api/src/main/java/org/apache/cloudstack/api/command/user/vm/BaseDeployVMCmd.java:79` (`zoneid` required) and `:176` (`hostid` "available for root admin only"); `api/src/main/java/org/apache/cloudstack/api/command/admin/vm/DeployVMCmdByAdmin.java:38,41` (`podid`, `clusterid`, root admin only).
- **Exact scope.** Each host runs its own hypervisor; the hosts of a cluster share a hypervisor *type* (and CPU architecture, when set). The docs' own sentence "The hosts in a cluster all have identical hardware, run the same hypervisor…" means the same type: quote it only with that gloss. A cluster has one or more hosts and one or more primary storage pools.
- **The learner must grasp:** each level answers a problem (isolation and redundancy, a shared subnet, shared storage and migration), so each is taught as the answer to its problem, never as a list.
- **Taught in:** 01, 04, 07.

### T3. It drives hypervisors it doesn't contain

- **Plain words.** CloudStack isn't a hypervisor. It commands hypervisors of several types through one API, and a VM's disk images are in its hypervisor type's format.
- **Evidence.** `api/src/main/java/com/cloud/hypervisor/Hypervisor.java:46-60` lists the types the code knows, with image formats (`XenServer` VHD, `KVM` QCOW2, `VMware` OVA, plus `Simulator`, `External` and others). "CloudStack supports three hypervisor families, KVM, XenServer/XCP-ng with XAPI, and VMware with vSphere"; LXC, Hyper-V and Oracle VM are "not tested to work fine for last many CloudStack releases" ([Compatibility Matrix](https://docs.cloudstack.apache.org/en/4.22.1.1/releasenotes/compat.html)).
- **Exact scope.** The code knows more types than the docs support. The course's lab is KVM; VMware and XenServer appear as contrasts; the rest are named once.
- **The learner must grasp:** CloudStack orchestrates; the hypervisor on each host runs the VMs.
- **Taught in:** 01, 04.

### T4. Two ways to reach a host, and KVM's agent dials in

- **Plain words.** On a KVM host, CloudStack's agent opens a connection to the management server and keeps it open; instructions come back down that connection, and the agent reports regularly. For VMware and XenServer there's no CloudStack agent on the host: the management server loads a "resource" for that host inside itself and talks to vCenter or XAPI.
- **Evidence.**
    - `agent/conf/agent.properties:30-31,45-46`: the agent's settings name the management server's address and port 8250.
    - `engine/orchestration/src/main/java/com/cloud/agent/manager/AgentManagerImpl.java:234,284`: the management server listens on 8250 "for remote (indirect) agent connections".
    - `engine/schema/src/main/java/com/cloud/configuration/ManagementServiceConfiguration.java:23-26`: `ping.interval` 60 seconds, `ping.timeout` a multiplier of 2.5.
    - `server/src/main/java/com/cloud/hypervisor/kvm/discoverer/LibvirtServerDiscoverer.java:300-304`: adding a KVM host, the management server logs in once over SSH to run `cloudstack-setup-agent`.
    - `engine/orchestration/src/main/java/com/cloud/agent/manager/AgentManagerImpl.java:995-1040`: `loadDirectlyConnectedHost` loads a directly connected host's resource inside the management server, as a `DirectAgentAttache`.
- **Exact scope.** "Dials in" is true of the KVM agent, and of the agent inside the secondary storage and console proxy VMs (T6), not of VMware or XenServer hosts. Why the KVM design opens the connection from the host is a question for the researcher; no reason may be stated without a source.
- **The learner must grasp:** who opens the connection, what flows over it, and what "the host went quiet" sets off.
- **Taught in:** 01 (role), 04 (depth).

### T5. Storage is split by job, and where a disk lives decides where its VM can go

- **Plain words.** Primary storage holds VMs' disks, close to the hosts; a pool serves one host (local), a cluster, or a whole zone. Secondary storage holds templates, ISOs and snapshots for a zone or a region. A running VM can move only to a host that can reach its disks, and a VM whose root disk is on a host's local storage isn't restarted elsewhere when that host dies.
- **Evidence.**
    - `api/src/main/java/com/cloud/storage/DataStoreRole.java:25` (`Primary`, `Image`, `ImageCache`, `Backup`, `Object`) and `api/src/main/java/com/cloud/storage/ScopeType.java:25` (`HOST`, `CLUSTER`, `ZONE`, `REGION`, `GLOBAL`).
    - [Concepts](https://docs.cloudstack.apache.org/en/4.22.1.1/conceptsandterminology/concepts.html): "Primary storage is associated with a cluster, and it stores virtual disks for all the Instances running on hosts in that cluster."; "On KVM and VMware, you can provision primary storage on a per-zone basis."; "You can add multiple primary storage servers to a cluster or zone. At least one is required."; secondary storage "may be defined as per zone or per region".
    - `server/src/main/java/com/cloud/storage/StorageManagerImpl.java:447-448`: zone-wide primary storage is accepted for KVM, VMware, Hyperv, LXC, Simulator and Any.
    - `engine/orchestration/src/main/java/com/cloud/vm/VirtualMachineManagerImpl.java:3142-3152`: a migration to a host in another cluster is refused unless every volume is on zone-wide storage (VMware excepted).
    - `server/src/main/java/com/cloud/ha/HighAvailabilityManagerImpl.java:388-394`: HA skips a VM whose root volume is on local storage, "Its fate is tied to the host."
    - `engine/storage/volume/src/main/java/org/apache/cloudstack/storage/volume/VolumeServiceImpl.java:1681-1692`: the first time a volume is made from a template on a primary store, the template is copied there first.
- **Exact scope.** The docs name KVM and VMware for zone-wide primary storage; the code accepts more types (a docs-vs-code note for module 05). Shared storage never means shared disks: each disk stays private to its VM.
- **The learner must grasp:** the chain, link by link: a disk is a file or block device somewhere → it can be on the host or on a storage server → VMs must move or restart elsewhere → so other hosts must reach the disk → hence host, cluster and zone scope.
- **Taught in:** 01 (the chain), 05 (depth), 07 (migration and HA).

### T6. CloudStack runs its own VMs to do its own work

- **Plain words.** Some of CloudStack's jobs are done by VMs it creates and manages itself: the secondary storage VM (fetches and copies templates and snapshots), the console proxy VM (shows a VM's screen in the browser) and the virtual router (network services for guest networks), plus a few rarer kinds.
- **Evidence.**
    - `api/src/main/java/com/cloud/vm/VirtualMachine.java:247-249`: VM types; `DomainRouter`, `ConsoleProxy`, `SecondaryStorageVm` and others are flagged "used by system".
    - "CloudStack manages these system VMs and creates, starts, and stops them as needed based on scale and immediate needs." ([System VMs](https://docs.cloudstack.apache.org/en/4.22.1.1/adminguide/systemvm.html)).
    - `server/src/main/java/com/cloud/consoleproxy/ConsoleProxyManagerImpl.java:697` and `services/secondary-storage/controller/src/main/java/org/apache/cloudstack/secondarystorage/SecondaryStorageManagerImpl.java:653`: console proxy and secondary storage VMs are created for the system account.
    - `server/src/main/java/org/apache/cloudstack/network/router/deployment/RouterDeploymentDefinition.java:346-350` and `server/src/main/java/com/cloud/network/element/VirtualRouterElement.java:236`: a virtual router is recorded under the system account for system and shared networks, and otherwise under the guest network's account.
    - `systemvm/debian/opt/cloud/bin/setup/secstorage.sh:24` (the secondary storage VM runs the `cloud` agent service), `systemvm/debian/opt/cloud/bin/setup/common.sh:703-705` (the router disables it) and `scripts/network/domr/router_proxy.sh:43` (the host reaches the router over SSH, port 3922).
- **Exact scope.** "System VMs belong to the system" is too short: the router of an isolated network is recorded under that network's account. The docs say "There is no mechanism for the administrator to log in to the virtual router", while the host's own script logs in over SSH: a docs-vs-code point for module 08.
- **The learner must grasp:** they're ordinary VMs on ordinary hosts, doing CloudStack's work, and CloudStack talks to each kind differently.
- **Taught in:** 01, 05, 06, 08.

### T7. Self-service for many tenants, from menus

- **Plain words.** Resources belong to accounts. Accounts sit in a tree of domains; users are the logins inside an account; projects let accounts share. Users choose from menus the operator made (offerings for sizes, templates for what a VM starts from), and they choose a zone, never a host.
- **Evidence.** "An Account typically represents a customer of the service provider or a department in a large organization."; "Resources belong to the Account, not individual Users in that Account."; "Domain administrators do not have visibility into physical servers or other domains." ([Accounts](https://docs.cloudstack.apache.org/en/4.22.1.1/adminguide/accounts.html)). `api/src/main/java/org/apache/cloudstack/acl/RoleType.java:33-38` (four role types: Admin, ResourceAdmin, DomainAdmin, User); `api/src/main/java/com/cloud/domain/Domain.java:31` (the ROOT domain is id 1); `server/src/main/java/com/cloud/server/ConfigurationServerImpl.java:447` (the `system` account is created on first start); T2's deploy-command pointers.
- **Exact scope.** Four default role *types*; the docs also list newer read-only and support roles. A "user" in CloudStack is a login, not a customer.
- **The learner must grasp:** ownership is by account; administrative power is scoped (root admin, domain admin); the menu model.
- **Taught in:** 01, 03.

### T8. API first, and asynchronous by design

- **Plain words.** Every action is an API command; the web UI and the command line are just clients. Commands that can take long answer at once with a job ID and finish in the background; work on one VM runs one job at a time.
- **Evidence.** `README.md:64-67` ("a full and open native API"); 1,038 source files under `*/src/main/` carry `@APICommand(` (`git grep -l`, plugins included, bundled or not); `ui/public/config.json:2` (`"apiBase": "/client/api"`); "Commands are designated as asynchronous when they can potentially take a long period of time to complete" and "will immediately return a job ID" ([Programmer Guide](https://docs.cloudstack.apache.org/en/4.22.1.1/developersguide/dev.html)); `api/src/main/java/org/apache/cloudstack/api/BaseAsyncCmd.java:24`; `engine/orchestration/src/main/java/com/cloud/vm/VirtualMachineManagerImpl.java:6023` with `framework/jobs/src/main/java/org/apache/cloudstack/framework/jobs/impl/AsyncJobManagerImpl.java:322` (VM work goes into a queue keyed by the VM, with a size limit of 1).
- **Exact scope.** "About a thousand command classes in the source tree", not "a thousand commands available": not every plugin is bundled.
- **The learner must grasp:** the UI isn't special; a ticket now, the result later; why a busy VM makes the next request wait.
- **Taught in:** 01, 02, 03.

### T9. Networks are assembled per tenant, from offerings and providers

- **Plain words.** A zone has a network model (Basic or Advanced) and a kind (Core or Edge). Guest networks are created from network offerings, and their services (addresses, names, address translation, firewall, load balancing…) come from providers, most often the virtual router.
- **Evidence.** `api/src/main/java/com/cloud/dc/DataCenter.java:31-37` (`NetworkType` Basic, Advanced; `Type` Core, Edge); `api/src/main/java/com/cloud/network/element/NetworkElement.java` (the provider interface); [System VMs](https://docs.cloudstack.apache.org/en/4.22.1.1/adminguide/systemvm.html) ("The end user has no direct access to the virtual router").
- **The learner must grasp:** a tenant's network is a product built from parts, and the virtual router is one of the parts.
- **Taught in:** 01 (big picture), 06.

### T10. One codebase, pluggable inside, configured from the database

- **Plain words.** The management server is assembled from Spring modules; hypervisors, storage drivers, network providers and authenticators are plugins in that hierarchy. Most settings are global settings kept in the database, some with a narrower scope (zone, cluster, account…).
- **Evidence.** `core/src/main/resources/META-INF/cloudstack/compute/module.properties:20-21` and `plugins/hypervisors/kvm/src/main/resources/META-INF/cloudstack/kvm-compute/module.properties:17-18` (a plugin's module names its parent); `framework/config/src/main/java/org/apache/cloudstack/framework/config/impl/ConfigurationVO.java:36` (the `configuration` table).
- **The learner must grasp:** change behaviour with settings, extend it with plugins, and know where each lives in the code.
- **Taught in:** 02, 10.

### T11. One product, three kinds of process

- **Plain words.** CloudStack calls itself "a turnkey solution". On the machines, it's three kinds of systemd service: the management server, the agent (on KVM hosts) and the optional usage server.
- **Evidence.** `README.md:64-67`; `packaging/systemd/cloudstack-management.service:26`, `cloudstack-agent.service:23`, `cloudstack-usage.service:26`; the agent package is for "this computer [that] will participate in your cloud as a KVM HyperVisor" (`debian/control:31-33`).
- **The learner must grasp:** what to install where, and that the usage server is separate and optional.
- **Taught in:** 01, 09.

**What these traits do to the course.** T1, T8 and T10 make the management server the first deep dive, as the user decided. T2, T4 and T5 put the physical estate and the storage chain at the heart of module 01, because they decide where a VM can run, move and restart. T6 and T9 mean networking and system VMs need their own modules, late, once hosts, storage and placement are known. T7 gets a module because "who may ask for what" runs through every later topic.

## 3. Module map

| Module | The question it answers | Arrives knowing | Leaves able to | Builds on |
|---|---|---|---|---|
| `01.General` | What is CloudStack, and what happens when someone asks it for a VM? | Basic Linux only | Explain what a cloud adds to virtualisation; name CloudStack's parts and what each is for; follow one VM request from the API to a running VM; explain why the physical layout and the storage layout decide where a VM can run, move and restart; say who may ask for what; (if the lab is kept here, see §7) build a small cloud from the docs and find each part in it | — |
| `02.Management-Server` | What is inside the one program that runs the whole cloud? | 01's map: the management server's role, the API, async jobs, the database as the record | Trace an API call through the layers (command, service, orchestrator, agent command) in the code; explain how the program is assembled from Spring modules and plugins; read the data model (VOs, DAOs, views) and the upgrade chain; explain async jobs and per-VM work queues; explain global settings and their scopes; explain how several copies share the work | 01 |
| `03.Accounts-And-API` | Who may ask the cloud for what, and how do they prove who they are? | 01 (accounts and domains in outline; the API as the only door); 02 (the request path) | Sign an API request by hand and name every check it passes; design domains, accounts and projects for an organisation; explain roles, API permissions and how the UI follows them; reason about resource limits; place external identity (LDAP, SAML, two-factor) in the picture | 01, 02 |
| `04.Hosts-And-Hypervisors` | How does CloudStack command a physical server it doesn't run on? | 01 (hosts, hypervisor types, agents that dial in); 02 (agent commands) | Describe a KVM host's stack (libvirt, QEMU, the agent) and each part's job; follow a command from the management server to libvirt and back; explain the connection's life (setup, startup report, pings, disconnection) and what a quiet host sets off (investigation, fencing, HA); contrast agent-based and directly connected hypervisors; place the simulator and the External type | 01, 02 |
| `05.Storage` | Where do a VM's disks and images live, and how do they move? | 01's storage chain; 04 (hosts mount storage) | Choose primary storage (protocol, scope) for a need and defend the trade-off; follow a template from registration to a VM's root disk; explain volumes, snapshots and their copies; read the storage plugin framework (providers, drivers, data motion); place object storage and shared filesystems | 01, 02, 04 |
| `06.Networking` | How does each VM get a network, and how are tenants kept apart? | 01 (guest and public networks; the virtual router exists); 04 (the host's bridges) | Explain physical networks and traffic types; isolation methods; guest network types and zone models (Basic with security groups, Advanced); each virtual-router service and how it's configured; design a VPC with tiers and ACLs; explain network offerings and providers, including SDN integrations in outline | 01, 02, 04 |
| `07.Instances` | How does CloudStack choose where a VM runs, and what happens over its life? | 01's journey; 04, 05, 06 | Explain deployment planning (planners, host and storage allocators, tags, affinity, dedication) and debug "insufficient capacity"; explain the VM state machine and work jobs; explain live and storage migration, scaling and VM HA; explain compute offerings in depth (speed, shares, overcommit); user data and config drive; import and unmanage; VM snapshots and the backup framework | 02, 04, 05, 06 |
| `08.System-VMs` | How does CloudStack build, run and talk to its own VMs? | 01 (what each system VM is for); 05 (the storage VM's role); 06 (the router's services); 07 (placement and lifecycle) | Explain the system VM template and how one image becomes a storage VM, console proxy or router; how the management server reaches each; the storage VM's and console proxy's jobs and scaling; the router's configuration path (databags, `configure.py`); upgrading and troubleshooting system VMs | 04, 05, 06, 07 |
| `09.Operating-A-Cloud` | How do you keep a cloud healthy, measured and up to date for years? | 01–08 | Plan management-server redundancy and database backups; find faults with events, alerts, logs and metrics; run maintenance on hosts and storage safely; upgrade CloudStack (packages, database, system VMs); explain usage records and quota; harden it (certificates, the CA framework, secrets) | 02–08 |
| `10.Extending-CloudStack` | How do you change CloudStack, add to it, and contribute back? | 02's code map; the deep dive of the part being changed | Build CloudStack and run it with the simulator on their own machine; add an API command end to end (command, service, registration, permissions, UI); write a plugin in its own Spring module; use the Extensions framework; write a Marvin test; prepare an upstream contribution | 02, 03, others as needed |
| `11.Beyond-VMs` (optional, §7) | What does CloudStack build out of VMs for its users? | 06, 07 | Explain how the Kubernetes Service (CKS) builds clusters from VMs, how VM AutoScale works, and how backup providers plug in | 06, 07 |

**Why this order.**

1. `01.General` first: the whole map, and the first-principles chains every deep dive leans on (the user fixed this).
2. `02.Management-Server` next: the brain drives everything else, code reading starts here, and the request path and async jobs recur in every later module (the user fixed this).
3. `03.Accounts-And-API`: the outside contract of 02's front door. Later modules ask "who may do this?" (who sees hosts, who owns a router), so it comes early.
4. `04.Hosts-And-Hypervisors`: every storage, network and VM operation ends as a command to a host.
5. `05.Storage` before `06.Networking`: storage is smaller and more concrete, and it introduces the storage VM; networking is the largest and hardest topic.
6. `07.Instances` after 04–06: a placement picks a host, storage pools and networks together, so it needs all three.
7. `08.System-VMs` after 07: they're VMs placed and started like any other, serving 05 and 06.
8. `09.Operating-A-Cloud` once the parts are known: operations cut across all of them.
9. `10.Extending-CloudStack` last: it needs 02's code map and the depth of the part being changed.

**Notes on the map.**

- **The lab.** The learner needs a cloud to look at well before the deep dives. The 4.22 Quick Installation Guide builds a one-machine KVM cloud ("This guide can NOT be used for production setup", [QIG](https://docs.cloudstack.apache.org/en/4.22.1.1/quickinstallationguide/qig.html)), and the repository documents a simulator image (`docker run --name simulator -p 8080:5050 -d apache/cloudstack-simulator`, `tools/docker/README.md:37`). The recommendation is to end 01 with these (§7, decision 3). Our posts are written from the docs and never show output from a run that didn't happen.
- **KVM first.** The lab and the examples use KVM; VMware and XenServer appear where the contrast teaches something (directly connected hosts, image formats).
- **Exercises.** The founding instruction asks for exercises. Proposed: one exercises article at the end of each module, with solutions on the answers pages (§5, §7 decision 4).

## 4. The analogy study

Two candidates, genuinely different: one an everyday scene designed around CloudStack's own shape, the other a bridge from what the learner already knows. Five other pictures were tried and dropped; they're listed after the candidates, with the reason.

### Candidate A: The cloud kitchen

**Chosen** by the user, 2026-10-01: the course's running analogy, used under the five conditions in "Comparison and recommendation".

- **The picture.** Order a meal on a delivery app and it may come from a restaurant with no dining room and no kitchen of its own. It's a virtual brand: a name, a menu and recipes, cooked at a station in a shared kitchen, next to other brands that never see each other. One company owns many such kitchens across a city. A business launches a brand there without buying an oven, and the company's head office decides which kitchen cooks it. CloudStack runs a cloud the same way: each VM is a virtual brand, each host a kitchen, and the management server the head office.
- **Mapping.**

| CloudStack thing | Analogy name | Why it fits | Evidence |
|---|---|---|---|
| VM (instance) | a virtual brand | A whole-seeming business that's really a station in a shared kitchen; many per kitchen; neighbours are kept apart (not absolutely: VMs on one network can reach each other) | `api/src/main/java/com/cloud/vm/VirtualMachine.java:247-249` (user VMs vs system VMs) |
| Host | a kitchen | One physical place whose burners, counter space and cooks (CPU, memory) its brands share | Concepts: "A host is a single computer"; "Hosts are not visible to the end user." |
| Hypervisor | the kitchen's equipment system | Each kitchen has its own; it divides the kitchen into private stations and shares out the burners | `engine/schema/src/main/java/com/cloud/host/HostVO.java:131` (each host has its own type) |
| Hypervisor type | the kind of equipment (induction, gas…) | A brand set up for one kind can't just carry on in another | `api/src/main/java/com/cloud/hypervisor/Hypervisor.java:47-49` (each type, its own image format) |
| Cluster | a row of kitchens | Kitchens with the same kind of equipment that share one or more cold stores; a brand moves only within its row | `ClusterVO.java:62-64`; `ResourceManagerImpl.java:3781-3784`; Concepts: "one or more hosts and one or more primary storage servers" |
| Pod | a kitchen hub | One building of rows, with its own internal phone network; customers never see it | Concepts: "Hosts in the same pod are in the same subnet."; "Pods are not visible to the end user." |
| Zone | a city | What the customer chooses; it has its own warehouse | Concepts: "Zones are visible to the end user."; `BaseDeployVMCmd.java:79` |
| Region | a sister company abroad, with its own head office | Separate head office, separate cities | Concepts: "Each region is controlled by its own cluster of Management Servers" |
| Management server | head office (HQ) | Takes every request, decides which kitchen, keeps the records, sends the instructions | `packaging/systemd/cloudstack-management.service:26,38` |
| Several management servers | several identical desks at HQ | They share one set of records; each kitchen's line rings at one desk, which passes on what it doesn't hold | `ManagementServerHostVO.java:38`; `HostVO.java:416`; `ClusteredAgentAttache.java:179` |
| Database | HQ's records | The one place the facts are written | Concepts: "requires a MySQL database for persistence" |
| API | HQ's counter | The only way to ask for anything; the web app and the phone (CLI) both go through it | `ui/public/config.json:2` |
| Async job | a ticket | HQ answers at once with a number, and does the work after | Programmer Guide (async commands); `BaseAsyncCmd.java:24` |
| Agent (KVM) | the kitchen supervisor | Phones HQ when the kitchen opens, keeps the line open, reports every minute (by default), carries out HQ's instructions. HQ never opens the line; it only sends someone over once, to set the supervisor up | `agent/conf/agent.properties:30-31,45-46`; `AgentManagerImpl.java:234,284`; `ManagementServiceConfiguration.java:23-26` |
| Directly connected host (VMware, XenServer) | a kitchen run through its supplier's control room | HQ calls the supplier's control room; there's no supervisor of CloudStack's on site | `AgentManagerImpl.java:995-1040` |
| Primary storage | cold stores | Where brands keep their shelves: a kitchen's own fridge (host scope), a row's cold store (cluster), a city-wide cold store (zone) | `ScopeType.java:25`; `StorageManagerImpl.java:447-448` |
| Volume (disk) | a brand's shelf | Private to its brand, even in a shared cold store; a brand can have more than one | Concepts: primary storage "stores virtual disks for all the Instances" |
| Secondary storage | the city warehouse | Launch kits, cookbooks and copies of shelves | `DataStoreRole.java:25`; Concepts (secondary storage contents) |
| Template | a launch kit | What a new brand starts from; one kit, many brands; copied to a cold store the first time it's used there | `VolumeServiceImpl.java:1681-1692` |
| Service offering | a kitchen allowance | How many burners and how much counter space a brand gets: a size, not a price | v1 F39 (offerings are sizes), to re-verify |
| System VMs | HQ's own units | Set up in the kitchens like brands, but run by HQ: the stock runner (storage VM), the camera window (console proxy), a business's receptionist (virtual router) | `VirtualMachine.java:247-249`; System VMs docs |
| Account, user, domain | a restaurant business, a staff login, a franchise group | The business owns the brands and, where the operator charges, gets the bill; staff log in; groups nest | Accounts docs: "Resources belong to the Account, not individual Users" |
| Root admin | the kitchen company's operations team | Sees and can do everything | `RoleType.java:34` |
| Live migration | moving a brand to another kitchen in its row, mid-service | Its shelves stay in the shared cold store | `VirtualMachineManagerImpl.java:3142-3152` |
| VM HA | restarting brands after a kitchen's power cut | The dishes on the burners are lost, the shelves aren't; a brand whose shelves were in that kitchen's own fridge has to wait | `HighAvailabilityManagerImpl.java:388-394` |

- **Stress test.**

| Behaviour | How the picture handles it | Verdict | Evidence |
|---|---|---|---|
| One management server, possibly several copies sharing one database | HQ, with one or more identical desks sharing one set of records. Each supervisor's line rings at one desk; a desk passes on instructions for kitchens it doesn't hold | Holds | `ManagementServerHostVO.java:38`; `HostVO.java:416`; `ClusteredAgentManagerImpl.java:581-586`; `ClusteredAgentAttache.java:179` |
| Zone, pod, cluster, host | City, hub, row, kitchen. Customers choose a city, never a kitchen; only the operations team can name a hub, row or kitchen | Holds for nesting and visibility; bends on scale (a zone is usually one data centre, not a city; a pod is usually a rack, not a building) | Concepts quotes (T2); `BaseDeployVMCmd.java:79,176`; `DeployVMCmdByAdmin.java:38,41` |
| Hosts of one cluster share a hypervisor type | Every kitchen has its own equipment; the kitchens of a row all have the same kind. The picture carries the exact scope the user asked for: "each its own, all the same kind", never "one equipment system per row" | Holds | `HostVO.java:131`; `ClusterVO.java:62-64`; `ResourceManagerImpl.java:3781-3784` |
| Agents that dial in | A new kitchen's supervisor is set up once (HQ sends someone over: SSH); from then on the supervisor phones HQ, keeps the line open and reports every minute; HQ sends instructions down that line. If the line stays quiet for two and a half report intervals, HQ treats the kitchen as unreachable and investigates: for a KVM kitchen whose row or city has cold stores that support it, HQ asks the row's other working kitchens before acting | Holds for KVM; bends for VMware and XenServer (HQ calls the supplier's control room) and for system VMs (the stock runner and camera window carry their own phones; the receptionist has none, so HQ's instructions for it go through the kitchen supervisor) | `LibvirtServerDiscoverer.java:300-304`; `agent.properties:30-31,45-46`; `AgentManagerImpl.java:234,284,995-1040`; `ManagementServiceConfiguration.java:23-26`; `api/src/main/java/com/cloud/ha/Investigator.java:24-31`; `plugins/hypervisors/kvm/src/main/java/com/cloud/ha/KVMInvestigator.java:85-97` (only with HA-capable storage); `plugins/hypervisors/kvm/src/main/java/org/apache/cloudstack/kvm/ha/KVMHostActivityChecker.java:156-169` (asks Up neighbours in the same cluster); `secstorage.sh:24`; `common.sh:703-705`; `router_proxy.sh:43` |
| System VMs | HQ's own units, set up in the kitchens like brands. The receptionist of a business's private network is booked to that business, though HQ runs it | Holds; the bookkeeping nuance is carried by the picture | `VirtualMachine.java:247-249`; `ConsoleProxyManagerImpl.java:697`; `SecondaryStorageManagerImpl.java:653`; `RouterDeploymentDefinition.java:346-350`; `VirtualRouterElement.java:236` |
| Primary and secondary storage | Cold stores near the kitchens, a warehouse per city. A shared cold store holds private shelves, so "shared storage" visibly doesn't mean shared disks. A kit is copied from the warehouse to a cold store the first time it's used there | Holds strongly: it answers the user's own complaint ("Why VMs always need to share storages?") | `ScopeType.java:25`; `DataStoreRole.java:25`; Concepts quotes (T5); `VolumeServiceImpl.java:1681-1692` |
| Self-service accounts and domains | Businesses launch brands themselves at HQ's counter; franchise groups nest; staff logins sit inside a business; the operations team sees all | Holds; bends on projects (a joint venture between businesses, taught in 03) | Accounts docs (T7); `RoleType.java:33-38`; `Domain.java:31` |
| Async jobs | A ticket number at the counter; HQ works through one brand's tickets one at a time | Holds | Programmer Guide (T8); `BaseAsyncCmd.java:24`; `VirtualMachineManagerImpl.java:6023`; `AsyncJobManagerImpl.java:322` |
| Live migration and HA | Moving a brand within its row; restarting brands after a power cut from their shelves, with the dishes lost. A brand on a kitchen's own fridge waits for its kitchen | Holds strongly; bends on the copy of memory (a real pan can't cross town still simmering) | `VirtualMachineManagerImpl.java:3142-3152`; `HighAvailabilityManagerImpl.java:388-394` |
| Templates and ISOs | Launch kits hold; an ISO is a cookbook a station is set up from by hand | Holds for templates; bends for ISOs | Concepts (secondary storage contents) |
| Networking below the role level (VLANs, address translation, firewall rules, load balancing, VPN, VPC tiers) | The receptionist covers the role only: gives each brand an extension (DHCP), keeps the directory (DNS), lets calls out (source NAT), forwards outside callers to the right brand (port forwarding) | Breaks below the role | T9 |
| The management server's internals (Spring modules, DAOs, plugins) | No kitchen parallel | Breaks: 02 and 10 use HQ only to orient | T10 |

- **Where it breaks, and what an article says there.**
    - Networking (06), below the receptionist's role: "The kitchen picture stops here. From now on, networks are taught as themselves."
    - Inside HQ (02, 10): "HQ is one program; its rooms are code, not people." The analogy orients the module's first article and is then dropped.
    - Directly connected hypervisors (04): "Some kitchens come with their supplier's own control room, and HQ phones it instead. CloudStack has no supervisor there."
    - Live migration (07): "A real pan can't cross town while it simmers. A VM's memory can be copied across the network while it runs."
    - Scale (01): "A zone is usually one data centre, not a city; the nesting is what the picture keeps."
    - ISOs (05): "Not a kit but a cookbook: the station is set up from it by hand."
- **Vocabulary cost.**
    - Words over the whole course, about 18: virtual brand, kitchen, equipment (kind), row, hub, city, HQ (and its counter, records and tickets), kitchen supervisor, cold store, the kitchen's own fridge, shelf, warehouse, launch kit, allowance, business, franchise group, and HQ's own units (stock runner, camera window, receptionist). Module 01 needs about 12 of them, spread over its articles, 1–3 per article, each counted in that article's concept budget.
    - No collision with CloudStack's own terms: host, zone, pod, cluster, template, offering, instance, domain, account, project, network and router stay CloudStack's. "Cold store" and "warehouse" line up with CloudStack's own "data store" and "image store", which helps.
    - Words deliberately avoided: "manager" (141 `*ManagerImpl` source files in the code), "agent", "guru", "planner", "order" (diners' orders are a VM's traffic; requests to HQ are API calls), "register" (`registerTemplate`), "port" and "switch" (networking words).
    - Small outside collisions: "hub" (Docker Hub), "row" (a database row), "supervisor" (supervisord).
- **Risks.**
    - Meals are short-lived; VMs run for months. Say once: a brand lasts as long as its business keeps it; the dishes are its work, not the brand.
    - "Supervisor" can sound like the one who decides. Say it: the supervisor never chooses which brands come in; HQ does.
    - Not every learner knows virtual brands. Two sentences and one picture in the first article fix that.
    - Inflated scale (a city for a data centre). State the real scale whenever a zone or pod is defined.
    - Food can feel playful. Use it sparingly: the picture orients, the CloudStack term carries the text.

### Candidate B: One Linux machine, scaled up

Not chosen (2026-10-01). Its Linux parallels stay available as one-off local bridges, never as a second running analogy.

- **The picture.** You already run a tiny "cloud" of one. On your Linux machine, programs run as processes; root decides who may do what; `apt` fetches software from a repository; the system runs its own daemons in the background; and `sleep 60 &` hands you a job number and gets on with it. CloudStack does each of these things for a whole data centre of machines, and for strangers. Every idea starts from what you'd do on one machine, then shows what changes with a thousand machines and many customers. Where the one-machine picture has nothing to offer (racks, data centres, customers' money), the course shows the real thing.
- **Mapping.**

| CloudStack thing | Linux parallel | Why it fits | Evidence |
|---|---|---|---|
| VM | a process | A running program with its own share of CPU and memory. On KVM, the agent asks libvirt to start the VM (`LibvirtComputingResource.java:2373`), and libvirt runs it as a QEMU process | `plugins/hypervisors/kvm/src/main/java/com/cloud/hypervisor/kvm/resource/LibvirtComputingResource.java:2373`; `debian/control:27` (the agent needs `qemu-kvm` and libvirt). "A QEMU process" is libvirt's behaviour, not yet backed by an approved source |
| Template | a program file, or a package | One file, many running copies | `VolumeServiceImpl.java:1681-1692` |
| Hypervisor type | a package format (`.deb`, `.rpm`) | A template is made in one hypervisor's disk format, like a package for one distribution | `Hypervisor.java:47-49` (VHD, QCOW2, OVA) |
| Secondary storage | the package repository | Where images are fetched from and kept | `DataStoreRole.java:25` |
| Primary storage | the disk a process's files live on | The machine's own disk, or an NFS share several machines mount: literal, not an analogy | `ScopeType.java:25` |
| Management server | the service manager (systemd) | You ask it to start something; it works out how, tracks the state and logs it | `packaging/systemd/cloudstack-management.service:26,38` |
| API | the commands you type (`systemctl`, `apt`) | The only way to ask | `ui/public/config.json:2` |
| Async job | a background job (`cmd &`, `jobs`, `wait`) | A number now, the result later | Programmer Guide (T8) |
| VM states | a unit's states (active, inactive, failed) | One small state machine per thing | `api/src/main/java/com/cloud/vm/VirtualMachine.java:50-58` |
| VM HA | `Restart=` in a unit file, across machines | Restart what died, somewhere it can run | `HighAvailabilityManagerImpl.java:388-394` |
| System VMs | system daemons | Run by the system, for the system | `VirtualMachine.java:247-249`; `ConfigurationServerImpl.java:447` |
| Root admin, users | root, ordinary users | The same idea, and CloudStack's own word | `RoleType.java:34`; `Domain.java:31` |
| Global settings | `sysctl` settings | Named knobs the running system reads | `ConfigurationVO.java:36` |
| Plugins | drivers | One per kind of hardware (hypervisor, storage) | T10 |

- **Stress test.**

| Behaviour | How the picture handles it | Verdict | Evidence |
|---|---|---|---|
| One management server, possibly several copies sharing one database | No one-machine parallel; taught literally ("several web servers sharing one database") | Breaks | T1 |
| Zone, pod, cluster, host | No parallel; taught literally (data centre, rack, group of servers, server) | Breaks | T2 |
| Hosts of one cluster share a hypervisor type | "A package built for one format won't install on another" carries image formats, but not why the hosts of a cluster must match (migration, shared storage) | Bends | `Hypervisor.java:47-49`; `ResourceManagerImpl.java:3781-3784` |
| Agents that dial in | No one-machine parallel; taught literally | Breaks | T4 |
| System VMs | Daemons, run by the system for the system | Holds | T6 |
| Primary and secondary storage | Local disk or NFS mount; the package repository | Holds, often literally | T5 |
| Self-service accounts and domains | Users and root hold; nested domains have no parallel (Linux groups don't nest) | Bends | T7 |
| Async jobs | Background jobs | Holds strongly | T8 |
| Live migration and HA | `Restart=` holds for HA; moving a running process to another machine has no everyday parallel | Holds (HA), breaks (migration) | T5 |

- **Where it breaks, and what an article says there.** Wherever there's no one-machine parallel (topology, agents, several management servers, offerings, domains), the article says "a single machine has nothing like this" and teaches the real thing, with a picture of the data centre.
- **Vocabulary cost.** No invented words: the learner already holds the parallels. Some go a little beyond "basic Linux" (`jobs`, `sysctl`, drivers), so they'd be used sparingly. The collisions are between layers, not words: a VM runs its own processes, its own daemons and its own root user, so "the VM's root isn't the cloud's root admin" must be said; on KVM a VM *is* a process on its host, which blurs "like" and "is"; and "kernel" must never stand for the management server, because KVM lives in each host's kernel.
- **Risks.**
    - Dry and abstract: there's no scene to draw, and the user has already called the first attempt "very dry".
    - Two technical layers held at once, which is hardest for the learners weakest in Linux.
    - "A VM is like a process" can plant a wrong idea about isolation: processes share one kernel, VMs don't.

### Also tried, and dropped

| Picture | What it fits best | Why it was dropped |
|---|---|---|
| The hotel (first attempt, retired) | Guests pick a site, never a floor; one head office | Borrowed from the OpenStack course. Rooms are fixed, while VMs are built on demand and move. Its building words invited wrong counts ("one storage room per wing"; a floor "running" a hypervisor). The user asked for a different analogy |
| Serviced offices | Tenants as businesses; files in a shared archive room | The hotel's family, with the hotel's break: suites don't move |
| A marina (boats at pontoons) | Movement; boats radioing the harbour office | Boats carry their own stores, so the storage chain, the user's main complaint, runs backwards; unfamiliar words (pontoon, berth) |
| A railway (gauge as hypervisor type, engineering trains as system VMs) | Type compatibility; the operator's own trains; signal boxes reporting in | Nothing maps a VM's disk; "network" collides with the railway itself |
| Air traffic control | One control room; pilots calling in; controllers owning sectors | Aircraft would be hosts and passengers VMs, which makes live migration absurd; no tenants, no storage |

### Comparison and recommendation

| | A: The cloud kitchen | B: One Linux machine, scaled up | The hotel (retired, for reference) |
|---|---|---|---|
| The storage chain | Strong: private shelves in shared cold stores; brands move and restart | Literal: local disk or NFS mount | Weak: rooms don't move |
| Physical hierarchy and types | Nesting and "each its own, all the same kind" hold; scale bends | Breaks: taught literally | Nesting held; invited "a floor runs one hypervisor" |
| One brain, dial-in, tickets | Holds; directly connected hosts bend | Tickets strong; dial-in and several brains break | Held; attendants only on KVM floors |
| System VMs and tenancy | Hold | System VMs strong; domains bend | Held |
| Main breaks | Networking internals, the management server's internals, ISOs | Topology, agents, several management servers, offerings | VMs built and moved; OpenStack heritage |
| Vocabulary cost | About 18 words over the course, 1–3 per article; no clash with CloudStack's terms | None invented; layer clashes (guest root and root admin, process and VM) | About 20 words, heavy up front |
| Scales into the deep dives | Orients 03–09; dropped on purpose inside 02, 06 and 10 | Everywhere, often literally | — |
| Main risk | Playful; inflated scale; virtual brands unfamiliar to some | Dry and abstract | The user rejected it |

**Recommendation: Candidate A, the cloud kitchen,** with B's Linux parallels allowed as one-off local bridges, never as a second running analogy.

- It answers the user's two main complaints. Its strongest mappings are exactly where the first attempt confused readers: storage that's shared without disks being shared, and why a VM can move or restart only where its disks can be reached. And it reads as a human scene, not a manual.
- It's built on CloudStack's own shape, not borrowed: customers choose a city and never a kitchen; HQ keeps one set of records for several desks; supervisors phone HQ; HQ runs units of its own inside the kitchens.
- Its words don't clash with CloudStack's.
- It stops cleanly where the internals begin, and every module plan says where.

Conditions, whichever candidate is chosen:

1. Analogy words count in each article's concept budget.
2. Each word is introduced at the moment its concept is taught. Never a mapping table up front: the full table lives here, not in a post.
3. Pictures label both: "kitchen (host)".
4. Where the picture breaks, the article says so in one sentence and carries on with the real thing.
5. Each module plan lists which analogy words it uses, and where it drops the picture.

If the user would rather pay no vocabulary at all, B is the honest alternative.

## 5. Voice and template

**Voice.** Confirmed as CLAUDE.md has it: "you" is the learner, who knows basic Linux and nothing else; operators and users are roles in the third person; British spelling; short paragraphs; questions move the reader on; misconceptions busted out loud.

**Template.** Confirmed as CLAUDE.md has it (header line, opening with the learner's question, "What you'll learn", body, "In short", "Check yourself", "Further reading", "Next up"). Proposed changes, for the user to accept (§7, decision 5):

1. **The analogy rules.** Once an analogy is chosen, add §4's five conditions to CLAUDE.md's "Writing rules".
2. **"Type" values.** The header's `**Type:**` takes one of: Concept (explains one idea), Journey (follows one request or event through the system), Hands-on (lab steps, from the docs), Exercises.
3. **Optional "Try it in your lab" sections.** Short, marked optional, never needed to follow the article; commands from the docs; output shown only when quoted from the docs or the code, and labelled so.
4. **One exercises article per module**, the module's last article, with solutions on the answers pages in `99.Check-Yourself-Answers/`.
5. **Each deep-dive module's first article** opens with one small picture placing that module's part in the whole cloud (with the analogy's names, if one is chosen): big picture first, at module level too.

**Where the lenses help most.** At most one or two per article. Kubernetes: the management server against the control plane, the agent against the kubelet, MySQL against etcd, and the word clashes ("pod" is a rack, "cluster" is a group of hosts), always noting that the lens isn't about CloudStack's own Kubernetes Service. OpenStack: one program against many services and a message queue (01, 02), `nova-compute` against the agent (04), Neutron's L3 agent against the virtual router (06), Keystone's domains and projects against CloudStack's (03), Glance against secondary storage (05).

## 6. Lessons from the first attempt

| Failure | Cause | What this strategy does about it |
|---|---|---|
| The course copied the OpenStack course: its module shape (Understand, Justify, Practise, Build), its post sequence and its template | Planning started from an existing course instead of from CloudStack | §2 derives the traits from CloudStack's docs and code first; §3's modules follow those traits; the OpenStack course was opened only after the plan stood, to check for copying and to place lenses |
| The hotel metaphor was borrowed | Same cause | §4 builds candidates from CloudStack's behaviour and stress-tests each one; the user picks |
| The analogy became a burden: a twenty-row mapping table in the first post | Analogy words weren't counted anywhere, and were all introduced at once | Analogy words count in the concept budget and arrive one at a time, at first need (§4, conditions) |
| Wrong shorthand: "a cluster runs exactly one hypervisor"; "one storage room per wing" | Facts compressed into analogy objects with a natural singular; the docs' own shorthand copied | Every trait and mapping records its exact scope ("each its own, all the same type"; "one or more cold stores"); the docs' shorthand is flagged where it appears (T2) |
| Concepts dumped: three storage scopes named before saying what a disk is or why other hosts need it | The problem wasn't taught before its options | Chains are written link by link (T5 here; in full in each module plan), and the order check forbids options before their problem |
| Dense posts: 30 to 40 minutes, dozens of excerpts, details kept because they were true | No concept budget; no list of details to leave out | 10–20 minute targets, 3–5 new concepts each, "details in" and "details out" for every article; code in the body only where it teaches; evidence on the answers pages |
| An arbitrary split into two parts | A long post was cut to fit a time cap | Only the strategy splits, by the learner's questions; each article must give a payoff on its own |
| The perspective switched between operator and user | No single voice | "You" is the learner; roles in the third person (§5) |
| One overview tried to hold everything: clouds, virtualisation, CloudStack, the hotel, the API, roles, history and versions | No "one question per article" rule | Every article answers one question, with one idea; history and version numbering go where a learner needs them, or nowhere |
| Many promises to unwritten posts ("coming soon") in the first article | Forward links used as signposts | Forward links only where the learner needs to know the answer is coming, each promise fitting the target's scope |

## 7. Decisions for the user

**Decided by the user, 2026-10-01:** (1) the cloud kitchen; (2) the module map as proposed, with `11.Beyond-VMs` kept as optional; (3) the lab at the end of `01.General`; (4) one exercises article per module; (5) all the template changes in §5. Decision 6 (hub.docker.com) is deferred until the lab articles are planned.

1. **The running analogy.**
    - A, the cloud kitchen (recommended).
    - B, one Linux machine, scaled up.
    - No running analogy at all: LearnKube's own practice, with short local analogies used once.
2. **The module map** (§3). Approve, or adjust. Points worth a look:
    - `03.Accounts-And-API` as a module of its own, rather than folded into 02;
    - the order of 04 to 08 (hosts, storage, networking, instances, system VMs);
    - `11.Beyond-VMs`: keep it as an optional module, or fold its topics into 07 and 09.
3. **Where the hands-on lab goes.**
    - The last articles of `01.General`: a simulator in minutes, then a one-machine KVM cloud from the 4.22 Quick Installation Guide (recommended: the learner has a cloud to look at before the deep dives, and the zone wizard walks back through every concept of 01).
    - A module of its own right after 01. That would make Management-Server `03`, against the numbering the user gave.
4. **Exercises.** One exercises article at the end of each module, with solutions on the answers pages (recommended), or none for now.
5. **Template changes** (§5): the "Type" values, the optional lab sections, the exercises article, and the opening picture of each deep-dive module.
6. **A proposed new source.** `hub.docker.com`, only to check which `apache/cloudstack-simulator` tags exist (the repository's `tools/docker/README.md` documents the image, but shows only an example tag, 4.17.2.0).

**Open questions** (for the module plans, not decisions now):

- Which simulator image tags match 4.22, and whether the image is current enough for the lab (needs decision 6, or another source).
- The 4.22.1.1 Quick Installation Guide builds on an EL8 distribution; whether the lab should follow it or the Ubuntu route in the KVM install guide.
- Where the Extensions framework (the External hypervisor type) is taught: the concept in 04, building one in 10, is the current guess.
- Why the KVM agent opens the connection to the management server, and not the other way round: no source found yet; the researcher looks in design pages and old threads before any article states a reason.

## Changelog

- 2026-10-02: wording fix (main session, from 03's research, A2, accepted by the user): the business "gets the bill" only where the operator charges (usage accounting is an optional server, and the university's tenants are departments).
- 2026-10-02: wording fix (main session, from the audit of 01.Virtual-Machines, A6): the virtual brand's mapping said "neighbours can't see each other", which is false for VMs on one network; now "neighbours are kept apart". No decision changed.
- 2026-10-01: approved by the user (main session): Candidate A, the cloud kitchen, chosen; the module map approved as proposed, 11 optional; the lab at the end of 01.General; one exercises article per module; all the template changes in §5. hub.docker.com deferred. The home page and CLAUDE.md updated to match.
- 2026-10-01: first proposal (strategist): eleven traits with evidence, a module map of ten modules plus one optional, two analogy candidates (the cloud kitchen, recommended; one Linux machine, scaled up) with five dropped pictures, voice and template changes, lessons from the first attempt, and decisions for the user.
