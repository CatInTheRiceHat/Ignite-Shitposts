# Shared Remotion engine and episode content — 2026-11-13

The current layout separates reusable rendering code from episode content:

- `workflow/remotion/`: shared components, schema, renderer, tools, tests,
  TypeScript settings, npm manifest, lockfile and one dependency install.
- `workflow/episodes/zipper_demo/`: the unchanged `edit.json`, `public/` assets,
  `renders/` and prior outputs now preserved in `renders/remotion/`.
- `workflow/episodes/sol_kling_test/remotion/`: custom lantern composition and
  its exact media verification, using the shared engine's dependencies.

The generic renderer accepts an episode name or edit JSON path. It reads
assets from that episode's `public/` and writes outputs to its `renders/`.
The shared root no longer imports or defaults to zipper. A neutral 30-second
starter lives at `workflow/templates/remotion-episode.json`.

`before.json` inventories original files and symlinks, excluding dependencies,
caches, environment files, OS metadata, vendor and historical migration records.
`original-text/` preserves changed source and instructions. `retired/` keeps
obsolete per-episode package manifests and the zipper TypeScript wrapper.
Whole-directory moves preserve media; no differing destination existed.

The [earlier episode-local move](../workspace-2026-11-13-remotion/README.md)
and [initial consolidation](../workspace-2026-11-13/README.md) remain historical.
See `moves.json` and `verification.json` for the current move and checks.
