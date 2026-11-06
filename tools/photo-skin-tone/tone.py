# Match MTG's skin tone in the profile photo to his skin in the 5 Checks video (skin only; shirt, watch, sign untouched).
import sys, numpy as np, cv2
from PIL import Image, ImageFilter
def lab(rgb): return cv2.cvtColor(rgb.astype(np.float32) / 255, cv2.COLOR_RGB2LAB)
def rgb(l): return np.clip(cv2.cvtColor(l, cv2.COLOR_LAB2RGB) * 255, 0, 255).astype(np.uint8)
def skin_stats(img, masks, cls=(3,)):
    L = lab(img); m = np.max([masks[c] for c in cls], 0) > 0.85
    px = L[m]; chroma = np.hypot(px[:, 1], px[:, 2])
    keep = (px[:, 0] > np.percentile(px[:, 0], 20)) & (px[:, 0] < np.percentile(px[:, 0], 95)) & (chroma > 8)   # no beard, shine or eye whites
    px = px[keep]
    return np.median(px, 0), np.percentile(px, 75, 0) - np.percentile(px, 25, 0), len(px)
P = np.array(Image.open('../brand/mtg-profile-photo.png').convert('RGB')); PM = np.load('photo_masks.npy')
vids = [(np.array(Image.open(f'{n}.png').convert('RGB')), np.load(f'{m}_masks.npy')) for n, m in (('video_40', 'video'), ('video_120', 'video2'), ('video_250', 'video3'))]
pm, ps, pn = skin_stats(P, PM)
vstats = [skin_stats(i, m) for i, m in vids]
vm = np.median([v[0] for v in vstats], 0); vs = np.median([v[1] for v in vstats], 0)
print(f'photo face skin  L {pm[0]:.1f}  a {pm[1]:.1f}  b {pm[2]:.1f}   (spread L {ps[0]:.1f})')
print(f'video face skin  L {vm[0]:.1f}  a {vm[1]:.1f}  b {vm[2]:.1f}   (spread L {vs[0]:.1f})   per frame L: ' + ', '.join(f'{v[0][0]:.1f}' for v in vstats))
strength = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
warm = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0     # share of the colour (a, b) shift; 1 = exact match
L = lab(P)
# soft skin mask: face skin + body skin, feathered; protect eye whites, teeth and shine (low colour) and the gold watch (class 5)
m = np.clip(PM[2] + PM[3], 0, 1) * (1 - np.clip(PM[5] * 1.5, 0, 1))
# protect the whites of the eyes only (face landmarks); beard hairs and everything else on the skin move with it
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
from PIL import ImageDraw
fl = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path='../v5/face_landmarker.task'), num_faces=1))
lm = fl.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(P))).face_landmarks[0]
H_, W_ = P.shape[:2]; em = Image.new('L', (W_, H_), 0); de = ImageDraw.Draw(em)
for idx in ([33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246], [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398]):
    de.polygon([(lm[i].x * W_, lm[i].y * H_) for i in idx], fill=255)
em = np.array(em.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255
m *= (1 - em)
m = np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255
k = np.ones(3)      # an even shift: keeps the skin's texture and the beard as they are, only deeper
new = L.copy()
for c in range(3): new[..., c] = (vm[c] + (L[..., c] - pm[c]) * k[c]) if c == 0 else (L[..., c] + (vm[c] - pm[c]) * warm)
out = L + (new - L) * (m * strength)[..., None]
res = rgb(out)
Image.fromarray(res).save(f'photo_tone_{strength:.2f}_{warm:.2f}.png')
qm, qs, _ = skin_stats(res, PM)
print(f'corrected photo  L {qm[0]:.1f}  a {qm[1]:.1f}  b {qm[2]:.1f}   (strength {strength}, colour {warm})')
