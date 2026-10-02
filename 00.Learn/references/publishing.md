# Publishing the blog

The contents of `00.Learn/` are built into a website with [MkDocs](https://www.mkdocs.org/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/). It's served in two places: on the author's machine, at <http://localhost:8000/>, by a small git-ignored local server; and publicly on GitHub Pages, at <https://lazybouy.github.io/cloudstack/>, since 2026-10-02. This page explains how the site is built, how to preview and check it, how it's published, and what per-post access control would take. It lives in `references/`, so, like the base instruction and the reference list, it is **not** part of the site.

## How it works

| Piece | File | Job |
|---|---|---|
| Site config | [`mkdocs.yml`](../../mkdocs.yml) | Builds the site from `00.Learn/`, leaving out `references/`, the diagram sources and their manifests (`exclude_docs`). `site_url` comes from `SITE_URL` (default `http://localhost:8000/`); the 404 page needs it for its stylesheets |
| Build tools | [`.github/blog-requirements.txt`](../../.github/blog-requirements.txt) | Pinned versions of MkDocs; the Material theme; the extension that renders `> [!TIP]` callout boxes; `awesome-nav` (navigation order and section titles); and `glightbox` (click an image to open it full-screen, with zoom) |
| Build image | [`.github/docker/blog.Dockerfile`](../../.github/docker/blog.Dockerfile) | The `cloudstack-blog` image with those tools, so nothing is installed on the host. Its build context is `.github/`, and [`.github/.dockerignore`](../../.github/.dockerignore) lets only the requirements file in |
| Strict build | [`.github/scripts/build-site.sh`](../../.github/scripts/build-site.sh) | `mkdocs build --strict` in that image, plus a guard against links into `references/` |
| Local server | `.github/local/` (git-ignored) | Serves the site on this machine and rebuilds it whenever a post changes. Its own `README.md` explains it |
| Diagrams | [`.github/scripts/render-diagrams.sh`](../../.github/scripts/render-diagrams.sh), [`check-diagrams.sh`](../../.github/scripts/check-diagrams.sh) | Each diagram's Mermaid source lives in a module's `diagrams/` folder as `NN-name.mmd`. The render script turns it into `NN-name.png` using the Mermaid CLI in Docker, and records the source's checksum in `diagrams/manifest.sha256`. The check script fails if a PNG is missing or older than its source |
| Navigation | [`00.Learn/.nav.yml`](../.nav.yml) and one `.nav.yml` per module | Sorts pages and folders together by their numbers (by default MkDocs lists folders last), and gives each module a sidebar title such as "01 · General" |
| Repo landing page | [`.github/README.md`](../../.github/README.md) | What visitors see on the fork's GitHub page. GitHub shows `.github/README.md` ahead of the upstream `README.md`, so no upstream file is touched |

Each folder's `README.md` becomes that section's landing page, and the navigation follows the numbered folder and file names. So a new module is a new numbered folder (for example `02.Management-Server/`) holding a `README.md`, plus a one-line `.nav.yml` with its sidebar title (`title: "02 · Management Server"`).

Posts show diagrams as images (`![description](diagrams/NN-name.png)`), not as inline Mermaid, so readers can click them to enlarge. Only the PNGs are published.

These checks stop a broken site from being served:

- `mkdocs build --strict` turns every warning into a failure: broken links between posts, and links to anchors that don't exist. The local server uses the same strict build, and keeps the previous build up when one fails.
- A small `grep` in `build-site.sh` fails if any post **links into `references/`**, since those links would be dead on the site. MkDocs itself only logs such links as information, so it can't catch them.
- `.github/scripts/check-diagrams.sh` fails if a diagram's source was changed without re-rendering its PNG.
- `.github/scripts/readability.py --check` fails a post that's too dense: too many defined terms for its strategy entry's budget, or too much bold, code or inline code per 1,000 words.

MkDocs is pinned to 1.6.x on purpose. The Material theme's authors warn that MkDocs 2.0 is incompatible with it, and the build prints that warning every time. It's expected and harmless while the pin is in place.

## Previewing locally

Everything runs in Docker containers, so nothing is installed on your machine. Run these from the repository root.

### The local server (author's machine only)

`.github/local/serve.sh` serves the site at <http://localhost:8000/> and rebuilds it within a second or two of saving a post. `--detach` keeps it running in the background, `logs` follows its build messages, and `stop` stops it. It's git-ignored, so it isn't in the repository; its own `README.md` explains it. It uses port 8000 because a CloudStack management server run from source takes 8080.

### Quick preview with live reload

```sh
docker build -t cloudstack-blog -f .github/docker/blog.Dockerfile .github   # once, and after changing blog-requirements.txt

# Live preview at http://127.0.0.1:8001/ that refreshes the browser by itself.
docker run --rm -p 8001:8000 -e SITE_URL=http://localhost:8001/ -v "$PWD":/docs cloudstack-blog serve -a 0.0.0.0:8000
```

### The checks

```sh
.github/scripts/build-site.sh "$SP/site"   # strict build + the references/ guard
.github/scripts/check-diagrams.sh          # every diagram's PNG is current
.github/scripts/check-lists.py             # lists that would render as run-on text on the blog
.github/scripts/check-lists.py --site "$SP/site"
.github/scripts/check-excerpts.py          # code excerpts and links match the pinned code (offline)
.github/scripts/readability.py --check     # concept, code and inline-code density per post
.github/scripts/reading-time.py --check --max 30   # every header's reading time matches the rule; 30 minutes at most
```

To (re-)render diagrams after editing their `.mmd` sources:

```sh
.github/scripts/render-diagrams.sh                                         # all diagrams
.github/scripts/render-diagrams.sh 00.Learn/01.General/diagrams/NN-name.mmd   # just one
.github/scripts/check-diagrams.sh
```

## Publishing on GitHub Pages

The public site, <https://lazybouy.github.io/cloudstack/>, is the strictly built site of the committed `learn` branch, served by GitHub Pages from the fork's `gh-pages` branch.

```sh
.github/scripts/publish-pages.sh --dry-run   # build it, show what would be published
.github/scripts/publish-pages.sh             # build it and push it to gh-pages
```

- **Only when the user asks.** Publishing makes every page public. The guard blocks the agents from the script.
- **From committed content.** The script refuses to run with uncommitted changes in `00.Learn/` or `mkdocs.yml`, so the site always matches a commit, named in the `gh-pages` commit message.
- **One build, one commit.** `gh-pages` holds only the latest build (with `.nojekyll`, so GitHub serves the files as they are); each publish force-pushes over the last one.
- **Set up once, by the user:** the repository's Settings → Pages → "Deploy from a branch", branch `gh-pages`, folder `/ (root)`. GitHub runs its own `pages-build-deployment` step to serve the branch.
- `SITE_URL` (in `mkdocs.yml`) is set to the Pages address for this build, so the 404 page finds its stylesheets.

## Per-post access control, later

Nothing here depends on where the site is served: it's a folder of static files. To put it on the internet with per-post access control, as the sister OpenStack course does, copy that project's setup (`/root/projects/openstack/openstack/`, its `references/publishing.md` explains every step):

1. **Access, build half:** its `.github/cloudflare/access_hook.py`, registered under `hooks:` in `mkdocs.yml`, with `extra.access.default: [members]`. Posts here carry no `access:` marking yet, so every post starts **restricted**, and only those the user marks `access: public` become readable by everyone. No post needs changing first.
2. **Access, serving half:** its Cloudflare Worker, `wrangler.jsonc`, grants script, end-to-end tests and the `wrangler` image.
3. **A deploy workflow**, run by hand, checking out only `00.Learn`, `.github` and `mkdocs.yml`.
4. **The pipeline's rules** come back too: the agents never change `access:`, and the report asks the user whether to make a post public.

One CloudStack-specific catch: this fork also carries upstream's own GitHub workflows (`build.yml`, `rat.yml` and others), which run on pushes to `main` once Actions are enabled. Disable those workflows individually before enabling Actions for a deploy workflow.

## What "excluded" does and doesn't mean

`references/` is kept **off the site**. On its own that doesn't make it private: anyone who can see the repository can open `00.Learn/references/`, including the course's strategy (`references/strategy/`) and the archived first attempt (`references/archive/`). The working files of the article pipeline (`references/articles/`, `references/archive/*/working/`) and the agents' handoffs (`references/handoff/`) are git-ignored, so they never leave this machine.
