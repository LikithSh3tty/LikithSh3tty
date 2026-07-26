"""Photo -> isolated, contrast-boosted, head-cropped grayscale PNG.

Run once per photo; needs requirements-art.txt. A flatly-lit face converts to a dark,
unreadable blob, so this removes the background, crops to head and collar, boosts
local contrast, and trims the empty margin before the ASCII step ever sees it.

    python -m scripts.prep_photo [source.png] [x y w h]

Passing an explicit crop box overrides face detection.
"""
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

SRC = sys.argv[1] if len(sys.argv) > 1 else "source-photo.png"
OUT = "source-prepped.png"

# 1. Cut the subject out of the background.
cut = remove(Image.open(SRC).convert("RGBA"))
alpha = np.array(cut)[:, :, 3]  # exact subject mask, independent of tonal edits

# 2. Composite onto pure white so the background maps to the blank end of the ramp.
white = Image.new("RGBA", cut.size, (255, 255, 255, 255))
flat = Image.alpha_composite(white, cut).convert("RGB")
arr = cv2.cvtColor(np.array(flat), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)

# 3. Find the face and crop to head + collar.
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
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])  # largest face

x0 = max(0, int(x - 0.92 * w))
x1 = min(arr.shape[1], int(x + w + 0.92 * w))
y0 = max(0, int(y - 0.70 * h))
y1 = min(arr.shape[0], int(y + h + 1.15 * h))
crop = gray[y0:y1, x0:x1]
crop_alpha = alpha[y0:y1, x0:x1]

# 4. CLAHE gives a flatly-lit face real highlights and shadows.
crop = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(crop)

# 5. Trim to the subject, then re-centre in a square.
# Empty margin is not free: it converts to blank glyphs and leaves the portrait
# floating in dead space inside its panel. The alpha mask locates the subject
# exactly, so trimming to it makes the art fill the frame.
ys, xs = np.where(crop_alpha > 12)
if len(xs):
    margin = 4
    tx0, tx1 = max(0, xs.min() - margin), min(crop.shape[1], xs.max() + 1 + margin)
    ty0, ty1 = max(0, ys.min() - margin), min(crop.shape[0], ys.max() + 1 + margin)
    crop = crop[ty0:ty1, tx0:tx1]

side = max(crop.shape)
square = np.full((side, side), 255, np.uint8)
oy, ox = (side - crop.shape[0]) // 2, (side - crop.shape[1]) // 2
square[oy:oy + crop.shape[0], ox:ox + crop.shape[1]] = crop
crop = square

# 6. Lift the mid-tones. Skin sits mid-gray, which lands on the ramp's dense
# glyphs and turns the face into a solid blob; gamma < 1 moves it onto sparser
# glyphs so only hair, shadows and clothing stay dark. 0.75 was chosen by
# comparing 1.0 / 0.75 / 0.55 — lower than this washes the features out.
GAMMA = 0.75
crop = np.power(crop.astype(np.float32) / 255.0, GAMMA) * 255.0

# 7. Stretch the contrast. Gamma alone leaves the whole face sitting in a narrow
# tonal band, so it converts to one near-uniform block of glyphs and reads as a
# filled silhouette. Expanding [LO, HI] to the full range is what separates eye
# sockets, brows and mouth from cheeks. Chosen by rendering the candidates side
# by side; without the stretch only ~195 cells land on dense glyphs, with it 377.
LO, HI = 40, 215
crop = np.clip((crop - LO) * 255.0 / (HI - LO), 0, 255).astype(np.uint8)

Image.fromarray(crop).save(OUT)
print(f"wrote {OUT}  {crop.shape[1]}x{crop.shape[0]}  (face at {x},{y},{w},{h})")
