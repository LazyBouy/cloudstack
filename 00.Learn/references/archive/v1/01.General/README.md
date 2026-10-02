# Module 01 · General

The big picture of Apache CloudStack: what it is, how it's put together, how a single request travels through it, why every piece exists, and three ways to run it yourself.

## Before you start

- **You need:** basic Linux. You should be comfortable with the shell, files, installing packages, starting services, SSH, and editing config files.
- **You don't need:** any knowledge of clouds, networking, storage, databases, Java or Kubernetes. Everything is explained as we go.
- **For the hands-on posts only:** the simulator and developer-mode posts run on an ordinary computer. The install-by-hand post needs one that can run a couple of virtual machines at once, one of which runs virtual machines itself ("nested virtualization"). The install posts give the exact sizes.

## Reading order

The module has four stages. First we **understand** what CloudStack is and how it moves. Then we **justify** every piece: why it's there and what could replace it. Then we **practise**, to make sure the ideas have stuck. Finally we **build** a real cloud, three different ways.

| # | Post | Level | Type |
|---|---|---|---|
| | **Understand** | | |
| 01 | [What Is CloudStack? A Hotel for Computers](01.Overview.md) | Beginner | Big picture |
| 02 | [Architecture: One Head Office, Many Floors](02.Architecture/README.md), in two parts: [Where Does Everything Live?](02.Architecture/01.Where-Everything-Lives.md) and [Who Calls Whom?](02.Architecture/02.Who-Calls-Whom.md) | Beginner → Intermediate | Big picture |
| 03 | [Inside the Management Server: One Program, Many Plugins](03.Inside-The-Management-Server.md) *(coming soon)* | Intermediate | Big picture |
| 04 | [How It Unfolds: A Cloud Waking Up, and One Request's Journey](04.How-It-Unfolds.md) *(coming soon)* | Intermediate | Big picture |
| | **Justify** | | |
| 05 | [The Foundation Services: Behind the "Staff Only" Door](05.Foundation-Services.md) *(coming soon)* | Intermediate | Big picture |
| 06 | [The control-plane building blocks the whole management server shares](06.Control-Plane-Building-Blocks.md) *(coming soon)* | Intermediate | Big picture |
| 07 | [The core subsystems: compute, network and storage, and what else could do the job](07.Core-Subsystems.md) *(coming soon)* | Intermediate | Big picture |
| | **Practise** | | |
| 08 | [Check-yourself answers](08.Check-Yourself-Answers/README.md) | — | Answers |
| 09 | [Exercises](09.Exercises.md) *(coming soon)* | Mixed | Exercises |
| 10 | [Exercise solutions](10.Exercise-Solutions.md) *(coming soon)* | — | Answers |
| | **Build** | | |
| 11 | [Install by hand, in several parts](11.Install-By-Hand/README.md) *(coming soon)* | Intermediate | Hands-on |
| 12 | [Try it in minutes: the CloudStack simulator](12.Try-The-Simulator.md) *(coming soon)* | Beginner | Hands-on |
| 13 | [Build from source and run it in developer mode](13.Build-From-Source.md) *(coming soon)* | Intermediate | Hands-on |
