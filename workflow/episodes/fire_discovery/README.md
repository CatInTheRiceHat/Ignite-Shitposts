# How Fire Was Discovered: start here

This folder holds every version. These are the files that matter right now
(per `handoff.txt`, v14 continuous-music delivery):

| What | Where |
| --- | --- |
| Delivered video | `../../completed/How Fire Was Discovered.mp4` |
| Current edit | `edit.json`, selected version `edit-continuous-music-v14.json` |
| Current script/storyboard | `script-continuous-music-v14.txt` |
| Latest handoff and receipt | `handoff.txt`, `revisions/continuous-music-v14/review/verification.json` |
| Elaine's feedback log | `feedback.txt` |

Clips the current edit pulls from:

| Scene | Clip |
| --- | --- |
| 01 | `revisions/chimney-ripple-v2/clips/01-selected-brief-blink.mp4` |
| 02 | `revisions/monkey-cartoon-cloud-v3/clips/02-fight-cloud-v2-selected.mp4` |
| 03 | `clips/edit-v4/03-lightning-with-sting-gap.mp4` |
| 04 | `clips/edit-v2/04-tight.mp4` |
| 05 | `revisions/night-camp-v3/clips/05-scene.mp4` |

Voices come from `audio/trimmed-v2/` and `audio/sound-v4/`.

## Everything else is history

- `edit-*.json` and `script-*.txt` (other than v14): earlier cuts, kept for the record.
- `revisions/<name>-vN/`: one folder per correction pass, each with its own
  clips, keyframes, reviews and renders.
- `reviews/`: frame checks and audits from earlier passes.
- `renders/`: drafts and earlier finals (`*-final.mp4` per version).
- `jobs/higgsfield/`: generation job receipts.

Don't move these folders: the edit files point at them with relative paths.
