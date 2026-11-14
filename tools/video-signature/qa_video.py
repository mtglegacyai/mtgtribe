# QA for a consistency rebuild: body frames identical to the published version (except emoji pops), speech-to-text of the
# new ending, loudness and true peak of the encoded file. Usage: qa_video.py old.mp4 new.mp4 kit_start [ending_from]
import subprocess, sys, json, re, numpy as np
old, new, k0 = sys.argv[1], sys.argv[2], float(sys.argv[3])
def info(f):
    o = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'json', f]))
    s = [x for x in o['streams'] if 'width' in x][0]; return s['width'], s['height']
W, H = info(new)
def grab(f, t):
    b = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', f, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    return np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
bad = []
for t in np.linspace(2, k0 - 1, 24):
    d = np.abs(grab(old, t) - grab(new, t)).mean(2); m = d > 25
    if m.mean() > 0.002:
        ys, xs = np.where(m); bad.append((round(float(t), 1), round(float(m.mean()), 4), (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))))
print('body frames differing (t, share, bbox):', bad if bad else 'none')
out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', new, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print('loudness', re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1], 'LUFS, true peak', re.findall(r'Peak:\s+(-?[\d.]+) dBFS', out)[-1], 'dBFS')
a0 = float(sys.argv[4]) if len(sys.argv) > 4 else k0
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a0), '-i', new, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
from faster_whisper import WhisperModel
segs, _ = WhisperModel('small.en', device='cpu', compute_type='int8').transcribe(x, language='en', beam_size=5)
print('ending heard:', ' '.join(s.text.strip() for s in segs))
