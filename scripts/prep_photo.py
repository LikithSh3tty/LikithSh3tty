"""Photo -> isolated, tonally-normalised grayscale PNG on black.

Run once per photo; needs requirements-art.txt.

    python -m scripts.prep_photo [source.png] [x y w h]

Passing an explicit crop box overrides face detection (needed for profile shots
and anything Haar cannot find a frontal face in).

Two things drive the design:

1. The art is light glyphs on a dark panel, so ink reads as brightness. The ramp
   maps bright -> dense, which means the background must be BLACK to fall off the
   blank end of it.
2. Photos are not reliably exposed. A night shot's subject can sit entirely in the
   bottom third of the range and render as nothing at all. So the subject's own
   tonal range is normalised to span the ramp, with a floor that keeps even its
   darkest parts faintly inked and separable from the background.
"""
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

SRC = sys.argv[1] if len(sys.argv) > 1 else "source-photo.png"
OUT = "source-prepped.png"

FLOOR = 58   # darkest glyph level the subject is allowed to reach (0 = invisible)
GAMMA = 0.85 # <1 lifts mid-tones so faces do not clump at one ramp position

# 1. Cut the subject out of the background.
cut = remove(Image.open(SRC).convert("RGBA"))
alpha = np.array(cut)[:, :, 3]

# 2. Composite onto black (see module docstring).
black = Image.new("RGBA", cut.size, (0, 0, 0, 255))
flat = Image.alpha_composite(black, cut).convert("RGB")
gray = cv2.cvtColor(np.array(flat), cv2.COLOR_RGB2GRAY)

# 3. Crop to the head, by face detection or an explicit box.
if len(sys.argv) >= 6:
    x, y, w, h = (int(v) for v in sys.argv[2:6])
else:
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    if len(faces) == 0:
        raise SystemExit(
            "No face detected. Re-run with an explicit crop box:\n"
            "  python -m scripts.prep_photo <src> <x> <y> <w> <h>"
        )
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])

x0 = max(0, int(x - 0.92 * w))
x1 = min(gray.shape[1], int(x + w + 0.92 * w))
y0 = max(0, int(y - 0.70 * h))
y1 = min(gray.shape[0], int(y + h + 1.15 * h))
crop, crop_a = gray[y0:y1, x0:x1], alpha[y0:y1, x0:x1]

# 4. CLAHE for local contrast, so a flatly-lit face gains highlights and shadows.
crop = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(crop)

# 5. Trim to the subject. Empty margin converts to blank glyphs and leaves the
# portrait floating in dead space inside its panel.
ys, xs = np.where(crop_a > 12)
if len(xs):
    m = 4
    tx0, tx1 = max(0, xs.min() - m), min(crop.shape[1], xs.max() + 1 + m)
    ty0, ty1 = max(0, ys.min() - m), min(crop.shape[0], ys.max() + 1 + m)
    crop, crop_a = crop[ty0:ty1, tx0:tx1], crop_a[ty0:ty1, tx0:tx1]

# 6. Pad to square so the aspect-aware grid has a balanced frame to fill.
side = max(crop.shape)
sq = np.zeros((side, side), np.uint8)
sq_a = np.zeros((side, side), np.uint8)
oy, ox = (side - crop.shape[0]) // 2, (side - crop.shape[1]) // 2
sq[oy:oy + crop.shape[0], ox:ox + crop.shape[1]] = crop
sq_a[oy:oy + crop.shape[0], ox:ox + crop.shape[1]] = crop_a

# 7. Normalise the SUBJECT's own range to [FLOOR, 255]; force background to 0.
# Percentiles rather than min/max so a single specular highlight cannot squash
# everything else into the bottom of the range.
subject = sq_a > 12
if subject.any():
    vals = sq[subject].astype(np.float32)
    lo, hi = np.percentile(vals, 2), np.percentile(vals, 98)
    scaled = (sq.astype(np.float32) - lo) / max(1.0, hi - lo)
    scaled = np.clip(scaled, 0.0, 1.0)
    scaled = np.power(scaled, GAMMA)
    sq = np.where(subject, FLOOR + scaled * (255 - FLOOR), 0).astype(np.uint8)

Image.fromarray(sq).save(OUT)
ink = subject.mean() * 100
print(f"wrote {OUT}  {sq.shape[1]}x{sq.shape[0]}  subject={ink:.0f}% of frame  "
      f"(crop box {x},{y},{w},{h})")
