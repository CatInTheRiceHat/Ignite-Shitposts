"""Reusable, local video anomaly screening. Findings are review candidates, not approvals."""
import argparse
from bisect import bisect_left, bisect_right
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

from paths import WORKFLOW

VERSION = 2
REPORTS = WORKFLOW / 'inspections'


def dependencies():
    try:
        import cv2
        import numpy as np
    except ImportError as error:
        raise RuntimeError('Install workflow/requirements.txt in workflow/.venv, then use '
                           'workflow/.venv/bin/python workflow/scripts/shorts.py inspect-video.') from error
    return cv2, np


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()


def run(args):
    return subprocess.run(args, check=True, capture_output=True)


def probe(video):
    data = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_streams', '-show_format', '-show_frames', '-show_entries',
        'stream=width,height,avg_frame_rate,duration:stream_side_data=rotation:format=duration:frame=best_effort_timestamp_time,duration_time,pkt_duration_time',
        '-of', 'json', str(video)]).stdout)
    if not data.get('streams') or not data.get('frames'):
        raise ValueError('Choose a video with decodable picture frames.')
    stream = data['streams'][0]
    times = [float(f['best_effort_timestamp_time']) for f in data['frames']]
    origin = times[0]
    times = [t - origin for t in times]
    if any(b < a for a, b in zip(times, times[1:])):
        raise ValueError('Video frame timestamps are not in chronological order.')
    num, den = map(float, stream['avg_frame_rate'].split('/'))
    fps = num / den if den else 0
    rotation = next((int(s['rotation']) % 360 for s in stream.get('side_data_list', [])
                     if 'rotation' in s), 0)
    if rotation not in (0, 90, 180, 270):
        raise ValueError('This rotation is not supported. Export with an upright picture first.')
    width, height = stream['width'], stream['height']
    if rotation in (90, 270): width, height = height, width
    last = data['frames'][-1]
    step = float(last.get('duration_time') or last.get('pkt_duration_time') or (1/fps if fps else .04))
    return {'width': width, 'height': height, 'fps': fps, 'rotation': rotation,
            'duration': times[-1]+step, 'timestamps': times,
            'frames': len(times)}


def components(mask, cv2, np, minimum=5, maximum=1500):
    count, labels, stats, centers = cv2.connectedComponentsWithStats(mask.astype('uint8'), connectivity=8)
    found = []
    for i in range(1, count):
        x, y, w, h, area = map(int, stats[i])
        if (minimum <= area <= maximum and min(w, h) >= 2 and
                max(w, h) / min(w, h) < 7 and area / (w * h) > .16):
            found.append({'box': [x, y, w, h], 'area': area, 'center': centers[i].tolist(),
                          'label': i, 'labels': labels})
    return found


def align(reference, current, cv2, np):
    a = cv2.cvtColor(reference, cv2.COLOR_RGB2GRAY).astype('float32')
    b = cv2.cvtColor(current, cv2.COLOR_RGB2GRAY).astype('float32')
    (dx, dy), response = cv2.phaseCorrelate(a, b)
    h, w = a.shape
    if response > .12 and abs(dx) < w * .12 and abs(dy) < h * .12:
        matrix = np.float32([[1, 0, dx], [0, 1, dy]])
        aligned = cv2.warpAffine(reference, matrix, (w, h), flags=cv2.INTER_LINEAR,
                                borderMode=cv2.BORDER_REFLECT_101)
        return aligned, math.hypot(dx, dy)
    return reference, 0.


def screen_frames(frames, timestamps, threshold=28, progress=lambda *args: None):
    """Resolution-independent temporal novelty and isolated-detail screening."""
    cv2, np = dependencies()
    n, h, w, _ = frames.shape
    hashes = [hashlib.md5(frames[i].tobytes()).digest() for i in range(n)]
    states = [i for i in range(n) if i == 0 or hashes[i] != hashes[i-1]]
    cuts, flashes = [], []
    for j in range(1, len(states)):
        a, b = states[j-1], states[j]
        delta = np.abs(frames[a].astype('int16') - frames[b].astype('int16')).mean(axis=2)
        if float((delta > 42).mean()) > .58:
            cuts.append(b)
            flashes.append({'frame': b, 'kind': 'flash_or_cut', 'box': [0, 0, w, h],
                            'strength': float(delta.mean()), 'priority': 'context'})
    segments = [0] + cuts + [n]
    detections = list(flashes)
    motion_count = 0
    analyzed_states = 0
    for start, end in zip(segments, segments[1:]):
        ids = [i for i in states if start <= i < end]
        if len(ids) < 3: continue
        samples = sorted(set(ids[int(x)] for x in np.linspace(0, len(ids)-1, min(25, len(ids)))))
        background = np.median(np.asarray(frames[samples]), axis=0).astype('uint8')
        edges = cv2.Canny(cv2.cvtColor(background, cv2.COLOR_RGB2GRAY), 50, 130)
        edge_distance = cv2.distanceTransform(255-edges, cv2.DIST_L2, 3)
        for position, index in enumerate(ids):
            analyzed_states += 1
            current = frames[index]
            t = timestamps[index]
            # Neighbor selection follows actual timestamps, including variable frame rate.
            before = bisect_right(timestamps,t-.18,lo=start,hi=index)-1
            after = bisect_left(timestamps,t+.18,lo=index+1,hi=end)
            if before >= start and after < end:
                left, shift1 = align(frames[before], current, cv2, np)
                right, shift2 = align(frames[after], current, cv2, np)
                motion_count += int(max(shift1, shift2) > 2)
                dl = np.abs(current.astype('int16')-left.astype('int16')).mean(axis=2)
                dr = np.abs(current.astype('int16')-right.astype('int16')).mean(axis=2)
                novelty = np.minimum(dl, dr)
                mask = (novelty > threshold).astype('uint8')
                mask[:3] = 0; mask[-3:] = 0; mask[:, :3] = 0; mask[:, -3:] = 0
                for c in components(mask, cv2, np, maximum=int(w*h*.008)):
                    x,y,bw,bh = c['box']
                    local = c['labels'][y:y+bh,x:x+bw] == c['label']
                    # Thin differences hugging an existing edge are usually normal motion.
                    clearance = float(np.median(edge_distance[y:y+bh,x:x+bw][local]))
                    if clearance < 1.8 and c['area'] / (bw*bh) < .5: continue
                    strength = float(np.median(novelty[y:y+bh,x:x+bw][local]))
                    detections.append({'frame':index,'kind':'brief_local_change','box':c['box'],
                                       'strength':strength,'priority':'review'})
            # A robust scene background finds small detached details lasting longer than a blink.
            delta = current.astype('int16')-background.astype('int16')
            delta -= np.median(delta.reshape(-1,3),axis=0).astype('int16')
            difference = np.abs(delta).mean(axis=2)
            mask = (difference > threshold+5).astype('uint8')
            mask[:3]=0;mask[-3:]=0;mask[:,:3]=0;mask[:,-3:]=0
            for c in components(mask,cv2,np,minimum=6,maximum=int(w*h*.004)):
                x,y,bw,bh=c['box']
                if max(bw,bh)>min(w,h)*.18: continue
                local=c['labels'][y:y+bh,x:x+bw]==c['label']
                if float(np.median(edge_distance[y:y+bh,x:x+bw][local]))<1.5: continue
                detections.append({'frame':index,'kind':'isolated_detail','box':c['box'],
                                   'strength':float(np.median(difference[y:y+bh,x:x+bw][local])),
                                   'priority':'review'})
            if analyzed_states % 12 == 0:
                progress(.25+.5*index/max(n,1),f'Inspecting frame {index+1} of {n}')
    events = group_detections(detections,timestamps,(w,h))
    return events, {'analyzed_frames':n,'distinct_states':len(states),'scene_boundaries':cuts,
                    'camera_motion_samples':motion_count,'raw_candidates':len(detections)}


def group_detections(detections, timestamps, size):
    """Merge repeated frame flags into spatially continuous review moments."""
    w,h=size
    tracks=[]
    for d in sorted(detections,key=lambda d:d['frame']):
        t=timestamps[d['frame']];x,y,bw,bh=d['box'];cx=x+bw/2;cy=y+bh/2
        best=None;distance_limit=max(10,min(w,h)*.055)
        for tr in reversed(tracks):
            last=tr['items'][-1]
            if tr['kind']!=d['kind'] or t-timestamps[last['frame']]>.24:continue
            lx,ly,lw,lh=last['box'];distance=math.hypot(cx-lx-lw/2,cy-ly-lh/2)
            if distance<distance_limit and (best is None or distance<best[0]):best=(distance,tr)
        if best:best[1]['items'].append(d)
        else:tracks.append({'kind':d['kind'],'items':[d]})
    events=[]
    for track in tracks:
        items=track['items'];frames=sorted({d['frame'] for d in items});kind=track['kind']
        start,end=timestamps[frames[0]],timestamps[frames[-1]]
        if kind=='isolated_detail':
            if len(frames)<2 or end-start>3.0:continue
            centers=[(d['box'][0]+d['box'][2]/2,d['box'][1]+d['box'][3]/2) for d in items]
            travel=max(math.hypot(x-centers[0][0],y-centers[0][1]) for x,y in centers)
            if travel<2.5:continue
        representative=max(items,key=lambda d:d['strength'])
        title={'brief_local_change':'Brief new mark or shape',
               'isolated_detail':'Small moving detail', 'flash_or_cut':'Flash or scene cut'}[kind]
        frames_dedup={d['frame']:d for d in items}
        events.append({'id':f'event-{len(events)+1:03d}','kind':kind,'title':title,
            'priority':representative['priority'],'start':start,'end':end,
            'frame_start':frames[0],'frame_end':frames[-1],
            'representative_frame':representative['frame'],
            'strength':round(representative['strength'],1),
            'box':[round(v/(w if i%2==0 else h),6) for i,v in enumerate(representative['box'])],
            'samples':[{'frame':f,'time':timestamps[f],
                        'box':[round(v/(w if i%2==0 else h),6) for i,v in enumerate(frames_dedup[f]['box'])]}
                       for f in frames],
            'verdict':'unreviewed'})
    return sorted(events,key=lambda e:(e['start'],e['kind']))


def cadence_check(video,fps,timestamps=None):
    text=run(['ffmpeg','-v','error','-nostdin','-i',str(video),'-map','0:v:0',
              '-fps_mode','passthrough','-f','framemd5','-']).stdout.decode()
    hashes=[line.rsplit(',',1)[1].strip() for line in text.splitlines() if line and not line.startswith('#')]
    mismatches=[i for i in range(0,len(hashes)-1,2) if hashes[i]!=hashes[i+1]]
    regular = timestamps is None or all(abs(b-a-1/30)<.00001 for a,b in zip(timestamps,timestamps[1:]))
    passed=abs(fps-30)<.001 and len(hashes)%2==0 and not mismatches and regular
    return {'requested':True,'passed':passed,'basis':'Native decoded frame hashes without pixel-format reduction',
            'frames':len(hashes),'fps':fps,'mismatched_pair_start_frames':mismatches,
            'complete_pairs':len(hashes)%2==0,'regular_frame_times':regular}


def write_report(report,output,frames,first=None,last=None):
    from PIL import Image,ImageDraw
    output=Path(output)
    assets=output/'evidence';assets.mkdir()
    # Decode all flagged full-size source states in one pass, once per unique frame.
    native_ids=sorted({e['representative_frame'] for e in report['events']})
    if native_ids:
        expression='+'.join(f'eq(n\\,{i})' for i in native_ids)
        run(['ffmpeg','-v','error','-nostdin','-i',str(output/report['video_url']),
             '-map','0:v:0','-vf',f'select={expression}','-fps_mode','passthrough',
             str(assets/'native-%05d.png')])
    native_paths={frame:assets/f'native-{i+1:05d}.png' for i,frame in enumerate(native_ids)}
    for event in report['events']:
        index=event['representative_frame'];box=event['box']
        ids=[max(0,index-6),index,min(len(frames)-1,index+6)]
        panels=[]
        for j in ids:
            im=Image.fromarray(frames[j].copy());draw=ImageDraw.Draw(im)
            x,y,w,h=[v*s for v,s in zip(box,[im.width,im.height,im.width,im.height])]
            draw.rectangle((x,y,x+w,y+h),outline='#ffcb69',width=2)
            panel=Image.new('RGB',(im.width,im.height+26),'#171b23');panel.paste(im,(0,26))
            ImageDraw.Draw(panel).text((8,6),f'Frame {j} / {report["video"]["timestamps"][j]:.3f}s',fill='white')
            panels.append(panel)
        sheet=Image.new('RGB',(sum(im.width for im in panels),panels[0].height))
        offset=0
        for im in panels:sheet.paste(im,(offset,0));offset+=im.width
        filename=f'{event["id"]}.jpg';sheet.save(assets/filename,quality=90)
        event['evidence']=f'evidence/{filename}'
        with Image.open(native_paths[index]) as native:
            nx,ny,nw,nh=[v*s for v,s in zip(box,[native.width,native.height,native.width,native.height])]
            padding=max(50,nw,nh)
            crop=native.crop((max(0,int(nx-padding)),max(0,int(ny-padding)),
                              min(native.width,int(nx+nw+padding)),min(native.height,int(ny+nh+padding))))
            crop_name=f'{event["id"]}-detail.png';crop.save(assets/crop_name)
            event['crop']='evidence/'+crop_name
            event['native_frame']='evidence/'+native_paths[index].name
    for name,path in [('first',first),('last',last)]:
        if path:
            destination=output/f'reference-{name}{Path(path).suffix.lower()}'
            shutil.copy2(path,destination)
            report.setdefault('references',{})[name]=destination.name
    # Contact sheets make the whole candidate list reviewable with ordinary image tools.
    pages=[]
    events=report['events']
    for start in range(0,len(events),20):
        batch=events[start:start+20]
        sheet=Image.new('RGB',(1000,290*math.ceil(len(batch)/4)),'#171b23')
        draw=ImageDraw.Draw(sheet)
        for offset,event in enumerate(batch):
            x=(offset%4)*250;y=(offset//4)*290
            with Image.open(output/event['crop']) as crop:
                crop.thumbnail((238,238))
                sheet.paste(crop,(x+(250-crop.width)//2,y+42+(238-crop.height)//2))
            draw.text((x+8,y+6),f'{event["id"]}  {event["start"]:.3f}-{event["end"]:.3f}s',fill='white')
            draw.text((x+8,y+22),event['title'],fill='#ffcb69')
        name=f'overview-{len(pages)+1:02d}.jpg';sheet.save(output/name,quality=92);pages.append(name)
    report['overview_pages']=pages
    lines=[f'VIDEO INSPECTION: {report["name"]}',
           f'{report["coverage"]["analyzed_frames"]} frames decoded; {len(events)} candidates for visual review.',
           'No automatic approval. The source video is unchanged.',
           *report['limitations'],'']
    if report['cadence']['requested']:
        lines.append('Exact animation on twos: '+('PASS' if report['cadence']['passed'] else 'CHECK REQUIRED'))
    lines+=['Overview sheets: '+(', '.join(pages) or 'No candidate frames.'),'']
    for event in events:
        lines.append(f'{event["id"]} | {event["start"]:.3f}-{event["end"]:.3f}s | '
                     f'frames {event["frame_start"]}-{event["frame_end"]} | {event["title"]} | {event["crop"]}')
    (output/'summary.txt').write_text('\n'.join(lines)+'\n')
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')


def scan(video,output=None,width=384,threshold=28,check_twos=False,first=None,last=None,
         progress=lambda *args: None):
    cv2,np=dependencies();video=Path(video).resolve()
    if not video.is_file():raise ValueError(f'Video not found: {video}')
    if not 192<=width<=768:raise ValueError('Analysis width must be 192–768 pixels.')
    if not 12<=threshold<=60:raise ValueError('Sensitivity threshold must be 12–60.')
    progress(.02,'Reading video and exact frame times')
    info=probe(video);source_hash=sha(video)
    config={'version':VERSION,'width':width,'threshold':threshold,'check_twos':check_twos,
            'first':sha(first) if first else None,'last':sha(last) if last else None}
    config_hash=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()[:8]
    slug=re.sub(r'[^a-zA-Z0-9_-]+','-',video.stem)[:60]
    output=Path(output).resolve() if output else REPORTS/f'{slug}-{source_hash[:10]}-{config_hash}'
    if output.exists():
        saved=output/'report.json'
        if saved.is_file():
            existing=json.loads(saved.read_text())
            if (existing['source_sha256']==source_hash and existing['settings']==config
                    and (output/'summary.txt').is_file() and not (output/'incomplete.txt').exists()):
                progress(1,'Existing inspection ready');return output
        raise FileExistsError(f'Existing output preserved: {output}')
    output.mkdir(parents=True)
    scratch=WORKFLOW/'.cache';scratch.mkdir(exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix='inspect-',dir=scratch) as temporary:
            h=round(info['height']*width/info['width']);n=info['frames']
            frames=np.memmap(Path(temporary)/'frames.rgb',dtype=np.uint8,mode='w+',shape=(n,h,width,3))
            process=subprocess.Popen(['ffmpeg','-v','error','-nostdin','-i',str(video),
                '-map','0:v:0','-vf',f'scale={width}:{h}','-fps_mode','passthrough',
                '-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            try:
                for i in range(n):
                    data=process.stdout.read(width*h*3)
                    if len(data)!=width*h*3:raise ValueError('Video decode ended before the reported frame count.')
                    frames[i]=np.frombuffer(data,np.uint8).reshape(h,width,3)
                    if i%30==0:progress(.05+.18*i/n,f'Decoding frame {i+1} of {n}')
                extra=process.stdout.read(1)
                error=process.stderr.read().decode(errors='replace')
                if process.wait()!=0 or extra:raise ValueError('Video decode/frame count failed: '+error[-600:])
            finally:
                if process.poll() is None:process.kill();process.wait()
                process.stdout.close();process.stderr.close()
            events,coverage=screen_frames(frames,info['timestamps'],threshold,progress)
            progress(.8,'Checking cadence and assembling evidence')
            cadence=cadence_check(video,info['fps'],info['timestamps']) if check_twos else {'requested':False}
            report={'version':VERSION,'name':video.name,'source_sha256':source_hash,'settings':config,
                'video':info,'video_url':'video'+video.suffix.lower(),'coverage':coverage,
                'cadence':cadence,'events':events,'created_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
                'status':'needs_visual_review','automatic_approval':False,
                'method':'Every decoded frame; temporal novelty, registered neighbor comparisons, compact moving details and scene-change screening.',
                'limitations':['Flags are candidates, not confirmed defects. Intentional blinks, fire and gestures can be flagged.',
                               'Small or persistent defects can be missed; visual identity and story review remain required.',
                               'Motion alignment is used only for analysis; source video is never changed.']}
            shutil.copy2(video,output/report['video_url'])
            if sha(output/report['video_url'])!=source_hash:raise ValueError('Video copy verification failed.')
            write_report(report,output,frames,first,last)
            del frames
        progress(1,f'Inspection ready: {len(events)} review moments')
        return output
    except Exception:
        # Keep any diagnostic output, clearly marked incomplete and never reusable as a result.
        (output/'incomplete.txt').write_text('Inspection did not complete. Original video preserved.\n')
        raise


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video',nargs='?')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--width',type=int,default=384)
    parser.add_argument('--threshold',type=int,default=28)
    parser.add_argument('--check-twos',action='store_true')
    parser.add_argument('--first',type=Path)
    parser.add_argument('--last',type=Path)
    args=parser.parse_args(argv)
    try:
        if not args.video:parser.error('Choose a video path.')
        out=scan(args.video,args.output,args.width,args.threshold,args.check_twos,args.first,args.last,
                 lambda p,m:print(f'{round(p*100):3d}% {m}',flush=True))
        print(json.dumps({'summary':str(out/'summary.txt'),'data':str(out/'report.json')}))
        return 0
    except (OSError,ValueError,RuntimeError,subprocess.CalledProcessError) as error:
        print(str(error),file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
