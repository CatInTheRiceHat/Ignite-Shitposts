# Video prompt

Reusable template for animating approved endpoint images through Higgsfield. Use the current model and input roles in [generation.json](../config/generation.json); historical Flow examples do not replace that configuration. Prepare keyframes with [image-prompt.md](image-prompt.md).

## Consistent art direction

Carry Ignite's established painted 2D look from the approved keyframes through the whole clip. Preserve the reference brushwork, simple shapes, character design, and lighting. Keep the background clean and accurate, with coherent perspective, scale, object placement, and contact.

Animate only the elements needed for the shot. Keep background movement restrained, maintain breathing room around the subject, and direct attention to one clear action. Use effects only when the scene brief calls for them; Sol stays particle-free under the current shared movement rule. Preserve technical geometry throughout the motion.

When Sol is visible, include the essential [identity constraints](shot-integration-and-sol.md#sol-identity) and write his [performance direction](shot-integration-and-sol.md#purposeful-performance-and-prop-contact) separately. Preserve anatomy through purposeful gestures and interactions. Omit character boilerplate in a cutaway without him.

## Reusable painted art direction

Use the [style guide's shared paint treatment](video-style-guide.md#painterly-surface-treatment). Include its concise essentials in each finished video prompt rather than expecting the generator to read a local guide.

Carry that finish from the approved first frame through the whole clip,
including Sol's colored layers and all visible props. Keep the brushwork stable
over time and preserve source contours, proportions and material contacts.
The original eyes remain unchanged; perform through posture, gesture and the requested coordinated bouncy flame-like follow-through.
The scene determines format, palette and subject count.

## How to fill it in

Read the scene brief, approved keyframes and project style guide. Put the scene, subject and main visible action or result first, then its connected stages, camera, movement quality, concise style and identity, and essential constraints. Use concrete verbs and visible outcomes. Each prompt must work independently with its declared endpoints and inputs.

Record model, aspect ratio, duration, resolution, audio policy and actual reference files outside the copyable prompt, using the current generation configuration. Record [reference roles and supplied assets](image-prompt.md#reference-roles-and-supplied-assets); paths must map to inputs actually supplied. Keep dialogue, caption content and editing-only moves outside the visual-generation block. Prompt writing does not authorize a media job.

## Main template

```text
[In this scene, subject] [one main action], ending with [visible result]. Begin in [starting pose or state] from the approved first frame.

[Describe the closely connected stages in physical order, including direction, support, grip or release where relevant]. End on [exact pose, contact and object state] from the approved last frame. [Include a brief hold only when it serves the beat].

[One camera choice, with starting and ending view if it moves]. Use [movement quality appropriate to the subject and action].

[Concise approved matte paint treatment and applicable identity constraints]. Preserve [essential geometry, lighting and spatial relationships]. [Only necessary shot-specific exclusions].
```

## Short version

Use this when the starting image already establishes the scene clearly.

```text
[Subject in the scene] [specific action and direction], from [starting state] to [exact visible result]. [One camera choice]. [Essential contact and movement quality]. Preserve [applicable identity constraints], [concise matte paint treatment] and [essential geometry and light].
```

## Optional transformation or reveal

Use this structure when the scene depends on a change of state. Identify what changes, where it happens, and what completes before the next movement begins.

```text
[Element in the scene] changes from [initial state] into [final state] through [specific visible transition]. [One camera choice]. Show [required contact or cause] before [result]. Once [completion condition], [connected stage or brief hold]. Finish in [final composition]. Preserve [concise paint treatment, applicable identity, geometry and lighting conditions].
```

## Motion and continuity

Give each clip one teaching purpose and one main visible action. Closely connected stages can form that action when their order is clear, such as placement, support, release and withdrawal. For a complicated sequence, simplify it or declare continuing subscenes and endpoints in the shot plan. Sol's appearance should contribute to the beat; a mechanism-focused cutaway can omit him.

Use the exact [shared motion rules](video-style-guide.md#motion-style): animate on twos, holding each pose or painted state unchanged for two consecutive frames of the final 30 fps timeline (15 pose updates per second). Longer holds use complete pairs; action and playback remain normal speed. Apply this to every visible animated subject, including hands, moving props, flames and animated local lighting. Keep background and painted texture stable, without interpolation, blending, optical-flow smoothing or concealing motion blur. Include applicable subjects in each independently usable prompt.

Specify short direct gesture paths, original attachment points and constant limb lengths. Sol moves through each gesture with a gentle connected body/tip wiggle, following the [particle-free movement rule](video-style-guide.md#particle-free-sol-movement). Keep feet supported and all colored shapes attached. During visible Narrator turns, establish attention to the fixed above-camera voice before the first word and keep gentle listening idle throughout. Avoid unrelated windups, repeated arm gestures, large bounce loops, unplanned hops or camera movement. Hands, held props and mechanisms retain their planned physical motion; Sol’s performance style is not a blanket instruction to bounce every object. Keep Sol’s face anchored to his body and both normal-height eye ovals uniformly navy #1C2447, with a brief natural blink allowed and no eye squish, highlights, whites, extra pupils, winks or drift. Aim for this during generation; enforce and verify exact two-frame cadence during editing.

Choose the camera for the teaching purpose: a close-up for a critical contact, a controlled push for a reveal, or a stable view for listening, anticipation or payoff. Specify size, height, angle, side and crop; a generated move needs explicit start and end views. Record whether each move belongs in generation or editing. For an editorial push, generate a stable source and put crop instructions outside the copyable block. A smooth digital move may follow cadence enforcement on the source footage; check crops throughout the move. Do not perform the push twice.

Match the ending pose, prop state, screen direction and light to the next shot. Include the [mandatory Narrator attention cue](shot-integration-and-sol.md#narrator-attention-and-listening-idle) when Sol is visible; use a short silent gaze-ready lead-in if continuity begins with another gaze. Reuse an approved ending asset unchanged when the next starting state is exact, following the [endpoint rules](shot-integration-and-sol.md#specify-the-first-and-last-frames). Keep lighting causal: an unlit starting object cannot already cast light from its later ignition.

For Ignite scenes, carry the approved painted 2D treatment through the motion. When Sol appears, preserve his reference features and mouthless face, using the scripted gesture or listening hold to convey his reaction without independent face or eye movement. Follow the current voice configuration when adding dialogue in the edit.

## Remove boilerplate and contradictions

Check every sentence against what is actually visible. Remove references to absent hands, characters, tools, fire, mechanisms or scenery; correct object counts and the initial lighting state. Keep optional glow, particles and movement only when the shot needs them. Keep essential identity and style instructions concise instead of repeating unrelated template restrictions. Timing follows the [recorded-dialogue policy](video-script-guide.md#dialogue-density-and-timing); trim unnecessary holds and repeated reactions while preserving readable actions.

Run the shared [final prompt review](checklist.md#final-prompt-review) before using the prompt. Loading-animation loop or rotation requirements remain scoped as described in the [guideline scope](README.md#scope-and-rule-owners).

## Review and revise

- Read the actual script/storyboard first, then inspect the entire clip against each spoken turn, visual cue and planned/recorded speaker window.
- Check character identity, prop shape, contact, movement direction and the intended stable or moving camera behavior.
- Compare Sol's arms, feet, eyes and flame layers with the source assets through the clip and across scene cuts; reject growth, reshaping or a different mascot design.
- Check visible gouache brushwork, layered color and paper texture on Sol as well as the props and environment; reject a smooth logo-like character on a painted background.
- Keep the original open oval design through the clip; a brief natural blink may close and reopen both eyes and return promptly to those ovals. Reject unrelated expressive eye reshaping, prolonged squinting or repeated blinking loops.
- Check that painted shapes stay consistent and the background retains accurate geometry and scale.
- Check that motion and effects support the main action and keep the frame easy to read.
- Verify unchanged source poses in exact consecutive two-frame pairs on the final 30 fps timeline, with normal-speed action and complete-pair longer holds. Inspect every animated subject, facial markings and physical contacts; inspect source cadence before any smooth editorial camera transform and check final crops in playback.
- Verify that a transformation completes in the intended order and ends in the specified state.
- Check that the next shot continues naturally from the final pose. Verify upward gaze and gentle idle during every visible Narrator turn, including the transitions into and out of speech; an up-looking last frame alone is insufficient.

If a take fails, identify the visible error and change the relevant prompt sentence or reference frame. Simplify competing actions, clarify direction or contact, and use closer start/end poses when needed. Compare the revised take against the same intended result.

Use the project editor to time voice tracks, sound effects, captions, logos, equations, and precise overlays. Keep the visual generation prompt focused on the action the clip must show.
