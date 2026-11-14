"""Build editable teaching references from one rigid step and one loop.

This is an illustrative kinematic guide, not manufacturer CAD. It generates
local reference artwork only and never calls an image/video/audio service.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK, PAPER, ORANGE = '#1A1A2E', '#FFF8F0', '#F07B2A'
CYAN, PURPLE = '#159EAD', '#8554BA'


def bezier(a, b, c, d, count=50):
    return [tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k]
                  for k in range(2)) for t in (i/count for i in range(count+1))]


def make_geometry():
    upper = []
    for args in [((180,600),(215,600),(245,600),(280,600)),
                 ((280,600),(320,600),(340,560),(380,540)),
                 ((380,540),(507,470),(633,400),(760,330)),
                 ((760,330),(800,308),(820,300),(860,300)),
                 ((860,300),(895,300),(925,300),(960,300))]:
        upper.extend(bezier(*args)[:-1])
    upper.append((960,300))
    points = [(x,y,0.0) for x,y in upper]
    upper_count = len(points)
    for i in range(1,101):
        t=math.pi*i/100
        # Delay body rotation until it has cleared the stationary floor.
        points.append((960+110*math.sin(t),410-110*math.cos(t),t*t/math.pi))
    for x,y in reversed(upper[:-1]):
        points.append((x,y+220,math.pi))
    for i in range(1,101):
        t=math.pi*i/100
        points.append((180-110*math.sin(t),710+110*math.cos(t),math.pi+t))
    cumulative=[0.0]
    for a,b in zip(points,points[1:]):
        cumulative.append(cumulative[-1]+math.dist(a[:2],b[:2]))
    return dict(points=points,cumulative=cumulative,total=cumulative[-1],
                upper_end=cumulative[upper_count-1],step_count=28,
                roller_radius=10,turn_radius=110,trailer_offset=[-65,65],
                tread=[[-72,-20],[12,-20]],
                body=[[-72,-20],[12,-20],[12,-12],[-72,-12]],
                far_side_depth_offset=[30,-18])


G=make_geometry()


def pose(s):
    import bisect
    distance=(s%1)*G['total']
    index=min(len(G['points'])-2,max(0,bisect.bisect_right(G['cumulative'],distance)-1))
    a,b=G['points'][index:index+2]
    length=G['cumulative'][index+1]-G['cumulative'][index]
    f=(distance-G['cumulative'][index])/length if length else 0
    return tuple(a[k]+(b[k]-a[k])*f for k in range(3))


def roller_centers(s):
    x,y,t=pose(s)
    ox,oy=G['trailer_offset']
    return (x,y),(x+ox*math.cos(t)-oy*math.sin(t),y+ox*math.sin(t)+oy*math.cos(t))


def path(points):
    return 'M '+' L '.join(f'{x:.3f},{y:.3f}' for x,y in points)


def rail_points(which):
    samples=[roller_centers(i/1200)[which] for i in range(1201)]
    result=[]
    for i,p in enumerate(samples):
        a=samples[(i-1)%1200]; b=samples[(i+1)%1200]
        dx,dy=b[0]-a[0],b[1]-a[1]
        length=math.hypot(dx,dy)
        nx,ny=-dy/length,dx/length
        # Rail stroke is 3 units: its near boundary touches the 10-unit roller.
        result.append((p[0]+nx*11.5,p[1]+ny*11.5))
    return result


def step(s, color='#D9DDE0', far=False):
    x,y,t=pose(s)
    transform=f'translate({x:.3f} {y:.3f}) rotate({math.degrees(t):.3f})'
    parts=[f'<g transform="{transform}" stroke="{INK}" stroke-width="2">']
    parts.append('<polygon points="'+ ' '.join(f'{x},{y}' for x,y in G['body'])+f'" fill="{color}"/>')
    parts.append('<path d="M 12 -12 V 28" fill="none" stroke-width="4"/>')
    parts.append('<path d="M -65 65 L 0 0 L -65 -15" fill="none" stroke-width="4"/>')
    for a,b in [(0,0),G['trailer_offset']]:
        parts.append(f'<circle cx="{a}" cy="{b}" r="10" fill="{INK}"/><circle cx="{a}" cy="{b}" r="3" fill="{PAPER}"/>')
    parts.append('</g>')
    return ''.join(parts)


def text(x,y,value,size=22,color=INK):
    from html import escape
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}">{escape(value)}</text>'


def loop(phase, highlight=True):
    lines=[]
    for which,color in [(0,CYAN),(1,PURPLE)]:
        lines.append(f'<path d="{path(rail_points(which))}" stroke="{color}" fill="none" stroke-width="3"/>')
    chain=[p[:2] for p in G['points']]
    lines.append(f'<path d="{path(chain)}" stroke="{INK}" fill="none" stroke-width="4" stroke-dasharray="9 5"/>')
    for i in range(G['step_count']):
        lines.append(step(phase+i/G['step_count'],ORANGE if i==0 and highlight else '#D9DDE0'))
    # Solid stationary landing covers the run before the upper turn.
    lines.append(f'<path d="M 920 275 H 1120 V 294 H 920 Z" fill="{INK}"/>')
    lines.append(text(930,260,'stationary exit plate',18))
    return ''.join(lines)


def write_svg(name,body,view='0 0 1280 1000'):
    destination=ROOT/'references'/name
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="1000" viewBox="{view}"><rect x="-3000" y="-3000" width="6000" height="6000" fill="{PAPER}"/>{body}</svg>')


def main():
    (ROOT/'references').mkdir(parents=True,exist_ok=True)
    config={k:v for k,v in G.items() if k not in ['points','cumulative']}
    config.update(schema_version=1,scope='Illustrative rigid-body reference; not dimensioned OEM CAD',
                  loop_definition='tools/build-schematic.py: make_geometry and pose',
                  total_rollers=4,visible_near_side_rollers=2,
                  chain_count=2,chain_speed_policy='Both side chains share one shaft and route clock',
                  contact_policy='Guide rails derived from each roller center trajectory plus radius; never independently animate the rollers',
                  tracked_step_id='S17',phase_origin='0 = lower entrance, increasing toward upper exit, return underneath, lower turn',
                  ledger=[{'time_sec':t,'route_phase':.357+(1-.357)*t/38.8,'event':label} for t,label in [
                      (0,'Transfer underway; trailing foot on the still-exposed part of S17'),
                      (.8,'Entire S17 tread is under exit plate after feet clear'),
                      (5,'Scene 02 starts in hidden upper turn'),
                      (12,'Scene 02 ends early in return run'),
                      (20,'Off-screen during drive close-up; return run'),
                      (29,'Off-screen during roller view; later return run'),
                      (37,'Scene 06 starts in lower turnaround'),
                      (38.8,'S17 reappears at lower entrance'),
                      (43,'S17 continues from the entrance onto the ascending run')]],
                  clock_formula='route_phase = 0.357 + (1 - 0.357) * time_sec / 38.8; one constant arc-speed for both chains and every step',
                  timing_status='provisional illustrative clock; remap ledger to actual voice-locked cuts without reversing or resetting S17')
    (ROOT/'references/mechanism-geometry.json').write_text(json.dumps(config,indent=2)+'\n')
    body=text(55,60,'ESCALATOR — SHARED GEOMETRY / SCENE 02',30)+text(55,95,'Teaching schematic: same rigid step, paired chains, separate roller tracks.',20)
    body+=loop(.357+(1-.357)*5/38.8)
    body+=text(90,930,'S17 orange = one persistent tread. Near-side profile shows two rollers; the far pair is occluded.',20)
    body+=text(90,963,'Chain-roller rail: cyan. Trailer-roller rail: purple. Markers are editable reference annotations.',18)
    write_svg('mechanism-schematic.svg',body)
    # Derive close-ups from the same geometry, never redraw a second step.
    body=text(55,60,'SCENE 04 — TWO NEAR ROLLERS / FOUR TOTAL',28)
    a,b=roller_centers(.205)
    profile_transform=f'translate({650-3*a[0]} {300-3*a[1]}) scale(3)'
    body+=text(80,150,'Profile: far-side pair is hidden',22)
    body+='<defs><clipPath id="profile-crop"><rect x="60" y="190" width="1160" height="450"/></clipPath></defs>'
    for i,color in [(0,CYAN),(1,PURPLE)]:
        body+=f'<g clip-path="url(#profile-crop)"><g transform="{profile_transform}"><path d="{path(rail_points(i)[180:310])}" fill="none" stroke="{color}" stroke-width="3"/></g></g>'
    body+=f'<g transform="{profile_transform}">'+step(.205)+'</g>'
    body+=text(80,690,'Same step assembly in a depth diagram: two rollers on each side',22)
    for offset,opacity in [((260,260),.35),((230,278),1)]:
        body+=f'<g transform="translate({offset[0]} {offset[1]})" opacity="{opacity}">'+f'<g transform="translate({-a[0]+180} {-a[1]+500})">'+step(.205)+'</g></g>'
    body+=text(80,920,'The standing surface stays horizontal. The rigid support holds both axle positions.',21)
    write_svg('roller-profile.svg',body)
    body=text(55,60,'SCENE 05 — SAME STEP AND GUIDE GEOMETRY',28)
    body+='<g clip-path="url(#exit-crop)"><g transform="translate(-650 -100) scale(1.5)">'+loop(.340,highlight=False)+'</g></g>'
    body='<defs><clipPath id="exit-crop"><rect x="30" y="110" width="1220" height="750"/></clipPath></defs>'+body
    body+=text(70,930,'Neighboring treads align before the leading step enters the hidden turn.',22)
    write_svg('exit-transition.svg',body)
    body=text(55,60,'SCENE 06 — RETURN VIEW FROM THE SAME WORLD',28)
    body+='<g transform="matrix(.85 -.06 .10 .80 10 130)">'+loop(1.0)+'</g>'
    body+=text(70,940,'S17 is back at the lower entrance. Camera projection changes; route direction and identity do not.',20)
    write_svg('return-view.svg',body)
    body=text(55,60,'SCENE 03 — ONE CONNECTED DRIVE',28)
    body+='<rect x="110" y="190" width="180" height="100" rx="18" fill="#4F9298" stroke="#1A1A2E" stroke-width="4"/>'
    body+=text(140,250,'motor',26)+'<path d="M 290 240 H 400 V 400 H 570 L 880 350" fill="none" stroke="#1A1A2E" stroke-width="18"/>'
    body+='<rect x="350" y="200" width="100" height="95" fill="#D9DDE0" stroke="#1A1A2E" stroke-width="4"/>'+text(340,175,'gearbox',22)
    for cx,cy in [(570,400),(880,350)]:
        radius=G['turn_radius']
        body+=f'<path d="M {cx-radius} {cy} A {radius} {radius} 0 0 1 {cx+radius} {cy} L {cx-130+radius} {cy+360} A {radius} {radius} 0 0 1 {cx-130-radius} {cy+360} Z" fill="none" stroke="#1A1A2E" stroke-width="6" stroke-dasharray="12 6"/>'
        body+=f'<circle cx="{cx}" cy="{cy}" r="{radius-5}" fill="#D9DDE0" stroke="#1A1A2E" stroke-width="10" stroke-dasharray="10 7"/>'
    body+=text(475,145,'paired sprockets on shared shaft',23)
    ax,ay,_=pose(.205)
    for dx,dy in [(658,660),(348,710)]:
        body+=f'<g transform="translate({dx-ax} {dy-ay})">'+step(.205)+'</g>'
    body+='<path d="M 276 690 L 360 690 L 670 640 L 586 640 Z" fill="#D9DDE0" stroke="#1A1A2E" stroke-width="3"/>'
    body+=text(70,920,'Both side chains engage their sprockets and attach to opposite sides of the same rigid steps.',21)
    write_svg('drive-system.svg',body)
    print('Built five local SVG reference views and references/mechanism-geometry.json.')


if __name__=='__main__':
    main()
