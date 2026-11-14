import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from paths import WORKFLOW
import clip_review as review


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg required')
class ClipReviewTests(unittest.TestCase):
    def setUp(self):
        (WORKFLOW / '.cache').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='review-test-', dir=WORKFLOW / '.cache')
        self.episode = Path(self.temp.name)
        (self.episode / 'keyframes').mkdir()
        (self.episode / 'clips').mkdir()
        (self.episode / 'public').mkdir()
        (self.episode / 'public/clips').symlink_to('../clips', target_is_directory=True)
        for name in ('first', 'last', 'reference'):
            Image.new('RGB', (64, 112), '#F07B2A').save(self.episode / 'keyframes' / (name + '.png'))
        self.clip = self.episode / 'clips/01.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                        'color=c=orange:s=64x112:r=8:d=1', '-c:v', 'libx264', '-pix_fmt',
                        'yuv420p', str(self.clip)], check=True, capture_output=True)
        self.plan = {'art_direction_reference': {
            'still': str(self.episode / 'keyframes/reference.png'), 'motion': str(self.clip)},
            'clips': [{'id': '01', 'start_sec': 0, 'end_sec': 3, 'sol_visible': True,
                       'first_frame': 'One planted pose.', 'last_frame': 'Same pose.',
                       'action': 'A test hold.', 'video_prompt': 'Test footage.',
                       'planned_outputs': {'first': 'keyframes/first.png', 'last': 'keyframes/last.png',
                                           'video': 'clips/01.mp4'}}]}
        self.save_plan()

    def tearDown(self):
        self.temp.cleanup()

    def save_plan(self):
        (self.episode / 'shot-plan.json').write_text(json.dumps(self.plan))

    def approve(self):
        review.prepare(self.episode, '01', 'frames')
        review.approve_frames(self.episode, '01', 'TEST USER: I approve both displayed test frames.')

    def packet_and_report(self):
        result = review.prepare(self.episode, '01', 'clip')
        packet = review.read(result['packet'])
        report = {'packet_id': packet['packet_id'], 'reviewer': 'independent-test-reviewer',
                  'method': 'Offline test decision over synthetic test evidence, not production media.',
                  'coverage_reviewed': packet['coverage']['sequence_pages'],
                  'checks': {name: {'verdict': 'pass', 'observed': 'Synthetic fixture inspection.',
                                   'timestamps_sec': [0], 'evidence': ['evidence/frame-comparison.jpg']}
                             for name in packet['contract']['policy']['checks']}}
        return packet, report

    def test_preparing_images_never_approves_them_or_allows_video_request(self):
        review.prepare(self.episode, '01', 'frames')
        self.assertFalse(review.frame_gate(self.episode, '01')['approved'])
        with self.assertRaisesRegex(ValueError, 'VIDEO BLOCKED'):
            review.video_request(self.episode, '01', 'start-id', 'end-id')
        with self.assertRaises(ValueError):
            review.approve_frames(self.episode, '01', '')

    def test_approved_payload_uses_canonical_omni_and_both_frames(self):
        self.approve()
        payload = review.video_request(self.episode, '01', 'approved-first-id', 'approved-last-id')
        self.assertEqual(payload['params']['model'], 'gemini_omni_flash_1_2')
        self.assertEqual(payload['params']['mode'], 'image-to-video')
        self.assertEqual([m['role'] for m in payload['params']['medias']], ['start_image', 'end_image'])
        self.assertFalse(payload['submission_performed'])

    def test_changed_frame_reference_or_contract_invalidates_user_approval(self):
        for mutation in ('last', 'reference', 'contract'):
            with self.subTest(mutation=mutation):
                self.approve()
                if mutation == 'contract':
                    self.plan['clips'][0]['action'] += ' Changed requirement.'
                    self.save_plan()
                else:
                    Image.new('RGB', (64, 112), '#001122').save(self.episode / f'keyframes/{mutation}.png')
                self.assertFalse(review.frame_gate(self.episode, '01')['approved'])

    def test_paired_frame_duration_over_ten_is_not_silently_submitted(self):
        self.plan['clips'][0]['end_sec'] = 11
        self.save_plan()
        self.approve()
        with self.assertRaisesRegex(ValueError, 'Split this scene'):
            review.video_request(self.episode, '01', 'start-id', 'end-id')

    def test_evidence_contains_every_source_frame_with_actual_timestamps(self):
        packet, _ = self.packet_and_report()
        self.assertEqual(packet['coverage']['source_frames'], 8)
        self.assertTrue(packet['coverage']['all_frames_extracted'])
        ctx = review.context(self.episode, '01', 'clip')
        index = review.read(ctx['directory'] / packet['coverage']['source_timestamps'])
        self.assertEqual([f['time_sec'] for f in index], [i / 8 for i in range(8)])
        self.assertEqual(packet['coverage']['full_resolution_samples'][-1]['index'], 7)
        self.assertEqual(packet['technical']['decode'], 'passed')
        self.assertFalse(review.clip_gate(self.episode, '01')['approved'])

    def test_clip_pass_requires_user_frame_approval(self):
        _, report = self.packet_and_report()
        with self.assertRaisesRegex(ValueError, 'User approval'):
            review.record_review(self.episode, '01', report)

    def test_uncertain_or_failed_check_blocks_production(self):
        self.approve()
        _, report = self.packet_and_report()
        for verdict in ('uncertain', 'fail'):
            report['checks']['object_continuity']['verdict'] = verdict
            recorded = review.record_review(self.episode, '01', report)
            self.assertEqual(recorded['decision'], 'rejected')
            self.assertFalse(review.clip_gate(self.episode, '01')['approved'])

    def test_missing_check_coverage_timestamp_or_evidence_cannot_pass(self):
        self.approve()
        _, original = self.packet_and_report()
        for case in ('check', 'coverage', 'timestamp', 'evidence', 'generator'):
            with self.subTest(case=case):
                report = copy.deepcopy(original)
                if case == 'check': del report['checks']['eyes']
                if case == 'coverage': report['coverage_reviewed'] = []
                if case == 'timestamp': report['checks']['eyes']['timestamps_sec'] = [99]
                if case == 'evidence': report['checks']['eyes']['evidence'] = ['evidence/missing.jpg']
                if case == 'generator': report['reviewer'] = 'generator'
                with self.assertRaises(ValueError): review.record_review(self.episode, '01', report)

    def test_pass_is_bound_to_clip_and_actual_evidence_bytes(self):
        self.approve()
        _, report = self.packet_and_report()
        review.record_review(self.episode, '01', report)
        self.assertTrue(review.clip_gate(self.episode, '01')['approved'])
        ctx = review.context(self.episode, '01', 'clip')
        evidence = ctx['directory'] / 'evidence/frame-comparison.jpg'
        evidence.write_bytes(evidence.read_bytes() + b'changed')
        self.assertFalse(review.clip_gate(self.episode, '01')['approved'])

    def test_final_edit_uses_selected_video_not_different_reviewed_take(self):
        self.approve()
        _, report = self.packet_and_report()
        review.record_review(self.episode, '01', report)
        edit = {'shots': [{'id': '01', 'scene': {'type': 'video', 'src': 'clips/01.mp4'}}]}
        self.assertTrue(review.edit_gate(self.episode, edit)['approved'])
        other = self.episode / 'clips/other.mp4'
        other.write_bytes(self.clip.read_bytes() + b'another take')
        edit['shots'][0]['scene']['src'] = 'clips/other.mp4'
        self.assertFalse(review.edit_gate(self.episode, edit)['approved'])


if __name__ == '__main__':
    unittest.main()
