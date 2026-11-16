"""User-requested preview: compress the up-gaze eyes vertically to 80%.

Separate candidates only. Retain the eye-cleanup v2 endpoints/canonical slots.
"""
import json

import numpy as np
from PIL import Image, ImageFilter

from cleanup_eyes import HERE, EPISODE, EYE_BOXES, NAVY, sha, matte, eye_region, expand, background


def main():
    source_receipt = json.loads((HERE/'local-cleanup-receipt-v2.json').read_text())
    receipt = {
        'user_request': 'do u wanna try changing the eyes so they squish vertically as if sol is loooking up',
        'status': 'preview_only_not_approved',
        'vertical_scale': .8, 'horizontal_scale': 1,
        'gaze_translation_px': [0, -20], 'eye_color_rgb': [28, 36, 71],
        'canonical_frames_changed': False, 'new_generation_jobs': 0, 'scenes': [],
    }
    for scene in source_receipt['scenes']:
        base_path, contour_path = EPISODE/scene['base'], EPISODE/scene['contour_source']
        locked_path = EPISODE/scene['proposed_output']
        output_path = EPISODE/'keyframes'/f"{scene['scene']}-last-upward-squish-v1.png"
        assert not output_path.exists(), output_path
        assert sha(base_path) == scene['base_sha256']
        assert sha(contour_path) == scene['contour_source_sha256']
        assert sha(locked_path) == scene['output_sha256']
        original = np.asarray(Image.open(base_path).convert('RGB'))
        contour = np.asarray(Image.open(contour_path).convert('RGB'))
        locked = np.asarray(Image.open(locked_path).convert('RGB'))
        result = original.copy()
        allowed = np.zeros(original.shape[:2], dtype=bool)
        difference_allowed = allowed.copy()
        eyes = []
        for x0, y0, x1, y1 in EYE_BOXES:
            original_alpha = matte(contour[y0:y1, x0:x1].astype(float))
            y_grid = np.arange(original_alpha.shape[0])[:, None]
            cy = float((original_alpha*y_grid).sum()/original_alpha.sum())
            image = Image.fromarray(original_alpha.astype('float32'))
            alpha = np.asarray(image.transform(image.size, Image.Transform.AFFINE,
                (1, 0, 0, 0, 1/.8, cy-cy/.8), resample=Image.Resampling.BICUBIC)).copy()
            alpha = np.clip(alpha, 0, 1)
            alpha[alpha < .10] = 0
            alpha[alpha > .98] = 1
            old_crop = original[y0:y1, x0:x1]
            old_mask = expand(eye_region(old_crop), 7)
            repaired = background(old_crop, old_mask)
            texture = original[y0:y1, x0-70:x1-70]
            blur = np.asarray(Image.fromarray(texture).filter(ImageFilter.BoxBlur(2))).astype(float)
            repaired += np.clip(texture.astype(float)-blur, -2, 2)
            patch = result[y0:y1, x0:x1]
            patch[old_mask] = np.clip(np.rint(repaired), 0, 255).astype('uint8')[old_mask]
            allowed[y0:y1, x0:x1] |= old_mask
            target = result[y0-20:y1-20, x0:x1]
            support = alpha > 0
            composite = np.clip(np.rint(target*(1-alpha[:, :, None])
                + NAVY*alpha[:, :, None]), 0, 255).astype('uint8')
            target[support] = composite[support]
            allowed[y0-20:y1-20, x0:x1] |= support
            difference_allowed[y0-20:y1-20, x0:x1] |= support | (original_alpha > 0)
            assert np.all(target[alpha == 1] == NAVY)
            bounds = lambda a: (np.argwhere(a >= .5).max(0)-np.argwhere(a >= .5).min(0)+1)[::-1].tolist()
            eyes.append({'original_wh_px': bounds(original_alpha),
                         'squished_wh_px': bounds(alpha),
                         'opaque_navy_pixels': int((alpha == 1).sum())})
        changed = np.any(result != original, axis=2)
        versus_locked = np.any(result != locked, axis=2)
        assert not changed[~allowed].any()
        assert not versus_locked[~difference_allowed].any(), 'Changed outside the existing eye shapes'
        Image.fromarray(result).save(output_path)
        receipt['scenes'].append({'scene': scene['scene'],
            'output': str(output_path.relative_to(EPISODE)), 'sha256': sha(output_path),
            'compare_with': str(locked_path.relative_to(EPISODE)),
            'compare_with_sha256': sha(locked_path),
            'eyes': eyes, 'changed_pixels_vs_eye_lock': int(versus_locked.sum()),
            'changed_pixels_outside_eye_shapes': 0, 'user_approved': False})
    (HERE/'upward-squish-trial-v1.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
