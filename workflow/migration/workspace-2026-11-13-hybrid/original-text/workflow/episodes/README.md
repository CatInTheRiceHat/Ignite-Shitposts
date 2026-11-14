# Episodes

Use this index to find an episode's editable source and completed work.
New Python episodes are prepared with
`python3 workflow/scripts/shorts.py prepare <name>` from the repository root.
Prepare preserves existing edits and downloads.

| Episode | Editable source | Media and renders |
| --- | --- | --- |
| [Calculus pilot](calculus_pilot/README.md) | `calculus_pilot/`: narration, `edit.json`, shot plan and Flow prompts | The same folder's `keyframes/`, `clips/`, `audio/` and `renders/` |
| [Sol lantern / Kling test](sol_kling_test/README.md) | `sol_kling_test/`: generation request, `audio-test.json` and `remotion/` | The same folder's `keyframes/`, `clips/`, `audio/` and `renders/` |
| [Zipper demo](zipper_demo/README.md) | `zipper_demo/remotion/`: [episode JSON](zipper_demo/remotion/episodes/zipper.json), source and `public/` assets | Working outputs in `zipper_demo/remotion/out/`; the preserved verified delivery is in `zipper_demo/renders/` |

## Remotion projects

Each Remotion episode owns its composition, configuration and assets in its
own `remotion/` folder. Dependencies are installed once at the episodes root:

```text
episodes/
  package.json              Shared npm workspace and dependency versions
  package-lock.json
  tsconfig.remotion.json    Shared TypeScript defaults
  node_modules/             Local shared install; ignored by Git
  zipper_demo/
    remotion/               Zipper source, settings, public assets and tools
    renders/                Preserved delivery
  sol_kling_test/
    remotion/               Sol composition and renderer
    clips/
    audio/
    renders/
  calculus_pilot/            Python/FFmpeg episode
```

Install dependencies from the repository root with:

```bash
npm --prefix workflow/episodes ci
```

Then use these commands from the repository root:

```bash
npm --prefix workflow/episodes run zipper:dev
npm --prefix workflow/episodes run zipper:render
npm --prefix workflow/episodes run sol:check
npm --prefix workflow/episodes run sol:render
```

You can also run `npm run dev`, `npm run render`, and the other local scripts
from `zipper_demo/remotion/`. The Sol project's scripts are `check` and `render`.
For another Remotion episode, create `episodes/<name>/remotion/` and register
its package in the root `package.json` workspaces. Share the root dependencies;
keep the new composition, settings, assets and outputs with its episode.

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

The zipper project's exact editing instructions are in its
[Remotion guide](zipper_demo/remotion/README.md). The Python CLI's calculus
template does not prepare or render the two Remotion examples.
