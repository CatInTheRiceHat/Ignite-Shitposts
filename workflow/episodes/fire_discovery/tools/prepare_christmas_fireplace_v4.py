"""New Christmas opening only; preserve exact approved landscape/campfire pairs."""
import json
import re
import shutil
from pathlib import Path

EP=Path(__file__).resolve().parents[1]
OLD=EP/'revisions/night-camp-v3'
OUT=EP/'revisions/christmas-fireplace-v4'
if OUT.exists(): raise FileExistsError(OUT)
for folder in ['keyframes','reviews']:(OUT/folder).mkdir(parents=True,exist_ok=True)
(OUT/'audio').symlink_to('../../audio',target_is_directory=True)
for sid in ['02','05']:
    for end in ['first','last']:
        shutil.copy2(OLD/'keyframes'/f'{sid}-{end}.png',OUT/'keyframes'/f'{sid}-{end}.png')

state=json.loads((OLD/'scene-plan.json').read_text())
s=state['scenes']['01']
s.update(title='A question beside the Christmas fireplace',
    room='A richly detailed, cozy cottage living room decorated for Christmas. On screen-left, a deep green fir tree has red and gold baubles, a small gold star and warm little string lights, with four differently wrapped presents tucked around its base. On screen-right, a broad charcoal-gray stone fireplace contains three short stacked logs and a low warm wood fire. The mantel carries a lush evergreen garland with red bows; three red-and-cream stockings hang from the mantel sides, clear of the dark fire opening. A wreath with a red ribbon hangs above it. A small window in the back wall shows still snowy fir trees in cool blue winter daylight. A few warm string lights cross the upper wall. A basket of split firewood sits to the right of the hearth, and a folded knitted throw lies over the edge of a background chair. A muted red-and-cream woven rug and warm wooden floor complete the room. Warm amber hearth and tree light mix with cool window fill; no floating particles. These decorations belong to this specific Christmas opening.',
    framing='Medium-wide full-body portrait view, camera at Sol eye height with a gentle downward angle. Sol stands on the floor just in front of the hearth apron at x=43%, feet y=78%, height about30%. The fireplace is on screen-right, its firebox centered x=76%, y=60%; the Christmas tree fills the left background from y=15% to y=66%. Frame the decorated mantel, wreath, snowy window and presents so they read as layered background details. Keep a clear gap around Sol and both feet; lower fifth is a calm area of rug/floor for editable captions. Fixed camera.',
    first='Exactly one original Sol stands in a shallow three-quarter orientation toward the fire on screen-right, with both original dark oval eyes visible. Both short rounded arms are low and gently forward, enjoying the warmth. His two tiny feet rest flat on the floor. All Christmas decorations are already in place and tree lights glow steadily. He wears no costume or accessories.',
    last='The same Sol in exactly the same Christmas room, camera, scale, facing direction and supported foot positions. Only the short arm nearest the fireplace is raised a little toward the burning logs in one compact questioning gesture; the other arm stays low. Keep the normal original oval eyes, mouthless face, short limbs and all flame layers unchanged. The tree, presents, garland, stockings, wreath, snowy window, firewood basket, throw and rug retain their exact positions.',
    action='Over the first1.6s, lift only the short arm nearest the fireplace along one small direct path toward the burning logs as Sol asks his question. Add gentle connected body/tip wiggle that follows the gesture and settles, keeping both feet supported. Preserve Sol\'s original small dark oval eyes, mouthless face and short limbs. The low fire flickers while attached to its three logs. Keep all Christmas decorations, tree lights, snowy window view, rug, furniture and camera stable. End in the supplied small questioning pose by2.0s and hold through the3s source tail. No walking, hopping, independent face turn or emitted particles.',
    transition='Hard cut from the richly decorated Christmas fireplace to the approved golden late-afternoon natural-fire landscape, introducing historical context.')
identity='Preserve the original mascot design: compact broad flame silhouette, asymmetric main tip and rounded side lobes, substantial red outer layer, original orange layer and broad cream inner flame with its lobed crown and rounded lower face. Two small close-spaced low-set tall oval eyes are completely opaque navy #1C2447, without highlights or extra pupils. Short rounded arms and tiny red stubby feet keep their original proportions and attachment points. The cream face is completely mouthless and blank beneath the eye pair. Sol has no hat, clothing, ornaments or particles; the Christmas decorations belong to the room.'
style='Soft matte gouache brushwork, visible layered paint and subtle paper texture cover Sol, every decoration, furniture, fire and surrounding surfaces alike. Use softly painted edges and coherent perspective/contact shadows. Keep the background rich with distinct Christmas objects, rendered as readable painted shapes, and preserve clear contrast around Sol. No inked outlines, glossy plastic, photographic fire, text, captions or watermark.'
cadence='Animate on twos at final30fps: every source pose or painted state stays unchanged for two consecutive frames,15 updates per second at normal speed; longer holds use complete pairs. Apply to Sol, wood fire and local animated light. Background, Christmas lights and paint texture stay stable. No interpolation, blending, optical flow or concealing blur. Enforce and verify during editing. No generated speech, music, effects, text or captions.'
s['first_prompt']='\n\n'.join(['Create a complete new vertical painted scene: Sol beside a fireplace in a detailed Christmas living room.',s['room'],s['framing'],s['first'],identity,style])
s['last_prompt']='\n\n'.join(['Use the supplied Christmas first frame as the exact composition reference. Create its matching last still, changing only Sol\'s small near-fire arm gesture.',s['last'],identity,style,'Keep the warm lighting, every background object, framing, floor contact and Sol design consistent with the supplied first frame.'])
s['video_prompt']='\n\n'.join([s['action'],identity,style,cadence])
old_selection=json.loads((OLD/'reviews/frame-pair-selection.json').read_text())
state.update(status='New Christmas01 pair pending; exact02/05 pairs approved by user and preserved unchanged.',selected_pairs={},frame_approvals={},preliminary_still_review={},unselected_candidates={},superseded_revision='../night-camp-v3/',clarification='Elaine requests more visual stimulation and background detail, specifically regenerate the fireplace at Christmas. The rest are okay: preserve approved02/05 pairs exactly. Scope is this episode, not shared art guidelines.')
state['lighting_sequence'][0]='01 cozy Christmas room with winter daylight, warm tree lights and fireplace warmth'
state['approved_unchanged_scenes']={sid:{'source_revision':'../night-camp-v3/','source_selection':'../night-camp-v3/reviews/frame-pair-selection.json','source_packet':old_selection['selected_pairs'][sid]['packet'],'first_sha256':old_selection['selected_pairs'][sid]['first_sha256'],'last_sha256':old_selection['selected_pairs'][sid]['last_sha256'],'approval_user_message':old_selection['selected_pairs'][sid]['approval_user_message']} for sid in ['02','05']}
(OUT/'scene-plan.json').write_text(json.dumps(state,indent=2)+'\n')

script=(OLD/'script.txt').read_text().replace('HOW FIRE WAS DISCOVERED — NIGHT CAMP REVISION','HOW FIRE WAS DISCOVERED — CHRISTMAS FIREPLACE REVISION')
script=script.replace('Three proposed scene replacements:01,02,05.', 'Scene01 is regenerated as a detailed Christmas living room. Scenes02/05 endpoint pairs were approved with “the rest areok” and are retained exactly from night-camp-v3.')
script=script.replace('Lighting now varies from daylight interior','Lighting now varies from a warm Christmas room with cool winter window light')
section=f"SCENE 01 — {s['title']} — edit2.333s (0.000–2.333s)\nSetting: {s['room']}\nFraming: {s['framing']}\nFirst frame: {s['first']}\nAction: {s['action']}\nLast frame: {s['last']}\n"+'\n'.join(s['dialogue'])+f"\nSpeaker cues: {s['voice']}\nNarrator attention: {s['attention']}\nNext cut: {s['transition']}\nGeneration length:3s; trim to actual voice timing2.333s after review.\nMotion: exact unchanged two-frame states at30fps, normal-speed action and1x speech.\n\n"
script=re.sub(r'SCENE 01 —.*?(?=SCENE 02 —)',lambda _:section,script,flags=re.S)
(OUT/'script.txt').write_text(script)
prompts=(OLD/'higgsfield-prompts.txt').read_text().replace('HOW FIRE WAS DISCOVERED — NIGHT CAMP REVISION','HOW FIRE WAS DISCOVERED — CHRISTMAS FIREPLACE REVISION')
prompts=prompts.replace('Reuse the unapproved01 pair unchanged. Generate new02 late-afternoon and05 three-Sol night-campfire first/last pairs.','Generate a new01 Christmas fireplace pair. Reuse the exact approved02 late-afternoon and05 three-Sol night-campfire pairs from night-camp-v3, without new image jobs for those scenes.')
prompts=prompts.replace('Scene01 establishes an indoor fireplace.', 'Scene01 establishes a richly decorated Christmas room and fireplace.')
prompts=re.sub(r'SCENE 01 — [^\n]+',f"SCENE 01 — {s['title']} — generate3s / edit2.333s",prompts)
for kind,label,key in [('IMAGE','I01-FIRST','first_prompt'),('IMAGE','I01-LAST','last_prompt'),('VIDEO','V01','video_prompt')]:
    prompts=re.sub(rf'BEGIN {kind} PROMPT {label}\n.*?END {kind} PROMPT {label}',lambda _:f"BEGIN {kind} PROMPT {label}\n{s[key]}\nEND {kind} PROMPT {label}",prompts,flags=re.S)
assert prompts.count('BEGIN IMAGE PROMPT ')==10 and prompts.count('BEGIN VIDEO PROMPT ')==5
(OUT/'higgsfield-prompts.txt').write_text(prompts)

plan=json.loads((OLD/'shot-plan.json').read_text());plan['status']=state['status'];plan['episode_revision_direction']=state['clarification']
c=next(c for c in plan['clips'] if c['id']=='01')
c.update(title=s['title'],action=s['action'],motion_prompt_action=s['action'],first_frame=s['first'],last_frame=s['last'],clean_first_frame=s['first'],clean_last_frame=s['last'],framing_prompt=s['framing'],setting_and_framing=s['room']+' '+s['framing'],image_prompts={'first':s['first_prompt'],'last':s['last_prompt']},video_prompt=s['video_prompt'],next_cut=s['transition'],lighting=s['room'])
c['camera']={'shot_size':s['framing'],'movement':'Fixed source camera','editing':'No automatic push.'}
c['performance_beats']=[{'body':s['action'],'cue':s['voice'],'gaze':s['attention']}]
for key in ['generated_stills','generated_video','first_frame_source','retry_reason','eye_gaze_squish_trial','body_up_tilt_trial','bounce_flame_accents']:c.pop(key,None)
for c in plan['clips']:
    if c['id'] in ['02','05']:c['approved_frame_source']=state['approved_unchanged_scenes'][c['id']]
(OUT/'shot-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
refs=json.loads((OLD/'generation-inputs.json').read_text())['reference_inputs'][:3]
inputs={'scope':state['clarification'],'reference_inputs':refs,'new_requests':[{'index':1,'scene':'01','endpoint':'first','params':{'model':'nano_banana_2_1','resolution':'2k','thinking_level':'medium','aspect_ratio':'9:16','count':1,'prompt':s['first_prompt']+'\n\nReference roles: image1 controls the original Sol identity; image2 controls short rounded arm anatomy only, without microphone or cable; image3 supplies the layered gouache finish only. Generate this new Christmas room with EXACTLY ONE Sol, without inheriting spring scenery or extra characters.','medias':[{'role':'image','value':r['media_id']} for r in refs]}}]}
(OUT/'generation-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
feedback=EP/'feedback.txt';t=feedback.read_text();entry='''29. Elaine requests more stimulation and detail in the background, specifically
    regenerating the fireplace as Christmas. She says “the rest areok” in
    response to the displayed01/02/05 pairs:02 late-afternoon landscape and05
    three-Sol night-campfire exact pairs are approved, recorded canonically in
    night-camp-v3. Only01 is replaced. Implementation: decorated Christmas
    tree, gifts, garland, stockings, wreath, warm lights and a snowy window,
    with clear space around the original mouthless Sol and his gesture.
    These are episode-specific scene notes, not shared art-style requirements.
    New01 first/last frames still need explicit approval before animation.

''';t=t.replace('IMPLEMENTATION / REVIEW STATUS',entry+'IMPLEMENTATION / REVIEW STATUS');feedback.write_text(t)
print('Prepared Christmas01 revision; approved02/05 copied byte-for-byte with source approval references.')
