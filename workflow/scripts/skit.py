"""Local preparation and validation for generated Higgsfield clips.

Codex submits the episode's reviewed prompts through the connected Higgsfield
tools. This module never submits paid jobs or synthesizes placeholder voices.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess

from paths import WORKFLOW


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open('x') as file:
            file.write(json.dumps(value, indent=2, ensure_ascii=False)+'\n' if not isinstance(value, str) else value)


def prepare(episode, duration=None):
    if not episode.resolve().is_relative_to(WORKFLOW/'episodes'):
        raise ValueError('New skits must live under '+str(WORKFLOW/'episodes'))
    for name in ('keyframes', 'clips', 'audio', 'renders', 'public', 'jobs/higgsfield'):
        (episode/name).mkdir(parents=True, exist_ok=True)
    for name in ('clips', 'audio'):
        link=episode/'public'/name
        if not link.exists() and not link.is_symlink():
            link.symlink_to(Path('..')/name, target_is_directory=True)
        elif link.resolve() != (episode/name).resolve():
            raise ValueError('Existing public media folder differs; preserved: '+str(link))
    plan_path=episode/'shot-plan.json'
    plan=json.loads(plan_path.read_text()) if plan_path.is_file() else None
    if not (episode/'edit.json').exists():
        if plan and plan.get('clips'):
            shots=[{'id':c['id'], 'label':'Scene '+c['id'],
                    'duration':c['end_sec']-c['start_sec'],
                    'scene':{'type':'video','src':'clips/'+c['id']+'-scene.mp4','fit':'contain','muted':True,'playbackRate':1}}
                   for c in plan['clips']]
        else:
            seconds=duration if duration is not None else 30
            if seconds <= 0 or not math.isfinite(seconds):
                raise ValueError('Episode duration must be positive and finite')
            if abs(seconds*30-round(seconds*30)) > 1e-6:
                raise ValueError('Duration must align to a 30 fps frame')
            shots=[{'id':'01','label':'Opening','duration':seconds,
                    'scene':{'type':'video','src':'clips/01-scene.mp4','fit':'contain','muted':True,'playbackRate':1}}]
        cast=json.loads((WORKFLOW/'config/voices.json').read_text())['speakers']
        edit={'id':episode.name.replace('_','-'), 'title':plan.get('title', 'New Ignite short') if plan else 'New Ignite short',
              'hook':plan.get('title', 'A question Sol can see') if plan else 'A question Sol can see',
              'format':{'width':1080,'height':1920,'fps':30}, 'layout':'fullscreen',
              'assets':{'paper':'art/ignite/painted-style-reference.jpg','font':'fonts/RammettoOne-Regular.ttf'},
              'palette':{'paper':'#FFF8F0','ink':'#1A1A2E','teal':'#4F9298','orange':'#F07B2A'},
              'captionStyle':{'fontSize':56,'fill':'#FFFFFF','outline':'#F07B2A','outlineWidth':6,
                              'leftPercent':10,'rightPercent':16,'topPercent':80},
              'shots':shots, 'captions':[], 'voiceover':None, 'audioTracks':[],
              'generation':json.loads((WORKFLOW/'config/generation.json').read_text()),
              'cast':cast, 'timing':{'confirmed':False,'note':'Record separate normal-rate takes, measure them, then review captions and cuts.'}}
        write_new(episode/'edit.json',edit)
    edit=json.loads((episode/'edit.json').read_text())
    if duration is not None and abs(sum(s['duration'] for s in edit['shots'])-duration)>1e-6:
        raise ValueError('Existing scene timing preserved; revise the episode plan and edit deliberately.')
    for source,target in [('calculus-painted-scene.jpg','art/ignite/painted-style-reference.jpg'),
                          ('fonts/RammettoOne-Regular.ttf','fonts/RammettoOne-Regular.ttf'),
                          ('fonts/RammettoOne-OFL.txt','fonts/RammettoOne-OFL.txt')]:
        src=WORKFLOW/'assets'/source; dst=episode/'public'/target
        dst.parent.mkdir(parents=True,exist_ok=True)
        if not dst.exists():
            with dst.open('xb') as out,src.open('rb') as inp:shutil.copyfileobj(inp,out)
        elif dst.read_bytes()!=src.read_bytes():
            print('Keeping differing artwork/font: '+str(dst))
    if plan:
        write_new(episode/'audio/voice-cues.plan.json', {
            'confirmed':False,'playback_rate':1,'status':'provisional; no actual takes available',
            'utterances':[{'scene':c['id'],'speaker':d['speaker'],'text':d['text'],
                           'source_audio':None,'source_sha256':None}
                          for c in plan['clips'] for d in c['dialogue']]})
    else:
        write_new(episode/'script.txt', 'DRAFT — write the complete Sol/Narrator skit and scene directions before generation.\n')
        write_new(episode/'higgsfield-prompts.txt','DRAFT — add one first-frame image prompt, one last-frame image prompt and one video prompt for every scene.\n')
    return edit


def probe(path):
    binary=os.environ.get('FFPROBE_PATH') or shutil.which('ffprobe')
    if not binary:raise RuntimeError('FFprobe not found; install FFmpeg or set FFPROBE_PATH.')
    result=subprocess.run([binary,'-v','error','-show_format','-show_streams','-of','json',str(path)],capture_output=True,text=True,timeout=30)
    if result.returncode:raise ValueError('Cannot read media '+str(path)+': '+result.stderr.strip())
    return json.loads(result.stdout)


def check(episode, images=False, inspect=False):
    edit_path=episode/'edit.json'
    report={'episode':str(episode),'missing':[],'errors':[],'warnings':[],'present':[],'final_ready':False}
    def need(path,kind):
        if path.is_file():report['present'].append(str(path));return True
        report['missing'].append({'kind':kind,'path':str(path)});return False
    if not need(edit_path,'EPISODE CONFIG'):return report
    edit=json.loads(edit_path.read_text()); total=sum(s['duration'] for s in edit['shots'])
    for shot in edit['shots']:
        if shot['scene']['type'] != 'video':
            report['errors'].append('Generated-clip skits require complete video shots: '+shot['id']);continue
        clip=episode/'public'/shot['scene']['src']
        if need(clip,'CLIP') and inspect:
            info=probe(clip)
            if not any(s['codec_type']=='video' for s in info['streams']):report['errors'].append('No video: '+str(clip))
            available=float(info['format']['duration'])-shot['scene'].get('trimBefore',0)
            if shot['scene'].get('playbackRate',1)!=1:report['errors'].append('Keep clip playback at 1x: '+shot['id'])
            if available+1/30<shot['duration']:report['errors'].append('CLIP TOO SHORT: '+str(clip))
    for name in edit['assets'].values():need(episode/'public'/name,'ARTWORK/FONT')
    tracks=edit.get('audioTracks',[])
    if not tracks:report['missing'].append({'kind':'SEPARATE VOICE TAKES','path':str(episode/'audio')})
    for track in tracks:
        path=episode/'public'/track['src']
        if not need(path,'VOICE TAKE'):continue
        if track.get('source_sha256')!=hashlib.sha256(path.read_bytes()).hexdigest():
            report['errors'].append('Voice take hash missing or changed: '+str(path))
        if track.get('playbackRate',1)!=1:report['errors'].append('Keep speech at 1x: '+str(path))
        if inspect:
            info=probe(path)
            if not any(s['codec_type']=='audio' for s in info['streams']):report['errors'].append('No audio: '+str(path))
            available=float(info['format']['duration'])-track.get('trimBefore',0)
            if available+1/30<track.get('duration',available):report['errors'].append('VOICE TAKE TOO SHORT: '+str(path))
    if images:
        for shot in edit['shots']:
            for frame in ('first','last'):need(episode/'keyframes'/f'{shot["id"]}-{frame}.png','KEYFRAME')
    confirmed=edit.get('timing',{}).get('confirmed') is True
    if not confirmed:report['warnings'].append('Voice/caption timing is provisional; final export is blocked.')
    if any(c['end']>total for c in edit['captions']):report['errors'].append('Caption extends past episode')
    from clip_review import edit_gate
    review=edit_gate(episode,edit)
    report['review']=review
    if not review['approved']:
        report['warnings'].extend('REVIEW BLOCKED '+c['scene']+': '+c['reason'] for c in review['scenes'] if not c['approved'])
    report['final_ready']=not report['missing'] and not report['errors'] and confirmed and review['approved']
    return report


def sync_audio(episode):
    """Measure individual takes at 1x and prepare explicitly provisional cues."""
    plan=json.loads((episode/'shot-plan.json').read_text()); edit=json.loads((episode/'edit.json').read_text())
    tracks=[];captions=[];measured=[];cursor=0
    for clip,shot in zip(plan['clips'],edit['shots'],strict=True):
        local=0.12
        for i,d in enumerate(clip['dialogue']):
            stem=f'{clip["id"]}-{i+1:02d}-{d["speaker"].lower()}'
            candidates=([episode/d['source_audio']] if d.get('source_audio') else
                        [p for ext in ('wav','mp3','m4a') if (p:=episode/'audio'/f'{stem}.{ext}').is_file()])
            candidates=[p for p in candidates if p.is_file()]
            if len(candidates)!=1:raise ValueError('Need exactly one recorded take for '+stem)
            path=candidates[0];length=float(probe(path)['format']['duration']); start=cursor+local
            track={'id':stem,'speaker':d['speaker'],'src':'audio/'+path.name,'start':round(start,6),
                   'duration':length,'trimBefore':0,'volume':1,'playbackRate':1,
                   'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
            tracks.append(track)
            words=d['text'].split();chunks=[words[j:j+6] for j in range(0,len(words),6)];offset=0
            for chunk in chunks:
                end=offset+length*len(chunk)/len(words)
                captions.append({'start':round(start+offset,6),'end':round(start+end,6),'text':' '.join(chunk)})
                offset=end
            measured.append({'scene':clip['id'],'speaker':d['speaker'],'text':d['text'],
                             'source_audio':str(path.relative_to(episode)),'source_sha256':track['source_sha256'],
                             'measured_start_sec':start,'measured_end_sec':start+length})
            local+=length+0.16
        # Preserve planned visual actions/holds, and extend when natural speech needs it.
        # The current video model accepts whole-second lengths; retain the complete
        # first-to-last clip and give the natural takes the remaining hold.
        shot['duration']=math.ceil(max(shot['duration'],local+clip.get('tail_hold_sec',0.4)))
        cursor+=shot['duration']
    edit['audioTracks']=tracks;edit['captions']=captions
    edit['timing']={'confirmed':False,'note':'Audio durations measured at 1x. Caption phrase times are estimates; review against the actual speech before setting confirmed.'}
    (episode/'edit.json').write_text(json.dumps(edit,indent=2,ensure_ascii=False)+'\n')
    (episode/'audio/voice-cues.measured.json').write_text(json.dumps({'confirmed':False,'utterances':measured,'caption_timing':'estimated phrase boundaries; review needed'},indent=2,ensure_ascii=False)+'\n')
    return {'duration_sec':cursor,'takes':len(tracks),'timing_confirmed':False}
