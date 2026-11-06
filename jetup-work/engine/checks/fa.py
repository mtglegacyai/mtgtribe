# Forced alignment with pocketsphinx: python3 fa.py audio.wav start dur "text"
import sys, subprocess, numpy as np
from pocketsphinx import Decoder
wav, ss, du, text = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(ss), '-t', str(du), '-i', wav, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'])
d = Decoder(samprate=16000, bestpath=False)
d.set_align_text(text.lower())
d.start_utt(); d.process_raw(pcm, full_utt=True); d.end_utt()
for seg in d.seg():
    print(f'{ss + seg.start_frame/100:8.2f} {ss + seg.end_frame/100:8.2f}  {seg.word}')
