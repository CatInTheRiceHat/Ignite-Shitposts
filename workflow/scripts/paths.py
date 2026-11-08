"""Stable workflow/episode paths, independent of the current working directory."""
import json
import os
from pathlib import Path
import shutil
import subprocess

WORKFLOW = Path(__file__).resolve().parents[1]
REPO = WORKFLOW.parent


def settings(name):
    return json.loads((WORKFLOW/'config'/f'{name}.json').read_text())


def episode_path(value='calculus_pilot'):
    value = Path(value)
    if value.is_absolute():
        return value.resolve()
    if len(value.parts) == 1:
        return (WORKFLOW/'episodes'/value).resolve()
    if value.exists():
        return value.resolve()
    candidate = REPO/value
    if candidate.exists():
        return candidate.resolve()
    return (WORKFLOW/'episodes'/value).resolve()


def clip_path(episode, name):
    canonical = episode/'clips'/name
    legacy = episode/'imports'/name
    return canonical if canonical.is_file() or not legacy.is_file() else legacy


def voice_paths(episode):
    found = []
    for folder in ('audio', 'imports'):
        for ext in ('.mp3', '.wav', '.m4a'):
            path = episode/folder/('mogofun-narration'+ext)
            if path.is_file() and path.resolve() not in [p.resolve() for p in found]:
                found.append(path)
    return found


def cue_path(episode):
    canonical = episode/'audio/voiceover-cues.json'
    legacy = episode/'imports/voiceover-cues.json'
    return canonical if canonical.is_file() or not legacy.is_file() else legacy


def ffmpeg_path(explicit=None):
    candidate = explicit or os.environ.get('FFMPEG_PATH') or shutil.which('ffmpeg')
    if not candidate:
        raise RuntimeError('FFmpeg not found. Install ffmpeg or pass --ffmpeg /full/path/to/ffmpeg.')
    try:
        result = subprocess.run([str(candidate), '-version'], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError(f'FFmpeg blocked/unavailable at {candidate}: {type(error).__name__}: {error}') from error
    if result.returncode:
        raise RuntimeError(f'FFmpeg failed at {candidate}: exit {result.returncode}: {result.stderr.strip()}')
    return str(candidate)
