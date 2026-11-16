# Cut MTG's banked voice lines for tutorial part 1, edges refined from the audio energy.
import subprocess, numpy as np, json, csv, wave
SR = 48000
def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
rows = list(csv.reader(open('sentences.tsv'), delimiter='\t'))
AUD = {'t1': load('t1.mp3'), 't3': load('t3.mp3'), 'v2': load('p1v2_raw.wav'), 'v3': load('p1v3_raw.wav')}
V2 = json.load(open('p1v2_lines.json'))
V2SPANS = [(0.256, 2.112), (2.688, 7.941), (8.366, 13.132), (13.785, 18.357), (19.181, 23.294), (23.832, 27.345), (28.246, 32.235),
           (32.811, 37.658), (38.653, 41.67), (42.322, 45.492), (45.992, 49.012), (50.086, 52.027), (52.603, 55.73), (56.23, 57.717),
           (58.426, 61.178), (61.754, 66.332), (67.216, 71.043), (71.696, 76.696), (77.537, 81.864), (82.401, 89.548)]
for (k, t), (a, b) in zip(V2, V2SPANS):
    rows.append(['signup-training/v2.mp3', str(a), str(b), t])
V3 = json.load(open('p1v3_lines.json'))
for (k, t), (a, b) in zip(V3, [(0.256, 6.639), (7.253, 11.738), (12.16, 18.0)]):
    rows.append(['signup-training/v3.mp3', str(a), str(b), t])
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
    ('hi', 't1', 'Hi, my name is MTG'), ('takeyour', 't1', 'Take your time.'), ('pause', 't1', 'You can pause any step'),
    ('grab', 't1', 'Grab your phone.'), ('together', 't1', "We're going to do this together"),
    ('share', 't3', "Share it with someone who's ready"), ('o_fin', 't3', 'Quick reminder'), ('o_dyor', 't3', 'Always do your own'),
    ('o_thanks', 't3', 'Thank you for tuning in'), ('o_support', 't3', 'Your support means'), ('o_massive', 't3', 'And thank yourself'),
    ('o_best', 't3', 'I wish you nothing'), ('o_im', 't3', "I'm MTG, Your Digital"), ('o_see', 't3', 'See you on the next'),
    ('o_lgtc', 't3', "Let's Get This Crypto"),
] + [(k, 'v2', t) for k, t in V2] + [(k, 'v3', t) for k, t in V3]
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
