# Ignite creative guidelines

Read these before writing or generating an episode:

1. [Script guide](video-script-guide.md): audience, hook, setup, reveal,
   payoff, narration and script review.
2. [Style guide](video-style-guide.md): painted art direction, colors,
   pacing, motion, type and visual review.
3. [Shot integration and Sol](shot-integration-and-sol.md): shot planning,
   continuity, character constraints, keyframes, animation and assembly.

Use the [workflow guide](../README.md) for commands and file locations, the
[templates](../templates/) for starting files, and the
[episode index](../episodes/README.md) for an existing edit's source.

## Defaults and episode overrides

New shorts default to **30 seconds, 9:16, painted 2D, off-screen MoGoFun Cub
(Female)** narration. Keep speech at its normal generated rate and 1×
playback. Time the edit to the actual recording and leave room for reveals.
Shared production settings live in [config/](../config/).

| Renderer | Format | Existing episodes |
| --- | --- | --- |
| Python/FFmpeg via `scripts/shorts.py` | 720 × 1280, 30 fps | Calculus pilot: 15 seconds |
| Shared engine in `remotion/`, with episode-owned edits/assets | 1080 × 1920, 30 fps | Zipper demo: 20 seconds; Sol lantern test: 4 seconds |

Preserve an episode's intentional duration, format, narrator and edit.
These guides describe the common creative approach; the episode files hold
its exact settings. The template currently models the calculus sequence,
so adapt the script and shot plan deliberately for another topic.
The neutral [Remotion starter](../templates/remotion-episode.json) provides
hook, setup, reveal and payoff placeholders without a topic-specific script
or shot plan. Replace its shared reference background with episode artwork.

Reference artwork lives in [assets/](../assets/README.md). The upstream
generator in `vendor/` contains a different 3D style; use these Ignite guides
for painted production.
