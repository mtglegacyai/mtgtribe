# QA for a new video: loudness, true peak, sample overshoots, full speech-to-text, a contact sheet and the emoji-pop frames.
# Usage: qa_new.py <video dir> <video.mp4>
import subprocess, sys, json, re, os, numpy as np
from PIL import Image, ImageDraw
D, F = sys.argv[1], sys.argv[2]; V = os.path.join(D, F)
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', V]))
out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', V, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print('duration', round(dur, 2), 's; loudness', re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1], 'LUFS, true peak', re.findall(r'Peak:\s+(-?[\d.]+) dBFS', out)[-1], 'dBFS')
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', V, '-f', 's16le', '-ac', '2', '-ar', '48000', '-'], capture_output=True).stdout
a = np.abs(np.frombuffer(raw, np.int16).astype(np.float32) / 32768); print('samples over 0.9:', int((a > .9).sum()), ' max', round(float(a.max()), 3))
def grab(t):
    return Image.open(__import__('io').BytesIO(subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', V, '-frames:v', '1', '-f', 'image2', '-c:v', 'mjpeg', '-'])))
ts = list(np.linspace(1, dur - .5, 24)); W, H = 480, 270
sh = Image.new('RGB', (W * 6, H * 4))
for i, t in enumerate(ts):
    im = grab(t).resize((W, H)); ImageDraw.Draw(im).text((6, 6), f'{t:.1f}', fill='yellow'); sh.paste(im, ((i % 6) * W, (i // 6) * H))
sh.save(os.path.join(D, 'final_sheet.jpg'), quality=86)
s = open(os.path.join(D, 'stage', 'timeline.js')).read(); TL = json.loads(s[s.index('=') + 1:].strip().rstrip(';'))
em = [e[0] for e in TL.get('emos', [])]
if em:
    es = Image.new('RGB', (960 * len(em), 540))
    for i, t in enumerate(em): es.paste(grab(t + .6).resize((960, 540)), (960 * i, 0))
    es.save(os.path.join(D, 'emo_check.jpg'), quality=86)
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', V, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
from faster_whisper import WhisperModel
segs, _ = WhisperModel('small.en', device='cpu', compute_type='int8').transcribe(x, language='en', beam_size=5)
open(os.path.join(D, 'transcript.txt'), 'w').write('\n'.join(f'{s_.start:6.1f} {s_.text.strip()}' for s_ in segs)); print('transcript written')
