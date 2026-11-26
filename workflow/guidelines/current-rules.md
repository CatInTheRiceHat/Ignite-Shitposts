# Elaine's current rules: read this first

Updated 2026-11-26, after the coffee-ring episode; first written after the candle episode ("Why does a flame always point up?").

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
  nothing else. Eyes that are "so far apart" are wrong. This is his resting face. Planned anime expressions
  (section 4) may change the eyes or add a small mark for a beat; anything unplanned is still a glitch.
- **Cartoony blinks are wanted.** "i like the cartoony blinks" (2026-11-25). Leave the painter's short
  closed-eye blinks in. Do not repair them out with `fix_blinks.py`. They are quick flat closed-eye lines
  and still read as blinks, not a mouth. Eyes must be back to the open navy ovals right after, and still
  nothing else on the face.
- **A blink closes fully or it is a glitch.** She sent back "a weird flash" (2026-11-26): three frames where
  his eyes were half shut and striped. A clean blink (open, flat closed line, open) stays. Eyes that are
  striped, split or half drawn for a few frames get repaired in the edit: lay the eye area of the last good
  frame over them. No repaint needed.
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
- **The narration must say exactly what the captions say.** "make sure the audio s [legible] becase the first
  one i saw it said authur smth smth and that clearly doesnt match with the captions" (2026-11-26). The voice
  model sometimes adds or changes words. Transcribe every take and the finished cut with
  `scripts/check_narration.py` and compare with the script. Regenerate a take that differs; do not cut around it.

## 3. Look

- **Painted gouache, not Arcane.** "lets just keep this painted gouache painting ... arcane style is a
  bit too hard to perfect". Matte brushwork, layered colour, paper texture, no inked outlines.
- **One paint style across the whole episode.** "the paint styles are a bit off depending on the
  scenes". Give every paint pass the same style reference frame, including scenes set somewhere else.
- **A different backdrop for every video.** "we should try to change the scene up every video cuz then it will
  get boring so see for each video u can set up a different backdrop" (2026-11-26). Pick a place that suits the
  topic and build that set in the skeleton; do not reuse the last episode's room. Inside one episode the room
  and the paint style still stay the same from clip to clip.
- **Be adventurous with the place, and make it the lively version.** "please experiment with more backgrounds.
  for example since we tlaking about coffee we can set this at a cafe instead of a kitchen which would liven
  up the video" (2026-11-26). Ask where the topic would naturally happen and pick the place with the most life
  in it: a café over a kitchen, a skate park over a pavement, a concert stage over a bedroom.
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
- **A different angle for each shot.** "I rly love dynamic angles so see if u can make the video more lively and
  cool with like different angle shots" (2026-11-26). Vary the viewpoint from clip to clip, not only the move:
  low and looking up, high and looking down, over Sol's shoulder, a tight close-up, a wide establishing shot,
  a tilted angle for a surprise. The coffee episode stayed near eye level for most shots; do not repeat that.
  The close-up science shots still keep a slow, steady camera so the demonstration is easy to read.
- **Anime-style expression for Sol.** "I also like to take inspo of like anime and what kind of expressions
  their characters do so lets see if we can apply that onto sol the next time" (2026-11-26). Borrow anime's
  acting: big clear poses, a sharp anticipation before a move, a jolt of surprise, a slump, a proud puff-up, a
  curious tilt, a held beat, a snap zoom on a reaction. He still has no mouth.
- **Expressive eyes and small anime marks are welcome.** Asked whether his eyes may change shape and whether
  marks may be added, she said "yeah that would be cute", then gave her own list (2026-11-26): "some examples of
  eye shapes include like this >< and then like the OO eyes when sol is surprised and then the inners are white
  and then like u can do sparkles and then like the ||| lines for worried". So:

  | Feeling | What it looks like |
  | --- | --- |
  | Squeezed shut: effort, a flinch, glee | `> <` eyes with rounded tips ("like rounded tips") |
  | Surprised | `O O` eyes: round navy rings with white inside |
  | Delighted, amazed | sparkles |
  | Worried, dread | a dark blue-purple shade that "starts from the top of sol to bottom": deep indigo at his flame tip, fading as it goes down ("i think i like B but lets make the purple like bluer and darker"), with thin lines hanging "on the side" of his face above one eye |
  | Shocked | the worried shade and lines with the `O O` eyes, as in her anime references |

  These are her examples, not the whole list; others in the same spirit are fine. Each is used for a beat, then
  his normal navy ovals return. Still no mouth. Marks are drawn on or near him for a moment; they are not fire
  particles coming off his body, which stay banned.
- **Every change of emotion gets a bounce.** "everytime u swap emotions make sure theres a bounce that acts as a
  trnasition between one emotion to the other" (2026-11-26). Never swap his expression on a still body. He dips
  into a squash, the face changes at the bottom of the dip, he springs up past his normal height and settles,
  and the new eyes pop slightly big and settle with him. `assets/sol-3d/eyes/eyes_rig.py` does this
  (`emotion_at`); use it for every swap.
- **Bouncy, dynamic animation.** "i also love bouncy animation and like dynamic animations" (2026-11-26).
  Squash and stretch on every hop and landing, a wind-up before a move, overshoot and a springy settle after
  it. Props he moves get the same treatment as long as they stay physically believable.
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
- **Nothing morphs and everything makes sense.** "a problem i seee all the time is clips that morph or dont
  make sense for example sol is supposed to use the dropper but the cap magically disappears and he just like
  gets the bottle" (2026-11-26). A prop keeps every part it started with, in the same place, for the whole
  video. If the story says Sol uses a thing, he visibly uses that thing the way it works.
- **Show the science close up, and keep it looking the same.** "the demonstration of the coffee is inconsistent.
  lets maybe do like close up scientific shots of whats happening" (2026-11-26). The thing being explained
  fills the frame in its own close-up shots, and it is the same object, size, colour and shape in every clip.
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
- **Never record an approval she did not give.** Two things are approved: the 3D Sol model (2026-11-25) and the
  separate-eyes version of it with its expressions and emotion bounce (2026-11-26). No clip or cut is. About candle cut v6
  she said "the rest is good" after asking for one last change; no clip or cut is formally approved.
- **Write her feedback down** in the [checklist](checklist.md) as it comes, in her words, separate from
  technical findings, and fold lasting rules into this page.

## 8. Making an episode, step by step *(working practice)*

The candle episode folder (`episodes/candle_flame_up/`) is the worked example; copy its scripts.

1. **Script** in the interactive format, with the filming plan per clip. Get her read on it.
2. **Narrator takes** first. **Transcribe each take and compare it with its line** (`check_narration.py`);
   regenerate any take that differs. Trim dead air; clip lengths and caption times come from the real takes.
3. **Skeleton** per clip with `skeleton/rig.py` and `skeleton/clips.py`: gray room and props, the real
   coloured 3D Sol, camera move keyed in. Render 720 by 1280 at 30 fps.
4. **Check the gray frames before paying for paint.** Is his hand actually on the prop? Is anything
   leaning or floating with nothing holding it? Is every prop the painter might invent (a handle, a
   strap) modelled in one fixed place?
5. **Paint** each clip at 720p with the same two image references every time: the episode's style frame
   and Sol's turnaround sheet.
6. **Check every painted frame**, not a sample: run `check_faces.py`, then look at the frames around
   each action. Look at every span it flags frame by frame at full size; a contact sheet is too small to
   judge an eye.
7. **Repair small slips** in post (`remove_mouth.py`; `fix_flame_ball.py` for the space flame); repaint
   anything bigger. Leave the cartoony blinks alone.
8. **Assemble** with `build_edit.py`: takes, captions, music, sound effects. Time sound effects to the
   painted clip, which can drift from the skeleton by half a second or more.
9. **Check the ending** for black frames and for sound running past the picture.
10. **Post-check the final cut, every frame.** "as a post check [procedure] be sure to analyze all the frames of
    the final clip" (2026-11-26). Run `scripts/frame_review.py` on the cut: it lays out every frame, in order
    and with its time, on contact sheets. Look at all of them, and transcribe the cut's audio. Look for a prop
    that changes, loses a part, moves by itself or appears from nowhere; Sol off-model (a mouth, wide eyes,
    long limbs, particles); the demonstration looking different from clip to clip; an action that does not
    read; captions that do not match the voice. Anything found is fixed or repainted before delivery, and the
    post-check is run again on the new cut.
11. **Deliver** (section 9).
12. **Log** her notes and the new file names in the episode's `script.txt` and the checklist.

### Avoiding morphs and mismatched demonstrations *(working practice)*

- Give Sol simple one-piece props and simple actions (tap, nudge, point, lean in, hop, nod). A prop with a part
  that comes off or opens (a dropper and its cap, a lid, a pen and its cap) is where the painter loses track.
- Model the thing being explained in its real colours in the skeleton, the way Sol is, and reuse that same
  object in every clip. A gray stand-in gets a new look in every paint pass.
- Keep the camera still or slow in the close-up science shots, so a change that should not happen is easy to see.
- Pause-based caption timing is a guess. Take word times from the transcript instead.
- In each paint prompt describe only what that clip shows. A prop that is named but out of frame gets painted in.
- When one clip's version of the demonstration comes back a different colour, repaint it with a frame of the
  neighbouring clip as the image reference.
- Keep the subject of a close-up in the upper half of the frame; the captions sit at 82% of its height.
- The coffee episode is the worked example for all of this: `episodes/coffee_ring/skeleton/clips_v2.py`,
  `prompts/build_v2.py`, `edit.json`.

### Planned expressions *(working practice)*

- Write each expression into the script with its clip and time, so the review knows what is meant to be there.
- Use the separate-eyes model for this (`assets/sol-3d/eyes/`, her idea: "rigg the eyes like seperately like
  attach a 3d polygon on top"). `pose_eyes()` sets the expression, the blink and where he is looking, per
  frame. Do not leave an expression to the painter to invent. She approved this model on 2026-11-26 ("OH ITS
  PERFECT."); the frozen copy is `assets/sol-3d/eyes/approved-2026-11-26/`.
- Name it in that clip's prompt ("from 2.0 to 2.6 seconds his eyes are two happy upward arcs, then they return
  to navy ovals") and keep the plain-face wording for every other moment.
- `check_faces.py` will flag these moments. A flag at a planned time is expected; a flag anywhere else is not.

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

## 10. Topics, the tracker sheet and working unattended

Elaine, 2026-11-26.

- **Topics come from her sheet**, "Ignite Shitposts Tracker", tab "Cofounder Reimbursement": columns Topic,
  Music, Description, Status. Take the first row whose Status is "Not Done". Never touch the other tab
  ("Ignite Spendings").
- **Scripts need no review.** "i dont think i need any supervision for scripts now". Write the script in the
  interactive format and go on; `episodes/coffee_ring/script.txt` is the one she read and liked.
- **Fix and continue.** "fix all changes and trust urself". When the gray frames show a problem, fix it and
  carry on without asking. Still stop for anything that is not about the episode itself.
- **When the video is in `completed/`, fill in its row:** Music (the song used), Description, and Status
  **"In Progress"** ("mark it in progress cuz i need to upload it").
- **Mark it "Done" yourself after uploading** (Elaine, 2026-11-26: "once ur done with uploading it looks
  great please mark done by urself ok"). Only when the video is public on YouTube and Instagram and both
  posts read back right. If an upload fails or looks wrong, leave "In Progress" and tell her.
- **Description format** (her candle row is the model): a short blurb that opens with the question, names Sol
  and the Narrator and gives the answer in plain sentences, then a line break inside the cell, then the
  hashtags on their own line.
- **Different hashtags for each video** (Elaine, 2026-11-26: "put different hashtags on the video
  description"). Do not reuse the candle row's `#science #physics #education #animation #cool`. Pick five
  that fit that video's topic, e.g. coffee: `#coffee #coffeering #fluiddynamics #sciencefacts #didyouknow`.
  *(working practice)* Five, because the same description is used as the Instagram caption.
- *(working practice)* **Uploading.** YouTube ("Ignite Education") and Instagram (`ignitefindyourfire`) are
  connected through Composio. Check what is already posted first (`YOUTUBE_LIST_CHANNEL_VIDEOS` with
  `mine`, `INSTAGRAM_GET_IG_USER_MEDIA`) so nothing is posted twice. YouTube:
  `YOUTUBE_MULTIPART_UPLOAD_VIDEO` with `--file`, run from inside `completed/`, title = the file's title,
  description = the sheet's Description cell. **YouTube is always "not made for kids"** (Elaine,
  2026-11-26: "for the youtube always rembmer to put not for kids"): the upload tool has no field for it,
  so after every upload read the video back (`YOUTUBE_GET_VIDEO_DETAILS_BATCH`, part `status`) and confirm
  `selfDeclaredMadeForKids` is false; if it is not, set it with `composio proxy` (videos.update, part
  `status`) before making the video public. Instagram: `INSTAGRAM_POST_IG_USER_MEDIA` (`video_file`,
  `media_type` REELS, caption = the same description) then `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`. Build the
  payload in Python so the caption is not wrapped in quotes. Instagram captions cannot be changed through
  the connector after posting. Posting publicly needs her go-ahead. Then set Status "Done" (rule above).
- **Use her Music cell if it is filled in**; otherwise pick a song from `assets/music/` and write it back.
- **Credits:** keep to a cap per night and skip the night if the balance is too low. A full episode's paint
  pass is about 83 credits at 720p (about 37 s at 2.25 credits a second), plus about 2 for the narrator.
  The coffee episode cost about 102 for its first version and about 114 for the redo.
- *(working practice)* Sheet edits go through Composio (`GOOGLESHEETS_VALUES_UPDATE`); the Drive connector
  can only read. Skeleton clips render headless with `episodes/<name>/skeleton/render_clip.py`. Cuts are
  built with `scripts/episode_edit.py <episode>` from the episode's `edit.json`. Paint one clip first and
  pass one of its frames as the style reference for the rest, so the room matches.

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
