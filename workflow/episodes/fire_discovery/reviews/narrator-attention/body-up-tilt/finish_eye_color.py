"""Use the authorized eye-only cleanup to normalize navy in new pose stills.

No eye translation, rotation or shape transform; no body/environment edits.
"""
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
EPISODE = HERE.parents[2]
sys.path.insert(0, str(HERE.parent/'eye-correction'))
from cleanup_eyes import NAVY, sha, matte, background, expand, eye_region


def main():
    receipt = {
        'scope': 'Eye-color-only finish of generated body-tilt candidates.',
        'authorization': 'Existing explicit permission: oh oops yeah sorry u can do that',
        'eye_color_rgb': [28, 36, 71], 'eye_geometry_transformed': False,
        'body_or_environment_edited': False, 'canonical_frames_changed': False,
        'scenes': [],
    }
    for scene in ('02', '05'):
        source = EPISODE/'keyframes'/f'{scene}-last-body-up-tilt-nano-v1.png'
        output = EPISODE/'keyframes'/f'{scene}-last-body-up-tilt-eye-finish-v1.png'
        assert not output.exists(), output
        original = np.asarray(Image.open(source).convert('RGB'))
        result = original.copy()
        allowed = np.zeros(original.shape[:2], dtype=bool)
        eyes = []
        for xa, xb in ((450, 610), (610, 750)):
            region = original[1320:1570, xa:xb]
            seed = ((region[:, :, 0] < 100) & (region[:, :, 1] < 110)
                    & (region[:, :, 2] > region[:, :, 0]*1.15)
                    & (region[:, :, 2] > region[:, :, 1]*1.10))
            ys, xs = np.nonzero(seed)
            assert len(xs) > 1500
            x0, x1 = int(xs.min()+xa-24), int(xs.max()+xa+25)
            y0, y1 = int(ys.min()+1320-24), int(ys.max()+1320+25)
            crop = original[y0:y1, x0:x1].astype(float)
            alpha = matte(crop)
            cream = background(crop, expand(eye_region(crop), 7))
            replacement = np.clip(np.rint(cream*(1-alpha[:, :, None])
                                         + NAVY*alpha[:, :, None]), 0, 255).astype('uint8')
            support = alpha > 0
            result[y0:y1, x0:x1][support] = replacement[support]
            allowed[y0:y1, x0:x1] |= support
            assert np.all(result[y0:y1, x0:x1][alpha == 1] == NAVY)
            eyes.append({'bounds': [x0, y0, x1, y1],
                         'opaque_navy_pixels': int((alpha == 1).sum())})
        changes = np.any(result != original, axis=2)
        assert not changes[~allowed].any()
        Image.fromarray(result).save(output)
        Image.fromarray(allowed.astype('uint8')*255).save(HERE/f'{scene}-color-only-mask-v1.png')
        receipt['scenes'].append({'scene': scene, 'source': str(source.relative_to(EPISODE)),
            'source_sha256': sha(source), 'output': str(output.relative_to(EPISODE)),
            'output_sha256': sha(output), 'eyes': eyes,
            'changed_pixels': int(changes.sum()), 'changed_pixels_outside_eye_shapes': 0,
            'all_opaque_eye_pixels_exact_navy': True, 'user_approved': False})
    (HERE/'eye-color-finish-v1.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
