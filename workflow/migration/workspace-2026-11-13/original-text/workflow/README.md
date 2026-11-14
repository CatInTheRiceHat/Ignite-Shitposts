# Ignite Shorts workflow

This is the home for all Ignite Shorts files. Run the commands below in VS
Code's terminal with `/Users/elaine/Documents/Ignite-Shitposts` open as the
workspace root. Paths are resolved from this workflow or the episode folder,
so an episode name never depends on the terminal's current directory.

## Setup

Use Python 3.10 or newer, Pillow, FFmpeg and ffprobe. Blender is not required.
Offline prepare/check/render need no API key; useapi.net generation requires
`USEAPI_TOKEN`. Flow can also use manual downloads. MoGoFun is used manually.
Downloaded media stays local.

```bash
python3 -m venv workflow/.venv
source workflow/.venv/bin/activate
python -m pip install -r workflow/requirements.txt
brew install ffmpeg
ffmpeg -version
ffprobe -version
```

If FFmpeg is installed elsewhere, add `--ffmpeg /full/path/to/ffmpeg` to check
or render, or set `FFMPEG_PATH`. If Mac security blocks execution, the command
reports the executable, exception or exit status and error text. Prepare and
ordinary missing-media checks do not execute FFmpeg. A temporary local voice
for an animatic uses macOS `say`; imported Cub audio works without `say`.

## Prepare an episode

```bash
python workflow/scripts/shorts.py prepare calculus_pilot
python workflow/scripts/shorts.py prepare my_next_short
```

New episodes use the shared **30-second, 720 × 1280, 30 fps** vertical format.
The existing calculus pilot keeps its explicit **15-second** edit. To create
another intentional duration, use `prepare name --duration 15` the first time.
Prepare never replaces an existing script, prompt, edit JSON, image or clip.
Existing files are reused; it does not reset edits to the template.

Edit `episodes/<name>/narration.txt`, `edit.json`, `shot-plan.json`, and the
episode's two Flow prompt documents. Keep the cue text in `edit.json` in sync
with the narration script: the renderer uses those cues for captions.

## A → B → C → D and download locations

Read the episode's `flow-image-prompts.md` and `flow-video-prompts.md`.
Use the shared Sol reference and painted scene in `workflow/assets/`.
The website repository remains read-only; no website file is needed to render.

For `calculus_pilot`, relative to `workflow/episodes/calculus_pilot/`:

| Frame | Action | Flow Image download | Flow Video download |
| --- | --- | --- | --- |
| A | Hop onto the moving board | `keyframes/A.png` | `clips/01-hop-on.mp4` |
| B | Low side angle, tiny balancing arm | `keyframes/B.png` | `clips/02-low-side-lean.mp4` |
| C | Match-cut to exact graph and tangent | `keyframes/C.png`, generated locally | None; the renderer draws the math |
| D | Deadpan reaction hold | `keyframes/D.png` | `clips/03-reaction.mp4` |

`keyframes/blocking/` contains the original timing guides and new lettered
blocking frames. They are not approved finished Flow images; prepare never
places them in the A/B/D download slots. C is a precise local graph, with
editable source in `layers/graph.svg` and `layers/tangent.svg`.

Use **MoGoFun → Cub (Female)** as the off-screen narrator. Paste the episode's
`narration.txt`. Save the actual download as:

`workflow/episodes/calculus_pilot/audio/mogofun-narration.mp3`

Narration runs at **1× playback**. For Higgsfield voice generation, use
`speech_rate: 0` for the provider's normal rate. Do not speed speech up to fit
shot slots. For full videos, time shots to the finished narration and leave
room for pauses and reveals; extend the edit or revise the script if needed.
These preferences are saved in `config/narration.json`. The custom Sol voice
test has its voice ID and episode override in `episodes/sol_kling_test/audio-test.json`.

If the download is WAV or M4A, retain its real format and use the same basename
with `.wav` or `.m4a`; keep only one version. The recorded pacing is preserved.
Do not put a new download into `audio/generated/`, which contains temporary
speech, processed narration, effects and mix stems.

## Generate the pilot's A → B shot with useapi.net

Connect your Google Flow account in useapi.net first. From the repository root,
set `USEAPI_TOKEN` in your terminal environment. In the default macOS zsh, this
prompts without displaying the token or putting its value into shell history:

```zsh
read -rs 'USEAPI_TOKEN?useapi.net token: '
export USEAPI_TOKEN
printf '\n'
python3 workflow/scripts/shorts.py generate calculus_pilot --shot A-B --email ignitefindyourfire@gmail.com
```

This command is deliberately limited to the pilot's **one A → B video**. It
defaults to **ignitefindyourfire@gmail.com**, checks `GET /accounts` for
`health: "OK"`, pins that account for all uploads and jobs, and uses
`GET /accounts/{email}` to check current health and the Flow credit balance
before any uploads. The account must use the current `flow` backend. Other
connected accounts are never selected as a fallback. To check the inputs,
account and credit budget without uploads, generation or state changes, use:

```bash
python3 workflow/scripts/shorts.py generate calculus_pilot --shot A-B --email ignitefindyourfire@gmail.com --dry-run
```

Use the same command on reruns. `--email` can explicitly override the default;
saved jobs must always be resumed with their original account. One regular Veo
3.1 Lite video needs **10 Flow credits**, or **5 on Ultra**; the account's reported
first/last-frame model cost takes precedence when available. Health and the video
budget are checked again immediately before the video generation. A job
already submitted can be polled even if its charge depleted the balance. The
token is read only from the environment and is never saved or printed; account
cookies returned by the API are also never logged or saved.

Existing finished `keyframes/A.png` and `keyframes/B.png` are required and reused
without alteration. If either is missing, the command names every missing path
and stops before contacting the API. It never generates replacement images or
uses blocking guides as finished art. Both frames must pass the portrait image
check before uploads. A saved video job can still resume if local frames or
prompts have since changed or been removed.

The video request uses `startImage` **and** `endImage`, `count: 1`, `async: true`,
Veo 3.1 Lite (`veo-3.1-lite`), portrait, **720p**, and **8 seconds**. Eight seconds is supported across paid
Flow tiers; the old manual prompt's five seconds is not a Veo duration. The shot
1 prompt in `flow-video-prompts.md` is reused with an explicit continuous A → B
ending and eight-second wording. Sol hops onto the moving board, lands, and
wobbles exactly once to catch his balance, reaching B by three seconds before
holding. Prompts preserve the compact flame shape, original eyes, stubby limbs
and mouthless face. Episode edits and cue timing are preserved.

Job IDs, submitted prompts, uploaded-file hashes, and verification results are
saved atomically in `episodes/calculus_pilot/jobs/useapi/A-B.json` (Git ignored).
After `SAVED JOB` appears, Ctrl-C or a polling timeout can be recovered by running
the exact same command. It polls the saved job instead of submitting another.
The default wait is 1,200 seconds per job; `--wait-timeout` and `--poll-interval`
can adjust polling. A second concurrent invocation is blocked by a local lock.
Keep this state directory until the result is safely downloaded.

If a submission loses its response before a job ID arrives, reruns stop for
review instead of risking a duplicate charge. Find the job in useapi.net and
add its ID as `job_id` to the `video` entry in
the local state file. A failed or expired job also stops without replacement;
inspect it before deliberately starting new work. HTTP errors never cause
automatic generation retries.

The MP4 is downloaded to a temporary file, then FFprobe checks the container,
video codec, frame rate, portrait dimensions (at least 720 × 1280), and enough
duration for the existing 3.6-second hop cue. Only a passing file is placed at
`workflow/episodes/calculus_pilot/clips/01-hop-on.mp4`. Existing files are
preserved and verified on reruns. Pass `--ffprobe /full/path/to/ffprobe` or set
`FFPROBE_PATH` if needed. Open the completed result with:

```bash
open workflow/episodes/calculus_pilot/clips/01-hop-on.mp4
```

When that clip already exists, a normal run verifies it locally and exits
without using the API. `--dry-run` also performs the live account/credit checks
in that case, but needs `USEAPI_TOKEN`. An output whose hash differs from its
saved generation state is preserved and reported as a filename collision.

Protocol references: useapi.net's [account health](https://useapi.net/docs/api-google-flow-v1/get-google-flow-accounts),
[account credits](https://useapi.net/docs/api-google-flow-v1/get-google-flow-accounts-email),
[raw asset uploads](https://useapi.net/docs/api-google-flow-v1/post-google-flow-assets-email),
[start/end-frame video generation](https://useapi.net/docs/api-google-flow-v1/post-google-flow-videos),
[job polling](https://useapi.net/docs/api-google-flow-v1/get-google-flow-jobs-jobid),
and [download URL refresh](https://useapi.net/docs/api-google-flow-v1/get-google-flow-assets-mediagenerationid).

## Check for missing or unusable media

```bash
python workflow/scripts/shorts.py check calculus_pilot
python workflow/scripts/shorts.py check calculus_pilot --images
python workflow/scripts/shorts.py check calculus_pilot --probe
```

The first command prints the full canonical path for every missing clip or
voiceover and exits 1. `--images` also checks the A/B/D image download slots.
`--probe` checks available clip lengths and voice duration using FFmpeg.
`--json` produces a structured report. An unconfirmed voice cue map is noted
separately; media can be present while final timing is still pending.

After importing Cub narration, an animatic build creates
`audio/voiceover-cues.suggested.json` if confirmed timing is absent. Its times
are explicitly estimates. Measure the paragraph boundaries against the real
recording and set `tangent_reveal_sec` to the spoken onset of “Tangent”. Save
the checked map as `audio/voiceover-cues.json` with `confirmed: true` and the
recording's `source_sha256`. Replacing the audio invalidates old confirmation.
The hop/lean/graph/reaction cues must be contiguous across the episode duration.

## Render a preview or final

```bash
python workflow/scripts/shorts.py render calculus_pilot --animatic
python workflow/scripts/shorts.py render calculus_pilot
python workflow/scripts/shorts.py render calculus_pilot --captions soft
```

`--animatic` permits labeled placeholder shots and temporary speech. It never
represents local speech as Cub. The final command requires all three clips,
the actual voice download, and confirmed cues tied to that recording. Missing
media or timing stops a final export rather than silently replacing it.

Exports go into the episode's `renders/` folder. Existing named exports are
moved to `renders/archive/run-<timestamp>/` before a new run. The old pilot
renders are preserved under `renders/`, including `renders/archive/v1/`.
Final video is H.264/AAC MP4; each export is fully decoded as a verification.
`renders/validation.json` records the exact output and pending inputs.

Captions are editable in the cue config and generated `captions.srt`.
`--captions soft` creates a selectable subtitle track; `--captions none`
omits it. Clean picture, graph/tangent SVGs and audio stems remain separate.
The graph and tangent are calculated locally and never generated by Flow.

## Shared files and compatibility

- `scripts/`: prepare/check CLI, existing artwork helpers and renderer.
- `config/`: format, painted style, caption appearance and Cub preference.
- `assets/`: the two reusable artwork copies, fonts/OFLs, and the pre-existing
  music downloads. The earlier preview from Music is preserved there too.
- `templates/`: editable episode and Flow prompt starting points.
- `episodes/`: all per-episode scripts, plans, prompts, media and renders.
- `tests/`: workflow path, preservation, missing-media and graph checks.
- `migration/`: original inventory, exact move list and pre-change text copies.
- `vendor/`: the original upstream generator, with its original sample files.

The old `zack-d-films-ai-video-generator-main/` and `Music/` paths are
compatibility links. The generator's original entry points still work, and
the old calculus script delegates to the new workflow implementation.
All new work belongs here, not in vendor. The legacy pilot `imports/` is
still accepted for existing downloads; new media belongs in clips/audio.

Credentials, virtual environments, caches, downloaded clips/audio, generated
images and renders are ignored by Git. They remain on disk. Ignore rules do
not retroactively untrack files already in Git; no credentials were inspected
or staged, and no commit was made during this move.

## Checks

```bash
python -m unittest discover -s workflow/tests -v
python -m compileall -q workflow/scripts
```

No automated test suite was present in the original upstream package. Its
Python sources remain available for syntax checks under `workflow/vendor/`.
