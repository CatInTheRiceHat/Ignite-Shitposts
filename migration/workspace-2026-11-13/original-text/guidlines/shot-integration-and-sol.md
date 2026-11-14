# Ignite shot integration and Sol generation

Use this after writing the script. Generate Sol **inside the painted keyframes**, then animate those full scenes. The existing Sol image supplies the character design. A production shot should show him interacting with the same space, props, and lighting as everything else.

## Plan the edit

For each shot, record its ID, narration beat, duration in the edit, framing, source asset, and one main action. For adjacent shots, note what must carry across the cut, such as Sol’s pose, direction of travel, board position, camera angle, and lighting. Choose Sol’s role per shot. He can set up the problem, demonstrate the action, or react to the payoff. An explanation shot can focus entirely on the mechanism when it needs the space.

Use the existing calculus pilot as the continuity example. Its painted A → B → C → D progression is **crouch beside the board → land on it → lean into the curve as it wobbles → recover balance**. Reuse the end of one beat as the next starting point when the camera and framing carry through. For a cut to a new angle, match the action and position across the two views.

## Generate Sol as part of the scene

1. **Choose two references.** Use approved Sol artwork for identity and an approved Ignite scene or frame for paint treatment. Keep Sol compact and mouthless, with his original eyes, flame silhouette, proportions, colors, and tiny stubby limbs. Use pose, timing, and body lean for expression. Flag added mouths, noses, eyebrows, fingers, longer limbs, or altered eyes.
2. **Generate the whole keyframe.** Describe the location, camera angle, and Sol’s exact pose relative to the prop. Ask for matching brushwork, perspective, scene lighting, and a grounded contact shadow where Sol touches the board or floor. Approve the still at phone size before using it for video. A flat Sol PNG sitting over the scene is a draft placeholder.
3. **Generate the motion.** Feed the approved painted scene to Flow as the start frame. Supply an approved end frame when the chosen mode supports it and the landing pose matters. Prompt one action and one camera instruction at a time. For a cut where Sol turns or moves away, make a matching painted pose frame first if the model drifts. If a shot needs a correction, rerender that shot and keep the surrounding approved clips.
4. **Assemble in Remotion.** Import the generated MP4 as the shot’s primary footage, then add the timed voiceover, captions, and sound cues. Use layered artwork in Remotion for diagrams, camera pushes, or simple cutaways. Keep captions and branding editable. Use the project’s existing shot IDs and episode files so regenerated clips can be swapped in. Flow/UseAPI can generate clips when configured, and Remotion can also work from local MP4s.

## Prompt examples for the calculus pilot

**Painted still**

> Create a full vertical painted 2D scene using the approved Ignite scene reference for texture and lighting and the approved Sol artwork for character identity. Sol crouches beside the board at the left side of the curve, facing right. Keep his original flame silhouette, eyes, mouthless face, proportions, and tiny limbs. Paint Sol, the board, and the ground together with the same brushwork and light. Give Sol and the board shadows where they meet the ground. Leave clear space for captions.

**Animate the approved A → B frames**

> Match the approved painted start and landing frames. Sol crouches, makes one short hop onto the board, and lands with a small bend. The board dips slightly under his weight. Hold the camera steady and keep the original painted texture, light, and character design through the whole shot. End on the landing pose so the next shot can continue the motion. Use stepped character motion and let the off-screen narration carry the explanation.

## Check each shot in the edit

- [ ] Sol is painted into the scene, with lighting, scale, and perspective that match the props.
- [ ] The action reads in silhouette and shows or reinforces the narrated idea.
- [ ] Sol’s face, colors, and proportions match the approved reference at the beginning, middle, and end.
- [ ] The board or prop makes believable contact, and direction, pose, and object position make sense across the cut.
- [ ] The generated MP4 occupies the planned shot and the caption sits clear of the action.

## References

- *Automate Ignite Videos* chat, Nov. 8, 2026. The painted calculus pilot, Sol’s A → B → C → D action, and mouthless performance with off-screen narration.
- *Code Flow Integration* chat, Nov. 9, 2026. Existing Flow A → B test, first hop-on clip, and the VS Code workflow.
- *Ignite video workflow guides* discussion, Nov. 10, 2026. Generate Sol in the painted scene so he can act within it.
- [Ignite_Moodle_Codex_Prompts.txt](https://chatgpt.com/library?file_id=libfile_41e7912a74808191b7964651794becc4&account_id=personal) for the approved mascot design constraints.
