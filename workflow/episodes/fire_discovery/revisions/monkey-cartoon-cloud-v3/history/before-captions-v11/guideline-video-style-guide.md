# Ignite video style guide

Use the shared Gemini Omni Flash 1.2 video settings in `../config/generation.json`.
Prepare and show the actual first AND last stills to the user, and obtain
explicit approval of both before animation. The mascot design comes from `../config/sol-references.json`: use Mascot.png
and the additional supplied examples. Elaine accepts the v4 mascot-design
direction, but its painted finish still needs work; the frame pair is not approved. A dedicated reviewer must inspect actual
footage after generation; colors or successful technical checks do not prove
that Sol matches the original mascot assets.

Read this before generating art or editing an Ignite educational short. Pair it with [video-script-guide.md](video-script-guide.md) and [shot-integration-and-sol.md](shot-integration-and-sol.md).

## Art direction

- Use Ignite’s existing **soft, matte painted 2D** look, established by the approved scene artwork. Keep broad simplified shapes, restrained detail, subtle texture and softened painted edges. Build depth through overlapping layers, gentle shading, coherent perspective and contact shadows; parallax is optional when the chosen camera move calls for it.
- Follow `../config/sol-references.json`: Mascot.png and the additional mascot examples define the character. Use the provided graphics and gouache prompt language for painted finish. The lantern video is a painted movement reference subordinate to the current on-twos policy; use the original mascot silhouette, broad cream inner flame, low-set oval eyes and compact nub limbs when translating it into paint.
- Keep the staging welcoming, playful and easy to read on a phone. Use Ignite cream `#FFF8F0`, orange `#F07B2A`, and dark orange `#D46A20` for titles, accents, or overlays where they fit. Let the actual setting, time and light sources determine the scene palette; warmth is not an instruction to add firelight to an unlit scene.
- Treat the earlier *Arcane* reference as shorthand for visibly painted surfaces and expressive lighting. Use Ignite’s own artwork to set the character design and overall look. Flag glossy 3D shading, a clay-render look, and generic vector art when they break the painted style.
- Paint Sol, props and surroundings together with the same brushwork, perspective and coherent light. Shading should communicate the reference form and volume while preserving its proportions. Avoid inflated anatomy, glossy or clay-like rendering, generic vector shapes, heavy grain and excessive decoration.
- Keep identity and performance separate. The [shot guide](shot-integration-and-sol.md#sol-identity) owns character constraints and [purposeful acting](shot-integration-and-sol.md#purposeful-performance-and-prop-contact); the [image guide](image-prompt.md#painted-depth-and-form) explains painted depth and [reference roles](image-prompt.md#reference-roles-and-supplied-assets).

### Painterly surface treatment

This is the shared paint description for image and video prompt authors. Include its concise essentials in independently usable prompts:

```text
Match the approved Ignite artwork: soft, matte gouache-like brushwork, broad simplified shapes, restrained detail, layered color, softened painted edges and subtle paper texture. Paint subjects, props and surroundings together with coherent perspective and lighting. Build rounded forms and space through overlapping painted layers, gentle shading and contact shadows while preserving the reference proportions and volume. Define forms through light and color, without outlines, black strokes or inked edges. Avoid glossy rendering, generic vector shapes, heavy grain and decorative clutter.
```

Preserve Sol's reference design and settled endpoint proportions while painting the colored surfaces. Small coordinated action-driven flex follows the movement policy below. The red outer flame is a filled layer, not inked linework. Keep navy eyes solid and unchanged. Palette, format and scene contents follow the episode; the supplied seasonal/office prompts establish art direction only.

## Voices and performance

- **Arthur** is the default off-screen narrator. Use Higgsfield’s built-in Arthur voice with a warm nature-documentary delivery, patient pauses, and dry humor.
- **Sol** is the curious student and uses the user's **Higgsfield custom voice named Sol**. Use the exact voice ID and `voice_type: element` in [the shared voice cast](../config/voices.json). Keep Sol mouthless. Time direct gestures and intentional listening holds to dialogue while keeping his facial markings anchored to his body.
- Label every spoken turn **Narrator:** or **Sol:** in the review script. Let both voices respond to the scene and to each other. Sol can ask a substantive follow-up; his part is not limited to one-word reactions. Preserve existing episode voice overrides, including earlier single-voice Cub narration.
- Use connected, conversational sentences with varied lengths. Arthur's dry humor should come from the situation and delivery. Remove forced slogan endings and repeated clipped clauses. Give an explanation enough words to make its cause and effect clear.
- When Arthur addresses visible Sol, use the [shot guide's listening and acting cues](shot-integration-and-sol.md#purposeful-performance-and-prop-contact). Give the primary action a distinct purpose. During Narrator speech, the mandatory above-camera listening gaze and gentle idle remain in force. Keep the narrator off-screen and avoid redundant reaction loops.

## Sol's cartoon expression and movement

Move Sol through each short gesture with a gentle connected body-and-tip wiggle, then settle into the supplied ending pose. Keep both feet supported. His filled red/orange/cream layers, face and original lobes move together as one compact painted form. No particles, sparks, brush-flecks, droplets, detached flame shapes, airborne hops or body splitting. During Narrator speech, establish body-led attention UP toward the fixed point just above camera before the first word and maintain it with quiet connected listening idle. Keep the normal-height close-spaced navy oval eyes unchanged; a brief natural blink is allowed. No extra gestures, windup, repeated nodding or camera movement.

Use the [identity and performance rules](shot-integration-and-sol.md#sol-identity). Preserve the recognizable compact design and coherent nested color layers through the flex. The face travels with the body; the normal navy oval eye design stays unchanged in shape, size and spacing, with a brief natural blink allowed. Tiny limbs retain their lengths and attachment points. Keep supported feet grounded unless a hop or step is explicitly scripted.

This supersedes the earlier blanket “no bounce,” rigid-body and no-tip-follow-through defaults. A brief natural blink is now allowed. It does not authorize unrelated expressive eye morphs, unmotivated facial sliding, separate head turns, exaggerated body stretching, automatic windups or camera bounce. The precise on-twos cadence below remains in force.

## Motion style

At the existing **30 fps export**, animation on twos means **15 pose updates per second**, with normal-speed playback. Use this shared motion block in generation prompts, tailoring the named subjects to what is visible:

```text
Animate on twos: hold each animated pose or painted state unchanged for two consecutive frames of the final 30 fps timeline, then advance to the next pose. Longer intentional holds may span multiple complete two-frame pairs. Maintain normal-speed action; this is a frame cadence instruction, not a speed-up or slow-motion effect.

Apply this cadence to Sol, the human hand, moving props, flames, and animated local lighting. Keep the background and painted surface texture stable. Do not interpolate or blend between held poses. Avoid optical-flow smoothing and motion blur that conceals the stepped animation.

Move Sol through each short gesture with a gentle connected body-and-tip wiggle, then settle into the supplied ending pose. Keep both feet supported. His filled red/orange/cream layers, face and original lobes move together as one compact painted form. No particles, sparks, brush-flecks, droplets, detached flame shapes, airborne hops or body splitting. During Narrator speech, establish body-led attention UP toward the fixed point just above camera before the first word and maintain it with quiet connected listening idle. Keep the normal-height close-spaced navy oval eyes unchanged; a brief natural blink is allowed. No extra gestures, windup, repeated nodding or camera movement.

Preserve Sol’s recognizable compact flame design, coherent red/orange/cream layers and stubby limb lengths. Allow small connected body/tip/lobe flex, with every colored part attached to the main body. The face remains part of the body. Intentional gaze shifts may move the existing eye ovals coherently as a pair inside the face while preserving their normal shape, size and gap. Do not detach or rotate the face as a separate head, introduce a neck, or allow unmotivated feature drift.

Keep the normal open-eye design as the original navy #1C2447 ovals with their reference shape, size, low resting placement and close spacing. Scripted upward glances may shift the pair coherently within the face. A brief natural blink may close/reopen both eyes, returning promptly to the same gaze and original oval design. No whites, highlights, extra pupils, eyebrows, winks, unrelated eye morphs or facial-feature drift.

Generation should aim for this motion quality. Enforce and verify the exact two-frame cadence during editing.
```

Omit Sol's identity paragraphs when he is absent. Do not replace this cadence with the ambiguous phrase “stepped poses.” A prompt is a generation target, not evidence of compliance.

During editing, enforce two-frame source-pose holds on the final 30 fps timeline before applying any editorial camera transform. Align longer holds, action trims and source-state changes to complete two-frame pairs. Preserve natural action timing and 1x voice playback; inspect consecutive source frames and final playback for facial drift and prop contact. Do not use optical flow, frame blending or concealed interpolation as a cadence conversion.

A purposeful digital push or crop can remain smooth over the stepped footage when the shot plan explicitly assigns it to editing. Check the crop throughout the move, keeping the face, limbs and important contacts visible. Do not apply the same move during generation. Record exact cadence as unverified until actual footage has been edited and checked.

## Cartoon exaggeration and action effects

Elaine wants visibly cartoony performance: readable effort, exaggerated bursts
of rapid movement, and a clear reaction when the action produces a result.
Use compact painted motion clouds, a few curved speed strokes and small puffs
when they help communicate how energetically a character is moving. A cloud
can briefly surround fast hands, then clear to reveal the outcome. Treat this
as a reusable visual vocabulary; choose effects that fit each action instead
of repeating the same effect in every shot.

For sustained frantic action, use the motion of a classic cartoon fight cloud:
keep one active cloud present while its lobes tumble over each other, fold,
bulge and change silhouette, with brief speed strokes and small escaping
puffs. Let it break apart and clear once when the action ends. Elaine rejected
an identical cloud repeatedly appearing and disappearing; inspect the actual
sequence for continuous internal change and evolving contours.

Once an action effect clears, leave its visible result readable through the
reaction and cut. Do not introduce an unmotivated late puff that hides or
abruptly erases the payoff. Elaine's latest correction removed that ending
poof; it did not reject the energetic fight cloud during the action. Keep
any different intentional disappearance specific to its own storyboard.

Keep effects localized to the action, with a clear onset and finish. Preserve
the face, silhouette and readable cause and effect; reveal the hands and prop
contact clearly as the cloud clears. Keep the actual limb and prop counts,
shapes and physical contacts coherent throughout. An effect must not conceal
broken anatomy or an incorrect mechanism. Paint clouds and motion strokes
with the same soft gouache brushwork, layered color and paper texture as the
rest of the scene.

Fast cartoon acting happens inside normal 1x clip and voice playback. Apply
the exact on-twos cadence to the character, props and every effect state;
use crisp painted shapes with a stable background, without blended frames
or photographic motion blur. Generate the effect as part of the complete
scene. Specify its visible starting and ending states in the storyboard.

Keep each character's identity rules. Sol expresses effort and surprise through
his supported body poses and compact gestures, retaining his original eyes,
mouthless face and connected flame layers. Action clouds are deliberate scene
effects; they do not authorize particles or detached flame pieces emitted by
Sol. Other characters retain their own established facial designs. Specific
characters, props, locations and ignition details stay in episode documents.

## Particle-free Sol movement

Elaine's latest direction is “scrap the fire particles” and use “just wiggle animation for sol.” Sol emits no particles, sparks, flecks, droplets or detached flame accents at any time. All wiggle and tip follow-through stays attached to his continuous filled body. The separate wood fire may flicker only at its fixed fuel contact. This supersedes the earlier allowance for tiny bounce-triggered flicks. Keep gesture transitions soft and connected, using a low-amplitude body/tip wiggle rather than an airborne bounce. Preserve the face, nested layers, anatomy and approved ending poses.

## Pacing, motion, and type

- Make every shot stimulating and nice to look at, with plenty of purposeful action that makes viewers curious about what is happening. Follow the [shot guide's visual interest and curiosity direction](shot-integration-and-sol.md#visual-interest-and-curiosity) when staging performances, interactions and reveals.
- Open on the question or a surprising image. Use a close-up or controlled camera push when it reveals an important detail, and a stable view when it serves listening, anticipation or a readable payoff. Hold the reveal long enough to read it.
- Keep entrances and exits brisk by trimming unnecessary lead-ins and tails from actual footage. Start during readable action when appropriate, and cut while the outcome is still visible. Retain complete voice releases and reactions; do not create a whole-scene freeze to extend a shot.
- Vary clip lengths around the action and dialogue. Keep several lines in one scene when they share an action; use a shorter reaction or cutaway when it adds something. Establish the exact first and last frames of every planned clip. Use normal voice playback and set final timing from the actual recordings.
- Export vertical at **1080 × 1920, 30 fps**. Keep draft durations provisional; the [script guide](video-script-guide.md#dialogue-density-and-timing) owns timing to real normal-rate recordings and removal of unnecessary holds or repeated reactions. The default deliverable remains complete generated clips, including the painted mechanism and motion.
- Set all dialogue and narration captions as editable overlays in Remotion. Use **Ramento** with white fill `#FFFFFF` and Ignite orange outline `#F07B2A` around each letter. Use one or two lines above the social controls, with room around Sol, diagrams, and equations. Use Poppins Bold for headings and Nunito for longer non-caption text when needed.
- Elaine requested slightly larger captions. The current 1080p fire edit moves from 56px to 64px, about 14% larger, while retaining the 12px orange outline. Use this as a working readability reference, scaled to the output; confirm the actual result at phone size. Keep one or two lines, generous side/bottom margins and space around the action. Check the longest phrases and final short word after changing the size; do not alter their wording or voice timing just to fit.
- Keep that orange outline visibly substantial at phone size. The1080p fire correction increases the stroke from6px to12px; preserve white letter interiors and check the actual export, rather than relying on a thin preview stroke.
- Confirm the actual local font family before assembly; a guide's display name can differ from the font filename. Keep per-episode font paths and renderer implementation gaps in the episode handoff. Caption words and timings follow the real voice takes. Keep any optional finishing graphics and sound effects editable; they are not required to explain a mechanism that is already visible in a complete generated clip.
- Keep assembly simple: arrange the complete clips, add separate voices, captions and sound, and export. Make explanatory colors or identifying details part of the generated scene where useful. Do not create SVGs, custom diagrams or separate mechanism animation unless explicitly requested. Additional visual overlays are optional, not a required production stage.

## Review the rendered video

- [ ] The opening reads immediately at phone size.
- [ ] Art texture and lighting feel consistent across adjacent shots.
- [ ] Sol's normal open-eye design matches the reference; brief natural blinks return to it promptly; body poses carry the performance, with a gentle connected wiggle and coherent layer follow-through, without emitted particles. The recognizable compact design and settled endpoint proportions stay intact.
- [ ] Sol, props and background all show the same visible gouache brushwork, layered color and paper texture, with no inked outlines.
- [ ] Motion and transitions draw attention to the explanation. The reveal remains visible long enough to understand.
- [ ] Arthur and Sol are distinct in the mix. Captions use the approved Ramento treatment, are timed to both voices, and sit clear of the subject. Replace any visible draft placeholders before release.
- [ ] Dialogue flows like a conversation, explains unfamiliar mechanisms clearly, and resolves the scene without a forced punchline.
- [ ] The clip durations support the performances and visible actions, with continuity between planned first and last frames.
- [ ] Expressive poses and original eye designs read at phone size; each reaction has a clear purpose, cue, target and result. Two-frame source-pose holds at 30 fps (15 updates per second), normal-speed action, stable texture and the absence of interpolation have been checked in consecutive frames and playback. Check smooth editorial camera crops separately.
- [ ] Whenever the Narrator speaks with Sol visible, Sol looks up before the first word and maintains that above-camera gaze and gentle listening idle throughout the turn. Review it against the actual script and available voice cues.
- [ ] Review the real frames at about 360 × 640 as well as full resolution. The first action, gaze, object identity, contact points and final reaction remain legible, and one or two caption lines clear the platform controls. Planned bounding boxes alone do not establish that finished footage passes this check.

Before generation, also run the shared [final prompt review](checklist.md#final-prompt-review). Keep the caption treatment above and current voice selections; older episode examples and legacy configuration do not replace them.

## References

- *Automate Ignite Videos* chat, Nov. 8, 2026. Painted 2D look, half-frame motion, and the calculus pilot reference frames.
- *Remotion setup and workflow checklist* discussion, Nov. 10, 2026. Painted Ignite art, Zack D. Films pacing, vertical export, and render review.
- *Escalator cartoon direction*, Nov. 13, 2026. Historical camera and acting discussion; its eye morphs and anatomy-changing exaggerations are superseded by the current identity rules.
- [Ignite Program Style Guide.pdf](https://chatgpt.com/library?file_id=libfile_02e662ff436881919a34e6913e985727&account_id=personal)
