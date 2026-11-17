# Elaine's critique checklist

Updated: 2026-11-16. This is the project's running memory of Elaine's reusable
art-direction feedback. Read it before writing prompts, generating frames or reviewing clips.
Update it when Elaine gives new critiques, following the maintenance rules below.
Unchecked boxes are reusable review questions, not claims about a particular take.

The complete fire episode feedback is consolidated in
[fire_discovery/feedback.txt](../episodes/fire_discovery/feedback.txt). Keep specific
scene requests, settings, sound cues and delivery notes in the relevant episode;
they do not become shared art-direction rules.

## Final prompt review

- [ ] Check the actual delivered footage for mouths and Sol particles, including every intermediate pose. The area beneath the eye pair stays blank; a third facial mark or mouth line is a failure. A mouthless prompt does not establish a mouthless result. Never present a rejected mouth-bearing take as the corrected result.
- [ ] Trim dead air from the actual voice files and unnecessary clip lead-ins and tails while retaining readable actions and short intentional pauses. Preserve normal speech speed. Keep the orange caption outline clearly visible at phone size; the current 1080p fire edit uses12px instead of the earlier thin6px.
- [ ] Are captions large enough to read on a phone? The current fire correction uses 70px, 25% above the original 56px at 1080p, with the existing 12px orange outline; this supersedes the 64px trial. Check every phrase, especially long lines and the last word, for one/two-line wrapping, safe margins and clear action.
- [ ] Does the revealed result stay visible through the reaction and cut, without an unmotivated late poof hiding or abruptly erasing it? Keep useful movement rather than adding a frozen scene to fill time.
- [ ] Preserve quiet word releases and a readable final hold; do not apply
  silence trimming so tightly that speech feels clipped.

- [ ] Review the actual complete script and speaker turns alongside the footage. Whenever Narrator speaks and Sol is visible, is the upward glance established before the first word and maintained with gentle listening idle throughout? Check transition frames and real voice cues when available; label unrecorded timing provisional.

Run this short review on the complete prompt set before generation. Follow the linked rule owners for details; keep shot-specific fixes scoped to their episode or animation.

- [ ] Does the scene match Ignite's approved [matte painted style](video-style-guide.md#painterly-surface-treatment)?
- [ ] Are shapes simple and readable, with believable [painted depth](image-prompt.md#painted-depth-and-form)?
- [ ] Is Sol's [identity preserved](shot-integration-and-sol.md#sol-identity) while his [action remains expressive](shot-integration-and-sol.md#purposeful-performance-and-prop-contact), where he is visible?
- [ ] Does each shot contribute a [distinct teaching beat](video-script-guide.md#distinct-visual-beats)?
- [ ] Is every shot stimulating and attractive, with plenty of purposeful
  action that invites “omg thats cool whats happening there”? Identify what
  catches the eye, how the action develops and the visible payoff; check
  [visual interest and curiosity](shot-integration-and-sol.md#visual-interest-and-curiosity).
- [ ] Does the performance use Elaine's preferred [cartoon exaggeration and
  action effects](video-style-guide.md#cartoon-exaggeration-and-action-effects)
  where useful: readable effort, rapid motion, compact painted clouds or speed
  strokes, then a clear reveal and reaction? Keep effects tied to the action,
  preserve anatomy and prop contact, and clear them so the result reads.
- [ ] For a sustained cartoon fight-cloud effect, do its lobes continuously
  churn, tumble and change shape until one final clearing? Reject an identical
  cloud repeatedly appearing and disappearing.
- [ ] Are camera behavior, generation/editing responsibility and [motion quality](video-prompt.md#motion-and-continuity) intentional, with exact two-frame source holds at 30 fps and normal-speed action to be verified during editing?
- [ ] Are there contradictory lighting instructions or [leftover objects and boilerplate](video-prompt.md#remove-boilerplate-and-contradictions)?
- [ ] Can matching frames connect naturally, and can an approved [endpoint be reused](shot-integration-and-sol.md#specify-the-first-and-last-frames) unchanged?
- [ ] Are durations explicitly provisional or grounded in [actual normal-rate voice tracks](video-script-guide.md#dialogue-density-and-timing)?
- [ ] Are captions and precise graphics assigned to editable overlays, preserving the [current caption treatment](video-style-guide.md#pacing-motion-and-type)?

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
- [ ] Record identity, style, composition and continuity [reference roles](image-prompt.md#reference-roles-and-supplied-assets). Every path maps to an actual supplied input; label future assets as planned until they exist and are approved.

## Sol

- [ ] Sol looks like the actual mascot, including the main flame tip, side
  lobes, layered colors, broad cream inner flame and compact rounded limbs.
  Preserve the cream flame's crown and rounded lower face.
- [ ] Compare the WHOLE design beside the original at a similar size: broad
  flat silhouette, asymmetric main tip, rounded lobes/notches, substantial red
  outer layer, original orange/cream contour paths and relative widths, face
  proportions and low eye placement. Dark eyes and small feet alone do not
  make a redesigned flame character the Ignite mascot.
- [ ] Preserve the original 2D geometry while painting its surfaces with visible
  gouache brushwork, layered color and paper texture. Sol, props and surroundings
  share that treatment. A smooth logo finish with only a grain overlay does not
  meet the requested painted look. Avoid inflated or sculpted anatomy.
- [ ] Preserve ALL mascot features across clips. Match the short rounded arms
  and stubby feet in the asset examples: their length, thickness, shape, color
  and attachment points stay consistent. A new pose keeps the same anatomy.
  Feet are tiny rounded red tabs immediately below the flame body, without a
  lower-leg shaft, ankle or long boot-like toe.
- [ ] His two small navy oval eyes retain the mascot's size, spacing and low
  placement. Avoid exaggerated or mismatched eyes. Convey attention through
  purposeful direct gestures and body poses, with facial markings fixed to his body. Keep their original flat navy
  appearance. Elaine's “dark pupils” mean these existing whole dark ovals: fill
  them completely with asset navy #1C2447, without eye whites, shine or gray gradients.
  Keep the normal open oval design unchanged. A brief natural blink may close
  and reopen both eyes, returning promptly to those ovals. No prolonged squint,
  unrelated expressive reshaping, winks or added eyebrows. Never slide or rotate facial markings independently,
  add a neck or reshape the body to simulate a head turn. Express action through
  posture, gestures and coordinated body/flame wobble; the face travels with the body and the normal oval eye design is preserved outside a brief natural blink.
- [ ] Keep the paired eyes close enough together to match the original mascot.
  Elaine accepted the fire Scene 01 direction but said its eyes were too far
  apart. Compare the gap relative to eye width, rather than spreading the eyes
  across the cream face. Correct spacing by moving the existing ovals inward;
  preserve their size, shape, dark fill, low height and the accepted painting.
- [ ] Elaine flagged the Fire Scene 02/05 upward-looking endings because the eyes
  became lighter and deformed. For a gaze-only change, move the original oval
  pair without tilting, skewing, shortening or rounding it. Preserve each eye's
  size, proportions, orientation and gap, with opaque dark navy #1C2447 rather than
  lighter blue/gray, gradients, sheen or pale rims. Compare enlarged first/last
  eye crops; looking up does not require a new eye design. See the
  [Narrator attention owner](shot-integration-and-sol.md#narrator-attention-and-listening-idle).
- Latest correction: Elaine rejected the vertical eye-squish trial as funny
  looking and asked for a small upward tilt of Sol's body instead. Restore the
  original tall navy ovals. Pitch the compact body, filled flame layers and
  attached face coherently together, with feet supported; no separate head,
  face slide, eye squash or body stretch. Review the new pose before animation.
- [ ] Keep Sol mouthless and his limbs stubby. Props from identity examples
  appear only when the scene calls for them.
- [ ] Paint the flame itself in the same storybook treatment as the scene.
  Keep the top softly tapering and wispy. Give intentional movements the requested small bouncy wobble and soft tip/lobe follow-through, settling between actions.
- [ ] Check identity and paint separately. Elaine clarified that the paint
  treatment was right while Sol's design was wrong; do not remove the painted
  finish when the requested correction is to his identity.
- [ ] Apply the painted aesthetic to the existing mascot shapes. It must not
  produce a different Sol with longer legs, larger hands, altered eyes or
  redesigned flame layers. Original assets control identity even when a
  generated continuity frame differs.
- [ ] Match the actual result to BOTH its prompt and the source assets,
  checking arms, feet and eyes at the beginning, middle, end and across cuts.

## Style and staging

- [ ] Keep Sol's painted interior stable through movement. Elaine flagged a
  rippling/waving deformation: gentle attached tip follow-through must not
  become a traveling wave through his red/orange/cream layers, a jelly-like
  body warp or texture swimming. Check every intermediate pose.

- [ ] Sol emits no particles, sparks, flecks, droplets or detached flame accents at any time. All wiggle and tip follow-through stays attached to his continuous filled body. The separate wood fire may flicker only at its fixed fuel contact. Follow the [particle-free movement rule](video-style-guide.md#particle-free-sol-movement).

- [ ] Latest instruction: use a gentle connected body/tip wiggle through Sol's pose changes and listening idle. Keep feet supported, face and layers coherent, and emit no particles. Check the approved body tilt with the actual dialogue; still approval alone does not prove upward attention.

- [ ] Match the approved Ignite scenes with soft, matte gouache-like brushwork,
  broad simplified shapes, restrained detail, softened painted edges, layered
  color and subtle paper texture across Sol, props and surroundings. Define
  forms with light and color; no glossy rendering, generic vector shapes, inked
  outlines, heavy grain or decorative clutter. Preserve the red outer flame as
  a filled shape and the original solid dark eyes.
- [ ] Preserve depth and the mascot's reference volume through overlapping
  painted layers, gentle shading, coherent perspective and contact shadows.
  Do not flatten the scene or invent inflated/sculpted mascot anatomy.
- [ ] Give each Sol scene a distinct readable action with enough connected
  physical stages to sustain visual interest. Each gesture uses a direct path,
  small bouncy flame-like follow-through and a readable endpoint; keep holds
  purposeful. Keep layers and face coherent, eyes unchanged, limbs stubby
  and feet supported. Avoid unrelated windup, repeated nodding, endless idle
  sway, extra hops or camera movement.
- [ ] Request animation on twos: every animated source pose or painted state stays
  unchanged for two consecutive frames at final 30 fps (15 updates per second),
  with normal-speed action and complete-pair longer holds. Apply it to Sol,
  visible hands, moving props, flames and animated local lighting. Keep the
  background and painted texture stable; no interpolation, frame blending,
  optical-flow smoothing or concealing motion blur. Enforce and inspect source
  pairs during editing, then check final playback and smooth editorial crops.
- [ ] Choose the camera per shot and state whether a move belongs in generation
  or editing. Continuing clips reuse the approved preceding ending asset as
  the next starting asset unchanged; label the reuse instead of regenerating.
- [ ] Keep the area beneath the eyes blank: no mouth, nose or added facial marks.
  Keep flame shapes solid and intact, without realistic fire effects.
- [ ] Transfer the art-direction language from Elaine's office, beach and spring
  examples. Keep the episode's own setting, palette, framing, character count
  and aspect ratio; those example scene details are not shared defaults.
- [ ] Use the lantern video's painted movement and readable held-pose rhythm
  alongside the [current motion style](video-style-guide.md#motion-style). Let
  each scene choose purposeful gestures, orientation or weight shifts rather
  than copying its small movements into every shot. Preserve anatomy and avoid
  stacking unrelated reactions.
- [ ] The setting reads as a real, understandable place. Elaine rejected the
  earlier escalator pictures as too abstract; simplified shapes still need
  believable scale, perspective, structure and contact.
- [ ] Background detail and effects support the focal action. Keep breathing
  room around Sol and the mechanism, with clear space for editable captions.
- [ ] Review at phone size and full resolution. Sol, the important contact
  points and the action should be legible in both.

- [ ] For prop placement, stable grip and lowering precede support, support precedes release, and the released prop stays stationary during one clear hand-withdrawal path. Inspect contact in actual consecutive frames.

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

Fire episode note, 2026-11-15: Elaine explicitly authorized local eye-only
cleanup for the Scene 02/05 endpoints after Nano retries changed the ovals.
Use the approved source contours, retain their size/orientation/gap, translate
the pair upward and restore opaque original navy. Preserve the scene outside
the eye repair areas. This permission covers that cleanup; the resulting exact
frame pairs still need her review before Higgsfield animation. Keep the shared
Nano Banana image and Omni Flash video defaults.

## Technical checks learned during clip review

These are production checks from inspecting the failed takes, rather than
additional aesthetic preferences attributed to Elaine.

- [ ] Inspect the moving silhouette at native resolution for faint red trails
  and emission buds still joined by a thin bridge. Phone-size sheets and
  connected-component counts can miss these. After a local cleanup, inspect
  every selected pose and the transitions around any complete-pair holds;
  confirm the repair preserves the main contour, face and limbs.

- [ ] Sol's filled shape stays coherent through wiggle. Reject any detached sparks, flicks or droplets, torn lobes, holes, separating layers or airborne hops. This implements Elaine's latest particle-free direction.

- [ ] When a generated mascot is wrong, remove it from scene/layout inputs
  before rebuilding. Use the original mascot as the primary identity image
  and a character-free scene as the environment reference. A rejected character
  must not quietly become the starting design for the next correction.
- [ ] In an exterior escalator view, show both opposing handrails. The flight
  connects two distinct floors with a normal incline and believable landings.
- [ ] The stationary landing is flush with the floor. The comb crosses the
  whole stair width, parallel to tread seams; separate treads flatten before it.
- [ ] Each foot has visible support. An already planted foot stays planted;
  the ending frame does not introduce a kick, lifted heel or extra step.
- [ ] A tracking mark stays attached to one tread and disappears beneath the
  fixed comb. Stationary parts keep their geometry and colors across the pair.

## Current visual anchors

- Latest cartoon direction: Elaine called the rapid-hand cloud frame direction
  “wonderful awesome” and explicitly asked to save it as what she wants for
  “cartoony.” Carry forward playful exaggeration, localized painted motion
  clouds/speed strokes and clear reactions under the [style owner](video-style-guide.md#cartoon-exaggeration-and-action-effects).
  The specific scene remains episode-scoped. This records style acceptance;
  approval of an exact frame pair remains a separate production decision.

- Latest mandatory direction: whenever Narrator is speaking with Sol visible, Sol looks UP toward the fixed voice above camera and keeps gentle listening idle. Review the actual clip WITH the script and speaker cues. This supersedes the earlier optional/no-upward-glance and no-listening-idle defaults. Intentional coherent paired eye-gaze shifts are allowed; normal eye design, brief natural blinks, mouthless face, connected flame layers and stubby limbs remain.

- Latest explicit preference: “i like omni flash” after viewing the Omni Flash 1.2 and Kling 3.0 Pro comparisons. Keep Omni Flash 1.2 for this episode. Elaine also said “Allow a brief natural blink.” Preserve the normal navy oval eye design and face attachment; brief closing/reopening is permitted, while unrelated eye morphs, highlights, added pupils and facial drift remain excluded.

- Latest motion clarification: “scrap the fire particles” and use “just wiggle animation for sol.” Gentle attached body/tip wiggle replaces the previous particle allowances. Keep the original eyes, compact anatomy and supported feet; actual wood fire remains separate.

- Current fire episode feedback: Elaine likes Scene 01's painted direction and
  staging, but its v1 eyes are too far apart. Preserve that painting while
  correcting eye spacing. This is not approval of the replacement frame pair.
- Identity: [Mascot.png](../assets/reference-art/Mascot.png) and the additional
  examples listed in [sol-references.json](../config/sol-references.json).
- Painted finish and movement: [lantern artwork](../episodes/sol_kling_test/keyframes/sol-lantern.jpg)
  and the [actual lantern clip](../episodes/sol_kling_test/clips/sol-lantern-kling.mp4).
- Latest positive direction: Elaine called the Nano Banana Scene 01
  `01-first-nano-v1.png` first frame and
  `01-last-nano-v1c.png` last frame “much better.”
  Her next correction is to preserve every mascot feature, explicitly including
  the arms, stubby feet and eyes, across all clips. Prompts are being revised to
  match the asset examples; the existing pair is not recorded as finally approved.
- Elaine subsequently rejected the v3 character as not looking like the Ignite
  mascot. Correcting isolated traits did not fix its overall design. V2/v3
  characters are rejected identity references; compare new candidates against
  the original assets, not against those generated versions.

- Latest clarification: Elaine accepts the v4 mascot-design direction but says
  its surface lacks the painted look. Preserve v4 geometry and use the supplied
  gouache art direction on Sol and the surroundings. The frame pair is not approved.

## Keeping this useful

When Elaine gives a critique, record the concrete visual problem and turn it
into a short, checkable instruction. Merge repeated points. Replace superseded
directions when she clarifies them, keeping any useful clarification beside the
rule. Label shot-specific fixes with their scope instead of applying them to
every episode. Keep reviewer observations distinct from Elaine's preferences.
Do not invent the additional notes she has not supplied yet, or mark an item
passed without inspecting the relevant result. Update the affected episode
prompts and storyboard when an authorized change is ready to apply.
