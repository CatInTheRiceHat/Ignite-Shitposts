# Ignite creative guidelines

Read these before writing or generating an episode:

Start with [Elaine's critique checklist](checklist.md), the running record of
her current feedback. Read it before each prompt or media review and update it
when she gives new critiques. Her later clarifications take precedence over
older examples or acting suggestions.

Current video default for all active clients: **Gemini Omni Flash 1.2**
(`gemini_omni_flash_1_2`), from `../config/generation.json`. Generate first and
last stills, show BOTH to the user and wait for explicit approval before any
video. Follow [the reviewer workflow](clip-review-guide.txt). Each paired-frame
video must be 3–10 seconds; declare longer scenes as continuing subscenes.

1. [Script guide](video-script-guide.md): conversational skits, complete
   explanations, Sol/Narrator labels, scene descriptions, dialogue density,
   timing and script review.
2. [Style guide](video-style-guide.md): painted art direction, colors,
   pacing, motion, type and visual review.
3. [Shot integration and Sol](shot-integration-and-sol.md): explicit first
   and last frames, varied clip lengths, continuity, character constraints,
   keyframes, animation and assembly.
4. [Image prompt template](image-prompt.md): clean, accurate scene art,
   reference roles and compatible first/last frames.
5. [Video prompt template](video-prompt.md): one clear action, preserved
   geometry and the established painted finish.

Use the [workflow guide](../README.md) for commands and file locations, the
[templates](../templates/) for starting files, and the
[episode index](../episodes/README.md) for an existing edit's source.

## Defaults and episode overrides

New shorts start with a **30-second target, 9:16, painted 2D**. New skits
use the style guide's cast: **Narrator / Arthur** off-screen and **Sol /
Higgsfield custom voice Sol**, with Sol remaining mouthless. Exact voice
settings live in the [shared voice cast](../config/voices.json).
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
the start and end of camera moves. Use Mascot.png and the supplied mascot examples for Sol's identity; read
../config/sol-references.json. Keep the accepted painted finish. Use the lantern
video for gentle movement, and keep the original mascot eyes, flame layers,
outline and compact nub limbs. Name gaze targets, restrained body poses and their cues.
Preserve his mouthless face and recognizable flame design.
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
