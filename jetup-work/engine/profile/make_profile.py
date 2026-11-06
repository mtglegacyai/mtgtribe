# MTG profile picture from an approved avatar frame: head-and-shoulders crop, gold ring, optional mtgtribe.com print on the t-shirt.
import sys, json, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OSW = '/home/claude/assets/fonts/Oswald.ttf'
GOLD, GOLD_L, GOLD_D = (232, 194, 90), (250, 228, 150), (196, 142, 44)
UP = 2                                   # work at 2x so the print stays crisp

def crop_up(frame_path, cx, top=105, size=500):
    im = cv2.imread(frame_path); x0 = int(cx - size / 2)
    c = im[top:top + size, x0:x0 + size]
    up = cv2.resize(c, (size * UP, size * UP), interpolation=cv2.INTER_LANCZOS4)
    bl = cv2.GaussianBlur(up, (0, 0), 1.6); up = cv2.addWeighted(up, 1.45, bl, -0.45, 0)      # gentle sharpen
    return up, x0, top

def brand(up, x0, top, text='mtgtribe.com', y_top=522, fill_ratio=0.9):
    """print the URL on the white t-shirt between the lapels, shaded by the fabric"""
    hsv = cv2.cvtColor(up, cv2.COLOR_BGR2HSV); white = (hsv[..., 2] > 185) & (hsv[..., 1] < 45)
    yt = (y_top - top) * UP
    xs = np.where(white[yt + 6, :])[0]
    runs, s, p = [], xs[0], xs[0]
    for x in xs[1:]:
        if x != p + 1: runs.append((s, p)); s = x
        p = x
    runs.append((s, p)); a, b = max(runs, key=lambda r: r[1] - r[0])
    width = (b - a) * fill_ratio
    f = ImageFont.truetype(OSW, 40); f.set_variation_by_name('Bold')
    size = 40 * width / f.getlength(text); f = ImageFont.truetype(OSW, int(size)); f.set_variation_by_name('Bold')
    H, W = up.shape[:2]; lay = Image.new('L', (W, H), 0); d = ImageDraw.Draw(lay)
    bb = d.textbbox((0, 0), text, font=f); tw = bb[2] - bb[0]
    d.text(((a + b) / 2 - tw / 2 - bb[0], yt - bb[1]), text, font=f, fill=255)
    alpha = np.array(lay.filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255 * 0.94
    m = cv2.dilate(white.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(np.float32); alpha *= m
    lum = cv2.cvtColor(up, cv2.COLOR_BGR2GRAY).astype(np.float32)
    shade = np.clip(lum / np.median(lum[white]), 0.72, 1.06)[..., None]
    ink = np.array([38, 26, 22], np.float32) * shade            # BGR near-black navy, carries the fabric folds
    out = up.astype(np.float32) * (1 - alpha[..., None]) + ink * alpha[..., None]
    return np.clip(out, 0, 255).astype(np.uint8), dict(size_frame_px=round(size / UP, 1), text_box=(int(a), int(yt), int(tw)))

def badge(up_bgr, D=600, ring=12):
    rgb = Image.fromarray(cv2.cvtColor(up_bgr, cv2.COLOR_BGR2RGB)).resize((D, D), Image.LANCZOS)
    pad = 40; S = D + 2 * pad + 2 * ring; out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    g = Image.new('RGBA', (S, S), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([pad - 6, pad - 6, S - pad + 5, S - pad + 5], fill=GOLD + (200,))
    out.alpha_composite(g.filter(ImageFilter.GaussianBlur(18)))
    rr = Image.new('RGBA', (S, S), (0, 0, 0, 0)); ImageDraw.Draw(rr).ellipse([pad, pad, S - pad - 1, S - pad - 1], fill=(255, 255, 255, 255))
    grad = np.zeros((S, S, 4), np.uint8); t = np.linspace(0, 1, S)[:, None]
    for i in range(3): grad[..., i] = (GOLD_L[i] * (1 - t) + GOLD_D[i] * t).astype(np.uint8)
    grad[..., 3] = np.array(rr.getchannel('A')); out.alpha_composite(Image.fromarray(grad))
    m = Image.new('L', (D, D), 0); ImageDraw.Draw(m).ellipse([0, 0, D - 1, D - 1], fill=255)
    face = rgb.convert('RGBA'); face.putalpha(m); out.alpha_composite(face, (pad + ring, pad + ring))
    return out

if __name__ == '__main__':
    f = sys.argv[1]; cx = float(sys.argv[2]); tag = sys.argv[3]
    up, x0, top = crop_up(f, cx)
    cv2.imwrite(f'{tag}_square_plain.png', up)
    br, info = brand(up, x0, top); cv2.imwrite(f'{tag}_square_branded.png', br)
    badge(up).save(f'{tag}_badge_plain.png'); badge(br).save(f'{tag}_badge_branded.png')
    print(tag, info)

def brand_tee(up, x0, top, print_png='tee_print.png', y_top=503, gap_fill=1.02, opacity=0.95):
    """MTG's mtgTribe.com evolution print on the white t-shirt, scaled so the URL sits fully between the lapels; the blazer covers its edges"""
    pr = cv2.imread(print_png, cv2.IMREAD_UNCHANGED).astype(np.float32)
    hsv = cv2.cvtColor(up, cv2.COLOR_BGR2HSV); white = (hsv[..., 2] > 185) & (hsv[..., 1] < 45)
    yt = (y_top - top) * UP; H, W = up.shape[:2]
    # visible shirt run at the URL row (about 75% down the print)
    def run(y):
        xs = np.where(white[min(H - 1, y), :])[0]; runs, s, p = [], xs[0], xs[0]
        for x in xs[1:]:
            if x != p + 1: runs.append((s, p)); s = x
            p = x
        runs.append((s, p)); return max(runs, key=lambda r: r[1] - r[0])
    a, b = run(yt + 20)
    pw = int((b - a) * gap_fill); ph = int(pw * pr.shape[0] / pr.shape[1])
    a2, b2 = run(int(yt + ph * 0.8)); cxp = ((a + b) / 2 + (a2 + b2) / 2) / 2
    p = cv2.resize(pr, (pw, ph), interpolation=cv2.INTER_AREA)
    lay = np.zeros((H, W, 4), np.float32); px0 = int(cxp - pw / 2)
    lay[yt:yt + ph, px0:px0 + pw] = p[:min(ph, H - yt)]
    alpha = cv2.GaussianBlur(lay[..., 3] / 255.0, (0, 0), 0.6) * opacity
    occl = cv2.dilate(white.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32)
    occl = cv2.GaussianBlur(occl, (0, 0), 0.8); alpha *= occl            # the lapels sit on top of the print
    lum = cv2.cvtColor(up, cv2.COLOR_BGR2GRAY).astype(np.float32)
    shade = np.clip(lum / np.median(lum[white]), 0.72, 1.06)[..., None]
    ink = lay[..., :3] * shade
    out = up.astype(np.float32) * (1 - alpha[..., None]) + ink * alpha[..., None]
    return np.clip(out, 0, 255).astype(np.uint8), dict(print_w_frame=pw / UP, print_h_frame=ph / UP)
