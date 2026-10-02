# CloudStack from the Ground Up

Most CloudStack tutorials hand you a wall of commands. You copy, you paste, and at the end you have a cloud you don't understand. The first time something breaks, you're stuck, because nobody told you *why* any of those commands were there.

This course goes the other way round. It explains how an Apache CloudStack cloud works, why each piece exists, what else could have done the job, and only then how to build one. And it doesn't take anyone's word for it: **the code is the source of truth.** When a post says "this is what happens", it links to the exact lines of CloudStack code that make it happen, and shows them to you.

## Who this is for

- **You know basic Linux:** the shell, files and permissions, installing packages, starting services, SSH, editing a config file.
- **That's all we assume.** Virtualization, networking, storage, databases, Java: every idea is explained from scratch, with everyday comparisons.
- **If you know Kubernetes,** look for the boxes marked *Kubernetes lens*. They compare CloudStack ideas to Kubernetes ones. If you don't, skip them; you won't miss anything you need.
- **If you know OpenStack,** look for the boxes marked *OpenStack lens*. CloudStack and OpenStack solve the same problem in very different ways, and the comparison often explains why CloudStack looks the way it does. There's a sister course, [OpenStack from the Ground Up](https://openstack.techphistudio.de/), if you want to go further.

## How to read it

- **Every post is labelled** Beginner, Intermediate or Advanced, so you can tell how much it expects of you.
- **Every post ends with "Check yourself"**: a few questions to test your understanding. The answers are on a separate page, so try first.
- **Read the modules in order.** Each builds on the ones before it.

## Which version of CloudStack?

CloudStack has two kinds of release: **LTS** (long-term support) releases, which are supported for two years (all fixes for 18 months, then blocker and security fixes for six more), and regular releases in between. This course uses two reference points:

- **Explanations and code links** use the CloudStack code pinned in this repository: the newest development code, where CloudStack is heading. Each post names the exact commit it was written against.
- **Installation guides** use **CloudStack 4.22**, the current LTS release, which you can install from ready-made packages.

The two are very close. Where they differ in a way that matters, the post tells you.

## Modules

| Module | What you'll learn |
|---|---|
| [01 · General](01.General/README.md) | The big picture: what CloudStack is, how it's put together, how a request flows through it, why each piece exists, and three ways to run it yourself |

## Where the course is going

Module 01 gives you the whole picture. The modules after it take one part of CloudStack at a time and go deep, from how it's designed to how you'd change it. The plan, which will grow as we go:

- **Inside the management server:** the API, async jobs, plugins and the database layer, in depth
- **Compute and hypervisors:** the agent on each host, libvirt and KVM, and the other hypervisors
- **Networking:** the virtual router, VPCs, security groups and SDN integrations
- **Storage:** primary and secondary storage, snapshots and the storage plugins
- **System VMs:** the virtual machines CloudStack runs for itself, and why
- **Operating a cloud:** high availability, upgrades, usage records and monitoring
- **Extending CloudStack:** adding an API command, writing a plugin, and contributing upstream
