import subprocess, json, hashlib
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
root=Path('workflow/episodes/fire_discovery'); out=root/'reviews/resume-native-v1/selected-v3';out.mkdir(exist_ok=True)
manifest={}
for scene in ['02','05']:
 src=root/f'clips/edit-v3/{scene}-clean-holds-v3.mp4'
 p=subprocess.Popen(['ffmpeg','-v','error','-i',str(src),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 kept=[]; hashes=[]; n=0
 while True:
  b=p.stdout.read(1080*1920*3)
  if not b:break
  hashes.append(hashlib.sha256(b).hexdigest())
  if n%2==0:
   im=Image.frombytes('RGB',(1080,1920),b)
   im.crop((100,530,650,1280)).save(out/f'{scene}-{n:03}-sol.png')
   if n in [0,20,22,24,36,38,40,42,44,46,48,50,60,62,64,66,68,70,96,98,100,102,112,114,116,118,120,124,126,128,130,132,140,142,166,168,170,178]:im.save(out/f'{scene}-{n:03}-full.png')
   kept.append((n,im))
  n+=1
 p.wait()
 sheets=[]
 for start in range(0,len(kept),24):
  part=kept[start:start+24]; sheet=Image.new('RGB',(6*275,4*400),'#222222'); d=ImageDraw.Draw(sheet)
  for j,(n,im) in enumerate(part):
   small=im.crop((100,530,650,1280)).resize((275,375))
   x=(j%6)*275;y=(j//6)*400
   sheet.paste(small,(x,y+25));d.text((x+6,y+5),f'{scene} f{n} {n/30:.3f}s',fill='white')
  name=f'{scene}-sequence-{start//24:02}.jpg';sheet.save(out/name,quality=95);sheets.append(name)
 manifest[scene]={'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'frames':len(hashes),'pair_mismatches':[i for i in range(0,len(hashes),2) if hashes[i]!=hashes[i+1]],'sheets':sheets}
(out/'extraction.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
