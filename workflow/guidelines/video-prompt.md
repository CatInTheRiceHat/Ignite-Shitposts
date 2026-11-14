# Video prompt

Reusable template for animating approved images in Flow or another video generator. Place this file in the project's guidelines folder. Prepare keyframes with [image-prompt.md](image-prompt.md).

## Consistent art direction

Carry Ignite's established painted 2D look from the approved keyframes through the whole clip. Preserve the reference brushwork, simple shapes, character design, and lighting. Keep the background clean and accurate, with coherent perspective, scale, object placement, and contact.

Animate only the elements needed for the shot. Keep background movement restrained, maintain breathing room around the subject, and direct attention to one clear action. Use particles, glow, camera shake, and other effects only when the scene brief calls for them. Preserve technical geometry throughout the motion.

## How to fill it in

Read the scene brief, approved keyframes, and project style guide. Choose the main action, camera behavior, starting state, and ending state. Replace the bracketed fields and remove optional sentences that do not apply. Use concrete verbs and visible outcomes.

Record the selected model, aspect ratio, duration, resolution, audio setting, and actual reference files alongside the prompt. Use the project's selected Omni Flash model for Flow work and the controls available in that generation mode. Set clip length from the action and edit timing.

## Main template

```text
[Camera instruction]. Begin with [subject] in [starting pose or state], as shown in the attached starting frame.

[Subject] [one main action] toward [direction or destination], with [speed and movement quality]. [Describe essential contact, weight, or interaction with the prop or surface].

End with [subject] in [ending pose or state]. [Finish on the attached end frame, when supplied]. [Hold the final pose for a duration suited to the edit, if needed].

Preserve [important identity features], the established painted 2D brushwork, and [scene details essential to continuity] from the references. Keep the composition clean and the background geometry, scale, and lighting consistent throughout the motion.
```

## Short version

Use this when the starting image already establishes the scene clearly.

```text
[Camera instruction]. [Subject] [specific action and direction]. [Describe the essential contact or movement quality]. End [exact visible result]. Preserve [key features], the established painted 2D style, and the clean, accurate background from the reference.
```

## Optional transformation or reveal

Use this structure when the scene depends on a change of state. Identify what changes, where it happens, and what completes before the next movement begins.

```text
[Camera instruction]. Begin with [initial state]. [Element] changes into [final state] through [specific visible transition]. As this happens, [describe the required relationship between the elements]. Once [completion condition], [next movement or final hold]. Finish in [final composition].
```

## Motion and continuity

Give each clip one main action. Closely connected stages can share a shot when their order is clear. For a complicated sequence, create compatible intermediate frames or divide it into readable beats.

Specify movement quality precisely, such as a single quick movement, a slow lean, a controlled rotation, or a glide that settles. Describe the intended direction and stopping point. For a prop interaction, state where contact occurs and how the prop responds.

Choose one camera instruction that supports the action. Match the ending pose and direction to the next shot. If the art calls for stepped animation, request that quality for the relevant movement and check the result in playback. Set exact frame cadence in the edit when needed.

For Ignite scenes, carry the approved painted 2D treatment through the motion. When Sol appears, preserve his reference features and mouthless face, using body language and eye direction to convey his reaction. Follow the current voice configuration when adding dialogue in the edit.

## Review and revise

- Play the clip and inspect the beginning, middle, and end for the requested action and timing.
- Check character identity, prop shape, contact, movement direction, and camera stability.
- Check that brushwork and simple shapes stay consistent, and the background retains accurate geometry and scale.
- Check that motion and effects support the main action and keep the frame easy to read.
- Verify that a transformation completes in the intended order and ends in the specified state.
- Check that the next shot continues naturally from the final pose.

If a take fails, identify the visible error and change the relevant prompt sentence or reference frame. Simplify competing actions, clarify direction or contact, and use closer start/end poses when needed. Compare the revised take against the same intended result.

Use the project editor to time voice tracks, sound effects, captions, logos, equations, and precise overlays. Keep the visual generation prompt focused on the action the clip must show.
