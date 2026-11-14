# Shared assets

Keep reusable assets here. Keep episode-specific keyframes, clips, narration
and renders with their episode; see the [episode index](../episodes/README.md).

| Location | Purpose |
| --- | --- |
| `sol-full-body.png` | Approved original Sol character reference |
| `calculus-painted-scene.jpg` | Painted world, texture and lighting reference |
| `reference-art/` | Existing Ignite artwork copies, previously in root `graphics/` |
| `fonts/` | Shared fonts and their license files |
| `music/` | Existing local music downloads and the older `ignite-sol-shorts-preview.mp4` |

Use the [creative guidelines](../guidelines/README.md) when choosing and
generating art. Preserve originals and flag differing filename collisions.
The `Ignite Website` repository remains a read-only source.

Sol's reference roles are recorded in `../config/sol-references.json`.
`reference-art/Mascot.png` defines the neutral design. The newly supplied
Curious, Puzzled, Artist, Celebrate and Lightbulb examples clarify the same
character across poses. Preserve the broad cream inner flame, low-set navy
oval eyes, outer flame lobes and compact nub limbs. Keep the painted treatment
the user accepted; example props and expression-specific accessories do not
belong in the neutral escalator shot. The lantern video guides finish/motion.

The zipper episode keeps renderer-ready copies in
`../episodes/zipper_demo/public/`. From `workflow/remotion/`, run
`npm run setup-assets -- zipper_demo` to copy the shared Sol,
painted reference and Nunito font; modified destination artwork is preserved.

Downloaded music stays local and is ignored by Git. The root `music/` path
is a compatibility link to this folder's `music/` directory.
