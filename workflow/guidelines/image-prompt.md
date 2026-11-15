# Image prompt

Reusable template for generating scene art, reference images, and video keyframes. Place this file in the project's guidelines folder. Use it with [video-prompt.md](video-prompt.md).

## Consistent art direction

Use Ignite's established soft, matte painted style in every scene. Match the approved artwork's broad simplified shapes, restrained detail, subtle paper texture, softened painted edges and layered color. The [style guide](video-style-guide.md#painterly-surface-treatment) owns the shared paint treatment; include its essential description in each finished prompt.

Build a clean, accurate background with the environmental details needed to understand the setting and action. Use correct perspective, believable scale, coherent lighting, and grounded contact shadows. Keep objects purposeful, group secondary shapes simply, and leave breathing room around the focal point. Base technical structures and mechanisms on the supplied references or verified scene plan. Carry their geometry into later views.

Let one action or teaching point lead the composition. Use background contrast and detail sparingly so the subject reads immediately at phone size. Keep decorative effects restrained and use them only when the scene calls for them.

## Painted depth and form

Build depth through overlapping foreground, middle-ground and background shapes, gentle shading, coherent perspective and contact shadows. Rounded forms and readable space belong in painted 2D. Preserve the reference character's proportions and volume while shading the existing design; do not inflate, stretch or flatten it into a different body shape.

Paint Sol, props and scenery together with consistent brushwork, perspective and illumination. Keep texture subtle; heavy grain, glossy surfaces, generic vector shapes and decorative clutter obscure the approved look. Match lighting to the actual moment: a light source cannot illuminate the starting frame before it exists. If illumination changes, name the cause and local extent of the change.

Sol must have visible gouache brushwork on the original colored flame shapes,
rather than retaining a smooth logo finish over a painted background. Keep the
original silhouette, proportions and layer layout while painting those surfaces.
The red outer flame is a filled character layer, not an outline to remove.
Solid navy eyes and other dark materials are filled shapes/materials; the
linework restriction does not erase their original dark colors.

## Reference roles and supplied assets

Record each actual input and its role outside the copyable prompt:

| Role | What it controls |
| --- | --- |
| Identity | Original `Mascot.png` and relevant limb examples from [sol-references.json](../config/sol-references.json): character anatomy, colors and features. |
| Style | Approved Ignite scenes such as `Spring.jpg`, `Practical Learning.jpg` and `Thank You.jpg` in `workflow/assets/reference-art/`: paint, edge treatment, depth and light. |
| Composition | The approved starting still: camera, crop, subject scale and object placement. |
| Continuity | An approved preceding endpoint: the specific pose, prop state and lighting that carry forward. |

A file may serve more than one role; say which. Inspect the supplied artwork and do not inherit its unrelated props, character counts, season, layout or format. A limb example supplies anatomy, not an automatic accessory. A rejected mascot cannot supply identity; use a character-free layout when rebuilding it.

Verify that every reference path exists and maps to a file or media input actually supplied to that generation request. Mentioning a path in prose does not attach an image. Label future endpoints as planned until they exist and are approved; never describe an unsupplied or rejected image as an approved input.

## Sol identity and continuity

The [shot guide](shot-integration-and-sol.md#sol-identity) owns Sol's identity constraints and reusable identity wording. Include the essential constraints when he is visible, then write the shot's pose separately using its [performance guidance](shot-integration-and-sol.md#purposeful-performance-and-prop-contact). Original assets define anatomy. For settled endpoints of an arm-led gesture, keep the same facing direction, face/eye design, ground contacts and reference proportions; change the specified arm positions with their original lengths and attachment points. The connecting video may have the small coordinated bouncy body/flame wobble specified in the [motion style](video-style-guide.md#motion-style), settling back into this endpoint. Do not make an intermediate elastic pose the default final pose. A change of facing direction belongs only in an explicitly scripted action; wobble does not create a separate head. Intentional paired eye-gaze shifts are allowed for the mandatory above-camera Narrator glance while preserving eye design and face attachment. Both eye ovals remain uniformly navy #1C2447 with their reference shape, size and spacing; no highlights, whites or extra pupils. Omit character instructions when the shot has no Sol.

## How to fill it in

Read the scene brief and project style guide. Write in this order: scene, subject, visible pose or state, camera, style and identity, then essential constraints. Describe a single moment rather than an action sequence. Put the focal information first, and remove every optional sentence that does not fit the current objects, lighting, character count or starting state.

Each finished prompt must be independently usable with its declared inputs. Include concise paint and applicable identity instructions; a cross-reference to a local guide is for the prompt author and does not replace instructions the generator needs.

Keep model selection, aspect ratio, resolution, and attached reference files in the generation settings. Identify each reference's purpose, such as character design, paint treatment, composition, or continuity.

## Main template

```text
Create a painted still of [subject] in [setting]. [Subject] is [specific static pose or state], facing [gaze target or direction]. [Describe the important prop and its contact or spatial relationship].

Frame as a [shot size] from [camera height, angle and side]. Place [subject] at [position and scale], with [crop and essential background layers].

Use [lighting source, direction and quality appropriate to this moment]. [Include the concise matte paint treatment and essential identity constraints from the relevant guides]. Give all subjects consistent perspective, rounded form and contact shadows.

Make [one focal point] immediately readable, with simple secondary shapes and breathing room. [Include only shot-specific constraints and any space needed for editable overlays].
```

## End-frame template

Attach the approved starting image as the composition reference. Describe the intended change first, then state what stays consistent: composition, geometry, identity and lighting. Name any planned camera or lighting change explicitly, including the ending crop or new light source. Choose a final state reachable through the planned action without a hidden cut. For a Narrator-listening endpoint, depict Sol looking up to the fixed above-camera voice in a neutral phase of gentle idle. If speech starts at the cut, the starting frame must already support that gaze; otherwise explicitly place a short silent gaze transition before the voice begins. If an old endpoint includes an unrequested face turn or a redesigned settled body, replace it or reuse a matching existing asset before animation; do not ask the video prompt to ignore a conflicting supplied image.

```text
Use the attached starting image as the composition and style reference. Create the final moment after [action].

[Subject] is now [ending pose], at [ending position], facing [direction]. [Prop] is now [ending state or position]. Show [final contact or spatial relationship].

Preserve [composition and crop], [character identity], [scene geometry and contacts] and [lighting]. [Describe a planned camera or light change only if required]. Include the concise matte paint treatment and any applicable identity constraints. Keep the background simple and consistent.
```

## Continuity across images

Track the subject's size, facing direction, facial markings, limb placement, prop positions, camera height, and light source. For a new camera angle, keep the scene's spatial relationships coherent. For a continuous shot, make the start and end frames visually compatible with the intended movement.

When continuity is exact, reuse the approved last image as the next starting asset unchanged; do not regenerate a lookalike. Keep both endpoint entries, label the reuse, and record the source and destination paths as described in the [shot guide](shot-integration-and-sol.md#specify-the-first-and-last-frames). A new angle uses the earlier endpoint as a continuity reference rather than claiming an exact asset reuse.

## Review

- The image shows the requested moment, pose, and composition clearly.
- Mascot geometry and painted style are checked independently against their respective references.
- Visible gouache brushwork covers Sol, props and surroundings; there are no inked outlines or realistic fire effects.
- First/last stills keep the original oval eyes open and unchanged, with the area beneath them blank. The connecting video may use a brief natural blink under the [motion style](video-style-guide.md#motion-style).
- Sol's arms, stubby feet, eyes and flame layers match the original assets and remain the same character across the first/last pair and other clips.
- Simple painted layers establish the setting with believable depth, gentle shading, accurate perspective, scale and essential details.
- The composition has one clear focus, breathing room, and restrained background detail.
- Props, hands, feet, and surfaces meet where the scene requires contact.
- The frame provides the space needed for captions or teaching graphics in the edit.
- The start and end frames can connect through the planned action.

Finish with the shared [final prompt review](checklist.md#final-prompt-review), including lighting contradictions, leftover objects, supplied references and endpoint reuse.

Use generated art as the scene layer. Add exact captions, logos, equations, and labels from editable assets in the composition when the project calls for them.
