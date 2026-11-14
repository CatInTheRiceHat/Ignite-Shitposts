"""Synchronize review documents and clean voice scripts from shot-plan.json."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def rebuild():
    p=json.loads((ROOT/'shot-plan.json').read_text())
    turns=[d for c in p['clips'] for d in c['dialogue']]
    for speaker,name in [('Narrator','narration.txt'),('Sol','sol-dialogue.txt')]:
        (ROOT/name).write_text('\n\n'.join(d['text'] for d in turns if d['speaker']==speaker)+'\n')
    lines=['HOW DOES AN ESCALATOR WORK?','Complete script and storyboard','',
           f"Revision {p['revision']}: {p['spoken_word_count']} spoken words; six scenes; exactly 12 image and six video prompts.",
           p['timing_note'],'','CAST AND PROJECT DECISIONS']
    for name,voice in p['speakers'].items():
        lines.extend([name+': '+voice['voice']+' / '+voice['provider']+' / '+voice['performance'],
                      'Voice identity: '+str(voice.get('voice_id'))+'; '+voice.get('voice_type',''),
                      voice.get('decision_note',voice.get('voice_id_status','')),''])
    lines.extend(['SETTING',p['staging'],'','NARRATOR EYELINE',p['composition_rules']['narrator_eyeline'],
                  '', 'SCHEMATIC AND ORIGINAL TREAD',p['tracked_object']['route_note'],
                  'The original tread is S17; the reference geometry and route ledger are in references/mechanism-geometry.json.',''])
    for row in p['tracked_object']['ledger']:
        lines.append(f"{row['time_sec']}s provisional: route phase {row['route_phase']}; {row['event']}.")
    for c in p['clips']:
        lines.extend(['',f"SCENE {c['id']} | {c['start_sec']}–{c['end_sec']} seconds PROVISIONAL",'',
                      'Scene: '+c['setting_and_framing'],'Camera: '+c['camera']['height_and_angle'],
                      'Composition: '+c['camera']['composition'],'Camera movement: '+c['camera']['movement'],
                      '', 'FIRST FRAME — FINISHED COMPOSITE',c['first_frame'],'','DIALOGUE'])
        lines.extend(d['speaker']+': “'+d['text']+'”' for d in c['dialogue'])
        lines.extend(['','ACTION / SPOKEN BEATS',c['action']])
        for beat in c['performance_beats']:
            lines.append(beat['cue']+': '+beat['body']+' Eyes: '+beat['eye_shape']+'. Gaze: '+beat['gaze'])
        lines.extend(['','LAST FRAME — FINISHED COMPOSITE',c['last_frame'],
                      'Next cut: '+c['next_cut'],
                      'Prepared technical references: '+(', '.join(c['reference_views']) or 'Opening character/landing art; no technical cutaway.'),
                      'Phone review target: '+p['phone_review']['criteria'][c['id']]])
    lines.extend(['','VOICE-FIRST TIMING AND FINISHING',p['timing_note'],
                  'Export 1080 × 1920 at 30 fps. Character poses may use a roughly 12 fps stepped feel; keep technical motion and camera moves smooth.',
                  'Captions: Ramento, local family Rammetto One; white #FFFFFF, Ignite orange glyph outline #F07B2A, one or two editable lines. Font source: '+p['finishing']['font_source'],
                  p['composition_rules']['captions'],
                  'Keep captions, arrows, track colors, orange S17 highlight, contact halos and sound effects editable. Sol and Arthur remain separate audio tracks.',
                  'Existing Remotion setup: '+p['finishing']['existing_remotion'],
                  'Assembly gap: '+p['finishing']['renderer_gap'],
                  '', 'GENERATION ORDER']+p['generation_order']+['','RELATED EPISODE FILES',
                  'higgsfield-prompts.txt — 12 self-contained still-image blocks and six motion blocks.',
                  'scene-01-test-plan.txt — first test and pass/fail criteria; no jobs submitted.',
                  'references/mechanism-geometry.json and the five matching SVG/PNG views — shared geometry and route clock.',
                  'handoff.txt — assumptions, remaining checks and exact file inventory.'])
    (ROOT/'script.txt').write_text('\n'.join(lines).rstrip()+'\n')
    lines=['HOW DOES AN ESCALATOR WORK?','Higgsfield prompt review draft','',
           'Six scenes. Exactly 12 standalone image prompts and six standalone video prompts.',
           f"Revision {p['revision']}; {p['spoken_word_count']} spoken words. 43 seconds is provisional, not voice-locked.",
           '', 'SETTINGS — OUTSIDE ALL COPYABLE BLOCKS',
           'Images: gpt_image_2_6; quality high; resolution 2k; PNG; 9:16; one output per block; image_references role.',
           'Video: kling3_0; mode std; sound off; 9:16; proposed durations 5, 7, 8, 9, 8, 6 seconds. start_image and end_image both required by this plan.',
           'These settings were checked against the connected catalog during this revision. All proposed durations fit its 3–15 whole-second range. Recheck before later submission.',
           'Sol: custom Sol / voice_id 68b3ae01-976b-4d18-995f-3d60c00d0b55 / voice_type element. Arthur: built-in preset; exact ID unresolved in available project records. Separate audio tracks at normal speech rate and 1x playback.',
           '', 'REFERENCES AND ORDER',
           'Existing Sol identity: assets/sol-full-body.png. Existing paint style: assets/calculus-painted-scene.jpg. Actual current Remotion install: remotion/.',
           'The five technical reference PNGs and matching editable SVGs in references/ are locally prepared teaching schematics, not generated production frames or OEM CAD. Review their conceptual geometry before using them in Scene 02.',
           'First-frame and last-frame outputs below are planned, not yet generated. Create Scene 01 first; validate grounded action and the exact disappearing tread. Before Scene 02, review the shared schematic; use its matching drive, roller, exit and return views for later scenes.',
           'For each last frame, use its approved first frame as the primary composition reference; references and media IDs belong to request fields, not the prompt text. Upload actual files to obtain media IDs at generation time.',
           'Both raw endpoints use the clean source camera. Scene 03 and 06 camera pushes are added in Remotion, not baked into either endpoint or generated video.',
           '', 'CLEAN FOOTAGE AND EDIT LAYERS',
           'Copyable blocks request neutral clean art. Orange S17 tracking, cyan/purple tracks, reference lines, arrows, halos, captions and sound effects stay outside generation and remain editable in Remotion. The script describes the finished composite; these prompts describe its clean source.',
           'Use the single S17 ledger even off-screen. Use controlled Remotion geometry wherever generated motion loses a contact, chain engagement, rigid shape or tracked identity.',
           'The generated footage is silent. Dialogue below is timing context only, never text for visual-generation prompts. Record takes before locking cuts, overlay timings and optional reactions.']
    for c in p['clips']:
        sid=c['id']
        lines.extend(['',f"SCENE {sid} | {c['start_sec']}–{c['end_sec']} seconds PROVISIONAL",'', 'Dialogue context:'])
        lines.extend(d['speaker']+': “'+d['text']+'”' for d in c['dialogue'])
        lines.extend(['','Existing identity/style inputs: '+(', '.join(c['identity_references']) or 'Paint style only.'),
                      'Prepared mechanism inputs: '+(', '.join(c['reference_views']) or 'None for the opening test.'),
                      'Continuity: '+c['next_cut']])
        for frame in ['first','last']:
            label=f'I{sid}-{frame.upper()}'
            lines.extend(['',f'Planned output: keyframes/{sid}-{frame}.png',
                          'Additional reference input: '+(f'approved keyframes/{sid}-first.png as primary composition' if frame=='last' else c['previous_reference']),
                          '',f'BEGIN IMAGE PROMPT {label}',c['image_prompts'][frame],f'END IMAGE PROMPT {label}'])
        lines.extend(['',f'Video inputs: approved keyframes/{sid}-first.png as start_image and keyframes/{sid}-last.png as end_image.',
                      f"Video settings: kling3_0; mode std; sound off; 9:16; duration {c['end_sec']-c['start_sec']} seconds, pending actual voice timing.",
                      f'Planned output: clips/{sid}-scene.mp4','',f'BEGIN VIDEO PROMPT V{sid}',c['video_prompt'],f'END VIDEO PROMPT V{sid}',
                      '', 'Remotion / performance notes: '+c['action']])
    lines.extend(['','MECHANISM SOURCES'])
    for s in p['sources']:
        lines.extend([s['title'],s['url'],s['supports']])
    (ROOT/'higgsfield-prompts.txt').write_text('\n'.join(lines).rstrip()+'\n')
    print('Rebuilt script.txt, narration.txt, sol-dialogue.txt and higgsfield-prompts.txt from the canonical plan.')


if __name__=='__main__':
    rebuild()
