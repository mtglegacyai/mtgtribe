# For every engine-rendered frame: how well does the old-version engine frame (C) match the live video frame,
# in the badge region and over the whole frame? Big numbers = the engine frame is not the same moment.
import subprocess, sys, numpy as np
R, V = sys.argv[1], sys.argv[2]
W, H = 1920, 1080; FS = W * H * 3
fl = [int(x) for x in open(f'{R}/frames_all.txt').read().split()]
want = set(fl)
def dec(f): return subprocess.Popen(['ffmpeg', '-v', 'error', '-i', f, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=FS * 2)
def rd(p):
    b = p.stdout.read(FS); return None if len(b) < FS else np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
po = dec(V); pcs = [dec(f'{R}/old/C_a.mkv'), dec(f'{R}/old/C_b.mkv')]; k = 0; n = 0; rows = []
while True:
    o = rd(po)
    if o is None: break
    if n in want:
        c = rd(pcs[0 if k < len(fl) // 2 else 1]); k += 1
        bd = np.abs(o[28:88, 38:112] - c[28:88, 38:112]).mean(); fd = np.abs(o - c).mean()
        rows.append((n, bd, fd))
    n += 1
rows = np.array(rows)
print('rendered frames', len(rows), 'badge diff median %.2f' % np.median(rows[:, 1]), 'whole-frame diff median %.2f' % np.median(rows[:, 2]))
bad = rows[rows[:, 1] > 15]
print('frames with badge diff > 15:', len(bad))
for r in bad[:60]: print('  frame %d (%.2f s) badge %.1f frame %.1f' % (r[0], r[0] / 25, r[1], r[2]))
np.save(f'{R}/align.npy', rows)
