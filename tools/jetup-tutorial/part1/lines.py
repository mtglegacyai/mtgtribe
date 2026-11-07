# Cut MTG's banked voice lines for tutorial part 1, edges refined from the audio energy.
import subprocess, numpy as np, json, csv, wave
SR = 48000
def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
AUD = {'t1': load('t1.mp3'), 't3': load('t3.mp3')}
rows = list(csv.reader(open('sentences.tsv'), delimiter='\t'))
def find(fid, text):
    for r in rows:
        if r[0] == f'signup-training/{fid}.mp3' and r[3].startswith(text):
            return float(r[1]), float(r[2]), r[3]
    raise SystemExit('missing ' + text)
LINES = [
    ('p1', 't1', 'Part one.'), ('create', 't1', 'Create your JetUP account.'),
    ('open', 't1', 'Open the Partner link'), ('partner', 't1', "Make sure it's the Partner link"),
    ('ifme', 't1', "If that's me"), ('indiv', 't1', 'On the sign up form'), ('type', 't1', 'Type your first name'),
    ('pw', 't1', 'Your password needs'), ('country', 't1', 'Choose your country'), ('code', 't1', 'The country code'),
    ('reg', 't1', 'Then pass the security check'), ('mail', 't1', 'Check your email, and tap'),
    ('inbox', 't1', 'Not in your inbox?'), ('spam', 't1', 'Check spam or junk mail.'),
    ('links', 't3', 'Everything I showed you'), ('save', 't3', 'Save this video'), ('pays', 't3', 'It pays to pay attention'),
]
def env(x):
    hop = SR // 200  # 5 ms
    n = len(x) // hop
    return np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
out = {}
for key, fid, txt in LINES:
    a, b, full = find(fid, txt)
    x = AUD[fid]
    e = env(x)
    sil = e < 0.007
    # silence gaps of at least 110 ms (5 ms bins)
    gaps = []; i = 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j + 1 < len(sil) and sil[j + 1]:
                j += 1
            if j - i + 1 >= 22:
                gaps.append((i / 200, (j + 1) / 200))
            i = j + 1
        else:
            i += 1
    g_end = min(gaps, key=lambda g: abs(g[1] - a))
    g_st = min(gaps, key=lambda g: abs(g[0] - b))
    s = g_end[1] - 0.04
    en = g_st[0] + 0.10
    y = x[int(s * SR):int(en * SR)].copy()
    f_in, f_out = int(0.012 * SR), int(0.06 * SR)
    y[:f_in] *= np.linspace(0, 1, f_in); y[-f_out:] *= np.linspace(1, 0, f_out)
    p = f'v_{key}.wav'
    with wave.open(p, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    out[key] = dict(file=p, src=fid, a=round(s, 3), b=round(en, 3), dur=round(len(y) / SR, 3), text=full)
    print(f'{key:8s} tsv {a:8.3f} {b:8.3f}  cut {s:8.3f} {en:8.3f} {len(y)/SR:6.2f}  {full}')
json.dump(out, open('lines.json', 'w'), indent=1)
