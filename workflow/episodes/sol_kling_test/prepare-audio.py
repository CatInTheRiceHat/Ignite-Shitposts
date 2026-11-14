"""Build a four-second Sol audition mix from the downloaded custom voice take.

Usage: python3 workflow/episodes/sol_kling_test/prepare-audio.py
All foley here is synthesized draft sound design; the original voice is preserved.
"""

from array import array
from pathlib import Path
import hashlib
import json
import math
import os
import random
import shutil
import subprocess
import tempfile
import wave

EPISODE = Path(__file__).resolve().parent
WORKFLOW = EPISODE.parents[1]
FFMPEG = os.environ.get("FFMPEG_PATH", "ffmpeg")
FFPROBE = os.environ.get("FFPROBE_PATH", "ffprobe")
RATE = 48000
DURATION = 4


def run(arguments):
    return subprocess.run(
        [str(arg) for arg in arguments], check=True, capture_output=True, text=True
    )


def probe(file):
    return json.loads(run([FFPROBE, "-v", "error", "-show_format", "-show_streams", "-of", "json", file]).stdout)


def process_audio(source, output, filters, *, start=0):
    run([FFMPEG, "-y", "-v", "error", "-ss", start, "-i", source,
         "-vn", "-af", filters, "-ar", RATE, "-ac", 2, "-c:a", "pcm_s16le", output])


def write_stem(file, samples, peak_db):
    peak = max(abs(sample) for sample in samples) or 1
    gain = 10 ** (peak_db / 20) / peak
    pcm = array("h", (max(-32768, min(32767, round(sample * gain * 32767))) for sample in samples))
    with wave.open(str(file), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(RATE)
        audio.writeframes(pcm.tobytes())


def draft_foley(directory):
    rng = random.Random(417)
    length = RATE * DURATION
    ambience = [0.0] * length
    rustle = [0.0] * length
    low = 0.0
    for index in range(length):
        low = 0.985 * low + 0.015 * rng.uniform(-1, 1)
        fade = min(1, index / (RATE * 0.15), (length - index) / (RATE * 0.25))
        ambience[index] = low * fade
    # Quiet flame ticks, with shaped envelopes rather than sharp digital clicks.
    for _ in range(28):
        start = rng.randrange(int(0.1 * RATE), int(3.75 * RATE))
        count = rng.randrange(int(0.008 * RATE), int(0.03 * RATE))
        for offset in range(count):
            envelope = math.sin(math.pi * offset / count) ** 2
            ambience[start + offset] += rng.uniform(-0.1, 0.1) * envelope
    # Paper movement follows the observed start of the lantern lift.
    for start, duration, strength in [(2.42, 0.24, 0.65), (2.61, 0.28, 1), (2.83, 0.24, 0.4)]:
        count = round(duration * RATE)
        previous = 0.0
        for offset in range(count):
            white = rng.uniform(-1, 1)
            high = white - previous * 0.75
            previous = white
            envelope = math.sin(math.pi * offset / count) ** 2
            texture = 0.6 + 0.4 * math.sin(offset / RATE * 2 * math.pi * 27) ** 2
            rustle[round(start * RATE) + offset] += high * envelope * strength * texture
    write_stem(directory / "night-ambience.wav", ambience, -39)
    write_stem(directory / "lantern-rustle.wav", rustle, -30)


def main():
    settings = json.loads((EPISODE / "audio-test.json").read_text())
    source = EPISODE / settings["narration"]["source"]
    music = WORKFLOW / "assets/music/Hide and Sneak 4.mp3"
    if not source.is_file() or not music.is_file():
        raise SystemExit(f"Required inputs: {source} and {music}")
    cache = EPISODE / ".cache"
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="audio-", dir=cache) as temporary:
        scratch = Path(temporary)
        defaults = json.loads((WORKFLOW / "config/narration.json").read_text())
        tempo = settings["narration"].get("playback_rate", defaults["playback_rate"])
        if tempo != 1:
            raise SystemExit("Narration playback must stay at 1x. Adjust the edit rather than speeding up the voice.")
        voice_duration = float(probe(source)["format"]["duration"])
        available = DURATION - settings["mix"]["voice_start_seconds"] - 0.10
        if voice_duration > available:
            raise SystemExit(f"The {voice_duration:.2f}s narration needs a longer edit. Playback stays at 1x; extend the shot or revise the script.")
        filters = (
            "loudnorm=I=-16:TP=-2:LRA=7,"
            f"adelay={round(settings['mix']['voice_start_seconds'] * 1000)}:all=1,"
            "apad,atrim=duration=4"
        )
        process_audio(source, scratch / "narration.wav", filters)
        draft_foley(scratch)
        process_audio(
            music, scratch / "music.wav",
            "atrim=duration=4,asetpts=PTS-STARTPTS,loudnorm=I=-32:TP=-9:LRA=7,"
            "afade=t=in:st=0:d=0.08,afade=t=out:st=3.65:d=0.35",
            start=8,
        )
        stems = ["narration.wav", "night-ambience.wav", "lantern-rustle.wav", "music.wav"]
        command = [FFMPEG, "-y", "-v", "error"]
        for stem in stems:
            command.extend(["-i", scratch / stem])
        command.extend([
            "-filter_complex",
            "[0:a][1:a][2:a][3:a]amix=inputs=4:normalize=0:duration=longest,"
            "alimiter=limit=0.891:level=false:latency=true[a]",
            "-map", "[a]", "-t", DURATION, "-ar", RATE, "-ac", 2,
            "-c:a", "pcm_s16le", scratch / "sol-lantern-mix.wav",
        ])
        run(command)
        mixed = probe(scratch / "sol-lantern-mix.wav")
        stream = next(stream for stream in mixed["streams"] if stream["codec_type"] == "audio")
        if abs(float(mixed["format"]["duration"]) - DURATION) > 0.001 or int(stream["sample_rate"]) != RATE:
            raise SystemExit("Mix verification failed: expected exactly four seconds at 48 kHz.")
        run([FFMPEG, "-v", "error", "-xerror", "-i", scratch / "sol-lantern-mix.wav", "-f", "null", "-"])
        measurement = run([
            FFMPEG, "-hide_banner", "-i", scratch / "sol-lantern-mix.wav", "-af",
            "loudnorm=I=-16:TP=-1:LRA=7:print_format=json", "-f", "null", "-",
        ])
        loudness, _ = json.JSONDecoder().raw_decode(measurement.stderr[measurement.stderr.rfind("{"):])
        if float(loudness["input_tp"]) > -1 or not math.isfinite(float(loudness["input_i"])):
            raise SystemExit("Mix has invalid loudness or exceeds the -1 dBTP ceiling.")
        report = {
            "voice": settings["narration"]["voice_name"],
            "voice_source": str(source),
            "voice_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "spoken_text": settings["narration"]["text"],
            "voice_duration": voice_duration,
            "provider_speech_rate": settings["narration"]["speech_rate"],
            "local_tempo_adjustment": tempo,
            "voice_start_seconds": settings["mix"]["voice_start_seconds"],
            "mix_duration": DURATION,
            "sample_rate": RATE,
            "channels": 2,
            "music_source": str(music),
            "music_offset_seconds": 8,
            "music_target_lufs": -32,
            "foley": "Synthesized draft night air, soft crackle and paper rustle; separately replaceable stems",
            "measured_mix_lufs": float(loudness["input_i"]),
            "measured_mix_true_peak_dbtp": float(loudness["input_tp"]),
            "decoded": True,
        }
        (scratch / "mix-verification.json").write_text(json.dumps(report, indent=2) + "\n")
        destination = (EPISODE / settings["mix"]["output"]).parent
        destination.mkdir(parents=True, exist_ok=True)
        files = stems + ["sol-lantern-mix.wav", "mix-verification.json"]
        for name in files:
            existing = destination / name
            if existing.exists() and existing.read_bytes() != (scratch / name).read_bytes():
                raise SystemExit(f"Filename collision: {existing}; previous mix preserved.")
        for name in files:
            if not (destination / name).exists():
                shutil.copy2(scratch / name, destination / name)
        print(json.dumps(report, indent=2))
        print(f"Mix ready: {destination / 'sol-lantern-mix.wav'}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.stderr or str(error)) from error
