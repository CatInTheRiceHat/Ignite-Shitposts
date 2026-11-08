import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
from paths import WORKFLOW, episode_path, clip_path, voice_paths
from shorts import prepare, check
from calculus_edit import Graph, validate


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        (WORKFLOW/'.cache').mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(prefix='test-',dir=WORKFLOW/'.cache')
        self.episode=Path(self.temp.name)/'episode'

    def tearDown(self):
        self.temp.cleanup()

    def test_prepare_uses_30_second_default_without_ffmpeg(self):
        with patch('subprocess.run',side_effect=AssertionError('prepare must not need FFmpeg')):
            edit=prepare(self.episode)
        self.assertEqual(edit['duration_sec'],30)
        self.assertEqual(edit['cues'][-1]['end'],30)
        self.assertEqual(edit['narrator']['voice'],'Cub (Female)')
        self.assertEqual(json.loads((self.episode/'shot-plan.json').read_text())['sequence'],['A','B','C','D'])
        self.assertTrue((self.episode/'keyframes/C.png').is_file())

    def test_prepare_preserves_edits_and_downloads(self):
        prepare(self.episode,15)
        edits={'narration.txt':'User narration edit\n','flow-image-prompts.md':'User image prompt\n',
               'flow-video-prompts.md':'User video prompt\n','clips/01-hop-on.mp4':b'USER DOWNLOAD'}
        for name,data in edits.items():
            p=self.episode/name
            p.write_bytes(data if isinstance(data,bytes) else data.encode())
        before={name:(self.episode/name).read_bytes() for name in edits}
        config=(self.episode/'edit.json').read_bytes()
        prepare(self.episode)
        self.assertEqual(before,{name:(self.episode/name).read_bytes() for name in edits})
        self.assertEqual(config,(self.episode/'edit.json').read_bytes())

    def test_missing_media_reports_exact_canonical_paths(self):
        prepare(self.episode,15)
        report=check(self.episode)
        paths={item['path'] for item in report['missing']}
        self.assertIn(str(self.episode/'clips/01-hop-on.mp4'),paths)
        self.assertIn(str(self.episode/'audio/mogofun-narration.mp3'),paths)
        self.assertEqual(len(paths),4)

    def test_legacy_import_paths_remain_readable(self):
        (self.episode/'imports').mkdir(parents=True)
        clip=self.episode/'imports/01-hop-on.mp4';clip.write_bytes(b'clip')
        voice=self.episode/'imports/mogofun-narration.wav';voice.write_bytes(b'voice')
        self.assertEqual(clip_path(self.episode,clip.name),clip)
        self.assertEqual(voice_paths(self.episode),[voice])

    def test_changed_voiceover_invalidates_confirmation(self):
        edit=prepare(self.episode,15)
        for item in edit['clips'].values():(self.episode/'clips'/item['file']).write_bytes(b'fixture')
        voice=self.episode/'audio/mogofun-narration.wav';voice.write_bytes(b'replacement audio')
        cues={'confirmed':True,'source_sha256':hashlib.sha256(b'old recording').hexdigest(),
              'cues':edit['cues'],'tangent_reveal_sec':edit['tangent_reveal_sec']}
        (self.episode/'audio/voiceover-cues.json').write_text(json.dumps(cues))
        report=check(self.episode)
        self.assertFalse(report['final_ready'])
        self.assertTrue(any('hash' in error for error in report['errors']))

    def test_exact_graph_and_invalid_timing(self):
        edit=prepare(self.episode,15)
        graph=Graph(edit['graph'])
        self.assertEqual(graph.point(1,1),(360,760))
        self.assertEqual(graph.slope,.5)
        self.assertEqual(graph.tangent()[0],graph.point(0,.5))
        changed=copy.deepcopy(edit);changed['tangent_reveal_sec']=1
        with self.assertRaises(ValueError):validate(changed)

    def test_episode_name_is_resolved_from_workflow(self):
        self.assertEqual(episode_path('calculus_pilot'),WORKFLOW/'episodes/calculus_pilot')


if __name__=='__main__':
    unittest.main()
