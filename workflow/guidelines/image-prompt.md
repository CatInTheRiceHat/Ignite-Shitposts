# Image prompt

Reusable template for generating scene art, reference images, and video keyframes. Place this file in the project's guidelines folder. Use it with [video-prompt.md](video-prompt.md).

## Consistent art direction

Use Ignite's established painted 2D style in every scene. Take the brush texture, edge treatment, palette, and lighting from the approved artwork. Keep shapes simple and readable, with restrained texture and depth from overlapping painted layers and light.

Build a clean, accurate background with the environmental details needed to understand the setting and action. Use correct perspective, believable scale, coherent lighting, and grounded contact shadows. Keep objects purposeful, group secondary shapes simply, and leave breathing room around the focal point. Base technical structures and mechanisms on the supplied references or verified scene plan. Carry their geometry into later views.

Let one action or teaching point lead the composition. Use background contrast and detail sparingly so the subject reads immediately at phone size. Keep decorative effects restrained and use them only when the scene calls for them.

## Reusable painted art direction

Elaine's office, beach and spring examples establish the rendering language.
Carry this treatment into the episode's own setting, palette, lighting and
format. Their character counts, landscape layouts and seasonal props are
specific to those examples.

```text
Use soft gouache-like brushwork, layered color, subtle paper texture and expressive painted shapes. Define forms through light and color, with no outlines, black strokes or inked edges. Paint every visible subject, prop and part of the environment with the same brushwork and surface texture. Keep clear spacing, gentle light and accurate, readable forms.
```

Sol must have visible gouache brushwork on the original colored flame shapes,
rather than retaining a smooth logo finish over a painted background. Keep the
original silhouette, proportions and layer layout while painting those surfaces.
The red outer flame is a filled character layer, not an outline to remove.
Solid navy eyes and charcoal rubber rails are filled shapes/materials; the
linework restriction does not erase their original dark colors.

## Sol identity and continuity

Use the original mascot assets to define every character feature. Mascot.png
sets the neutral silhouette, proportions and eyes; examples such as Curious.png
and Celebrate.png show the short arms and stubby feet in different poses.
Attach a relevant limb example as well as the neutral mascot when needed.
Compare the entire silhouette, nested flame contours and proportions against the original before passing the design. If a layout reference contains a rejected Sol, use a character-free background for the rebuild. Example props and accessories are separate from the character design. The
painted references supply gouache brushwork, layered color, paper texture and light. Pose and perspective
can change while Sol's anatomy and features stay consistent across scenes.

Include this wording in prompts where Sol is visible:

```text
Use the attached mascot artwork as a strict character model. Preserve Sol's exact height-to-width ratio, flame silhouette, nested red/orange/cream layer shapes and widths, original colors, tiny stubby hands and feet. Scale the whole character uniformly; keep these proportions in every pose. Keep the original dark navy oval eyes identical in shape, size, spacing and placement throughout: no reshaping, squinting, widening, closed-eye curves or added eyebrows. Sol is completely mouthless; leave the area beneath the eyes blank, with no nose or extra facial marks. Express action through posture and gestures while keeping the original compact anatomy. Keep the flame shapes solid and intact, without realistic fire effects.
```

## How to fill it in

Read the scene brief and project style guide. Replace the bracketed fields with concrete visual details and remove optional sentences that do not apply. Describe a single moment that can be seen in one image. Use the approved references to establish character identity and visual style.

Keep model selection, aspect ratio, resolution, and attached reference files in the generation settings. Identify each reference's purpose, such as character design, paint treatment, composition, or continuity.

## Main template

```text
Create a [aspect ratio] painted 2D image of [subject] in [setting], using the established style of the attached Ignite artwork.

Frame the scene as a [shot size] from [camera angle]. Place [subject] at [position in frame], facing [direction], in [specific pose]. [Describe the important prop and its position relative to the subject]. Show [contact or spatial relationship that makes the scene understandable].

Use [lighting direction and quality] and the palette and brush treatment of the attached style reference. Match [subject's identifying features] to the attached identity reference. Give the subject and surroundings consistent perspective, scale, lighting, and contact shadows.

Keep the composition simple and clean. Show [essential background features] with accurate placement and proportions. Keep secondary details understated and leave breathing room around the subject.

Make [main focal point] immediately readable. Leave [area] clear for [planned overlay, if any].
```

## End-frame template

Attach the starting image as the composition reference. Choose an ending pose that follows naturally from the planned action. Use this when creating the final still for a video shot.

```text
Use the attached starting image as the composition and style reference. Create the final moment after [action].

[Subject] is now [ending pose], at [ending position], facing [direction]. [Prop] is now [ending state or position]. Show [final contact or spatial relationship].

Carry forward [character features], [scene geometry], [lighting], and the established painted 2D treatment from the starting image. Keep the background simple, accurate, and consistent with the scene. [Describe an intentional camera or scene change only if the shot requires one].
```

## Continuity across images

Track the subject's size, facing direction, limb placement, prop positions, camera height, and light source. For a new camera angle, keep the scene's spatial relationships coherent. For a continuous shot, make the start and end frames visually compatible with the intended movement.

For Ignite scenes, use the approved painted 2D art to set texture and lighting. When Sol appears, preserve his reference design, mouthless face, eyes, flame silhouette, proportions, and limbs. Express the requested emotion through pose and eye direction. Apply the current project guide to any additional character or brand details.

## Review

- The image shows the requested moment, pose, and composition clearly.
- Mascot geometry and painted style are checked independently against their respective references.
- Visible gouache brushwork covers Sol, props and surroundings; there are no inked outlines or realistic fire effects.
- Original eyes stay unchanged and open; the area beneath them remains blank.
- Sol's arms, stubby feet, eyes and flame layers match the original assets and remain the same character across the first/last pair and other clips.
- The background establishes the setting with accurate perspective, scale, and essential details.
- The composition has one clear focus, breathing room, and restrained background detail.
- Props, hands, feet, and surfaces meet where the scene requires contact.
- The frame provides the space needed for captions or teaching graphics in the edit.
- The start and end frames can connect through the planned action.

Use generated art as the scene layer. Add exact captions, logos, equations, and labels from editable assets in the composition when the project calls for them.
