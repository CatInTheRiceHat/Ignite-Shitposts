import sys,json,subprocess,hashlib
from pathlib import Path
sys.path.insert(0,'workflow/.cache/cv2-vendor')
import cv2,numpy as np
from PIL import Image
p=Path(__file__).resolve().parents[1];review=p/'reviews/particle-removal-native-v2';review.mkdir(exist_ok=True);W,H=1080,1920;X,Y,R,B=70,420,560,900
def stream(src):
 q=subprocess.Popen(['ffmpeg','-v','error','-nostdin','-i',str(src),'-vf','select=not(mod(n\\,2))','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 for i in range(90):
  data=q.stdout.read(W*H*3);assert len(data)==W*H*3
  yield i,np.frombuffer(data,np.uint8).reshape(H,W,3)
 q.stdout.close();assert q.wait()==0
def analyze(im):
 a=im[Y:B,X:R].astype(np.int16);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2];red=((r>95)&((r-g)>6)&((r-b)>10)).astype('uint8')
 count,labels,stats,cent=cv2.connectedComponentsWithStats(red,connectivity=4);main=1+np.argmax(stats[1:,cv2.CC_STAT_AREA]);core=(labels==main).astype('uint8')
 # Close only interior holes, preserving the exact actual outer body contour.
 holes=core.copy();flood=np.zeros((core.shape[0]+2,core.shape[1]+2),np.uint8);cv2.floodFill(holes,flood,(0,0),1);core=core|(~holes.astype(bool)).astype('uint8');core=cv2.dilate(core,np.ones((3,3),np.uint8))
 top=stats[main,cv2.CC_STAT_TOP];bottom=top+stats[main,cv2.CC_STAT_HEIGHT];mask=np.zeros_like(core);boxes=[]
 for n in range(1,count):
  x,y,w,h,area=stats[n]
  if n!=main and area>=1 and y<(top+bottom)/2:
   mask[labels==n]=1;boxes.append([int(x+X),int(y+Y),int(w),int(h),int(area)])
 return core,mask,boxes
for scene in ['02','05']:
 src=p/'clips'/f'{scene}-scene-omni-v6-particle-free-native-v1.mp4';out=p/'clips'/f'{scene}-scene-omni-v6-particle-free-native-v2.mp4';assert not out.exists(),out
 states=[];refs={};refids=[0,5,10,20,30,40,50,60,70,75,80,85,89]
 for i,im in stream(src):
  states.append(analyze(im))
  if i in refids:refs[i]=im.copy()
 original=[s[1].copy() for s in states]
 for i,(core,mask,boxes) in enumerate(states):
  mask=mask.copy()
  for k in [1,2,3]:
   if i>=k:mask|=cv2.warpAffine(original[i-k],np.float32([[1,0,0],[0,1,-k*2]]),(R-X,B-Y))
  mask=cv2.dilate(mask,np.ones((9,9),np.uint8));states[i]=(core,mask,boxes)
 print(scene,'native isolated states',sum(bool(s[1].any()) for s in states),flush=True)
 enc=subprocess.Popen(['ffmpeg','-v','error','-nostdin','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-an','-frames:v','180','-c:v','libx264','-preset','fast','-qp','18','-g','1','-bf','0','-x264-params','aq-mode=0:mbtree=0:scenecut=0','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 repairs=[]
 for i,im in stream(src):
  core,m,boxes=states[i];clean=im
  alpha=cv2.GaussianBlur(m.astype(np.float32),(5,5),.7);alpha[core>0]=0;alpha[900-Y:]=0;need=alpha>0
  if need.any():
   donor=np.zeros((B-Y,R-X,3),np.uint8);missing=need.copy();used=[]
   for j in sorted(refs,key=lambda j:abs(j-i)):
    fg=states[j][0]|states[j][1];valid=missing&~fg.astype(bool)
    if valid.any():donor[valid]=refs[j][Y:B,X:R][valid];missing[valid]=False;used.append(j*2)
   count=int(missing.sum())
   if count:
    by,bx=np.where(~need&~core.astype(bool));assert len(bx)
    for y,x in zip(*np.where(missing)):
     j=np.argmin((by-y)**2+(bx-x)**2);donor[y,x]=im[Y+by[j],X+bx[j]]
   clean=im.copy();old=im[Y:B,X:R];new=np.round(old*(1-alpha[:,:,None])+donor*alpha[:,:,None]).astype('uint8');assert np.array_equal(old[core>0],new[core>0]);clean[Y:B,X:R]=new
   assert np.array_equal(im[900:],clean[900:]);repairs.append(dict(frames=[i*2,i*2+1],time_sec=i/15,boxes_native=boxes,changed_pixels=int(np.any(new!=old,axis=2).sum()),protected_native_body_pixels_changed=0,face_changed=0,donors=used,adjacent_background_pixels=count))
   if i in [10,20,34,50,60,61,62,63,64,65,66,11,21,22]:Image.fromarray(im).save(review/f'{scene}-{i*2:03d}-before.jpg');Image.fromarray(clean).save(review/f'{scene}-{i*2:03d}-after.jpg')
  enc.stdin.write(clean.tobytes());enc.stdin.write(clean.tobytes())
 enc.stdin.close();assert enc.wait()==0
 r=subprocess.check_output(['ffmpeg','-v','error','-i',str(out),'-f','framemd5','-'],text=True);hs=[l.split(',')[-1].strip() for l in r.splitlines() if l and not l.startswith('#')];assert len(hs)==180 and all(hs[j]==hs[j+1] for j in range(0,180,2))
 (review/f'{scene}-native-particle-removal.json').write_text(json.dumps({'source':str(src.relative_to(p)),'output':str(out.relative_to(p)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'method':'Native1080p warm-color isolation includes faint red trails omitted by the previous high-saturation threshold. Restore isolated background contaminants above the upper-body midpoint from same-take background. Preserve the current main silhouette and every pixel below900, including face and limbs. Three-state fading masks; normal source speed, exact pairs. Does not fix attached emission buds; those are excluded by a separate complete-pair editorial selection.','repairs':repairs,'decoded_pair_mismatches':[],'review':'pending actual native visual inspection'},indent=2)+'\n');print(scene,'native cleanup complete',len(repairs),flush=True)
