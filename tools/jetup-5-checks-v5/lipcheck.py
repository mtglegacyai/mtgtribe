# Lip sync check without face landmarks: mouth-area motion vs voice loudness, best lag in frames (25 fps).
import sys, subprocess, numpy as np
def frames(path, ss, dur, roi):
    x0, y0, x1, y1 = roi; w, h = x1 - x0, y1 - y0
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-t', str(dur), '-i', path, '-vf', f'crop={w}:{h}:{x0}:{y0},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    a = np.frombuffer(p, np.uint8).reshape(-1, h, w).astype(np.float32)
    return np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
def audio_env(path, ss, dur, n):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-t', str(dur), '-i', path, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    a = np.frombuffer(p, np.int16).astype(np.float32); hop = 640
    e = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(n)])
    return np.abs(np.diff(np.log(e + 1), prepend=np.log(e[0] + 1)))     # change in loudness, like change in the mouth
def best(m, e):
    m = (m - m.mean()) / m.std(); e = (e - e.mean()) / e.std(); n = min(len(m), len(e)); m, e = m[:n], e[:n]
    cs = {k: float(np.mean(m[max(0, k):n + min(0, k)] * e[max(0, -k):n + min(0, -k)])) for k in range(-6, 7)}
    k = max(cs, key=cs.get); return k, cs[k], cs
name, video, audio, ss, dur, x0, y0, x1, y1 = sys.argv[1:10]
m = frames(video, float(ss), float(dur), tuple(int(v) for v in (x0, y0, x1, y1)))
e = audio_env(audio, float(ss), float(dur), len(m) + 1)[1:]
k, c, cs = best(m, e)
print(f'{name}: best lag {k:+d} frames ({k * 40:+d} ms; positive = mouth moves AFTER the sound), corr {c:.3f}, corr at 0: {cs[0]:.3f}')
