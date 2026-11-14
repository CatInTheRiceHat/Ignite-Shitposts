# Ignite production instructions for Claude

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
examples for Sol's design, retain the paint treatment the user accepted, and
use the lantern video for finish/movement. The character/pair remain unapproved.
Never record frame approval on the user's behalf. Preserve all existing media.
