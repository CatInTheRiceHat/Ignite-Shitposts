# Episodes

Each episode owns its scripts, edit settings, artwork, media and renders.
Reusable Remotion code and the single npm install live in
[../remotion/](../remotion/README.md). Custom compositions can stay in an
episode's own `remotion/` folder.

| Episode | Editable source | Media and renders |
| --- | --- | --- |
| [Calculus pilot](calculus_pilot/README.md) | Narration, Python `edit.json`, shot plan and Flow prompts | Its `keyframes/`, `clips/`, `audio/` and `renders/` |
| [Zipper demo](zipper_demo/README.md) | [edit.json](zipper_demo/edit.json), rendered by the shared engine | Its `public/` assets and `renders/` outputs |
| [Sol lantern / Kling test](sol_kling_test/README.md) | Generation request, `audio-test.json` and custom `remotion/` composition | Its `keyframes/`, `clips/`, `audio/` and `renders/` |

## Remotion episodes

```text
workflow/
  remotion/                  Shared renderer, components, tools and dependencies
  episodes/
    zipper_demo/
      edit.json
      public/
      renders/
    sol_kling_test/
      remotion/              Custom composition and verification
      clips/
      audio/
      renders/
```

From the repository root:

```bash
npm --prefix workflow/remotion ci
npm --prefix workflow/remotion run dev -- zipper_demo
npm --prefix workflow/remotion run render -- zipper_demo
npm --prefix workflow/remotion run sol:check
npm --prefix workflow/remotion run sol:render
```

To start another standard Remotion short, copy
[the neutral starter](../templates/remotion-episode.json) into a new episode's
`edit.json`, then run `setup-assets` and `dev` for its name. See the
[shared engine guide](../remotion/README.md) for the complete commands. Every
standard edit uses its own `public/` and `renders/`; it does not need another
npm project. The Sol test demonstrates an episode-specific composition.

## Python episodes

Prepare with `python3 workflow/scripts/shorts.py prepare <name>` from the
repository root. Prepare preserves existing edits and downloads. The typical
layout is:

```text
<episode>/
  narration.txt
  edit.json
  shot-plan.json
  flow-image-prompts.md
  flow-video-prompts.md
  keyframes/
  clips/
  audio/
  layers/
  plans/
  renders/
```

The Python CLI uses the calculus template and does not prepare or render the
Remotion examples; their edit schemas differ. Provider job records stay in
the episode's ignored `jobs/` directory. Keep audio in its real format, preserve
render archives and approved media, and flag differing filename collisions.
