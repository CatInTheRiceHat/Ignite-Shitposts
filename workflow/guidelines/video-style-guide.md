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
- Follow `../config/sol-references.json`: Mascot.png and the additional mascot examples define the character. Use the provided graphics and gouache prompt language for painted finish. The lantern video guides gentle movement; use the original mascot silhouette, broad cream inner flame, low-set oval eyes and compact nub limbs when translating it into paint.
- Keep the staging welcoming, playful and easy to read on a phone. Use Ignite cream `#FFF8F0`, orange `#F07B2A`, and dark orange `#D46A20` for titles, accents, or overlays where they fit. Let the actual setting, time and light sources determine the scene palette; warmth is not an instruction to add firelight to an unlit scene.
- Treat the earlier *Arcane* reference as shorthand for visibly painted surfaces and expressive lighting. Use Ignite’s own artwork to set the character design and overall look. Flag glossy 3D shading, a clay-render look, and generic vector art when they break the painted style.
- Paint Sol, props and surroundings together with the same brushwork, perspective and coherent light. Shading should communicate the reference form and volume while preserving its proportions. Avoid inflated anatomy, glossy or clay-like rendering, generic vector shapes, heavy grain and excessive decoration.
- Keep identity and performance separate. The [shot guide](shot-integration-and-sol.md#sol-identity) owns character constraints and [purposeful acting](shot-integration-and-sol.md#purposeful-performance-and-prop-contact); the [image guide](image-prompt.md#painted-depth-and-form) explains painted depth and [reference roles](image-prompt.md#reference-roles-and-supplied-assets).

### Painterly surface treatment

This is the shared paint description for image and video prompt authors. Include its concise essentials in independently usable prompts:

```text
Match the approved Ignite artwork: soft, matte gouache-like brushwork, broad simplified shapes, restrained detail, layered color, softened painted edges and subtle paper texture. Paint subjects, props and surroundings together with coherent perspective and lighting. Build rounded forms and space through overlapping painted layers, gentle shading and contact shadows while preserving the reference proportions and volume. Define forms through light and color, without outlines, black strokes or inked edges. Avoid glossy rendering, generic vector shapes, heavy grain and decorative clutter.
```

Preserve Sol's exact geometry while painting the colored surfaces. The red outer flame is a filled layer, not inked linework. Keep navy eyes solid and unchanged. Palette, format and scene contents follow the episode; the supplied seasonal/office prompts establish art direction only.

## Voices and performance

- **Arthur** is the default off-screen narrator. Use Higgsfield’s built-in Arthur voice with a warm nature-documentary delivery, patient pauses, and dry humor.
- **Sol** is the curious student and uses the user's **Higgsfield custom voice named Sol**. Use the exact voice ID and `voice_type: element` in [the shared voice cast](../config/voices.json). Keep Sol mouthless. Time gestures and whole-face orientation to dialogue while preserving his original eye design.
- Label every spoken turn **Narrator:** or **Sol:** in the review script. Let both voices respond to the scene and to each other. Sol can ask a substantive follow-up; his part is not limited to one-word reactions. Preserve existing episode voice overrides, including earlier single-voice Cub narration.
- Use connected, conversational sentences with varied lengths. Arthur's dry humor should come from the situation and delivery. Remove forced slogan endings and repeated clipped clauses. Give an explanation enough words to make its cause and effect clear.
- When Arthur addresses visible Sol, use the [shot guide's Narrator eyeline and acting cues](shot-integration-and-sol.md#purposeful-performance-and-prop-contact). Let each scene choose an expressive gesture, orientation, weight shift or purposeful interaction rather than repeating one listening pose. Keep the narrator off-screen and avoid redundant reaction loops.

## Sol's cartoon expression and movement

Use the [identity and performance rules](shot-integration-and-sol.md#sol-identity) for Sol. Original open oval eyes remain consistent relative to his face with coherent perspective during turns; personality comes from the action and its timing. Anatomy preservation allows expressive staging. The current identity rules supersede the historical eye-morph and squash/stretch examples in earlier discussions.

## Motion style

Specify the movement quality directly. Use stepped, hand-animated pose-to-pose character movement with deliberate silhouettes, connected preparation and action, and brief holds when they clarify the beat. Quieter listening, anticipation and payoff poses are useful choices alongside expressive gestures; no single reaction is the default for every scene. Use the actual lantern video for painted movement and held-pose rhythm, without inheriting its eye changes or imposing its exact action on other episodes.

Requesting a stepped look in generation does not establish exact exposure/frame cadence. Record the stylistic request separately from the editing plan; establish and enforce the exact cadence during editing at **30 fps delivery**, then verify it in playback with the actual voices. Preserve paint and identity between poses. Avoid texture crawl, smeared transitions and blanket frame holds that obscure camera movement or physical contact.

Keep technical movement smooth when stepping would hide contact, engagement or relative motion. Choose camera behavior for the explanation and say whether a push belongs in generation or editing; the [video prompt guide](video-prompt.md#motion-and-continuity) owns those shot instructions. Check the result rather than assuming frame-rate conversion alone produces the desired style.

## Pacing, motion, and type

- Open on the question or a surprising image. Use a close-up or controlled camera push when it reveals an important detail, and a stable view when it serves listening, anticipation or a readable payoff. Hold the reveal long enough to read it.
- Vary clip lengths around the action and dialogue. Keep several lines in one scene when they share an action; use a shorter reaction or cutaway when it adds something. Establish the exact first and last frames of every planned clip. Use normal voice playback and set final timing from the actual recordings.
- Export vertical at **1080 × 1920, 30 fps**. Keep draft durations provisional; the [script guide](video-script-guide.md#dialogue-density-and-timing) owns timing to real normal-rate recordings and removal of unnecessary holds or repeated reactions. The default deliverable remains complete generated clips, including the painted mechanism and motion.
- Set all dialogue and narration captions as editable overlays in Remotion. Use **Ramento** with white fill `#FFFFFF` and Ignite orange outline `#F07B2A` around each letter. Use one or two lines above the social controls, with room around Sol, diagrams, and equations. Use Poppins Bold for headings and Nunito for longer non-caption text when needed.
- Confirm the actual local font family before assembly; a guide's display name can differ from the font filename. Keep per-episode font paths and renderer implementation gaps in the episode handoff. Caption words and timings follow the real voice takes. Keep any optional finishing graphics and sound effects editable; they are not required to explain a mechanism that is already visible in a complete generated clip.
- Keep assembly simple: arrange the complete clips, add separate voices, captions and sound, and export. Make explanatory colors or identifying details part of the generated scene where useful. Do not create SVGs, custom diagrams or separate mechanism animation unless explicitly requested. Additional visual overlays are optional, not a required production stage.

## Review the rendered video

- [ ] The opening reads immediately at phone size.
- [ ] Art texture and lighting feel consistent across adjacent shots.
- [ ] Sol's eyes remain identical to the reference throughout; body poses carry the performance without stretching the mascot. His exact flame layers and proportions stay intact.
- [ ] Sol, props and background all show the same visible gouache brushwork, layered color and paper texture, with no inked outlines.
- [ ] Motion and transitions draw attention to the explanation. The reveal remains visible long enough to understand.
- [ ] Arthur and Sol are distinct in the mix. Captions use the approved Ramento treatment, are timed to both voices, and sit clear of the subject. Replace any visible draft placeholders before release.
- [ ] Dialogue flows like a conversation, explains unfamiliar mechanisms clearly, and resolves the scene without a forced punchline.
- [ ] The clip durations support the performances and visible actions, with continuity between planned first and last frames.
- [ ] Expressive poses and original eye designs read at phone size; each reaction has a clear purpose, cue, target and result. Stepped movement and exact editing cadence have been checked in playback.
- [ ] When the Narrator addresses visible Sol, Sol acknowledges the voice above the camera and the plan explicitly cues any return look at the mechanism.
- [ ] Review the real frames at about 360 × 640 as well as full resolution. The first action, gaze, object identity, contact points and final reaction remain legible, and one or two caption lines clear the platform controls. Planned bounding boxes alone do not establish that finished footage passes this check.

Before generation, also run the shared [final prompt review](checklist.md#final-prompt-review). Keep the caption treatment above and current voice selections; older episode examples and legacy configuration do not replace them.

## References

- *Automate Ignite Videos* chat, Nov. 8, 2026. Painted 2D look, half-frame motion, and the calculus pilot reference frames.
- *Remotion setup and workflow checklist* discussion, Nov. 10, 2026. Painted Ignite art, Zack D. Films pacing, vertical export, and render review.
- *Escalator cartoon direction*, Nov. 13, 2026. Historical camera and acting discussion; its eye morphs and anatomy-changing exaggerations are superseded by the current identity rules.
- [Ignite Program Style Guide.pdf](https://chatgpt.com/library?file_id=libfile_02e662ff436881919a34e6913e985727&account_id=personal)
