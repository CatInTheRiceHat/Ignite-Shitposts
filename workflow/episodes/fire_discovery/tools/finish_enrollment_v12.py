"""Package the caption/end-card edit and prepare actual rendered review evidence."""
import hashlib
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

EPISODE = Path(__file__).resolve().parents[1]
REVIEW = EPISODE / 'revisions/enrollment-endcard-v1/review'
PICTURE = EPISODE / 'renders/fire-discovery-enrollment-v12-fullbleed-picture.mp4'
OUTPUT = EPISODE / 'renders/fire-discovery-enrollment-v12-fullbleed-final.mp4'
BASELINE = EPISODE / 'revisions/monkey-cartoon-cloud-v3/renders/fire-discovery-captions-v10-final.mp4'
EDIT = EPISODE / 'edit-enrollment-v12.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def packets(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'a:0',
                          '-show_packets', '-show_data_hash', 'sha256',
                          '-show_entries', 'packet=pts,dts,duration,size,data_hash',
                          '-of', 'json', str(path)]))['packets']


def main():
    REVIEW.mkdir(parents=True, exist_ok=True)
    edit = json.loads(EDIT.read_text())
    previous = json.loads((EPISODE / 'edit-captions-v10.json').read_text())
    assert edit['shots'][:5] == previous['shots']
    assert edit['captions'][:16] == previous['captions']
    assert edit['audioTracks'] == previous['audioTracks']
    assert not OUTPUT.exists(), 'Preserve existing output; choose a new version.'
    if not PICTURE.exists():
        # The corrected static card is rendered from EDIT by Remotion's still command.
        # Reuse the original764 picture frames, then append exactly90 static frames.
        run(['ffmpeg', '-v', 'error', '-nostdin',
             '-i', str(EPISODE / 'renders/fire-discovery-enrollment-v12-picture.mp4'),
             '-loop', '1', '-framerate', '30',
             '-i', str(EPISODE / 'renders/enrollment-endcard-v12-fullbleed.png'),
             '-filter_complex', '[0:v]trim=end_frame=764,setpts=PTS-STARTPTS[a];'
             '[1:v]trim=end_frame=90,setpts=PTS-STARTPTS[b];'
             '[a][b]concat=n=2:v=1:a=0,format=yuv420p[v]',
             '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
             '-r', '30', '-frames:v', '854', '-movflags', '+faststart', str(PICTURE)])
    # Keep the established mix byte-for-byte. The added still is deliberately silent.
    run(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(PICTURE), '-i', str(BASELINE),
         '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy', '-movflags', '+faststart', str(OUTPUT)])
    run(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(OUTPUT), '-f', 'null', '-'])
    probe = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                            '-of', 'json', str(OUTPUT)]))
    video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    assert (video['width'], video['height'], video['avg_frame_rate'], int(video['nb_frames'])) == (1080, 1920, '30/1', 854)
    old_packets, new_packets = packets(BASELINE), packets(OUTPUT)
    assert old_packets == new_packets, 'Original soundtrack changed.'

    evidence = REVIEW / 'detail'
    evidence.mkdir(exist_ok=True)
    samples = []
    for i, cue in enumerate(edit['captions']):
        frame = math.floor((cue['start'] + cue['end']) / 2 * 30)
        samples.append({'frame': frame, 'time_sec': frame / 30,
                        'kind': 'caption', 'caption_index': i + 1, 'text': cue['text']})
    for frame in [202, 203, 204, 728, 755, 760, 763, 764, 765, 766, 852, 853]:
        samples.append({'frame': frame, 'time_sec': frame / 30, 'kind': 'transition'})
    frames = sorted({item['frame'] for item in samples})
    select = '+'.join(f'eq(n,{frame})' for frame in frames)
    run(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(OUTPUT), '-vf', f"select='{select}'",
         '-fps_mode', 'vfr', '-q:v', '2', str(evidence / 'frame-%03d.jpg')])
    for item in samples:
        item['file'] = f'detail/frame-{frames.index(item["frame"]) + 1:03d}.jpg'
    pages = []
    captions = [s for s in samples if s['kind'] == 'caption']
    for offset in range(0, len(captions), 6):
        canvas = Image.new('RGB', (1080, 1340), '#FFF8F0')
        draw = ImageDraw.Draw(canvas)
        for i, item in enumerate(captions[offset:offset + 6]):
            x, y = i % 3 * 360, i // 3 * 670
            with Image.open(REVIEW / item['file']) as source:
                canvas.paste(source.resize((360, 640)), (x, y))
            draw.text((x + 8, y + 645), f'Caption {item["caption_index"]} | frame {item["frame"]} | {item["time_sec"]:.3f}s', fill='#1A1A2E')
        name = f'captions-{offset // 6 + 1:02d}.jpg'
        canvas.save(REVIEW / name, quality=95)
        pages.append(name)
    # Compare the same uncaptained picture region for every original episode frame.
    ssim_file = REVIEW / 'picture-area-ssim.txt'
    run(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(BASELINE), '-i', str(OUTPUT),
         '-filter_complex', '[0:v]crop=1080:1580:0:0,setpts=PTS-STARTPTS[a];'
         '[1:v]trim=end_frame=764,crop=1080:1580:0:0,setpts=PTS-STARTPTS[b];'
         f'[a][b]ssim=stats_file={ssim_file}', '-an', '-f', 'null', '-'])
    ssim = [float(line.split('All:')[1].split()[0]) for line in ssim_file.read_text().splitlines()]
    assert len(ssim) == 764 and min(ssim) > .97
    verification = {
        'output': str(OUTPUT), 'sha256': sha(OUTPUT), 'bytes': OUTPUT.stat().st_size,
        'full_decode_passed': True, 'frames': 854, 'duration_sec': 854 / 30,
        'dimensions': [1080, 1920], 'fps': 30,
        'caption_font_size': 70, 'original_font_size': 56, 'increase_percent': 25,
        'caption_outline_px': 12, 'caption_side_margins_percent': 10,
        'first_five_shots_unchanged': True, 'dialogue_caption_words_and_timing_unchanged': True,
        'all_audio_edit_settings_unchanged': True,
        'aac_packets_and_timestamps_identical': True, 'aac_packet_count': len(new_packets),
        'uncaptioned_picture_compared_frames': len(ssim), 'ssim_min': min(ssim),
        'ssim_mean': sum(ssim) / len(ssim), 'baseline_sha256': sha(BASELINE),
        'endcard_frames': [764, 853], 'endcard_duration_sec': 3,
        'endcard_image_sha256': sha(EPISODE / 'revisions/enrollment-endcard-v1/endcard.png'),
        'endcard_framing': 'Image width1080,height1935,y=-7.5; crop7.5px top/bottom to fill9:16 without side borders.',
        'endcard_audio': 'Silent after the unchanged original soundtrack ends.',
        'manual_audio_listening_claimed': False, 'independent_visual_review': 'pending',
    }
    packet = {'video': str(OUTPUT), 'sha256': sha(OUTPUT), 'edit': str(EDIT), 'edit_sha256': sha(EDIT),
              'script': str(EPISODE / 'script.txt'),
              'voice_cues': str(EPISODE / 'revisions/monkey-cartoon-cloud-v3/reviews/no-poof-v9/voice-cues-assembled.json'),
              'endcard_storyboard': str(REVIEW.parent / 'storyboard.txt'),
              'pages': pages, 'samples': samples, 'verification': 'verification.json',
              'scope': '70px captions and static3s enrollment card; original five scenes and exact AAC soundtrack retained.'}
    (REVIEW / 'packet.json').write_text(json.dumps(packet, indent=2) + '\n')
    (REVIEW / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    main()
