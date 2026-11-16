"""Make versioned review clips from inspected complete source-frame pairs.

No image synthesis, pixel repair, interpolation, voice edits, or active-edit
selection. The mapping omits residual emission buds in the native-v2 cleanup.
Every output frame is verified against an actual decoded source frame.
"""
import hashlib
import json
import subprocess
from pathlib import Path

EPISODE = Path(__file__).resolve().parents[1]
PLANS = {
    "02": {
        "frames": 144,
        "replacements": {
            38: 36, 40: 42,
            68: 66,
            98: 96, 100: 102,
            126: 124, 128: 130,
        },
    },
    "05": {
        "frames": 134,
        "replacements": {
            16: 14, 18: 14, 20: 22,
            40: 38, 42: 38, 44: 46,
            50: 48,
        },
    },
}


def frame_hashes(path):
    result = subprocess.check_output([
        "ffmpeg", "-v", "error", "-nostdin", "-i", str(path),
        "-map", "0:v:0", "-pix_fmt", "yuv420p", "-f", "framemd5", "-",
    ], text=True)
    return [line.split(",")[-1].strip() for line in result.splitlines()
            if line and not line.startswith("#")]


def main():
    reports = []
    output_dir = EPISODE / "clips/edit-v3"
    output_dir.mkdir(exist_ok=True)
    for scene, plan in PLANS.items():
        source = EPISODE / f"clips/{scene}-scene-omni-v6-particle-free-native-v2.mp4"
        output = output_dir / f"{scene}-clean-holds-v3.mp4"
        if output.exists():
            raise FileExistsError(f"Preserve existing output: {output}")
        nframes = plan["frames"]
        mapping = []
        for frame in range(0, nframes, 2):
            selected = plan["replacements"].get(frame, frame)
            assert selected % 2 == 0
            mapping.extend([selected, selected + 1])
        # Preserve source YUV values exactly, including painted edges. Lossless
        # all-intra encoding avoids another lossy generation of the cleanup.
        frame_size = 1080 * 1920 * 3 // 2
        raw = subprocess.check_output([
            "ffmpeg", "-v", "error", "-nostdin", "-i", str(source),
            "-map", "0:v:0", "-frames:v", str(nframes),
            "-pix_fmt", "yuv420p", "-f", "rawvideo", "-",
        ])
        assert len(raw) == nframes * frame_size
        encoder = subprocess.Popen([
            "ffmpeg", "-v", "error", "-nostdin", "-n", "-f", "rawvideo",
            "-pix_fmt", "yuv420p", "-s", "1080x1920", "-r", "30",
            "-i", "-", "-an", "-c:v", "libx264", "-preset", "fast",
            "-qp", "0", "-g", "1", "-bf", "0", "-movflags", "+faststart",
            str(output),
        ], stdin=subprocess.PIPE)
        for index in mapping:
            encoder.stdin.write(raw[index * frame_size:(index + 1) * frame_size])
        encoder.stdin.close()
        if encoder.wait() != 0:
            raise RuntimeError(f"Encoding failed: {output}")
        source_hashes = frame_hashes(source)
        actual = frame_hashes(output)
        assert len(actual) == nframes
        assert actual == [source_hashes[i] for i in mapping]
        assert all(actual[i] == actual[i + 1] for i in range(0, nframes, 2))
        report = {
            "scene": scene,
            "source": str(source.relative_to(EPISODE)),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "output": str(output.relative_to(EPISODE)),
            "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            "frames": nframes,
            "duration_sec": nframes / 30,
            "replaced_pair_first_frames": plan["replacements"],
            "source_frame_mapping": mapping,
            "decoded_frames_match_selected_source_exactly": True,
            "decoded_pair_mismatches": [],
            "method": "Complete-pair editorial holds from inspected adjacent clean states. No new pixel edits. Other source action remains at 1x. Scene 05 retains 8 more source frames for the Narrator's reply after the upward tilt.",
            "status": "Review candidate; visual transition review pending.",
        }
        reports.append(report)
        print(f"{scene}: {nframes} frames, exact source match, exact pairs", flush=True)
    receipt = EPISODE / "reviews/resume-native-v1/clean-state-selection-v3.json"
    if receipt.exists():
        raise FileExistsError(receipt)
    receipt.write_text(json.dumps(reports, indent=2) + "\n")


if __name__ == "__main__":
    main()
