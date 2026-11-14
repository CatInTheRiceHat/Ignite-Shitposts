# Ignite creative guidelines

Read these before writing or generating an episode:

1. [Script guide](video-script-guide.md): conversational skits, complete
   explanations, Sol/Narrator labels, scene descriptions, dialogue density,
   timing and script review.
2. [Style guide](video-style-guide.md): painted art direction, colors,
   pacing, motion, type and visual review.
3. [Shot integration and Sol](shot-integration-and-sol.md): explicit first
   and last frames, varied clip lengths, continuity, character constraints,
   keyframes, animation and assembly.

Use the [workflow guide](../README.md) for commands and file locations, the
[templates](../templates/) for starting files, and the
[episode index](../episodes/README.md) for an existing edit's source.

## Defaults and episode overrides

New shorts start with a **30-second target, 9:16, painted 2D**. New skits
use the style guide's cast: **Narrator / Arthur** off-screen and **Sol /
Cub (Female)**, with Sol remaining mouthless. Existing single-voice Cub
episodes and explicit episode overrides retain their assignments.
Keep speech at its normal generated rate and **1× playback**. Use fuller
connected dialogue when the subject needs it and state when a draft runs
longer. Time the final edit to the actual recordings and visible actions.
Shared production settings live in [config/](../config/).

Review scripts must label every spoken turn and describe each clip's setting,
first frame, action, and last frame. Vary clip lengths according to what
happens; several dialogue lines can share the same clip. Resolve the scene
through Sol's understanding or action, without adding a slogan ending.
Specify camera height and angle, shot size, composition, subject scale, and
the start and end of camera moves. Use emphatic cartoon acting within the
painted 2D style. Sol's two dark eye shapes may intentionally morph to show
emotion; name those shapes, gaze targets, body poses, and change cues in the
plan. Preserve his mouthless face and recognizable flame design.

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
