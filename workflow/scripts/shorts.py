#!/usr/bin/env python3
"""Prepare, generate, check and render Ignite Shorts from any working directory."""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from paths import WORKFLOW, episode_path, clip_path, voice_paths, cue_path, settings, ffmpeg_path


def write_new(path, text):
    """Never replace an existing episode edit or download."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open('x') as file:
            file.write(text)
        return True
    return False


def write_json_new(path, value):
    return write_new(path, json.dumps(value, indent=2)+'\n')


def shot_plan(episode, edit):
    mapping = [('A','hop'),('B','lean'),('C','graph'),('D','reaction')]
    frames = []
    for letter, key in mapping:
        cue = next(c for c in edit['cues'] if c['id'] == key)
        entry = {'frame': letter, 'cue': key, 'start': cue['start'], 'end': cue['end'],
                 'keyframe': f'keyframes/{letter}.png', 'blocking': f'keyframes/blocking/{letter}.png',
                 'narration': cue['text']}
        if key == 'graph':
            entry.update({'source':'analytic renderer', 'clip':None})
        else:
            entry.update({'source':'Flow', 'clip':'clips/'+edit['clips'][key]['file']})
        frames.append(entry)
    return {'episode':episode.name, 'sequence':['A','B','C','D'], 'frames':frames}


def prepare_calculus(episode, duration=None):
    if not episode.resolve().is_relative_to(WORKFLOW):
        raise ValueError('New Ignite episodes must live inside '+str(WORKFLOW))
    for directory in ('keyframes/blocking','clips','audio/generated','renders/previews','layers','plans'):
        (episode/directory).mkdir(parents=True, exist_ok=True)
    config = episode/'edit.json'
    if not config.exists():
        edit = json.loads((WORKFLOW/'templates/episode.json').read_text())
        seconds = duration if duration is not None else settings('format')['duration_sec']
        if seconds <= 0 or not math.isfinite(seconds):
            raise ValueError('Episode duration must be positive and finite')
        factor = seconds/edit['duration_sec']
        for cue in edit['cues']:
            cue['start']*=factor
            cue['end']*=factor
        edit['tangent_reveal_sec']*=factor
        edit['duration_sec']=seconds
        edit['narrator']={k:v for k,v in settings('narration').items() if k in ('provider','voice','role')}
        edit['voice_lufs']=settings('narration')['voice_lufs']
        edit['sfx_peak_dbfs']=settings('narration')['sfx_peak_dbfs']
        edit['captions']=settings('captions')['mode']
        write_json_new(config, edit)
    edit=json.loads(config.read_text())
    if duration is not None and edit['duration_sec'] != duration:
        raise ValueError(f'Existing edit preserved at {config}; change its duration and cues deliberately instead of overwriting it with --duration.')
    write_new(episode/'narration.txt','\n\n'.join(c['text'] for c in edit['cues'])+'\n')
    write_json_new(episode/'shot-plan.json', shot_plan(episode,edit))
    context={'EPISODE':episode.name,'SOL':str(WORKFLOW/'assets/sol-full-body.png'),
             'SCENE':str(WORKFLOW/'assets/calculus-painted-scene.jpg')}
    for letter,key in [('A','hop'),('B','lean'),('D','reaction')]:
        cue=next(c for c in edit['cues'] if c['id']==key)
        context[letter]=str(episode/f'keyframes/{letter}.png')
        context[f'CLIP_{letter}']=str(episode/'clips'/edit['clips'][key]['file'])
        context[f'{letter}_SECONDS']=str(math.ceil(cue['end']-cue['start']+.6))
    context['C']=str(episode/'keyframes/C.png')
    for name in ('flow-image','flow-video'):
        text=(WORKFLOW/'templates'/f'{name}.md').read_text()
        for key,value in context.items():
            text=text.replace('{{'+key+'}}',value)
        write_new(episode/f'{name}-prompts.md',text)
    write_json_new(episode/'audio/voiceover-cues.template.json',{
        'confirmed':False,'source_sha256':None,'cues':edit['cues'],
        'tangent_reveal_sec':edit['tangent_reveal_sec'],
        'note':'Replace placeholder boundaries with measured times from the Cub recording and use its SHA-256 hash.'})
    from calculus_edit import Art, validate
    validate(edit)
    art=Art(episode,edit,{'ready':False,'imported_voice':False,'label':'BLOCKING GUIDE'})
    (WORKFLOW/'.cache').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='prepare-', dir=WORKFLOW/'.cache') as temp:
        scratch=Path(temp);(scratch/'layers').mkdir()
        art.g.export(scratch)
        for source in (scratch/'layers').iterdir():
            target=episode/'layers'/source.name
            if not target.exists():shutil.move(source,target)
    for letter,key in [('A','hop'),('B','lean'),('C','graph'),('D','reaction')]:
        target=episode/f'keyframes/blocking/{letter}.png'
        cue=next(c for c in edit['cues'] if c['id']==key)
        if not target.exists():
            frame=art.stage(cue['start'],cue)
            if key=='graph':
                frame=art.overlays(frame,cue['start']+.3,cue,False,False)
            frame.save(target)
        if key=='graph' and not (episode/'keyframes/C.png').exists():
            shutil.copyfile(target,episode/'keyframes/C.png')
    return edit


def is_skit(episode):
    config=episode/'edit.json'
    if config.is_file():return 'shots' in json.loads(config.read_text())
    return episode.name != 'calculus_pilot'


def prepare(episode, duration=None):
    if is_skit(episode):
        from skit import prepare as prepare_skit
        return prepare_skit(episode,duration)
    return prepare_calculus(episode,duration)


def check(episode, images=False, probe=False, ffmpeg=None):
    if is_skit(episode):
        from skit import check as check_skit
        return check_skit(episode,images,probe)
    return check_calculus(episode,images,probe,ffmpeg)


def check_calculus(episode, images=False, probe=False, ffmpeg=None):
    report={'episode':str(episode),'missing':[],'errors':[],'warnings':[],'present':[]}
    config=episode/'edit.json'
    if not config.is_file():
        report['missing'].append({'kind':'EPISODE CONFIG','path':str(config)})
        return report
    edit=json.loads(config.read_text())
    for clip in edit['clips'].values():
        actual=clip_path(episode,clip['file'])
        if actual.is_file():report['present'].append(str(actual))
        else:report['missing'].append({'kind':'CLIP','path':str(episode/'clips'/clip['file'])})
    voices=voice_paths(episode)
    if not voices:
        report['missing'].append({'kind':'VOICEOVER','path':str(episode/'audio/mogofun-narration.mp3')})
    elif len(voices)>1:
        report['errors'].append('More than one voiceover exists: '+', '.join(map(str,voices)))
    else:report['present'].append(str(voices[0]))
    for name in ('sol-full-body.png','calculus-painted-scene.jpg'):
        path=WORKFLOW/'assets'/name
        if not path.is_file():report['missing'].append({'kind':'ARTWORK','path':str(path)})
    if images:
        for letter in ('A','B','D'):
            path=episode/f'keyframes/{letter}.png'
            if not path.is_file():report['missing'].append({'kind':'FLOW IMAGE','path':str(path)})
            else:report['present'].append(str(path))
    cue_file=cue_path(episode)
    confirmed=False
    if cue_file.is_file():
        cues=json.loads(cue_file.read_text())
        confirmed=cues.get('confirmed') is True
        if confirmed and len(voices)==1:
            if cues.get('source_sha256') != hashlib.sha256(voices[0].read_bytes()).hexdigest():
                report['errors'].append('Voice cue hash does not match recording: '+str(cue_file))
                confirmed=False
            else:
                from calculus_edit import validate
                resolved=copy.deepcopy(edit)
                resolved['cues']=cues['cues'];resolved['tangent_reveal_sec']=cues['tangent_reveal_sec']
                try:
                    validate(resolved)
                    edit=resolved
                except ValueError as error:report['errors'].append(f'{cue_file}: {error}');confirmed=False
    if not confirmed:report['warnings'].append('Exact voice timing is unconfirmed: '+str(episode/'audio/voiceover-cues.json'))
    report['final_ready']=not report['missing'] and not report['errors'] and confirmed
    if probe and not report['missing'] and not report['errors']:
        from calculus_edit import seconds
        binary=ffmpeg_path(ffmpeg)
        for key,clip in edit['clips'].items():
            cue=next(c for c in edit['cues'] if c['id']==key)
            needed=cue['end']-cue['start']-clip.get('hold_sec',0)
            available=seconds(binary,clip_path(episode,clip['file']))-clip.get('in_sec',0)
            if available+.04 < needed:report['errors'].append(f'CLIP TOO SHORT {clip_path(episode,clip["file"])}: {available:.2f}s available, {needed:.2f}s required')
        if len(voices)==1:
            length=seconds(binary,voices[0])
            if length > edit['duration_sec']+.05:report['errors'].append(f'VOICEOVER TOO LONG {voices[0]}: {length:.2f}s for {edit["duration_sec"]:.2f}s edit')
        report['final_ready']=report['final_ready'] and not report['errors']
    return report


def archive_outputs(episode):
    """Retain previous named exports instead of silently replacing them."""
    names=['final.mp4','animatic.mp4','picture-clean.mp4','picture-with-overlays.mp4',
           'picture-clean.log','picture-with-overlays.log','decode-check.log','validation.json',
           'storyboard.jpg','timeline.resolved.json','previews']
    paths=[episode/'renders'/name for name in names if (episode/'renders'/name).exists()]
    if not paths:return
    archive=episode/'renders/archive'/datetime.now(timezone.utc).strftime('run-%Y%m%dT%H%M%S%fZ')
    archive.mkdir(parents=True,exist_ok=False)
    for path in paths:shutil.move(path,archive/path.name)
    if (episode/'captions.srt').exists():shutil.copyfile(episode/'captions.srt',archive/'captions.srt')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for action in ('prepare','generate','check','render','sync-audio'):
        command=sub.add_parser(action)
        command.add_argument('episode',nargs='?',default='calculus_pilot',help='Episode name or full episode folder path')
        if action=='prepare':command.add_argument('--duration',type=float)
        if action=='generate':
            command.add_argument('--shot',choices=('A-B',),default='A-B',help='First live test: only the pilot A -> B shot')
            command.add_argument('--email',help='Flow account email (default: ignitefindyourfire@gmail.com)')
            command.add_argument('--dry-run',action='store_true',help='Check inputs/account/credits with GET requests only; no uploads or generation')
            command.add_argument('--ffprobe',help='FFprobe executable, also configurable with FFPROBE_PATH')
            command.add_argument('--poll-interval',type=float,default=10)
            command.add_argument('--wait-timeout',type=float,default=1200,help='Seconds to wait per job; rerun to resume')
        if action=='check':
            command.add_argument('--images',action='store_true')
            command.add_argument('--probe',action='store_true')
            command.add_argument('--json',action='store_true')
        if action in ('check','render'):command.add_argument('--ffmpeg')
        if action=='render':
            command.add_argument('--animatic',action='store_true',help='Allow marked placeholders and temporary speech')
            command.add_argument('--draft',action='store_true',help='Export actual skit media with provisional caption timing')
            command.add_argument('--captions',choices=('burn','soft','none'))
    args=parser.parse_args(argv)
    episode=episode_path(args.episode)
    try:
        if args.command=='generate':
            if is_skit(episode):
                raise ValueError('Codex generates skit frames, clips and voices through the connected Higgsfield tools using '+str(episode/'higgsfield-prompts.txt')+'. This Flow command is only for the preserved calculus A-B test.')
            from google_flow import generate
            generate(episode,args.shot,args.email,args.ffprobe,args.poll_interval,args.wait_timeout,dry_run=args.dry_run)
            return 0
        if args.command=='sync-audio':
            from skit import sync_audio
            print(json.dumps(sync_audio(episode),indent=2))
            return 0
        if args.command=='prepare':
            if not episode.exists() and not re.fullmatch(r'[A-Za-z0-9_-]+',Path(args.episode).name):
                raise ValueError('Use a simple episode name, e.g. calculus_pilot')
            prepare(episode,args.duration)
            print('PREPARED '+str(episode)+' (existing edits/downloads preserved)')
            return 0
        if args.command=='check':
            report=check(episode,args.images,args.probe,args.ffmpeg)
            if args.json:print(json.dumps(report,indent=2))
            else:
                for item in report['missing']:print(f'MISSING {item["kind"]}: {item["path"]}')
                for error in report['errors']:print('ERROR: '+error)
                for warning in report['warnings']:print('NOTE: '+warning)
                if not report['missing'] and not report['errors']:print('MEDIA PRESENT; '+('FINAL READY' if report['final_ready'] else 'VOICE TIMING PENDING'))
            return 1 if report['missing'] or report['errors'] else 0
        if is_skit(episode):
            if args.animatic:
                raise ValueError('Use Remotion Studio for a skit preview; generated clips and actual voices are required for export.')
            report=check(episode,probe=True)
            if report['missing'] or report['errors'] or (not args.draft and not report.get('final_ready')):
                raise ValueError('Final skit export blocked: '+json.dumps(report))
            command=['npm','--prefix',str(WORKFLOW/'remotion'),'run','render','--',str(episode/'edit.json')]
            if args.draft:command.append('--draft')
            return subprocess.run(command).returncode
        binary=ffmpeg_path(args.ffmpeg)
        if not args.animatic:
            report=check(episode,probe=True,ffmpeg=binary)
            if not report.get('final_ready'):
                for item in report['missing']:print(f'MISSING {item["kind"]}: {item["path"]}')
                for message in report['errors']+report['warnings']:print(message)
                raise ValueError('Final render needs all clips, actual Cub audio and confirmed cue timing. Use --animatic for an explicitly marked preview.')
        archive_outputs(episode)
        command=[sys.executable,str(WORKFLOW/'scripts/calculus_pilot.py'),'--project',str(episode),'--ffmpeg',binary]
        if not args.animatic:command.append('--require-final')
        if args.captions:command+=['--captions',args.captions]
        return subprocess.run(command).returncode
    except KeyboardInterrupt:
        print('\nInterrupted. Rerun the same command to resume a saved generation job.',file=sys.stderr)
        return 130
    except (ValueError,RuntimeError,OSError,KeyError,json.JSONDecodeError) as error:
        print('ERROR: '+str(error),file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
