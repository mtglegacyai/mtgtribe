import json, sys
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2], device='cpu', compute_type='int8', cpu_threads=4)
import wave, numpy as np
wf = wave.open(sys.argv[1]); a = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
segs, info = m.transcribe(a, language='en', word_timestamps=True, vad_filter=False, beam_size=5,
                          initial_prompt='MTG TRIBE, MusaTheGiant, ALTRUVA, Bellver, WhatsApp, TikTok, mtgtribe.com/group, Crypto Regards.')
out = []
for s in segs:
    out.append({'start': s.start, 'end': s.end, 'text': s.text.strip(),
                'words': [{'w': w.word, 's': round(w.start, 3), 'e': round(w.end, 3), 'p': round(w.probability, 3)} for w in s.words]})
    print(f"{s.start:7.2f} {s.end:7.2f} {s.text.strip()}", flush=True)
json.dump(out, open(sys.argv[3], 'w'), indent=1)
