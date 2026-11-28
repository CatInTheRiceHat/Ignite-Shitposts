import sys, pathlib
wf = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2]); topic = sys.argv[3]
def f(p, first=None):
    t = (wf / p).read_text()
    if first: t = "\n".join(t.split("\n")[:first])
    return t
brief = f"""You are writing the script and the animation plan for one episode of Ignite's short science videos
(vertical 9:16, about 30 to 40 seconds). Do not use any tools and do not ask questions: answer in ONE message
with the finished document. Everything you need is pasted below.

TOPIC (from Elaine's tracker sheet): "{topic}"

WHAT TO RETURN
One plain-text episode document in exactly the format of EXAMPLE A below (the shower-curtain script), from its
title line down to its "Accuracy" paragraph. It must hold everything an animator needs to build the video
without asking you anything:
1. Title line, then a short header: runtime, number of shots, spoken word count, voice (Narrator = Arthur; Sol
   has no voice and no mouth).
2. "DIALOGUE AND WHAT SOL DOES": every clip in order with the Narrator's exact final words and what Sol does in
   answer. Expression names in CAPITALS, taken only from the 38 names in the expression list below.
3. "HOW IT IS FILMED": the set (a NEW, lively place that suits the topic; not a bathroom, cafe, kitchen, desk or
   beach, which earlier videos used), fixed places of Sol and each prop, how the invisible thing (light) is shown
   (animated arrows or rays laid over the picture, and what colour they are), the camera idea, the list of gags
   (each used once), and what must stay identical from clip to clip.
4. One "CLIP NN — name — seconds" block per clip with: Camera (start view, the move with times, end view; the
   first clip opens with a fly-in from high over the whole set), Action (timed beats in seconds), Eyes (the
   expression timeline with times, each swap rides a bounce), Narrator (start and end time of the line inside
   the clip, starting only AFTER the thing the line is about is on screen), Arrows/overlays (what is drawn over
   the picture and when), Sound (at most one emotion sound from the list for every other face, plus any squeak
   or boing), and Props in frame (only what this clip shows).
5. "Accuracy": the real physics in a few sentences, what is simplified, and what is still uncertain.
6. After the document, three short extras: TITLE (a YouTube headline in title case), DESCRIPTION (blurb in the
   style of the tracker rows quoted in the rules: opens with the question, names Sol and the Narrator, gives the
   answer plainly, ends on the twist), HASHTAGS (five, specific to this video).

HARD RULES (all from the pasted guidelines; where two guidelines disagree, "current-rules.md" wins and its
"Superseded" table lists what no longer applies: no on-twos, no paired stills, no Sol voice)
- Narrator only. Sol is silent and mouthless and answers by acting. The Narrator talks TO Sol and reacts to what
  he does. No "Got it?"-style check-in at the end.
- Ending order: Sol looks up and listens through the last line, nods once when it is over, then makes one happy
  face. The video ends on that, no black.
- About 75 to 90 spoken words in total, 6 to 8 clips, each clip 4 to 8 seconds, leaving about a second of quiet
  after every line. A line is said only when its subject is already on screen.
- Sol never reaches for a prop with an arm; he hops beside it, bumps it with his side or leans. His feet stay
  on the ground. Props are simple one-piece objects that keep every part, never morph, never appear or vanish
  inside a shot, and move only when something visibly moves them.
- The thing being explained gets its own close-up science shots with a slow, steady camera, and it is the same
  object, size and colour in every clip. Keep the close-up's subject in the upper half of the frame (captions
  sit low).
- Every clip has a different angle and a travelling camera move at its start or end; no two neighbouring clips
  share a framing; the camera goes round things, never through them.
- No words, letters or numbers anywhere in the picture (no signs, labels or logos on the shirt).
- Sol is a cute cartoon goober: plan a face for nearly every beat, and use a different cartoon gag each time
  (never the catfight, the slip, the slap, singing in the shower or the dizzy spin again: those were used).
  A fall must not look like he dies (no X eyes, no lying still).
- Explain every link of the cause and effect in plain words for a curious middle-school student, and keep it
  physically correct. Do not write the explanation as slogans or clipped fragments.

THE PASTED CONTEXT
"""
parts = [
 ("GUIDELINE 1 (wins every disagreement): guidelines/current-rules.md", f("guidelines/current-rules.md")),
 ("GUIDELINE 2 (older; follow it only where current-rules.md does not say otherwise): guidelines/video-script-guide.md", f("guidelines/video-script-guide.md")),
 ("GUIDELINE 3 (older; the script guide links to it for shot planning and Sol's acting): guidelines/shot-integration-and-sol.md", f("guidelines/shot-integration-and-sol.md")),
 ("CHARACTER REFERENCE: guidelines/sol-3d-model.md", f("guidelines/sol-3d-model.md")),
 ("CHARACTER REFERENCE, the expression set (38 names) and its marks: assets/sol-3d/eyes/README.md", f("assets/sol-3d/eyes/README.md")),
 ("EMOTION SOUNDS available (one per mood): amazed, bewilderment, cold-chill, confident, curiosity, daydreaming, exclamation, fearful, glee, greetings, heartbreak, inspiration, joy, laughter, love, pleased, pride, sadness, shocked, showmanship, shyness, sighing, sleepy, smirking, surprise, thought, worry, complete. Plus squeaks, boings and twinkles for actions.", ""),
 ("EXAMPLE A, the format to copy (latest episode; its header and build logs are history, your document needs only the script parts): episodes/shower_curtain/script.txt, first 170 lines", f("episodes/shower_curtain/script.txt", 170)),
 ("EXAMPLE B, the script Elaine read and liked: episodes/coffee_ring/script.txt", f("episodes/coffee_ring/script.txt")),
]
body = brief + "".join(f"\n\n<<<<< BEGIN {h} >>>>>\n{t}\n<<<<< END >>>>>" for h, t in parts)
out.write_text(body); print(len(body), "chars")
