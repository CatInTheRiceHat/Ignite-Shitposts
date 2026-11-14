# Calculus media locations

From the repository root, use these exact paths:

| Download | Destination |
| --- | --- |
| Flow Image A, hop opening | `workflow/episodes/calculus_pilot/keyframes/A.png` |
| Flow Image B, low side lean | `workflow/episodes/calculus_pilot/keyframes/B.png` |
| C exact graph | Already generated locally at `workflow/episodes/calculus_pilot/keyframes/C.png` |
| Flow Image D, reaction | `workflow/episodes/calculus_pilot/keyframes/D.png` |
| First Flow clip | `workflow/episodes/calculus_pilot/clips/01-hop-on.mp4` |
| Second Flow clip | `workflow/episodes/calculus_pilot/clips/02-low-side-lean.mp4` |
| Third Flow clip | `workflow/episodes/calculus_pilot/clips/03-reaction.mp4` |
| MoGoFun Cub (Female) audio | `workflow/episodes/calculus_pilot/audio/mogofun-narration.mp3` |
| Confirmed timing | `workflow/episodes/calculus_pilot/audio/voiceover-cues.json` |

Full audio path:
`/Users/elaine/Documents/Ignite Shitposts/workflow/episodes/calculus_pilot/audio/mogofun-narration.mp3`

Use the episode's `narration.txt` in MoGoFun, voice **Cub (Female)**, off-screen.
Keep WAV or M4A downloads in their real format with the same basename; keep
only one voiceover. Never rename WAV data to MP3. Original Flow audio is muted.

Read the actual recording and set the cue boundaries at “How steep…”,
“Tangent line…”, and “Tiny arms…”. Pin tangent_reveal_sec to the onset of
“Tangent”. The generated suggested cue file is only an estimate. Confirm the
measured cue file and retain its source_sha256 to bind timing to this recording.
Final rendering refuses missing or stale timing. An overlong narration is
reported instead of silently cut or accelerated.

```bash
python3 workflow/scripts/shorts.py check calculus_pilot --probe
python3 workflow/scripts/shorts.py render calculus_pilot --animatic
python3 workflow/scripts/shorts.py render calculus_pilot
```

New media belongs in clips/audio. Any existing legacy imports are preserved
and accepted as a fallback; moving an old download is never required just
to render. See `../../README.md` for setup, checks and shared settings.
