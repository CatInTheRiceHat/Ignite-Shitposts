"""Apply episode-only scene replacement direction, preserving earlier candidates."""
import json
import re
import shutil
from pathlib import Path

EP=Path(__file__).resolve().parents[1]
OLD=EP/'revisions/fireplace-v1'
OUT=EP/'revisions/scene-replacements-v2'
if OUT.exists(): raise FileExistsError(OUT)
OUT.mkdir(parents=True)
(OUT/'keyframes').mkdir()
(OUT/'reviews').mkdir()
(OUT/'audio').symlink_to('../../audio',target_is_directory=True)
for sid in ['01','02']:
    for end in ['first','last']:
        shutil.copy2(OLD/'keyframes'/f'{sid}-{end}.png',OUT/'keyframes'/f'{sid}-{end}.png')

state=json.loads((OLD/'scene-plan.json').read_text())
s=state['scenes']['05']
s.update(
    title='Understanding beside a campfire after dark',
    room='A small campsite on an open ridge at blue hour, with a low stone-ring campfire, a simple muted-ochre canvas tent in the far upper-right, packed mauve-gray earth and broad distant blue hills. An open slate-blue evening sky replaces the enclosed woodland or indoor walls. Cool ambient evening light and gentle local amber firelight; no stars, flying embers or decorative particles.',
    framing='Medium-wide full-body shot at Sol face height, slightly downward. Sol stands on SCREEN-RIGHT at x=66%, height38%, feet y=76%; a low campfire occupies SCREEN-LEFT at x=28%, y=64%, with a clear gap from Sol. The small tent is distant, at x=77%, y=38%; hills and open sky form broad simple layers. Fixed camera. Quiet lower fifth for editable captions.',
    first='Sol stands on solid packed earth beside the campfire, both tiny feet supported and both short rounded arms lowered at his flanks. His compact body is angled shallowly toward the fire on screen-left, with both original dark oval eyes visible. A small contained flame burns on three charred pieces of wood inside a low ring of stones; no people are present.',
    last='Exactly the same campsite, camera, Sol scale, ground contacts, tent, hills, stones and three wood pieces. Sol holds both stubby arms slightly open in a low gesture of understanding. His compact body, filled flame layers and attached face tilt gently backward/up together toward the fixed Narrator point just above camera. Preserve original tall close-spaced navy oval eyes, broad cream inner flame, unchanged limb lengths and supported feet.',
    transition='Hold the clear upward listening pose through the complete Right release and existing music fade; no additional scene.'
)
identity=('Preserve the original mascot as a whole: broad compact flame silhouette, asymmetric tip, rounded side lobes, substantial red outer layer, '
          'original orange layer and broad cream inner flame with a lobed crown and rounded lower face. Two small close-spaced low-set tall oval eyes '
          'are opaque navy #1C2447 with no highlights, whites, gray rims or extra pupils. Short rounded arms and tiny stubby feet keep their original '
          'lengths and attachment points. Completely mouthless and blank below the eye pair. No nose, fingers, long legs, neck or separate torso. '
          'Keep the face and all filled flame layers coherent. Sol emits no sparks, particles, droplets or detached flame pieces.')
style=('Soft matte gouache brushwork, visible layered painted color, subtle paper texture and broad readable shapes across Sol, tent, fire, rocks, '
       'earth and sky. Coherent perspective, gentle shading and contact shadows. Keep the cream face readable in the low light. '
       'Define forms through light and color without ink outlines, gloss, plastic surfaces, heavy grain or photographic fire.')
s['first_prompt']='\n\n'.join(['Create one complete new vertical painted scene of Sol beside an outdoor campfire after dark.',s['room'],s['framing'],s['first'],identity,style,'No text, captions, watermark, indoor fireplace, walls or dense woodland.'])
s['last_prompt']='\n\n'.join(['Create the matching last still using the supplied campsite first frame as the exact composition reference.',s['framing'],s['last'],identity,style,'Keep the low campfire attached to its wood; no flying sparks. No text, captions or watermark.'])
s['video_prompt']='\n\n'.join([s['action'].replace('The low fire remains fixed to its logs.','The low campfire remains fixed to its wood inside the stone ring. Keep the tent, hills, ground, stones and camera stable.'),'Preserve the exact supplied campsite composition and lighting. No camera move.',identity,style,'Animate on twos at final30fps: every source pose or painted state stays unchanged for two consecutive frames,15 updates per second at normal speed; longer holds use complete pairs. Apply to Sol, campfire and local animated light. Stable background and paint texture; no interpolation, blending, optical flow or concealing blur. Enforce and verify the cadence during editing.','A brief natural blink is allowed and returns promptly to the original dark ovals and upward gaze. No generated speech, music, sound effects, text or captions.'])
state['status']='Episode-only scene replacement revision.01/02 pairs carried forward unchanged and unapproved; new05 campfire pair pending.'
state['original_edit']='../../edit-thunder-sync-v5.json'
state['selected_pairs']={sid:value for sid,value in state.get('selected_pairs',{}).items() if sid!='05'}
state['frame_approvals']={}
state['preliminary_still_review'].pop('05',None)
state['superseded_revision']='../fireplace-v1/'
state['clarification']='Replace repeated clips in this video by generating new scenes from first/last stills; specific scene choices do not belong in shared art-style guidelines.'
(OUT/'scene-plan.json').write_text(json.dumps(state,indent=2)+'\n')

script=(OLD/'script.txt').read_text().replace('FIREPLACE REVISION','SCENE REPLACEMENTS').replace('Current selected/completed cut remains intact.','Current selected/completed cut remains intact. Scene05 now uses a different outdoor campsite; the earlier second fireplace view is preserved only as an unused candidate.')
section=f"SCENE 05 — {s['title']} — edit5.200s (20.600–25.800s)\nSetting: {s['room']}\nFraming: {s['framing']}\nFirst frame: {s['first']}\nAction: {s['action']}\nLast frame: {s['last']}\n"+'\n'.join(s['dialogue'])+f"\nSpeaker cues: {s['voice']}\nNarrator attention: {s['attention']}\nNext cut: {s['transition']}\nGeneration length:6s; trim to actual voice timing5.2s after review.\nMotion: exact unchanged two-frame states at30fps, normal-speed action and1x speech.\n"
script=re.sub(r'SCENE 05 —.*\Z',lambda _:section,script,flags=re.S)
(OUT/'script.txt').write_text(script)

prompts=(OLD/'higgsfield-prompts.txt').read_text().replace('FIREPLACE REVISION','SCENE REPLACEMENTS')
prompts=prompts.replace('New images/clips only for01,02,05.','New clips planned for01,02,05. Reuse the unapproved01/02 candidate stills unchanged; generate a new05 campfire first/last pair.')
prompts=prompts.replace('Scene01 first establishes the new room; use it as continuity input for05.','Scene01 establishes an indoor fireplace. Scene05 is a different outdoor campsite and uses fresh first/last images, without the fireplace as a layout reference.')
prompts=prompts.replace('keyframes/05-first-reverse.png','keyframes/05-first.png').replace('keyframes/05-last-reverse.png','keyframes/05-last.png').replace('approved05-first-reverse.png and05-last-reverse.png','approved05-first.png and05-last.png')
prompts=prompts.replace('SCENE 05 — Back at the hearth, understanding the difference','SCENE 05 — Understanding beside a campfire after dark')
for kind,label,body in [('IMAGE','I05-FIRST',s['first_prompt']),('IMAGE','I05-LAST',s['last_prompt']),('VIDEO','V05',s['video_prompt'])]:
    prompts=re.sub(rf'BEGIN {kind} PROMPT {label}\n.*?END {kind} PROMPT {label}',lambda _:f'BEGIN {kind} PROMPT {label}\n{body}\nEND {kind} PROMPT {label}',prompts,flags=re.S)
(OUT/'higgsfield-prompts.txt').write_text(prompts)

plan=json.loads((OLD/'shot-plan.json').read_text())
plan['status']=state['status'];plan['historical_scope']=state['clarification'];plan['resolved_user_preferences'].pop('scene_variety',None)
plan['episode_revision_direction']=state['clarification']
c=next(c for c in plan['clips'] if c['id']=='05')
c.update(title=s['title'],action=s['action'],motion_prompt_action=s['action'],first_frame=s['first'],last_frame=s['last'],clean_first_frame=s['first'],clean_last_frame=s['last'],framing_prompt=s['framing'],setting_and_framing=s['room']+' '+s['framing'],image_prompts={'first':s['first_prompt'],'last':s['last_prompt']},video_prompt=s['video_prompt'],next_cut=s['transition'])
c['camera']={'shot_size':s['framing'],'movement':'Fixed source camera','editing':'No automatic push.'}
c['planned_outputs']={'first':'keyframes/05-first.png','last':'keyframes/05-last.png','video':'clips/05-scene.mp4'}
c['performance_beats']=[{'body':s['action'],'cue':s['voice'],'gaze':s['attention']}]
(OUT/'shot-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
assert prompts.count('BEGIN IMAGE PROMPT ')==10 and prompts.count('BEGIN VIDEO PROMPT ')==5
print('Prepared the episode-only revision with a new campfire ending; existing01/02 images copied unchanged.')
