# Patch the live v4.2 sign-up training: original frame + (circle-card render - square-card render) on the rendered
# frames, and the static badge change on every other frame. Audio is copied untouched.
import subprocess, sys, numpy as np
from PIL import Image
R = sys.argv[1]; V = sys.argv[2]; OUT = sys.argv[3]
W, H = 1920, 1080; FS = W * H * 3
fl = [int(x) for x in open(f'{R}/frames_all.txt').read().split()]
A0 = np.asarray(Image.open(f'{R}/new/qa3/f_0019.00.png').convert('RGB'), np.float32)
C0 = np.asarray(Image.open(f'{R}/old/qa3/f_0019.00.png').convert('RGB'), np.float32)
BY0, BY1, BX0, BX1 = 28, 88, 38, 112
DB = (A0 - C0)[BY0:BY1, BX0:BX1]                                  # the static badge change
def rd(p):
    b = p.stdout.read(FS)
    return None if len(b) < FS else np.frombuffer(b, np.uint8).reshape(H, W, 3)
dec = lambda f: subprocess.Popen(['ffmpeg', '-v', 'error', '-i', f, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=FS * 2)
po, pa, pc = dec(V), None, None
srcA = [f'{R}/new/A_a.mkv', f'{R}/new/A_b.mkv']; srcC = [f'{R}/old/C_a.mkv', f'{R}/old/C_b.mkv']
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '25', '-i', '-', '-i', V,
                        '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-g', '50',
                        '-c:a', 'copy', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
want = set(fl); k = 0; seg = -1; n = 0; align = []
while True:
    o = rd(po)
    if o is None: break
    f = o.astype(np.float32)
    if n in want:
        if k == 0 or k == len(fl) // 2:
            seg += 1; pa = dec(srcA[seg]); pc = dec(srcC[seg])
        a = rd(pa).astype(np.float32); c = rd(pc).astype(np.float32); k += 1
        align.append(float(np.abs(f[BY0:BY1, BX0:BX1] - c[BY0:BY1, BX0:BX1]).mean()))
        f += a - c
    else:
        f[BY0:BY1, BX0:BX1] += DB
    enc.stdin.write(np.clip(f + 0.5, 0, 255).astype(np.uint8).tobytes()); n += 1
    if n % 2000 == 0: print('frame', n, flush=True)
enc.stdin.close(); enc.wait()
al = np.array(align)
print('frames', n, 'rendered used', k, '| badge alignment on rendered frames: median %.2f, max %.2f' % (np.median(al), al.max()))
