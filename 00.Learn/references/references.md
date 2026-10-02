# References

Approved sources for the learning material in `00.Learn/`. Every host in the tables below is allowed for WebFetch in [`.claude/settings.json`](../../.claude/settings.json). To add a source, add it both here and there.

**How to weigh them.** The code is the source of truth. Design pages, pull requests and mailing-list threads explain why a design was chosen, the docs explain how things are meant to be used, and blogs give context. Check any claim against the code.

## The code (source of truth)

| Source | Use it for |
|---|---|
| This repository, at the commit the course pins (`.github/scripts/pinned.py`) | Reading CloudStack's code exactly as the posts quote it. Release tags such as `4.22.1.1` are here too, after `git fetch upstream --tags` |
| https://github.com/apache/cloudstack | Browsing the code and its history online; the permalinks in the posts point here |
| https://github.com/apache/cloudstack/pulls | Pull requests: the discussion behind each change, often including why it was done that way. Use `api.github.com` for the full conversation of one PR, and `raw.githubusercontent.com` for single files at a commit |
| https://github.com/apache/cloudstack/issues | Bug reports and feature requests since the project moved to GitHub issues |
| https://issues.apache.org/jira/projects/CLOUDSTACK | The older JIRA issue tracker: the history behind many long-standing features |

Other Apache CloudStack repositories (the documentation sources, CloudMonkey, the Kubernetes provider and others) are cited as ordinary links. Code excerpts and pinned links come only from apache/cloudstack.

## Design rationale

| Source | Use it for |
|---|---|
| https://cwiki.apache.org/confluence/display/CLOUDSTACK/Home | The project wiki (Confluence): design documents and community notes, from release plans to how-tos |
| https://cwiki.apache.org/confluence/display/CLOUDSTACK/Design | The wiki's design documents and functional specifications for features: the problem, the proposed design and the alternatives considered |
| https://cloudstack.apache.org/mailing-lists | The mailing lists (users, dev, and others), where developers discuss designs and releases and users get support: how to join, and links to the archives |
| https://lists.apache.org/list.html?dev@cloudstack.apache.org | The developers' list archive. The page is a JavaScript app: for WebFetch, use its `/api/` endpoints (for example `https://lists.apache.org/api/stats.lua?list=dev&domain=cloudstack.apache.org`) |
| https://github.com/apache/cloudstack-documentation | The source of the official docs, open to pull requests. Its history and pull requests show when, and often why, a page changed |

## Official documentation

The docs are versioned. The **4.22.1.1** pages describe the LTS release the install posts use; **latest** is currently 4.23.0.0, the newest release (the pinned code is newer still: 24.0.0-SNAPSHOT). Every guide below exists under both, at the same path: swap `4.22.1.1` and `latest` in the URL.

| Source | Use it for |
|---|---|
| https://docs.cloudstack.apache.org/en/4.22.1.1/ | The docs for CloudStack 4.22.1.1: concepts, the quick and full installation guides, upgrading, and the guides below |
| https://docs.cloudstack.apache.org/en/latest/ | The newest docs (4.23.0.0 today), for features the pinned code has and 4.22 doesn't |
| https://docs.cloudstack.apache.org/en/4.22.1.1/adminguide/index.html | The Usage Guide: operating a cloud (accounts and domains, offerings, networking, instances, templates, hosts, storage, system VMs, usage). It includes the [Provisioning and Authentication API](https://docs.cloudstack.apache.org/en/4.22.1.1/adminguide/api.html) chapter (user data, metadata, config drive) |
| https://docs.cloudstack.apache.org/en/4.22.1.1/developersguide/index.html | The Developers Guide: [building from source, the simulator and building packages](https://docs.cloudstack.apache.org/en/4.22.1.1/developersguide/developer_guide.html), [storage plugins](https://docs.cloudstack.apache.org/en/4.22.1.1/developersguide/plugins.html), [custom host and storage-pool allocators](https://docs.cloudstack.apache.org/en/4.22.1.1/developersguide/alloc.html), and a worked [Ansible deployment](https://docs.cloudstack.apache.org/en/4.22.1.1/developersguide/ansible.html) |
| https://docs.cloudstack.apache.org/en/4.22.1.1/developersguide/dev.html | The Programmer Guide: using the API (API and secret keys, the request format and how requests are signed), event types and time zones |
| https://cloudstack.apache.org/api/ | The API reference, one per version, at `https://cloudstack.apache.org/api/apidocs-<major.minor>/`: every command, its parameters and its response. Use [`apidocs-4.22`](https://cloudstack.apache.org/api/apidocs-4.22/) for the install posts and [`apidocs-4.23`](https://cloudstack.apache.org/api/apidocs-4.23/) for the newest release; old ones such as [4.11](https://cloudstack.apache.org/api/apidocs-4.11/) and [4.14](https://cloudstack.apache.org/api/apidocs-4.14/) are still online, for history. The pinned code is the final word on anything newer |
| https://cloudstack.apache.org/downloads | Every current release, which ones are LTS and how long each is supported; the signed source releases and how to verify them; the CloudMonkey binaries; the community packages |
| https://cloudstack.apache.org/ | The project's website: news, history, who uses it |

## Releases and packages

| Source | Use it for |
|---|---|
| https://dlcdn.apache.org/cloudstack/ | The signed source releases of the current versions (`releases/<version>/`), with their `.asc` signatures and `.sha512` checksums, and the [`KEYS`](https://dlcdn.apache.org/cloudstack/KEYS) file to check them against |
| https://archive.apache.org/dist/cloudstack/ | Every older release, for history |
| https://github.com/apache/cloudstack-cloudmonkey/releases | CloudMonkey (`cmk`, the command-line client) binaries, built by the community from the official source releases |
| https://download.cloudstack.org/ | The community package repositories the install posts use: DEB (`ubuntu/`) and RPM (`el/`, `suse/`) packages, ARM64 builds, system VM templates (`systemvm/`) and Kubernetes Service ISOs (`cks/`) |
| https://hub.docker.com/r/apache/cloudstack-simulator | The simulator's Docker image (`apache/cloudstack-simulator`), approved by the user on 2026-10-01 only to check which release tags exist (the JSON at `https://hub.docker.com/v2/repositories/apache/cloudstack-simulator/tags`). The image itself is documented in the repository, `tools/docker/README.md` |
| https://documentation.ubuntu.com/server/ | The Ubuntu Server documentation, approved by the user on 2026-10-01 only for the KVM lab's Ubuntu facts (netplan, NFS, MySQL and services on Ubuntu 24.04 LTS) that CloudStack's own docs leave unstated |
| https://ubuntu.com/server/docs/ | The Ubuntu Server documentation's new address: documentation.ubuntu.com/server/ now redirects here (301, checked 2026-10-02). Approved by the user on 2026-10-02 for the KVM lab's Ubuntu facts and article 01's `kvm-ok` check, and widened the same day to the KVM stack (KVM, QEMU, libvirt) as installed on Ubuntu 24.04 LTS, for article 02 onwards |
| https://manpages.ubuntu.com/ | Ubuntu's manual pages, approved on 2026-10-01 for the same purpose: the exact behaviour of a command or configuration file on Ubuntu 24.04 LTS |
| https://dev.mysql.com/doc/ | The MySQL Reference Manual, approved on 2026-10-01 only for the lab's MySQL facts (the version Ubuntu installs, the root login, `server_id`) |

## Blogs

More will be added as the project goes on.

| Source | Use it for |
|---|---|
| https://cloudstack.apache.org/blog | The project's own blog: release announcements and feature articles |
| https://www.shapeblue.com/blog/ | Technical articles by ShapeBlue, a company whose engineers write much of CloudStack. Often the clearest explanation of a feature, but a vendor's blog: check its claims against the code |

## Standards

| Source | Use it for |
|---|---|
| https://csrc.nist.gov/pubs/sp/800/145/final | NIST SP 800-145, "The NIST Definition of Cloud Computing": the five essential characteristics of a cloud |
| https://nvlpubs.nist.gov/ | NIST's final publications (the PDFs that csrc.nist.gov's pages link to), approved by the user on 2026-10-02 only for NIST's final texts, such as SP 800-125A Rev. 1 and NISTIR 8221, so articles quote finals rather than drafts |
| https://docs.kernel.org/virt/kvm/ | The Linux kernel's own KVM documentation (`virt/kvm/api.html`, the KVM API): how QEMU and KVM hand control to each other, virtual processors as threads, guest memory. Approved by the user on 2026-10-02 |
| https://libvirt.org/ | libvirt's documentation: the QEMU driver, the domain XML, transient and persistent domains. Approved by the user on 2026-10-02 |
| https://www.qemu.org/docs/ | QEMU's documentation: accelerators (KVM, TCG), device emulation, virtio and vhost. Approved by the user on 2026-10-02 |

## Style model

The user's model for how every post reads: **"the exact style I would like to follow in the CloudStack series"** (2026-10-01). It's a model for form, not a source of facts about CloudStack. The style is summarised in the project memory (`learnkube-style`) and in `CLAUDE.md`'s writing rules.

| Article | What it shows best |
|---|---|
| https://learnkube.com/kubernetes-control-plane | The short map of a whole system: one claim per heading ("The API server is the entry point"), ending in "Read the control plane as a chain reaction" |
| https://learnkube.com/kubernetes-api-explained | Following one request (`kubectl apply`) through every stage, with a picture per stage and a numbered recap of the journey |
| https://learnkube.com/etcd-kubernetes | Why a component was chosen (the requirements first, then the answer), then hands-on: building and breaking a three-node cluster |
| https://learnkube.com/etcd-breaks-at-scale | Limits and alternatives: what breaks at scale, how it's worked around, and the honest practical answer at the end |
| https://learnkube.com/kubernetes-scheduler-explained | Step-by-step picture sequences (32 pictures), misconception busting ("It's not. The controller manager does that."), and scenarios in the user's voice |
| https://learnkube.com/real-time-dashboard | Building something small with the API, one improvement per section |

## Kubernetes (for comparisons)

| Source | Use it for |
|---|---|
| https://kubernetes.io/docs/ | Official Kubernetes docs, to check the Kubernetes side of every "Kubernetes lens" comparison |

## OpenStack (for comparisons)

| Source | Use it for |
|---|---|
| https://docs.openstack.org/ | Official OpenStack docs, to check the OpenStack side of every "OpenStack lens" comparison |
| https://openstack.techphistudio.de/ | The sister course, *OpenStack from the Ground Up*. Link only to its public posts: the rest ask readers to sign in |

## Repositories

- Upstream: https://github.com/apache/cloudstack (the official repository is https://gitbox.apache.org/repos/asf/cloudstack.git; GitHub is its mirror)
- This fork: https://github.com/LazyBouy/cloudstack

## Planned deep dives

Topics promised in published posts, with the sources to start from. Each has a placeholder page, and its promise is tracked in `in_progress_checks.md`.

None yet.
