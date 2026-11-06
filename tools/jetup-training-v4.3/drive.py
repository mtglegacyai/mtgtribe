# Drive the v4.2 training engine for single frames or frame ranges, without the cover screenshot (never patched).
# Usage (from train/run, with FACE set):
#   python3 ../drive.py still t1 t2 ...          -> qa3/f_<t>.png
#   python3 ../drive.py range a b out.mp4        -> frames a..b-1 as a lossless clip
#   python3 ../drive.py times                    -> the photo scene times as JSON
# CIRCLE=1 swaps the engine's rounded-square photo card for MTG's gold-ringed circle (MTG, 6 Nov 2026).
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.argv_saved = sys.argv; sys.argv = ['render_tut2.py', 'none']
sys.path.insert(0, '/home/claude/jv')
import render_tut2 as T2
sys.argv = sys.argv_saved
W, H, FPS = T2.W, T2.H, T2.FPS

if os.environ.get('CIRCLE'):
    PHOTO = os.environ['PHOTO']
    GOLD_L, GOLD_D = (250, 228, 150), (196, 142, 44)
    _src = Image.open(PHOTO).convert('RGB'); _cache = {}
    def circle_card(size):
        """Same footprint as the old card (size, ring, pad), but a circle: gold gradient ring, soft gold glow."""
        if size in _cache: return _cache[size].copy()
        ring = max(4, size // 55); pad = max(14, size // 9)
        S = size + 2 * ring + 2 * pad
        out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        g = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([pad - 4, pad - 4, S - pad + 3, S - pad + 3], fill=(232, 194, 90, 170))
        out.alpha_composite(g.filter(ImageFilter.GaussianBlur(pad * 0.55)))
        K = 3; SS = S * K
        m = Image.new('L', (SS, SS), 0); ImageDraw.Draw(m).ellipse([pad * K, pad * K, SS - pad * K - 1, SS - pad * K - 1], fill=255)
        m = m.resize((S, S), Image.LANCZOS)
        grad = np.zeros((S, S, 4), np.uint8); t = np.linspace(0, 1, S)[:, None] * 0.6 + np.linspace(0, 1, S)[None, :] * 0.4
        for i in range(3): grad[..., i] = (GOLD_L[i] * (1 - t) + GOLD_D[i] * t).astype(np.uint8)
        grad[..., 3] = np.array(m); out.alpha_composite(Image.fromarray(grad))
        D = size * K
        ph = _src.resize((D, D), Image.LANCZOS).convert('RGBA')
        pm = Image.new('L', (D, D), 0); ImageDraw.Draw(pm).ellipse([0, 0, D - 1, D - 1], fill=255); ph.putalpha(pm)
        ph = ph.resize((size, size), Image.LANCZOS)
        out.alpha_composite(ph, (pad + ring, pad + ring))
        _cache[size] = out
        return out.copy()
    T2.photo_card = circle_card
    T2.R.card_img.__globals__['photo_card'] = circle_card   # the intro card closure looks the name up in render_tut2's globals

# the cover (t < 1 s) is never re-drawn; COVER_PNG gives the real first frame so the cover-to-intro fade matches
COVER = np.asarray(Image.open(os.environ['COVER_PNG']).convert('RGB'), np.float32) if os.environ.get('COVER_PNG') else np.zeros((H, W, 3), np.float32)
def frame(t): return np.clip(T2.frame(t, COVER), 0, 255).astype(np.uint8)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'still':
        os.makedirs('qa3', exist_ok=True)
        for ts in sys.argv[2:]:
            t = round(float(ts) * FPS) / FPS
            Image.fromarray(frame(t)).save(f'qa3/f_{float(ts):07.2f}.png')
    elif cmd == 'range':
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '0', '-pix_fmt', 'yuv444p', out], stdin=subprocess.PIPE)
        for fi in range(a, b): ff.stdin.write(frame(fi / FPS).tobytes())
        ff.stdin.close(); ff.wait(); print('done', out, a, b)
    elif cmd == 'frames':
        fl, out = [int(x) for x in open(sys.argv[2]).read().split()], sys.argv[3]
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264rgb', '-preset', 'ultrafast', '-crf', '0', out], stdin=subprocess.PIPE)
        for fi in fl: ff.stdin.write(frame(fi / FPS).tobytes())
        ff.stdin.close(); ff.wait(); print('done', out, len(fl))
    elif cmd == 'times':
        mtg = [i for i, s in enumerate(T2.STATES) if s['kind'] == 'mtg']
        print(json.dumps(dict(mtg_states=[(i, T2.TIMES[i], T2.TIMES[i + 1]) for i in mtg], T_RECAP=T2.T_RECAP, T_SLOG=T2.T_SLOG, T_OUT=T2.T_OUT,
                              TWISH=T2.TWISH, TSIG=T2.TSIG, END_CARD=T2.END_CARD, TOTAL=T2.TOTAL, FPS=FPS)))
