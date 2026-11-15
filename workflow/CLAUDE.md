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

The order is mandatory: generate both stills; show BOTH to the user; wait for
explicit approval of that exact pair; then generate the Higgsfield clip.
Run independent actual-footage review before production use. Read
`workflow/config/sol-references.json`: use Mascot.png and the additional mascot
examples for Sol's design. V4 establishes the accepted identity direction;
its surface still needs visible gouache brushwork, layered color and paper
texture on both Sol and the scene, with no inked outlines. Use the supplied
graphic examples for finish and the lantern video as a painted movement reference subordinate to the current cadence. Keep
the original eyes unchanged and open. The frame pair remains unapproved.
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
Use short direct actions with clean stops, without unrequested preparation,
windup, recoil, overshoot, bounce, repeated nodding, idle swaying or camera moves.
Keep Sol's facial markings anchored to his body and eyes uniformly navy #1C2447;
no independent face turn, neck, blinking, highlights or drift. A gesture change
or listening hold can acknowledge Arthur without an automatic upward look.
Enforce and verify cadence during editing; prompts alone do not prove it.
Smooth planned editorial pushes may follow stepped footage; check all crops.
Preserve current models, voice selections, caption styling and frame approvals.
