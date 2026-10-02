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
