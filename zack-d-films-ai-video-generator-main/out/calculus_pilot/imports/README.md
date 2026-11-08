# Media drop folder

Save all media in this exact directory:

`/Users/elaine/Documents/Ignite-Shitposts/zack-d-films-ai-video-generator-main/out/calculus_pilot/imports/`

| File | Content |
| --- | --- |
| `01-hop-on.mp4` | Generated 5-second portrait hop/landing clip |
| `02-low-side-lean.mp4` | Generated 5-second low side angle/balance clip |
| `03-reaction.mp4` | Generated 4-second deadpan reaction clip |
| `mogofun-narration.mp3` | Actual MoGoFun **Cub (Female)** off-screen narration download |
| `voiceover-cues.json` | Confirmed cut/caption boundaries and tangent-word onset for this exact recording |

Do not rename WAV data to `.mp3`. If MoGoFun supplies WAV or M4A, use
`mogofun-narration.wav` or `mogofun-narration.m4a` instead. Keep only one
voiceover format in this directory. The renderer preserves its pacing;
it does not silently shorten or speed up the MoGoFun performance.

Paste into MoGoFun, keeping the paragraph breaks as short pauses:

```text
Sol brought confidence. Not brakes.

How steep is this curve right here?

Tangent line. Its slope is the derivative.

Tiny arms. Massive responsibility.
```

Voice direction: Cub (Female), off-screen; dry, playful delivery, roughly
14–15 seconds total. Small pause after “confidence,” a clear “Tangent,” and
a deadpan last sentence. Sol remains mouthless and never lip-syncs.

## Timing the actual recording

The initial preview's cue times are placeholders, not an analysis of a
MoGoFun recording. On the first build after an audio import, the renderer
creates `voiceover-cues.suggested.json`. Those are explicitly estimated
boundaries. Listen to the recording and set:

1. The hop/low-side cut to the start of “How steep…”.
2. The graph cut to the start of “Tangent line.”
3. `tangent_reveal_sec` to the exact onset of “Tangent”.
4. The reaction cut to the start of “Tiny arms.”

Cue boundaries describe contiguous edit sections from 0 to 15 seconds;
caption text and boundaries use the same editable cues. Put a brief action
hold into `hold_sec` for the imported clip if needed. Adjust `in_sec` to find
the board-contact match frame; the code cannot certify a generated clip's
composition without visual review.

Save the checked cue map as `voiceover-cues.json` and set `confirmed: true`.
Keep `source_sha256` from the suggested file: replacing the audio invalidates
old timing confirmation. Until the voice cues are checked, the output stays
labeled as an animatic, even if generated clips are available.

Run from the video repository root:

```bash
python3 scripts/calculus_pilot.py --ffmpeg /path/to/ffmpeg
```

Missing footage uses a clearly marked animatic pose plate. All imported
clip audio is discarded. Once all three clips, the real voiceover, and its
confirmed cues exist, the same command exports `../final.mp4`. To require
these inputs and refuse a placeholder export:

```bash
python3 scripts/calculus_pilot.py --ffmpeg /path/to/ffmpeg --require-final
```
