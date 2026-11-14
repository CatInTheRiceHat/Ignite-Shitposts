# Ignite video

A standalone Remotion project, scaffolded with the official [blank starter](https://www.remotion.dev/templates/blank), version 4.0.542. It lives in `ignite-video/` as requested and does not use the Python generator, UseAPI, API tokens, or paid generation. All animation is deterministic and driven by the Remotion frame clock.

The demo is **20 seconds / 600 frames / 1080 × 1920 / 30 fps**. It opens on a jam, pushes into the slider, fades its cover to reveal caught fabric, shows the pinch, and finishes with the original mouthless Sol. The cream paper, teal fabric, warm ochre hardware, brush-like edges, and existing Nunito font follow the workspace's painted Ignite reference. The seven zipper SVGs are labeled art studies for replacement, not finished commissioned artwork. The default demo is silent; its narration script and captions are in the episode file.

## Preview and render

From the repository root:

```bash
cd ignite-video
npm run dev
```

Open the Studio URL printed in the terminal (normally http://localhost:3000), select `IgniteShort`, and press Space. Changes to the selected episode JSON are validated and reloaded while Studio runs. Stop with Ctrl-C.

```bash
npm run render
```

Output: `out/zipper.mp4`. The command uses ffprobe to verify width, height, fps, and duration, then writes `out/zipper.verification.json`. A failed render never replaces the existing output. Successful rerenders preserve the previous MP4 in `out/archive/`.

Use another episode without editing React:

```bash
npm run dev -- episodes/episode-two.json
npm run render -- episodes/episode-two.json --output out/episode-two.mp4
```

Equivalent: `npm run render -- --episode episodes/episode-two.json`. Paths passed on the command line are relative to `ignite-video/` (absolute episode paths also work). All asset paths inside JSON are relative to `ignite-video/public/`.

Useful checks:

```bash
npm test
npm run lint
npm run still -- --frame 270 --output out/reveal.png
ffprobe -v error -show_streams -show_format -of json out/zipper.mp4
```

`--concurrency 2` lowers render memory use; default is 4. On macOS, the launcher uses installed Google Chrome when available because the current bundled headless browser crashes while loading ICU resources on this machine. Other installations use Remotion's downloaded headless browser. Set `REMOTION_BROWSER_EXECUTABLE` or pass `--browser-executable /path/to/chrome` to choose a browser explicitly; this uses Remotion's [documented browser override](https://www.remotion.dev/docs/cli/render#--browser-executable). Browser downloads need internet on the first run. Local renders need no internet after installation/browser download. If ffprobe is missing, install `brew install ffmpeg` or set `FFPROBE_PATH` to the executable.

## Replace artwork

Edit **`episodes/zipper.json`** for the hook, titles, shot durations, paths, captions, and narration. In each `shots[].scene`, image order is back to front. The camera moves all layers together, while every layer can translate, rotate, scale, fade, or tug independently.

| File or directory                               | Purpose                                                                     |
| ----------------------------------------------- | --------------------------------------------------------------------------- |
| `public/art/zipper/zipper-track.svg`            | Painted fabric panels and teeth                                             |
| `public/art/zipper/fabric-fold.svg`             | The loose fabric; moves independently into the gap                          |
| `public/art/zipper/inner-channel.svg`           | Simplified inside of the slider                                             |
| `public/art/zipper/slider-shell.svg`            | Outer cover; fades for the cutaway                                          |
| `public/art/zipper/pull-tab.svg`                | Pull tab; tugs separately                                                   |
| `public/art/zipper/catch-ring.svg`              | Reveal circle and pointer                                                   |
| `public/art/zipper/paper.svg`                   | Paper grain and pale painted wash                                           |
| `public/art/ignite/sol-full-body.png`           | Unmodified copy of the existing Sol artwork                                 |
| `public/art/ignite/painted-style-reference.jpg` | Original painted scene copied for art direction; not used as zipper scenery |
| `public/fonts/Nunito.ttf`                       | Existing workspace font; OFL included                                       |
| `src/Composition.tsx`                           | Reusable scene/camera/layer/MP4/caption/voiceover components                |
| `src/style.css`                                 | Typography, safe areas, brand, caption placement                            |
| `src/episode.ts`                                | Validated JSON structure and timing rules                                   |

Replace a layer's `src` with a local PNG, WebP, JPG, or SVG. Use transparent artwork for independently moving pieces. Full-canvas layers use a **1080 × 1280 artboard** inside the vertical frame; that artboard begins 415 pixels below the top. Alternatively set a layer's `x`, `y`, `width`, and `height`. Its camera `x/y` is the point in that artboard centered on screen; `scale` controls the push-in. Shot motion and annotation times are relative to that shot. Caption and voiceover times are absolute episode seconds. Durations must align to a 30 fps frame; total episode length is calculated from the shots.

If you do not have an image yet, replace the layer with a labeled placeholder:

```json
{
  "id": "jacket",
  "placeholder": "REPLACE: painted jacket and zipper",
  "x": 100,
  "y": 160,
  "width": 880,
  "height": 900
}
```

Remove `artNote` after replacing the study artwork to use the default “FIND YOUR FIRE.” footer. Remove the cutaway annotations too if your finished artwork already contains labels. Original artwork copies and imported/generated media stay local and are ignored by Git; editable SVGs and episode JSON are source files.

## Drop in a Flow MP4

Save the finished clip to `public/clips/zipper-closeup.mp4`, then replace a shot's entire `scene` object:

```json
{
  "type": "video",
  "src": "clips/zipper-closeup.mp4",
  "trimBefore": 0,
  "playbackRate": 1,
  "muted": true,
  "fit": "cover"
}
```

Keep that shot's `duration`, `title`, and `label`. Titles, captions, and the Ignite frame remain above the clip. `cover` fills the 1080 × 1280 scene window and can crop a portrait clip; `contain` preserves the entire clip. The renderer checks that the source has enough video after trimming and playback speed changes. It never calls Flow or UseAPI. Downloads and generation stay entirely outside this project.

## Optional narration

Save Cub (Female), or another recording, to `public/audio/zipper-narration.mp3`. Set `voiceover.src` in the same episode JSON to `audio/zipper-narration.mp3`; adjust `start`, `volume`, shot durations, and captions to match the recording. `src: null` keeps the video silent. The `script` field is editable narration copy; it does not synthesize speech. Local MP4 audio is muted by default to avoid colliding with narration.

## Episode two

```bash
cp episodes/zipper.json episodes/episode-two.json
```

In that file, change `id` to `episode-two`, then edit `title`, `hook`, `shots`, `captions`, artwork paths, and optional voiceover. Reuse the Sol layer for a brief ending cameo. Set each shot's motion end time within its new duration. Then use the alternate episode commands above; a new `id` automatically gives you a separate default output filename.

## Reinstall

Tested locally with Node.js v20.17.0 and npm 10.8.2. For a fresh machine, install Node.js LTS (which includes npm), then:

```bash
cd ignite-video
npm ci
npm run setup-assets
npm run dev
```

`setup-assets` copies Sol, the painted reference, and the font from `../workflow/assets/`. It preserves differing existing files and reports them rather than replacing custom art. If the original assets are unavailable, put your own files at the paths in the episode JSON or use labeled placeholders. Keep the font license with any replacement font.
