# Apply the same skin correction (photo -> 5 Checks video tone, version D) to any image that contains the profile photo.
import sys, numpy as np, cv2, mediapipe as mp
from PIL import Image, ImageFilter, ImageDraw
from mediapipe.tasks.python import vision, BaseOptions
DL = np.array([46.1 - 62.7, 0.85 * (14.9 - 33.8), 0.85 * (17.6 - 37.9)], np.float32)   # measured shift, version D
src, dst = sys.argv[1], sys.argv[2]
box = tuple(int(v) for v in sys.argv[3].split(',')) if len(sys.argv) > 3 else None
im = Image.open(src).convert('RGB'); full = np.array(im)
x0, y0, x1, y1 = box or (0, 0, im.width, im.height)
P = np.ascontiguousarray(full[y0:y1, x0:x1])
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=BaseOptions(model_asset_path='selfie_multiclass.tflite'), output_confidence_masks=True))
cm = np.stack([np.squeeze(c.numpy_view()) for c in seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=P)).confidence_masks]).astype(np.float32)
m = np.clip(cm[2] + cm[3], 0, 1) * (1 - np.clip(cm[5] * 1.5, 0, 1))
try:
    fl = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path='../v5/face_landmarker.task'), num_faces=1))
    lm = fl.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=P)).face_landmarks[0]
    h, w = P.shape[:2]; em = Image.new('L', (w, h), 0); de = ImageDraw.Draw(em)
    for idx in ([33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246], [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398]):
        de.polygon([(lm[i].x * w, lm[i].y * h) for i in idx], fill=255)
    em = np.array(em.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32) / 255; m *= (1 - em)
except Exception as e:
    print('no eye landmarks (small face), skin mask only:', e)
m = np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(1, P.shape[0] // 400)))).astype(np.float32) / 255
L = cv2.cvtColor(P.astype(np.float32) / 255, cv2.COLOR_RGB2LAB)
out = np.clip(cv2.cvtColor(L + DL[None, None, :] * m[..., None], cv2.COLOR_LAB2RGB) * 255, 0, 255).astype(np.uint8)
full[y0:y1, x0:x1] = out
Image.fromarray(full).save(dst, quality=90)
print('skin pixels changed: %.1f%% of the box' % (100 * np.mean(m > 0.5)))
