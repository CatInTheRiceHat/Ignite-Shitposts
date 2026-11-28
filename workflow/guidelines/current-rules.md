# Elaine's current rules: read this first

Updated 2026-11-27 (late), with Elaine's notes on the first Neon-written script (more science, a definite conclusion, section 2); earlier that day with her notes on the shower-curtain script and on its first cut (camera and emotions, section 4); before that 2026-11-26, after the coffee-ring episode; first written after the candle episode ("Why does a flame always point up?").

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

- **Gemini 4 Neon writes the script and plans the animation.** Elaine, 2026-11-27: "Whenever I give you a video
  topic, use Gemini 4 Neon to write the script and plan the animation." Her steps: pass Neon the topic and the
  **full text** of the current script guidelines, with "any examples, templates, or character references the
  guidelines rely on so Neon has the same context you do"; ask it "to follow our existing format and return
  everything you need to animate the video, including the final narration, scene order, timing, on-screen
  actions, and any visual cues"; send it with `agy --model gemini-4-neon-high -p`; "check Neon's output against
  the guidelines. If something is missing or off-brand, send that specific feedback back to Neon for revision";
  then "save it in the project and animate from it using our existing workflow". *(working practice)* What was
  sent the first time (the wet-shirt episode): this page, `video-script-guide.md`, `shot-integration-and-sol.md`,
  `sol-3d-model.md`, `assets/sol-3d/eyes/README.md`, the emotion sound list, the shower-curtain script as the
  format and the coffee-ring script as the one she liked; the request builder is saved in that episode's
  `neon/` folder. Neon's answers and each round of feedback are kept there too. `agy` needs a Google sign-in.
- **Be more scientific.** Elaine, 2026-11-27, on the first wet-shirt script: "also be more scientific". That script
  said light "bounces" and "goes deeper" and "wet fabric traps more light" without ever naming what happens.
  *(my reading)* Name the real process and use its real words, each explained in passing the first time: light
  scatters, reflects, refracts (bends), is absorbed; say what property differs and why that changes the result (for
  the shirt: how much light bends and bounces at a boundary depends on how different the two materials are, and
  water is far closer to cotton than air is). Give one concrete figure or comparison where it helps. Still plain
  sentences for a curious middle or high school student, and still correct: a real term replaces a vague phrase, it
  is not piled on top. The "Accuracy" note at the end of the script says what was simplified.
- **End on a definite conclusion.** Elaine, the same message: "lets have a definative conclusion". The last line
  states the answer to the title question outright, as a fact a viewer could repeat: what is really happening and
  what is not ("the cloth is not a darker colour; less light is coming back to your eyes"). *(my reading)* Not a
  recap of the steps, not a soft "just", not a question, not a slogan. It goes with the ending order in section 4:
  Sol listens through it, nods when it is over, then the pleased face.
- **Make it funny.** Elaine, 2026-11-27, while the wet-shirt rewrite was being written: "can u tell neon to add
  some humor to this". *(my reading)* The Narrator gets a dry, teasing sense of humour about what Sol does (one or
  two short quips that react to him, never a pun for its own sake), and Sol's physical comedy carries the rest: the
  goober gags of section 4. A joke never replaces a step of the explanation and never costs it accuracy, and the
  last line stays the definite conclusion. This replaces the older guide's "avoid forced jokes" as the default:
  jokes are wanted, as long as they come from the situation.
- **The Narrator is a loud, funny friend, and the text is written for the voice to perform.** Elaine, 2026-11-27, on
  Neon's draft V5 (whose quips were dry: "It WAS a nice shirt."): "the voice to text can do smth rly funny so like you
  can use all caps ike WOAH sol nice shirt. the girls are gonna like this one or smth like that and then like
  NOOOOOOOO dude! that wasn't so nice. lets fix this shirt up and stuff". So: the Narrator talks to Sol like a hyped
  friend ("dude", teasing, big reactions), and the script writes the delivery into the words: a word in ALL CAPS is
  shouted or punched, a stretched word (NOOOOOOOO) is drawn out, "!" is excitement. *(my reading)* Use them where the
  moment is big (the compliment, the disaster, the reveal), one or two per line at most; the science sentences keep
  the same friendly voice but stay clear and correct, and the last line is still the definite conclusion.
  *(working practice)* Send the line to the voice exactly as written, caps and all. Captions show the same words.
  `check_narration.py` hears "NOOOOOOOO" as "no", so read its transcript for those takes instead of trusting FAIL,
  and plan about a second for a stretched word.
- **A friendly opening before the trouble.** Her opening for the wet-shirt episode: "woah sol nice shirt and then
  he gets sprayed with water by a car and then we do like the explanation thing". *(my reading)* The Narrator can
  open by greeting Sol or remarking on what he has or is doing, a calm beat, and then the thing that needs
  explaining happens TO Sol, big and funny. The splash itself is that episode's idea, not a rule.
- *(working practice)* **Time lines at Arthur's real pace when planning:** about 2.3 words a second plus about 0.3 s
  at each comma or full stop inside a line. Neon's first draft allowed 4.4 s for a 16-word line that takes about 7.
  And **no more than two close-ups in a row without Sol**, with different framings; three in a row (17 s) left the
  Narrator talking to nobody.
- **Sol is silent.** "we will cut the sol voice entirely so like sol will just be a silent character and
  it will just be the narrator just educating us". Narrator only (Arthur, `config/voices.json`).
- **Scripts are interactive.** The Narrator talks to Sol and reacts to what he does; Sol answers by
  acting. Her example: "what are you doing sol?", Sol wiggles the candle and looks up "as if hes trying
  to signal the narrator", "ohhh, you must be wondering why its standing up still", "and then sol nods".
- **A line is said when the thing it is about is on screen.** Elaine, 2026-11-27, on the shower-curtain opening: "when
  sol has the furious eyes thats when narrator says sol why are u mad its these kinds of logic that you need to know
  when making the videos so they're more accurate". The Narrator was asking why Sol was glaring almost a second
  before the glare was on his face. The Narrator can only react to what he, and the viewer, can already see: a face,
  an action, an arrow, a prop. So for every line, ask what on screen it refers to, and start the line after that is
  showing, not before. *(working practice)* Time lines from the PAINTED clip, not the gray one: the paint pass can
  hold a face longer than planned. If the clip is then too short for the line, restage it longer; do not start the
  line early to make it fit. Check every line this way before building, including the science lines (an arrow or a
  motion should be visible when the words name it).
- **Sol nods as an answer.** "we also need the nodding animation for sol too". The last clip of an
  episode ends on Sol nodding: "make the last clip sol nodding its head".
- **Each script also says how the clips are filmed** (set, camera, action, timing per clip), in one
  document she can read through: "storyboarding and scripting ... that includes how the clips will be
  filmed".
- About 30 to 40 seconds, vertical 9:16. *(my reading)* Up to about 50 seconds and about 105 words when the fuller science
  she asked for on 2026-11-27 needs it (the first try at squeezing it into 45 gave run-on lines with the commas taken
  out); say the runtime in the script's header.
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
- **Way more dynamic, and open with a fly-in.** "i wish the camera angles were way more dynamic for example when u
  introduce the scene fly the camera in from the top of the bathroom and into the shot where its aimed at sol in
  the bathrub" (2026-11-27, on shower-curtain script v1, where each shot had one slow push, slide or crane). The
  first clip introduces the place with a travelling camera: start high over the whole set and fly down into the
  shot on Sol. The later clips travel too: a whip to the prop, riding along with the thing being explained, a
  crane over a wall, an orbit round Sol. *(my reading)* Do the travelling at the start or end of a clip and
  settle while the science has to be read, so the steady close-up rule above still holds for those seconds.
- **No cut between two shots with the same framing.** On the stress ad: "the cut from first clip to 2nd clip is a bit
  unusual ... starting the camera from a close up of sol's face and zooming out instead ... removes the uneessesary
  choppyness" (2026-11-26). Clip 2 had opened on clip 1's own wide framing. *(working practice)* When two clips share a
  set, change the shot size at the cut: open the second one close and pull back, or the other way round.
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
- **Cartoony Sol, using the whole emotion set.** "sol should also be more cartoony and utilize the many spirtes of
  emotions we have. this will make the video more appealling to audiences and make sol very cute and marketable"
  (2026-11-27; shower-curtain script v1 used three faces in 38 seconds). Plan a face from the 38 in
  `assets/sol-3d/eyes/` for nearly every beat (singing, startled, angry, determined, dizzy, idea, smug and so
  on), each with its bounce, and give him cartoon business to go with them (singing in the shower, going dizzy
  from following something round). *(my reading)* This is her go-ahead to use the 32 newer faces and marks in
  episodes; no frozen approved copy of that set exists yet. *(working practice)* Floating marks sit on a flat
  plane in front of him, so time them for when the camera is roughly in front of him.
- **A goober who fights back.** "when the shower curtain comes to sol can u lwk make him try to catfight it away
  lol we wanna make sol this super cute animated goober" (2026-11-27). When something bothers Sol he reacts with
  silly physical comedy: eyes squeezed shut, leaning away, both little arm nubs slapping at it as fast as they
  go. *(my reading)* "Super cute animated goober" is the target for his acting in every episode, not only this
  one. *(working practice)* A catfight is not a reach: his nubs keep their
  short length and flap in place, so stage the thing against his side or let him slap the air (see the rule
  on reaching arms below).
- **Never repeat a gag; use a different cartoon trope each time.** "lets try to not repeeat the catfight multiple
  times instaed we should utilize different cartoony troupes so like catfight is one but another one is like if
  the floor is slippery they just slip and fall dramatically like they run in place for a while and then they slip
  back and flop" (2026-11-27, when script v2.1 used the catfight in two clips). Each gag appears once in a video.
  Her two so far: the catfight, and the slip (legs run in place, going nowhere, then he slips backward and flops).
  *(my reading)* Others from the same family are fair game: a freeze before a fall, a double take, spinning dizzy,
  a puffed-up strut, being flattened and popping back. Pick ones the place suggests (a wet floor, a swinging
  door). *(working practice)* A fall ends with him lying on the surface, touching it and his shadow; that is the
  one time his feet may leave the ground.
- **Every change of emotion gets a bounce.** "everytime u swap emotions make sure theres a bounce that acts as a
  trnasition between one emotion to the other" (2026-11-26). Never swap his expression on a still body. He dips
  into a squash, the face changes at the bottom of the dip, he springs up past his normal height and settles,
  and the new eyes pop slightly big and settle with him. `assets/sol-3d/eyes/eyes_rig.py` does this
  (`emotion_at`); use it for every swap.
- **Bouncy, dynamic animation.** "i also love bouncy animation and like dynamic animations" (2026-11-26).
  Squash and stretch on every hop and landing, a wind-up before a move, overshoot and a springy settle after
  it. Props he moves get the same treatment as long as they stay physically believable.
- **Emotion comes from movement**, since he has no mouth: tilts, bounces, arm raises, nods.
- **He stands on the ground.** "sol is floating which goes against nature" (2026-11-26). His feet touch the surface
  and his shadow in every frame; after a hop he comes back down. *(working practice)* The painter can leave him in
  the air after a hop: prefer a squash-and-spring with his feet planted, and measure his feet after any hop
  (`episodes/due_in_5_minutes/fix_float.py --measure`; the same script lands him).
- **He faces what he is reacting to.** "sol is also looking the wrong way" (2026-11-26). *(working practice)* A Sol
  standing at the side of the frame and facing straight ahead reads as looking out of frame: turn him toward the
  camera or the prop.
- **Distress is for the moment of distress only.** "during the tip sequences sol still has the purple gradient
  distressed emotion even though he should be calm during thes parts" (2026-11-26). The indigo shade and worry lines
  come off as soon as the scene moves on; do not let them linger or fade across later shots.

- **A fall must not look like he dies.** Elaine on the shower-curtain cut, 2026-11-27: "just remove the sol
  slipping cuz it just looks like he dies lol". The slip ended with X eyes and Sol lying still on his back.
  *(my reading)* A pratfall may happen, but no X eyes and no lying motionless; he bounces straight back up.
- **Make the hit obvious and the reaction big.** "lets make it more obvioust that the shower curtain hits sol
  lol maybe u can have it comededitely slap sol in the face thats why he gets mad like very dramatically"
  (2026-11-27). When something happens to Sol that sets up his mood, show it as a clear, exaggerated beat,
  then a dramatic reaction. A gentle touch on his side did not read.
- **No sudden gag tacked on the end of a shot.** "the dizzy animation is very sudden so just remove that"
  (2026-11-27; the snap zoom to spiral eyes at the end of the whirlwind shot).
- **Animated arrows for things you cannot see.** "can we annimate arrows to further demonstrate the flow and
  how air moves?" (2026-11-27). Air, pressure, heat and forces get moving arrows on screen. *(working
  practice)* They are rendered from the gray scene's own camera with everything else held out, then laid over
  the painted clip, so they cost no credits and track the camera.
  Her note on the first try: "the arrows look svery choppy ... theres random stuff poking out of them". Those were
  flat 3D arrows rendered in the scene: edge-on parts stuck out and walls cut pieces off. Now only each arrow's path
  is taken from the scene (`skeleton/arrows2.py`, `export_arrows.py`) and the arrow is drawn in 2D along it
  (`overlays/draw_arrows.py`): one smooth shape that bends with the flow, soft edges, fading in and out.
- **Nothing pops into a shot.** "can we get rid of the water puddle appearing lol redo the clip" (2026-11-27; a puddle
  faded in under Sol near the end of the whirlwind shot). Whatever is on the floor or in the room at the first frame
  of a shot is what is there at the last. *(working practice)* The puddle came from a style frame that had one and a
  prompt that named it; for a shot without it, use a style frame without it and state a rule ("the floor under him
  is dry in every frame").
- **No jump inside a shot.** "theres a weird cut from 32 to 33" (2026-11-27). The paint pass had drawn the first second
  of the last clip from a different camera angle and then snapped to the right one. *(working practice)* On the frame
  sheets, compare where the walls and the curtain sit at the start of each painted clip with a second later; the
  jump detector missed this one. Cut the clip to start after the jump, or repaint.
- **End on the payoff, not on a string of faces.** "can we remove the thinking emotion and just cut to the happy star
  shit" (2026-11-27). The last clip went thinking dots, light bulb, bump, smug star, happy; she kept only the star
  and the happy nods. *(my reading)* One or two faces for the ending, straight to the pleased one.
  She then found that version "kind of chopped": "instead of having sol like react immediately can we have him look
  up and nod before mkaing happy face" (2026-11-27). So the ending has an order: Sol looks up at the Narrator and
  listens through the last line, nods when it is over, and only then makes the happy face. A reaction that is
  already on his face when the shot starts reads as a cut, not as an ending.
- **No "Got it?" endings.** "in the future lets get rid of like the 'got its.'" (2026-11-27). From the next
  script on, the Narrator does not end by checking in with Sol ("Got it?", "See?", "Make sense?"). End on the
  last piece of the answer and Sol's reaction to it.

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

- **The Narrator is Arthur on Eleven v4** (Elaine, 2026-11-27: "i changed the voice so in higgsfield u can now see we use
  eleven labs but i kept arthur"). Model `elevenlabs_v4`, stability 0.5, similarity 0.75, same Arthur voice id
  (`config/voices.json`). He reads slower than on seed_audio, so record the takes before timing the skeleton.
- **A pause after every narrator line, and whole takes.** Elaine, 2026-11-27: "after every time arthur says smth there
  needs to be a pause ... be really aware of like the pauses make sure that the video flows nicely", and "the 'second'
  from arthur is cut off. make sure that you put full audio for each thing". About a second of quiet between lines; no
  take that starts or ends mid-sound. How: "Several Sols, square films and a bare set" in section 8.
- **Cute sound effects.** "can we add like cute sound effects like squeaks". Small squeaks, boings and
  twinkles on Sol's actions. The candle set is in `episodes/candle_flame_up/audio/sfx/`.
- **Emotion sounds for Sol's faces.** Elaine, 2026-11-27: "i also put smth in assets called emotion sounds there
  are so many sound effects that can correspond with the emotions sol is using try using these in the video".
  `assets/emotion sounds/` holds 28 short emote sounds, one per mood (amazed, bewilderment, curiosity, fearful,
  glee, inspiration, joy, pleased, pride, shocked, smirking, surprise, thought, worry and more). Play the one
  that matches each face Sol makes, at the moment the face changes. *(working practice)* Their loudness differs
  a lot, so make level-matched copies in the episode's `audio/sfx/` (peak -3 dB, leading silence trimmed) and
  play them at about 0.3. There is no angry sound in the set; squeaks and boings still cover actions (a stomp,
  a slap, a nod).
- **Not a sound on every face.** Elaine on the shower-curtain cut with the emotion sounds, 2026-11-27: "theres a bit
  too much going on i feel like near the end like maybe when theres like chains of emotion phasess we can do like oh
  sound effect for one no sound effect for thte other and then sound effect for the other one". When Sol goes through
  several faces in a row, give a sound to one, leave the next silent, give a sound to the one after. *(working
  practice)* Pick the beats that matter most (the hit, the idea, the big reaction) and leave the in-between ones bare;
  do not stack a squeak or boing on a face that already has its emotion sound.
- **No sound across a cut, and room before it.** Elaine, 2026-11-27: "make sure that when a sound efffect is still
  playing that we dont cut to the next clip" and "the cuts between the clips are sometimes abrupt so leave some room for
  sound to end before u switch". Every sound effect and every narrator line finishes inside its own clip, with a
  beat of quiet before the picture changes. *(working practice)* `episode_edit.py` now fails the build if a take or a
  sound effect ends less than `min_tail` (0.25 s) before its clip does. Make room by starting the line earlier,
  using more of the clip, or picking a shorter sound; never by letting it run over.
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
   *(working practice, 2026-11-27)* Also run it on the finished cut (`--video`): a take can open with a
   garbled sound that the per-take check skips (shower-curtain take 05), and the cut check hears it.
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

- **More emotions (Elaine, 2026-11-26, later).** "can you make an angry and sad emotion for sol 3d ... and all other
  emotions that one could need". Her directions: angry is "the OO circle eyes but like they're cut so like its two
  semicircles that rotate down into the middle", with "the red gradient instead of purple"; the anger mark is
  "thin"; sad, crying, gloomy and heartbroken use "the same [eyes] as bashful"; smug is the half eye turned 180; every mark has a dark outline and is drawn large; the stars are inflated solids, not flat; awe uses yellow four-point stars around him, "just the stars", no lines. All built into the eyes model:
  38 expressions with marks that move, sheet `assets/sol-3d/eyes/sol-eyes-expressions-v9.png`, list in that
  folder's README. **She has not approved the new set yet**; the approved six are unchanged. On 2026-11-27 she
  asked for the set to be used in episodes ("utilize the many spirtes of emotions we have", section 4).

### Planned expressions *(working practice)*

- Write each expression into the script with its clip and time, so the review knows what is meant to be there.
- Use the separate-eyes model for this (`assets/sol-3d/eyes/`, her idea: "rigg the eyes like seperately like
  attach a 3d polygon on top"). `pose_eyes()` sets the expression, the blink and where he is looking, per
  frame. Do not leave an expression to the painter to invent. She approved this model on 2026-11-26 ("OH ITS
  PERFECT."); the frozen copy is `assets/sol-3d/eyes/approved-2026-11-26/`.
- Name it in that clip's prompt ("from 2.0 to 2.6 seconds his eyes are two happy upward arcs, then they return
  to navy ovals") and keep the plain-face wording for every other moment.
- `check_faces.py` will flag these moments. A flag at a planned time is expected; a flag anywhere else is not.

### Words on screen, reaching arms, and ads *(working practice, from the "Due in 5 Minutes" ad, 2026-11-26)*

- **Lettering on signs and 3D objects goes in the Blender skeleton itself** (Elaine, 2026-11-27, after the "Whole Group
  Project" ad: "in the future when u put text on signs and 3d objects can we just put that in the skeleton directly so
  like with blender do that"). From the next film on, the words are on the sign in the skeleton clip the painter is
  given (the lettering planes already exist: `render_clip.py` shows them with `SHOWOVL=1`), and the prompt tells the
  painter to keep that lettering exactly as it is. This replaces laying the words on in the edit as the first choice.
  *(working practice, mine)* The painter has garbled and re-spelled words before, which is why the bullet below was
  written. So: check every lettered frame of the paint; if the words come back wrong, say so to Elaine and fall back to
  the overlay method below for that shot only. Captions and the end card are not on 3D objects and stay in the edit.
  Proof from this ad: words laid over a card in a sliding shot hung off its edge for half a second (Elaine on cut v9:
  "the letters are still fucked up"), while "1st" painted from the skeleton stayed clean. Composite such a clip with
  `composite.py --painted-text` so nothing is laid over the painted words.
- **(Fallback) Never let the painter write words.** Draw each piece of lettering once as a PNG, put it on a plane in the
  Blender scene, render that plane alone in the shot's perspective, and lay it over the painted clip. The skeleton
  and the prompt keep every board, card and page blank. Lock the camera off in any shot with lettering, and keep
  lettering behind Sol with his silhouette from the skeleton. Worked example:
  `episodes/due_in_5_minutes/overlays/` (`make_art.py`, `composite.py`) and `skeleton/render_clip.py` (`MODE=ovl`,
  `MODE=mask`).
- **Do not have Sol reach for anything with an arm.** Three paints in a row gave him a long arm or a detached arm
  nub when he reached for a prop, even with the prop within reach and "never stretch" in the prompt. Stage the
  action with his body instead: a hop beside the thing, a bump with his side, a lean. Say in the prompt that both
  arm nubs stay tucked at his sides.
- **Check for eyebrows.** The painter adds brow strokes to worried and upward-looking faces. He has none.
  `episodes/due_in_5_minutes/fix_brows.py` paints them out, and with `--redraw` lays clean navy ovals back where a
  brow has fused with the eye.
- **Render the skeleton at 24 fps** (`SKEL_FPS=24` with the ad's `rig.py`). The painter returns 24 fps; a 30 fps
  skeleton dropped to 24 makes a camera move hitch six times a second.
- **Check handwriting fonts letter by letter.** Gochi Hand's "lt" read as a capital H ("saH", "meH"); Patrick
  Hand does not. An independent frame-by-frame reviewer caught that, two one-frame caption faults and a label drawn
  over Sol, so run one on the cut before delivering.
- **Leave a tint out if it should be barely there.** A faint indigo tip in the skeleton came back as the full
  worried look. State a tint that must hold as a rule of its own ("from the first frame to the last").
- **A long shot needs a camera move.** Elaine on the 9-second locked-off payoff: "kind of scuffed ... for this long
  duration can we just replace this clip with like a 3d like motion that looks through his poster and then pivot to
  him" (2026-11-26). For a moving camera, render the lettering for every frame (`MODE=ovlseq`); it tracked the painted
  cards exactly. Keep Sol clear of all lettering so nothing has to be cut out around him.
- **Do not redraw his eyes frame by frame.** She saw them "jitter and move position". Prefer a repaint; if a repair is
  unavoidable, smooth the eye positions over time and watch it at speed.
- **Check where the painter put Sol against the caption band.** It can draw him smaller and lower than the skeleton;
  `composite.py`'s `reframe` pushes in on him.
- **Ads:** captions go in a band centred at 70% of the height, at most 840 px wide (`caption_y`, `caption_max_width`
  in `edit.json`), to stay clear of the bottom fifth and the right edge where the platform's buttons sit. An ad has
  no tracker row, no description and no upload unless she asks. The songs in `assets/music/` are game soundtracks:
  for a paid ad, build a cut without music as well (`"music": null`) and tell her.

### Landscape ads and end cards *(from the "All Due This Week" ad, 2026-11-26)*

- **Her landscape layout** (her script): "SOL ON THE LEFT THIRD. THE STRESS ON THE RIGHT TWO THIRDS", captions in the
  "lower third, centered", "Nothing important in the bottom 10% of the frame". *(working practice)* Put his feet about
  70% of the way down the frame so the captions have the surface under him; captions Rammetto One 72 px with a 9 px
  outline, centred at y = 895 of 1080 (`width`, `height`, `caption_size`, `caption_stroke` in `edit.json`).
- **Her end card** (her reusable prompt, `episodes/all_due_this_week/end-card-prompt-elaine.txt`): a rounded card in the
  site orange; the course's ORIGINAL card art on top, uncropped; the course name "exactly as written on the course
  card"; big "Join Ignite today!"; small "Link in description" (YouTube) or the sign-up address without "https://"
  (website, presentations); never "?gclid=..."; "Same fonts as the Ignite course cards. No em dashes, no extra slogans,
  no emojis"; 16:9 on the right two thirds, 9:16 on the top two thirds; a transparent PNG at full frame size; it slides
  in over about half a second and holds. `overlays/make_end_card.py` builds it. *(working practice)* Stop the card above
  the caption band while the narrator is still talking under it.
- *(working practice)* **Check the course before the ad says "teaches all of this".** Course outlines are in Drive
  (search the course name); the Resilience outline is Emma Zhou's doc.
- *(working practice)* **Lettering as a per-frame holdout pass** (`render_clip.py MODE=ovlseq` in that episode): every
  lettering plane is rendered for every frame with everything in front of it cut out, so words follow a moving camera or
  prop and hide behind whatever passes. It tracked the painted props to within a frame; where the painter moves a prop a
  frame or two early, remap those frames (`seq_map` in `composite.py`).
- *(working practice)* **A thing that goes into a box must stay in sight**, or the painter forgets it and paints the box
  empty. Keep boxes low. Do not squash a box to make it bounce: the painter drew flaps opening. Turn a lettered prop's
  blank back to the camera before it flies.
- *(working practice)* **The style frame sets how a clip STARTS.** A clip that must open on purple Sol, or on a changed
  prop, needs a reference frame that shows that (the last frame of the clip before). A clip that must hold sparkle eyes
  to its end painted right once a sparkle-eyes frame of the same shot was the reference.
- *(working practice)* **Never give a frame of an earlier take of the same shot as the style reference when the layout
  changed**: the painter brought the old props back and doubled them. To carry a room's paint across, give a SWATCH: two
  strips of wall and floor cut from the good take, with "paint only, no objects".
- *(working practice)* **A missing colour shade can be laid on in the edit** (`composite.py` "tint": Sol-coloured pixels
  inside his skeleton silhouette, fading from his tip). Cheaper than a repaint and it matched the painted purple.

### Several Sols, square films and a bare set *(working practice, from the "Whole Group Project" ad, 2026-11-27)*

- **Square films are painted wide and cropped.** The painter returns only 16:9 or 9:16. Render and paint 16:9 at 720p,
  frame every shot for the middle square, and cut the square out in the compositor
  (`episodes/group_project/overlays/composite.py`). Her "can we make them 1:1" was read as the square format; she has
  not confirmed that reading.
- **A flat blockout comes back flat.** The first beach (bare sand, three bands of sky) was returned unpainted. Dress the
  set in the skeleton (bunting, palms, dunes, ripples, clouds, a sun glint) and open the prompt with a paragraph that
  says the source is an untextured blockout and names how each surface is painted. Give a painted frame of an earlier
  film as the reference for how Sol himself is painted.
- **Ring eyes are for our Sol alone, in a simple shot.** On a teammate, in a shot with three or four Sols, "round rings
  with white centres" came back with pupils five times, whatever the wording. Teammates show surprise with plain eyes,
  a hop and an exclamation mark (`act(..., marks=("exclaim",))`).
- **No travelling shot past several Sols with things landing beside them.** Two paints of it added a Sol, doubled one
  and drew an open laughing face. Give each beat its own simple shot: two Sols, both in frame from the first frame to
  the last.
- **Keep a gap between two Sols.** When our Sol landed touching Ring Sol the painter merged them and he was gone for two
  seconds.
- **A happy face tempts the painter to add a smile.** Check every pleased, smug or cheering beat for one.
  `episodes/group_project/fix_mouth.py` fills it from the cream around it.
- **Floating marks must not cut lettering.** In the lettering pass his marks are no longer holdouts (a star cut the T
  out of "Towers"). Hold lettering back until the painted thing it sits on has landed (`seq_from` in `composite.py`).
- **A thing that drops in never lands on the skeleton's frame.** The painter's sign, board or ribbon arrives a few frames
  early or late, so words that ride it hang in the air. Render each lettered thing as its own pass
  (`render_clip.py MODE=ovlseq OVLONLY=<plane> SEQNAME=<name>`) and start it once the painted thing is down (`layers` in
  `composite.py`); for something that moves with a crane, find the painted thing by its colour and put the words on it
  (`find_rosette`). During a fast fly-in letter only what is big and square to the camera.
- **Keep an accessory off his face.** The swim ring sat across Ring Sol's eyes and one paint left him eyeless; it now
  sits low. Straight overhead a Sol does not read as a Sol: use a high three-quarter angle.
- **A low camera loses the sea.** Two shots came back with a plain orange sky. Keep the camera about 0.85 high or more
  so the sea band shows and the look matches the shots around it.
- **Long prompts go by reference.** Put them in one JSON file, upload it as a file, fetch it in the Higgsfield sandbox
  and pass `{"ref": "sandbox:~/gp/prompts.json#/p1"}` as the prompt. Change a prompt with a small patch script run in
  both places and compare the hashes.
- **A pause after every line** (Elaine on cut v5: "after every time arthur says smth there needs to be a pause ... make
  sure that the video flows nicely"). Leave about a second of quiet between two narrator lines, more when Sol is doing
  something in between; a question is followed by Sol's answer in action before the narrator speaks again. The edit
  script of an episode prints every pause and stops below its minimum (`MIN_PAUSE` in `group_project/make_edit.py`). If a
  line does not fit with its pause, make the clip longer; never squeeze the lines together.
- **A take must be whole** (Elaine: "the 'second' from arthur is cut off"). Run `group_project/audio/check_takes.py` on
  the raw and the trimmed takes: a take that is not quiet in its first and last 20 ms begins or ends mid-sound and is
  re-recorded. Trim loosely (0.07 s before the first sound, 0.14 s after the last) and never cut a tail off to make room.
- **Words ride on the painted sign** (Elaine: "the text must move when the signs are moving"). A sign the painter moves
  is followed in the painted frames themselves (`"track"` layers in `group_project/overlays/composite.py`): the sign is
  found in the last frame, where it stands still, and followed backwards, so its words fall, land and shake with it.
  This replaces holding the words back until it has landed.
- **Lettering is centred and on one baseline.** In a row of words centre the CAPITAL height, not each word's own ink
  (`centre()` in `overlays/make_art.py`), or "Moat" and "Flag" sit at different heights. Words on a ribbon or badge go
  on its plain middle, not the middle of its whole outline.
- **Nothing comes and goes inside a shot** (Elaine: "sand appears in somehow"). A half-hidden prop behind a row of Sols
  (a heap of sand, a castle, a bucket) is what the painter redraws or drops. If a prop is not needed in a shot, leave it
  out of the skeleton and say in the prompt that the sand is open; no Sol walks off to do something at a prop the shot
  does not show. A Sol who leaves, leaves by hopping out of the frame.
- **An accessory sits clear of the face from every camera height** (Elaine: "HE CANT EVEN SEE ... CAN WE LIKE MAKE IT
  LOWER"; "this si what floaty sol should look like"). The swim ring is at his feet (`mate()` in `skeleton/clips.py`);
  check it at eye level and while he nods, not only from above. Use a painted frame she has approved as the style frame.
- **Every Sol in a group shot is whole and in view** (Elaine: "poor guy in floaty"). No Sol half behind another or cut by
  the edge of the square or the end card; pull the camera back until they stand side by side with sand between them.
- **The camera goes round things, never through them** (Elaine: "it just fazes through the flag"). A fly-in passes under
  a banner or over a wall, and the prompt says so.
- **No expression she did not ask for at the end of a beat** (Elaine, of smug half-shut eyes: "why is he doing this can
  we just keep it like this"). Pleased is plain eyes and a tall stance unless the script names a face.
- **Two paints of one skeleton can be joined inside a whip pan.** When one paint has the right teammates and another the
  right close-up, take each part from the paint that got it right and cut in the middle of the whip
  (`group_project/splice_clip2.py`). Line the two up by eye first: paints do not whip on the same frame.
- **A caption may wait for the picture.** If the first words of a line would lie across a face or a lettered thing while
  the camera moves, keep the voice where it is and start that caption a few tenths later (`CAPTION_FROM` in
  `group_project/make_edit.py`). If the painter frames a Sol on the edge of the square, slide the square (`crop_pan` in
  `overlays/composite.py`); the 16:9 paint has room on both sides.
- **Effects are rigged in Blender, not left to the painter** (Elaine on cut v7: "can we try to rig this in 3d instead?
  like make the hash marks vibrate and the arms move rly fast"). Motion lines, like every other mark, are objects in the
  skeleton that the painter copies (`hash_marks()` / `hash_at()` in `group_project/skeleton/clips.py`); a fast action is
  animated fast in the skeleton (six flaps a second), not asked for in words. When the painter makes up an effect it also
  makes up the face that goes with it (an open mouth).
- **The ending of a group film: the teammate has the flowers, our Sol smirks** (Elaine: "wheres the flowers and the
  sparkles", then, of flowers and sparkles round both: "i meant just the floaty has the flowers and i think the sol in
  front does the smirk animation"). The cheering teammate is `joy` (flowers); our Sol in front is `smug` (half-moon eyes,
  one star), standing tall. Ask which Sol gets which mark before painting an ending with more than one Sol.
- **When the narrator offers help, Sol looks confident, not cross** (Elaine, of a glare at "here are five things that'll
  fix this": "this doesnt make sense ... hold his hands on his sides like hes confident"). Nubs on his sides, tall,
  plain eyes.
- **Hands on his sides are a plain < > angle** (Elaine, 2026-11-27: "can we not have the las segment of the hands be like
  pointed out so just an angle like this <>"). Each arm is one bend, elbow out, tip resting back on his body; the tip
  never flares outward. *(working practice)* The rig's nubs are straight, so the painter invented the bend and the flared
  tip. For this pose give the skeleton a two-piece arm (out to the elbow, back in to the body) so the painter copies the
  angle, and say in the prompt that each arm is one simple bend whose tip touches his side.
- **Never hold a frame to make a shot longer** (Elaine on cut v8: "somehow its just frozen"). If a line outgrows its shot,
  lengthen a shot that ends on a standing pose by playing its last frames back and forth (`group_project/extend_tail.py`),
  or re-shoot it longer. Scan the finished cut with `ffmpeg -vf freezedetect=n=0.0005:d=0.2`; nothing should be frozen
  for more than about a quarter of a second except a locked-off shot of a sign.
- **One re-roll can fix a paint, two can give two new faults.** A paint that comes back flat, or redraws the set, is
  re-submitted as it is; but check every re-roll against the accessories (a hat appeared on our Sol in two re-rolls of
  one shot). A mouth on a turned face: `group_project/fix_mouth_below_eyes.py` (it finds the eyes and fills the patch
  between and under them).

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
2. **Put the finished video in `completed/` at the top of the repository** (`Ignite Shitposts/completed/`, beside
   `workflow/`, not inside it: Elaine moved the folder there on 2026-11-26, "im gonna move the completed clips folder out
   and put it outside workspace"), **named exactly as the title** with `.mp4` after it,
   for example `completed/Why Does A Flame Always Point Up?.mp4`. That folder already holds her earlier
   finished videos. The file is the final cut, with voice, captions, music and sound effects, ending on the
   last frame with no black.

Do not overwrite or delete anything already in `completed/`. If a file with a similar name is there, leave
it and tell her. Keep the working versions in the episode's `renders/` folder.

Candle episode: she chose the title **Why Does A Flame Always Point Up?** (2026-11-25). The finished cut is
not in `completed/` under that name yet; see the note at the end of this page.

## 10. Topics, the tracker sheet and working unattended

Elaine, 2026-11-26.

- **Topics come from her sheet**, "Ignite Shitposts Tracker", tab **"General"** (it was called "Cofounder
  Reimbursement" until 2026-11-26): columns Topic, Music, Description, Status. Take the first row whose Status is
  "Not Done".
- **Ads go on the "Advertisements" tab**, same four columns (Elaine, 2026-11-26: "do the advertisement tabs and then
  like name the advertisement something and then put a description with the link to the webiste ... and the link to
  the form"). For each ad fill the next row: **Topic** = a name for the ad; **Music** = the song used;
  **Description** = the blurb, then `Website: https://ignitefindyourfire.org/` and
  `Sign up: https://forms.ignitefindyourfire.org/t/oqB8WMKbJ6us` each on its own line, then the five hashtags on the
  last line; **Status** as for episodes. *(working practice)* Her form link came with `?gclid=xxxxx` on the end, a
  placeholder for Google's click id; the sheet has the link without it. An ad is not a topic: never take the next
  episode from this tab. Worked example: row 2, "Due in 5 Minutes".
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
- **Show her the caption before posting.** "wait before u post ... can i take a look at caption" (Elaine, 2026-11-26,
  the ad's Instagram Reel). Write the caption, show it to her, and post only after she says so. The sheet's
  Description cell is the caption.
- **Use her Music cell if it is filled in**; otherwise pick a song from `assets/music/` and write it back.
- **Do not reuse a song.** "can we change the music as well thats why the spreadsheet exists" (2026-11-26, when the
  stress ad came with the coffee episode's song). *(my reading of it)* Before picking, read the Music column of both
  tabs and choose a song that is not in either.
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
