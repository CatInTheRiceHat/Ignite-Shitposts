# Ignite Shorts workflow

This is the home for all Ignite Shorts files. Run the commands below in VS
Code's terminal with this repository open as the workspace root. Paths are
resolved from this workflow or the episode folder, so an episode name never
depends on the terminal's current directory.

## Find your files

| Folder | Contents |
| --- | --- |
| [guidelines/](guidelines/README.md) | Script structure, painted style, Sol rules and shot planning |
| [episodes/](episodes/README.md) | Episode edits, scripts, plans, prompts, artwork, media, renders and custom compositions |
| [assets/](assets/README.md) | Shared character/style references, reference artwork, fonts and music |
| `config/` | Shared format, narration, style and caption defaults |
| `templates/` | Starting episode JSON and image/video prompt documents |
| `scripts/` | Canonical Python CLI, generator integration and renderer |
| [remotion/](remotion/README.md) | Shared Remotion renderer, components, tools and one dependency install |
| `tests/` | Python workflow checks |
| `vendor/` | Preserved upstream generator and examples |
| `migration/` | Move records, original text and preservation reports |

Read the [creative guidelines](guidelines/README.md) before developing an
episode. Use the [episode index](episodes/README.md) to choose its renderer.
New episodes use complete generated Higgsfield clips and the shared Remotion
editor. The calculus pilot retains its older Python renderer and Cub voice.

## Current Higgsfield production workflow

Codex generates the media through the connected Higgsfield tools. The episode's
`higgsfield-prompts.txt` supplies the reviewed prompts; no manual prompt entry
or download handoff is required. Generate and inspect Scene 01 first, then use
approved frames as references for the remaining scenes. Keep the mechanism
inside the generated footage. Remotion only assembles clips, voices, captions
and sound.

The shared settings for every active workspace client are in
`config/generation.json`. Video now uses **Gemini Omni Flash 1.2**
(`gemini_omni_flash_1_2`), `image-to-video`, 1080p, 9:16, with BOTH approved
frame inputs. Paired-frame clips are 3–10 whole seconds; declare continuing
subscenes for a longer shot. Image generation uses **Nano Banana 2.1**
(`nano_banana_2_1`), 2k, 9:16, with its separate image settings in the same config.

**Frames first:** generate the first and last stills, show BOTH to the user,
wait for explicit approval of that exact pair, then generate its Higgsfield
clip. A request to fix an old take is not approval of the new stills. Run
`review-frames`, `approve-frames` (only with the user's actual approval), and
`video-request` through the canonical CLI. No pair is approved automatically.

After generation, `review-clip` prepares every source frame, actual timestamps,
full-resolution detail samples and the reference comparison for the dedicated
reviewer. Failed, uncertain or stale reviews block production, including the
direct Remotion final command. See
[the reviewer workflow](guidelines/clip-review-guide.txt). Preparation and a
successful decode do not themselves establish visual correctness.

1. Run `python3 workflow/scripts/shorts.py prepare <episode>`. New skits use
   full-screen 1080 × 1920 footage, the shared Arthur/Sol cast and editable
   white captions with orange outlines. Existing scripts and media are preserved.
2. Review the complete script/storyboard and the separate 2N image / N video
   prompts. Generate and show both stills; wait for the user's explicit approval
   before submitting the paired-frame Omni Flash 1.2 video request. Save job receipts under the episode's ignored
   `jobs/higgsfield/`. Resume saved jobs rather than submitting duplicates.
3. Codex records each spoken turn with its exact saved voice pair at
   `speech_rate: 0`. Save each take under `audio/<scene>-<turn>-<speaker>.wav`,
   for example `audio/03-02-narrator.wav`. Source clips live in `clips/`;
   `public/clips` and `public/audio` link to those originals.
4. Run `python3 workflow/scripts/shorts.py sync-audio <episode>` to measure the
   takes at 1x and extend scenes if needed. Its caption boundaries are marked
   provisional; review actual speech, acting and captions before confirming
   timing. Generate videos long enough for those measured scene lengths.
5. Run the independent clip review, then `python3 workflow/scripts/shorts.py check <episode> --images --probe`.
   Use `npm --prefix workflow/remotion run dev -- <episode>` for review.
   Set `edit.json`'s `timing.confirmed` only after reviewing the real takes and
   caption cues. `python3 workflow/scripts/shorts.py render <episode>` checks
   media and voice hashes before exporting.
   `render <episode> --draft` exports actual downloaded media with provisional
   timing to a clearly named draft MP4; it still requires every clip and take.

Arthur's exact preset ID and Sol's exact custom element ID are verified in
`config/voices.json`. No Cub substitution or accelerated speech is used in
new skits. The `generate ... --shot A-B` command below is specifically the
preserved calculus Flow integration; skit generation uses Codex's Higgsfield
connection.

New two-voice skits use **Arthur** as the off-screen Narrator and the user's
**Higgsfield custom voice Sol** for Sol. The [shared voice cast](config/voices.json)
stores the exact custom voice ID and `voice_type: element`. Use that saved
pair for Sol's dialogue. Keep speech at the provider's normal rate and 1x
playback. When the Narrator addresses Sol on screen, cue Sol looking upward
toward the voice just above the camera, breaking the fourth wall; he can
look back at the mechanism when the explanation directs him there.

Reusable Remotion code and dependencies live in `remotion/`. Episodes own
their edit JSON, public assets and renders; a custom composition can live in
`episodes/<name>/remotion/`. The shared engine accepts an episode name or an
edit JSON path. Start a new Remotion short from
`templates/remotion-episode.json`; see the [Remotion guide](remotion/README.md).

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
for an animatic uses macOS `say`; imported voice recordings work without `say`.

## Prepare an episode

```bash
python workflow/scripts/shorts.py prepare calculus_pilot
python workflow/scripts/shorts.py prepare my_next_short
```

New skits use a **30-second target, 1080 × 1920, 30 fps** vertical format.
Scenes with a reviewed shot plan retain their planned timing until voices are
measured. The Python calculus renderer uses 720 × 1280.
The existing calculus pilot keeps its explicit **15-second** edit. To create
another intentional duration, use `prepare name --duration 15` the first time.
Prepare never replaces an existing script, prompt, edit JSON, image or clip.
Existing files are reused; it does not reset edits to the template.

For skits, edit `script.txt`, `higgsfield-prompts.txt`, `shot-plan.json` and
`edit.json` in the episode folder. Keep dialogue, prompt context, separate
voice scripts and captions in sync. The preserved calculus pilot uses its
`narration.txt` and two Flow prompt documents described below.

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

The existing calculus pilot retains **MoGoFun → Cub (Female)** as its
off-screen narrator. New skits use the shared Arthur/Sol cast above. For the
pilot, paste the episode's
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
- `guidelines/`: script, style and Sol/shot production guides.
- `config/`: shared voice cast, plus format, style and caption settings in the existing workflow layout. Earlier calculus narration settings preserve its Cub recording.
- `assets/`: reusable Sol/style references, `reference-art/` (formerly root
  `graphics/`), fonts/OFLs and local `music/` downloads. The earlier music
  preview is preserved there too.
- `templates/`: Python and generic Remotion episode starters and Flow prompts.
- `episodes/`: per-episode scripts, plans, prompts, media, renders and
  optional custom `remotion/` compositions.
- `remotion/`: reusable renderer, components, tools and the single npm install.
- `tests/`: workflow path, preservation, missing-media and graph checks.
- `migration/`: original inventory, exact move list and pre-change text copies.
- `vendor/`: the original upstream generator, with its original sample files.

The root `zack-d-films-ai-video-generator/` and `music/` paths are
compatibility links. The generator's original entry points still work, and
the old calculus script delegates to the new workflow implementation.
All new work belongs here, not in vendor. The legacy pilot `imports/` is
still accepted for existing downloads; new media belongs in clips/audio.
See the [workspace move record](migration/workspace-2026-11-13/README.md)
for old-to-new folder locations and preservation checks.
The [Remotion move record](migration/workspace-2026-11-13-remotion/README.md)
records its subsequent organization into episode-local projects.
The [hybrid move record](migration/workspace-2026-11-13-hybrid/README.md)
records the current shared engine and episode-owned content.

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
