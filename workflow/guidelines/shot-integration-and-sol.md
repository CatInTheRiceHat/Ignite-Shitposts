# Ignite shot integration and Sol generation

Current model: Gemini Omni Flash 1.2 (`gemini_omni_flash_1_2`), image-to-video,
with both user-approved endpoint stills. Read `../config/generation.json`.
FIRST prepare both endpoint stills (generate or reuse as specified), THEN show
both to the user and wait for explicit approval of that pair, THEN submit the
Higgsfield clip. The model's paired-frame
limit is 3–10 seconds; split longer scenes into declared continuing subscenes.
Follow `clip-review-guide.txt` for independent review and production gates.

Develop the shot plan alongside the skit script. When Sol appears, generate him **inside the painted keyframes**, then animate those full scenes. The existing Sol image supplies the character design. A production shot should show him interacting with the same space, props, and lighting as everything else.

## Sol identity

Use the original mascot artwork and relevant examples in [sol-references.json](../config/sol-references.json) for the complete design. Preserve compact height-to-width proportions and reference volume, the asymmetric flame silhouette and side lobes, nested red/orange/cream contours and layer widths, original colors, and tiny rounded arms and stubby feet at their original lengths and attachment points. Preserve the broad cream inner flame and softly tapering wispy tip. Allow small coordinated action-driven flex while retaining that recognizable design and settled endpoint form. Paint it using the [style treatment](video-style-guide.md#painterly-surface-treatment).

Keep both eye ovals uniformly navy #1C2447, preserving their reference shape, size, low placement and close spacing. A brief natural blink may close and reopen both eyes, returning promptly to the original open ovals. No highlights, whites, extra pupils, winks, prolonged squinting, unrelated expressive reshaping or facial-feature drift. His face is part of his body: allow only intentional coherent paired eye-gaze shifts inside the face; do not detach/rotate the face as a separate head, introduce a neck, or permit accidental feature drift. Small bouncy body motion and flame-tip/lobe follow-through are allowed under the current [motion style](video-style-guide.md#motion-style), with the eye ovals unchanged and attached to the coherent face. A face turn remains a separate scripted choice. Sol is completely mouthless, with the area beneath the eyes blank. Exclude noses, eyebrows, other added facial features, fingers, elongated limbs, ankles, shoes and a separate humanoid torso. The filled flame body remains intact; do not apply realistic fire effects to it. Bouncy motion keeps the primary tips, lobes and nested layers connected. Follow the [particle-free movement rule](video-style-guide.md#particle-free-sol-movement): no detached flicks, sparks, droplets, holes or floating pieces; use attached body/tip wiggle.

Keep these identity constraints separate from the shot's performance direction.

Check the space between the eyes relative to their width against the original mascot, allowing coherent perspective. Do not spread them toward the edges of the cream face. An eye-spacing correction moves the existing ovals horizontally inward while preserving their size, shape, dark fill, height and the accepted scene treatment.

Include concise identity wording in each independently usable prompt where Sol appears:

```text
Match the original Sol artwork exactly: compact reference proportions and volume, asymmetric flame silhouette, original red/orange/cream contours and layer widths, short rounded arms and tiny stubby feet. Keep both original eye ovals uniformly navy #1C2447 and unchanged in shape, size, spacing and low placement. A brief natural blink is allowed, returning promptly to the original open ovals. No highlights, whites, extra pupils, winks or drift. His face is part of his body: allow only scripted coherent paired gaze shifts; do not detach the face, add a neck or permit unmotivated feature drift. Keep him completely mouthless and blank beneath the eyes. No nose, eyebrows, added facial features, fingers, elongated limbs or separate humanoid torso. Preserve the softly tapering tip and coherent filled flame layers; allow a small action-driven bouncy wobble that settles back to reference proportions, without inflating the character or lengthening limbs.
```

## Purposeful performance and prop contact

Choose a readable action that explains why Sol is in this shot. Anatomy preservation allows expressive gestures, body orientation, weight shifts, steps and purposeful interactions within his actual limb range. Do not make "feet planted, arms at sides, small lean, look upward, hold" the default for every scene. A quiet listening or payoff pose is useful when it contributes to the explanation; it should be a deliberate choice.

Name the initial pose, gaze target, main action, ending pose and spoken or visual cue. Closely connected stages can form one action. Examples include a small direct single-arm lift, lowering a presenting arm once to listen, or opening both arms once into a low gesture of understanding; these are options rather than a required sequence. Preserve original arm lengths and attachment points. Move the specified limb directly between clear positions. Let the movement create a gentle connected body/tip wiggle, then settle; keep feet supported and emit no particles. Preserve the face and all nested layers coherently. Do not add unrelated anticipation, windup, repeated nodding, perpetual swaying, extra steps or camera movement. Follow the exact [on-twos motion policy](video-style-guide.md#motion-style).

### Narrator attention and listening idle

This is mandatory for all educational scenes: **whenever the Narrator speaks and Sol is visible, Sol looks UP toward a fixed point just above the camera and maintains gentle listening idle for the whole spoken turn.** Establish the gaze before the first word; do not wait until the last frame. If exact frame continuity starts with Sol looking at the mechanism, use a short silent gaze transition before the Narrator's audio begins.

Move the original navy eye ovals coherently as a pair for a readable upward glance, retaining their normal shapes, sizes, close spacing and low resting placement. A slight coherent body/face angle can support the gaze; Sol has no separate head or neck. Scripted gaze movement is allowed, while accidental facial sliding or eye redesign is not. A brief natural blink returns to the same listening gaze.

For a gaze-only change with the body's facing direction unchanged, translate the original oval pair; preserve each oval's contour, height-to-width ratio and long-axis orientation. Do not tilt, skew, shorten or round the eyes to indicate looking up. Their opaque navy fill stays dark and consistent between endpoints: lighting and the painted treatment must not introduce lighter blue/gray interiors, gradients, sheen or pale rims. Compare enlarged first/last eye crops as well as the full scene. A separately scripted body turn may use coherent perspective; an upward glance alone does not call for one.

**Latest direction:** Elaine rejected the vertical eye-squish trial and asked
for Sol to tilt his body up a little instead. Use a small coherent upward pitch
of the entire compact flame body: outer silhouette, nested layers and attached
face move together, keeping the tiny feet supported. Preserve the normal tall
navy eye ovals; do not squash them or move the face as a separate head. Choose
the modest angle for the shot, with no body rise, stretch or exaggerated lean.
Elaine approved the displayed Fire Scene 02/05 first/last pairs and asked to
animate them. Bounce fluidly into every new pose, with overlapping tip/lobe
follow-through and a brief controlled rebound, then maintain quiet listening
idle. The still reviewer found the UP direction ambiguous because the pose
also rolls sideways; establish clear above-camera attention in motion and
verify it against the script. The rejected eye-squish previews remain history,
not a reusable expression rule.

Use low-amplitude connected flame-tip/lobe/body motion while listening. The hands can remain in the required pose after one main gesture; avoid repeated pointing, nodding or large bounces. Keep all colored layers connected and feet supported. During Sol's own lines he can look at the mechanism as scripted, then lift his gaze before Arthur's reply.

Record the gaze-ready cue, Narrator turn, idle state and next speaker change in the storyboard. Set final windows from actual normal-rate voice tracks at 1x. Until recordings exist, mark those windows provisional rather than claiming exact speech alignment. A Sol-off-screen cutaway has no invisible gaze requirement; its mechanism still follows the script.



Describe prop support and contact explicitly: what is held, where contact occurs, what stays rigid, when release happens and what supports the object afterward. For placement, keep the grip stable during lowering, establish support before release, then keep the released prop stationary as the hand withdraws along one clear path. Placement, release and withdrawal must be sequential. A planted foot stays supported until a planned step; a weight shift or step needs coherent ground contact and shadows. A hand gesture must fit Sol's short rounded limbs without fingers or extra reach. Keep props distinct from his anatomy, including any actual fire shown beside the flame-shaped mascot. Example accessories appear only when the shot calls for them.

## Plan the edit

For each clip, record its ID, teaching purpose, provisional edit duration, setting, framing, source asset or intended generation method, speaker-labeled dialogue, first frame, one main visible action and last frame. State what will be visible rather than using a vague instruction such as “show how it works.” Choose Sol's role per clip: asking, demonstrating or responding. A mechanism view can omit him when that improves the explanation.

Make framing specific: shot size; camera height relative to Sol or the mechanism; viewing angle and camera side; subject placement; approximate subject size within the vertical frame; foreground, background, and crop boundaries; and the exact starting and ending view for any camera move. Identify the feature that should attract attention first. Keep expression shots large enough for Sol's eye shapes to read, and reserve a stated caption area that does not cover his face or the mechanism.

Choose an intentional camera for each teaching purpose. Vary shot size and composition when it improves clarity; use a close-up or controlled push to reveal a detail, and quieter framing for listening or payoff. Record whether each camera move belongs in generation or editing, including its starting and ending crop, so it is not performed twice. Follow the [video prompt camera guidance](video-prompt.md#motion-and-continuity).

For every visible Sol, record the original eye design, gaze target and body states at both endpoints using the identity and performance sections above. Keep the face and relevant contacts readable; do not replace his eyes to create an expression. State explicitly when he is off-screen.

Plan different clip lengths around the dialogue and physical action. A single clip can carry two lines, several sentences, or a short exchange. Cut when the viewpoint or action needs to change; a sentence ending alone does not require a new clip.

For adjacent clips, note what carries across the cut: Sol's pose and location, the tracked object's position, direction of travel, camera side, and lighting. If the next view changes scale, shows a diagram, or skips time, state that explicitly. Keep screen direction consistent unless the transition clearly establishes a new view.

Use the existing calculus pilot as the continuity example. Its painted A → B → C → D progression is **crouch beside the board → land on it → lean into the curve as it wobbles → recover balance**. Reuse the end of one beat as the next starting point when the camera and framing carry through. For a cut to a new angle, match the action and position across the two views.

## Complete generated clips and continuity

Enforce the [two-frame source-pose cadence](video-style-guide.md#motion-style) at 30 fps during editing, preserving normal-speed action. Inspect source pairs before any smooth editorial camera move, then check final playback, crops, facial anchoring and prop contact. This is required editing and review work, not a claim that prompt wording implements it.

Use generated stills and complete Higgsfield clips for the visual production. A cutaway is a painted cartoon scene generated and animated like any other scene. Keep the explanation inside the clip. Do not create SVGs, custom diagrams, geometry tools or separately animated mechanism layers unless the user explicitly asks for them.

Use the approved character/style artwork and previous generated frames as visual references. Carry the same design, direction and identifiable object across cuts. Record continuity in plain scene directions, including where an object goes while off-screen; no mathematical route model is required. A distinctive painted edge or color can identify a recurring object inside the generated footage.

Check generated clips for correct contacts, connections, proportions and clear action. If a scene fails, simplify its framing or action, revise that scene's prompts and regenerate only that scene. Do not automatically replace it with a separate animation pipeline.

## Specify the first and last frames

The **first frame** is a still composition: name the camera angle and crop, Sol's exact pose, original eye design, gaze target and location when present, the important objects, their positions and the mechanism's starting state. Do not put a sequence of actions into the first-frame description.

The **action** describes how that starting state becomes the ending state. Specify one main physical action, a camera instruction if needed, and the spoken words that cue a reveal. Describe secondary performance only when it supports that action.

The **last frame** is another still composition: state what has moved, where it ended, Sol's unchanged eye design and ending gaze target when present, the resulting body pose or mechanism state, and what the viewer must still be able to see. “Sol reacts” or “finish explaining” is not a usable end frame. If the camera moves, specify its ending crop.

For exact continuity, reuse the approved last image as the next starting asset unchanged, with no duplicate generation. Keep the next scene's first-endpoint entry and existing output path, label it REUSE, and record the source scene/frame/path and destination path. Supply the same approved asset, or an identical-byte copy at the required slot, and check its identity when preparing the request. A reused start does not approve the new scene's end or bypass approval of that exact pair.

For a cut to another angle or crop, use the earlier endpoint as a continuity reference and describe what changes; it is not an exact source-image reuse. Match the relevant object state and say which spatial details and lighting stay consistent. The [image guide](image-prompt.md#end-frame-template) owns matching-endpoint prompt construction. Plan editorial reveals, overlays and cutaways separately from physical movement so generation does not invent a mechanism changing shape.

For a technical explanation, describe which parts stay rigid and which rotate or slide directly in the generated scene. Keep its camera and main action simple enough to read. Review the resulting clip before assembly and revise that scene if the motion is inaccurate.

## Edit duration and generation duration

Record the desired **edit duration** before choosing a provider. Check supported generation lengths when generation is requested. A planned 11-second scene may use two continuing generated segments; it does not imply that a provider accepts an 11-second request. Name each segment's first frame, last frame, and continuity requirements before submitting it.

Use the finished speech at 1× playback to set final clip lengths, following the [recorded-dialogue timing rules](video-script-guide.md#dialogue-density-and-timing). Keep estimates provisional until then. Trim unnecessary holds or repeated reactions, or extend a scene with a planned continuation when necessary. Do not stretch footage containing mechanical motion or speed up speech to hide a timing mismatch. Request the exact two-frame cadence in generation, then enforce and verify it during editing under the [motion style](video-style-guide.md#motion-style); it remains unconfirmed until actual footage passes.

## Prompt document standard

Save a separate plain-text prompt document alongside the complete episode script. For **N scenes**, include exactly **2N image endpoint entries** and **N video prompts**. Give each scene one labeled first-frame entry, one last-frame entry and one continuous first-to-last video prompt. Label an exactly reused endpoint instead of submitting another image generation; the entry count stays 2N while unique still generations can be fewer. Use the same scene IDs in both documents. If a scene needs separate generated segments, declare them as subscenes and update the count explicitly before generation.

Make every copyable image prompt self-contained: painted cartoon style, applicable character identity, precise framing, static pose, mechanism state and clean composition. For a new last image, use its approved first frame as the composition reference; specify what changes and what stays spatially consistent. Describe one still in each image prompt, not an action sequence or a contact sheet.

Make every video prompt self-contained: lead with the main visible action and result, then its start/end states, connected stages, gaze targets, camera, movement quality, concise style and identity, and essential constraints. Use a hold only when useful. Put actual first/end media roles, reference inputs, model settings, duration fields, paths, dialogue and Remotion edit notes outside copyable blocks. Verify the [reference roles and supplied assets](image-prompt.md#reference-roles-and-supplied-assets), use supported silent-video controls only, and keep exact captions and precise graphics in editable overlays. A prompt draft is not a submitted generation.

For example, a six-scene episode needs **12 image endpoint entries and 6 video prompts**; reused endpoints remain labeled entries. Last-frame composition and pose must be reachable from the first frame without a hidden cut, an unrequested new camera angle, or incompatible character placement. Choose one camera instruction that the generated clip can carry clearly. Reference lists distinguish existing character/style art from planned generated frames; do not require separate schematic assets. Test the opening action first before extending the run to later scenes.

## Generate Sol as part of the scene

1. **Choose references by role.** Supply original Sol artwork for identity and approved Ignite artwork for paint treatment, plus composition or continuity inputs when needed. Apply the identity rules above; prior generated anatomy does not override original assets. Preserve explicitly locked designs in older approved shots unless a revision is requested.
2. **Prepare the whole keyframe.** Generate or exactly reuse the planned still. Describe the location, camera and Sol's pose relative to the prop, with shared brushwork, perspective, light and contact shadows. Inspect it at phone size and show both endpoints for explicit user approval. A flat Sol PNG over a painted scene is a draft placeholder.
3. **Generate the motion after approval.** Use both approved endpoint images with the configured Higgsfield paired-frame model and production gate. Follow the [video prompt guide](video-prompt.md), including one main action and intentional camera behavior. For a turn or move, plan compatible endpoint poses; revise only the affected shot if it fails, preserving surrounding approved clips and rejected takes. Do not replace current settings with older Flow/UseAPI examples.
4. **Assemble in Remotion.** Import the complete generated MP4 as the primary footage; add separate voices, editable captions, sound and basic transitions. Enforce the exact two-frame source cadence first, then apply any declared smooth editorial crop and verify source frames and final playback. Keep existing shot IDs and episode paths so clips can be replaced. Historical episode integrations retain their own settings.

## Prompt examples for the calculus pilot

The hop and board response below belong to that pilot. They do not authorize unrequested preparation, extra hops or prop movement in other shots. Sol’s current bouncy follow-through is defined by the shared motion owner, not by that pilot’s board action.

**Painted still**

> Create a full vertical painted 2D scene using the approved Ignite scene reference for texture and lighting and the approved Sol artwork for character identity. Sol crouches beside the board at the left side of the curve, facing right. Keep his original flame silhouette, eyes, mouthless face, proportions, and tiny limbs. Paint Sol, the board, and the ground together with the same brushwork and light. Give Sol and the board shadows where they meet the ground. Leave clear space for captions.

**Animate the approved A → B frames**

> Match the approved painted start and landing frames. Sol crouches, makes one short hop onto the board, and lands with a small bend. The board dips slightly under his weight. Hold the camera steady and keep the original painted texture, light, and character design through the whole shot. End on the landing pose so the next shot can continue the motion. Animate on twos: each source pose/state held unchanged for two consecutive frames at final 30 fps, at normal speed; enforce and verify cadence during editing. Let the off-screen narration carry the explanation.

## Check each shot in the edit

- [ ] When visible, Sol is painted into the scene with lighting, scale and perspective that match the props.
- [ ] The action reads in silhouette and shows or reinforces the narrated idea.
- [ ] The first and last frames each specify a visible state; the action connects them without an unexplained change.
- [ ] The framing specifies shot size, camera height and angle, subject placement and scale, crop, focus, and the start and end of any camera move.
- [ ] Every visible Sol has a purposeful action, original eye design, named gaze targets and body poses, with cues that read at phone size.
- [ ] Dialogue is labeled Sol or Narrator, and each line matches what is visible at that point in the clip.
- [ ] Clip lengths vary with the scene; longer continuous scenes have a feasible segment plan if needed.
- [ ] Sol’s face, colors, and proportions match the approved reference at the beginning, middle, and end.
- [ ] The board or prop makes believable contact, and direction, pose, and object position make sense across the cut.
- [ ] The generated MP4 occupies the planned shot and the caption sits clear of the action.

Use the shared [final prompt review](checklist.md#final-prompt-review) before generation. The [revised fire episode](../episodes/fire_discovery/higgsfield-prompts.txt) illustrates distinct gestures, close-up contact, declared camera roles and endpoint reuse; its setting, actions, crop percentages and durations are episode-specific examples.

## References

- *Automate Ignite Videos* chat, Nov. 8, 2026. The painted calculus pilot, Sol’s A → B → C → D action, and mouthless performance with off-screen narration.
- *Code Flow Integration* chat, Nov. 9, 2026. Existing Flow A → B test, first hop-on clip, and the VS Code workflow.
- *Ignite video workflow guides* discussion, Nov. 10, 2026. Generate Sol in the painted scene so he can act within it.
- *Escalator script feedback*, Nov. 13, 2026. Write the scene alongside the dialogue; specify both endpoint frames and allow several lines within clips of varied lengths.
- *Escalator cartoon direction*, Nov. 13, 2026. Historical camera and acting discussion; current identity rules supersede its eye morphs and anatomy-changing squash/stretch suggestions.
- [Ignite_Moodle_Codex_Prompts.txt](https://chatgpt.com/library?file_id=libfile_41e7912a74808191b7964651794becc4&account_id=personal) for the approved mascot design constraints.
