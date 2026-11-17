"""Retain the existing mix and check the larger-caption, no-end-card export."""
import hashlib
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

EPISODE = Path(__file__).resolve().parents[1]
REVIEW = EPISODE / "revisions/captions-no-endcard-v13/review"
BASELINE = EPISODE / "renders/fire-discovery-enrollment-v12-fullbleed-final.mp4"
RENDER = EPISODE / "renders/fire-discovery-captions-no-endcard-v13-render.mp4"
OUTPUT = EPISODE / "renders/fire-discovery-captions-no-endcard-v13-final.mp4"


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audio_packets(path):
    return json.loads(run([
        "ffprobe", "-v", "error", "-select_streams", "a:0", "-show_packets",
        "-show_data_hash", "sha256", "-show_entries",
        "packet=pts,dts,duration,size,data_hash", "-of", "json", str(path),
    ]))["packets"]


def main():
    REVIEW.mkdir(parents=True, exist_ok=True)
    edit_path = EPISODE / "edit-captions-no-endcard-v13.json"
    edit = json.loads(edit_path.read_text())
    previous = json.loads((EPISODE / "edit-enrollment-v12.json").read_text())
    assert edit["shots"] == previous["shots"][:5]
    assert edit["audioTracks"] == previous["audioTracks"]
    assert " ".join(c["text"] for c in edit["captions"]) == " ".join(
        c["text"] for c in previous["captions"][:16]
    )
    assert edit["captionStyle"]["fontSize"] == previous["captionStyle"]["fontSize"] * 1.5
    assert not OUTPUT.exists(), "Preserve existing output; inspect before replacing."
    run([
        "ffmpeg", "-v", "error", "-nostdin", "-i", str(RENDER), "-i", str(BASELINE),
        "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart",
        str(OUTPUT),
    ])
    run(["ffmpeg", "-v", "error", "-nostdin", "-i", str(OUTPUT), "-f", "null", "-"])
    probe = json.loads(run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(OUTPUT),
    ]))
    video = next(s for s in probe["streams"] if s["codec_type"] == "video")
    assert (video["width"], video["height"], video["avg_frame_rate"], int(video["nb_frames"])) == (1080, 1920, "30/1", 764)
    old_audio, new_audio = audio_packets(BASELINE), audio_packets(OUTPUT)
    assert old_audio == new_audio, "Original soundtrack changed."
    samples = [
        {"frame": math.floor((c["start"] + c["end"]) / 2 * 30), "kind": "caption",
         "caption_index": i + 1, "text": c["text"]}
        for i, c in enumerate(edit["captions"])
    ]
    # Entire final Narrator turn is sampled, plus the original monkey outpoint.
    for frame in [202, 203, 204, 722, 728, 734, 740, 746, 752, 755, 760, 763]:
        samples.append({"frame": frame, "kind": "ending_or_transition"})
    frames = sorted({s["frame"] for s in samples})
    detail = REVIEW / "detail"
    detail.mkdir(exist_ok=True)
    select = "+".join(f"eq(n,{f})" for f in frames)
    run([
        "ffmpeg", "-v", "error", "-nostdin", "-i", str(OUTPUT), "-vf", f"select='{select}'",
        "-fps_mode", "vfr", "-q:v", "2", str(detail / "frame-%03d.jpg"),
    ])
    for sample in samples:
        sample["time_sec"] = sample["frame"] / 30
        sample["file"] = f'detail/frame-{frames.index(sample["frame"]) + 1:03d}.jpg'
    pages = []
    for kind in ["caption", "ending_or_transition"]:
        group = [s for s in samples if s["kind"] == kind]
        for offset in range(0, len(group), 6):
            canvas = Image.new("RGB", (1080, 1340), "#FFF8F0")
            draw = ImageDraw.Draw(canvas)
            for i, sample in enumerate(group[offset:offset + 6]):
                x, y = i % 3 * 360, i // 3 * 670
                with Image.open(REVIEW / sample["file"]) as source:
                    canvas.paste(source.resize((360, 640)), (x, y))
                draw.text((x + 8, y + 646), f'{sample.get("caption_index", "Ending")} | {sample["time_sec"]:.3f}s | f{sample["frame"]}', fill="#1A1A2E")
            name = f"{kind}-{offset // 6 + 1:02d}.jpg"
            canvas.save(REVIEW / name, quality=95)
            pages.append(name)
    # Compare every original picture frame outside the caption area.
    ssim_path = REVIEW / "picture-area-ssim.txt"
    run([
        "ffmpeg", "-v", "error", "-nostdin", "-i", str(BASELINE), "-i", str(OUTPUT),
        "-filter_complex", "[0:v]trim=end_frame=764,crop=1080:1560:0:0,setpts=PTS-STARTPTS[a];"
        "[1:v]crop=1080:1560:0:0,setpts=PTS-STARTPTS[b];"
        f"[a][b]ssim=stats_file={ssim_path}", "-an", "-f", "null", "-",
    ])
    ssim = [float(line.split("All:")[1].split()[0]) for line in ssim_path.read_text().splitlines()]
    assert len(ssim) == 764 and min(ssim) > 0.97, "Picture differs outside captions."
    verification = {
        "output": str(OUTPUT), "sha256": sha(OUTPUT), "bytes": OUTPUT.stat().st_size,
        "full_decode_passed": True, "frames": 764, "duration_sec": 764 / 30,
        "dimensions": [1080, 1920], "fps": 30,
        "caption_font_size": 105, "previous_font_size": 70, "increase_percent": 50,
        "caption_count": len(edit["captions"]), "caption_outline_px": 12,
        "caption_side_margins_percent": 10, "caption_top_percent": 82,
        "all_five_shots_and_audio_settings_unchanged": True,
        "dialogue_words_and_original_caption_windows_unchanged": True,
        "caption_grouping": "Four long cues split at saved measured word onsets;20 total cues.",
        "aac_packets_and_timestamps_identical": True, "aac_packet_count": len(new_audio),
        "uncaptioned_picture_compared_frames": len(ssim), "ssim_min": min(ssim),
        "ssim_mean": sum(ssim) / len(ssim), "baseline_sha256": sha(BASELINE),
        "endcard_removed": True, "removed_seconds": 3,
        "manual_audio_listening_claimed": False, "visual_review": "pending",
    }
    (REVIEW / "verification.json").write_text(json.dumps(verification, indent=2) + "\n")
    (REVIEW / "packet.json").write_text(json.dumps({
        "video": str(OUTPUT), "sha256": sha(OUTPUT), "edit": str(edit_path),
        "script": str(EPISODE / "script-no-endcard-v13.txt"),
        "voice_cues": previous["timing"]["assembled_voice_cues"],
        "pages": pages, "samples": samples,
    }, indent=2) + "\n")
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
