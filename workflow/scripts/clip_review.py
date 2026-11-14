"""Evidence preparation and approval gates; never a vision model or generator.

The user approves frame pairs. An independent reviewer inspects actual footage.
This module binds those decisions to exact files, references and shot contracts.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageOps
from paths import WORKFLOW, episode_path

ROOT = WORKFLOW.parent
POLICY = WORKFLOW / 'config/clip-review.json'
SCENE_FIELDS = ('id', 'first_frame', 'last_frame', 'action', 'framing_prompt',
                'camera', 'dialogue', 'performance_beats', 'sol_visible',
                'image_prompts', 'video_prompt', 'start_sec', 'end_sec')


def read(path):
    return json.loads(Path(path).read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False).encode()).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as out:
        json.dump(data, out, indent=2, ensure_ascii=False)
        out.write('\n')
        temporary = Path(out.name)
    temporary.replace(path)


def resolve(episode, value):
    path = Path(value)
    choices = [path] if path.is_absolute() else [episode / path, ROOT / path, WORKFLOW / path]
    for candidate in choices:
        if candidate.is_file():
            return candidate.resolve()
    raise ValueError('Missing review input: ' + str(choices[0]))


def entry(path):
    path = Path(path).resolve()
    return {'path': str(path.relative_to(ROOT)), 'sha256': file_hash(path)}


def context(episode, scene_id, stage, clip=None, first=None, last=None):
    episode = Path(episode).resolve()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', str(scene_id)):
        raise ValueError('Invalid scene ID')
    policy = read(POLICY)
    plan = read(episode / 'shot-plan.json')
    scene = next((c for c in plan['clips'] if c['id'] == scene_id), None)
    if scene is None:
        raise ValueError('Scene not found: ' + scene_id)
    outputs = scene.get('planned_outputs', {})
    overrides = {'first': first, 'last': last}
    sources = {key: resolve(episode, overrides[key] or outputs.get(key, f'keyframes/{scene_id}-{key}.png'))
               for key in ('first', 'last')}
    reference = plan.get('art_direction_reference', {})
    # Require the selected sources; do not quietly substitute the old flat mascot.
    reference_paths = {key: resolve(episode, reference[key]) for key in ('still', 'motion')}
    contract = {'policy': policy,
                'scene': {key: scene[key] for key in SCENE_FIELDS if key in scene},
                'style': {key: value for key, value in reference.items()
                          if key not in ('generation_status',)},
                'composition_rules': plan.get('composition_rules', {})}
    binding = {'scene': scene_id, 'stage': stage, 'contract_sha256': digest(contract),
               'frames': {key: entry(path) for key, path in sources.items()},
               'references': {key: entry(path) for key, path in reference_paths.items()}}
    if stage == 'clip':
        sources['clip'] = resolve(episode, clip or outputs.get('video', f'clips/{scene_id}-scene.mp4'))
        binding['clip'] = entry(sources['clip'])
    packet_id = digest(binding)
    directory = episode / 'reviews' / scene_id / stage / packet_id[:20]
    return {'episode': episode, 'scene': scene, 'policy': policy, 'contract': contract,
            'binding': binding, 'packet_id': packet_id, 'directory': directory,
            'sources': sources, 'reference_paths': reference_paths}


def tool(name):
    value = os.environ.get(name.upper() + '_PATH') or shutil.which(name)
    if not value:
        raise ValueError(name + ' is required for actual clip review')
    return value


def run(args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise ValueError('Review extraction failed: ' + result.stderr[-2000:])
    return result.stdout


def picture(source, target, size=(360, 640)):
    with Image.open(source) as source_image:
        image = ImageOps.exif_transpose(source_image).convert('RGB')
        image.thumbnail(size)
        image.save(target, quality=95)


def sheet(items, output, columns=4, size=(180, 320)):
    rows = math.ceil(len(items) / columns)
    canvas = Image.new('RGB', (columns * size[0], rows * (size[1] + 25)), '#FFF8F0')
    draw = ImageDraw.Draw(canvas)
    for index, (path, label) in enumerate(items):
        with Image.open(path) as source:
            image = ImageOps.contain(source.convert('RGB'), size)
            x, y = index % columns * size[0], index // columns * (size[1] + 25)
            canvas.paste(image, (x + (size[0] - image.width) // 2, y))
            draw.text((x + 5, y + size[1] + 5), label, fill='#1A1A2E')
    canvas.save(output, quality=94)


def prepare(episode, scene_id, stage, clip=None, first=None, last=None):
    ctx = context(episode, scene_id, stage, clip, first, last)
    directory = ctx['directory']
    existing = directory / 'packet.json'
    if existing.is_file():
        packet = read(existing)
        if packet.get('binding') == ctx['binding'] and all(
                (directory / item).is_file() for item in packet.get('evidence', [])):
            return {'packet': str(existing), 'request': str(directory / 'review-request.txt'),
                    'status': 'prepared; not approved'}
    directory.mkdir(parents=True, exist_ok=True)
    evidence = directory / 'evidence'
    evidence.mkdir(exist_ok=True)
    for label, source in {'reference': ctx['reference_paths']['still'],
                          'first': ctx['sources']['first'], 'last': ctx['sources']['last']}.items():
        picture(source, evidence / (label + '.jpg'), (720, 1280))
    sheet([(evidence / (label + '.jpg'), label.upper())
           for label in ('reference', 'first', 'last')], evidence / 'frame-comparison.jpg',
          columns=3, size=(360, 640))
    coverage = {}
    technical = {}
    if stage == 'clip':
        source = ctx['sources']['clip']
        probe = json.loads(run([tool('ffprobe'), '-v', 'error', '-show_streams', '-show_format',
                                '-of', 'json', str(source)]))
        video = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
        if video is None:
            raise ValueError('No video stream in review clip')
        frames = json.loads(run([tool('ffprobe'), '-v', 'error', '-select_streams', 'v:0',
                                 '-show_frames', '-show_entries', 'frame=best_effort_timestamp_time',
                                 '-of', 'json', str(source)]))['frames']
        timestamps = [float(f['best_effort_timestamp_time']) for f in frames]
        if not timestamps or timestamps != sorted(timestamps):
            raise ValueError('Missing or unordered actual source-frame timestamps')
        frame_dir = evidence / 'frames'
        frame_dir.mkdir(exist_ok=True)
        # Decode EVERY source frame, including between the usual sampling times.
        run([tool('ffmpeg'), '-v', 'error', '-y', '-i', str(source), '-map', '0:v:0',
             '-vf', 'scale=360:-2', '-fps_mode', 'passthrough', '-q:v', '3',
             str(frame_dir / 'frame-%06d.jpg')])
        paths = sorted(frame_dir.glob('frame-*.jpg'))
        if len(paths) != len(timestamps):
            raise ValueError('Decoded frame count differs from the source timestamp count')
        mapping = [{'index': i, 'time_sec': t, 'image': str(path.relative_to(directory))}
                   for i, (path, t) in enumerate(zip(paths, timestamps))]
        write(evidence / 'frame-index.json', mapping)
        pages = []
        for start in range(0, len(paths), 20):
            name = f'evidence/sequence-{start // 20 + 1:02d}.jpg'
            sheet([(path, f'n={i}  {timestamps[i]:.3f}s')
                   for i, path in enumerate(paths[start:start + 20], start)],
                  directory / name)
            pages.append(name)
        # Full-resolution samples: dense opening, every half-second, and the actual last frame.
        targets = [0, .125, .25, .375, .5, .75, 1] + [i / 2 for i in range(math.ceil(timestamps[-1] * 2) + 1)]
        indices = sorted({min(range(len(timestamps)), key=lambda n: abs(timestamps[n] - t))
                          for t in targets} | {len(timestamps) - 1})
        detail = evidence / 'detail'
        detail.mkdir(exist_ok=True)
        selection = '+'.join(f'eq(n\\,{i})' for i in indices)
        run([tool('ffmpeg'), '-v', 'error', '-y', '-i', str(source), '-map', '0:v:0',
             '-vf', 'select=' + selection, '-fps_mode', 'passthrough', '-q:v', '2',
             str(detail / 'frame-%06d.jpg')])
        detail_paths = sorted(detail.glob('frame-*.jpg'))
        if len(detail_paths) != len(indices):
            raise ValueError('Detail evidence is incomplete')
        detail_index = [{'index': i, 'time_sec': timestamps[i],
                         'image': str(path.relative_to(directory))}
                        for i, path in zip(indices, detail_paths)]
        write(evidence / 'detail-index.json', detail_index)
        # The unmodified reference video remains available as a bound input.
        coverage = {'source_frames': len(paths), 'all_frames_extracted': True,
                    'source_timestamps': 'evidence/frame-index.json', 'sequence_pages': pages,
                    'full_resolution_samples': detail_index, 'sampling_is_not_approval': True}
        technical = {'decode': 'passed', 'duration_sec': float(probe['format']['duration']),
                     'width': video['width'], 'height': video['height'],
                     'fps': video.get('avg_frame_rate'),
                     'audio_streams': sum(s['codec_type'] == 'audio' for s in probe['streams'])}
    files = sorted(str(f.relative_to(directory)) for f in evidence.rglob('*') if f.is_file())
    packet = {'version': 1, 'packet_id': ctx['packet_id'], 'binding': ctx['binding'],
              'created_at': datetime.now(timezone.utc).isoformat(), 'contract': ctx['contract'],
              'technical': technical, 'coverage': coverage, 'evidence': files,
              'evidence_sha256': {name: file_hash(directory / name) for name in files},
              'state': 'awaiting user approval of both frames' if stage == 'frames' else 'awaiting independent visual review'}
    write(existing, packet)
    request = '''ROLE: Independent clip reviewer. Do not generate media or approve frames for the user.
Read packet.json and inspect ACTUAL evidence with image/video tools. Start with
the original lantern source and frame-comparison.jpg. Open every chronological
sequence page, then full-resolution detail frames around each action and flaw.
Use frame-index.json's real timestamps. Inspect the original bound clip and
reference video when supported. State the method actually used; do not claim
playback if you only inspected frames. Contact sheets alone do not prove style.

Every check in contract.policy.checks needs pass/fail/uncertain, an observation,
timestamp(s), and evidence paths relative to this packet. For a character-free
cutaway use an explained not_applicable only for eyes/flame_and_limbs. Fail and
uncertain block production. Do not infer accurate motion from the prompt, colors,
an arrow, an endpoint, or a successful FFprobe check. Missing user frame approval
blocks production regardless of the reviewer opinion. Report ALL material flaws.

For clip review create a JSON with packet_id, reviewer (dedicated reviewer ID),
method, coverage_reviewed (all sequence page paths), checks (an object keyed by
EVERY required check ID; each value has verdict, observed, timestamps_sec, evidence),
and summary. Never mark a check passed without opening supporting evidence.
Record with shorts.py record-review <episode> --scene <id> --report <file>.
For frames, show BOTH original images to the user and wait for their actual
approval. Do not fill a user approval field yourself.
'''
    (directory / 'review-request.txt').write_text(request)
    return {'packet': str(existing), 'request': str(directory / 'review-request.txt'),
            'comparison': str(evidence / 'frame-comparison.jpg'), 'status': packet['state']}


def current_events(ctx):
    events = ctx['directory'] / 'decisions'
    return [read(f) for f in sorted(events.glob('*.json'))] if events.is_dir() else []


def record(ctx, data):
    data = dict(data, packet_id=ctx['packet_id'], binding=ctx['binding'],
                recorded_at=datetime.now(timezone.utc).isoformat())
    directory = ctx['directory'] / 'decisions'
    directory.mkdir(parents=True, exist_ok=True)
    name = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json'
    write(directory / name, data)
    return data


def approve_frames(episode, scene_id, user_text):
    if not user_text or not user_text.strip():
        raise ValueError('Record the actual user message approving BOTH displayed frames')
    ctx = context(episode, scene_id, 'frames')
    if not (ctx['directory'] / 'packet.json').is_file():
        raise ValueError('Prepare and show the frame pair before recording user approval')
    return record(ctx, {'type': 'user_frame_approval', 'decision': 'approved',
                        'user_message': user_text.strip()})


def frame_gate(episode, scene_id):
    try:
        ctx = context(episode, scene_id, 'frames')
        events = current_events(ctx)
        event = events[-1] if events else {}
        passed = (event.get('type') == 'user_frame_approval' and event.get('decision') == 'approved'
                  and event.get('binding') == ctx['binding'] and bool(event.get('user_message')))
        return {'approved': passed, 'scene': scene_id, 'packet_id': ctx['packet_id'],
                'reason': 'both exact stills approved by user' if passed else 'both exact stills need explicit user approval'}
    except (OSError, ValueError, KeyError) as error:
        return {'approved': False, 'scene': scene_id, 'reason': str(error)}


def validate_report(ctx, packet, report):
    if report.get('packet_id') != ctx['packet_id']:
        raise ValueError('Review is for different or changed clip inputs')
    if not report.get('reviewer') or not report.get('method'):
        raise ValueError('Name the independent reviewer and actual inspection method')
    if report['reviewer'].lower() in ('generator', 'codex-primary', 'assistant', 'root'):
        raise ValueError('The generator cannot be the independent clip reviewer')
    checks = report.get('checks', {})
    if set(checks) != set(ctx['policy']['checks']):
        raise ValueError('Every required visual check needs an explicit verdict')
    for name, check in checks.items():
        verdict = check.get('verdict')
        if verdict not in ('pass', 'fail', 'uncertain', 'not_applicable'):
            raise ValueError('Invalid verdict: ' + name)
        if verdict == 'not_applicable' and (ctx['scene'].get('sol_visible', True) or name not in ('eyes', 'flame_and_limbs')):
            raise ValueError('This visual check cannot be skipped: ' + name)
        if not check.get('observed') or not check.get('evidence'):
            raise ValueError('Observation and actual evidence required: ' + name)
        for value in check['evidence']:
            if value not in packet['evidence'] or not (ctx['directory'] / value).is_file():
                raise ValueError('Unknown/missing review evidence: ' + value)
            if packet.get('evidence_sha256', {}).get(value) != file_hash(ctx['directory'] / value):
                raise ValueError('Review evidence changed: ' + value)
        times = check.get('timestamps_sec', [])
        if not times or any(not isinstance(t, (int, float)) or not math.isfinite(t)
                            or t < 0 or t > packet['technical']['duration_sec'] for t in times):
            raise ValueError('Actual timestamps inside this clip are required: ' + name)
    pages = set(packet['coverage']['sequence_pages'])
    passed = all(c['verdict'] in ('pass', 'not_applicable') for c in checks.values())
    reviewed = set(report.get('coverage_reviewed', []))
    if not reviewed.issubset(pages):
        raise ValueError('Unknown chronological sequence page in coverage')
    if passed and not pages.issubset(reviewed):
        raise ValueError('The reviewer has not inspected every chronological sequence page')
    for value in reviewed:
        if packet.get('evidence_sha256', {}).get(value) != file_hash(ctx['directory'] / value):
            raise ValueError('Chronological evidence changed: ' + value)
    if passed and not frame_gate(ctx['episode'], ctx['scene']['id'])['approved']:
        raise ValueError('User approval of both frames is missing; cannot record production pass')
    return passed


def record_review(episode, scene_id, report, clip=None, first=None, last=None):
    ctx = context(episode, scene_id, 'clip', clip, first, last)
    packet_path = ctx['directory'] / 'packet.json'
    if not packet_path.is_file():
        raise ValueError('Prepare actual clip evidence before recording a review')
    packet = read(packet_path)
    passed = validate_report(ctx, packet, report)
    return record(ctx, dict(report, type='independent_clip_review', decision='passed' if passed else 'rejected'))


def clip_gate(episode, scene_id, clip=None):
    frames = frame_gate(episode, scene_id)
    if not frames['approved']:
        return dict(frames, stage='frames')
    try:
        ctx = context(episode, scene_id, 'clip', clip)
        events = current_events(ctx)
        decision = events[-1] if events else {}
        approved = (decision.get('type') == 'independent_clip_review'
                    and decision.get('decision') == 'passed' and decision.get('binding') == ctx['binding'])
        if approved:
            approved = validate_report(ctx, read(ctx['directory'] / 'packet.json'), decision)
        return {'approved': approved, 'scene': scene_id, 'stage': 'clip',
                'reason': 'independent review passed' if approved else 'independent clip review is missing, rejected or stale'}
    except (OSError, ValueError, KeyError) as error:
        return {'approved': False, 'scene': scene_id, 'reason': str(error)}


def edit_gate(episode, edit):
    episode = Path(episode).resolve()
    checks = [clip_gate(episode, shot['id'], str((episode / 'public' / shot['scene']['src']).resolve()))
              for shot in edit['shots'] if shot['scene']['type'] == 'video']
    return {'approved': bool(checks) and all(c['approved'] for c in checks), 'scenes': checks}


def video_request(episode, scene_id, start_media_id, end_media_id):
    gate = frame_gate(episode, scene_id)
    if not gate['approved']:
        raise ValueError('VIDEO BLOCKED: ' + gate['reason'])
    if not start_media_id or not end_media_id:
        raise ValueError('Supply the uploaded media IDs for the exact approved first and last files')
    ctx = context(episode, scene_id, 'frames')
    settings = read(WORKFLOW / 'config/generation.json')['video']
    duration = ctx['scene']['end_sec'] - ctx['scene']['start_sec']
    bounds = settings['paired_frame_duration_sec']
    if not float(duration).is_integer() or not bounds['min'] <= duration <= bounds['max']:
        raise ValueError('Split this scene before requesting a paired-frame video; supported whole seconds: 3–10')
    return {'params': {'model': settings['model'], 'mode': settings['mode'],
                       'resolution': settings['resolution'], 'aspect_ratio': settings['aspect_ratio'],
                       'duration': duration, 'count': 1, 'prompt': ctx['scene']['video_prompt'],
                       'medias': [{'role': 'start_image', 'value': start_media_id},
                                  {'role': 'end_image', 'value': end_media_id}]},
            'approved_frames': ctx['binding']['frames'], 'submission_performed': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('review-frames', 'review-clip', 'approve-frames', 'record-review', 'review-gate', 'video-request'))
    parser.add_argument('episode')
    parser.add_argument('--scene')
    parser.add_argument('--clip')
    parser.add_argument('--first')
    parser.add_argument('--last')
    parser.add_argument('--edit')
    parser.add_argument('--stage', choices=('frames', 'clip'), default='clip')
    parser.add_argument('--user-approval-text')
    parser.add_argument('--report')
    parser.add_argument('--start-media-id')
    parser.add_argument('--end-media-id')
    args = parser.parse_args(argv)
    try:
        episode = episode_path(args.episode)
        if args.command == 'review-gate' and args.edit:
            result = edit_gate(episode, read(args.edit))
        else:
            if not args.scene:
                raise ValueError('--scene is required')
            if args.command in ('review-frames', 'review-clip'):
                result = prepare(episode, args.scene, 'frames' if args.command == 'review-frames' else 'clip', args.clip, args.first, args.last)
            elif args.command == 'approve-frames':
                result = approve_frames(episode, args.scene, args.user_approval_text)
            elif args.command == 'record-review':
                if not args.report:
                    raise ValueError('--report is required')
                result = record_review(episode, args.scene, read(args.report), args.clip, args.first, args.last)
            elif args.command == 'video-request':
                result = video_request(episode, args.scene, args.start_media_id, args.end_media_id)
            else:
                result = frame_gate(episode, args.scene) if args.stage == 'frames' else clip_gate(episode, args.scene, args.clip)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 2 if args.command == 'review-gate' and not result['approved'] else 0
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({'approved': False, 'error': str(error)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
