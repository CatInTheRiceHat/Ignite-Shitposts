# Ignite video script guide

Current production order: prepare first and last stills (generate or reuse) -> show BOTH to the user ->
explicit approval of that exact pair -> Gemini Omni Flash 1.2 clip ->
independent actual-footage review. Shared settings: `../config/generation.json`.
Paired-frame clips support 3–10 seconds; declare continuing subscenes and update
the script/prompt counts before generation when a scene needs more time.

Use this to write short educational skits for Ignite. Develop the dialogue and scene descriptions together, using [shot-integration-and-sol.md](shot-integration-and-sol.md) for clip planning and [video-style-guide.md](video-style-guide.md) for performance and visual review.

## Write one answer viewers can see

1. **Hook.** Open on Sol noticing, doing, or questioning something visible. His question should come from what is happening in the scene.
2. **Setup.** Let the narrator respond to Sol and direct attention to the part that will explain the answer. Give enough context for someone seeing the mechanism for the first time.
3. **Reveal.** Explain the cause and effect while the viewer sees the relevant parts move. Sol can ask a follow-up when a reasonable viewer would have the same question.
4. **Payoff.** Let Sol use or recognize what he has learned. Resolve the opening question through the action and conversation. An ending does not need a joke.

Write for a curious middle or high school student. Make the exchange sound like people responding to each other. Use contractions, connected sentences, and varied sentence lengths. A speaker can explain an idea across two or more sentences while one scene continues.

Avoid a string of clipped clauses, slogan endings, forced jokes, and artificial punchlines. Humor should come from Sol's situation, behavior, or a natural response in the conversation.

Explain each necessary connection: which part moves, what moves it, where it goes, and why the visible result follows. Identify an unfamiliar part by its appearance or function before relying on its name. Replace vague mechanism descriptions with a concrete cause and effect. Check pronouns when several objects could be “it” or “they.” Keep wording precise when a shortcut would imply the wrong mechanism.

## Distinct visual beats

Give each shot one clear teaching purpose and one main visible action. Closely connected stages may form that action. State what the viewer learns or recognizes from the beat, and make each shot contribute something distinct rather than repeating a small lean, upward look and hold. Multiple spoken lines can share a clip when they support the same action.

Make every shot visually stimulating and attractive, with plenty of purposeful
action that sparks curiosity about what is happening. Write the eye-catching
situation, the developing action and its visible payoff into the storyboard,
following [visual interest and curiosity](shot-integration-and-sol.md#visual-interest-and-curiosity).

Choose shot size, composition and camera behavior to reveal the explanation. A close-up can clarify a contact, a controlled push can reveal a detail, and quieter staging can serve listening, anticipation or a readable payoff. State whether a camera move belongs in generation or editing. Sol can ask, demonstrate or react when that role helps the beat; he may be absent from a mechanism-focused cutaway. Follow the [shot guide](shot-integration-and-sol.md#plan-the-edit) for detailed staging and [purposeful performance](shot-integration-and-sol.md#purposeful-performance-and-prop-contact).

## Speakers and script format

- Deliver one complete episode document that combines the full dialogue and shot directions in reading order. Each clip must be understandable from that document alone. Keep dialogue, timestamps, reference assets and technical choices specific to the subject in the episode folder.
- Deliver a separate reviewable prompt text file with exactly **two image endpoint entries and one video prompt per scene**. Describe the first and last still states, labeling exact asset reuse instead of requiring a duplicate generation; the video prompt connects the endpoints. Match scene IDs, speaker lines, original eye design, scripted acknowledgment, camera and continuity. Keep dialogue for timing context outside visual-generation blocks, following the [prompt document standard](shot-integration-and-sol.md#prompt-document-standard).
- Write each scene so its full explanation and action can appear in one generated clip, including technical cutaways. Plan generated stills and clips followed by simple editing; do not require separate SVG illustrations, diagram construction or custom mechanism animation.
- Label every spoken turn **Sol:** or **Narrator:**. Keep the narrator off-screen. Sol remains mouthless and performs through purposeful gestures and small action-driven bouncy flame-like body motion, with facial markings anchored to his body.
- For new two-voice skits, use **Narrator / Arthur** and **Sol / the user's Higgsfield custom voice named Sol**. Read the exact custom voice ID and `voice_type: element` from [the shared voice cast](../config/voices.json); do not substitute Cub for Sol. Preserve explicit episode voice overrides and existing single-voice Cub episodes.
- Arthur is the built-in Higgsfield preset, delivered warmly like a nature documentary, with space for the visual reveal. Use his saved verified ID from the shared cast; keep Sol on a separate dialogue track. The custom Sol voice is an explicit project decision saved in the shared cast; Cub references belong to preserved legacy episodes. Record any intentional episode override, its exact provider/voice identity, and the supporting decision in that episode's shot plan. If evidence conflicts and no explicit decision resolves it, flag the mismatch and retain the documented shared default.
- The review script must include the setting, characters' positions, visible action and dialogue for every clip. Describe the mechanism during explanation scenes, camera height and angle, shot size, subject placement and scale, and the intended camera behavior. For Sol, record the original eye design, gaze target, body poses and cue for each performance change using the [identity and acting rules](shot-integration-and-sol.md#sol-identity). Use the [style guide](video-style-guide.md#motion-style) for painted movement; preserve the normal original oval eye design. A brief natural blink may support a beat and return promptly to those ovals; it is optional, not a repeated default gesture.
- Keep dialogue, scene direction, and captions in separate fields. Do not send speaker labels or production directions to text-to-speech as spoken words. Export separate clean text for each voice when audio is requested.
- Whenever the Narrator speaks with Sol visible, cue Sol's upward glance to the fixed above-camera voice BEFORE the first word, maintained through the whole turn with gentle body/flame listening idle. Record the gaze-ready cue, Narrator window and next speaker change. Sol's own lines can use a different gaze; transition up before Arthur's reply. A short silent lead-in can preserve an exact reused starting image. Follow the [Narrator attention owner](shot-integration-and-sol.md#narrator-attention-and-listening-idle).
- Review the actual generated footage side by side with this complete script and the per-scene speaker cues, not the visual prompt alone. Use recorded normal-rate voices for final alignment; planned timings remain explicitly provisional until then.

Use this review format for each clip:

```text
Clip ID — estimated edit duration
Teaching purpose: what this beat contributes to the explanation.
Setting and framing: location, shot size, camera height/angle, subject placement/scale, crop, and camera move.
Camera responsibility: generated movement or editing-only crop, with starting and ending views.
First frame: original eye design, gaze target, body pose, object positions, and mechanism state; name an exact reused asset when applicable.
Action: one main visible action, its connected stages in physical order and dialogue/visual cue; specify the gesture, bouncy follow-through and ending pose.
Speaker attention: Narrator turn, gaze-ready cue before the first word, above-camera gaze and gentle idle through the turn; label timing planned or grounded in actual recordings.
Motion: on twos at final 30 fps, each source pose/state held unchanged for two consecutive frames, normal-speed action; exact cadence enforced and verified during editing.
Sol: "Spoken line, when Sol speaks."
Narrator: "Spoken line, when the narrator speaks."
Last frame: original eye design, ending gaze target, body pose, object positions, mechanism state, and camera crop.
Next cut: what carries into the next view or what deliberately changes.
```

Include only the speakers who speak in that clip. A clip may contain multiple turns or several sentences from one speaker when the same action supports them.

## Dialogue density and timing

- Follow the [on-twos editing policy](video-style-guide.md#motion-style): 30 fps delivery, 15 pose updates per second, unchanged two-frame source states and longer holds in complete pairs. Align source-state trims to pairs, preserve normal-speed action and 1x voice playback, and verify actual footage. Smooth editorial camera moves can be applied afterward and need crop checks throughout.
- Remove unnecessary leading/trailing silence from the recorded voice files and shorten excessive silent gaps without changing speech speed. Then trim unused visual tails to the finished dialogue and action, preserving a brief readable payoff. Keep original recordings and clips; save trimmed derivatives and update real cue/caption times.

- Open with a readable visual beat in the first second. Let a clip's one main action support several spoken beats when they belong together, rather than inventing a new gesture for every line. Keep quieter listening or payoff poses when purposeful, and simplify competing reactions that obscure the explanation.
- Work voice-first: record or import the separate takes, mark real phrase boundaries and speaker changes, then lock scene lengths, editable caption cues, reveal holds and final reactions. Until takes are available, label timing and caption cues **provisional**. Preserve natural delivery and **1× playback**. Trim unnecessary holds, repeated reactions and optional accents while keeping reveals readable. If necessary, extend the edit or plan a continuation; never accelerate speech to fit a slot.
- New shorts start with a **30-second target**; the existing calculus pilot stays at its intentional 15 seconds. Allow a longer draft when the mechanism needs more explanation and state the estimated runtime. Do not remove necessary explanation just to hit a number.
- Write enough connected dialogue to explain the mechanism at a conversational pace. Do not assume viewers need a long silent pause after every short sentence. As a planning estimate, 30 seconds can accommodate roughly **80–95 spoken words** with a brisk delivery; speaker changes, reactions, and visual reveals use some of that time. Check the actual performance rather than treating this range as a quota.
- Vary clip lengths according to the action. A quick question may take 3–5 seconds, an exchange 6–8 seconds, and a mechanism explanation 9–12 seconds. These are examples, not fixed slots. Keep multiple lines in one clip when they belong to the same scene.
- Treat draft timings as estimates. Time the final edit to the downloaded voices at their normal generated rate and **1× playback**. Never accelerate speech to force it into a slot. Revise the script or extend a clip when the recording needs more time.
- Distinguish the duration used in the edit from a provider's generated clip duration. Plan longer scenes as continuing segments when necessary, as described in the shot guide.

| Beat | What to write | What to plan |
| --- | --- | --- |
| Hook | Sol's question prompted by what he sees | The visible situation and Sol's action |
| Setup | A narrator response and any useful follow-up | The part or movement the viewer should track |
| Reveal | A complete explanation in connected sentences | The detail that demonstrates each cause and effect |
| Payoff | Sol responding to what he now understands | An action or image that resolves his original question |

Preserve an existing episode's approved script and recordings unless a rewrite is requested. When dialogue changes, synchronize the main document, separate voice scripts, shot plan, prompt context and caption plan, then recalculate the spoken word count.

## Review before generating shots

- [ ] The opening and ending address the same question.
- [ ] Every spoken turn is labeled Sol or Narrator, and the conversation responds to the visible situation.
- [ ] Sentences sound natural read aloud, with no forced slogan ending or unnecessary fragments.
- [ ] The explanation identifies the parts and connects their movement to the result without vague shortcuts.
- [ ] Each clip describes its scene, first frame, action, and last frame clearly enough to plan generation.
- [ ] Each shot has a distinct teaching purpose, main visible action and intentional camera choice; any visible Sol has named gaze targets, expressive body poses and cues with his original eye design.
- [ ] Clip lengths vary with the action; several lines share a clip where appropriate.
- [ ] The explanation is correct and the reveal lands with the matching line.
- [ ] The spoken word count and estimated runtime are stated; final timing remains tied to the real recordings.

Run the shared [final prompt review](checklist.md#final-prompt-review) after translating the storyboard into prompts. It also checks reference roles, lighting, endpoint reuse and editable captions/precise graphics.

## References

- *Automate Ignite Videos* chat, Nov. 8, 2026. Off-screen Cub (Female) narration, the 15-second calculus pilot, and timing to the downloaded take.
- *Remotion setup* discussion, Nov. 10, 2026. Question first, visual reveal, and episode-specific captions and voiceover.
- *Escalator script feedback*, Nov. 13, 2026. Natural connected dialogue, fuller explanations, Sol/Narrator labels, skit staging, explicit first and last frames, and varied clip lengths.
