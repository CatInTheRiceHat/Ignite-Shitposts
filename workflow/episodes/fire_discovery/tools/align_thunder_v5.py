"""Advance the existing effect to align its internal impact with the flash."""
import hashlib
import json
import math
import re
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

EP = Path(__file__).resolve().parents[1]
QC = EP / 'reviews/thunder-sync-v5'
QC.mkdir(parents=True, exist_ok=True)
SOURCE = EP / 'renders/fire-discovery-sound-v4-review.mp4'
OUTPUT = EP / 'renders/fire-discovery-thunder-sync-v5-review.mp4'
MIX = EP / 'audio/sound-v5/mix.wav'
MIX.parent.mkdir(exist_ok=True)

def run(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def measure(path):
    r=run(['ffmpeg','-hide_banner','-nostdin','-i',str(path),'-vn','-af',
           'loudnorm=I=-16:LRA=11:TP=-1.5:print_format=json','-f','null','-'],capture_output=True,text=True)
    return json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr,re.S)[-1])

def read_wav(path):
    with wave.open(str(path)) as w:
        rate=w.getframerate()
        data=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,w.getnchannels()).mean(axis=1)/32768
    return rate,data

assert not OUTPUT.exists(), 'Preserve the existing output.'
edit=json.loads((EP/'edit.json').read_text())
for name in ['edit.json','script.txt','shot-plan.json','higgsfield-prompts.txt','handoff.txt','handoff-validation.json']:
    backup=QC/'prior-state'/name
    backup.parent.mkdir(exist_ok=True)
    if backup.exists(): raise FileExistsError(backup)
    shutil.copy2(EP/name,backup)
sting=next(t for t in edit['audioTracks'] if t['id']=='lightning-bomboclat')
previous_start=sting['start']
sting['start']=286/30
rate,data=read_wav(EP/sting['src'])
window=round(rate*.001)
rms=np.sqrt(np.mean(data[:len(data)//window*window].reshape(-1,window)**2,axis=1))
impact=float(np.flatnonzero(rms>10**(-24/20))[0]*window/rate)
assert abs(sting['start']+impact-292/30)<1/30

# Match the renderer's frame-rounded track starts, trims and durations.
cmd=['ffmpeg','-v','error','-nostdin','-n']
filters=[]
for i,t in enumerate(edit['audioTracks']):
    source=EP/t['src']
    assert sha(source)==t['source_sha256']
    assert t['playbackRate']==1
    cmd+=['-i',str(source)]
    start=math.floor(t['start']*30+.5)*1600
    trim=math.floor(t.get('trimBefore',0)*30+.5)/30
    duration=math.floor(t['duration']*30+.5)/30
    filters.append(f'[{i}:a]aresample=48000,atrim=start={trim}:duration={duration},asetpts=PTS-STARTPTS,volume={t["volume"]},adelay={start}S:all=1[a{i}]')
filters.append(''.join(f'[a{i}]' for i in range(len(edit['audioTracks'])))+f'amix=inputs={len(edit["audioTracks"])}:duration=longest:normalize=0,apad,atrim=duration=25.8[mix]')
run(cmd+['-filter_complex',';'.join(filters),'-map','[mix]','-ar','48000','-ac','2','-c:a','pcm_f32le',str(MIX)])
before=measure(MIX)
af=('loudnorm=I=-16:LRA=11:TP=-1.5:linear=true:measured_I='+before['input_i']+':measured_LRA='+before['input_lra']+':measured_TP='+before['input_tp']+':measured_thresh='+before['input_thresh']+':offset='+before['target_offset'])
run(['ffmpeg','-v','error','-nostdin','-n','-i',str(SOURCE),'-i',str(MIX),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',af,'-c:a','aac','-b:a','192k','-ar','48000','-t','25.8','-movflags','+faststart',str(OUTPUT)])
run(['ffmpeg','-v','error','-nostdin','-i',str(OUTPUT),'-f','null','-'])
after=measure(OUTPUT)
assert abs(float(after['input_i'])+16)<.2 and float(after['input_tp'])<-1
def video_hash(path):
    return subprocess.check_output(['ffmpeg','-v','error','-nostdin','-i',str(path),'-map','0:v:0','-c:v','copy','-f','hash','-hash','sha256','-'],text=True).strip()
assert video_hash(SOURCE)==video_hash(OUTPUT)
raw=subprocess.check_output(['ffmpeg','-v','error','-nostdin','-i',str(OUTPUT),'-ss',str(sting['start']),'-t','1','-vn','-ac','1','-ar','48000','-f','f32le','-'])
decoded=np.frombuffer(raw,np.float32)
corr=float(np.corrcoef(decoded,data[:len(decoded)])[0,1])
assert corr>.95
edit['timing']['note']='25.8-second sound correction: file starts at9.533333s; main impact at9.722333s meets lightning flash at9.733333s (11ms early, within one frame). All dialogue/music/captions/picture retained. New fireplace scene stills remain separate pending approval.'
for name in ['edit.json','edit-thunder-sync-v5.json']:
    (EP/name).write_text(json.dumps(edit,indent=2)+'\n')
receipt={'status':'Export complete; decode, loudness, picture preservation and numerical cue alignment passed.','source':str(SOURCE.relative_to(EP)),'output':str(OUTPUT.relative_to(EP)),'sha256':sha(OUTPUT),'picture_duration_sec':25.8,'previous_file_start_sec':previous_start,'file_start_sec':sting['start'],'advance_frames':6,'advance_sec':.2,'internal_impact_sec':impact,'impact_measurement':'First1ms RMS window over -24dBFS after low-level lead-in','flash_sec':292/30,'flash_frame':292,'impact_global_sec':sting['start']+impact,'impact_offset_sec':sting['start']+impact-292/30,'final_effect_correlation':corr,'measured_lufs':after['input_i'],'true_peak_dbtp':after['input_tp'],'video_packet_hash_unchanged':True,'speech_playback_rate':1,'manual_listening_claimed':False,'completed_delivery_preserved':True}
(QC/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
