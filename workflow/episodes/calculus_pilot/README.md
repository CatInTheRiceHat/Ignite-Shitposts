# Calculus pilot — A → B → C → D

This existing episode keeps its 15-second edit. New workflow episodes default
to 30 seconds. Start with [the workflow entry point](../../README.md).

- A: Sol hops onto the moving board; `keyframes/A.png`, `clips/01-hop-on.mp4`.
- B: Low side lean and tiny balance arm; `keyframes/B.png`, `clips/02-low-side-lean.mp4`.
- C: Exact graph and tangent; local `keyframes/C.png` and editable `layers/`.
- D: Reaction hold; `keyframes/D.png`, `clips/03-reaction.mp4`.

The original episode narration, edit JSON, detailed Flow Video prompts,
blocking frames, SVGs, audio stems, previous previews and renders have been
moved here. Shared artwork and fonts live in `../../assets/`; `assets/` is
only a compatibility link. Flow images go in `keyframes/`, clips in `clips/`,
and the MoGoFun Cub (Female) download in `audio/mogofun-narration.mp3`.
Read `MEDIA.md` for exact import/timing instructions. No website file is edited.

```bash
python3 workflow/scripts/shorts.py prepare calculus_pilot
python3 workflow/scripts/shorts.py generate calculus_pilot --shot A-B
python3 workflow/scripts/shorts.py check calculus_pilot
python3 workflow/scripts/shorts.py render calculus_pilot --animatic
python3 workflow/scripts/shorts.py render calculus_pilot
```

Run those commands from the video repository root. `narration.txt` and
`edit.json` remain the editable script/cue sources. `shot-plan.json` names
all four frames. The graph is y=sqrt(x), with slope 1/2 at (1,1); the tangent
reveal is tied to the spoken “Tangent” cue after real voice timing is confirmed.

`generate` needs an exported `USEAPI_TOKEN` and a healthy connected Flow
account. It generates only A → B with both frames attached, reusing finished
A/B images or making the missing ones from the original references. Rerun the
same command to resume the job saved in `jobs/useapi/A-B.json`. After FFprobe
verification, open it with `open workflow/episodes/calculus_pilot/clips/01-hop-on.mp4`.
See the workflow README for token setup, API details and recovery behavior.

The previous playable animatic is `renders/animatic.mp4`; old versions remain
under `renders/archive/`. Generated local speech stays clearly temporary.
Prior layout text is preserved in `../../migration/original-text/`, and all
pre-move file hashes are in `../../migration/before.json`.
