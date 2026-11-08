# Ignite calculus pilot

A 15-second portrait explainer: a secant approaches a tangent, whose slope is
the derivative. The worked graph is `y = x²`, with `f'(1) = 2`.

Open `final.mp4` for the finished pilot or `storyboard.jpg` for all five beats.
The video includes burned-in captions and local synthetic draft narration.
`captions.srt` and `narration.txt` are supplied separately for revision.

## Source artwork

The Ignite website was used only as a read-only asset source:

| Original file | Unmodified copy in this project |
| --- | --- |
| `/Users/elaine/Documents/Ignite Website/public/mascots/Mascot.png` | `assets/sol-full-body.png` |
| `/Users/elaine/Documents/Ignite Website/public/courses/Differential Calculus.jpg` | `assets/calculus-painted-scene.jpg` |

The Sol PNG is 1920 × 1920 with an alpha channel and transparent pixels. The
painted scene is 2752 × 1536. Both copied files are byte-identical to their
originals; see `asset-manifest.json` for SHA-256 hashes. They remain Ignite
artwork; no new artwork license is assigned by this pilot.

The palette and typography follow the website's `IGNITE_STYLE_GUIDE.md`:
cream `#FFF8F0`, orange `#F07B2A`, charcoal `#1A1A2E`; Rammetto One,
Poppins, and Nunito. Font files were obtained from the Google Fonts
repository at `https://github.com/google/fonts/tree/main/ofl/`. Each font's
SIL Open Font License is copied alongside it in `assets/fonts/`.

## Timeline

| Time | Narration and visual |
| --- | --- |
| 0–3s | “How steep is a curve at one point?” Painted calculus scene, gentle push. |
| 3–6s | “Two points give an average slope.” Two marked points and a secant. |
| 6–9s | “Bring those points closer together.” Q moves toward P; the secant rotates. |
| 9–12s | “The line approaches a tangent.” Tangent and slope `f'(1) = 2`. |
| 12–15s | “Its slope is the derivative: change right here.” Painted scene and full-body Sol. |

This is a local composition, rendered by `scripts/calculus_pilot.py`. It does
not invoke the upstream MuAPI generation workflow or its assembler. The
mascot is the existing artwork with gentle whole-image movement; it is not
rigged character animation. Narration uses macOS's installed Samantha voice
as a replaceable draft, with each sentence fitted into a three-second beat.
There is no music. No API key or paid generation service was used.

## Rebuild

From the video repository root, with Python 3, Pillow, macOS `say`, and FFmpeg:

```bash
python3 scripts/calculus_pilot.py --ffmpeg /path/to/ffmpeg
```

To reuse or replace the existing 15-second narration WAV:

```bash
python3 scripts/calculus_pilot.py --ffmpeg /path/to/ffmpeg --reuse-narration
```

The initial build used FFmpeg 9.0 from an `imageio-ffmpeg` installation in
`/tmp/ignite-calculus-pilot-tools`. This temporary tool location may be removed
by the operating system; use an available FFmpeg binary when rebuilding.
No website files or secrets are needed to rebuild from these copied assets.

## Validation

The build fully decodes the final video through FFmpeg, then writes
`validation.json` and `decode-check.log`. Expected output: 450 frames,
720 × 1280, 30 fps, 15.00 seconds, H.264 video and AAC narration.
