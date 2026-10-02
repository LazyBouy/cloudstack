# CloudStack from the Ground Up

A free, beginner-friendly course on how Apache CloudStack works and *why* it's built the way it is. The code is the source of truth: explanations link to the exact lines of CloudStack code this repository pins, and show them.

Browse the course's Markdown sources in [`00.Learn/`](https://github.com/LazyBouy/cloudstack/tree/learn/00.Learn), starting with its [home page](https://github.com/LazyBouy/cloudstack/blob/learn/00.Learn/README.md). The course is being written; for now it's served as a website only on the author's machine.

## How this repository is organized

This is a fork of [Apache CloudStack](https://github.com/apache/cloudstack).

- **`learn`** holds the course in `00.Learn/`. CloudStack's own code is never modified here; `learn` is kept current by merging in upstream changes.
- **`main`** is an untouched mirror of upstream `apache/cloudstack`.

For CloudStack itself (what it is, how to build it, how to contribute upstream), see the upstream [README](https://github.com/apache/cloudstack/blob/main/README.md).
