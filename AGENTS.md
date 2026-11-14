# Ignite Shorts workspace

- Read `workflow/guidelines/checklist.md` before prompts, generation and media
  review. Keep this running record updated with Elaine's critiques, preserving
  their scope and latest clarifications. Follow `workflow/AGENTS.md` for details.
- Current image model: **Nano Banana 2.1** through Higgsfield, exact ID
  `nano_banana_2_1`. Use the shared 2k, 9:16 settings; do not pass GPT-specific
  `quality` or `output_format` options. Model changes do not authorize generation.
- Current video model: **Gemini Omni Flash 1.2** through Higgsfield,
  exact ID `gemini_omni_flash_1_2`. Shared settings for every active client
  live in `workflow/config/generation.json`; follow `workflow/AGENTS.md`.
- Generate each scene's first and last stills, show BOTH to the user, and wait
  for explicit approval of that exact pair BEFORE generating its Higgsfield
  clip. Do not treat a request to fix an earlier version as approval of new
  stills. The current escalator character is unapproved. Read
  `workflow/config/sol-references.json`: Mascot.png and the new mascot examples
  control design; retain the paint treatment the user accepted. The lantern
  video guides finish/motion. Do not replace the mascot's broad cream inner
  flame and low-set oval eyes with a narrow droplet mask and raised eyes.

- All new Ignite Shorts code, configuration, prompts, artwork copies, episodes,
  downloads, tests and renders belong under `workflow/`.
- Start with `workflow/README.md`. The canonical CLI is
  `python3 workflow/scripts/shorts.py` from this repository root.
- Read `workflow/guidelines/README.md` and its script, style and Sol/shot
  guides before writing scripts, generating art or planning shots. If those
  guides are located at the repository root, use `guidelines/README.md` and
  its linked guides; do not skip them because the workflow path is absent.
- For each new episode, deliver one complete script and storyboard document
  combining all Sol/Narrator dialogue with the scene, framing, action,
  expressions, first frame, last frame and transitions for every clip. The
  escalator example is `workflow/episodes/escalator/script.txt`.
- Alongside each episode document, save a separate reviewable prompt text
  file. For N scenes, provide exactly 2N image prompts (one first frame and
  one last frame per scene) and N video prompts (one continuous first-to-last
  motion prompt per scene). Match scene IDs, dialogue, framing, expressions
  and continuity to the episode document. Keep settings, reference inputs
  and edit-only overlays outside the copyable prompt blocks. Writing or
  reviewing prompts does not authorize image, video or audio generation.
- Use a clips-first production workflow: generate the first/last stills,
  animate each pair into a complete Higgsfield clip, then assemble the clips
  with voices, captions and sound. Explanations and cutaways belong inside
  the generated scenes. Do not create SVGs, custom diagrams, geometry tools
  or separately animated mechanisms unless the user explicitly requests them.
  If a generated scene is inaccurate, revise its prompts and regenerate that
  scene. Keep final editing simple; do not introduce a separate animation
  workflow as an automatic fallback.
- Write a conversational skit with connected sentences and enough concrete
  explanation to understand the mechanism. Avoid repeated clipped clauses,
  vague shortcuts, forced jokes and slogan endings. Label every spoken turn
  `Sol:` or `Narrator:`. Vary clip lengths around the action; multiple lines
  can share a clip. Set final timing from the normal-rate voice recordings.
- Preserve every original mascot feature across clips, explicitly including
  Sol's short rounded arms, stubby feet, small navy oval eyes, flame layers,
  colors and proportions. Keep him mouthless. The painted aesthetic changes
  surface treatment while preserving the asset design. Use gaze, restrained
  body poses and gentle flame-tip follow-through for acting; do not redesign
  the eyes or lengthen limbs. Read the latest critique checklist and guides.
- Make every shot specific: camera height and angle, shot size, subject
  placement and scale, crop, camera movement, and exact visible first/last
  states. Keep mechanical motion accurate while exaggerating performance
  and cartoon attention effects.
- When the Narrator addresses Sol while he is visible, Sol acknowledges the
  voice with an upward glance toward a fixed point just above the camera,
  breaking the fourth wall. Specify that eye/body turn and its spoken cue.
  He can follow a directed look at the mechanism, then return his attention
  to the Narrator as the exchange continues.
- Shared artwork and music live in `workflow/assets/`; additional reference
  artwork is in `workflow/assets/reference-art/`. Reusable Remotion components,
  tools and the single npm install live in `workflow/remotion/`. Keep each
  episode's edit, artwork, media and renders in `workflow/episodes/<name>/`;
  custom compositions can live in that episode's `remotion/` folder.
  The generic Remotion starter is `workflow/templates/remotion-episode.json`.
  See `workflow/episodes/README.md` for episode locations and commands.
- `Ignite Website` is a read-only source. Never write into that repository.
- Preserve episode edits and downloaded files. Prepare is non-destructive;
  flag differing filename collisions before moving or replacing files.
- Shared defaults are a 30-second target, 9:16 and painted 2D. New two-voice
  skits use Arthur as the off-screen Narrator and the user's Higgsfield
  custom voice named `Sol` for Sol. Use the saved exact voice ID and
  `voice_type: element` in `workflow/config/voices.json`; do not substitute
  Cub for Sol. Keep speech at its normal generated rate and 1x playback.
  Preserve existing episode overrides, including single-voice Cub narration.
- The root `zack-d-films-ai-video-generator` and `music` paths are compatibility
  links. Actual files live inside `workflow/`; do not put new work into vendor
  or legacy paths. Vendor is the original upstream reference, not Ignite's
  painted production guide.
- Do not commit credentials, caches or downloaded/generated media.
