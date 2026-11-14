# Zipper demo

The existing **20-second, 1080 × 1920, 30 fps** demo is edited and rendered
with this episode's [Remotion project](remotion/README.md).

- Edit the [zipper episode JSON](remotion/episodes/zipper.json) for the
  script, shots, captions, layer paths and optional narration.
- Editable SVG artwork lives in `remotion/public/art/zipper/`.
- Working renders and stills live in `remotion/out/`.
- This episode's `renders/` retains the previously verified delivery and
  verification record.

From the repository root:

```bash
cd workflow/episodes/zipper_demo/remotion
npm run dev
# Or render the existing local demo:
npm run render
```

The default demo is silent and its zipper art is labeled study artwork.
Follow the Remotion guide to replace artwork or import narration and clips.
Keep the existing 20-second edit unless changing it intentionally.

Dependencies are shared with the other Remotion episodes. Install them once
with `npm --prefix workflow/episodes ci` from the repository root; see the
[episode index](../README.md) for workspace commands.
