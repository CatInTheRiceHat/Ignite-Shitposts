# Zipper demo

This existing 20-second, 1080 × 1920, 30 fps edit is one episode rendered by the
[shared Remotion engine](../../remotion/README.md).

- [edit.json](edit.json): hook, script, shots, captions, artwork paths and optional narration.
- `public/art/zipper/`: editable SVG study artwork.
- `public/art/ignite/` and `public/fonts/`: local shared-reference and font copies.
- `public/clips/` and `public/audio/`: optional imported footage and narration.
- `renders/`: new exports and the preserved verified delivery.
- `renders/remotion/`: outputs and stills previously in `remotion/out/`.

From the repository root:

```bash
npm --prefix workflow/remotion run dev -- zipper_demo
npm --prefix workflow/remotion run render -- zipper_demo
npm --prefix workflow/remotion run still -- zipper_demo --frame 270
```

Install dependencies once with `npm --prefix workflow/remotion ci`.
New renders default to `renders/zipper.mp4`; prior outputs are archived before
replacement. The default edit remains silent, and its zipper art is labeled
study artwork. Replace that art and time imported narration deliberately.

Asset paths in the JSON are relative to this episode's `public/` folder.
The shared engine guide documents layer placement, camera motion, imported
MP4s and optional narration. The zipper JSON and all existing media retain
their contents; only their file locations have changed.
