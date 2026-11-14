# Ignite video script guide

Current production order: first and last stills -> show BOTH to the user ->
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

## Speakers and script format

- Deliver one complete episode document that combines the full dialogue and shot directions in reading order. Each clip must be understandable from that document alone. Keep dialogue, timestamps, reference assets and technical choices specific to the subject in the episode folder.
- Deliver a separate reviewable prompt text file with exactly **two image prompts and one video prompt per scene**. The image prompts describe the first and last still states; the video prompt describes the continuous action between those states. Match the script's scene IDs, speaker lines, eye shapes, Narrator eyeline, camera and continuity. Keep dialogue for timing context outside visual-generation prompt blocks.
- Write each scene so its full explanation and action can appear in one generated clip, including technical cutaways. Plan generated stills and clips followed by simple editing; do not require separate SVG illustrations, diagram construction or custom mechanism animation.
- Label every spoken turn **Sol:** or **Narrator:**. Keep the narrator off-screen. Sol remains mouthless and performs his lines through his eyes, pose, and body movement.
- For new two-voice skits, use **Narrator / Arthur** and **Sol / the user's Higgsfield custom voice named Sol**. Read the exact custom voice ID and `voice_type: element` from [the shared voice cast](../config/voices.json); do not substitute Cub for Sol. Preserve explicit episode voice overrides and existing single-voice Cub episodes.
- Arthur is the built-in Higgsfield preset, delivered warmly like a nature documentary, with space for the visual reveal. Use a verified preset ID when available; record an unresolved ID explicitly rather than inventing one. Keep Sol on a separate dialogue track. The custom Sol voice is an explicit project decision saved in the shared cast; Cub references belong to preserved legacy episodes. Record any intentional episode override, its exact provider/voice identity, and the supporting decision in that episode's shot plan. If evidence conflicts and no explicit decision resolves it, flag the mismatch and retain the documented shared default.
- The review script must include the setting, characters' positions, visible action, and dialogue for every clip. Describe what we actually see, including the mechanism during explanation scenes. State shot size, camera height and angle, subject placement and scale, and the intended camera move. For Sol, name the eye shapes, gaze target, body poses, and the words or action that cue each expression change. Match the lantern reference's restrained acting, original oval eyes, painted storybook flame and wispy tip.
- Keep dialogue, scene direction, and captions in separate fields. Do not send speaker labels or production directions to text-to-speech as spoken words. Export separate clean text for each voice when audio is requested.
- When Arthur addresses visible Sol, cue one clear glance toward the voice just above the camera, then let Sol follow the demonstrated object. Cue a new upward look for a new reply or confirmation when needed; avoid automatic repeated glances within a single answer.

Use this review format for each clip:

```text
Clip ID — estimated edit duration
Setting and framing: location, shot size, camera height/angle, subject placement/scale, crop, and camera move.
First frame: starting eye shape, gaze target, body pose, object positions, and mechanism state.
Action: physical movement and cartoon expression changes with their dialogue or visual cues.
Sol: "Spoken line, when Sol speaks."
Narrator: "Spoken line, when the narrator speaks."
Last frame: ending eye shape, gaze target, body pose, object positions, mechanism state, and camera crop.
Next cut: what carries into the next view or what deliberately changes.
```

Include only the speakers who speak in that clip. A clip may contain multiple turns or several sentences from one speaker when the same action supports them.

## Dialogue density and timing

- Start with visible action in the first second. Pair each spoken beat with one primary visible action. Several beats can share a continuous shot, but simplify the performance if competing reactions obscure the explanation.
- Work voice-first: record or import the separate takes, mark real phrase boundaries and speaker changes, then lock scene lengths, editable caption cues, reveal holds and final reactions. Until takes are available, label timing and caption cues **provisional**. Preserve natural delivery and **1× playback**, leaving room for the reveal and final reaction. Optional accents are removed before compressing necessary holds or accelerating speech.
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
- [ ] Framing is specific, and Sol's cartoon expressions have named eye shapes, gaze targets, body poses, and cues.
- [ ] Clip lengths vary with the action; several lines share a clip where appropriate.
- [ ] The explanation is correct and the reveal lands with the matching line.
- [ ] The spoken word count and estimated runtime are stated; final timing remains tied to the real recordings.

## References

- *Automate Ignite Videos* chat, Nov. 8, 2026. Off-screen Cub (Female) narration, the 15-second calculus pilot, and timing to the downloaded take.
- *Remotion setup* discussion, Nov. 10, 2026. Question first, visual reveal, and episode-specific captions and voiceover.
- *Escalator script feedback*, Nov. 13, 2026. Natural connected dialogue, fuller explanations, Sol/Narrator labels, skit staging, explicit first and last frames, and varied clip lengths.
