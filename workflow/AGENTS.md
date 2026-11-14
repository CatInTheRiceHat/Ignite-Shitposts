# Frame approval and clip review

These requirements record the user's current production instructions.

- All active clients use `config/generation.json`: **Gemini Omni Flash 1.2**
  (`gemini_omni_flash_1_2`) for video, mode `image-to-video`, with approved
  `start_image` AND `end_image`. Paired-frame clips are 3–10 seconds.
  Split longer scenes into declared continuing subscenes before preparing
  prompts. Do not silently switch back to Kling or Flow. This is a video
  model; shared image settings remain separate in the same config.

- Before animating EACH scene, send the user its actual first and last images,
  clearly labeled with scene ID and version. Compare them with the lantern
  source artwork first. Wait for explicit user approval of BOTH images.
  Showing the pair, a generator's own review, or a request to fix a previous
  version is not approval of the replacement pair. Do not approve on their behalf.
- Prepare the frame packet with `shorts.py review-frames <episode> --scene <id>`.
  Record approval only after the user gives it, using their actual words.
  Run `shorts.py review-gate <episode> --scene <id> --stage frames` before
  submitting any video. Do not bypass this check by calling Higgsfield directly.
- Prepare video tool payloads with `shorts.py video-request <episode> --scene <id>
  --start-media-id <id> --end-media-id <id>`. This loads the canonical model
  settings and refuses unapproved frame pairs or unsupported durations. Upload
  only the exact files identified by its approved frame hashes. This command
  prepares a request; it does not submit a job or authorize charges.
- Sol's primary reference is the existing lantern clip and its source frame.
  Check the actual silhouette, paint treatment, cream mask, eyes, limbs and
  softly wispy tip. Colors alone do not prove a match. Current escalator v4
  artwork is unapproved and appearance-rejected by the user.
- After a clip finishes, prepare `shorts.py review-clip <episode> --scene <id>`.
  Use the dedicated clip reviewer requested by the user to inspect the packet,
  reference comparison, chronological sheets and full-size evidence. Inspect
  actual media; do not approve from the prompt or FFprobe alone.
- Record timestamped observations for every check. Fail and uncertain both
  block production. Changed frames, reference artwork, requirements or video
  bytes invalidate prior approvals. Keep all rejected takes.
- Show raw drafts when the user asks, clearly stating unresolved errors.
  Do not call a draft approved or continue the batch from rejected footage.
  Reviewer findings and still approvals do not authorize paid regeneration.

Canonical commands run from the repository root as
`python3 workflow/scripts/shorts.py ...`. See `guidelines/clip-review-guide.txt`.
