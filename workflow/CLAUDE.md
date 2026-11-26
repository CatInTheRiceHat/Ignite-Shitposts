# Ignite production instructions for Claude

Current episode: **How Fire Was Discovered**, workflow/episodes/fire_discovery/.
The user changed the story topic; preserve the earlier escalator episode.

Read `workflow/AGENTS.md`, `workflow/README.md` and the linked creative guides
from the repository root. All new work belongs under `workflow/`.

Read `workflow/guidelines/checklist.md` before prompts, generation and review.
Update this shared critique list when Elaine gives new feedback, keeping her
latest clarifications and distinguishing them from technical reviewer findings.

Use the same canonical settings as Codex and the other workspace clients:
`workflow/config/generation.json`. Current Higgsfield video model is
**Gemini Omni Flash 1.2**, ID `gemini_omni_flash_1_2`, mode `image-to-video`,
with user-approved first AND last stills (3–10 seconds per paired-frame clip).
Do not silently use Kling or the preserved calculus Flow integration.

For images use **Nano Banana 2.1**, ID `nano_banana_2_1`, at 2k and 9:16.
Read its settings from the same config. Do not pass GPT-specific `quality`
or `output_format` options. Changing the model does not authorize generation.

For the older paired-stills method only: generate both stills, show BOTH to the
user, wait for explicit approval of that exact pair, then generate the clip.
The Blender-skeleton pipeline below replaces it for current shots.
Keep the choppy on-twos look (each pose held 2 frames at 30 fps; Elaine
reconfirmed 2026-11-25).
Run independent actual-footage review before production use. Read
`workflow/config/sol-references.json`: use Mascot.png and the additional mascot
examples for Sol's design. V4 establishes the accepted identity direction.

**Art direction: painted gouache, NOT Arcane** (Elaine, 2026-11-25: "lets just
keep this painted gouache painting… arcane style is a bit too hard to perfect").
The Arcane trial (options B/C, ink linework) is dropped. Use visible matte
gouache brushwork, layered color and paper texture on Sol and the whole scene,
with no inked outlines, per the supplied graphic examples and
`guidelines/video-style-guide.md`. Elaine also called the first lantern render
"so bland": shots need livelier staging, depth and lighting, not a flat static
layout.

**Pipeline (Elaine, 2026-11-25):** animate a gray Blender skeleton clip, then
give that clip to Higgsfield (Gemini Omni Flash 1.2, mode `edit`, skeleton as
`video_references`, Mascot.png as `image_references`) to render the painted
video. Do not make intermediate stills/photos for this pipeline unless asked.
Sol's identity geometry is unchanged (compact red/orange/cream flame layers,
low navy #1C2447 oval eyes, mouthless face, short rounded arms, tiny stubby feet,
no particles). Keep
the normal original oval eye design unchanged, with a brief natural blink allowed. The frame pair remains unapproved.
Keep every mascot feature consistent across clips, including the original
eyes, short rounded arms and stubby feet; paint must preserve their design.
Never record frame approval on the user's behalf. Preserve all existing media.


## Exact motion policy

Follow workflow/guidelines/video-style-guide.md#motion-style from the repository
root: animate on twos at final 30 fps, holding every source pose/painted state
unchanged for two consecutive frames (15 updates per second) at normal speed.
Longer holds use complete pairs. Apply this to Sol, visible human hands, moving
props, flames and animated local lighting; keep background/texture stable.
No interpolation, blending, optical flow or motion blur concealing the steps.
Use short direct gestures with a small bouncy flame-like body/tip/lobe wobble
and soft follow-through that damps and settles. This latest user preference
supersedes earlier rigid-body/no-bounce defaults. Keep layers and face coherent,
eyes unchanged, limbs stubby and feet supported. Add no unrelated windup,
repeated nodding, endless idle sway, extra hops or camera movement.
Keep Sol's facial markings anchored to his body and eyes uniformly navy #1C2447;
no separate head/neck or unmotivated facial drift. A brief natural blink is allowed.
Whenever Narrator speaks with Sol visible, establish his upward gaze to the fixed
above-camera voice before the first word and maintain it with gentle listening
idle for the whole turn. Intentional paired gaze shifts are allowed. Review the
actual script, speaker cues and footage together; final timing uses real voices.
Enforce and verify cadence during editing; prompts alone do not prove it.
Smooth planned editorial pushes may follow stepped footage; check all crops.
Preserve current models, voice selections, caption styling and frame approvals.

Mandatory script review: read the actual script/storyboard and per-scene speaker cues with every clip. Narrator speech plus visible Sol requires upward gaze and gentle listening idle throughout. New endpoint directions require review of the changed actual frame pairs before animation; preserve exact frame reuse where applicable.
