"""Second request to Gemini 4 Neon for the wet-shirt episode (2026-11-27), after Elaine read script V3.
Usage: python3 build_prompt_v2.py <workflow dir> <out.txt>
Same pasted context as build_prompt.py (the guidelines now hold her three new notes), plus her message and V3."""
import sys, pathlib
wf = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
def f(p, first=None):
    t = (wf / p).read_text()
    if first: t = "\n".join(t.split("\n")[:first])
    return t
brief = """You are writing the script and the animation plan for one episode of Ignite's short science videos
(vertical 9:16). Do not use any tools and do not ask questions: answer in ONE message with the finished document.
Everything you need is pasted below.

TOPIC (from Elaine's tracker sheet): "Why does a wet patch look darker on a gray shirt?"

THIS IS A REWRITE. You wrote script V3 for this topic earlier today (pasted at the very end). Elaine, who directs
these videos, read it and answered, in her own words:

  "hmm can we start out with woah sol nice shirt and then he gets sprayed with water by a car and then we do like
   the explanation thing also be more scientific and lets have a definative conclusion mk"

So V4 must do exactly these three things:

A. NEW OPENING. The film opens with the Narrator saying "Woah, Sol, nice shirt!" to Sol, who is WEARING a little
   plain light-gray T-shirt and is proud of it. Then a car drives past through a puddle and sprays him with water,
   which leaves the dark wet patch on the shirt he is wearing. Then the explanation. This replaces the garden,
   the drying rack and the sprinkler. The set is now a lively street corner just after rain (new for this series:
   earlier videos used a bathroom, a cafe, a kitchen, a desk, a beach). Rules for the new props:
   - The shirt is ONE simple one-piece plain gray tee (no words, logo, pocket or pattern) that sits low on his round
     body, entirely below his eyes, with his two short arm nubs poking out of its sleeves. It never covers his face,
     never rides up, never comes off, and is the same in every clip. He has no neck and no shoulders: describe it
     as a snug band of cloth round his middle with two short sleeves.
   - The wet patch is one dark-gray patch on the front of the shirt, the same shape, size and place from the moment
     it lands to the last frame. Sol himself is a flame and does not look wet, and nothing drips off him.
   - The car is ONE simple rounded one-piece cartoon car in one colour, with no driver seen, no words, no number
     plate text. It crosses the frame once, hits one puddle by the kerb, and is gone; it is in clip 01 only. The
     splash is one sheet of water drops that flies from the puddle to Sol's front and then stops. Make the hit
     obvious and comic and his reaction big (rule: "make the hit obvious and the reaction big"), but he is never
     knocked flat and it must not look like he is hurt.
   - A line is said only when its subject is on screen, so the shirt and Sol's pride in it are visible before
     "nice shirt".

B. MORE SCIENTIFIC. V3 said light "bounces", "goes deeper" and that wet fabric "traps more light" without naming
   what happens. Name the real processes in real words, each explained in passing the first time it is used:
   scatter / scattering, reflect, refract (bend), absorb, and the idea that how strongly light is turned back at
   a boundary depends on how different the two materials are for light (you may say "refractive index" once if
   you explain it in the same breath as "how much a material bends light", and you may give the numbers air 1.0,
   water 1.33, cotton about 1.5 if they fit in a line). Cover both halves of the real mechanism: (1) with water in
   the gaps the fiber surfaces scatter much less light back toward the viewer, so light travels deeper and meets
   more dyed fiber; (2) light heading back out can be reflected back in at the water's own surface (total internal
   reflection: name it only if you can explain it in a clause). Each extra pass means more absorption by the dye.
   Stay correct and stay plain: sentences a curious middle or high school student follows on first hearing. A real
   term replaces a vague phrase; do not stack jargon on top of the old wording.

C. A DEFINITE CONCLUSION. The last Narrator line states the answer to the title question outright, as a fact a
   viewer could repeat: what is really happening and what is not (the cloth has not changed colour; less light is
   coming back to the eye, because more of it is absorbed). No recap of the steps, no soft "just", no question, no
   slogan.

KEEP FROM V3: the document format; at most TWO close-ups without Sol, with different framings (the steep
three-quarter look down on the dry weave, the side-on slice of the wet weave) and Sol reacting right after them;
gold light arrows that thin and dim to bronze as light is absorbed; the dry-versus-wet arrow comparison on the
shirt (now the shirt Sol is wearing, so he is in that shot); the ending order (Sol looks up and listens through
the last line, nods once after it, then one happy face, no black).

WHAT TO RETURN
One plain-text episode document in exactly the format of EXAMPLE A below and of your V3, from the title line down
to the "Accuracy" paragraph, then TITLE / DESCRIPTION / HASHTAGS. It must hold everything an animator needs:
1. Title line (SCRIPT V4), then a short header: runtime, number of shots, spoken word count, voice.
2. "DIALOGUE AND WHAT SOL DOES": every clip in order with the Narrator's exact final words and what Sol does.
   Expression names in CAPITALS, only from the 38 names in the expression list below.
3. "HOW IT IS FILMED": the set, fixed places of Sol and every prop, how light is shown, the camera idea, the gags
   (each used once), what stays identical from clip to clip.
4. One "CLIP NN — name — seconds" block per clip with Camera, Action, Eyes, Narrator (start and end inside the
   clip), Arrows/overlays, Sound, Props in frame.
5. "Accuracy": the real physics, what is simplified, what is uncertain.

HARD RULES (from the pasted guidelines; "current-rules.md" wins every disagreement, and its "Superseded" table
lists what no longer applies: no on-twos, no paired stills, no Sol voice)
- Narrator only. Sol is silent and mouthless and answers by acting. The Narrator talks TO Sol and reacts to what
  he does, including at least once in the middle of the film. No "Got it?"-style check-in.
- TIMING AT THE REAL VOICE: Arthur reads about 2.3 words a second plus about 0.3 s at each comma or full stop
  inside a line. Time every Narrator window at that rate, leave about a second of quiet after every line, and
  keep every line and sound at least 0.3 s clear of its clip's end. Because the science is fuller, the film may
  run up to 45 s and about 85 to 95 spoken words; 6 to 8 clips; no clip longer than 8 s; no line longer than 17
  words (split a longer thought over two clips). State the word count and runtime.
- Every face stays at least 0.8 s; each swap rides a bounce of about 0.35 s. A face on nearly every beat.
- No hops: his feet stay on the ground (waddles, shuffles, squash-and-spring). He never reaches with an arm.
- Props are simple one-piece objects that keep every part, never morph, never appear or vanish inside a shot, and
  move only when something visibly moves them. Name only the props a clip shows.
- Science close-ups: slow steady camera, the same yarns, same size and colour in both, subject in the upper half
  of the frame (captions sit low).
- Every clip has a different angle and a travelling move at its start or end; the first clip opens with a fly-in
  from high over the whole set; no two neighbouring clips share a framing; the camera goes round things, never
  through them; a long shot never sits still.
- No words, letters or numbers anywhere in the picture (no shop signs, street signs, number plates).
- A different cartoon gag each time, each once; not the catfight, the slip, the curtain slap, singing in the
  shower or the dizzy spin (already used in earlier videos). A fall must not look like he dies.
- DESCRIPTION in the tracker's style (opens with the question in a few words, then "Sol and the Narrator find
  out:", the answer in plain sentences, the twist last; no dash characters). Five everyday HASHTAGS.

THE PASTED CONTEXT
"""
parts = [
 ("GUIDELINE 1 (wins every disagreement; section 2 holds Elaine's three new notes): guidelines/current-rules.md", f("guidelines/current-rules.md")),
 ("GUIDELINE 2 (older; its 'Current additions' box is current, the rest applies only where current-rules.md does not say otherwise): guidelines/video-script-guide.md", f("guidelines/video-script-guide.md")),
 ("GUIDELINE 3 (older; the script guide links to it for shot planning and Sol's acting): guidelines/shot-integration-and-sol.md", f("guidelines/shot-integration-and-sol.md")),
 ("CHARACTER REFERENCE: guidelines/sol-3d-model.md", f("guidelines/sol-3d-model.md")),
 ("CHARACTER REFERENCE, the expression set (38 names) and its marks: assets/sol-3d/eyes/README.md", f("assets/sol-3d/eyes/README.md")),
 ("EMOTION SOUNDS available (one per mood): amazed, bewilderment, cold-chill, confident, curiosity, daydreaming, exclamation, fearful, glee, greetings, heartbreak, inspiration, joy, laughter, love, pleased, pride, sadness, shocked, showmanship, shyness, sighing, sleepy, smirking, surprise, thought, worry, complete. Plus squeaks, boings and twinkles for actions.", ""),
 ("EXAMPLE A, the format to copy (an earlier episode; its header and build logs are history): episodes/shower_curtain/script.txt, first 170 lines", f("episodes/shower_curtain/script.txt", 170)),
 ("EXAMPLE B, the script Elaine read and liked: episodes/coffee_ring/script.txt", f("episodes/coffee_ring/script.txt")),
 ("YOUR SCRIPT V3 FOR THIS TOPIC, the one Elaine answered (rewrite it as V4): episodes/wet_shirt/neon/neon-answer-v3.txt", f("episodes/wet_shirt/neon/neon-answer-v3.txt")),
]
body = brief + "".join(f"\n\n<<<<< BEGIN {h} >>>>>\n{t}\n<<<<< END >>>>>" for h, t in parts)
out.write_text(body); print(len(body), "chars")
