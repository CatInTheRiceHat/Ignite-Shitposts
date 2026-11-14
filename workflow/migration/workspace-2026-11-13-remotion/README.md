# Episode-local Remotion projects — 2026-11-13

The zipper project's source, configuration, public assets, tools and working
outputs moved from `workflow/remotion/` into
`workflow/episodes/zipper_demo/remotion/`. The Sol lantern composition remains
in `workflow/episodes/sol_kling_test/remotion/` and now resolves its own project
configuration rather than depending on the zipper project.

One shared npm workspace lives at `workflow/episodes/`: `package.json`,
`package-lock.json`, `tsconfig.remotion.json` and the ignored `node_modules/`
install. Each episode has its own small package manifest and commands. The
existing dependency installation was moved intact. The updated lockfile adds
the two workspace entries without changing any existing dependency version.

`before.json` records the original file hashes and symlinks, excluding caches,
dependency installs, environment files, OS metadata and compiled Python files.
`original-text/` preserves instructions and source before updating references.
No destination collided with an existing file; no episode edits, clips,
recordings, renders or provider job history were replaced.

See `verification.json` for preservation and local checks. The earlier
[workspace move record](../workspace-2026-11-13/README.md) remains historical;
its `workflow/remotion/` destination has been superseded by this move.
