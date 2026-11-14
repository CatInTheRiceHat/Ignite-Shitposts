# Ignite video style guide

Read this before generating art or editing an Ignite educational short. Pair it with [video-script-guide.md](video-script-guide.md) and [shot-integration-and-sol.md](shot-integration-and-sol.md).

## Art direction

- Use Ignite’s existing **painted 2D** look. Match the approved scene references for brush texture, edge treatment, and lighting. Build depth with overlapping painted layers, value contrast, and gentle parallax.
- Push the staging and performance into an emphatic **cartoon** style: bold silhouettes, simplified rounded scenery, strong readable poses, elastic character movement, fast takes, and held reactions. Keep the painted surface treatment. The older Arcane shorthand below refers to brushwork; it does not set a realistic performance or cinematic mood.
- Keep the staging warm, playful, and easy to read on a phone. Use Ignite cream `#FFF8F0`, orange `#F07B2A`, and dark orange `#D46A20` for titles, accents, or overlays where they fit. Let the subject and reference art guide the scene palette.
- Treat the earlier *Arcane* reference as shorthand for visibly painted surfaces and expressive lighting. Use Ignite’s own artwork to set the character design and overall look. Flag glossy 3D shading, a clay-render look, and generic vector art when they break the painted style.
- Give Sol the same brushwork, perspective, and light as the scene. Use approved Sol art as a character reference for generating the painted keyframe. See the shot guide for the actual generation steps.

## Voices and performance

- **Arthur** is the default off-screen narrator. Use Higgsfield’s built-in Arthur voice with a warm nature-documentary delivery, patient pauses, and dry humor.
- **Sol** is the curious student and uses **Cub (Female)** for short questions and reactions. Keep Sol mouthless. Time his body language to the dialogue in the edit.
- Label every spoken turn **Narrator:** or **Sol:** in the review script. Let both voices respond to the scene and to each other. Sol can ask a substantive follow-up; his part is not limited to one-word reactions. Preserve existing episode voice overrides, including earlier single-voice Cub narration.
- Use connected, conversational sentences with varied lengths. Arthur's dry humor should come from the situation and delivery. Remove forced slogan endings and repeated clipped clauses. Give an explanation enough words to make its cause and effect clear.

## Sol's cartoon expression and movement

Sol is mouthless. His two dark eye shapes are expressive drawing shapes and may morph intentionally. Keep their original dark color, their home positions on the cream face, and their neutral oval design as the reset pose. A planned eye-shape change is an expression, not a character-design error. Do not add white eyeballs, pupils, eyebrows, a mouth, or new facial features to create that expression.

| Acting intent | Eye drawing | Supporting pose |
| --- | --- | --- |
| Neutral / listening | Original paired dark vertical ovals | Compact upright body |
| Surprise / double-take | Both eyes pop into larger round shapes | Quick backward lean, brief upward stretch, flame tip follows late |
| Curious / questioning | One eye taller, the other shorter and slightly flatter | Whole body tilts toward the object being examined |
| Concentrating | Two narrow horizontal shapes | Slight forward lean and short still hold |
| Following movement | Ovals lean or compress toward the tracked object's side while staying on the face | Body and flame tip turn after the eyes |
| Understanding / delight | Two upward-arched closed-eye crescents | Anticipation squash, small bounce, then a relaxed settle |

Specify the starting eye shape, the dialogue or visual cue for the change, the target shape, and the ending shape in each character clip. Also name the object or off-screen location Sol is looking toward. “Sol looks curious” alone is insufficient direction.

Use strong anticipation, squash and stretch, overshoot, follow-through, and short smear poses where they clarify an action. Let Sol's flame body compress and extend expressively while retaining its recognizable layered flame design, colors, and stubby limbs. Use pose changes with a roughly 12 fps feel inside the 30 fps edit. Hold the important expression long enough to read on a phone. Use a single main reaction at a time rather than continuously bouncing every feature.

Apply cartoon exaggeration to performance, camera accents, arrows, and attention effects. Mechanical parts must retain the geometry and motion that make the explanation correct. For example, a spotlight ring may spring into place around a chain wheel while the wheel and attached chain keep their consistent motion.

## Pacing, motion, and type

- Open on the question or a surprising image. Borrow Zack D. Films’ pacing by using a close-up or camera push to show the detail that answers the question. Hold the reveal long enough to read it.
- Vary clip lengths around the action and dialogue. Keep several lines in one scene when they share an action; use a shorter reaction or cutaway when it adds something. Establish the exact first and last frames of every planned clip. Use normal voice playback and set final timing from the actual recordings.
- Export vertical at **1080 × 1920, 30 fps**. For the painted half-frame feel, use stepped character poses with a roughly 12 fps feel where it suits the action. Camera pushes, caption timing, and the final render can stay smooth at 30 fps.
- Set all dialogue and narration captions as editable overlays in Remotion. Use **Ramento** with white fill `#FFFFFF` and Ignite orange outline `#F07B2A` around each letter. Use one or two lines above the social controls, with room around Sol, diagrams, and equations. Use Poppins Bold for headings and Nunito for longer non-caption text when needed.

## Review the rendered video

- [ ] The opening reads immediately at phone size.
- [ ] Art texture and lighting feel consistent across adjacent shots.
- [ ] Sol's eye changes match the planned expressions, retain the original color and facial placement, and return to the intended ending pose. His flame design and colors stay recognizable through squash and stretch. He belongs in the same painted space as the props.
- [ ] Motion and transitions draw attention to the explanation. The reveal remains visible long enough to understand.
- [ ] Arthur and Sol are distinct in the mix. Captions use the approved Ramento treatment, are timed to both voices, and sit clear of the subject. Replace any visible draft placeholders before release.
- [ ] Dialogue flows like a conversation, explains unfamiliar mechanisms clearly, and resolves the scene without a forced punchline.
- [ ] The clip durations support the performances and visible actions, with continuity between planned first and last frames.
- [ ] Cartoon poses and eye shapes read at phone size; each reaction has a clear cue, target, and held result.

## References

- *Automate Ignite Videos* chat, Nov. 8, 2026. Painted 2D look, half-frame motion, and the calculus pilot reference frames.
- *Remotion setup and workflow checklist* discussion, Nov. 10, 2026. Painted Ignite art, Zack D. Films pacing, vertical export, and render review.
- *Escalator cartoon direction*, Nov. 13, 2026. Specific camera framing, intentional eye-shape morphs for a mouthless Sol, and strongly exaggerated cartoon performance.
- [Ignite Program Style Guide.pdf](https://chatgpt.com/library?file_id=libfile_02e662ff436881919a34e6913e985727&account_id=personal)
