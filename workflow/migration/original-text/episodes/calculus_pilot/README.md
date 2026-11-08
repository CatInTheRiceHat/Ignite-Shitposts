# Ignite calculus pilot, revised edit

Open `animatic.mp4` for the current 15-second portrait preview. It is labeled
ANIMATIC because generated clips and the MoGoFun Cub (Female) download have
not been supplied. Any local voice is temporary, never represented as Cub.
Previous exports are preserved in `archive/v1/`.

## Read-only artwork source

Only these two website artwork files are needed, and both copies are
byte-identical to their originals:

| Website original | Video project copy |
| --- | --- |
| `/Users/elaine/Documents/Ignite Website/public/mascots/Mascot.png` | `assets/sol-full-body.png` |
| `/Users/elaine/Documents/Ignite Website/public/courses/Differential Calculus.jpg` | `assets/calculus-painted-scene.jpg` |

`Mascot.png` is the website widget's default Sol reference, as selected in
`src/sol/widget/loader.tsx`. There is no separately named “approved” file or
approval record in the inspected artwork directory. This revision uses the
same original reference selected in the prior pilot, with the painted scene
as the style/limb reference. It does not invent a new face or mouth.

The animatic uses the real Sol image, stepped whole-body poses, a tiny arm
timing placeholder, a camera crop of the painted scene and code-drawn board
blocking. It is not a claim that the requested low-angle painted animation
has already been generated. `generation/prompts.md` describes the actual
three clips to generate. The numbered start-frame PNGs are blocking guides.

## Script and delivery

Use MoGoFun **Cub (Female)** as an off-screen narrator. Paste `narration.txt`
or the script in `imports/README.md`; save the actual download as
`imports/mogofun-narration.mp3`. Aim for 14–15 seconds, including short pauses.
The code accepts MP3, WAV or M4A, preserves imported pacing and refuses a read
longer than the edit rather than clipping or accelerating it silently.

## Editable edit

- `edit.json`: cut/caption text and timing, clip in points/holds, graph function,
  graph point and scale, tangent reveal time and audio levels.
- `imports/voiceover-cues.json`: checked timing for the real recording, tied to
  its SHA-256 hash. See `imports/README.md` for the exact sync procedure.
- `timeline.resolved.json`: timeline actually used for the latest export.
- `captions.srt`: editable subtitles; `--captions soft` exports a selectable MP4
  subtitle track instead of burned-in captions. `--captions none` omits them.
- `layers/graph.svg`: separate editable graph and point.
- `layers/tangent.svg`: separate editable tangent line and slope label.
- `picture-clean.mp4`: picture before captions, graph, tangent and status labels.
- `audio/narration.wav`, `audio/sfx.wav`, `audio/mix.wav`: separate audio stems.

The exact graph is `y = sqrt(x)`, with tangent `y = x/2 + 1/2` at `(1,1)` and
slope `1/2`. Its increasing, concave-down shape follows the painted track's
direction more closely than the old quadratic. The board-contact match point
is `(360,760)` in a 720 × 1280 frame; the tangent rises about 25 degrees toward
screen right. Graph geometry comes from the analytic function, never a model.
`generation/match-cut-target.png` supplies the precise exit-framing target.

The tangent starts drawing on the “Tangent” narration cue. A soft landing tap
and tiny balance squeak are synthesized locally at a -30 dBFS peak ceiling;
narration is normalized toward -16 LUFS, and generated clip audio is muted.
The final mix has a limiter. There is no background music.

## Build and import

Python, Pillow and FFmpeg are sufficient for imported-media rendering.
macOS `say` is used only when making temporary animatic narration.
No Blender, API key, cloud generation request or paid service call is made
by the renderer. Existing asset/font helpers are reused from
`scripts/calculus_pilot.py`; the revised edit lives in `scripts/calculus_edit.py`.

```bash
python3 scripts/calculus_pilot.py --ffmpeg /path/to/ffmpeg
python3 scripts/calculus_pilot.py --ffmpeg /path/to/ffmpeg --require-final
```

The first command accepts whatever imports are present and explicitly labels
missing footage or unconfirmed voice timing. The second refuses a final until
all three clips, actual downloaded voiceover and confirmed audio cues exist.
No background watcher is installed: rerun after importing, or ask for the edit
to be timed to the new recording.

The current machine has a temporary FFmpeg 9.0 executable at:

`/tmp/ignite-calculus-pilot-tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v9.0`

Font copies and their OFL license files remain in `assets/fonts/`. Original
artwork hashes remain in `asset-manifest.json`. The renderer fully decodes
each exported MP4; see `validation.json` and `decode-check.log`.
