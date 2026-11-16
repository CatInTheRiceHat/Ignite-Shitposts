"""Elaine-authorized, non-generative cleanup of two Fire episode endpoints.

Copy actual source eye mattes without scaling/rotation, translate upward 20px,
restore opaque original navy, and heal only the old eye footprints. Never
overwrite a source, canonical endpoint, or existing versioned output.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


HERE = Path(__file__).resolve().parent
EPISODE = HERE.parents[2]
NAVY = np.array([28, 36, 71], dtype=np.float64)
EYE_BOXES = ((480, 1395, 605, 1545), (610, 1380, 735, 1530))
VERSION = 'v2'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expand(mask, radius):
    return np.asarray(Image.fromarray(mask.astype('uint8') * 255).filter(
        ImageFilter.MaxFilter(radius * 2 + 1))) > 0


def shrink(mask):
    return np.asarray(Image.fromarray(mask.astype('uint8') * 255).filter(
        ImageFilter.MinFilter(3))) > 0


def eye_region(rgb):
    seed = ((rgb[:, :, 0] < 110) & (rgb[:, :, 1] < 110)
            & (rgb[:, :, 2] < 145)
            & (rgb[:, :, 2] > rgb[:, :, 0] * 1.15))
    ys, xs = np.nonzero(seed)
    assert len(xs) > 1500
    window = np.zeros(seed.shape, dtype=bool)
    window[ys.min()-8:ys.max()+9, xs.min()-8:xs.max()+9] = True
    # Include the brown/dark perimeter inherited from the generated source;
    # a blue-only mask leaves that perimeter behind as a ghost eye.
    return (rgb.mean(axis=2) < 170) & window


def background(rgb, mask):
    """Harmonic cream repair bounded by the existing painted perimeter."""
    result = rgb.astype(np.float64).copy()
    for y in np.flatnonzero(mask.any(axis=1)):
        xs = np.flatnonzero(mask[y])
        lo, hi = int(xs[0]), int(xs[-1])
        assert lo >= 6 and hi + 6 < rgb.shape[1]
        left = np.median(rgb[y, lo-5:lo], axis=0)
        right = np.median(rgb[y, hi+1:hi+6], axis=0)
        t = ((xs - lo + 1) / (hi - lo + 2))[:, None]
        result[y, xs] = left * (1-t) + right * t
    for _ in range(650):
        average = (np.roll(result, 1, 0) + np.roll(result, -1, 0)
                   + np.roll(result, 1, 1) + np.roll(result, -1, 1)) / 4
        result[mask] = average[mask]
    return result


def matte(rgb):
    """Recover the existing perimeter/antialiasing; never fit a new ellipse."""
    core = eye_region(rgb)
    assert 1500 < core.sum() < 5000
    support = expand(core, 2)
    bg = background(rgb, expand(core, 7))
    dark = np.median(rgb[shrink(core)], axis=0)
    direction = bg - dark
    alpha = np.clip(((bg-rgb) * direction).sum(axis=2)
                    / np.maximum((direction**2).sum(axis=2), 1), 0, 1)
    alpha[~support] = 0
    alpha[alpha < .10] = 0
    alpha[(alpha > .90) | shrink(core)] = 1
    return alpha


def main():
    proposal = json.loads((HERE/'local-cleanup-proposal.json').read_text())
    receipt = {
        'method': 'Authorized local eye-only cleanup; no image/video generation.',
        'user_authorization': 'oh oops yeah sorry u can do that',
        'scope': 'The eye-only operation proposed immediately before that reply.',
        'eye_color_rgb': NAVY.astype(int).tolist(),
        'gaze_translation_px': [0, -20], 'user_approved_frames': False,
        'scenes': [],
    }
    for scene in proposal['scenes']:
        base_path = EPISODE/scene['base']
        source_path = EPISODE/scene['contour_source']
        output_path = EPISODE/scene['proposed_output'].replace('v1.png', VERSION+'.png')
        assert sha(base_path) == scene['base_sha256']
        assert sha(source_path) == scene['contour_source_sha256']
        assert not output_path.exists(), output_path
        base_image = Image.open(base_path).convert('RGB')
        source_image = Image.open(source_path).convert('RGB')
        assert base_image.size == source_image.size == (1536, 2752)
        original = np.asarray(base_image)
        source = np.asarray(source_image)
        result = original.copy()
        allowed = np.zeros(original.shape[:2], dtype=bool)
        eye_proofs = []
        for index, (x0, y0, x1, y1) in enumerate(EYE_BOXES):
            source_crop = source[y0:y1, x0:x1].astype(np.float64)
            alpha = matte(source_crop)
            old_crop = original[y0:y1, x0:x1]
            old_mask = expand(eye_region(old_crop), 7)
            healed = background(old_crop, old_mask)
            # Borrow only local high-frequency cream texture, not facial art.
            clean_texture = original[y0:y1, x0-70:x1-70]
            blur = np.asarray(Image.fromarray(clean_texture).filter(
                ImageFilter.BoxBlur(2))).astype(float)
            residual = np.clip(clean_texture.astype(float)-blur, -2, 2)
            repaired = np.clip(np.rint(healed + residual), 0, 255).astype('uint8')
            view = result[y0:y1, x0:x1]
            view[old_mask] = repaired[old_mask]
            allowed[y0:y1, x0:x1] |= old_mask

            target_y0, target_y1 = y0-20, y1-20
            target = result[target_y0:target_y1, x0:x1]
            support = alpha > 0
            composite = np.clip(np.rint(target*(1-alpha[:, :, None])
                                        + NAVY*alpha[:, :, None]), 0, 255).astype('uint8')
            target[support] = composite[support]
            allowed[target_y0:target_y1, x0:x1] |= support
            assert np.all(target[alpha == 1] == NAVY), 'Non-navy eye core'
            ys, xs = np.nonzero(alpha >= .5)
            eye_proofs.append({
                'eye': index+1,
                'source_box': [x0, y0, x1, y1],
                'target_box': [x0, target_y0, x1, target_y1],
                'contour_transform': 'integer translation only; no scale/rotation/reshape',
                'contour_wh_px': [int(xs.max()-xs.min()+1), int(ys.max()-ys.min()+1)],
                'source_center_xy': [float(xs.mean()+x0), float(ys.mean()+y0)],
                'target_center_xy': [float(xs.mean()+x0), float(ys.mean()+y0-20)],
                'opaque_navy_pixels': int((alpha == 1).sum()),
                'alpha_sha256': hashlib.sha256(alpha.tobytes()).hexdigest(),
            })
            Image.fromarray(np.rint(alpha*255).astype('uint8')).save(
                HERE/f"{scene['scene']}-eye-{index+1}-source-matte-{VERSION}.png")
        changed = np.any(result != original, axis=2)
        assert not changed[~allowed].any(), 'Artwork changed outside eye masks'
        assert sha(base_path) == scene['base_sha256']
        assert sha(source_path) == scene['contour_source_sha256']
        Image.fromarray(result).save(output_path)
        assert np.array_equal(np.asarray(Image.open(output_path)), result)
        Image.fromarray(allowed.astype('uint8')*255).save(
            HERE/f"{scene['scene']}-allowed-edit-mask-{VERSION}.png")
        receipt['scenes'].append({**scene,
            'proposed_output': str(output_path.relative_to(EPISODE)),
            'output_sha256': sha(output_path),
            'dimensions': list(base_image.size), 'eyes': eye_proofs,
            'changed_pixels': int(changed.sum()),
            'allowed_pixels': int(allowed.sum()), 'changed_pixels_outside_eye_masks': 0,
            'all_opaque_eye_pixels_exact_navy': True, 'user_approved': False})
    (HERE/f'local-cleanup-receipt-{VERSION}.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
