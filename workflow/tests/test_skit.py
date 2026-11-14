import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from paths import WORKFLOW
from shorts import prepare, check
from skit import sync_audio


class SkitTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='skit-test-',dir=WORKFLOW/'episodes')
        self.episode=Path(self.temp.name)/'new_skit'

    def tearDown(self):self.temp.cleanup()

    def test_new_episode_uses_generated_clips_and_verified_cast(self):
        edit=prepare(self.episode)
        self.assertEqual(edit['layout'],'fullscreen')
        self.assertEqual(sum(s['duration'] for s in edit['shots']),30)
        self.assertTrue(all(s['scene']['type']=='video' for s in edit['shots']))
        self.assertEqual(edit['cast']['Sol']['voice_type'],'element')
        self.assertEqual(edit['cast']['Narrator']['voice'],'Arthur')
        self.assertTrue(edit['cast']['Narrator']['voice_id'])
        self.assertFalse((self.episode/'layers').exists())
        self.assertFalse((self.episode/'flow-image-prompts.md').exists())
        self.assertEqual((self.episode/'public/clips').resolve(),self.episode/'clips')

    def test_prepare_preserves_script_prompts_media_and_edits(self):
        prepare(self.episode)
        paths=['script.txt','higgsfield-prompts.txt','clips/01-scene.mp4','edit.json']
        for name in paths[:3]:(self.episode/name).write_bytes(b'user work')
        before={name:(self.episode/name).read_bytes() for name in paths}
        prepare(self.episode)
        self.assertEqual(before,{name:(self.episode/name).read_bytes() for name in paths})

    def test_skit_media_check_does_not_request_cub_or_calculus(self):
        prepare(self.episode)
        report=check(self.episode,images=True)
        self.assertFalse(report['final_ready'])
        kinds=[m['kind'] for m in report['missing']]
        self.assertIn('SEPARATE VOICE TAKES',kinds)
        self.assertEqual(kinds.count('KEYFRAME'),2)
        self.assertNotIn('mogofun',json.dumps(report))
        self.assertNotIn('graph',json.dumps(report))

    def test_measured_takes_extend_scene_without_speeding_speech_or_confirming_cues(self):
        plan={'title':'Test','clips':[{'id':'01','start_sec':0,'end_sec':3,
              'dialogue':[{'speaker':'Sol','text':'One natural sentence.'},{'speaker':'Narrator','text':'A connected answer.'}]}]}
        self.episode.mkdir(parents=True)
        (self.episode/'shot-plan.json').write_text(json.dumps(plan))
        prepare(self.episode)
        for name in ('01-01-sol.wav','01-02-narrator.wav'):(self.episode/'audio'/name).write_bytes(b'actual downloaded take')
        with patch('skit.probe',return_value={'format':{'duration':'4'},'streams':[{'codec_type':'audio'}]}):
            result=sync_audio(self.episode)
        edit=json.loads((self.episode/'edit.json').read_text())
        self.assertGreater(result['duration_sec'],8)
        self.assertFalse(edit['timing']['confirmed'])
        self.assertEqual(len(edit['audioTracks']),2)
        self.assertTrue(all(t['playbackRate']==1 for t in edit['audioTracks']))
        self.assertNotEqual(edit['audioTracks'][0]['start'],edit['audioTracks'][1]['start'])
        edit['timing']['confirmed']=True
        (self.episode/'edit.json').write_text(json.dumps(edit))
        (self.episode/'audio/01-01-sol.wav').write_bytes(b'replacement')
        self.assertTrue(any('hash' in error for error in check(self.episode)['errors']))

    def test_conflicting_public_media_directory_is_preserved(self):
        (self.episode/'public/clips').mkdir(parents=True)
        target=self.episode/'public/clips/download.mp4';target.write_bytes(b'keep me')
        with self.assertRaisesRegex(ValueError,'preserved'):prepare(self.episode)
        self.assertEqual(target.read_bytes(),b'keep me')

if __name__=='__main__':unittest.main()
