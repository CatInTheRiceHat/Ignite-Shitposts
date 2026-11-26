# Elaine's current rules: read this first

Updated 2026-11-25 (later), after the candle episode ("Why does a flame always point up?").

This page collects everything Elaine has asked for into one place, sorted by topic, so a new episode can
start from here. Where this page and an older guide disagree, **this page wins**; the
[superseded list](#superseded-do-not-follow) names the old rules that no longer apply.

Lines in quotes are Elaine's own words. Lines marked *(working practice)* are things learned while
making the candle episode, not preferences she stated. The dated history behind each rule is in the
[critique checklist](checklist.md).

## 1. Sol

- **Use the approved 3D Sol model for every clip.** "can we just make a sol 3d model or smth so we can
  always have the right reference". Approved 2026-11-25: "YES ... that is what i want, lets save that".
  See [sol-3d-model.md](sol-3d-model.md). Do not rebuild Sol by hand or from a description.
- **Sol is round and plump**, "a gumdrop shape", like the mascot images in
  `~/Documents/Ignite Website/public/mascots/`. Not wide, and no twisted flame tip: "rn this sol is kind
  of wide ... and theres a twisted flame tip but sol doesnt have that".
- **How the model is made:** "trace over the mascot outline and then u just inflate the thing", applied
  to `Logo.png`, "except the legs".
- **Legs and arms:** legs are Mascot.png's own leg shape, "tapered at the ends", with a blunt rounded
  tip: "not too pointy look at the reference". Arms are "the same shape", longer. Both stay short stubs.
- **Sol is mouthless, always.** "sol is a mouthless charcter it must only express emotions through
  motion so no random mouths popping up". Happiness is arms up, a bounce, a tilt, a nod. Never a smile.
- **Face:** plain cream with two navy (#1C2447) oval eyes close together and low on the face, and
  nothing else. Eyes that are "so far apart" are wrong.
- **Cartoony blinks are wanted.** "i like the cartoony blinks" (2026-11-25). Leave the painter's short
  closed-eye blinks in. Do not repair them out with `fix_blinks.py`. They are quick flat closed-eye lines
  and still read as blinks, not a mouth. Eyes must be back to the open navy ovals right after, and still
  nothing else on the face.
- **No particles** come off Sol, ever: "scrap the fire particles".
- **A logo version exists** (body only, no arms or legs), saved at her request beside the full model.

## 2. Script and voice

- **Sol is silent.** "we will cut the sol voice entirely so like sol will just be a silent character and
  it will just be the narrator just educating us". Narrator only (Arthur, `config/voices.json`).
- **Scripts are interactive.** The Narrator talks to Sol and reacts to what he does; Sol answers by
  acting. Her example: "what are you doing sol?", Sol wiggles the candle and looks up "as if hes trying
  to signal the narrator", "ohhh, you must be wondering why its standing up still", "and then sol nods".
- **Sol nods as an answer.** "we also need the nodding animation for sol too". The last clip of an
  episode ends on Sol nodding: "make the last clip sol nodding its head".
- **Each script also says how the clips are filmed** (set, camera, action, timing per clip), in one
  document she can read through: "storyboarding and scripting ... that includes how the clips will be
  filmed".
- About 30 to 40 seconds, vertical 9:16.

## 3. Look

- **Painted gouache, not Arcane.** "lets just keep this painted gouache painting ... arcane style is a
  bit too hard to perfect". Matte brushwork, layered colour, paper texture, no inked outlines.
- **One paint style across the whole episode.** "the paint styles are a bit off depending on the
  scenes". Give every paint pass the same style reference frame, including scenes set somewhere else.
- **Not bland.** She called an early flat render "so bland". Shots need lively staging, depth and
  lighting.
- **"make it stimulating ... and cute".** Add small delightful extras where they fit the scene. Her
  example: "floating sols in the background with space helmets ... during the space sequence".
- **Space helmets leave his legs out.** Floating Sols "need to have their legs hanging out so theyre
  not like trapped in bubbles", like `Ignite Website/public/courses/Introductory Physics and
  Astronomy.jpg`: a clear bubble over the body that stops at a collar ring, legs dangling below.

## 4. Motion and camera

- **Smooth motion. No on-twos.** "lets just remove the 2 frame choppy step". Smooth skeleton keys,
  smooth painted motion, no stepping conform.
- **Dynamic camera.** "can these camera angles be dynamic". Plan one purposeful move per shot (push,
  arc, crane, slide) and animate it in the Blender skeleton so the paint pass follows it.
- **Emotion comes from movement**, since he has no mouth: tilts, bounces, arm raises, nods.

## 5. Props and physics

Props must behave like real objects. Each rule below came from a clip she sent back.

- **Props do not morph or change sides.** "the handle like morphs to the other side which isnt
  realistic".
- **Props do not drift toward a character.** "the spiral kind of shifts towards sols hand which is
  unrealistic". A prop moves only because someone visibly moves it.
- **Show Sol moving the prop, in its own shot.** "in the candle scene we dont see the spiral in the
  background and in the 2nd scene we see sol pull it to it ... or push the paper spiral". Do not tease a
  prop in the background of a close-up it is not part of.
- **Nothing stays off-balance by itself.** "dont make the lamp stand up automatically sol should tilt
  it with his hand and when he raises his hand up it should topple down". A tilted prop stays tilted
  only while his hand is on it, and falls back when he lets go.

## 6. Sound and edit

- **Cute sound effects.** "can we add like cute sound effects like squeaks". Small squeaks, boings and
  twinkles on Sol's actions. The candle set is in `episodes/candle_flame_up/audio/sfx/`.
- **Music:** use the songs she puts in `assets/music/`.
- **No black at the end.** "when the clip ends cut the black"; she confirmed "yes no black at last clip".
  The video stops the moment the last clip stops, with no fade or cut to black. Picture and sound end on
  the same frame; trim the audio to the video length.
- **Captions:** Rammetto One, 105 px at 1080p, white with a 12 px orange (#F07B2A) outline.

## 7. How she wants the work done

- **Pipeline:** gray Blender skeleton clip, then a Higgsfield paint pass (Gemini Omni Flash 1.2, mode
  `edit`) with the skeleton as the video reference. No intermediate stills unless she asks.
- **Keep credit use down.** "to cut down on credits". Repaint only the clips that need it, and ask before
  a big spend.
- **720p is the final quality.** "i lwk couldnt tell it was low quality lets just keep it like this"
  (2026-11-25). Paint at 720p and deliver that, upscaled to 1080 by 1920 in the edit. No separate 1080p
  pass, so no 1080p paint cost.
- **When she sends a clip back, regenerate that clip** with the fix in the skeleton and the prompt:
  "regenerate the clip but without the mouth in the prompt and the 3d preview".
- **Keep everything.** Version new files; never overwrite earlier takes, cuts or the approved Sol.
- **Never record an approval she did not give.** Only the 3D Sol model is approved. About candle cut v6
  she said "the rest is good" after asking for one last change; no clip or cut is formally approved.
- **Write her feedback down** in the [checklist](checklist.md) as it comes, in her words, separate from
  technical findings, and fold lasting rules into this page.

## 8. Making an episode, step by step *(working practice)*

The candle episode folder (`episodes/candle_flame_up/`) is the worked example; copy its scripts.

1. **Script** in the interactive format, with the filming plan per clip. Get her read on it.
2. **Narrator takes** first. Trim dead air; clip lengths come from the real takes.
3. **Skeleton** per clip with `skeleton/rig.py` and `skeleton/clips.py`: gray room and props, the real
   coloured 3D Sol, camera move keyed in. Render 720 by 1280 at 30 fps.
4. **Check the gray frames before paying for paint.** Is his hand actually on the prop? Is anything
   leaning or floating with nothing holding it? Is every prop the painter might invent (a handle, a
   strap) modelled in one fixed place?
5. **Paint** each clip at 720p with the same two image references every time: the episode's style frame
   and Sol's turnaround sheet.
6. **Check every painted frame**, not a sample: run `check_faces.py`, then look at the frames around
   each action.
7. **Repair small slips** in post (`remove_mouth.py`; `fix_flame_ball.py` for the space flame); repaint
   anything bigger. Leave the cartoony blinks alone.
8. **Assemble** with `build_edit.py`: takes, captions, music, sound effects. Time sound effects to the
   painted clip, which can drift from the skeleton by half a second or more.
9. **Check the ending** for black frames and for sound running past the picture.
10. **Deliver** (section 9).
11. **Log** her notes and the new file names in the episode's `script.txt` and the checklist.

### Paint prompt rules *(working practice)*

- Never write the word "mouth", not even "no mouth", and no mood words such as "happily". Say what his
  face is: "plain smooth cream with exactly two navy oval eyes on it and nothing else".
- Say "paint only what each source frame shows", or the painter adds characters and objects.
- Say "VERTICAL 9:16 ... frame for frame", or a clip can come back landscape.
- State physics as a rule and number the beats: "the candle leans ONLY while Sol's arm is holding the
  handle".
- Name each prop's place: "exactly ONE ring handle, on its left edge, in every frame".
- Say "short stubby arms, two short blunt bare red legs", or limbs grow long.
- The painter slips in short blinks. She likes them, so they stay. Still check that the eyes come back open
  and that no mouth appears.

## 9. Delivering a finished video

When a video is done, always do both of these without being asked (Elaine, 2026-11-25):

1. **Think of a good title.** It is the YouTube headline: a plain question or hook a viewer would click,
   in title case, like "Why Does A Flame Always Point Up?". Tell her the title.
2. **Put the finished video in `workflow/completed/`, named exactly as the title** with `.mp4` after it,
   for example `completed/Why Does A Flame Always Point Up?.mp4`. That folder already holds her earlier
   finished videos. The file is the final cut, with voice, captions, music and sound effects, ending on the
   last frame with no black.

Do not overwrite or delete anything already in `completed/`. If a file with a similar name is there, leave
it and tell her. Keep the working versions in the episode's `renders/` folder.

Candle episode: she chose the title **Why Does A Flame Always Point Up?** (2026-11-25). The finished cut is
not in `completed/` under that name yet; see the note at the end of this page.

## Still to do on the candle episode

Elaine said these changes apply "in the future", and told me not to build the video again for now. So:

- The newest cut, `renders/candle-v7-draft.mp4`, still has the painter's blinks painted out of clips 3, 4
  and 5. The versions with the blinks left in exist (`clips/03-paint-v4.mp4`,
  `clips/04-paint-v6-ball.mp4`, `clips/05-paint-v8-raw.mp4`) and are not in a cut yet.
- `completed/Why Does a Flame Always Point Up.mp4` is a copy of that v7 cut that she put there. Her chosen
  title, with a capital A and a question mark, is not saved yet. Ask before replacing her file.

## Superseded: do not follow

These still appear in older guides and in `CLAUDE.md` / `AGENTS.md`. They no longer apply.

| Old rule | Replaced by |
| --- | --- |
| Animate on twos (each pose held 2 frames at 30 fps) | Smooth motion (section 4) |
| Sol has a voice (two-voice skits) | Sol is silent (section 2) |
| Make first and last stills and get the pair approved before each clip | Blender skeleton, then paint; no stills (section 7) |
| Fixed camera by default | Dynamic camera (section 4) |
| Keep Sol flat; avoid inflated anatomy | Round, plump Sol from the 3D model (section 1) |
| Arcane / ink linework trial | Painted gouache (section 3) |
| Mascot.png as the image reference for paint passes | Style frame plus Sol's turnaround sheet (section 8) |
| Repair every painter blink | Keep the cartoony blinks (section 1) |
| Draft at 720p, then a 1080p final pass | 720p is final (section 7) |
| "Sol looks up for the whole Narrator turn" as a blanket rule | He looks up when addressed or answering and at the prop while demonstrating (a reading of her clip 1 example, not her words) |
