# Sol 3D model: the reference for every clip

Approved by Elaine on 2026-11-25: "YES ... that is what i want, lets save that". Use this Sol, not a
hand-built stand-in and not a description from memory. Read this before blocking a skeleton or writing a
paint prompt that has Sol in it.

![Sol turnaround](sol-3d/sol-turnaround.png)

## The two models

| Model | Picture | File | Use it for |
| --- | --- | --- | --- |
| **Sol** (arms and legs) | [sol-turnaround.png](sol-3d/sol-turnaround.png) | `../assets/sol-3d/sol.blend`, collection `SOL` | The character in clips. |
| **Sol logo** (body only) | [sol-logo-turnaround.png](sol-3d/sol-logo-turnaround.png) | `../assets/sol-3d/sol-logo.blend`, collection `SOL_LOGO` | The logo mark: the same body with no arms or legs. Saved at Elaine's request the same day. |

The frozen copies are in `../assets/sol-3d/approved-2026-11-25/`. Do not overwrite that folder.
In each `.blend`, the root empty (`RIG_Sol` or `RIG_Sol_logo`) sits on the ground and he is 1.0 tall with legs.
Arms pivot on `RIG_Sol_arm_L` and `RIG_Sol_arm_R`. The legs hang off the root so they stay planted when
the body (`RIG_Sol_body`) leans.

## How he is made (Elaine's method)

1. **Body:** the real outline of `Logo.png` (Sol with no legs) is traced and inflated like a balloon. The
   logo art itself is wrapped on the front, so the layers, colours and eyes are exactly his. The back is
   plain body red.
2. **Legs:** not inflated. Their outline is read off `Mascot.png` row by row and spun into a round limb
   with no reshaping: wide where it joins the body, sides closing in, a blunt rounded tip. They sit exactly
   where the mascot has them. [The check image](sol-3d/sol-legs-check.png) shows the mascot's outline
   drawn over the model's legs.
3. **Arms:** that same leg shape, 1.9 times as long, pointing out and down from his sides.

## Rules that came out of building him

- He is **round**: a plump inflated body, a teardrop from the side and back, like the website's 360
  (`Ignite Website/public/backgrounds/Loading.gif`).
- **Legs are the mascot's own shape.** Narrowed legs and tapered ovals were both rejected as too pointy:
  "not too pointy look at the reference".
- **Arms are the same shape as the legs**, only longer.
- **One simple flame tip**, the one in the art. No curl, twist or swirl.
- Eyes, layers and colours come from the art on his front. Do not redraw them.
- No brown streak along his sides: near the outline, colour comes only from clean interior red.

## Using him

- **Skeleton clips:** append the `SOL` collection instead of building a gray stand-in. Whether a coloured
  Sol in an otherwise gray skeleton is what Elaine wants is still her call; ask before the first clip.
- **Paint passes:** pass `sol-3d/sol-turnaround.png` as an image reference alongside `Mascot.png`.
- **Rebuilding:** see `../assets/sol-3d/README.md`. `compare.py` checks the result against `Mascot.png`.

[Sol beside Mascot.png](sol-3d/sol-vs-mascot.png)
