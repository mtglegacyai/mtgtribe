# m/b/p closure check: at each m, b or p sound the lips must be shut. Scan video offsets to find the best sync.
import sys, json, re, subprocess, numpy as np, mediapipe as mp
from pocketsphinx import Decoder
from mediapipe.tasks.python import vision, BaseOptions
SUB = {'authorised': 'authorized', 'copyx': 'copy x', 'jetup': 'jet up', "jetup's": "jet up's", 'metatrader': 'meta trader', 'mtg': 'm t g', "tag's": 'tags', "markets'": 'markets', 'step-by-step': 'step by step', 'sign-up': 'sign up'}
def toks(w):
    w = re.sub(r"[^a-z'\-]", '', w.lower()).strip("'"); w = SUB.get(w, w); return [p for p in re.split(r'[\s\-]+', w) if p]
def bilabials(audio, words, t0, t1):
    """words: list of (word, start, end) in audio time"""
    pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', audio, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'])
    sents, cur = [], []
    for w in words:
        if not (t0 <= w[1] <= t1): continue
        cur.append(w)
        if w[0][-1] in '.?!,:': sents.append(cur); cur = []
    if cur: sents.append(cur)
    out = []
    for s in sents:
        a = max(0, s[0][1] - 0.1); b = s[-1][2] + 0.1
        seg = pcm[int(a * 16000) * 2:int(b * 16000) * 2]
        d = Decoder(samprate=16000, bestpath=False, loglevel='FATAL')
        try:
            d.set_align_text(' '.join(t for w in s for t in toks(w[0])))
            d.start_utt(); d.process_raw(seg, full_utt=True); d.end_utt()
            d.set_alignment(); d.start_utt(); d.process_raw(seg, full_utt=True); d.end_utt()
            for w in d.get_alignment():
                for p in w:
                    if p.name in ('M', 'B', 'P'): out.append(a + (p.start + p.duration / 2) / 100)
        except Exception as e:
            print('align fail:', repr(e)[:120], ' '.join(w[0] for w in s)[:60], file=sys.stderr)
    return out
def aperture(video, t0, dur, cx, cy, model):
    S = 560; x0, y0 = cx - S // 2, max(0, cy - S // 2)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', str(dur), '-i', video, '-vf', f'crop={S}:{S}:{x0}:{y0}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, S, S, 3)
    lm = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=model), running_mode=vision.RunningMode.VIDEO, num_faces=1))
    ap = []
    for i, f in enumerate(fr):
        r = lm.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(f)), int(i * 40))
        if not r.face_landmarks: ap.append(np.nan); continue
        L = r.face_landmarks[0]; d = lambda a, b: np.hypot(L[a].x - L[b].x, L[a].y - L[b].y)
        ap.append(d(13, 14) / d(234, 454))
    return np.array(ap)
if __name__ == '__main__':
    name, video, audio, words_json, t0, dur, cx, cy, vid_off = sys.argv[1:10]
    t0, dur, cx, cy, vid_off = float(t0), float(dur), int(cx), int(cy), float(vid_off)
    W = json.load(open(words_json))
    bl = bilabials(audio, [tuple(w) for w in W], t0, t0 + dur)
    ap = aperture(video, t0 + vid_off, dur, cx, cy, 'face_landmarker.task')
    thr = np.nanpercentile(ap, 25)
    res = {}
    for k in range(-6, 7):
        v = [ap[int(round((b - t0) * 25)) + k] for b in bl if 0 <= int(round((b - t0) * 25)) + k < len(ap)]
        res[k] = 100 * np.nanmean(np.array(v) < thr)
    best = max(res, key=res.get)
    print(f'{name}: {len(bl)} m/b/p sounds; lips shut on the sound at offset 0: {res[0]:.0f}%; best offset {best:+d} frames ({best * 40:+d} ms) = {res[best]:.0f}%')
    print('   by offset (frames, + = take the video later): ' + ' '.join(f'{k:+d}:{res[k]:.0f}' for k in range(-6, 7)))
