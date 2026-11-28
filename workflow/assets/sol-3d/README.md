# 3D Sol

The reference Sol for every clip. **Approved by Elaine on 2026-11-25** ("YES ... that is what i want,
lets save that"). The approved copy is frozen in `approved-2026-11-25/`; do not overwrite that folder.

| File | What it is |
| --- | --- |
| `sol.blend` | The model. Collection `SOL`, root `RIG_Sol` at his feet, 1.0 tall. Append the collection into a scene. |
| `sol-turnaround.png` | Front, three-quarter, side and back. Hand this to the painter as the Sol reference. |
| `sol-logo.blend`, `sol-logo-turnaround.png` | The logo version: the same body with no arms or legs (collection `SOL_LOGO`). Built with `LIMBS = False`. Saved at Elaine's request 2026-11-25. |
| `sol-vs-mascot.png`, `sol-legs-check.png` | The model beside Mascot.png, and the legs with the mascot's outline drawn over them. |
| `prepare_sol.py` | Step 1, plain Python: traces Logo.png and inflates it, measures the legs off Mascot.png, makes the textures. |
| `build_sol_model.py` | Step 2, inside Blender with `OUT_DIR` set: builds the mesh, renders the views, writes `sol.blend`. |
| `compare.py` | Rebuilds the turnaround and the check images, and prints how closely the legs match. |

## How he is made (Elaine's method)

1. **Body:** the real outline of `reference-art/Logo.png` (Sol with no legs) is traced and inflated like a
   balloon. The logo art itself is wrapped on the front, so the layers, colours and eyes are exactly his.
   The back is plain body red.
2. **Legs:** not inflated. Their outline is read off `reference-art/Mascot.png` row by row and spun into a
   round limb with no reshaping: wide where it joins the body, sides closing in, blunt rounded tip. They sit
   exactly where the mascot has them.
3. **Arms:** the same leg shape, 1.9 times as long, pointing out and down from his sides.

## What was rejected on the way

- Building him by hand from estimated points, or as a gumdrop: "this does NOT look like sol".
- Legs and arms narrowed or made into tapered ovals: too pointy ("not too pointy look at the reference").
- A brown streak along the sides: the soft brownish edge of the logo art smeared along the seam. Fixed by
  using only clean interior colour near the outline.

Rebuild: `python3 prepare_sol.py`, then run `build_sol_model.py` in Blender (once as is for Sol, once with
`LIMBS = False` for the logo), then `python3 compare.py`. The guideline that tells people to use him is
`../../guidelines/sol-3d-model.md`.

## poses/

Painted reference frames of poses Elaine has approved for Sol. `hands-on-hips-approved-2026-11-28.png`: his nubs tucked
against his sides ("yyayyyyy looks good! lets keep that for the sol model"). How to pose and prompt it:
`guidelines/sol-3d-model.md`, "Poses Elaine has approved".

