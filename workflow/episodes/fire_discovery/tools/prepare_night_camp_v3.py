"""Prepare episode-specific lighting and ensemble candidates, preserving prior work."""
import json
import re
import shutil
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
OLD = EP / 'revisions/scene-replacements-v2'
OUT = EP / 'revisions/night-camp-v3'
if OUT.exists():
    raise FileExistsError(OUT)
for folder in ['keyframes', 'reviews']:
    (OUT / folder).mkdir(parents=True, exist_ok=True)
(OUT / 'audio').symlink_to('../../audio', target_is_directory=True)
for endpoint in ['first', 'last']:
    shutil.copy2(OLD / 'keyframes' / f'01-{endpoint}.png', OUT / 'keyframes' / f'01-{endpoint}.png')

state = json.loads((OLD / 'scene-plan.json').read_text())
identity = ('Each of the exactly three characters is the original Sol mascot: compact broad flame body, asymmetric tip, rounded side lobes, substantial red outer layer, orange layer and broad cream inner flame with its lobed crown and rounded lower face. Preserve the original two small close-spaced low-set opaque navy oval eyes, short rounded arms and tiny stubby feet. Keep all faces mouthless, the normal oval eye design unchanged, and the face attached to its coherent filled flame layers. All feet have solid ground contact. Sols emit no particles or detached flame pieces.')
style = ('Soft matte gouache brushwork, layered painted color, subtle paper texture and broad readable shapes across every subject, prop and surface. Define forms through light and color with softly painted edges, coherent perspective and contact shadows. No ink outlines, gloss, plastic rendering or photographic fire. No text, captions or watermark.')
cadence = ('Animate on twos at final 30 fps: each source pose or painted state stays unchanged for two consecutive frames, 15 updates per second, at normal speed; longer holds use complete pairs. Apply to every Sol, prop, real flame and animated local light. Background and paint texture stay stable. No interpolation, blending, optical flow or concealing blur. Enforce and verify exact source pairs during editing. No generated speech, music, sound effects, text or captions.')
s2 = state['scenes']['02']
s2.update(title='Natural fire in late-afternoon grassland',
    room='Uninhabited dry grassland in warm late-afternoon sunlight. Low sun from off-screen upper-left gives the straw-gold grasses and dusty ground warm honey light and long soft shadows to the right. Distant muted blue hills and peach-gold haze beneath a broad pale warm sky. This is a clear late-afternoon landscape; only the small branch fire gives localized orange light.',
    framing='Wide elevated three-quarter view across an open grassy basin. A fallen branch and small natural fire occupy x=56%, y=60%; distant layered blue hills lie below the upper third. Static camera, no zoom. Quiet light-colored lower fifth for captions.')
s2['action'] = s2['action'].replace('cloudy sky', 'late-afternoon sky')
s2['last'] = s2['last'].replace('cloud shapes', 'warm sky and sunlight')
s2['first_prompt'] = '\n\n'.join(['Create a vertical painted natural landscape in distinct warm late-afternoon light.', s2['room'], s2['framing'], s2['first'], style, 'No characters, people, campsite, structures or human-made objects.'])
s2['last_prompt'] = '\n\n'.join(['Use the supplied first image as the exact composition reference. Create its matching last still; retain the same late-afternoon lighting.', s2['last'], s2['room'], style])
s2['video_prompt'] = '\n\n'.join([s2['action'], 'Preserve exact endpoint framing, late-afternoon light, long soft shadows and static camera.', style, cadence])
s5 = state['scenes']['05']
s5.update(title='Three Sols at a cozy night campfire',
    room='A cozy campsite well after nightfall on an open ridge. Deep navy night sky, a small fixed painted crescent and a few subdued stars; distant dark blue hills, one small muted canvas tent at upper-right, packed mauve-gray earth. A low wood campfire casts a strong intimate amber pool of light around the group, with gentle cool blue moonlight on the outer silhouettes. Keep cream faces readable and navy eyes dark. Calm, warm, friendly atmosphere.',
    framing='Static medium-wide full-body view, camera slightly above the front Sols eye height and angled gently downward. Exactly three Sols gather around a small low campfire centered x=50%, wood base y=73%, flame top y=58%. Speaking Sol is foreground-right x=77%, feet y=77%, height about30%. Toasting friend is foreground-left x=21%, feet y=76%, height about30%. Warming friend is farther back x=49%, feet y=56%, height about23%, separated above the fire. Same world-size through perspective. Clear gaps keep every face and both feet readable. Tent small in the upper-right background; quiet lower fifth for editable captions.',
    first='The foreground-left Sol holds one slim wooden skewer in its tiny rounded arm, with one white marshmallow suspended just above the campfire. The rear Sol holds its short rounded arms low, ready to extend them toward the warmth. The foreground-right speaking Sol watches the toasting friend, both arms low. All three have supported stubby feet, shallow three-quarter orientations and both original dark oval eyes visible. The low faceless wood fire stays on three pieces of charred wood inside a simple stone ring.',
    last='Exactly the same three Sols, campsite, sizes, positions, foot contacts, fire, stones, wood, tent and night lighting. The foreground-left friend now holds the skewer slightly lifted, with its single lightly toasted marshmallow clear of the flame. The rear friend holds both short arms a little forward in a warming pose. The foreground-right speaking Sol holds both short arms slightly open in a low understanding gesture. All THREE compact bodies and their attached faces tilt gently backward/up together to look toward the fixed Narrator point just above camera, keeping original normal navy oval eyes and tiny limbs unchanged. All three remain firmly on the ground.',
    action='During local0.0–2.4s, the left friend gently rotates its one marshmallow skewer once over the fire, then lifts the marshmallow a little clear of the flame. The rear friend extends both short arms a small direct distance toward the warmth and settles. During its existing0.080–2.914s sentence, the right speaking Sol watches the toasting friend and opens its short arms once into a small low understanding gesture. Tiny attached body/tip follow-through; keep everyone grounded. During local3.0–3.6s, ALL THREE tilt their coherent bodies and attached faces gently upward toward the fixed Narrator point above camera. The skewer settles and stays still. All three maintain upward gaze and gentle listening idle throughout Arthur at4.0–4.9s, the edited ending5.2s, and the remaining source tail to6s. The campfire flickers softly while rooted on its wood; stable tent, stars, hills, ground and camera. No extra characters or speech.',
    attention='ALL THREE visible Sols must look above camera by local3.6s and maintain that gaze with gentle listening idle through Narrator4.0–4.9s and the ending. Only foreground-right Sol speaks; the two friends are silent.',
    transition='Hold all three upward listening poses through the complete Right release and existing music fade. Preserve the full5.2s picture ending.')
s5['first_prompt'] = '\n\n'.join(['Create one complete new vertical painted scene of EXACTLY THREE original Sol mascots sharing a cozy campfire at NIGHT.', s5['room'], s5['framing'], s5['first'], identity, style])
s5['last_prompt'] = '\n\n'.join(['Use the supplied night campsite first image as the exact continuity reference. Create the matching last still with the same THREE Sols.', s5['last'], 'Keep every fixed background object, wood piece, stone and camera position identical; preserve deep navy night and amber firelight.', identity, style])
s5['video_prompt'] = '\n\n'.join([s5['action'], s5['framing'], s5['room'], identity, style, cadence])
state.update(status='Night and ensemble revision: four new stills pending, all three scene pairs unapproved; no new clips.',
    selected_pairs={}, frame_approvals={}, preliminary_still_review={}, unselected_candidates={},
    superseded_revision='../scene-replacements-v2/',
    clarification='Episode-only request: vary lighting/time of day, include an unmistakably nighttime cozy campfire, add action and more Sols. Shared guidelines retain reusable art direction only.',
    lighting_sequence=['01 soft window daylight and fireplace warmth', '02 golden late-afternoon grassland', '03 existing cool lightning scene', '04 existing ember-tending scene', '05 deep-night amber campfire with three Sols'])
(OUT / 'scene-plan.json').write_text(json.dumps(state, indent=2)+'\n')

script=(OLD/'script.txt').read_text()
script=script.replace('HOW FIRE WAS DISCOVERED — SCENE REPLACEMENTS', 'HOW FIRE WAS DISCOVERED — NIGHT CAMP REVISION')
script=script.replace('Scene05 now uses a different outdoor campsite; the earlier second fireplace view is preserved only as an unused candidate.', 'Lighting now varies from daylight interior to golden late afternoon, existing cool storm light and a deep-night campfire. Scene05 has three Sols sharing a marshmallow-toasting action. Earlier candidates are preserved unused. The two friends remain silent; original dialogue and voices are unchanged.')
for sid in ['02','05']:
    s=state['scenes'][sid]
    times={'02':'2.333–7.133','05':'20.600–25.800'}[sid]
    section=f"SCENE {sid} — {s['title']} — edit{s['duration']:.3f}s ({times}s)\nSetting: {s['room']}\nFraming: {s['framing']}\nFirst frame: {s['first']}\nAction: {s['action']}\nLast frame: {s['last']}\n"+'\n'.join(s['dialogue'])+f"\nSpeaker cues: {s['voice']}\nNarrator attention: {s['attention']}\nNext cut: {s['transition']}\nGeneration length:{s['generation_duration']}s; trim to actual voice timing after review.\nMotion: exact unchanged two-frame states at30fps, normal-speed action and1x speech.\n\n"
    script=re.sub(rf'SCENE {sid} —.*?(?=SCENE \d\d —|\Z)',lambda _:section,script,flags=re.S)
(OUT/'script.txt').write_text(script)
prompts=(OLD/'higgsfield-prompts.txt').read_text().replace('HOW FIRE WAS DISCOVERED — SCENE REPLACEMENTS','HOW FIRE WAS DISCOVERED — NIGHT CAMP REVISION')
prompts=prompts.replace('Reuse the unapproved01/02 candidate stills unchanged; generate a new05 campfire first/last pair.', 'Reuse the unapproved01 pair unchanged. Generate new02 late-afternoon and05 three-Sol night-campfire first/last pairs.')
for sid in ['02','05']:
    s=state['scenes'][sid]
    prompts=re.sub(rf'SCENE {sid} — [^\n]+',f"SCENE {sid} — {s['title']} — generate{s['generation_duration']}s / edit{s['duration']:.3f}s",prompts)
    for kind,label,key in [('IMAGE',f'I{sid}-FIRST','first_prompt'),('IMAGE',f'I{sid}-LAST','last_prompt'),('VIDEO',f'V{sid}','video_prompt')]:
        prompts=re.sub(rf'BEGIN {kind} PROMPT {label}\n.*?END {kind} PROMPT {label}',lambda _:f"BEGIN {kind} PROMPT {label}\n{s[key]}\nEND {kind} PROMPT {label}",prompts,flags=re.S)
assert prompts.count('BEGIN IMAGE PROMPT ')==10 and prompts.count('BEGIN VIDEO PROMPT ')==5
(OUT/'higgsfield-prompts.txt').write_text(prompts)

plan=json.loads((OLD/'shot-plan.json').read_text())
plan['status']=state['status'];plan['episode_revision_direction']=state['clarification']
for c in plan['clips']:
    if c['id'] not in ['02','05']: continue
    sid=c['id'];s=state['scenes'][sid]
    c.update(title=s['title'],action=s['action'],motion_prompt_action=s['action'],first_frame=s['first'],last_frame=s['last'],clean_first_frame=s['first'],clean_last_frame=s['last'],framing_prompt=s['framing'],setting_and_framing=s['room']+' '+s['framing'],image_prompts={'first':s['first_prompt'],'last':s['last_prompt']},video_prompt=s['video_prompt'],next_cut=s['transition'],lighting=s['room'],narrator_attention=s['attention'])
    c['narrator_attention']={'required':sid=='05','gaze_target':'Fixed point just above camera' if sid=='05' else None,'coverage':s['attention'],'final_voice_alignment_verified':False}
    c['camera']={'shot_size':s['framing'],'movement':'Fixed source camera','editing':'No automatic push.'}
    c['planned_outputs']={'first':f'keyframes/{sid}-first.png','last':f'keyframes/{sid}-last.png','video':f'clips/{sid}-scene.mp4'}
    c['performance_beats']=[{'body':s['action'],'cue':s['voice'],'gaze':s['attention']}]
    for key in ['generated_stills','generated_video','first_frame_source','retry_reason','eye_gaze_squish_trial','body_up_tilt_trial','bounce_flame_accents']:
        c.pop(key,None)
    c['cast']=['Sol speaking foreground-right','Sol silent toasting friend foreground-left','Sol silent warming friend rear'] if sid=='05' else []
(OUT/'shot-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
refs=json.loads((OLD/'generation-inputs.json').read_text())['reference_inputs']
inputs={'scope':state['clarification'],'reference_inputs':refs,'new_requests':[], 'retained_pair':'01 copied byte-for-byte from scene-replacements-v2, still unapproved'}
for index,sid in [(1,'02'),(2,'05')]:
    if sid=='02':
        media=['61cb1925-cd4f-46c4-8f63-64d34b526296',refs[2]['media_id']]
        roles='Image1 is the earlier landscape layout reference; change its cool overcast light to warm late-afternoon sunlight. Image2 supplies painted finish only, without its characters or props.'
    else:
        media=[r['media_id'] for r in refs[:3]]
        roles='Image1 controls the original mascot design for ALL THREE Sols. Image2 controls short rounded arm anatomy only, without its microphone or cable. Image3 supplies gouache finish and the idea of a small group only; use the new night campsite, not its spring setting or props.'
    inputs['new_requests'].append({'index':index,'scene':sid,'endpoint':'first','params':{'model':'nano_banana_2_1','resolution':'2k','thinking_level':'medium','aspect_ratio':'9:16','count':1,'prompt':state['scenes'][sid]['first_prompt']+'\n\nReference roles: '+roles,'medias':[{'role':'image','value':m} for m in media]}})
(OUT/'generation-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
feedback=EP/'feedback.txt';text=feedback.read_text()
entry='''28. Elaine asks for more variation in lighting and time of day, including
    nighttime, a cozy campfire, more action and more Sols. This applies to the
    current fire episode and stays out of shared art-style guidelines.
    Implementation proposal: retain the daylight fireplace opening; relight
    the natural-fire grassland to warm late afternoon; keep the existing
    lightning and ember clips; end at a deep-night campfire with three Sols.
    One silent friend toasts a marshmallow, another warms its short arms,
    and the speaking Sol makes its understanding gesture. All three look UP
    before Narrator's Right and listen through the full release. Fresh02/05
    first/last frames require approval; no replacement clips authorized yet.

'''
text=text.replace('IMPLEMENTATION / REVIEW STATUS',entry+'IMPLEMENTATION / REVIEW STATUS')
feedback.write_text(text)
print('Prepared night-camp-v3;10 image prompts,5 video prompts;01 pair copied unchanged.')
