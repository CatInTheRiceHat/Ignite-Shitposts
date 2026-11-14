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
Higgsfield custom voice Sol**, with Sol remaining mouthless. Exact voice
settings live in the [shared voice cast](../workflow/config/voices.json).
Existing single-voice Cub
episodes and explicit episode overrides retain their assignments.
Keep speech at its normal generated rate and **1× playback**. Use fuller
connected dialogue when the subject needs it and state when a draft runs
longer. Time the final edit to the actual recordings and visible actions.
Shared production settings live in [config/](../config/).

Review scripts must label every spoken turn and describe each clip's setting,
first frame, action, and last frame. Vary clip lengths according to what
happens; several dialogue lines can share the same clip. Resolve the scene
through Sol's understanding or action, without adding a slogan ending.
Deliver the dialogue and shot directions together in one complete episode
document. Keep subject-specific dialogue, timing and asset paths
in that episode folder.
The default production flow is generated first/last stills, complete
Higgsfield clips, then simple assembly with voices, captions and sound.
Cutaways are generated cartoon scenes too. Do not add SVGs, custom diagrams
or separate mechanism animation unless the user explicitly requests them.
Save a separate prompt text file alongside it. For **N scenes**, provide
exactly **2N image prompts** (first and last frame for each scene) and **N
video prompts** (the continuous motion between each pair). Use matching
scene IDs and keep reference inputs and settings outside the copyable text.
Specify camera height and angle, shot size, composition, subject scale, and
the start and end of camera moves. Use emphatic cartoon acting within the
painted 2D style. Sol's two dark eye shapes may intentionally morph to show
emotion; name those shapes, gaze targets, body poses, and change cues in the
plan. Preserve his mouthless face and recognizable flame design.
When the Narrator addresses Sol on screen, give Sol an upward glance toward
the voice just above the camera, breaking the fourth wall. Cue that look in
the script, then let him follow the demonstrated object. A new reply may
cue a new glance; avoid repeated reaction loops within one answer.

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
