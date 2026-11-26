# Sol with separate eyes

Elaine's idea, 2026-11-26: "do u think u can rigg the eyes like seperately like attach a 3d polygon on top when u
do the blender thing". Built the same day. **Approved by Elaine on 2026-11-26**: after seeing sheet version 3 and the bounce test clip
she said "OH ITS PERFECT." The approved copy is frozen in `approved-2026-11-26/`; do not overwrite that folder.
The original model (`../sol.blend`, frozen in `../approved-2026-11-25/`) is untouched; this is a second file
beside it, and it is the one to use from now on whenever Sol shows an expression, blinks or glances.

![expression sheet](sol-eyes-expressions.png)

| File | What it is |
| --- | --- |
| `sol-eyes.blend` | The approved Sol with the eyes painted out of his front art and rebuilt as separate pieces. Collection `SOL`, same object names as the approved model plus the eye rig, so a skeleton only has to load this file instead. |
| `sol-eyes-expressions.png` | The sheet, version 3 (v2 with only the tip-down shade, bluer and darker). Version 2 showed: normal, blink, two glances, `> <` with round tips, `O O`, sparkles, worried and shocked (each with the purple shade two ways), side views, one mid-bounce. `sol-eyes-expressions-v1.png` is the first sheet. |
| `eyes_rig.py` | `find_eyes()`, `pose_eyes(eyes, expr, blink, look, size, shade, gloom)`, `key_eyes()`. Expressions: `normal`, `squeeze`, `surprised`, `sparkle`, `worried`, `shocked`. |
| `build_sol_eyes.py` | Rebuilds `sol-eyes.blend` from `../sol.blend`. `Blender -b ../sol.blend --python build_sol_eyes.py` |
| `render_expressions.py` | Renders the poses for the sheet. |
| `sol-front-texture-noeyes.png`, `eye-outlines.json`, `eye-metrics.json` | His front art with the eyes painted out; the eye outlines traced from the art; where the eyes sit on the model. |
| `sol-gloom-mask-face.png`, `sol-gloom-mask-top.png`, `gloom.json` | Where the worried shade falls (his face only, or from his flame tip down) and where the side lines hang. |

How it works: his normal eye is the exact outline traced from the art, in the art's navy (27, 36, 71), so the
resting face matches the approved model. Each piece is a thin shape pressed onto the front of his body by a
Shrinkwrap modifier, so it follows the curve of his face wherever it slides, and everything hangs off
`RIG_Sol_body`, so the eyes lean, squash and bounce with him. A piece is hidden by scaling it to nothing.

What it allows: planned expressions keyed per frame, blinks timed by us instead of by the painter, and glances
(the eyes slide a little left, right, up or down). The painter still has the last word on each frame, so every
painted frame is still checked.

Changes she asked for after the first sheet (2026-11-26): "can we make the squeezed shut things like rounded
tips"; "for the anime worried try making a pruple gradient that starts from the top of sol to bottom"; "and then
the dashed lines go on the side like this" (her reference: thin lines hanging at the upper side of the face,
above one eye). All three are in version 2. The purple shade is built two ways, on his face only (A) and from
his flame tip down (B), because "the top of sol" could mean either; she has not picked one. Both of her
references pair the worried look with round white eyes, so `shocked` (worried plus `O O`) was added.

Her picks after version 2 (2026-11-26): "i think i like B but lets make the purple like bluer and darker", and
"everytime u swap emotions make sure theres a bounce that acts as a trnasition between one emotion to the other".
Version 3: the shade runs from his flame tip down by default (`shade="top"`), in a deep indigo blue, on the back
of his body as well. `eyes_rig.py` has `emotion_at(t, timeline)`, which gives the bounce for every swap;
`sol-eyes-emotion-bounce-test.mp4` shows it (`render_demo.py` makes it). Sheets v1 and v2 are kept.

Still to do when the next episode starts: no clip has used it yet; `rig.py`'s `build_sol()` still loads the approved `sol.blend`; the Sol
turnaround sheet given to the painter still shows only the normal eyes.
