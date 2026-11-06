# Skin correction (version D) for a SMALL face badge: crop the badge, upscale it so the segmenter can see the face,
# build the skin mask there, shrink the mask back and apply the same Lab shift as the main photo.
# Usage: python3 recolor_small.py in out cx,cy,r [scale]
import sys, os, numpy as np, cv2, mediapipe as mp
from PIL import Image, ImageFilter, ImageDraw
from mediapipe.tasks.python import vision, BaseOptions
HERE = os.path.dirname(os.path.abspath(__file__))
DL = np.array([46.1 - 62.7, 0.85 * (14.9 - 33.8), 0.85 * (17.6 - 37.9)], np.float32)   # same shift as the main photo
src, dst = sys.argv[1], sys.argv[2]
cx, cy, r = (float(v) for v in sys.argv[3].split(','))
K = int(sys.argv[4]) if len(sys.argv) > 4 else 8
im = Image.open(src).convert('RGB'); full = np.array(im)
x0, y0, x1, y1 = int(cx - r - 2), int(cy - r - 2), int(np.ceil(cx + r + 2)), int(np.ceil(cy + r + 2))
P = np.ascontiguousarray(full[y0:y1, x0:x1]); h, w = P.shape[:2]
U = np.array(Image.fromarray(P).resize((w * K, h * K), Image.LANCZOS))
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=BaseOptions(model_asset_path=os.path.join(HERE, 'selfie_multiclass.tflite')), output_confidence_masks=True))
cm = np.stack([np.squeeze(c.numpy_view()) for c in seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=U)).confidence_masks]).astype(np.float32)
mu = np.clip(cm[2] + cm[3], 0, 1) * (1 - np.clip(cm[5] * 1.5, 0, 1))
# only inside the photo circle (never the gold ring or the background)
cm_ = Image.new('L', (w * K, h * K), 0); ImageDraw.Draw(cm_).ellipse(((cx - x0 - r) * K, (cy - y0 - r) * K, (cx - x0 + r) * K, (cy - y0 + r) * K), fill=255)
mu *= np.array(cm_).astype(np.float32) / 255
m = np.array(Image.fromarray((mu * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
L = cv2.cvtColor(P.astype(np.float32) / 255, cv2.COLOR_RGB2LAB)
out = np.clip(cv2.cvtColor(L + DL[None, None, :] * m[..., None], cv2.COLOR_LAB2RGB) * 255, 0, 255).astype(np.uint8)
full[y0:y1, x0:x1] = out
Image.fromarray(full).save(dst, quality=92)
print('%s: skin pixels changed %.0f%% of the badge box' % (os.path.basename(dst), 100 * np.mean(m > 0.5)))
