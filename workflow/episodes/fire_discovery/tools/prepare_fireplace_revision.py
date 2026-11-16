"""Prepare a separate three-scene revision without changing the selected cut."""
import json
import re
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
OUT = EP / 'revisions/fireplace-v1'
OUT.mkdir(parents=True, exist_ok=True)

STYLE = ('Soft matte gouache brushwork, visible layered paint and subtle paper texture on every subject, prop and surface. '
         'Broad readable shapes, gentle painted shading, coherent perspective and contact shadows. '
         'Define forms through light and color with softly painted edges, without inked outlines, gloss, plastic rendering or heavy grain.')
IDENTITY = ('Match the original Sol mascot: compact broad flame body, asymmetric main tip and side lobes, substantial red outer layer, '
            'original orange layer and broad cream inner flame with its crown and rounded lower face. Keep the two small, close-spaced, '
            'low-set tall oval eyes opaque navy #1C2447 with no highlights, whites or pale rims. Preserve short rounded arms and tiny stubby '
            'feet directly below the body; no fingers, long limbs, neck or separate torso. Completely mouthless, blank beneath the eye pair. '
            'Keep the face attached to the coherent filled body. No particles, sparks, droplets or detached pieces from Sol.')
MOTION = ('Animate on twos at final30fps: each source pose or painted state stays unchanged for two consecutive frames, '
          '15 updates per second, at normal speed; longer holds use complete pairs. Apply this to Sol when present, '
          'actual fire and animated local light. Background and painted texture stay stable. No interpolation, blending, '
          'optical flow or concealing blur. Enforce and verify exact source pairs in editing.')
ROOM = ('A small lived-in room with a simple ochre plaster wall, a broad charcoal-gray stone fireplace on screen-right, '
        'a recessed dark firebox containing two short horizontal logs and one low contained faceless wood fire, '
        'a flat slate hearth and muted blue-gray wooden floor. Cool soft window light enters from off-screen left; '
        'the hearth gives a restrained warm tint to the nearby stones and Sol. No decorations, text, tools or extra characters.')

scenes = {
 '01': {
  'title':'A question beside the fireplace', 'duration':70/30, 'generation_duration':3,
  'dialogue':['Sol: “Who actually discovered fire?”'],
  'framing':'Medium-wide full-body view at Sol face height, slight downward angle; Sol x=30%, height40%, feet y=74%; fireplace at x=72%, logs y=64%. Fixed camera; lower fifth quiet for captions.',
  'first':'Sol stands on the flat hearth apron, clear of the firebox, in a shallow three-quarter orientation toward the logs with both eyes visible. Both short arms are held low and slightly forward as if enjoying the warmth; feet rest flat and separated beneath the body.',
  'last':'The same Sol, room and framing. The arm nearest the fireplace is now raised a little toward the logs in one compact questioning gesture. The other arm stays low, both feet supported and gaze directed toward the fire; original anatomy and eye design unchanged.',
  'action':'Over the first1.6s, lift only the short arm nearest the fireplace along a small direct path toward the burning logs as Sol asks his question. Gentle connected body/tip wiggle follows the gesture and settles. Do not walk, hop or turn the face independently. The low fire flickers within the same log contact; no flying sparks. End in the supplied small questioning pose.',
  'attention':'Only Sol speaks; no Narrator attention cue in this scene.',
  'voice':'Existing01-01-sol at local0.080–1.886s, unchanged1x.',
  'transition':'Hard cut from the contained household fire to an empty landscape showing natural fire; the cut introduces historical context, not an adjacent room.'
 },
 '02': {
  'title':'Natural fire before people', 'duration':4.8, 'generation_duration':5,
  'dialogue':['Narrator: “We don\'t know. Natural fires existed long before people.”'],
  'framing':'Wide elevated three-quarter view across an open dry grassy basin, not an enclosed woodland. A low charred fallen branch and small natural fire occupy x=56%, y=60%; distant layered slate-blue hills below broad gray cloud banks. Static camera, no zoom. Empty pale foreground in lower fifth.',
  'first':'No people or Sol. An isolated dry fallen branch lies on bare earth among sparse straw-gold grass, with a small orange fire already rooted on its center. A single soft gray plume rises above it. The surroundings remain mostly unburned, with no campsite, buildings, tools or stone ring.',
  'last':'Exactly the same elevated view, branch position, hills, grass and cloud shapes. The small fire remains rooted to the same branch, with its connected upper tongues in a slightly different natural flicker state and the thin smoke plume a little higher. No new fire patches or objects.',
  'action':'Continue the already-established small natural wood fire while the Narrator explains that fire existed before people. Only its connected upper flame shapes flicker softly and the thin smoke plume rises slowly. Keep the flame base fixed on the fallen branch. Keep the entire terrain, branch, grass and cloudy sky stable. No new ignition, lightning, sweeping flame front or human activity.',
  'attention':'Sol is absent throughout; Narrator is off-screen.',
  'voice':'Existing02-01-narrator at local0.800–4.596s, unchanged1x.',
  'transition':'Cut to the existing storm-tree shot for a specific example of natural ignition.'
 },
 '05': {
  'title':'Back at the hearth, understanding the difference', 'duration':5.2, 'generation_duration':6,
  'dialogue':['Sol: “So finding fire wasn\'t the same as making it.”','Narrator: “Right.”'],
  'framing':'Return to the same room established in01, from a camera30degrees closer to the front of Sol on the same side of the fireplace. Medium full-body view at eye height, slight downward angle; Sol x=38%, height48%, feet y=76%; the matching hearth/firebox occupies the upper-right half. Keep both feet and full flame tip visible, lower fifth quiet. Fixed camera.',
  'first':'Sol stands on the same hearth apron, shallow three-quarter toward the logs, both eyes visible and both short arms at his flanks. Preserve the room materials, two logs, low fire, floor geometry and direction of light from01; this is a deliberate closer camera angle, not a new room.',
  'last':'Sol holds both stubby arms slightly open in a low understanding gesture. His whole compact body, flame layers and attached face share a small backward/upward listening tilt toward the fixed point just above camera; both original tall navy ovals retain shape and close spacing. Both feet remain supported. Same low fire and room, no extra objects.',
  'action':'During Sol\'s sentence, open both short arms once into the small low understanding gesture, with gentle attached body/tip follow-through and unchanged limb lengths. By local3.6s, tilt the whole compact body and attached face slightly upward toward the fixed Narrator point above camera. Maintain that gaze, low open arms and gentle listening idle throughout Arthur\'s Right at4.0–4.9s and the ending. Keep feet supported; no face slide, eye squish, mouth, particles or hops. The low fire remains fixed to its logs.',
  'attention':'Gaze ready by3.6s, before Arthur at4.0s; maintain above-camera listening through his complete0.9s take and final hold.',
  'voice':'Existing05-01-sol at0.080–2.914s; original-release05-02-narrator at4.000–4.900s. Unchanged1x; preserve final picture through5.2s.',
  'transition':'Readable final hold, existing music fade and complete Right release.'
 }
}

requests = {}
for sid,s in scenes.items():
 for which in ['first','last']:
  lead = ('Create one complete vertical painted still. ' if which=='first' else
          'Use the supplied starting still as the exact composition and continuity reference. Create only its matching ending still. ')
  setting = ROOM if sid!='02' else 'An uninhabited natural grassland landscape under cool overcast daylight; warm light is confined to the small existing fire.'
  s[which+'_prompt']='\n\n'.join([lead+s['framing']+' '+setting,s[which],IDENTITY if sid!='02' else 'No mascot, human, human-made structure or text.',STYLE,'No text, captions or watermark.'])
 s['video_prompt']='\n\n'.join([s['action'],'Fixed source camera; preserve exact endpoint composition, object contacts, framing and light.',IDENTITY if sid!='02' else 'No characters or human activity.',STYLE,MOTION,'No generated speech, music, sound effects, text or captions.'])

old_prompts=(EP/'higgsfield-prompts.txt').read_text()
old_script=(EP/'script.txt').read_text()
new_script=['HOW FIRE WAS DISCOVERED — FIREPLACE REVISION\n\nThree proposed scene replacements:01,02,05. Existing03/04 footage, seven voice takes, dialogue, music, captions and extended ending retained. Target picture duration25.8s. New frame pairs require explicit user approval before animation. Current selected/completed cut remains intact.\n']
new_prompts=['HOW FIRE WAS DISCOVERED — FIREPLACE REVISION\n\nFive scenes: exactly ten image prompts and five video prompts. New images/clips only for01,02,05. Scenes03/04 retain their existing endpoints, footage and prompt text.\n\nSETTINGS / REFERENCES / EDITING — OUTSIDE COPYABLE PROMPTS\nImages: Nano Banana2.1,2k,9:16,count1,thinking_level medium. Video: Gemini Omni Flash1.2,1080p,9:16, approved first AND last frame; no video submitted before approval. Original Mascot controls identity, Microphone controls short-arm anatomy only, Spring/Practical Learning/Thank You control paint only. Scene01 first establishes the new room; use it as continuity input for05. Each new last image uses its own first image as composition input. Settings and media IDs are recorded separately in generation-inputs.json. Existing Arthur/custom Sol takes stay1x. White/orange editable captions stay unchanged. Sound correction: advance the supplied sting6frames so its ~0.19s impact meets the actual flash at9.733333s. Native generated audio is discarded.\n']
elapsed=0
durations={'01':70/30,'02':4.8,'03':206/30,'04':6.6,'05':5.2}
for sid in ['01','02','03','04','05']:
 if sid in scenes:
  s=scenes[sid]
  new_script += [f"SCENE {sid} — {s['title']} — edit{durations[sid]:.3f}s ({elapsed:.3f}–{elapsed+durations[sid]:.3f}s)\nSetting: {ROOM if sid!='02' else 'Open uninhabited grassland, small natural wood fire, distant hills and cloudy sky.'}\nFraming: {s['framing']}\nFirst frame: {s['first']}\nAction: {s['action']}\nLast frame: {s['last']}\n"+'\n'.join(s['dialogue'])+f"\nSpeaker cues: {s['voice']}\nNarrator attention: {s['attention']}\nNext cut: {s['transition']}\nGeneration length: {s['generation_duration']}s, trimmed to actual voice timing after review.\nMotion: {MOTION}\n"]
  new_prompts += [f"SCENE {sid} — {s['title']} — generate{s['generation_duration']}s / edit{durations[sid]:.3f}s\nDialogue context, outside prompts:\n"+'\n'.join(s['dialogue'])+'\n']
  for which in ['first','last']:
   label=f'I{sid}-{which.upper()}'
   new_prompts += [f"Output: keyframes/{sid}-{which}.png (relative to this revision)\nBEGIN IMAGE PROMPT {label}\n{s[which+'_prompt']}\nEND IMAGE PROMPT {label}\n"]
  new_prompts += [f"Inputs: this revision's explicitly approved{sid}-first.png and{sid}-last.png.\nOutput: clips/{sid}-scene.mp4 (planned)\nBEGIN VIDEO PROMPT V{sid}\n{s['video_prompt']}\nEND VIDEO PROMPT V{sid}\n"]
 else:
  section=re.search(rf'SCENE {sid} —.*?(?=\nSCENE \d|\nEDITORIAL NOTES|\Z)',old_script,re.S).group(0)
  if sid=='03':
   section=section.replace('begins at local2.600s/global9.733333s on the visible lightning pair','begins at local2.400s/global9.533333s; its main impact about0.19s later aligns with the visible lightning pair at local2.600s/global9.733333s')
  new_script += [section+'\n']
  new_prompts += [f'SCENE {sid} — RETAIN EXISTING APPROVED-INPUT FOOTAGE; no regeneration requested.\n']
  for kind,label in [('IMAGE',f'I{sid}-FIRST'),('IMAGE',f'I{sid}-LAST'),('VIDEO',f'V{sid}')]:
   new_prompts += [re.search(rf'BEGIN {kind} PROMPT {label}\n.*?END {kind} PROMPT {label}',old_prompts,re.S).group(0)+'\n']
 elapsed+=durations[sid]

for filename,content in [('script.txt','\n'.join(new_script)),('higgsfield-prompts.txt','\n'.join(new_prompts))]:
 path=OUT/filename
 if path.exists(): raise FileExistsError(path)
 path.write_text(content)
(OUT/'scene-plan.json').write_text(json.dumps({'status':'New stills pending; no new pair approval or clip generation','scenes':scenes,'retained_scenes':['03','04'],'original_edit':'../../edit-sound-v4.json','picture_duration_sec':25.8,'dialogue_changed':False},indent=2)+'\n')
assert len(re.findall(r'^BEGIN IMAGE PROMPT ',(OUT/'higgsfield-prompts.txt').read_text(),re.M))==10
assert len(re.findall(r'^BEGIN VIDEO PROMPT ',(OUT/'higgsfield-prompts.txt').read_text(),re.M))==5
print('Prepared separate five-scene storyboard and10 image/5 video prompts; three scene replacements planned.')
