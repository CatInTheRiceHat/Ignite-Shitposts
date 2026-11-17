"""Remove reviewed video artifacts using same-take background and short paired holds."""
import hashlib
import argparse
import json
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image

EP = Path(__file__).resolve().parents[1]
import cv2

REV = EP / 'revisions/christmas-fireplace-v4'
SOURCE = REV / 'clips/01-scene.mp4'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=REV/'clips/01-scene-clean-v6.mp4')
parser.add_argument('--review-dir',type=Path,default=REV/'reviews/cleanup-v6')
parser.add_argument('--settle-hold',action='store_true',help='Use clean complete poses through the reviewed ribbon/particle overlap')
args=parser.parse_args()
OUTPUT = args.output
QC = args.review_dir
QC.mkdir(exist_ok=True)
if OUTPUT.exists(): raise FileExistsError(OUTPUT)
W,H = 1080,1920
SIZE = W*H*3//2
raw = subprocess.check_output(['ffmpeg','-v','error','-nostdin','-i',str(SOURCE),
    '-vf',r'select=not(mod(n\,2))','-fps_mode','passthrough',
    '-pix_fmt','yuv420p','-f','rawvideo','-'])
assert len(raw) == 45*SIZE
states = np.frombuffer(raw,np.uint8).reshape(45,SIZE)

# These two boxes follow the independent review's observed detached trajectories.
# Current Sol pixels are protected, including the moving tip at the lower edge.
def artifact_box(frame):
    first={24:(432,1082,464,1154),26:(436,1046,466,1124),28:(438,1014,468,1088),
           30:(438,992,466,1062),32:(436,960,464,1022),34:(436,960,466,1022),
           36:(432,936,462,990),38:(432,902,460,952),40:(438,880,464,924),
           42:(448,866,464,886),44:(448,866,464,886)}
    if frame in first:
        x,y,r,b=first[frame]
        return (x-6,y-6,r+6,b+6)
    second={48:(356,1080,412,1144),50:(364,1060,414,1134),52:(374,1042,418,1118),
            54:(374,1040,418,1118),56:(382,1028,420,1094),58:(386,1016,420,1070),
            60:(392,1008,420,1048)}
    if frame in second: return second[frame]
    return None

def core_blocks(frame):
    path=REV/'reviews/independent-native-v6'/f'01-f{frame:03d}.png'
    rgb=np.asarray(Image.open(path).convert('RGB'))
    hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV)
    mask=((hsv[:,:,0]<20)&(hsv[:,:,1]>160)&(hsv[:,:,2]>65)).astype(np.uint8)
    count,labels,stats,_=cv2.connectedComponentsWithStats(mask,connectivity=4)
    votes=np.bincount(labels[1370:1560,400:650].ravel(),minlength=count);votes[0]=0
    main=int(votes.argmax());assert votes[main]>200
    core=(labels==main).astype(np.uint8)
    # Fill the interior and protect a two-pixel edge around the original silhouette.
    inv=1-core;flood=inv.copy();cv2.floodFill(flood,None,(0,0),2)
    core |= (flood==1).astype(np.uint8)
    core=cv2.dilate(core,np.ones((5,5),np.uint8))
    return core.reshape(H//2,2,W//2,2).any(axis=(1,3))

donor_frames=[0,20,62,88,18,64,66,68,70,72,74,76,78,80,82,84,86]
donor_frames += [f for f in range(0,90,2) if f not in donor_frames and f not in (22,46,52,54)]
cores={f:core_blocks(f) for f in sorted(set(donor_frames+list(range(24,46,2))+list(range(48,62,2))))}

def planes(buf):
    y=buf[:W*H].reshape(H,W)
    u=buf[W*H:W*H+W*H//4].reshape(H//2,W//2)
    v=buf[W*H+W*H//4:].reshape(H//2,W//2)
    return y,u,v

cleaned={}
repairs=[]
holds=({22:20,24:20,**{f:62 for f in range(42,62,2)}} if args.settle_hold
       else {22:20,46:44,52:50,54:50})
selected_states={holds.get(f,f) for f in range(0,90,2)}
for frame in range(0,90,2):
    if frame not in selected_states:continue
    original=states[frame//2]
    box=artifact_box(frame)
    if box is None:
        cleaned[frame]=original
        continue
    x,y,r,b=box
    wanted=np.zeros((H//2,W//2),bool);wanted[y//2:b//2,x//2:r//2]=True
    wanted &= ~cores[frame]
    remaining=wanted.copy();dst=original.copy();dy,du,dv=planes(dst);used=[]
    for donor in donor_frames:
        valid=remaining & ~cores[donor]
        bad=artifact_box(donor)
        if bad:
            bx,by,br,bb=bad
            valid[by//2:bb//2,bx//2:br//2]=False
        if not valid.any(): continue
        sy,su,sv=planes(states[donor//2]);full=np.repeat(np.repeat(valid,2,axis=0),2,axis=1)
        dy[full]=sy[full];du[valid]=su[valid];dv[valid]=sv[valid]
        remaining[valid]=False;used.append(donor)
        if not remaining.any():break
    assert not remaining.any(),(frame,int(remaining.sum()))
    # No changes to Sol's protected shape, face, limbs, or any pixel outside the box.
    oy,ou,ov=planes(original);fullwanted=np.repeat(np.repeat(wanted,2,axis=0),2,axis=1)
    assert np.array_equal(dy[~fullwanted],oy[~fullwanted])
    assert np.array_equal(du[~wanted],ou[~wanted]) and np.array_equal(dv[~wanted],ov[~wanted])
    cleaned[frame]=dst
    repairs.append({'source_pair':frame,'box':box,'background_donors':used,'protected_body_pixels_changed':0})

# Complete-pair source holds retain the original poses without redrawing the character.
mapping=[]
enc=subprocess.Popen(['ffmpeg','-v','error','-nostdin','-n','-f','rawvideo','-pix_fmt','yuv420p',
    '-s','1080x1920','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-qp','0',
    '-g','1','-bf','0','-movflags','+faststart',str(OUTPUT)],stdin=subprocess.PIPE)
expected=[]
for frame in range(0,90,2):
    selected=holds.get(frame,frame);data=cleaned[selected].tobytes()
    for _ in range(2):enc.stdin.write(data);expected.append(hashlib.md5(data).hexdigest())
    mapping.extend([selected,selected+1])
enc.stdin.close();assert enc.wait()==0
md5=subprocess.check_output(['ffmpeg','-v','error','-nostdin','-i',str(OUTPUT),'-pix_fmt','yuv420p','-f','framemd5','-'],text=True)
actual=[line.rsplit(',',1)[1].strip() for line in md5.splitlines() if line and not line.startswith('#')]
assert actual==expected
assert all(actual[i]==actual[i+1] for i in range(0,90,2))
assert actual[0]==hashlib.md5(states[0].tobytes()).hexdigest()
assert actual[-1]==hashlib.md5(states[-1].tobytes()).hexdigest()
report={'source':str(SOURCE),'output':str(OUTPUT),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'output_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),'frames':90,'duration_sec':3,
    'paired_holds':holds,'source_frame_mapping':mapping,'background_repairs':repairs,
    'decoded_output_matches_selected_and_repaired_yuv_exactly':True,'pair_mismatches':[],
    'first_and_last_source_frames_unchanged':True,
    'method':'Local same-take static-background replacement outside protected Sol silhouette. Complete-pair source holds remove reviewed emission/mouth states; settle mode also excludes ribbon-overlap states42–60. No redraw, interpolation, optical flow, speed change or audio edits.',
    'visual_review':'pending fresh independent review'}
(QC/'repair.json').write_text(json.dumps(report,indent=2)+'\n');(QC/'output.framemd5').write_text(md5)
print(json.dumps({'output':str(OUTPUT),'frames':90,'background_repaired_states':len(repairs),'paired_holds':holds}),flush=True)
