# Ignite creative guidelines

Read these before writing or generating an episode:

**Start here: [Elaine's current rules](current-rules.md).** One page with everything she has asked for,
sorted by topic, plus the step-by-step way an episode is made. Where it disagrees with the older guides
below (on-twos motion, paired stills, Sol's voice, fixed cameras), the current-rules page wins.

**Sol himself:** use the approved [3D Sol model](sol-3d-model.md) (2026-11-25) as the character reference.
It has the full Sol and a body-only logo version, with turnaround pictures in `sol-3d/`.

Start with [Elaine's critique checklist](checklist.md), the running record of
her current feedback. Read it before each prompt or media review and update it
when she gives new critiques. Her later clarifications take precedence over
older examples or acting suggestions.

Keep shared visual guidance focused on reusable art direction: painted finish,
character identity, motion and visual consistency. Specific scenes, settings,
story beats and episode sound requests belong in that episode's feedback,
script and shot plan. Elaine's scene examples are not shared style requirements.

Current video default for all active clients: **Gemini Omni Flash 1.2**
(`gemini_omni_flash_1_2`), from `../config/generation.json`. Prepare first and
last stills by generating or reusing the specified assets. Show BOTH to the
user and wait for explicit approval before any video. Follow
[the reviewer workflow](clip-review-guide.txt). Each paired-frame
video must be 3–10 seconds; declare longer scenes as continuing subscenes.

1. [Script guide](video-script-guide.md): connected dialogue, distinct visual
   teaching beats, provisional timing and timing to recorded voices.
2. [Style guide](video-style-guide.md): shared matte paint treatment, overall
   motion style, exact on-twos generation targets and editing verification, voices and type.
3. [Shot integration and Sol](shot-integration-and-sol.md): character identity,
   purposeful acting, prop contact, exact frame reuse and clip assembly.
4. [Image prompt template](image-prompt.md): visual simplicity, painted depth,
   supplied reference roles and matching-endpoint construction.
5. [Video prompt template](video-prompt.md): action clarity, intentional camera
   choices, two-frame motion cadence, continuity and removal of irrelevant boilerplate.

Use the [workflow guide](../README.md) for commands and file locations, the
[templates](../templates/) for starting files, and the
[episode index](../episodes/README.md) for an existing edit's source.

## Scope and rule owners

The guides above own their respective rules; link to the owner instead of copying the full policy into every document. Finished prompts still need concise style and applicable identity instructions, since the generator does not read local guides. Use the shared [final prompt review](checklist.md#final-prompt-review) before generation.

The revised [fire episode](../episodes/fire_discovery/higgsfield-prompts.txt) is an example of applying these principles. Its setting, lighting states, gestures, camera percentages, character counts and durations are not educational-video defaults. Requirements from a separate loading animation, including rotation counts, directions, loops or timing, remain scoped to that animation's brief; do not import them into educational shots.

Read current model settings from [generation.json](../config/generation.json) and exact speaker identities from [voices.json](../config/voices.json). Historical episode settings and template examples do not replace newer configuration or the current caption styling in the style guide. Writing or reviewing prompts does not authorize image, video or audio generation.

## Defaults and episode overrides

[Narrator attention](shot-integration-and-sol.md#narrator-attention-and-listening-idle) is mandatory: visible Sol looks up before each Narrator turn and maintains the gaze with gentle idle while the voice speaks. Every review includes the actual script and speaker cues; final speech alignment uses real normal-rate recordings.

The [motion style owner](video-style-guide.md#motion-style) specifies animation on twos: each source pose/state held for two consecutive frames at final 30 fps, 15 updates per second and normal playback. Elaine’s latest preference adds small bouncy flame-like body/tip follow-through to Sol’s intentional movements, settling at each endpoint; it supersedes the earlier rigid-body/no-bounce defaults. A brief natural blink is now allowed, returning to the original open navy ovals. Exact cadence, normal eye design and the ban on independent face turns remain. Smooth editorial digital pushes may follow stepped source footage, with crop checks throughout. Exact cadence must be enforced and verified on actual footage during editing.

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
The default production flow is prepared first/last endpoints, complete
Higgsfield clips, then simple assembly with voices, captions and sound.
Cutaways are generated cartoon scenes too. Do not add SVGs, custom diagrams
or separate mechanism animation unless the user explicitly requests them.
Save a separate prompt text file alongside it. For **N scenes**, provide
exactly **2N image endpoint entries** (first and last frame for each scene) and **N
video prompts** (the continuous motion between each pair). Use matching
scene IDs and keep reference inputs and settings outside the copyable text.
Label exact endpoint reuse instead of requiring duplicate image generations.
Use the [shot guide](shot-integration-and-sol.md) for camera, identity, acting,
scripted acknowledgment and continuity; the [image guide](image-prompt.md) for actual
supplied references; and the [style guide](video-style-guide.md) for paint and
motion. The critique checklist retains frame-specific acceptance history;
it does not turn a previous episode's staging into a shared default.

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
