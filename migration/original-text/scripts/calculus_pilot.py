#!/usr/bin/env python3
"""Render a local 15-second Ignite calculus pilot from copied website artwork.

Requires Pillow and FFmpeg; macOS `say` supplies replaceable draft narration.
No provider calls, API keys, or access to the original website are needed.
"""

import argparse
from functools import lru_cache
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import wave

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT, FPS = 720, 1280, 30
SHOT_SECONDS = 3
PAPER = '#FFF8F0'
INK = '#1A1A2E'
ORANGE = '#F07B2A'
TEAL = '#4F9298'
BEATS = [
    ('How steep is a curve at one point?', 'How steep is\na curve?', 'A question for Sol.'),
    ('Two points give an average slope.', 'Two points.\nOne slope.', 'AVERAGE CHANGE'),
    ('Bring those points closer together.', 'Bring them\ncloser.', 'LET THE GAP SHRINK'),
    ('The line approaches a tangent.', 'Meet the\ntangent.', 'ONE POINT, ONE DIRECTION'),
    ('Its slope is the derivative: change right here.', 'Change.\nRight here.', 'THAT IS A DERIVATIVE'),
]


def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-6000:] or result.stdout[-6000:])
    return result


def ease(value):
    value = max(0, min(1, value))
    return value * value * (3 - 2 * value)


class Art:
    def __init__(self, project):
        self.project = project
        self.font_dir = project / 'assets/fonts'
        self.scene = Image.open(project / 'assets/calculus-painted-scene.jpg').convert('RGB')
        self.sol = Image.open(project / 'assets/sol-full-body.png').convert('RGBA')
        # Trim only transparent margins in the rendered instance; source copies stay intact.
        self.sol = self.sol.crop(self.sol.getchannel('A').getbbox())
        self.sol_small = self.sol.resize((164, round(164 * self.sol.height / self.sol.width)), Image.Resampling.LANCZOS)
        self.scene_cache = {}

    @lru_cache(maxsize=40)
    def font(self, family, size):
        font = ImageFont.truetype(str(self.font_dir / family), size)
        if family == 'Nunito.ttf':
            font.set_variation_by_axes([650])
        return font

    def text(self, draw, xy, text, size=28, color=INK, family='Nunito.ttf', **kwargs):
        draw.text(xy, text, font=self.font(family, size), fill=color, **kwargs)

    def pill(self, draw, box, text, color=INK, fill='#FFFFFF', size=25):
        draw.rounded_rectangle(box, radius=20, fill=fill)
        self.text(draw, ((box[0]+box[2])/2, (box[1]+box[3])/2), text, size, color, anchor='mm', family='Poppins-SemiBold.ttf')

    def scene_panel(self, frame, draw, top, height, progress):
        # Reframe the copied wide scene with a gentle camera push, preserving all artwork.
        base_width = 624
        scale = 1 + 0.035 * ease(progress)
        size = (round(base_width * scale), round(height * scale))
        key = size
        if key not in self.scene_cache:
            self.scene_cache[key] = self.scene.resize(size, Image.Resampling.LANCZOS)
        picture = self.scene_cache[key]
        x, y = (picture.width-base_width)//2, (picture.height-height)//2
        picture = picture.crop((x, y, x+base_width, y+height))
        mask = Image.new('L', picture.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, base_width-1, height-1), 30, fill=255)
        draw.rounded_rectangle((48, top+8, 672, top+height+8), radius=30, fill='#EFDFD0')
        frame.paste(picture, (48, top), mask)

    def graph(self, frame, draw, shot, progress):
        draw.rounded_rectangle((48, 374, 672, 916), radius=30, fill='#FFFFFF')
        self.text(draw, (76, 398), 'y = x²', 26, TEAL, family='Poppins-SemiBold.ttf')
        self.text(draw, (644, 408), 'SLOPE LAB', 16, '#73737F', anchor='ra')
        x0, y0, sx, sy = 96, 838, 205, 58

        def point(x, y):
            return (x0+x*sx, y0-y*sy)

        for x in (0, 1, 2):
            px, _ = point(x, 0)
            draw.line((px, 466, px, y0), fill='#F1F0EC', width=2)
            self.text(draw, (px, y0+14), str(x), 20, '#6C6C79', anchor='ma')
        for y in (0, 2, 4, 6):
            _, py = point(0, y)
            draw.line((x0, py, 634, py), fill='#F1F0EC', width=2)
        draw.line((x0, 464, x0, y0, 638, y0), fill='#D7D4D0', width=3)
        curve = [point(i/100, (i/100)**2) for i in range(249)]
        draw.line(curve, fill=TEAL, width=8, joint='curve')
        q = 2.28 if shot == 1 else (2.28 - 1.25*ease(progress) if shot == 2 else 1.0)
        slope = 1 + q if shot < 3 else 2
        intercept = 1-slope
        left = max(0, -intercept/slope)
        right = min(2.58, (6.2-intercept)/slope)
        draw.line((point(left, slope*left+intercept), point(right, slope*right+intercept)), fill=ORANGE, width=5)
        p = point(1, 1)
        if shot < 3:
            qp = point(q, q*q)
            elbow = point(q, 1)
            for a, b in ((p, elbow), (elbow, qp)):
                length = math.dist(a, b)
                for start in range(0, int(length), 14):
                    end = min(start+7, length)
                    draw.line((a[0]+(b[0]-a[0])*start/length, a[1]+(b[1]-a[1])*start/length,
                               a[0]+(b[0]-a[0])*end/length, a[1]+(b[1]-a[1])*end/length), fill='#D9AC84', width=3)
            draw.ellipse((qp[0]-9, qp[1]-9, qp[0]+9, qp[1]+9), fill=ORANGE, outline='#FFFFFF', width=3)
            if q > 1.15:
                self.text(draw, (qp[0]+12, qp[1]-26), 'Q', 23, ORANGE, family='Poppins-SemiBold.ttf')
        draw.ellipse((p[0]-10, p[1]-10, p[0]+10, p[1]+10), fill=INK, outline='#FFFFFF', width=3)
        self.text(draw, (p[0]-10, p[1]+20), 'P', 23, INK, family='Poppins-SemiBold.ttf')
        if shot == 1:
            self.pill(draw, (76, 868, 460, 906), 'average slope = rise / run', size=19, fill='#FFF2E6')
        elif shot == 2:
            self.pill(draw, (76, 868, 454, 906), 'smaller gap, closer slope', size=19, fill='#FFF2E6')
        else:
            self.pill(draw, (76, 868, 420, 906), "f'(1) = 2", size=24, fill='#FFF2E6')
            self.pill(draw, (391, 453, 633, 494), 'TANGENT', color='#FFFFFF', fill=TEAL, size=19)
        bob = round(3*math.sin(progress*math.pi*2))
        frame.paste(self.sol_small, (500, 837+bob), self.sol_small)

    def frame(self, number):
        t = number/FPS
        shot = min(4, int(t/SHOT_SECONDS))
        progress = (t-shot*SHOT_SECONDS)/SHOT_SECONDS
        frame = Image.new('RGB', (WIDTH, HEIGHT), PAPER)
        draw = ImageDraw.Draw(frame)
        self.text(draw, (48, 57), 'Ignite', 27, ORANGE, family='RammettoOne-Regular.ttf')
        self.text(draw, (672, 68), 'CALCULUS / 15 SECONDS', 17, '#73737F', anchor='ra', family='Poppins-SemiBold.ttf')
        draw.line((48, 110, 672, 110), fill='#E9D9C9', width=2)
        self.text(draw, (48, 148), BEATS[shot][1], 54, family='RammettoOne-Regular.ttf', spacing=5)
        self.text(draw, (50, 315), BEATS[shot][2], 17, '#77717A', family='Poppins-SemiBold.ttf')
        if shot == 0:
            self.scene_panel(frame, draw, 389, 348, progress)
            self.pill(draw, (106, 786, 614, 854), 'A whole curve. A single point.', size=23)
            self.text(draw, (360, 897), 'Start with a question. Follow the change.', 23, '#706A70', anchor='ma')
        elif shot < 4:
            self.graph(frame, draw, shot, progress)
        else:
            self.scene_panel(frame, draw, 377, 348, progress)
            sol = self.sol.resize((172, round(172*self.sol.height/self.sol.width)), Image.Resampling.LANCZOS)
            frame.paste(sol, (61, 786+round(3*math.sin(progress*math.pi*2))), sol)
            self.text(draw, (279, 800), 'Derivative', 32, family='Poppins-SemiBold.ttf')
            self.text(draw, (279, 848), '= slope here.', 31, TEAL, family='Poppins-SemiBold.ttf')
            self.text(draw, (279, 906), 'For this curve, at x = 1:  2', 19, '#706A70')
        # Burn in the exact narrated sentence; leave mobile UI safe space below.
        draw.rounded_rectangle((40, 1043, 680, 1191), radius=26, fill=INK)
        words = BEATS[shot][0].split()
        lines, line = [], ''
        for word in words:
            candidate = (line+' '+word).strip()
            if draw.textlength(candidate, font=self.font('Nunito.ttf', 33)) > 566:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
        caption = '\n'.join(lines)
        self.text(draw, (360, 1117), caption, 33, '#FFFFFF', anchor='mm', align='center', spacing=7)
        for index in range(5):
            left = 48+index*127
            draw.rounded_rectangle((left, 1220, left+112, 1225), radius=2, fill='#EAD9C9')
            amount = 1 if index < shot else (progress if index == shot else 0)
            if amount:
                draw.rounded_rectangle((left, 1220, left+max(2,112*amount), 1225), radius=2, fill=ORANGE)
        return frame


def generate_narration(project, ffmpeg, voice):
    audio = project/'audio'
    audio.mkdir(exist_ok=True)
    pieces = []
    timings = []
    for i, (sentence, _, _) in enumerate(BEATS):
        source = audio/f'beat_{i+1}.aiff'
        raw = audio/f'beat_{i+1}-raw.wav'
        target = audio/f'beat_{i+1}.wav'
        run(['say', '-v', voice, '-r', '175', '-o', str(source), sentence])
        run([ffmpeg, '-y', '-v', 'error', '-i', str(source), '-ar', '48000', '-ac', '1', str(raw)])
        with wave.open(str(raw)) as wav:
            duration = wav.getnframes()/wav.getframerate()
        speed = max(1, duration/2.72)
        run([ffmpeg, '-y', '-v', 'error', '-i', str(raw), '-af', f'atempo={speed:.6f},adelay=100,apad', '-t', '3', str(target)])
        with wave.open(str(target)) as wav:
            pieces.append(wav.readframes(wav.getnframes()))
        timings.append({'beat':i+1,'raw_seconds':duration,'tempo':speed,'timeline_seconds':3})
    narration = audio/'narration.wav'
    with wave.open(str(narration), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(48000)
        wav.writeframes(b''.join(pieces))
    (audio/'timing.json').write_text(json.dumps(timings,indent=2)+'\n')
    return narration


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=REPO/'out/calculus_pilot')
    parser.add_argument('--ffmpeg', default=os.environ.get('FFMPEG_PATH') or shutil.which('ffmpeg'))
    parser.add_argument('--voice', default='Samantha', help='Installed macOS voice for draft narration')
    parser.add_argument('--reuse-narration', action='store_true', help='Keep the existing 15-second audio/narration.wav')
    args = parser.parse_args()
    if not args.ffmpeg:
        parser.error('Pass --ffmpeg /path/to/ffmpeg or set FFMPEG_PATH.')
    project = args.project.resolve()
    project.mkdir(parents=True,exist_ok=True)
    assets = project/'assets'
    for name in ('sol-full-body.png','calculus-painted-scene.jpg'):
        if not (assets/name).is_file():
            parser.error(f'Missing copied asset: {assets/name}')
    art = Art(project)
    (project/'previews').mkdir(exist_ok=True)
    for shot in range(5):
        art.frame(shot*90+45).save(project/f'previews/beat_{shot+1}.png')
    storyboard = Image.new('RGB',(WIDTH*5//2,HEIGHT//2),PAPER)
    for shot in range(5):
        image = Image.open(project/f'previews/beat_{shot+1}.png')
        storyboard.paste(image.resize((WIDTH//2,HEIGHT//2),Image.Resampling.LANCZOS),(shot*WIDTH//2,0))
    storyboard.save(project/'storyboard.jpg',quality=92)
    beats = {'project_name':'calculus_pilot','topic':'A derivative is a tangent slope','aspect_ratio':'9:16',
             'renderer':'scripts/calculus_pilot.py','fps':FPS,'duration_sec':15,'voice':args.voice,
             'beats':[{'beat_id':f'beat_{i+1}','narration':sentence,'start_sec':i*3,'end_sec':(i+1)*3,
                       'shots':[{'shot_id':f'beat_{i+1}_a','duration_sec':3,'scene_description':title.replace('\n',' ')}]}
                      for i,(sentence,title,_) in enumerate(BEATS)]}
    (project/'beats.json').write_text(json.dumps(beats,indent=2)+'\n')
    srt=[]
    for i,(sentence,_,_) in enumerate(BEATS):
        srt.append(f'{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{sentence}\n')
    (project/'captions.srt').write_text('\n'.join(srt))
    (project/'narration.txt').write_text('\n'.join(b[0] for b in BEATS)+'\n')
    narration = project/'audio/narration.wav'
    if args.reuse_narration:
        if not narration.is_file():
            parser.error('--reuse-narration needs audio/narration.wav')
    else:
        narration = generate_narration(project,args.ffmpeg,args.voice)
    silent = project/'picture.mp4'
    command=[args.ffmpeg,'-y','-v','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24',
             '-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast',
             '-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(silent)]
    # Use a disk log to keep stderr from blocking the raw-frame pipe.
    with (project/'render.log').open('w') as log:
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=log)
        try:
            for number in range(FPS*15):
                process.stdin.write(art.frame(number).tobytes())
                if number%90==0:
                    print(f'Rendering beat {number//90+1}/5',flush=True)
        finally:
            process.stdin.close()
        if process.wait():
            raise RuntimeError((project/'render.log').read_text())
    final=project/'final.mp4'
    run([args.ffmpeg,'-y','-v','error','-i',str(silent),'-i',str(narration),'-map','0:v:0','-map','1:a:0',
         '-c:v','copy','-c:a','aac','-b:a','160k','-t','15','-movflags','+faststart',str(final)])
    # Decode the whole deliverable, not just its container header.
    decoded=run([args.ffmpeg,'-hide_banner','-i',str(final),'-f','null','-'])
    (project/'decode-check.log').write_text(decoded.stderr)
    duration=re.search(r'Duration: ([\d:.]+)',decoded.stderr)
    report={'output':str(final),'duration':duration.group(1) if duration else None,'frames':FPS*15,
            'canvas':[WIDTH,HEIGHT],'fps':FPS,'full_decode':'passed','narration':'local macOS synthetic draft',
            'paid_generation_calls':0,'assets':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                            for p in assets.iterdir() if p.is_file()}}
    (project/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    # V2 reuses the artwork/font helpers above, with an importable edit timeline.
    from calculus_edit import main as revised_main
    revised_main()
