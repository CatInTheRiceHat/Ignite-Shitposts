# Elaine's critique checklist

Updated: 2026-11-14. This is the project's running memory of Elaine's visual
feedback. Read it before writing prompts, generating frames or reviewing clips.
Update it when Elaine gives new critiques, following the maintenance rules below.
Unchecked boxes are reusable review questions, not claims about a particular take.

## References and prompts

- [ ] Inspect the actual example clips as well as their stills. Compare the
  current result against them; remembering the general look is not enough.
- [ ] Use [image-prompt.md](image-prompt.md) and
  [video-prompt.md](video-prompt.md): concrete composition, one main action,
  simple readable shapes, restrained texture and an accurate environment.
- [ ] Keep reference roles clear: the original mascot and supplied examples
  define Sol's identity; the lantern artwork and clip guide painted finish and
  movement. A rejected draft can supply useful geometry without defining style.
- [ ] Describe the visible first state, last state and the movement connecting
  them. Keep settings and attached-file details outside copyable prompt blocks.

## Sol

- [ ] Sol looks like the actual mascot, including the main flame tip, side
  lobes, layered colors, broad cream inner flame and compact rounded limbs.
  Preserve the cream flame's crown and rounded lower face.
- [ ] His two small navy oval eyes retain the mascot's size, spacing and low
  placement. Avoid exaggerated or mismatched eyes. Convey attention through
  gaze, a small whole-face turn and body pose.
- [ ] Keep Sol mouthless and his limbs stubby. Props from identity examples
  appear only when the scene calls for them.
- [ ] Paint the flame itself in the same storybook treatment as the scene.
  Keep the top softly tapering and wispy, with gentle follow-through in motion.
- [ ] Check identity and paint separately. Elaine clarified that the paint
  treatment was right while Sol's design was wrong; do not remove the painted
  finish when the requested correction is to his identity.

## Style and staging

- [ ] Match the lantern video's painted look and restrained movement with
  readable held poses. Avoid replacing that direction with generic glossy
  character rendering or excessive acting.
- [ ] The setting reads as a real, understandable place. Elaine rejected the
  earlier escalator pictures as too abstract; simplified shapes still need
  believable scale, perspective, structure and contact.
- [ ] Background detail and effects support the focal action. Keep breathing
  room around Sol and the mechanism, with clear space for editable captions.
- [ ] Review at phone size and full resolution. Sol, the important contact
  points and the action should be legible in both.

## Frames and clips

- [ ] Generate and show BOTH first and last frames, with scene/version labels,
  before generating a Higgsfield clip. Make them visible in the conversation
  and provide full-size file links.
- [ ] Wait for Elaine's explicit approval of that exact pair. A compliment,
  request for changes or approval of the general look does not settle remaining
  frame notes or authorize another generation.
- [ ] Use the dedicated reviewer to inspect actual generated footage for
  identity, style, contact, mechanical motion and continuity. Technical file
  checks alone cannot establish that a clip looks correct.
- [ ] Keep failed takes and current episode edits. Use versioned replacements
  and the selected models in [generation.json](../config/generation.json).

## Technical checks learned during escalator review

These are production checks from inspecting the failed takes, rather than
additional aesthetic preferences attributed to Elaine.

- [ ] In an exterior escalator view, show both opposing handrails. The flight
  connects two distinct floors with a normal incline and believable landings.
- [ ] The stationary landing is flush with the floor. The comb crosses the
  whole stair width, parallel to tread seams; separate treads flatten before it.
- [ ] Each foot has visible support. An already planted foot stays planted;
  the ending frame does not introduce a kick, lifted heel or extra step.
- [ ] A tracking mark stays attached to one tread and disappears beneath the
  fixed comb. Stationary parts keep their geometry and colors across the pair.

## Current visual anchors

- Identity: [Mascot.png](../assets/reference-art/Mascot.png) and the additional
  examples listed in [sol-references.json](../config/sol-references.json).
- Painted finish and movement: [lantern artwork](../episodes/sol_kling_test/keyframes/sol-lantern.jpg)
  and the [actual lantern clip](../episodes/sol_kling_test/clips/sol-lantern-kling.mp4).
- Latest positive direction: Elaine called the Nano Banana Scene 01
  [first frame](../episodes/escalator/keyframes/01-first-nano-v1.png) and
  [last frame](../episodes/escalator/keyframes/01-last-nano-v1c.png) “much better.”
  She has further notes to give; this is not recorded as final pair approval.

## Keeping this useful

When Elaine gives a critique, record the concrete visual problem and turn it
into a short, checkable instruction. Merge repeated points. Replace superseded
directions when she clarifies them, keeping any useful clarification beside the
rule. Label shot-specific fixes with their scope instead of applying them to
every episode. Keep reviewer observations distinct from Elaine's preferences.
Do not invent the additional notes she has not supplied yet, or mark an item
passed without inspecting the relevant result. Update the affected episode
prompts and storyboard when an authorized change is ready to apply.
