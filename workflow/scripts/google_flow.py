"""Single-shot, resumable useapi.net Google Flow integration (stdlib HTTP).

Protocol: https://useapi.net/docs/api-google-flow-v1
Only the calculus pilot A -> B test is currently enabled. No POST is retried.
"""
import base64
from contextlib import contextmanager, nullcontext
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
IGNITE_EMAIL = 'ignitefindyourfire@gmail.com'
VIDEO_MODEL = 'veo-3.1-lite'
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
        if email is None and len(accounts) > 1:
            raise ValueError('Multiple connected Flow accounts. Specify the Ignite account with '
                             '--email ADDRESS. Connected accounts: ' + ', '.join(sorted(accounts)))
        if email is None:
            email = next((key for key, value in sorted(accounts.items())
                          if isinstance(value, dict) and value.get('health') == 'OK'
                          and value.get('backend') == 'flow'), None)
        if email is None:
            raise RuntimeError('No healthy connected Google Flow account. Connect or repair the account in useapi.net.')
        if (not isinstance(accounts.get(email), dict) or accounts[email].get('health') != 'OK'
                or accounts[email].get('backend') != 'flow'):
            raise RuntimeError('Selected Google Flow account is missing or unhealthy. Repair it in useapi.net before submitting jobs.')
        return email

    def check_credits(self, email, submitting=True):
        # This endpoint includes cookies. Keep its full response only in memory.
        account = self.request('GET', '/accounts/' + quote(email, safe=''))
        if account.get('health') != 'OK' or account.get('backend') != 'flow':
            raise RuntimeError('Selected Google Flow account is unhealthy. Repair it before submitting jobs.')
        credits = account.get('credits', {})
        balance = credits.get('credits') if isinstance(credits, dict) else None
        if type(balance) not in (int, float) or not math.isfinite(balance) or balance < 0:
            raise RuntimeError('Flow credit balance is unavailable; no jobs submitted.')
        # Prefer the actual first/last-frame model cost returned by this account.
        models = account.get('models', {}).get('videoModels', [])
        matching = [model for model in models if isinstance(model, dict)
                    and re.fullmatch(r'veo_3_1_interpolation_lite(?:_ultra)?', str(model.get('key', '')))
                    and model.get('videoLengthSeconds') == VIDEO_SECONDS
                    and model.get('resolution') == '720p'
                    and 'VIDEO_ASPECT_RATIO_PORTRAIT' in model.get('supportedAspectRatios', [])]
        reported = [model.get('creditCost') for model in matching]
        if reported and any(type(value) not in (int, float) or not math.isfinite(value) or value <= 0
                            for value in reported):
            raise RuntimeError('Flow model credit cost is unavailable; no jobs submitted.')
        # Documented regular Lite fallback: Ultra 5, all other known tiers 10.
        # Reserve the video budget before uploading the existing keyframes.
        tier = credits.get('userPaygateTier')
        costs = {'PAYGATE_TIER_ZERO': 10, 'PAYGATE_TIER_ONE': 10,
                 'PAYGATE_TIER_TIER1P5': 10, 'PAYGATE_TIER_TWO': 5}
        if not reported and tier not in costs:
            raise RuntimeError('Flow plan/credit cost is unavailable; no jobs submitted.')
        cost = max(reported) if reported else costs[tier]
        if submitting and balance < cost:
            raise RuntimeError(f'Insufficient Flow credits: {balance:g} available; '
                               f'{cost} required for one Veo 3.1 Lite clip. No generation submitted.')
        return balance, cost

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


def approved_keyframes(episode):
    frames = [episode/f'keyframes/{letter}.png' for letter in ('A', 'B')]
    missing = [str(frame) for frame in frames if not frame.is_file()]
    if missing:
        raise ValueError('Missing required keyframe(s): ' + ', '.join(missing)
                         + '. Supply the existing finished A/B artwork before generating; '
                         'no uploads or video job submitted.')
    guides = {sha256(path) for path in (episode/'keyframes/blocking').glob('*.png')}
    for frame in frames:
        verify_image(frame, portrait=True)
        if sha256(frame) in guides:
            raise ValueError(f'Blocking guide in approved keyframe slot; supply finished painted artwork: {frame}')
    return frames


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
    return (re.sub(r'(?:Save the downloaded image as|Save as)[^\n]*', '', content).strip()
            + '\nKeep Sol\'s original compact flame shape, original eyes, stubby rounded '
            'limbs and completely mouthless face.')


def video_prompt(episode):
    text = (episode/'flow-video-prompts.md').read_text()
    section = re.search(r'(?ms)^## 1\..*?```(?:text)?\s*\n(.*?)```', text)
    if section is None:
        raise ValueError(f'Missing shot 1 prompt in {episode}/flow-video-prompts.md')
    prompt = section.group(1).strip().replace('five-second', 'eight-second')
    return (prompt + '\n\nUse the supplied startImage A as the exact opening composition and '
            'endImage B as the exact closing composition. Animate one continuous A to B shot: '
            'hop onto the moving board, land, and wobble exactly once to catch his balance. '
            'One tiny existing arm begins to extend as he settles into the low side angle. '
            'Timing: anticipate at 0-0.4 seconds, hop at '
            '0.4-1.2 seconds, land both feet by 1.8 seconds, wobble once at 1.8-2.8 seconds, '
            'and reach the B composition by '
            '3 seconds. Hold that composition through the remaining clip, with gentle board '
            'motion, so the existing 3.6-second edit retains the full action. Preserve the painted '
            'Sol identity, compact flame shape, original eyes, stubby limbs, mouthless face, '
            'texture and palette in both frames. No cuts, dissolves, speech or music.')


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
            self.client.check_credits(self.state['email'])
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


def generate(episode, shot='A-B', email=None, ffprobe=None, poll_interval=10, wait_timeout=1200,
             dry_run=False):
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
    # A dry run makes only GET requests and does not even create a state/lock file.
    with nullcontext() if dry_run else shot_lock(folder):
        state_path = folder/'A-B.json'
        state = json.loads(state_path.read_text()) if state_path.exists() else {'version': 1, 'shot': shot}
        if state.get('version') != 1 or state.get('shot') != shot:
            raise ValueError(f'Unrecognized generation state: {state_path}')
        if target.exists():
            probe = verify_mp4(target, binary)
            if state.get('output_sha256') and state['output_sha256'] != sha256(target):
                raise ValueError(f'Differing filename collision with saved output; existing file preserved: {target}')
            if not dry_run:
                state['verification'] = probe
                save_json(state_path, state)
            print(f'EXISTING MP4 VERIFIED: {target} ({probe["width"]}x{probe["height"]}, {probe["duration_sec"]:.2f}s)')
            if not dry_run:
                return target
        video_state = state.get('video', {})
        if video_state.get('job_id') and video_state.get('request', {}).get('model') != VIDEO_MODEL:
            raise ValueError('Saved video job uses a different model. Inspect that job before starting a Lite test; no replacement submitted.')
        submitting = not target.exists() and not (video_state.get('job_id') or video_state.get('status'))
        if submitting:
            frames = approved_keyframes(episode)
            motion = video_prompt(episode)
        client = FlowClient()
        selected = client.healthy_account(email or IGNITE_EMAIL)
        if state.get('email') and selected != state['email']:
            raise ValueError('Saved jobs belong to a different Flow account; resume with the original account.')
        balance, cost = client.check_credits(selected, submitting=submitting)
        print(f'ACCOUNT CHECK PASSED: {selected}; health OK; {balance:g} Flow credits available; '
              f'one Lite clip costs {cost}. Scope: calculus_pilot A -> B only.', flush=True)
        if dry_run:
            action = ('verify the existing clip' if target.exists() else
                      f'resume saved job {video_state["job_id"]}' if video_state.get('job_id') else
                      'stop for submission outcome review' if video_state.get('status') else
                      'upload A/B and submit one portrait Veo 3.1 Lite video')
            print(f'DRY RUN: would {action}. No uploads, submissions or state changes.', flush=True)
            return target
        state['email'] = selected
        run = Generation(client, state_path, state, poll_interval, wait_timeout)
        run.save()
        with tempfile.TemporaryDirectory(prefix='download-', dir=folder) as temporary:
            scratch = Path(temporary)
            video = state.setdefault('video', {})
            if not video.get('job_id') and not video.get('status'):
                for frame in frames:
                    print(f'REUSING KEYFRAME: {frame}', flush=True)
                start, end = [run.upload(letter, frame) for letter, frame in zip(('A', 'B'), frames)]
                request = {'email': state['email'], 'model': VIDEO_MODEL, 'prompt': motion,
                           'aspectRatio': 'portrait', 'resolution': '720p', 'duration': VIDEO_SECONDS, 'count': 1,
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
