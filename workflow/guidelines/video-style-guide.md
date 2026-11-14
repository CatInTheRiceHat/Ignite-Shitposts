# Ignite video style guide

Use the shared Gemini Omni Flash 1.2 video settings in `../config/generation.json`.
Generate and show the actual first AND last stills to the user, and obtain
explicit approval of both before animation. The current escalator artwork is
not an approved character reference. A dedicated reviewer must inspect actual
footage after generation; colors or successful technical checks do not prove
that Sol matches the original lantern source.

Read this before generating art or editing an Ignite educational short. Pair it with [video-script-guide.md](video-script-guide.md) and [shot-integration-and-sol.md](shot-integration-and-sol.md).

## Art direction

- Use Ignite’s existing **painted 2D** look. Match the approved scene references for brush texture, edge treatment, and lighting. Build depth with overlapping painted layers, value contrast, and gentle parallax.
- The current visual reference is the [Sol lantern video](../episodes/sol_kling_test/clips/sol-lantern-kling.mp4) and its [source frame](../episodes/sol_kling_test/keyframes/sol-lantern.jpg). Match its hand-painted storybook finish on Sol as well as the scenery, original small oval eyes, compact limbs, softly wispy flame tip, gentle performance and brief held poses. Use this concrete reference when broader cartoon directions conflict.
- Keep the staging warm, playful, and easy to read on a phone. Use Ignite cream `#FFF8F0`, orange `#F07B2A`, and dark orange `#D46A20` for titles, accents, or overlays where they fit. Let the subject and reference art guide the scene palette.
- Treat the earlier *Arcane* reference as shorthand for visibly painted surfaces and expressive lighting. Use Ignite’s own artwork to set the character design and overall look. Flag glossy 3D shading, a clay-render look, and generic vector art when they break the painted style.
- Give Sol the same brushwork, perspective, and light as the scene. Use approved Sol art as a character reference for generating the painted keyframe. See the shot guide for the actual generation steps.

## Voices and performance

- **Arthur** is the default off-screen narrator. Use Higgsfield’s built-in Arthur voice with a warm nature-documentary delivery, patient pauses, and dry humor.
- **Sol** is the curious student and uses the user's **Higgsfield custom voice named Sol**. Use the exact voice ID and `voice_type: element` in [the shared voice cast](../config/voices.json). Keep Sol mouthless. Time his eye shapes and body language to the dialogue in the edit.
- Label every spoken turn **Narrator:** or **Sol:** in the review script. Let both voices respond to the scene and to each other. Sol can ask a substantive follow-up; his part is not limited to one-word reactions. Preserve existing episode voice overrides, including earlier single-voice Cub narration.
- Use connected, conversational sentences with varied lengths. Arthur's dry humor should come from the situation and delivery. Remove forced slogan endings and repeated clipped clauses. Give an explanation enough words to make its cause and effect clear.
- When the Narrator speaks directly to Sol and Sol is visible, let Sol break the fourth wall: his eyes lead an upward turn toward a fixed point just above the camera, then his flame body and tip follow. Use curious or listening eye shapes and a readable held pose. The Narrator remains off-screen. When a line directs attention to a mechanism, Sol may follow that cue and then look back up for the response. Record those gaze changes explicitly.
- Stage one clear acknowledgment of Arthur, then let Sol follow the demonstrated object. Add another look upward only when a new spoken exchange requires it. Use eye direction, body lean and held poses for most acting; avoid stacking eye morphs, a double-take, a bounce and a camera move onto one brief reply. The existing eye-shape and squash/stretch permissions below allow accents, not mandatory motion in every beat.

## Sol's cartoon expression and movement

Sol is mouthless. Keep the lantern reference's two small dark oval eyes at their original size, spacing and facial placement throughout the performance. Convey attention through whole-face turns and small body leans. A natural blink may close both eyes together when cued. The current direction replaces the earlier exaggerated eye-morph vocabulary; do not enlarge one eye, collapse one into a dot or replace the pair with crescents. Preserve the painted orange/cream layers and a softly tapering, wispy flame tip.

| Acting intent | Eyes | Supporting pose |
| --- | --- | --- |
| Neutral / listening | Original small paired navy ovals | Compact body and a clear hold |
| Listening to the Narrator | Retain the same oval shapes and proportions | Tip the whole face toward the fixed point just above the camera |
| Curious / questioning | Retain the same paired ovals | Small lean toward the object, then hold |
| Following movement | Retain the same paired ovals | Track with a restrained whole-face turn; body follows slightly |
| Understanding / pleased | Retain the same paired ovals | Relax the body into a quiet, grounded ending pose |

Name the gaze target, body pose and cue for each turn. Keep the flame painted in the same storybook finish as the reference, with brushy layered color and a wispy taper at its tip. Let the tip trail gently after a turn and settle. Match the lantern video's small deliberate movements and held poses while retaining compact limbs and recognizable proportions.

Keep technical parts mechanically accurate while matching the lantern artwork's painted finish. Motion should reveal the explanation clearly, with supported feet, engaged chains and readable roller contact.

## Pacing, motion, and type

- Open on the question or a surprising image. Borrow Zack D. Films’ pacing by using a close-up or camera push to show the detail that answers the question. Hold the reveal long enough to read it.
- Vary clip lengths around the action and dialogue. Keep several lines in one scene when they share an action; use a shorter reaction or cutaway when it adds something. Establish the exact first and last frames of every planned clip. Use normal voice playback and set final timing from the actual recordings.
- Export vertical at **1080 × 1920, 30 fps**. Use the actual lantern video as the reference for the character's movement and held-pose rhythm. Preserve the painted surface and proportions through the motion; changing frame rate alone does not establish that look.
- Keep technical motion smooth when stepped motion would obscure roller contact, chain engagement, or relative movement. Describe this distinction in the video prompt. Use a clear generated camera view; keep it locked when a push would obscure the explanation. The default deliverable is a complete generated clip, including its painted mechanism and motion.
- Set all dialogue and narration captions as editable overlays in Remotion. Use **Ramento** with white fill `#FFFFFF` and Ignite orange outline `#F07B2A` around each letter. Use one or two lines above the social controls, with room around Sol, diagrams, and equations. Use Poppins Bold for headings and Nunito for longer non-caption text when needed.
- Confirm the actual local font family before assembly; a guide's display name can differ from the font filename. Keep per-episode font paths and renderer implementation gaps in the episode handoff. Caption words and timings follow the real voice takes. Keep any optional finishing graphics and sound effects editable; they are not required to explain a mechanism that is already visible in a complete generated clip.
- Keep assembly simple: arrange the complete clips, add separate voices, captions and sound, and export. Make explanatory colors or identifying details part of the generated scene where useful. Do not create SVGs, custom diagrams or separate mechanism animation unless explicitly requested. Additional visual overlays are optional, not a required production stage.

## Review the rendered video

- [ ] The opening reads immediately at phone size.
- [ ] Art texture and lighting feel consistent across adjacent shots.
- [ ] Sol's eye changes match the planned expressions, retain the original color and facial placement, and return to the intended ending pose. His flame design and colors stay recognizable through squash and stretch. He belongs in the same painted space as the props.
- [ ] Motion and transitions draw attention to the explanation. The reveal remains visible long enough to understand.
- [ ] Arthur and Sol are distinct in the mix. Captions use the approved Ramento treatment, are timed to both voices, and sit clear of the subject. Replace any visible draft placeholders before release.
- [ ] Dialogue flows like a conversation, explains unfamiliar mechanisms clearly, and resolves the scene without a forced punchline.
- [ ] The clip durations support the performances and visible actions, with continuity between planned first and last frames.
- [ ] Cartoon poses and eye shapes read at phone size; each reaction has a clear cue, target, and held result.
- [ ] When the Narrator addresses visible Sol, Sol acknowledges the voice above the camera and the plan explicitly cues any return look at the mechanism.
- [ ] Review the real frames at about 360 × 640 as well as full resolution. The first action, gaze, object identity, contact points and final reaction remain legible, and one or two caption lines clear the platform controls. Planned bounding boxes alone do not establish that finished footage passes this check.

## References

- *Automate Ignite Videos* chat, Nov. 8, 2026. Painted 2D look, half-frame motion, and the calculus pilot reference frames.
- *Remotion setup and workflow checklist* discussion, Nov. 10, 2026. Painted Ignite art, Zack D. Films pacing, vertical export, and render review.
- *Escalator cartoon direction*, Nov. 13, 2026. Specific camera framing, intentional eye-shape morphs for a mouthless Sol, and strongly exaggerated cartoon performance.
- [Ignite Program Style Guide.pdf](https://chatgpt.com/library?file_id=libfile_02e662ff436881919a34e6913e985727&account_id=personal)
