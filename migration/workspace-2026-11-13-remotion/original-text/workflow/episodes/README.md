# Episodes

Use this index to find an episode's editable source and completed work.
New Python episodes are prepared with
`python3 workflow/scripts/shorts.py prepare <name>` from the repository root.
Prepare preserves existing edits and downloads.

| Episode | Editable source | Media and renders |
| --- | --- | --- |
| [Calculus pilot](calculus_pilot/README.md) | `calculus_pilot/`: narration, `edit.json`, shot plan and Flow prompts | The same folder's `keyframes/`, `clips/`, `audio/` and `renders/` |
| [Sol lantern / Kling test](sol_kling_test/README.md) | `sol_kling_test/`: generation request, `audio-test.json` and `remotion/` | The same folder's `keyframes/`, `clips/`, `audio/` and `renders/` |
| [Zipper demo](zipper_demo/README.md) | The standalone Remotion project's [episode JSON](../remotion/episodes/zipper.json), source and `public/` assets | Renderer outputs in `../remotion/out/`; the preserved verified delivery is in `zipper_demo/renders/` |

For a Python episode, the usual structure is:

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

Provider job records stay in that episode's ignored `jobs/` directory.
Keep downloaded audio in its real format. Keep render archives and approved
media; do not replace a differing existing file to resolve a naming collision.

The zipper project keeps its own working layout so its existing npm commands
and relative asset paths continue to work. Its exact instructions are in the
[Remotion guide](../remotion/README.md). The Python CLI's calculus template
does not prepare or render the two Remotion examples.
