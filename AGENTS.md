# Ignite Shorts workspace

- All new Ignite Shorts code, configuration, prompts, artwork copies, episodes,
  downloads, tests and renders belong under `workflow/`.
- Start with `workflow/README.md`. The canonical CLI is
  `python3 workflow/scripts/shorts.py` from this repository root.
- `Ignite Website` is a read-only source. Never write into that repository.
- Preserve episode edits and downloaded files. Prepare is non-destructive;
  flag differing filename collisions before moving or replacing files.
- Shared defaults are 30-second, 9:16 painted Ignite shorts with MoGoFun
  Cub (Female) off-screen narration. Existing episode overrides are preserved.
- The old generator path and `Music` are compatibility links. Actual files
  live inside `workflow/`; do not put new work into vendor or legacy paths.
- Do not commit credentials, caches or downloaded/generated media.
