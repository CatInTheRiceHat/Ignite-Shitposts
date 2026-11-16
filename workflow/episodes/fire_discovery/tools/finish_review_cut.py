import json,subprocess,hashlib,re,sys
from pathlib import Path
p=Path(__file__).resolve().parents[1];renders=p/'renders'
v2=True
src=renders/('fire-discovery-resumed-v3-draft.mp4' if v2 else 'fire-discovery-draft.mp4');out=renders/('fire-discovery-resumed-v3-review.mp4' if v2 else 'fire-discovery-with-sound-draft.mp4')
expected_duration=716/30
assert src.is_file(),src
assert not out.exists(),'Preserve existing finished cut; choose a new version before rerunning.'
measure=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-i',str(src),'-vn','-af','loudnorm=I=-16:LRA=11:TP=-1.5:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
m=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',measure.stderr,re.S)[-1])
af=('loudnorm=I=-16:LRA=11:TP=-1.5:linear=true:measured_I='+m['input_i']+':measured_LRA='+m['input_lra']+':measured_TP='+m['input_tp']+':measured_thresh='+m['input_thresh']+':offset='+m['target_offset'])
subprocess.run(['ffmpeg','-v','error','-nostdin','-i',str(src),'-map','0:v:0','-map','0:a:0','-c:v','copy','-af',af,'-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(out)],check=True)
subprocess.run(['ffmpeg','-v','error','-nostdin','-i',str(out),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert v['width']==1080 and v['height']==1920 and v['avg_frame_rate']=='30/1'
assert abs(float(probe['format']['duration'])-expected_duration)<.04
assert a['codec_name']=='aac' and a['sample_rate']=='48000'
finalmeasure=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-i',str(out),'-vn','-af','loudnorm=I=-16:LRA=11:TP=-1.5:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
lm=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',finalmeasure.stderr,re.S)[-1]);assert float(lm['input_tp']) < -.9
qc=renders/('full-cut-review-v3' if v2 else 'full-cut-review-v1');qc.mkdir(exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-nostdin','-i',str(out),'-vf','fps=2,scale=180:320,tile=6x4','-frames:v','3',str(qc/'sequence-%02d.jpg')],check=True)
times=([.5,1.5,2.1,3.1333,3.8333,4.8333,5.8333,6.7333,7.7,9.7333,10.3,12.5,13.6,15.8,17.4,19.2,20.1333,21.4,22.1,23.2,23.4,23.6,23.8] if v2 else [.5,1.5,3.8,4.5,6,7.2,9.7,10.6,12.8,14.8,18.7,20.7,23.5,24.5,27.8,29.5,31.1,32.5])
for i,t in enumerate(times):
 subprocess.run(['ffmpeg','-v','error','-nostdin','-ss',str(t),'-i',str(out),'-frames:v','1',str(qc/f'detail-{i+1:02d}-{t:g}s.jpg')],check=True)
edit=json.loads((p/'edit-resume-v3.json').read_text())
report={'status':'complete review draft; independent clip/final visual approval required','output':str(out.relative_to(p)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'duration_sec':float(probe['format']['duration']),'dimensions':[1080,1920],'fps':30,'audio':{'codec':'aac','sample_rate':48000,'measured_lufs':lm['input_i'],'true_peak_dbtp':lm['input_tp'],'dialogue_playback_rate':1,'exact_voice_config':'workflow/config/voices.json','voice_takes':7,'music':'Hide and Sneak 4.mp3','source_audio_hashes_preserved':True},'source_clips':[{'scene':s['id'],'src':s['scene']['src'],'sha256':hashlib.sha256((p/'public'/s['scene']['src']).read_bytes()).hexdigest()} for s in edit['shots']],'verification':{'full_audio_video_decode':'passed','source_state_twos':'Each conformed source separately verified; planned smooth editorial pushes and editable captions are separate.','manual_audio_playback_claimed':False,'final_visual_review':'pending'},'native_details':[f'detail-{i+1:02d}-{t:g}s.jpg' for i,t in enumerate(times)],'sequence_sheets':[f'sequence-{i:02d}.jpg' for i in range(1,4)]}
(qc/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'output':str(out.resolve()),'bytes':report['bytes'],'audio':report['audio'],'qc':str(qc.resolve())},indent=2))
