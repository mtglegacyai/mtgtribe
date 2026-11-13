import sys, wave, json, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
w = wave.open(sys.argv[1]); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768.0
segs, info = m.transcribe(a, language="en", word_timestamps=True, vad_filter=False)
out=[]
for s in segs:
    print(f"{s.start:6.2f} {s.end:6.2f} {s.text.strip()}", flush=True)
    for x in s.words: out.append(dict(w=x.word.strip(), a=round(x.start,3), b=round(x.end,3), p=round(x.probability,3)))
json.dump(out, open(sys.argv[2],'w'))
