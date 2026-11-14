"""Mock the actual HTTP boundary: no credentials, network calls or paid jobs."""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit

from PIL import Image

SCRIPTS = Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0, str(SCRIPTS))
import google_flow as flow
from paths import WORKFLOW
from shorts import main

EMAIL = flow.IGNITE_EMAIL
VIDEO_ID = 'j123v-pilot'
PROBE = {'format': {'format_name': 'mov,mp4,m4a,3gp,3g2,mj2', 'duration': '8.0'},
         'streams': [{'codec_type': 'video', 'codec_name': 'h264', 'width': 720,
                      'height': 1280, 'avg_frame_rate': '24/1'}]}


def video_media(url=True):
    media = {'mediaGenerationId': 'user:1-email:abc-video:result',
             'video': {'generatedVideo': {'model': 'veo_3_1_i2v_fl'}}}
    if url:
        media['videoUrl'] = 'https://flow-content.google/video/result?Signature=temporary'
    return media


def image_media(letter):
    return {'image': {'generatedImage': {
        'mediaGenerationId': 'user:1-email:abc-image:' + letter,
        'fifeUrl': 'https://flow-content.google/image/' + letter}}}


class MockFlowTests(unittest.TestCase):
    def setUp(self):
        (WORKFLOW/'.cache').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='test-flow-', dir=WORKFLOW/'.cache')
        self.episode = Path(self.temp.name)/'calculus_pilot'
        (self.episode/'keyframes/blocking').mkdir(parents=True)
        (self.episode/'edit.json').write_text('{}')
        pilot = WORKFLOW/'episodes/calculus_pilot'
        for name in ('flow-image-prompts.md', 'flow-video-prompts.md'):
            shutil.copyfile(pilot/name, self.episode/name)
        png = io.BytesIO()
        Image.new('RGB', (90, 160), '#ea7529').save(png, 'PNG')
        self.png = png.getvalue()
        self.approved_frames()
        self.accounts = {EMAIL: {'health': 'OK', 'backend': 'flow'}}
        self.account = {'health': 'OK', 'backend': 'flow',
                        'credits': {'credits': 1000, 'userPaygateTier': 'PAYGATE_TIER_ONE'},
                        'accountCookies': [{'value': 'private-cookie-do-not-log'}]}
        self.calls = []
        self.posts = []
        self.image_count = 0
        self.video_count = 0
        self.polls = ['started', 'completed']
        self.bad_video = False
        self.no_video_url = False
        self.encoded_image = False
        self.network_error = None
        self.env_patch = patch.dict('os.environ', {'USEAPI_TOKEN': 'mock-secret-token'})
        self.http_patch = patch('google_flow.urlopen', side_effect=self.http)
        self.tools_patch = patch('google_flow.subprocess.run', side_effect=self.probe)
        self.sleep_patch = patch('google_flow.time.sleep')
        self.output = io.StringIO()
        for item in (self.env_patch, self.http_patch, self.tools_patch, self.sleep_patch,
                     redirect_stdout(self.output), redirect_stderr(self.output)):
            item.__enter__()
            self.addCleanup(item.__exit__, None, None, None)
        self.addCleanup(self.temp.cleanup)

    @property
    def state_path(self):
        return self.episode/'jobs/useapi/A-B.json'

    def state(self):
        return json.loads(self.state_path.read_text())

    def approved_frames(self):
        for letter in ('A', 'B'):
            (self.episode/f'keyframes/{letter}.png').write_bytes(self.png)

    def probe(self, args, **kwargs):
        if '-version' in args:
            return subprocess.CompletedProcess(args, 0, 'ffprobe version fixture', '')
        if self.bad_video:
            return subprocess.CompletedProcess(args, 1, '', 'Invalid data found')
        return subprocess.CompletedProcess(args, 0, json.dumps(PROBE), '')

    def http(self, request, timeout):
        method, url = request.get_method(), request.full_url
        path = unquote(urlsplit(url).path.removeprefix('/v1/google-flow'))
        self.calls.append((method, path))
        if url.startswith(flow.BASE_URL):
            self.assertEqual(request.get_header('Authorization'), 'Bearer mock-secret-token')
        else:
            self.assertIsNone(request.get_header('Authorization'))
            if '/image/' in path:
                return io.BytesIO(self.png)
            return io.BytesIO(b'MOCK VIDEO DOWNLOAD')
        if method == 'GET' and path == '/accounts':
            return io.BytesIO(json.dumps(self.accounts).encode())
        if method == 'GET' and path == '/accounts/' + EMAIL:
            return io.BytesIO(json.dumps(self.account).encode())
        if method == 'POST' and path.startswith('/assets/'):
            self.assertEqual(path, '/assets/' + EMAIL)
            self.assertIn(request.get_header('Content-type'), ('image/png', 'image/jpeg'))
            return io.BytesIO(json.dumps({'mediaGenerationId': {
                'mediaGenerationId': 'uploaded-' + str(len(self.calls))}}).encode())
        if method == 'POST' and path in ('/images', '/videos'):
            # The last request must check current health AND credits of the pinned account.
            self.assertEqual(self.calls[-2], ('GET', '/accounts/' + EMAIL))
            self.assertEqual(timeout, 300)
            payload = json.loads(request.data)
            self.assertEqual(payload['email'], EMAIL)
            self.assertEqual(payload['count'], 1)
            self.posts.append((path, payload))
            if self.network_error:
                raise self.network_error
            if path == '/images':
                letter = ('A', 'B')[self.image_count]
                self.image_count += 1
                media = image_media(letter)
                if self.encoded_image:
                    import base64
                    generated = media['image']['generatedImage']
                    generated.pop('fifeUrl')
                    generated['encodedImage'] = base64.b64encode(self.png).decode()
                result = {'jobId': 'image-' + letter, 'media': [media]}
            else:
                self.video_count += 1
                result = {'jobid': VIDEO_ID, 'type': 'video', 'status': 'created'}
            return io.BytesIO(json.dumps(result).encode())
        if method == 'GET' and path.startswith('/jobs/'):
            job_id = path.removeprefix('/jobs/')
            if job_id == VIDEO_ID:
                self.assertEqual(self.state()['video']['job_id'], VIDEO_ID)
                status = self.polls.pop(0) if self.polls else 'completed'
                result = {'jobid': VIDEO_ID, 'type': 'video', 'status': status}
                if status == 'completed':
                    result['response'] = {'media': [video_media(not self.no_video_url)]}
            else:
                letter = job_id[-1]
                self.assertEqual(self.state()['images'][letter]['job_id'], job_id)
                result = {'jobid': job_id, 'type': 'image', 'status': 'completed',
                          'response': {'media': [image_media(letter)]}}
            return io.BytesIO(json.dumps(result).encode())
        if method == 'GET' and path.startswith('/assets/'):
            return io.BytesIO(json.dumps({'url': 'https://flow-content.google/video/refreshed'}).encode())
        raise AssertionError((method, path))

    def generate(self, **kwargs):
        return flow.generate(self.episode, ffprobe='/mock/ffprobe', **kwargs)

    def test_approved_frames_reused_and_exactly_one_video_with_both_frames(self):
        self.approved_frames()
        before = [(self.episode/f'keyframes/{letter}.png').read_bytes() for letter in ('A', 'B')]
        result = self.generate()
        self.assertEqual(result, self.episode/'clips/01-hop-on.mp4')
        self.assertEqual(result.read_bytes(), b'MOCK VIDEO DOWNLOAD')
        self.assertEqual(self.image_count, 0)
        self.assertEqual(self.video_count, 1)
        payload = self.posts[0][1]
        self.assertTrue(payload['startImage'])
        self.assertTrue(payload['endImage'])
        self.assertNotEqual(payload['startImage'], payload['endImage'])
        self.assertTrue(payload['async'])
        self.assertEqual(payload['duration'], 8)
        self.assertEqual(payload['aspectRatio'], 'portrait')
        self.assertEqual(payload['model'], 'veo-3.1-lite')
        self.assertEqual(payload['resolution'], '720p')
        self.assertIn('wobble exactly once', payload['prompt'])
        self.assertIn('mouthless face', payload['prompt'])
        self.assertEqual(before, [(self.episode/f'keyframes/{letter}.png').read_bytes() for letter in ('A', 'B')])
        self.assertEqual(self.state()['verification']['width'], 720)
        self.assertNotIn('mock-secret-token', self.state_path.read_text() + self.output.getvalue())
        self.assertNotIn('Signature', self.state_path.read_text())
        self.assertNotIn('private-cookie-do-not-log', self.state_path.read_text() + self.output.getvalue())
        self.assertEqual(list((self.episode/'clips').iterdir()), [result])
        self.assertFalse((self.episode/'keyframes/D.png').exists())

    def test_missing_frames_are_named_before_any_api_call(self):
        for missing in (('A',), ('B',), ('A', 'B')):
            with self.subTest(missing=missing):
                self.approved_frames()
                for letter in missing:
                    (self.episode/f'keyframes/{letter}.png').unlink()
                with self.assertRaisesRegex(ValueError, 'Missing required keyframe') as error:
                    self.generate()
                for letter in missing:
                    self.assertIn(str(self.episode/f'keyframes/{letter}.png'), str(error.exception))
                self.assertEqual(self.calls, [])
                self.assertFalse(self.state_path.exists())

    def test_existing_frames_do_not_require_image_generation_inputs(self):
        (self.episode/'flow-image-prompts.md').unlink()
        self.generate()
        self.assertEqual(self.image_count, 0)
        self.assertEqual([endpoint for endpoint, _ in self.posts], ['/videos'])
        self.assertEqual(set(self.state()['uploads']), {'A', 'B'})

    def test_dry_run_checks_account_and_budget_without_mutation(self):
        self.generate(dry_run=True)
        self.assertEqual(self.calls, [('GET', '/accounts'), ('GET', '/accounts/' + EMAIL)])
        self.assertFalse((self.episode/'jobs').exists())
        self.assertFalse((self.episode/'clips').exists())
        self.assertIn('DRY RUN: would upload A/B and submit one portrait Veo 3.1 Lite video', self.output.getvalue())

    def test_dry_run_with_existing_output_checks_live_account_without_changing_state(self):
        self.generate()
        before = self.state_path.read_bytes()
        self.calls.clear()
        self.account['credits']['credits'] = 0
        self.generate(dry_run=True)
        self.assertEqual(self.calls, [('GET', '/accounts'), ('GET', '/accounts/' + EMAIL)])
        self.assertEqual(self.state_path.read_bytes(), before)
        self.assertEqual(self.video_count, 1)

    def test_unhealthy_missing_and_unknown_health_never_submit(self):
        for accounts in ({}, {EMAIL: {'health': 'Expired'}}, {EMAIL: {}}, {EMAIL: {'health': True}}):
            with self.subTest(accounts=accounts):
                self.accounts = accounts
                with self.assertRaisesRegex(RuntimeError, 'healthy'):
                    self.generate()
        self.assertEqual(self.posts, [])

    def test_health_is_rechecked_before_paid_job(self):
        self.approved_frames()
        original = self.http
        def expire_after_upload(request, timeout):
            result = original(request, timeout)
            if request.get_method() == 'POST':
                self.account['health'] = 'expired'
            return result
        with patch('google_flow.urlopen', side_effect=expire_after_upload):
            with self.assertRaisesRegex(RuntimeError, 'unhealthy'):
                self.generate()
        self.assertEqual(self.posts, [])

    def test_multiple_accounts_default_to_ignite(self):
        self.accounts['other@example.com'] = {'health': 'OK', 'backend': 'flow'}
        self.generate()
        self.assertEqual(self.state()['email'], EMAIL)
        self.assertEqual(self.video_count, 1)

    def test_missing_ignite_account_does_not_fall_back_to_another_account(self):
        self.accounts = {'other@example.com': {'health': 'OK', 'backend': 'flow'}}
        with self.assertRaisesRegex(RuntimeError, 'missing or unhealthy'):
            self.generate()
        self.assertFalse(any(method == 'POST' for method, _ in self.calls))

    def test_insufficient_credits_stop_before_uploads_or_images(self):
        self.account['credits']['credits'] = 9
        with self.assertRaisesRegex(RuntimeError, 'Insufficient Flow credits.*10 required'):
            self.generate()
        self.assertFalse(any(method == 'POST' for method, _ in self.calls))

    def test_invalid_or_missing_credit_balance_fails_closed(self):
        for balance in (None, '1000', True, float('nan'), -1):
            with self.subTest(balance=balance):
                self.account['credits']['credits'] = balance
                with self.assertRaisesRegex(RuntimeError, 'balance is unavailable'):
                    self.generate()
        self.assertFalse(any(method == 'POST' for method, _ in self.calls))

    def test_detail_health_is_checked_before_submitting_anything(self):
        self.account['health'] = 'expired'
        with self.assertRaisesRegex(RuntimeError, 'unhealthy'):
            self.generate()
        self.assertFalse(any(method == 'POST' for method, _ in self.calls))

    def test_ultra_credit_requirement_is_five(self):
        self.account['credits'] = {'credits': 4, 'userPaygateTier': 'PAYGATE_TIER_TWO'}
        with self.assertRaisesRegex(RuntimeError, '5 required'):
            self.generate()
        self.account['credits']['credits'] = 5
        self.generate()
        self.assertEqual(self.video_count, 1)

    def test_credit_balance_rechecked_before_generation(self):
        self.approved_frames()
        original = self.http
        def spent_elsewhere(request, timeout):
            result = original(request, timeout)
            if request.get_method() == 'POST':
                self.account['credits']['credits'] = 0
            return result
        with patch('google_flow.urlopen', side_effect=spent_elsewhere):
            with self.assertRaisesRegex(RuntimeError, 'Insufficient Flow credits'):
                self.generate()
        self.assertEqual(self.posts, [])

    def test_unknown_plan_fails_before_any_submission(self):
        self.account['credits']['userPaygateTier'] = 'UNKNOWN'
        with self.assertRaisesRegex(RuntimeError, 'cost is unavailable'):
            self.generate()
        self.assertFalse(any(method == 'POST' for method, _ in self.calls))

    def test_free_plan_uses_reported_first_last_frame_model_cost(self):
        self.account['credits'] = {'credits': 50, 'userPaygateTier': 'PAYGATE_TIER_NOT_PAID'}
        self.account['models'] = {'videoModels': [{
            'key': 'veo_3_1_interpolation_lite', 'creditCost': 10,
            'videoLengthSeconds': 8, 'resolution': '720p',
            'supportedAspectRatios': ['VIDEO_ASPECT_RATIO_PORTRAIT']}]}
        self.generate()
        self.assertEqual(self.video_count, 1)
        self.assertIn('50 Flow credits available', self.output.getvalue())
        self.assertIn('one Lite clip costs 10', self.output.getvalue())

    def test_reported_model_cost_is_checked_before_uploads(self):
        self.account['models'] = {'videoModels': [{
            'key': 'veo_3_1_interpolation_lite', 'creditCost': 1001,
            'videoLengthSeconds': 8, 'resolution': '720p',
            'supportedAspectRatios': ['VIDEO_ASPECT_RATIO_PORTRAIT']}]}
        with self.assertRaisesRegex(RuntimeError, '1001 required'):
            self.generate()
        self.assertFalse(any(method == 'POST' for method, _ in self.calls))

    def test_missing_token_does_not_contact_api(self):
        with patch.dict('os.environ', {'USEAPI_TOKEN': ''}):
            with self.assertRaisesRegex(ValueError, 'USEAPI_TOKEN'):
                self.generate()
        self.assertEqual(self.calls, [])

    def test_interrupt_after_submission_resumes_saved_id_without_second_post(self):
        self.approved_frames()
        with patch('google_flow.time.sleep', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.generate()
        self.assertEqual(self.state()['video']['job_id'], VIDEO_ID)
        # Resuming requires neither the original artwork nor unchanged prompts.
        (self.episode/'keyframes/A.png').unlink()
        (self.episode/'flow-video-prompts.md').write_text('edited while waiting')
        # A submitted job has already consumed its credits; polling needs no new budget.
        self.account['credits']['credits'] = 0
        self.generate()
        self.assertEqual(self.video_count, 1)

    def test_wait_timeout_resumes_without_second_submission(self):
        self.approved_frames()
        with patch('google_flow.time.monotonic', side_effect=[0, 2]):
            with self.assertRaisesRegex(RuntimeError, 'timed out'):
                self.generate(wait_timeout=1)
        self.generate()
        self.assertEqual(self.video_count, 1)

    def test_failed_job_is_never_replaced(self):
        self.approved_frames()
        self.polls = ['failed', 'failed']
        for _ in range(2):
            with self.assertRaisesRegex(RuntimeError, 'job failed'):
                self.generate()
        self.assertEqual(self.video_count, 1)
        self.assertFalse((self.episode/'clips/01-hop-on.mp4').exists())

    def test_lost_post_response_does_not_risk_duplicate_job(self):
        self.approved_frames()
        self.network_error = URLError('secret must not be logged')
        with self.assertRaisesRegex(RuntimeError, 'connection failed'):
            self.generate()
        self.network_error = None
        with self.assertRaisesRegex(RuntimeError, 'outcome needs review'):
            self.generate()
        self.assertEqual(len(self.posts), 1)
        self.assertNotIn('secret must not', self.output.getvalue())

    def test_bad_download_does_not_publish_and_saved_job_can_redownload(self):
        self.approved_frames()
        self.bad_video = True
        with self.assertRaisesRegex(ValueError, 'FFprobe rejected'):
            self.generate()
        self.assertFalse((self.episode/'clips/01-hop-on.mp4').exists())
        self.bad_video = False
        self.generate()
        self.assertEqual(self.video_count, 1)

    def test_missing_and_expired_video_url_resolved_without_new_job(self):
        self.approved_frames()
        self.no_video_url = True
        self.generate()
        self.assertTrue(any(path.startswith('/assets/user:') for method, path in self.calls if method == 'GET'))
        self.assertEqual(self.video_count, 1)

    def test_expired_signed_url_is_refreshed(self):
        self.approved_frames()
        original = self.http
        def expired_url(request, timeout):
            if 'Signature=temporary' in request.full_url:
                raise HTTPError(request.full_url, 403, 'expired', {}, None)
            return original(request, timeout)
        with patch('google_flow.urlopen', side_effect=expired_url):
            self.generate()
        self.assertEqual(self.video_count, 1)
        self.assertTrue(any(path.startswith('/assets/user:') for method, path in self.calls if method == 'GET'))

    def test_encoded_image_fallback(self):
        import base64
        media = {'image': {'generatedImage': {'encodedImage': base64.b64encode(self.png).decode()}}}
        target = self.episode/'encoded.png'
        run = flow.Generation(flow.FlowClient(), self.state_path, {}, 1, 1)
        run.download_media(media, 'image', target)
        self.assertEqual(target.read_bytes(), self.png)
        self.assertEqual(self.calls, [])

    def test_video_download_interruption_resumes_video_job(self):
        original = self.http
        def interrupt_download(request, timeout):
            if request.full_url.startswith('https://flow-content.google/video/'):
                raise URLError('interrupted download')
            return original(request, timeout)
        with patch('google_flow.urlopen', side_effect=interrupt_download):
            with self.assertRaisesRegex(RuntimeError, 'download interrupted'):
                self.generate()
        self.assertEqual(self.state()['video']['job_id'], VIDEO_ID)
        self.generate()
        self.assertEqual(self.video_count, 1)

    def test_existing_clip_is_preserved_and_verified_offline(self):
        target = self.episode/'clips/01-hop-on.mp4'
        target.parent.mkdir()
        target.write_bytes(b'EXISTING USER DOWNLOAD')
        with patch.dict('os.environ', {'USEAPI_TOKEN': ''}):
            self.generate()
        self.assertEqual(target.read_bytes(), b'EXISTING USER DOWNLOAD')
        self.assertEqual(self.calls, [])

    def test_changed_output_is_preserved_and_reported_as_collision(self):
        target = self.generate()
        target.write_bytes(b'USER REPLACEMENT')
        self.calls.clear()
        with self.assertRaisesRegex(ValueError, 'Differing filename collision'):
            self.generate()
        self.assertEqual(target.read_bytes(), b'USER REPLACEMENT')
        self.assertEqual(self.calls, [])

    def test_blocking_art_in_approved_slot_is_rejected(self):
        self.approved_frames()
        (self.episode/'keyframes/blocking/A.png').write_bytes(self.png)
        with self.assertRaisesRegex(ValueError, 'Blocking guide'):
            self.generate()
        self.assertEqual(self.posts, [])

    def test_missing_ffprobe_stops_before_api_work(self):
        with patch('google_flow.subprocess.run', side_effect=FileNotFoundError):
            with self.assertRaisesRegex(RuntimeError, 'FFprobe unavailable'):
                self.generate()
        self.assertEqual(self.calls, [])

    def test_collision_preserves_existing_media(self):
        source, target = Path(self.temp.name)/'source', Path(self.temp.name)/'target'
        source.write_bytes(b'new')
        target.write_bytes(b'approved')
        with self.assertRaisesRegex(ValueError, 'collision'):
            flow.publish(source, target)
        self.assertEqual(target.read_bytes(), b'approved')

    def test_concurrent_generator_cannot_submit(self):
        with flow.shot_lock(self.episode/'jobs/useapi'):
            with self.assertRaisesRegex(RuntimeError, 'Another'):
                self.generate()
        self.assertEqual(self.posts, [])

    def test_cli_dispatch_and_scope(self):
        with patch('google_flow.generate') as generate:
            self.assertEqual(main(['generate', str(self.episode), '--shot', 'A-B', '--dry-run']), 0)
            self.assertEqual(generate.call_args.args[:2], (self.episode, 'A-B'))
            self.assertEqual(generate.call_args.kwargs, {'dry_run': True})
        with self.assertRaisesRegex(ValueError, 'only calculus_pilot'):
            flow.generate(self.episode.parent/'other')


class RealFFprobeTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg/FFprobe required')
    def test_real_mp4_and_invalid_download(self):
        (WORKFLOW/'.cache').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='test-probe-', dir=WORKFLOW/'.cache') as temporary:
            video = Path(temporary)/'test.mp4'
            subprocess.run([shutil.which('ffmpeg'), '-v', 'error', '-f', 'lavfi',
                            '-i', 'color=c=orange:s=720x1280:r=24:d=4', '-c:v', 'libx264',
                            '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', str(video)], check=True)
            binary = flow.ffprobe_path()
            result = flow.verify_mp4(video, binary)
            self.assertEqual(result['width'], 720)
            self.assertEqual(result['height'], 1280)
            self.assertAlmostEqual(result['duration_sec'], 4)
            video.write_text('<html>not a video</html>')
            with self.assertRaisesRegex(ValueError, 'FFprobe rejected'):
                flow.verify_mp4(video, binary)


if __name__ == '__main__':
    unittest.main()
