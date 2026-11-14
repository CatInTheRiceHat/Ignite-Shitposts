# Sol lantern / Kling test

This existing episode is a **4-second** painted lantern shot. Its downloaded
Kling clip is 720 × 1280; the Remotion preview places it without cropping in
a 1080 × 1920, 30 fps composition. Preserve the episode's custom Sol voice
override in `audio-test.json`; the shared default for new shorts remains Cub.

- `generation-request.json`: submitted shot settings, prompt and source art.
- `keyframes/` and `clips/`: approved first frame and downloaded footage.
- `audio-test.json` and `audio/`: voice choice, recordings and mix settings.
- `prepare-audio.py`: builds the draft mix at 1× narration playback.
- `remotion/`: composition and preview renderer.
- `renders/`: previews, verification records and visual review.
- `jobs/`: local provider job history; preserve it for recovery.

From the repository root, check the composition without rendering footage:

```bash
node workflow/episodes/sol_kling_test/remotion/render.mjs --check-composition
```

To render from the existing local media:

```bash
python3 workflow/episodes/sol_kling_test/prepare-audio.py
node workflow/episodes/sol_kling_test/remotion/render.mjs --with-audio
```

The renderer uses dependencies installed in `workflow/remotion/`. See the
[Remotion guide](../../remotion/README.md) for installation. Review the saved
audio settings before rebuilding a mix; differing existing outputs are
preserved and reported. These commands do not submit generation jobs.
