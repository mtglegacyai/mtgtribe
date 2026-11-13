# QA for the finished video: frames all present and decodable, brightness jumps, speech-to-text of the final audio.
import os, sys, json, subprocess, re, wave
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); MP4 = sys.argv[1]
LO = json.load(open(f'{D}/wa/lines_out.json')); N = round(LO['T'] * 30)
# brightness per frame (from the encoded video, 108x192 grey)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', MP4, '-vf', 'scale=108:192,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(np.float32); m = fr.mean(axis=(1, 2))
d = np.abs(np.diff(m)); big = np.where(d > 6)[0]
print('frames', len(m), 'of', N, '| mean luma', round(m.mean(), 1), '| jumps > 6:', [(int(i), round(float(d[i]), 1), round(i / 30, 2)) for i in big][:20])
