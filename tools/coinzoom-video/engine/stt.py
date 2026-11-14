# speech-to-text with word times (faster-whisper small.en), audio decoded by ffmpeg
import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
def load16(p, ss=None, to=None):
    cmd = ['ffmpeg', '-v', 'error'] + (['-ss', str(ss)] if ss is not None else []) + (['-to', str(to)] if to is not None else []) + ['-i', p, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)
if __name__ == '__main__':
    p = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else None
    m = WhisperModel('small.en', device='cpu', compute_type='int8')
    segs, _ = m.transcribe(load16(p), beam_size=5, word_timestamps=True)
    W = []
    for s in segs:
        print(f"{s.start:7.2f}-{s.end:7.2f} {s.text}", flush=True)
        W += [dict(w=w.word.strip(), a=round(w.start, 3), b=round(w.end, 3)) for w in s.words]
    if out: json.dump(W, open(out, 'w'))
