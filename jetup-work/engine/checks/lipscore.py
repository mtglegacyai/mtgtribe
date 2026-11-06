# Lip-sync score from real lip aperture: lag vs voice loudness, closure on m/b/p, closure in pauses.
import sys, json, subprocess, numpy as np
ap = np.load(sys.argv[1]); wav = sys.argv[2]; fps = 25.0; n = len(ap)
a = np.frombuffer(subprocess.check_output(['ffmpeg', '-v', 'error', '-i', wav, '-ac', '1', '-ar', '16000', '-f', 's16le', '-']), np.int16).astype(np.float32)
hop = int(16000 / fps)
env = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9) if i * hop < len(a) else 0 for i in range(n)])
le = np.log(env + 1)
x = (ap - np.nanmean(ap)) / np.nanstd(ap); y = (le - le.mean()) / le.std()
cs = {k: float(np.nanmean(x[max(0, k):n + min(0, k)] * y[max(0, -k):n + min(0, -k)])) for k in range(-6, 7)}
lag = max(cs, key=cs.get)
bil = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else []
bf = [int(round((b[2] + b[3]) / 2 * fps)) for b in bil]
co = {k: round(float(np.nanmean([ap[min(n - 1, max(0, f + k))] for f in bf])), 3) for k in range(-3, 4)} if bf else {}
silent = env < env.max() * 0.02
print(json.dumps(dict(file=sys.argv[1], lag_frames=lag, lag_ms=int(lag * 40), corr_best=round(cs[lag], 3), corr_0=round(cs[0], 3),
      curve={k: round(v, 2) for k, v in cs.items()}, aperture_speech=round(float(np.nanmean(ap[~silent])), 3),
      aperture_pause=round(float(np.nanmean(ap[silent])), 3), bilabial_by_offset=co,
      bilabial_closed_pct=round(100 * float(np.mean([ap[min(n - 1, f)] < 0.04 for f in bf])), 0) if bf else None)))
