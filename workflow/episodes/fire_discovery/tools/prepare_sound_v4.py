"""Add the requested lightning sting, audible music and a longer ending."""
import hashlib
import json
import shutil
import subprocess
import wave
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
WORKFLOW = EP.parents[1]
REVIEW = EP / "reviews/sound-v4"
AUDIO = EP / "audio/sound-v4"
CLIPS = EP / "clips/edit-v4"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args):
    subprocess.run(args, check=True)


def wav_read(path):
    with wave.open(str(path)) as w:
        return w.getparams(), w.readframes(w.getnframes())


def wav_write(path, params, data):
    if path.exists():
        raise FileExistsError(path)
    with wave.open(str(path), "wb") as w:
        w.setparams(params)
        w.writeframes(data)


def frame_hashes(path):
    text = subprocess.check_output([
        "ffmpeg", "-v", "error", "-nostdin", "-i", str(path),
        "-map", "0:v:0", "-pix_fmt", "yuv420p", "-f", "framemd5", "-",
    ], text=True)
    return [s.split(",")[-1].strip() for s in text.splitlines()
            if s and not s.startswith("#")]


def main():
    for directory in [REVIEW, AUDIO, CLIPS]:
        directory.mkdir(parents=True, exist_ok=True)
    prior = REVIEW / "prior-state"
    prior.mkdir(exist_ok=True)
    for name in ["edit.json", "script.txt", "shot-plan.json", "higgsfield-prompts.txt",
                 "audio/voice-cues.json", "handoff.txt", "handoff-validation.json"]:
        target = prior / Path(name).name
        if target.exists():
            raise FileExistsError(target)
        shutil.copy2(EP / name, target)
    edit = json.loads((EP / "edit.json").read_text())

    # Insert a 1.2-second gap inside the existing silence after "Yes". Every
    # spoken sample stays unchanged; the sting plays at the original bolt.
    params, data = wav_read(EP / "audio/trimmed-v2/03-02-narrator.wav")
    sample_bytes = params.nchannels * params.sampwidth
    split = round(.4 * params.framerate) * sample_bytes
    pause = b"\0" * (round(1.2 * params.framerate) * sample_bytes)
    narrator = AUDIO / "03-02-narrator-with-sting-gap.wav"
    wav_write(narrator, params, data[:split] + pause + data[split:])
    assert wav_read(narrator)[1] == data[:split] + pause + data[split:]
    # Restore the original quiet word release, instead of padding the earlier
    # aggressively shortened derivative. Keep 0.9 seconds at normal speed.
    right_params, right_data = wav_read(EP / "audio/05-02-narrator.wav")
    right = AUDIO / "05-02-narrator-full-release.wav"
    right_bytes = round(.9 * right_params.framerate) * right_params.nchannels * right_params.sampwidth
    wav_write(right, right_params, right_data[:right_bytes])

    sound_source = WORKFLOW / "assets/meme sounds/bomboclat-with-thunder.mp3"
    sting = AUDIO / "bomboclat-with-thunder.wav"
    run(["ffmpeg", "-v", "error", "-nostdin", "-n", "-i", str(sound_source),
         "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(sting)])
    sting_params, _ = wav_read(sting)
    sting_duration = sting_params.nframes / sting_params.framerate
    duration = 25.8
    music_source = WORKFLOW / "assets/music/Hide and Sneak 4.mp3"
    music = AUDIO / "hide-and-sneak-bed.wav"
    run(["ffmpeg", "-v", "error", "-nostdin", "-n", "-i", str(music_source),
         "-t", str(duration), "-af",
         "volume=0.1,afade=t=in:st=0:d=0.35,afade=t=out:st=24.6:d=1.2,"
         "volume=0.5:enable='between(t,9.65,10.85)'",
         "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(music)])

    # Extend the lightning scene using actual remaining source footage.
    tree_source = EP / "clips/03-scene-omni-v2-bolt-trim.mp4"
    tree = CLIPS / "03-lightning-with-sting-gap.mp4"
    run(["ffmpeg", "-v", "error", "-nostdin", "-n", "-ss", "1.2",
         "-i", str(tree_source), "-map", "0:v:0", "-an", "-frames:v", "206",
         "-c:v", "copy", "-avoid_negative_ts", "make_zero", "-movflags", "+faststart", str(tree)])
    assert frame_hashes(tree) == frame_hashes(tree_source)[36:242]
    # End on the same clean listening pose for 22 extra frames. Repeating a
    # complete pair preserves the exact on-twos cadence and avoids new artifacts.
    ending_source = EP / "clips/edit-v3/05-clean-holds-v3.mp4"
    ending = CLIPS / "05-extended-ending.mp4"
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-nostdin", "-i", str(ending_source),
        "-map", "0:v:0", "-pix_fmt", "yuv420p", "-f", "rawvideo", "-",
    ])
    frame_bytes = 1080 * 1920 * 3 // 2
    assert len(raw) == 134 * frame_bytes
    enc = subprocess.Popen([
        "ffmpeg", "-v", "error", "-nostdin", "-n", "-f", "rawvideo",
        "-pix_fmt", "yuv420p", "-s", "1080x1920", "-r", "30", "-i", "-",
        "-an", "-c:v", "libx264", "-preset", "fast", "-qp", "0", "-g", "1",
        "-bf", "0", "-movflags", "+faststart", str(ending),
    ], stdin=subprocess.PIPE)
    enc.communicate(raw + raw[-2 * frame_bytes:] * 11)
    assert enc.returncode == 0
    ending_hashes = frame_hashes(ending)
    original_hashes = frame_hashes(ending_source)
    assert ending_hashes == original_hashes + original_hashes[-2:] * 11
    assert all(ending_hashes[i] == ending_hashes[i+1] for i in range(0, 156, 2))
    edit["shots"][2]["scene"]["src"] = str(tree.relative_to(EP))
    edit["shots"][2]["duration"] = 206 / 30
    edit["shots"][4]["scene"]["src"] = str(ending.relative_to(EP))
    edit["shots"][4]["duration"] = 156 / 30
    edit["audioTracks"] = [t for t in edit["audioTracks"] if t["speaker"] != "Music"]
    for track in edit["audioTracks"]:
        if track["id"] == "03-02-narrator":
            track.update(src=str(narrator.relative_to(EP)), duration=params.nframes / params.framerate + 1.2, source_sha256=sha(narrator))
        if track["id"].startswith(("04-", "05-")):
            track["start"] = round(track["start"] + 1.2, 6)
        if track["id"] == "05-02-narrator":
            track.update(src=str(right.relative_to(EP)), duration=.9, source_sha256=sha(right))
    for caption in edit["captions"]:
        if caption["start"] >= 9.6895:
            caption["start"] = round(caption["start"] + 1.2, 6)
            caption["end"] = round(caption["end"] + 1.2, 6)
        if caption["text"] == "Right.":
            caption["end"] = 25.7
    edit["audioTracks"].extend([
        {"id": "lightning-bomboclat", "speaker": "Sound effect", "src": str(sting.relative_to(EP)),
         "start": 292 / 30, "duration": sting_duration, "trimBefore": 0, "volume": .55,
         "playbackRate": 1, "source_sha256": sha(sting)},
        {"id": "music-bed-v4", "speaker": "Music", "src": str(music.relative_to(EP)),
         "start": 0, "duration": duration, "trimBefore": 0, "volume": 1,
         "playbackRate": 1, "source_sha256": sha(music)},
    ])
    edit["timing"] = {"confirmed": False, "note": "25.8-second sound review: meme starts at the lightning pair, frame292;1.2s narration gap after Yes; music at an audible background level; original Right release restored and ending held. All speech at1x. Final playback review separate."}
    for name in ["edit.json", "edit-sound-v4.json"]:
        (EP / name).write_text(json.dumps(edit, indent=2, ensure_ascii=False) + "\n")
    receipt = {
        "user_request": "Bomboclat sound at lightning, background music, extend the ending so Right is not cut off.",
        "lightning_frame": 292, "lightning_sec": 292 / 30,
        "sting_source": str(sound_source.relative_to(WORKFLOW)), "sting_source_sha256": sha(sound_source),
        "sting_duration_sec": sting_duration, "sting_volume": .55,
        "music_source": str(music_source.relative_to(WORKFLOW)), "music_source_sha256": sha(music_source),
        "music_processing": "Source gain0.1,0.35s fade-in,1.2s fade-out,6dB dip during sting; edit gain1. Previous quiet bed replaced, not stacked.",
        "narrator_gap": {"utterance": "03-02-narrator", "source_split_sec": .4, "inserted_silence_sec": 1.2, "original_spoken_samples_preserved": True},
        "right_release": {"source": "audio/05-02-narrator.wav", "kept_sec": .9, "unchanged_source_prefix": True},
        "tree_source_exact_frames": [36, 241], "tree_output_frames": 206,
        "ending_original_frames": 134, "ending_added_hold_frames": 22, "ending_pair_mismatches": [],
        "new_duration_sec": duration, "new_frames": 774,
        "status": "Prepared; export verification pending.",
    }
    (REVIEW / "sound-edit-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print("Prepared774 frames/25.8s; lightning sting at9.733s, audible music, extended Right release.", flush=True)


if __name__ == "__main__":
    main()
