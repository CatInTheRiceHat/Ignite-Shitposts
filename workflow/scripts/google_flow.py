"""Single-shot, resumable useapi.net Google Flow integration (stdlib HTTP).

Protocol: https://useapi.net/docs/api-google-flow-v1
Only the calculus pilot A -> B test is currently enabled. No POST is retried.
"""
import base64
from contextlib import contextmanager
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

from PIL import Image

from paths import WORKFLOW

BASE_URL = 'https://api.useapi.net/v1/google-flow'
VIDEO_MODEL = 'veo-3.1-fast'
IMAGE_MODEL = 'nano-banana-pro'
VIDEO_SECONDS = 8


class FlowHTTPError(RuntimeError):
    def __init__(self, status):
        self.status = status
        hint = {401: 'Check USEAPI_TOKEN.', 402: 'Check the useapi.net subscription.',
                429: 'Flow is rate limited; wait before resuming.',
                596: 'Reconnect the Google Flow account.'}.get(status, 'Check the job in useapi.net.')
        super().__init__(f'useapi.net HTTP {status}. {hint}')


class FlowClient:
    def __init__(self):
        self.token = os.environ.get('USEAPI_TOKEN', '').strip()
        if not self.token:
            raise ValueError('Set USEAPI_TOKEN in the environment before running generate.')

    def request(self, method, path, body=None, content_type='application/json'):
        if body is not None and not isinstance(body, bytes):
            body = json.dumps(body).encode()
        request = Request(BASE_URL + path, data=body, method=method, headers={
            'Authorization': 'Bearer ' + self.token, 'Content-Type': content_type})
        try:
            # Captcha retries can take minutes, even with async video submission.
            with urlopen(request, timeout=300 if method == 'POST' else 60) as response:
                result = json.load(response)
        except HTTPError as error:
            # Never dump account cookies, bearer tokens, or signed URLs.
            raise FlowHTTPError(error.code) from None
        except (URLError, TimeoutError, OSError):
            raise RuntimeError('useapi.net connection failed. Rerun to resume saved jobs; POSTs are never retried automatically.') from None
        except (ValueError, UnicodeError):
            raise RuntimeError('useapi.net returned invalid JSON.') from None
        if not isinstance(result, dict) or result.get('error'):
            raise RuntimeError('useapi.net returned an error or unexpected response; inspect the job in useapi.net.')
        return result

    def healthy_account(self, email=None):
        accounts = self.request('GET', '/accounts')
        if email is None:
            email = next((key for key, value in sorted(accounts.items())
                          if isinstance(value, dict) and value.get('health') == 'OK'), None)
        if email is None:
            raise RuntimeError('No healthy connected Google Flow account. Connect or repair the account in useapi.net.')
        if not isinstance(accounts.get(email), dict) or accounts[email].get('health') != 'OK':
            raise RuntimeError('Selected Google Flow account is missing or unhealthy. Repair it in useapi.net before submitting jobs.')
        return email

    def download(self, url, target):
        if not isinstance(url, str) or urlsplit(url).scheme != 'https':
            raise RuntimeError('Flow did not return an HTTPS media download URL.')
        try:
            # Signed CDN downloads need no API credentials.
            with urlopen(Request(url), timeout=120) as response, target.open('wb') as output:
                shutil.copyfileobj(response, output)
        except HTTPError as error:
            raise FlowHTTPError(error.code) from None
        except (URLError, TimeoutError, OSError):
            raise RuntimeError('Media download interrupted. Rerun generate to download the saved job again.') from None


def sha256(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest() if hasattr(hashlib, 'file_digest') else hashlib.sha256(source.read()).hexdigest()


def save_json(path, value):
    """Atomic state updates; a killed poller must not lose the submitted job ID."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix='.state-', dir=path.parent)
    try:
        with os.fdopen(handle, 'w') as output:
            json.dump(value, output, indent=2)
            output.write('\n')
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


@contextmanager
def shot_lock(folder):
    folder.mkdir(parents=True, exist_ok=True)
    with (folder/'A-B.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('Another A -> B generator is running for this episode.') from None
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def verify_image(path, portrait=False):
    try:
        with Image.open(path) as image:
            width, height = image.size
            image.verify()
    except (OSError, ValueError):
        raise ValueError(f'Unusable keyframe/reference image: {path}') from None
    if portrait and (width >= height or abs(width/height - 9/16) > .03):
        raise ValueError(f'Keyframe must be 9:16 portrait: {path}')


def ffprobe_path(explicit=None):
    binary = explicit or os.environ.get('FFPROBE_PATH') or shutil.which('ffprobe')
    if not binary:
        raise RuntimeError('FFprobe not found. Install ffmpeg or pass --ffprobe /full/path/to/ffprobe.')
    try:
        result = subprocess.run([str(binary), '-version'], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        raise RuntimeError(f'FFprobe unavailable at {binary}') from None
    if result.returncode:
        raise RuntimeError(f'FFprobe failed at {binary}: exit {result.returncode}')
    return str(binary)


def verify_mp4(path, binary):
    try:
        result = subprocess.run([binary, '-v', 'error', '-show_format', '-show_streams',
                                 '-of', 'json', str(path)], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        raise RuntimeError(f'FFprobe could not inspect {path}') from None
    if result.returncode or result.stderr.strip():
        raise ValueError(f'FFprobe rejected MP4: {path}')
    try:
        probe = json.loads(result.stdout)
        video = next(stream for stream in probe['streams'] if stream.get('codec_type') == 'video')
        duration = float(probe['format']['duration'])
        width, height = int(video['width']), int(video['height'])
        fps_parts = video['avg_frame_rate'].split('/')
        fps = float(fps_parts[0])/float(fps_parts[1])
        valid = ('mp4' in probe['format']['format_name'].split(',')
                 and video.get('codec_name') and math.isfinite(duration)
                 and duration >= 3.6 and width >= 720 and height >= 1280
                 and abs(width/height - 9/16) <= .03 and math.isfinite(fps) and fps > 0)
    except (KeyError, StopIteration, TypeError, ValueError, ZeroDivisionError, IndexError):
        valid = False
    if not valid:
        raise ValueError(f'Expected a playable portrait MP4, at least 720x1280 and 3.6 seconds: {path}')
    return {'codec': video['codec_name'], 'width': width, 'height': height,
            'duration_sec': duration, 'fps': fps}


def publish(source, target):
    """Never overwrite a download, even if another process created the target."""
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, target)
    except FileExistsError:
        if sha256(source) != sha256(target):
            raise ValueError(f'Differing filename collision; existing file preserved: {target}') from None


def image_prompt(episode, letter):
    text = (episode/'flow-image-prompts.md').read_text()
    sections = re.split(r'(?m)^##\s+', text)
    section = next((part for part in sections[1:] if re.match(letter + r'\s+[—–-]', part)), None)
    if section is None:
        raise ValueError(f'Missing {letter} section in {episode}/flow-image-prompts.md')
    # Keep the editable creative text, omit local download instructions/paths.
    content = sections[0].split('\n', 1)[-1] + '\n' + section.split('\n', 1)[-1]
    content = re.sub(r'Upload the original Sol reference.*?\nUse those references',
                     'Use the attached original Sol and painted scene references', content, flags=re.S)
    return re.sub(r'(?:Save the downloaded image as|Save as)[^\n]*', '', content).strip()


def video_prompt(episode):
    text = (episode/'flow-video-prompts.md').read_text()
    section = re.search(r'(?ms)^## 1\..*?```(?:text)?\s*\n(.*?)```', text)
    if section is None:
        raise ValueError(f'Missing shot 1 prompt in {episode}/flow-video-prompts.md')
    prompt = section.group(1).strip().replace('five-second', 'eight-second')
    return (prompt + '\n\nUse the supplied startImage A as the exact opening composition and '
            'endImage B as the exact closing composition. Animate one continuous A to B shot: '
            'hop onto the moving board, land, then settle into the low side angle with the tiny '
            'balance arm beginning to extend. Arrive at B and hold briefly. Preserve the painted '
            'Sol identity, texture and palette in both frames. No cuts, dissolves, speech or music.')


class Generation:
    def __init__(self, client, state_path, state, poll_interval, wait_timeout):
        self.client, self.path, self.state = client, state_path, state
        self.poll_interval, self.wait_timeout = poll_interval, wait_timeout

    def save(self):
        save_json(self.path, self.state)

    def upload(self, key, path):
        digest = sha256(path)
        uploads = self.state.setdefault('uploads', {})
        cached = uploads.get(key, {})
        if cached.get('sha256') == digest:
            return cached['media_id']
        mime = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}[path.suffix.lower()]
        result = self.client.request('POST', '/assets/' + quote(self.state['email'], safe=''),
                                     path.read_bytes(), mime)
        media_id = result['mediaGenerationId']['mediaGenerationId']
        uploads[key] = {'sha256': digest, 'media_id': media_id}
        self.save()
        return media_id

    def job(self, entry, endpoint, request):
        if not entry.get('job_id'):
            if entry.get('status'):
                raise RuntimeError(f'Submission outcome needs review in {self.path}. '
                                   'Find the job in useapi.net and set this entry\'s job_id; '
                                   'reruns will not submit a possible duplicate.')
            # Fail closed on missing/unknown health, immediately before every job.
            self.client.healthy_account(self.state['email'])
            entry.update(status='submitting', request=request)
            self.save()
            result = self.client.request('POST', endpoint, request)
            job_id = result.get('jobid') or result.get('jobId')
            if not job_id:
                raise RuntimeError(f'No job ID returned. Inspect useapi.net and {self.path}; do not blindly resubmit.')
            entry.update(job_id=job_id, status=result.get('status', 'completed'))
            self.save()  # Must precede polling, media parsing and downloading.
            print(f'SAVED JOB {job_id} in {self.path}', flush=True)
        else:
            print(f'RESUMING JOB {entry["job_id"]}', flush=True)
            result = None
        deadline = time.monotonic() + self.wait_timeout
        last_status = None
        while True:
            if result is None:
                result = self.client.request('GET', '/jobs/' + quote(entry['job_id'], safe=''))
            status = result.get('status', 'completed' if result.get('media') else None)
            entry['status'] = status
            self.save()
            if status == 'completed':
                media = result.get('response', result).get('media', [])
                if len(media) != 1:
                    raise RuntimeError('Expected exactly one Flow result; saved job retained for inspection.')
                return media[0]
            if status == 'failed':
                raise RuntimeError(f'Flow job failed: {entry["job_id"]}. No replacement job submitted; inspect useapi.net.')
            if status not in ('created', 'started'):
                raise RuntimeError(f'Unknown Flow job status for {entry["job_id"]}; saved job retained.')
            if status != last_status:
                print(f'Flow job {status}; waiting (Ctrl-C is safe after SAVED JOB).', flush=True)
                last_status = status
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError(f'Wait timed out for {entry["job_id"]}. Rerun the same command to resume.')
            time.sleep(min(self.poll_interval, remaining))
            result = None

    def download_media(self, media, kind, target):
        generated = media.get('image', {}).get('generatedImage', {})
        media_id = media.get('mediaGenerationId') or generated.get('mediaGenerationId')
        url = media.get('videoUrl') if kind == 'video' else generated.get('fifeUrl')
        encoded = generated.get('encodedImage')
        if kind == 'image' and encoded and not url:
            target.write_bytes(base64.b64decode(encoded, validate=True))
            return
        if not url and media_id:
            url = self.client.request('GET', '/assets/' + quote(media_id, safe='')).get('url')
        try:
            self.client.download(url, target)
        except FlowHTTPError as error:
            if error.status not in (401, 403) or not media_id:
                raise
            # A resumed job can contain an expired signed URL. Refresh without generating.
            url = self.client.request('GET', '/assets/' + quote(media_id, safe=''))['url']
            self.client.download(url, target)


def generate(episode, shot='A-B', email=None, ffprobe=None, poll_interval=10, wait_timeout=1200):
    episode = Path(episode).resolve()
    if not episode.is_relative_to(WORKFLOW) or episode.name != 'calculus_pilot' or shot != 'A-B':
        raise ValueError('This first integration supports only calculus_pilot --shot A-B inside workflow/.')
    if not all(math.isfinite(value) and value > 0 for value in (poll_interval, wait_timeout)):
        raise ValueError('Poll interval and wait timeout must be positive and finite.')
    if not (episode/'edit.json').is_file():
        raise ValueError('Prepare calculus_pilot before generating it.')
    binary = ffprobe_path(ffprobe)  # Check tools before any paid work.
    folder = episode/'jobs/useapi'
    target = episode/'clips/01-hop-on.mp4'
    with shot_lock(folder):
        state_path = folder/'A-B.json'
        state = json.loads(state_path.read_text()) if state_path.exists() else {'version': 1, 'shot': shot}
        if state.get('version') != 1 or state.get('shot') != shot:
            raise ValueError(f'Unrecognized generation state: {state_path}')
        if target.exists():
            probe = verify_mp4(target, binary)
            state['verification'] = probe
            save_json(state_path, state)
            print(f'EXISTING MP4 VERIFIED: {target} ({probe["width"]}x{probe["height"]}, {probe["duration_sec"]:.2f}s)')
            return target
        client = FlowClient()
        if email and state.get('email') and email != state['email']:
            raise ValueError('Saved jobs belong to a different Flow account; resume with the original account.')
        state['email'] = client.healthy_account(state.get('email') or email)
        run = Generation(client, state_path, state, poll_interval, wait_timeout)
        run.save()
        print('Flow account health: OK. Scope: calculus_pilot A -> B, one video.', flush=True)
        with tempfile.TemporaryDirectory(prefix='download-', dir=folder) as temporary:
            scratch = Path(temporary)
            video = state.setdefault('video', {})
            if not video.get('job_id') and not video.get('status'):
                # Validate all local inputs before the first generation, and never use blocking art.
                prompts = {letter: image_prompt(episode, letter) for letter in ('A', 'B')}
                motion = video_prompt(episode)
                references = [WORKFLOW/'assets/sol-full-body.png', WORKFLOW/'assets/calculus-painted-scene.jpg']
                for letter in ('A', 'B'):
                    frame = episode/f'keyframes/{letter}.png'
                    if frame.exists():
                        verify_image(frame, portrait=True)
                        if any(sha256(frame) == sha256(guide) for guide in (episode/'keyframes/blocking').glob('*.png')):
                            raise ValueError(f'Blocking guide in approved keyframe slot; supply finished painted artwork: {frame}')
                missing = [letter for letter in ('A', 'B') if not (episode/f'keyframes/{letter}.png').exists()]
                refs = []
                if missing:
                    for path in references:
                        verify_image(path)
                    refs = [run.upload('reference-' + path.stem, path) for path in references]
                for letter in ('A', 'B'):
                    frame = episode/f'keyframes/{letter}.png'
                    if not frame.exists():
                        entry = state.setdefault('images', {}).setdefault(letter, {})
                        media = run.job(entry, '/images', {
                            'email': state['email'], 'model': IMAGE_MODEL, 'prompt': prompts[letter],
                            'aspectRatio': '9:16', 'count': 1, 'reference_1': refs[0], 'reference_2': refs[1]})
                        download = scratch/f'{letter}.png'
                        run.download_media(media, 'image', download)
                        verify_image(download, portrait=True)
                        # Flow can return JPEG/WebP; canonical .png slots must contain actual PNGs.
                        with Image.open(download) as image:
                            image.convert('RGB').save(scratch/f'{letter}-canonical.png', 'PNG')
                        publish(scratch/f'{letter}-canonical.png', frame)
                        entry['sha256'] = sha256(frame)
                        run.save()
                    else:
                        print(f'REUSING KEYFRAME: {frame}', flush=True)
                start, end = [run.upload(letter, episode/f'keyframes/{letter}.png') for letter in ('A', 'B')]
                request = {'email': state['email'], 'model': VIDEO_MODEL, 'prompt': motion,
                           'aspectRatio': 'portrait', 'duration': VIDEO_SECONDS, 'count': 1,
                           'startImage': start, 'endImage': end, 'async': True}
            else:
                # Resume the submitted request even if prompts or local keyframes were edited.
                request = video.get('request', {})
            media = run.job(video, '/videos', request)
            download = scratch/'01-hop-on.mp4'
            run.download_media(media, 'video', download)
            probe = verify_mp4(download, binary)
            publish(download, target)
            state['verification'] = probe
            state['output_sha256'] = sha256(target)
            run.save()
        print(f'MP4 VERIFIED: {target} ({probe["width"]}x{probe["height"]}, {probe["duration_sec"]:.2f}s)', flush=True)
        return target
