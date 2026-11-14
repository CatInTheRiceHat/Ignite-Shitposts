# Ignite shot integration and Sol generation

Develop the shot plan alongside the skit script. Generate Sol **inside the painted keyframes**, then animate those full scenes. The existing Sol image supplies the character design. A production shot should show him interacting with the same space, props, and lighting as everything else.

## Plan the edit

For each clip, record its ID, estimated duration in the edit, setting, framing, source asset or intended generation method, speaker-labeled dialogue, first frame, main action, and last frame. State what will be visible rather than using a vague instruction such as “show how it works.” Choose Sol's role per clip. He can ask, demonstrate, or respond to the explanation. A mechanism view can omit him when it needs the space.

Make framing specific: shot size; camera height relative to Sol or the mechanism; viewing angle and camera side; subject placement; approximate subject size within the vertical frame; foreground, background, and crop boundaries; and the exact starting and ending view for any camera move. Identify the feature that should attract attention first. Keep expression shots large enough for Sol's eye shapes to read, and reserve a stated caption area that does not cover his face or the mechanism.

For every visible character, specify eye shape, gaze target, whole-body pose, and the change that occurs on a named spoken or visual cue. Use the style guide's eye-shape vocabulary and cartoon movement. Record expression and body states separately for the first and last frames. If Sol is off-screen during a line, state that explicitly instead of inventing an invisible pose.

Plan different clip lengths around the dialogue and physical action. A single clip can carry two lines, several sentences, or a short exchange. Cut when the viewpoint or action needs to change; a sentence ending alone does not require a new clip.

For adjacent clips, note what carries across the cut: Sol's pose and location, the tracked object's position, direction of travel, camera side, and lighting. If the next view changes scale, shows a diagram, or skips time, state that explicitly. Keep screen direction consistent unless the transition clearly establishes a new view.

Use the existing calculus pilot as the continuity example. Its painted A → B → C → D progression is **crouch beside the board → land on it → lean into the curve as it wobbles → recover balance**. Reuse the end of one beat as the next starting point when the camera and framing carry through. For a cut to a new angle, match the action and position across the two views.

## Specify the first and last frames

The **first frame** is a still composition: name the camera angle and crop, Sol's exact pose, eye shape, gaze target, and location when present, the important objects, their positions, and the mechanism's starting state. Do not put a sequence of actions into the first-frame description.

The **action** describes how that starting state becomes the ending state. Specify one main physical action, a camera instruction if needed, and the spoken words that cue a reveal. Describe secondary performance only when it supports that action.

The **last frame** is another still composition: state what has moved, where it ended, Sol's ending eye shape and gaze target when present, the resulting body pose or mechanism state, and what the viewer must still be able to see. “Sol reacts” or “finish explaining” is not a usable end frame. If the camera moves, specify its ending crop.

For a continuing clip, reuse the last frame as the next first frame. For a cut to another angle, match the relevant object state and say which spatial details stay consistent. Plan editorial reveals, overlays, and cutaways separately from physical movement so generation does not have to invent a mechanism changing shape.

For a technical explanation, identify what must stay rigid, what rotates or slides, and what causes that movement. Keep labels and measured overlays editable. Use a controlled diagram or Remotion animation when free-form video generation would obscure or distort the explanation.

## Edit duration and generation duration

Record the desired **edit duration** before choosing a provider. Check supported generation lengths when generation is requested. A planned 11-second scene may use two continuing generated segments; it does not imply that a provider accepts an 11-second request. Name each segment's first frame, last frame, and continuity requirements before submitting it.

Use the finished speech at 1× playback to set final clip lengths. Trim a generated hold or extend a scene with a planned continuation when necessary. Do not stretch footage containing mechanical motion or speed up speech to hide a timing mismatch.

## Generate Sol as part of the scene

1. **Choose two references.** Use approved Sol artwork for identity and an approved Ignite scene or frame for paint treatment. Keep Sol mouthless, with his recognizable layered flame design, colors, and tiny stubby limbs. His original dark oval eyes are the neutral pose; intentionally morph those same two shapes into the planned cartoon expressions. Squash and stretch the flame body for acting, then settle into the intended held pose. Flag unplanned facial changes, added mouths, noses, eyebrows, pupils, fingers, or longer limbs. Preserve explicitly locked designs in older approved shots unless a revision is requested.
2. **Generate the whole keyframe.** Describe the location, camera angle, and Sol’s exact pose relative to the prop. Ask for matching brushwork, perspective, scene lighting, and a grounded contact shadow where Sol touches the board or floor. Approve the still at phone size before using it for video. A flat Sol PNG sitting over the scene is a draft placeholder.
3. **Generate the motion.** Feed the approved painted scene to Flow as the start frame. Every clip needs an explicit planned last frame, even when the provider takes only a start image. Supply an approved end image when the chosen mode supports it and the ending state matters. Prompt one main action and one camera instruction at a time. Let that action support multiple dialogue lines when appropriate. For a cut where Sol turns or moves away, make a matching painted pose frame first if the model drifts. If a shot needs a correction, rerender that shot and keep the surrounding approved clips.
4. **Assemble in Remotion.** Import the generated MP4 as the shot’s primary footage, then add the timed voiceover, captions, and sound cues. Use layered artwork in Remotion for diagrams, camera pushes, or simple cutaways. Keep captions and branding editable. Use the project’s existing shot IDs and episode files so regenerated clips can be swapped in. Flow/UseAPI can generate clips when configured, and Remotion can also work from local MP4s.

## Prompt examples for the calculus pilot

**Painted still**

> Create a full vertical painted 2D scene using the approved Ignite scene reference for texture and lighting and the approved Sol artwork for character identity. Sol crouches beside the board at the left side of the curve, facing right. Keep his original flame silhouette, eyes, mouthless face, proportions, and tiny limbs. Paint Sol, the board, and the ground together with the same brushwork and light. Give Sol and the board shadows where they meet the ground. Leave clear space for captions.

**Animate the approved A → B frames**

> Match the approved painted start and landing frames. Sol crouches, makes one short hop onto the board, and lands with a small bend. The board dips slightly under his weight. Hold the camera steady and keep the original painted texture, light, and character design through the whole shot. End on the landing pose so the next shot can continue the motion. Use stepped character motion and let the off-screen narration carry the explanation.

## Check each shot in the edit

- [ ] Sol is painted into the scene, with lighting, scale, and perspective that match the props.
- [ ] The action reads in silhouette and shows or reinforces the narrated idea.
- [ ] The first and last frames each specify a visible state; the action connects them without an unexplained change.
- [ ] The framing specifies shot size, camera height and angle, subject placement and scale, crop, focus, and the start and end of any camera move.
- [ ] Every visible Sol performance specifies eye shapes, gaze targets, body poses, and the cues for expression changes; the shapes read at phone size.
- [ ] Dialogue is labeled Sol or Narrator, and each line matches what is visible at that point in the clip.
- [ ] Clip lengths vary with the scene; longer continuous scenes have a feasible segment plan if needed.
- [ ] Sol’s face, colors, and proportions match the approved reference at the beginning, middle, and end.
- [ ] The board or prop makes believable contact, and direction, pose, and object position make sense across the cut.
- [ ] The generated MP4 occupies the planned shot and the caption sits clear of the action.

## References

- *Automate Ignite Videos* chat, Nov. 8, 2026. The painted calculus pilot, Sol’s A → B → C → D action, and mouthless performance with off-screen narration.
- *Code Flow Integration* chat, Nov. 9, 2026. Existing Flow A → B test, first hop-on clip, and the VS Code workflow.
- *Ignite video workflow guides* discussion, Nov. 10, 2026. Generate Sol in the painted scene so he can act within it.
- *Escalator script feedback*, Nov. 13, 2026. Write the scene alongside the dialogue; specify both endpoint frames and allow several lines within clips of varied lengths.
- *Escalator cartoon direction*, Nov. 13, 2026. Explicit camera placement and composition, eye-shape acting, and cartoon anticipation, squash, stretch, overshoot, and held poses.
- [Ignite_Moodle_Codex_Prompts.txt](https://chatgpt.com/library?file_id=libfile_41e7912a74808191b7964651794becc4&account_id=personal) for the approved mascot design constraints.
