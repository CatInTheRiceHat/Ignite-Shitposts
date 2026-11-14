# Shared Ignite Remotion engine

One reusable renderer serves multiple episodes. Shared components, validation,
commands, TypeScript settings and the single npm dependency install live here.
Each episode owns its edit JSON, public assets, narration, footage and renders.
The shared renderer does not import or default to the zipper episode.

See the [workflow guide](../README.md), [creative guidelines](../guidelines/README.md)
and [episode index](../episodes/README.md).

## Install and run

From the repository root:

```bash
npm --prefix workflow/remotion ci
npm --prefix workflow/remotion run dev -- zipper_demo
npm --prefix workflow/remotion run render -- zipper_demo
npm --prefix workflow/remotion run still -- zipper_demo --frame 270
```

The same commands work from `workflow/remotion/` as `npm run dev -- zipper_demo`,
etc. Studio prints its local URL; select `IgniteShort` and press Space. Edits to
its selected JSON reload while Studio runs. Stop with Ctrl-C. `--no-open` keeps
Studio from opening a browser window.

Remotion is pinned to 4.0.542. Rendering needs a browser and ffprobe (install
FFmpeg or set `FFPROBE_PATH`). On macOS the launcher prefers installed Google
Chrome. Set `REMOTION_BROWSER_EXECUTABLE` or pass `--browser-executable` to
choose another browser. These commands use local files and do not submit
paid generation jobs or synthesize narration.

## Episode inputs and outputs

| Input | Meaning |
| --- | --- |
| `zipper_demo` | `workflow/episodes/zipper_demo/edit.json`, independent of the terminal directory |
| An explicit JSON path | That edit, resolved from the invocation directory when relative |
| An explicit episode folder path | That folder's `edit.json` |

A standard episode has:

```text
episodes/<name>/
  edit.json
  public/          Art, fonts, imported clips and narration used by this edit
  renders/         Exports, stills and render archives
  remotion/        Optional custom composition
```

Asset paths inside JSON are relative to that episode's `public/` folder.
Exports default to `renders/<edit-id>.mp4` or `renders/<edit-id>-preview.png`.
`--output` paths are relative to the episode folder; absolute paths also work.
For example, `--output renders/alternate.mp4` stays with the selected episode.
The renderer checks video dimensions, fps and duration before replacing an
existing output, which is archived first.

## Start another short

The neutral starter is a 30-second hook, setup, reveal and payoff with labeled
art placeholders. It contains no zipper-specific content. From the repository
root, use a new episode name:

```bash
mkdir -p workflow/episodes/my_next_short
cp -n workflow/templates/remotion-episode.json workflow/episodes/my_next_short/edit.json
npm --prefix workflow/remotion run setup-assets -- my_next_short
npm --prefix workflow/remotion run dev -- my_next_short
```

Edit the new JSON's `id`, title, hook, shots, captions, palette and narration.
The starter uses the shared painted reference as a temporary background.
Replace draft artwork and caption text before release. `setup-assets` copies
shared Sol, the painted reference and Nunito into that episode's `public/`;
modified destination files are preserved and reported. No package manifest or
separate dependency install is needed for a standard episode.

The shared layout is 1080 × 1920 at 30 fps. Each edit determines its duration
from its shot lengths. Keep intentional existing overrides: zipper is 20
seconds and the custom Sol lantern composition is 4 seconds. The Python
workflow separately defaults to 720 × 1280 and uses its own edit schema.

## Generated skits

Use `python3 workflow/scripts/shorts.py prepare <episode>` to prepare a new
skit, or create an edit from its reviewed shot plan. Set `layout: "fullscreen"`
for complete 9:16 footage. This fills the entire 1080 × 1920 picture without
the older card headers or cropped scene window. Existing edits default to
the original `cards` layout.

`audioTracks` holds separate timed takes with `id`, `speaker`, `src`, `start`,
`duration`, `trimBefore`, `volume`, `playbackRate: 1` and `source_sha256`.
The legacy single `voiceover` remains supported. `captionStyle` controls the
font size, white fill, orange outline and safe-area position; skits use the
shared Rammetto One font. Captions remain editable text in the episode JSON.

`python3 workflow/scripts/shorts.py sync-audio <episode>` measures the actual
downloaded takes and prepares provisional phrase captions. Review them in
Studio, then set `timing.confirmed: true`. Final full-screen exports require
confirmed timing, actual audio tracks and matching source hashes.
Use `npm --prefix workflow/remotion run render -- <episode> --draft` for an
explicit draft export while caption timing is provisional. Actual clips and
voice takes are still required; the output is named `<id>-draft.mp4`.

## Artwork, footage and narration

Layer scenes support independent position, scale, rotation, opacity, tugging,
camera movement and annotations. A missing image can use a labeled
`placeholder` instead of `src`. The scene window is a 1080 × 1280 artboard,
415 pixels below the top of the vertical frame.

A shot can instead use local footage:

```json
{
  "type": "video",
  "src": "clips/shot-01.mp4",
  "trimBefore": 0,
  "playbackRate": 1,
  "muted": true,
  "fit": "contain"
}
```

Use `contain` to retain the entire source frame or `cover` to fill the window.
Clips must have enough usable duration after trimming. Save narration under
`public/audio/`, set `voiceover.src`, and time shots and captions to the actual
recording. `src: null` keeps the edit silent. The narration script field does
not generate speech; retain normal speech speed and 1× playback.

## Custom compositions and checks

An episode with different animation can keep its own `remotion/` composition
and renderer while using this shared dependency install. The Sol lantern test
is the existing example:

```bash
npm --prefix workflow/remotion run sol:check
npm --prefix workflow/remotion run sol:render
npm --prefix workflow/remotion test
npm --prefix workflow/remotion run lint
```

The Sol test retains its exact clip/audio verification and existing renderer;
`sol:render` uses the prepared local mix. See its [episode guide](../episodes/sol_kling_test/README.md).
The named zipper and Sol npm shortcuts are conveniences; the generic `dev`,
`render`, `still` and `setup-assets` commands take any compatible episode.
