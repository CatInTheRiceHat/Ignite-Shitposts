# Ignite Shorts

All production files live in **[workflow/](workflow/README.md)**.

| What you need | Where to go |
| --- | --- |
| Production steps and CLI commands | [Workflow guide](workflow/README.md) |
| Script, visual style, shot planning and Sol rules | [Creative guidelines](workflow/guidelines/README.md) |
| Existing episodes and their renderers | [Episode index](workflow/episodes/README.md) |
| Shared artwork, fonts and music | [Asset index](workflow/assets/README.md) |
| Remotion Studio, editing and rendering | [Remotion project](workflow/remotion/README.md) |

From this repository root:

```bash
python3 workflow/scripts/shorts.py prepare my_next_short
python3 workflow/scripts/shorts.py check calculus_pilot
```

New episodes default to 30 seconds, painted 9:16 and off-screen Cub (Female)
narration. Existing episode overrides are preserved. The root `music/` and
`zack-d-films-ai-video-generator/` links keep older paths working; use the
canonical folders under `workflow/` for new work.

The [workspace move record](workflow/migration/workspace-2026-11-13/README.md)
lists previous locations and preservation checks.
