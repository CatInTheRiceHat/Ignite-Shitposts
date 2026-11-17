"""Behavior checks for the shared video inspection tool; no episode-specific scripts."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import video_inspect as inspect

try:
    import numpy as np
    import cv2
except ImportError:
    np=cv2=None


@unittest.skipUnless(np is not None and cv2 is not None,'Install workflow/requirements.txt')
class ScreeningTests(unittest.TestCase):
    def test_static_scene_has_no_candidates(self):
        frames=np.full((30,192,192,3),170,dtype='uint8')
        events,coverage=inspect.screen_frames(frames,[i/30 for i in range(30)])
        self.assertEqual(events,[])
        self.assertEqual(coverage['analyzed_frames'],30)

    def test_brief_mark_between_held_frames_is_found(self):
        frames=np.full((30,192,192,3),170,dtype='uint8')
        frames[12:14,100:106,90:102]=20
        times=[i/30 for i in range(30)]
        events,_=inspect.screen_frames(frames,times)
        hits=[e for e in events if e['frame_start']<=12<=e['frame_end']
              and e['box'][0]<=95/192<=e['box'][0]+e['box'][2]
              and e['box'][1]<=103/192<=e['box'][1]+e['box'][3]]
        self.assertTrue(hits,'A two-frame added mark should not disappear among longer holds.')
        self.assertAlmostEqual(hits[0]['start'],.4)

    def test_global_flash_is_context_not_many_blemishes(self):
        frames=np.full((30,192,192,3),90,dtype='uint8');frames[12:14]=240
        events,_=inspect.screen_frames(frames,[i/30 for i in range(30)])
        self.assertTrue(events)
        self.assertTrue(all(e['kind']=='flash_or_cut' and e['priority']=='context' for e in events))


@unittest.skipUnless(np is not None and cv2 is not None and shutil.which('ffmpeg') and shutil.which('ffprobe'),
                     'OpenCV, NumPy and FFmpeg required')
class VideoIntegrationTests(unittest.TestCase):
    def setUp(self):
        (inspect.WORKFLOW/'.cache').mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(prefix='inspect-test-',dir=inspect.WORKFLOW/'.cache')
        self.root=Path(self.temp.name)

    def tearDown(self):self.temp.cleanup()

    def video(self,name,frames):
        path=self.root/name
        subprocess.run(['ffmpeg','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','192x192',
                        '-r','30','-i','-','-c:v','libx264rgb','-crf','0',str(path)],
                       input=frames.tobytes(),check=True,capture_output=True)
        return path

    def test_report_contains_real_evidence_and_preserves_source(self):
        frames=np.full((30,192,192,3),170,dtype='uint8');frames[12:14,100:106,90:102]=20
        path=self.video('mark.mp4',frames);before=inspect.sha(path);output=self.root/'report'
        inspect.scan(path,output,width=192,check_twos=True)
        report=json.loads((output/'report.json').read_text())
        self.assertEqual(inspect.sha(path),before)
        self.assertEqual(inspect.sha(output/report['video_url']),before)
        self.assertFalse(report['automatic_approval'])
        self.assertTrue(report['cadence']['passed'])
        self.assertEqual(report['coverage']['analyzed_frames'],30)
        self.assertTrue(report['overview_pages'])
        self.assertTrue((output/report['events'][0]['native_frame']).is_file())
        self.assertTrue((output/'summary.txt').is_file())
        self.assertFalse((output/'index.html').exists())
        self.assertEqual(inspect.scan(path,output,width=192,check_twos=True),output)
        with self.assertRaises(FileExistsError):inspect.scan(path,output,width=192,threshold=20)

    def test_single_frame_change_fails_exact_pair_cadence(self):
        frames=np.full((30,192,192,3),170,dtype='uint8');frames[13,100:106,90:102]=20
        path=self.video('broken-pair.mp4',frames)
        result=inspect.cadence_check(path,30,[i/30 for i in range(30)])
        self.assertFalse(result['passed']);self.assertIn(12,result['mismatched_pair_start_frames'])

    def test_nonuniform_timestamps_do_not_pass_on_twos(self):
        frames=np.full((30,192,192,3),170,dtype='uint8')
        path=self.video('held.mp4',frames)
        irregular=[i/30+(.1 if i>=12 else 0) for i in range(30)]
        self.assertFalse(inspect.cadence_check(path,30,irregular)['passed'])


if __name__=='__main__':unittest.main()
