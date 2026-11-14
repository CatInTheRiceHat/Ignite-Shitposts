"""Verify counts, cross-document dialogue, route continuity and rigid contacts."""
import importlib.util
import json
import math
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=json.loads((ROOT/'shot-plan.json').read_text())
    text=(ROOT/'higgsfield-prompts.txt').read_text()
    script=(ROOT/'script.txt').read_text()
    images=dict(re.findall(r'^BEGIN IMAGE PROMPT (I\d{2}-(?:FIRST|LAST))\n(.*?)\nEND IMAGE PROMPT \1$',text,re.M|re.S))
    videos=dict(re.findall(r'^BEGIN VIDEO PROMPT (V\d{2})\n(.*?)\nEND VIDEO PROMPT \1$',text,re.M|re.S))
    assert len(p['clips'])==6 and len(images)==12 and len(videos)==6
    assert len(re.findall(r'^BEGIN IMAGE PROMPT ',text,re.M))==12
    assert len(re.findall(r'^BEGIN VIDEO PROMPT ',text,re.M))==6
    turns=[d for c in p['clips'] for d in c['dialogue']]
    assert sum(len(d['text'].split()) for d in turns)==p['spoken_word_count']==99
    for who,name in [('Narrator','narration.txt'),('Sol','sol-dialogue.txt')]:
        assert (ROOT/name).read_text()=='\n\n'.join(d['text'] for d in turns if d['speaker']==who)+'\n'
    forbidden=r'gpt_image|kling3|start_image|end_image|image_references|Remotion|\.png|\.svg|\.json|Narrator:|Sol:|\bseconds\b'
    for block in list(images.values())+list(videos.values()):
        assert not re.search(forbidden,block), 'Settings/paths/dialogue leaked into a copyable block'
        for d in turns:
            assert d['text'] not in block
    previous=0
    for c in p['clips']:
        sid=c['id']
        assert c['start_sec']==previous and c['end_sec']>previous
        previous=c['end_sec']
        for key in ['FIRST','LAST']: assert f'I{sid}-{key}' in images
        assert 'V'+sid in videos
        assert c['first_frame'] in script and c['last_frame'] in script
        for d in c['dialogue']:
            line=d['speaker']+': “'+d['text']+'”'
            assert line in text and line in script
        for name in c['reference_views']:
            assert (ROOT/name).is_file(),name
    assert previous==43 and p['timing_status'].startswith('provisional')
    assert p['clips'][1]['performance_beats'][-1]['eye_shape']=='tracking'
    assert sum(b['eye_shape']=='listening_up' for b in p['clips'][1]['performance_beats'])==1
    for sid in ['03','06']:
        c=next(c for c in p['clips'] if c['id']==sid)
        assert 'locked' in c['video_prompt'].lower() and 'push' not in c['video_prompt'].lower()
    assert 'two rollers' in p['clips'][3]['first_frame'] and 'four total' in p['clips'][3]['first_frame']
    geometry=json.loads((ROOT/'references/mechanism-geometry.json').read_text())
    assert geometry['visible_near_side_rollers']==2 and geometry['total_rollers']==4
    assert geometry['chain_count']==2
    ledger=p['tracked_object']['ledger']
    assert ledger==geometry['ledger']
    assert all(a['time_sec']<b['time_sec'] and a['route_phase']<b['route_phase'] for a,b in zip(ledger,ledger[1:]))
    spec=importlib.util.spec_from_file_location('schematic',ROOT/'tools/build-schematic.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    span=math.hypot(*m.G['trailer_offset'])
    rails=[m.rail_points(0),m.rail_points(1)]
    for i in range(1200):
        phase=i/1200;a,b=m.roller_centers(phase)
        assert abs(math.dist(a,b)-span)<1e-8, 'Rigid axle offsets changed'
        if phase<m.G['upper_end']/m.G['total']: assert abs(m.pose(phase)[2])<1e-10
        for which,center in enumerate([a,b]):
            # Rail center is 10-unit roller radius + half its 3-unit stroke away.
            rail=rails[which][i]
            assert abs(math.dist(center,rail)-11.5)<1e-7
    # At the first-second target the whole tread, not merely its front axle,
    # has passed under the exit plate at world x=920.
    x,y,angle=m.pose(ledger[1]['route_phase'])
    leftmost=min(x+a*math.cos(angle)-b*math.sin(angle) for a,b in m.G['tread'])
    assert ledger[1]['time_sec']<=1 and leftmost>=920
    caps=json.loads((ROOT/'references/model-capabilities.json').read_text())['models']
    model=caps['kling3_0']; roles={r for media in model['medias'] for r in media['roles']}
    assert {'start_image','end_image'}<=roles
    duration=next(x for x in model['parameters'] if x['name']=='duration')
    assert all(duration['min']<=c['end_sec']-c['start_sec']<=duration['max'] for c in p['clips'])
    cues=json.loads((ROOT/'audio/voice-cues.plan.json').read_text())
    assert not cues['confirmed'] and all(x['measured_start_sec'] is None for x in cues['utterances'])
    assert [(x['speaker'],x['text']) for x in cues['utterances']]==[(x['speaker'],x['text']) for x in turns]
    cast=json.loads((ROOT.parents[1]/'config/voices.json').read_text())['speakers']
    assert cast['Sol']['voice_id']==p['speakers']['Sol']['voice_id'] and cast['Sol']['voice_type']=='element'
    assert p['speakers']['Narrator']['voice_id'] is None
    report={'status':'passed planning and analytic geometry checks','scenes':6,'image_prompts':12,'video_prompts':6,'spoken_words':99,'provisional_seconds':43,
            'geometry_samples':1200,'checks':['matching dialogue and frame states','clean standalone prompt blocks','one Scene 02 upward glance','edit-only camera pushes','four rollers / two visible','constant rigid roller offsets and derived rail tangency','monotonic S17 route, including off-screen cuts','whole tread under plate within first second','compatible model inputs and durations','unconfirmed voice cue map'],
            'not_yet_verified':['generated painted frames at phone size','actual foot contact and shadows in generated footage','actual voice timings and caption cues','Arthur exact preset ID','final rendered caption treatment and social-control clearance'],
            'generation_jobs_submitted':0}
    (ROOT/'handoff-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
