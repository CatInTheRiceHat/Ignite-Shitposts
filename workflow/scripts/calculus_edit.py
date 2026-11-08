"""Imported-media calculus edit and clearly labeled, Blender-free animatic."""
import argparse
import hashlib
import html
import json
import math
import mmap
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
import wave

from PIL import Image, ImageDraw
from paths import WORKFLOW, episode_path, clip_path, voice_paths, cue_path, ffmpeg_path, settings
CAPTIONS = settings("captions")
from calculus_pilot import Art as ExistingArt, REPO, WIDTH as W, HEIGHT as H, FPS, PAPER, INK, ORANGE, TEAL

DEFAULT = {
    'duration_sec': 15.0, 'captions': 'burn',
    'narrator': {'provider': 'MoGoFun', 'voice': 'Cub (Female)', 'role': 'off-screen'},
    'cues': [
        {'id': 'hop', 'start': 0.0, 'end': 3.6, 'text': 'Sol brought confidence. Not brakes.'},
        {'id': 'lean', 'start': 3.6, 'end': 7.5, 'text': 'How steep is this curve right here?'},
        {'id': 'graph', 'start': 7.5, 'end': 11.8, 'text': 'Tangent line. Its slope is the derivative.'},
        {'id': 'reaction', 'start': 11.8, 'end': 15.0, 'text': 'Tiny arms. Massive responsibility.'}],
    'tangent_reveal_sec': 7.5, 'tangent_draw_sec': 0.2,
    'graph': {'function': 'sqrt', 'point_x': 1.0, 'x_max': 2.35,
              'point_px': [360, 760], 'x_scale': 240, 'y_scale': 224},
    'clips': {'hop': {'file': '01-hop-on.mp4', 'in_sec': 0.0, 'hold_sec': 0.25},
              'lean': {'file': '02-low-side-lean.mp4', 'in_sec': 0.0, 'hold_sec': 0.3},
              'reaction': {'file': '03-reaction.mp4', 'in_sec': 0.0, 'hold_sec': 0.4}},
    'voice_lufs': -16, 'sfx_peak_dbfs': -30}


def run(command):
    result = subprocess.run([str(x) for x in command], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-5000:] or result.stdout[-5000:])
    return result


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')


def ease(x):
    x = max(0, min(1, x))
    return x*x*(3-2*x)


def seconds(ffmpeg, path):
    result = subprocess.run([ffmpeg, '-hide_banner', '-i', str(path)], capture_output=True, text=True)
    match = re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)', result.stderr)
    if not match:
        raise ValueError(f'Cannot probe media: {path}\n{result.stderr[-1000:]}')
    h, m, s = map(float, match.groups())
    return h*3600+m*60+s


def wav_duration(path):
    with wave.open(str(path)) as file:
        return file.getnframes()/file.getframerate()


def validate(edit):
    if edit['duration_sec'] <= 0 or not math.isfinite(edit['duration_sec']):
        raise ValueError('duration_sec must be positive and finite')
    if [c['id'] for c in edit['cues']] != ['hop', 'lean', 'graph', 'reaction']:
        raise ValueError('Cue ids must be hop, lean, graph, reaction, in that order')
    last = 0
    for cue in edit['cues']:
        if not all(math.isfinite(cue[k]) for k in ('start','end')) or abs(cue['start']-last) > .001 or cue['end'] <= cue['start']:
            raise ValueError(f'Cues must be finite, contiguous and increasing: {cue}')
        last = cue['end']
    if abs(last-edit['duration_sec']) > .001:
        raise ValueError('The last cue must end at duration_sec')
    graph_cue = edit['cues'][2]
    if not graph_cue['start'] <= edit['tangent_reveal_sec'] < graph_cue['end'] or edit['tangent_draw_sec'] <= 0:
        raise ValueError('Tangent reveal must occur inside the graph cue, with positive draw duration')
    g = edit['graph']
    if g['function'] not in ('sqrt','square') or not 0 < g['point_x'] < g['x_max'] or min(g['x_scale'], g['y_scale']) <= 0:
        raise ValueError('Invalid graph function, domain, point or scale')


class Graph:
    def __init__(self, config):
        self.c = config
        self.x = config['point_x']
        self.y = self.f(self.x)
        self.px, self.py = config['point_px']
        self.slope = .5/math.sqrt(self.x) if config['function'] == 'sqrt' else 2*self.x

    def f(self, x):
        return math.sqrt(x) if self.c['function'] == 'sqrt' else x*x

    def point(self, x, y):
        return self.px+(x-self.x)*self.c['x_scale'], self.py-(y-self.y)*self.c['y_scale']

    def curve(self):
        return [self.point(x, self.f(x)) for x in [self.c['x_max']*i/700 for i in range(701)]]

    def tangent(self):
        return [self.point(x, self.y+self.slope*(x-self.x)) for x in (0, self.c['x_max'])]

    @property
    def angle(self):
        return math.degrees(math.atan(self.slope*self.c['y_scale']/self.c['x_scale']))

    @property
    def formula(self):
        return 'y = sqrt(x)' if self.c['function'] == 'sqrt' else 'y = x²'

    @property
    def label(self):
        value = '1/2' if abs(self.slope-.5)<1e-9 else f'{self.slope:g}'
        return f"f'({self.x:g}) = {value}"

    def export(self, project):
        points = ' '.join(f'{x:.3f},{y:.3f}' for x,y in self.curve())
        ox,oy = self.point(0,0)
        header = '<svg xmlns="http://www.w3.org/2000/svg" width="720" height="1280" viewBox="0 0 720 1280">'
        graph = f'''<title>Editable analytic graph; coordinates derive from edit.json</title>
<path id="axes" d="M {ox} 420 V {oy} H 680" fill="none" stroke="#C9C4BB" stroke-width="3"/>
<polyline id="curve" points="{points}" fill="none" stroke="{TEAL}" stroke-width="8"/>
<circle id="point-P" cx="{self.px}" cy="{self.py}" r="10" fill="{INK}"/>
<text x="72" y="370" font-family="sans-serif" font-size="32" fill="{TEAL}">{html.escape(self.formula)}</text>
<text x="{self.px-60}" y="{self.py+52}" font-family="sans-serif" font-size="26" fill="{INK}">P = ({self.x:g}, {self.y:g})</text>'''
        a,b = self.tangent()
        tangent = f'''<title>Editable tangent, slope {self.slope:g}</title>
<line id="tangent" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{ORANGE}" stroke-width="6"/>
<text x="72" y="430" font-family="sans-serif" font-size="36" fill="{INK}">{html.escape(self.label)}</text>'''
        (project/'layers/graph.svg').write_text(header+graph+'</svg>')
        (project/'layers/tangent.svg').write_text(header+tangent+'</svg>')


class Art(ExistingArt):
    def __init__(self, project, edit, status):
        super().__init__(project)
        self.edit, self.status, self.g = edit, status, Graph(edit['graph'])
        # Video camera crop of the scene's clear right side, avoiding a second Sol.
        self.paint = self.scene.crop((round(self.scene.width*.70),0,self.scene.width,self.scene.height)).resize((W,H),Image.Resampling.LANCZOS)
        self.paint = Image.blend(self.paint,Image.new('RGB',(W,H),PAPER),.40)
        self.sprites = {}

    def puppet(self, frame, anchor, height, angle=0, arm=False):
        key = height,round(angle)
        if key not in self.sprites:
            sprite = self.sol.resize((round(height*self.sol.width/self.sol.height),height),Image.Resampling.LANCZOS)
            self.sprites[key] = sprite.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        sprite = self.sprites[key]
        x,y = anchor
        if arm:
            ImageDraw.Draw(frame).ellipse((x+height*.35,y-height*.35,x+height*.35+42,y-height*.35+20),fill='#D86525')
        frame.paste(sprite,(round(x-sprite.width/2),round(y-sprite.height)),sprite)

    def ribbon(self, draw, points, width):
        # A filled outline avoids the gaps produced by very thick short line segments.
        upper,lower=[],[]
        for i,(x,y) in enumerate(points):
            a=points[max(0,i-1)];b=points[min(len(points)-1,i+1)]
            dx,dy=b[0]-a[0],b[1]-a[1]
            length=math.hypot(dx,dy) or 1
            nx,ny=-dy/length*width/2,dx/length*width/2
            upper.append((x+nx,y+ny));lower.append((x-nx,y-ny))
        draw.polygon(upper+lower[::-1],fill='#73A9A9')

    def board(self, frame, center, width, angle, perspective=False):
        bh = round(width*.09)
        layer = Image.new('RGBA',(width+32,bh+38))
        d = ImageDraw.Draw(layer)
        if perspective:
            d.polygon([(8,bh//2),(width-8,2),(width+12,bh//2),(32,bh+8)],fill='#D5912F')
            d.line([(20,bh//2),(width-8,6)],fill='#F5C160',width=5)
        else:
            d.rounded_rectangle((7,2,width+5,bh),radius=bh//2,fill='#D5912F')
            d.line((25,9,width-12,9),fill='#F5C160',width=5)
        layer = layer.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        frame.paste(layer,(round(center[0]-layer.width/2),round(center[1]-layer.height/2)),layer)

    def stage(self, t, cue):
        frame = self.paint.copy()
        d = ImageDraw.Draw(frame)
        u = max(0,min(1,(t-cue['start'])/(cue['end']-cue['start'])))
        stepped = math.floor(u*12)/12
        if cue['id'] == 'hop':
            self.ribbon(d,self.g.curve(),72)
            bx=310+110*ease(min(1,u/.7))
            x=self.g.x+(bx-self.g.px)/self.g.c['x_scale']
            by=self.g.point(x,self.g.f(x))[1]+20
            self.board(frame,(bx,by),450,self.g.angle)
            jump = math.sin(min(1,stepped/.4)*math.pi)*190
            self.puppet(frame,(155+(bx-155)*ease(min(1,stepped/.4)),by-20-jump),300,[-8,5,0][min(2,int(u*7))])
            self.text(d,(48,210),'Confidence: 100%',37,family='Poppins-SemiBold.ttf')
            if u>.28:self.text(d,(48,264),'Brakes: 0%',37,ORANGE,family='Poppins-SemiBold.ttf')
        elif cue['id'] == 'lean':
            self.ribbon(d,self.g.curve(),120)
            tilt = 18 if u<.25 else 29 if u<.72 else self.g.angle
            self.board(frame,(360,775),610,tilt,True)
            self.puppet(frame,(360,760),410,-12 if u<.24 else -21 if u<.74 else -16,arm=u>.25)
            self.text(d,(48,214),'Right. Here.',40,family='RammettoOne-Regular.ttf')
            if u>.72:d.ellipse((350,750,370,770),fill=INK)
        elif cue['id'] == 'graph':
            frame = Image.new('RGB',(W,H),PAPER)
        else:
            self.board(frame,(360,805),420,self.g.angle)
            self.puppet(frame,(360,780),460,0 if u<.18 else -7 if u<.36 else 4,arm=True)
            self.text(d,(360,252),'A lot of responsibility.',31,anchor='mm',family='Poppins-SemiBold.ttf')
        return frame

    def overlays(self, frame, t, cue, captions=True, labels=True):
        d = ImageDraw.Draw(frame)
        if cue['id']=='graph':
            g = self.g
            ox,oy = g.point(0,0)
            for x in (0,1,2):
                px,_ = g.point(x,0)
                d.line((px,470,px,oy),fill='#E9E2D7',width=2)
                self.text(d,(px,oy+15),str(x),23,'#72707A',anchor='ma')
            for y in (0,.5,1,1.5,2):
                _,py = g.point(0,y)
                d.line((ox,py,675,py),fill='#E9E2D7',width=2)
            d.line((ox,450,ox,oy,675,oy),fill='#C9C4BB',width=3)
            d.line(g.curve(),fill=TEAL,width=8,joint='curve')
            self.text(d,(48,206),'The slope, right here.',37,family='RammettoOne-Regular.ttf')
            self.text(d,(72,344),g.formula,32,TEAL,family='Poppins-SemiBold.ttf')
            reveal = ease((t-self.edit['tangent_reveal_sec'])/self.edit['tangent_draw_sec'])
            if reveal>0:
                a,b = g.tangent()
                p = g.px,g.py
                line = [(p[0]+(q[0]-p[0])*reveal,p[1]+(q[1]-p[1])*reveal) for q in (a,b)]
                d.line(line,fill=ORANGE,width=6)
                self.text(d,(72,400),g.label,36,family='Poppins-SemiBold.ttf')
                self.text(d,(540,650),'tangent',25,ORANGE,anchor='mm')
            d.ellipse((g.px-11,g.py-11,g.px+11,g.py+11),fill=INK,outline='#FFFFFF',width=3)
            self.text(d,(g.px-35,g.py+26),f'P = ({g.x:g}, {g.y:g})',25)
        if labels:
            d.rounded_rectangle((28,35,692,93),radius=16,fill=INK)
            label = 'IGNITE / CALCULUS' if self.status['ready'] else 'ANIMATIC / '+self.status['label']
            self.text(d,(360,64),label,17,'#FFFFFF',anchor='mm',family='Poppins-SemiBold.ttf')
            if not self.status['imported_voice']:
                self.text(d,(360,119),'TEMP VOICE / CUB (FEMALE) DOWNLOAD PENDING',15,'#7C6B5F',anchor='mm')
        if captions:
            lines=[];line=''
            for word in cue['text'].split():
                candidate=(line+' '+word).strip()
                if d.textlength(candidate,font=self.font(CAPTIONS['font'],CAPTIONS['size']))>CAPTIONS['max_text_width']:
                    lines.append(line);line=word
                else:line=candidate
            lines.append(line)
            d.rounded_rectangle(CAPTIONS['box'],radius=24,fill=CAPTIONS['background'])
            self.text(d,tuple(CAPTIONS['anchor']),'\n'.join(lines),CAPTIONS['size'],CAPTIONS['color'],family=CAPTIONS['font'],anchor='mm',align='center',spacing=8)
        return frame


def prepare_voice(project, edit, ffmpeg, temp_voice):
    found = voice_paths(project)
    if len(found)>1:raise ValueError('Keep just one mogofun-narration.mp3/.wav/.m4a in audio/')
    source = found[0] if found else None
    raw = project/'audio/generated/voice-raw.wav'
    confirmed = False
    if source:
        run([ffmpeg,'-y','-v','error','-i',source,'-vn','-ar','48000','-ac','1',raw])
        duration = wav_duration(raw)
        if duration>edit['duration_sec']+.02:
            raise ValueError(f'Voiceover is {duration:.2f}s, longer than this {edit["duration_sec"]:.2f}s edit. Re-export a shorter read or edit duration_sec/cues; narration is never silently cut or accelerated.')
        cue_file = cue_path(project)
        if cue_file.is_file():
            cues = json.loads(cue_file.read_text())
            if cues.get('confirmed') is True:
                if cues.get('source_sha256') != hashlib.sha256(source.read_bytes()).hexdigest():
                    raise ValueError('Confirmed voice cues do not match this audio file. Re-time the new recording and update source_sha256.')
                edit['cues'] = cues['cues']; edit['tangent_reveal_sec'] = cues['tangent_reveal_sec']; confirmed = True
        if not confirmed:
            factor = min(1,duration/edit['duration_sec'])
            for cue in edit['cues']:
                cue['start']*=factor;cue['end']*=factor
            edit['tangent_reveal_sec']*=factor;edit['cues'][-1]['end']=edit['duration_sec']
            save(project/'audio/voiceover-cues.suggested.json',{'confirmed':False,
                'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                'note':'Estimated only. Listen, set cut/caption boundaries and the onset of Tangent, then save voiceover-cues.json with confirmed=true.',
                'cues':edit['cues'],'tangent_reveal_sec':edit['tangent_reveal_sec']})
    else:
        if not shutil.which('say'):raise ValueError('Add audio/mogofun-narration.mp3; temporary macOS voice is unavailable')
        pieces=[]
        for cue in edit['cues']:
            aiff=project/f'audio/generated/{cue["id"]}-temp.aiff';wav=project/f'audio/generated/{cue["id"]}-temp.wav';fitted=project/f'audio/generated/{cue["id"]}-fitted.wav'
            run(['say','-v',temp_voice,'-r','165','-o',aiff,cue['text']])
            run([ffmpeg,'-y','-v','error','-i',aiff,'-ar','48000','-ac','1',wav])
            slot=cue['end']-cue['start'];speed=max(1,wav_duration(wav)/(slot-.25))
            run([ffmpeg,'-y','-v','error','-i',wav,'-af',f'atempo={speed:.6f},apad','-t',str(slot),fitted])
            with wave.open(str(fitted)) as file:pieces.append(file.readframes(file.getnframes()))
        with wave.open(str(raw),'wb') as file:
            file.setnchannels(1);file.setsampwidth(2);file.setframerate(48000);file.writeframes(b''.join(pieces))
        duration=wav_duration(raw)
    validate(edit)
    run([ffmpeg,'-y','-v','error','-i',raw,'-af',f'loudnorm=I={edit["voice_lufs"]}:TP=-2:LRA=7,apad','-t',str(edit['duration_sec']),'-ar','48000','-ac','1',project/'audio/generated/narration.wav'])
    return source,confirmed,duration


def sound(project,edit,ffmpeg):
    rate=48000; samples=[0.0]*round(edit['duration_sec']*rate);amplitude=10**(edit['sfx_peak_dbfs']/20)
    lean=edit['cues'][1]
    for start,duration,f0,f1 in [(.95,.09,170,60),(lean['start']+.34*(lean['end']-lean['start']),.14,880,420)]:
        phase=0
        for i in range(round(duration*rate)):
            at=round(start*rate)+i
            if at>=len(samples):continue
            u=i/(duration*rate);phase+=2*math.pi*(f0+(f1-f0)*u)/rate
            samples[at]+=amplitude*math.sin(phase)*math.sin(math.pi*u)**2
    with wave.open(str(project/'audio/generated/sfx.wav'),'wb') as file:
        file.setnchannels(1);file.setsampwidth(2);file.setframerate(rate)
        file.writeframes(b''.join(struct.pack('<h',max(-32768,min(32767,round(s*32767)))) for s in samples))
    run([ffmpeg,'-y','-v','error','-i',project/'audio/generated/narration.wav','-i',project/'audio/generated/sfx.wav',
         '-filter_complex','[0:a][1:a]amix=inputs=2:normalize=0,alimiter=limit=0.891:level=false[a]',
         '-map','[a]','-t',str(edit['duration_sec']),project/'audio/generated/mix.wav'])


class Clip:
    def __init__(self,ffmpeg,path,settings,slot,cache):
        duration=seconds(ffmpeg,path);start=settings['in_sec'];hold=settings['hold_sec'];live=slot-hold
        if start<0 or hold<0 or live<=0 or duration-start<live-.04:
            raise ValueError(f'{path.name}: need {live:.2f}s usable video after in_sec={start}; have {duration-start:.2f}s')
        raw=cache/(path.stem+'.rgb')
        vf=f'trim=duration={live},setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,tpad=stop_mode=clone:stop_duration={hold+.08},trim=duration={slot}'
        run([ffmpeg,'-y','-v','error','-ss',str(start),'-i',path,'-vf',vf,'-an','-pix_fmt','rgb24','-f','rawvideo',raw])
        self.file=raw.open('rb');self.data=mmap.mmap(self.file.fileno(),0,access=mmap.ACCESS_READ);self.frames=len(self.data)//(W*H*3)
        if not self.frames:raise ValueError(f'No decoded frames: {path}')

    def frame(self,n):
        n=max(0,min(self.frames-1,n));size=W*H*3
        return Image.frombytes('RGB',(W,H),self.data[n*size:(n+1)*size])

    def close(self):self.data.close();self.file.close()


def stamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,default=WORKFLOW/'episodes/calculus_pilot')
    parser.add_argument('--ffmpeg',default=os.environ.get('FFMPEG_PATH') or shutil.which('ffmpeg'))
    parser.add_argument('--temp-voice',default=settings('narration')['temporary_voice'],help='Animatic only; never labeled as Cub')
    parser.add_argument('--captions',choices=('burn','soft','none'))
    parser.add_argument('--require-final',action='store_true')
    args=parser.parse_args()
    args.ffmpeg=ffmpeg_path(args.ffmpeg)
    p=episode_path(args.project)
    for folder in ('clips','layers','keyframes/blocking','renders/previews','audio/generated','.cache'):(p/folder).mkdir(parents=True,exist_ok=True)
    if not (p/'edit.json').exists():save(p/'edit.json',DEFAULT)
    edit=json.loads((p/'edit.json').read_text())
    if args.captions:edit['captions']=args.captions
    validate(edit)
    if args.require_final:
        expected=[clip_path(p,c['file']) for c in edit['clips'].values()]
        voices=voice_paths(p)
        cue_file=cue_path(p)
        if any(not path.is_file() for path in expected) or not any(path.is_file() for path in voices) or not cue_file.is_file():
            parser.error('Final export needs all three clips, the MoGoFun download and audio/voiceover-cues.json. See MEDIA.md.')
    imported,confirmed,vo_duration=prepare_voice(p,edit,args.ffmpeg,args.temp_voice)
    missing=[c['file'] for c in edit['clips'].values() if not (clip_path(p,c['file'])).is_file()]
    ready=not missing and imported is not None and confirmed
    reasons=[]
    if missing:reasons.append('MOTION PENDING')
    if imported is None:reasons.append('TEMP VOICE')
    elif not confirmed:reasons.append('VOICE CUES UNCONFIRMED')
    status={'ready':ready,'imported_voice':imported is not None,'label':' / '.join(reasons)}
    if args.require_final and not ready:raise ValueError('Final export blocked: '+status['label'])
    art=Art(p,edit,status);art.g.export(p);sound(p,edit,args.ffmpeg)
    save(p/'renders/timeline.resolved.json',edit)
    if not (p/'narration.txt').exists():
        (p/'narration.txt').write_text('\n\n'.join(c['text'] for c in edit['cues'])+'\n')
    (p/'captions.srt').write_text('\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}\n' for i,c in enumerate(edit['cues'])))
    for i,key in enumerate(('hop','lean','reaction'),1):
        cue=next(c for c in edit['cues'] if c['id']==key)
        art.stage(cue['start'],cue).save(p/f'keyframes/blocking/{i:02d}-{key}-start.png')
    gc=edit['cues'][2]
    art.overlays(art.stage(gc['start'],gc),gc['start']+.3,gc,False,False).save(p/'keyframes/blocking/match-cut-target.png')
    processes=[];logs=[];clips={};frames=round(edit['duration_sec']*FPS)
    with tempfile.TemporaryDirectory(prefix='frames-',dir=p/'.cache') as temp:
        try:
            for key,settings in edit['clips'].items():
                path=clip_path(p,settings['file']);cue=next(c for c in edit['cues'] if c['id']==key)
                if path.is_file():clips[key]=Clip(args.ffmpeg,path,settings,cue['end']-cue['start'],Path(temp))
            for name in ('picture-clean','picture-with-overlays'):
                log=(p/'renders'/(name+'.log')).open('w');logs.append(log)
                command=[args.ffmpeg,'-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(p/'renders'/(name+'.mp4'))]
                processes.append(subprocess.Popen(command,stdin=subprocess.PIPE,stderr=log))
            shots=[.6,2.2,edit['cues'][1]['start']+1.5,gc['start']+.5,edit['cues'][3]['start']+.8]
            snapshots={min(frames-1,round(t*FPS)):i+1 for i,t in enumerate(shots)}
            for n in range(frames):
                t=n/FPS;cue=next((c for c in edit['cues'] if t<c['end']),edit['cues'][-1])
                frame=clips[cue['id']].frame(round((t-cue['start'])*FPS)) if cue['id'] in clips else art.stage(t,cue)
                processes[0].stdin.write(frame.tobytes())
                composite=art.overlays(frame.copy(),t,cue,edit['captions']=='burn')
                processes[1].stdin.write(composite.tobytes())
                if n in snapshots:composite.save(p/f'renders/previews/beat_{snapshots[n]}.png')
                if n%90==0:print(f'Rendering {n}/{frames}: {cue["id"]}',flush=True)
        finally:
            for process in processes:process.stdin.close()
            errors=[process.wait() for process in processes]
            for log in logs:log.close()
            for clip in clips.values():clip.close()
            if any(errors):raise RuntimeError('Encoding failed; see picture-*.log')
    output=p/'renders'/('final.mp4' if ready else 'animatic.mp4')
    cmd=[args.ffmpeg,'-y','-v','error','-i',p/'renders/picture-with-overlays.mp4','-i',p/'audio/generated/mix.wav']
    if edit['captions']=='soft':cmd+=['-i',p/'captions.srt']
    cmd+=['-map','0:v:0','-map','1:a:0']
    if edit['captions']=='soft':cmd+=['-map','2:0','-c:s','mov_text','-metadata:s:s:0','language=eng']
    cmd+=['-c:v','copy','-c:a','aac','-b:a','160k','-t',str(edit['duration_sec']),'-movflags','+faststart',output]
    run(cmd)
    decoded=run([args.ffmpeg,'-hide_banner','-i',output,'-f','null','-']);(p/'renders/decode-check.log').write_text(decoded.stderr)
    board=Image.new('RGB',(W*5//2,H//2),PAPER)
    for i in range(5):board.paste(Image.open(p/f'renders/previews/beat_{i+1}.png').resize((W//2,H//2),Image.Resampling.LANCZOS),(i*W//2,0))
    board.save(p/'renders/storyboard.jpg',quality=93)
    report={'output':str(output),'status':'final' if ready else 'animatic','duration_sec':seconds(args.ffmpeg,output),
            'frames':frames,'canvas':[W,H],'fps':FPS,'decode':'passed','missing_clips':missing,
            'requested_voice':'MoGoFun Cub (Female), off-screen','voice_source':str(imported) if imported else 'temporary local '+args.temp_voice,
            'voice_duration_sec':vo_duration,'voice_cues_confirmed':confirmed,'tangent_reveal_sec':edit['tangent_reveal_sec'],
            'graph_slope':art.g.slope,'caption_mode':edit['captions'],'paid_generation_calls':0}
    save(p/'renders/validation.json',report);print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
