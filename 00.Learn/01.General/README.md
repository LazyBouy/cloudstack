# 01 · General: The Big Picture

What is CloudStack, and what happens when someone asks it for a virtual machine? This module answers that, one question per article, starting from what a virtual machine is.

It ends with a cloud of your own to look at: first a simulated one, then a small real one on a single Ubuntu machine. You need basic Linux (the shell, files, packages, services, SSH) and nothing else.

## What you'll be able to do

- Explain what a virtual machine (VM) is, how a hypervisor runs it, what a cloud adds on top, and why that needs one program in charge.
- Name each part of a CloudStack cloud, say what it's for, and where it runs.
- Explain why where a VM's disk lives, and how servers are grouped, decide where a VM can run, move and restart.
- Say who may ask the cloud for what.
- Follow one request for a VM, step by step, from the moment it's sent to a running VM.
- Run a simulated cloud, then build a one-machine cloud on Ubuntu, and find each part in it.

## Reading order

Read the articles in order: each one builds on the ones before it.

### Foundations

What a virtual machine is, how a hypervisor runs it, and what a cloud adds.

| # | Article | Level | Reading time |
|---|---|---|---|
| 01 | [What Is a Virtual Machine, and What Runs It?](01.Virtual-Machines.md) | Beginner | about 10 minutes |
| 02 | [How Does a Hypervisor Work?](02.Hypervisors.md) | Beginner | about 15 minutes |
| 03 | [What Does a Cloud Add to Virtual Machines?](03.What-A-Cloud-Adds.md) *(coming soon)* | Beginner | about 15 minutes |

### Asking the cloud

How a request reaches CloudStack, and who may make it.

| # | Article | Level | Reading time |
|---|---|---|---|
| 04 | [How Do You Ask CloudStack for Something?](04.API-And-Database.md) *(coming soon)* | Beginner | about 15 minutes |
| 05 | [Who May Ask the Cloud for What?](05.Accounts-And-Roles.md) *(coming soon)* | Beginner | about 15 minutes |

### The machines underneath

Hosts, disks, how hosts are grouped, images, CloudStack's own VMs and networks.

| # | Article | Level | Reading time |
|---|---|---|---|
| 06 | [How Does CloudStack Talk to a Host?](06.Talking-To-Hosts.md) *(coming soon)* | Beginner | about 15 minutes |
| 07 | [Where Does a VM's Disk Live?](07.Where-Disks-Live.md) *(coming soon)* | Beginner | about 15 minutes |
| 08 | [Which Hosts Can a VM Move Between?](08.Clusters.md) *(coming soon)* | Beginner | about 15 minutes |
| 09 | [How Does CloudStack Map a Data Centre?](09.Zones-And-Pods.md) *(coming soon)* | Beginner | about 12 minutes |
| 10 | [Where Do New VMs Come From?](10.Templates.md) *(coming soon)* | Beginner | about 15 minutes |
| 11 | [Why Does CloudStack Run VMs of Its Own?](11.System-VMs.md) *(coming soon)* | Beginner | about 12 minutes |
| 12 | [How Does a VM Get onto a Network?](12.Guest-Networks.md) *(coming soon)* | Beginner | about 15 minutes |

### The whole journey

One request, followed through every part.

| # | Article | Level | Reading time |
|---|---|---|---|
| 13 | [What Happens When Someone Asks for a VM?](13.Journey-Of-A-VM.md) *(coming soon)* | Beginner | about 20 minutes |

### Your own cloud

A simulated cloud first, then a small real one on one Ubuntu machine.

| # | Article | Level | Reading time |
|---|---|---|---|
| 14 | [Can You Try CloudStack Without Real Servers?](14.Lab-Simulator.md) *(coming soon)* | Beginner | about 15 minutes |
| 15 | [What Does One Machine Need to Run CloudStack?](15.Lab-Preparing-A-Machine.md) *(coming soon)* | Intermediate | about 20 minutes |
| 16 | [How Does One Machine Become a Working Cloud?](16.Lab-Building-The-Cloud.md) *(coming soon)* | Intermediate | about 20 minutes |

### Exercises

Check that the big picture holds.

| # | Article | Level | Reading time |
|---|---|---|---|
| 17 | [Exercises: The Big Picture](17.Exercises.md) *(coming soon)* | Beginner–Intermediate | about 20 minutes |
