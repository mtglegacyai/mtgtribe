# CoinZoom video 2: "How to Load Cash into your CoinZoom Account", narrated by MTG (14 Nov 2026).
# Builds the timeline from the voice: where every line plays, which source frame shows when, the camera, rings, taps,
# chips, step pills, panels, captions, emoji pops, the signature ending's cues and the body sounds.
# Writes timeline.json, voice.wav, kitcues.json, mixcues.json, sfx_body.json.
import json, os, re, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'engine'))
import mtg_ending as ME
SR, FPS = 48000, 30
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))

BODY = ['hi', 'n_thanks', 'n_in', 'n_four', 'takeyour', 'pause', 'n_what', 'n_s1', 'n_s2', 'n_s3', 'n_s3b', 'n_s4', 'n_tip',
        'n_done', 'n_recap', 'n_recap2', 'n_turn2']
ORDER = BODY + ['every', 'n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive',
                'o_best', 'o_im', 'o_see', 'o_lgtc']
GAP = {'hi': .35, 'n_thanks': .6, 'n_in': .35, 'n_four': .45, 'takeyour': .25, 'pause': .85, 'n_what': 1.1, 'n_s1': 1.1,
       'n_s2': 1.35, 'n_s3': .35, 'n_s3b': 1.1, 'n_s4': .45, 'n_tip': 1.05, 'n_done': 1.25, 'n_recap': .3, 'n_recap2': .5,
       'n_turn2': .6, 'every': .5, 'n_save': .3, 'n_share': .4, 'n_we': .5, 'n_slog': .6, 'o_dyor': .35, 'o_massive': .35,
       'o_best': .35, 'o_see': .2}
t = 0.7; S, E = {}, {}
for k in ORDER:
    S[k] = round(t, 3); E[k] = round(t + L[k]['dur'], 3); t = E[k] + GAP.get(k, .28)
T = round(E['o_lgtc'] + .12 + 3.25, 2)

def norm(w): return re.sub(r"[^a-z0-9]", '', w.lower())
def wt(k, word, n=0, end=False):
    """absolute time of the n-th occurrence of word in line k"""
    hits = [w for w in WD[k] if norm(w['w']) == norm(word)]
    return round(S[k] + (hits[n]['b'] if end else hits[n]['a']), 3)

# ---------------------------------------------------------------- voice track
voice = np.zeros(int(round(T * SR)), np.float32)
for k in ORDER:
    with wave.open(os.path.join(HERE, 'lines', L[k]['file'])) as w:
        y = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    a = int(round(S[k] * SR)); voice[a:a + len(y)] += y[:len(voice) - a]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())

# ---------------------------------------------------------------- the signature ending's cues (links line not spoken)
absw = [dict(w=w['w'], a=S[k] + w['a'], b=S[k] + w['b']) for k in ORDER for w in WD[k]]
K = ME.find_cues(absw, links=False)

# ---------------------------------------------------------------- source frames: (out t0, out t1, src t0, src t1)
# the clip (1920x1080, read at 30 fps): title and stores to 4.5 s, Wallet 6.0 to 10.1, Deposit 10.3 to 11.9, the map
# 12.1 to 14.1, the barcode 14.3 to 16.8, the closing card "You're done!" from 17.3; CoinZoom's own tap circles at 7.1
# (Wallet), 9.4 (Deposit) and 11.1 (CoinZoom Cash) are skipped by holding the frames before them
Tin = S['n_in'] - .35
Tw = S['n_s1'] - 1.0                          # title fades, the Wallet screen comes in
Tdep = wt('n_s1', 'Deposit') + .55            # Deposit opens
Tmap = wt('n_s2', 'Cash') + .55               # CoinZoom Cash opens the map
Tbar = S['n_s4'] - .55                        # the barcode screen
Tdone = S['n_done'] - .45                     # the closing card
Trec = S['n_recap'] - .3
SRC = [(0, Tw, 1.3, 1.3),
       (Tw, Tw + 1.65, 4.45, 6.10), (Tw + 1.65, Tdep, 6.30, 6.30),
       (Tdep, Tdep + .3, 10.05, 10.35), (Tdep + .3, Tmap, 10.60, 10.60),
       (Tmap, Tmap + .7, 11.45, 12.15), (Tmap + .7, Tbar, 12.90, 12.90),
       (Tbar, Tbar + .75, 13.65, 14.40), (Tbar + .75, Tdone, 15.20, 15.20),
       (Tdone, Tdone + .75, 16.70, 17.45), (Tdone + .75, T, 17.95, 17.95)]

# ---------------------------------------------------------------- camera moves (t0, t1, cx, cy, z) in source px
CAM0 = (960, 540, 1.0)
CAM = [(0, Tin, 960, 540, 1.04),
       (E['pause'] + .2, E['pause'] + 1.7, 700, 600, 1.12),    # the stores
       (Tw - .1, Tw + .4, 960, 540, 1.0),
       (Tw + 1.7, Tw + 2.5, 1390, 430, 1.6),                    # Wallet: the title, the balance line, Deposit
       (Tdep + .1, Tdep + .8, 1390, 420, 1.8),                  # the Deposit list
       (Tmap + .2, Tmap + .9, 1390, 576, 1.35),                 # the map
       (Tbar + .2, Tbar + .9, 1390, 480, 1.7),                  # the barcode screen
       (Tdone - .75, Tdone - .05, 960, 540, 1.0),               # out for the closing card
       (Tdone + .8, Trec + .4, 960, 540, 1.04)]

# ---------------------------------------------------------------- rings, taps, chips, step pills (source rects)
B = {'stores': (250, 770, 990, 995), 'wallet': (1186, 186, 1300, 224), 'deposit': (1187, 283, 1377, 338),
     'czcash': (1199, 424, 1575, 466), 'map': (1180, 196, 1594, 956), 'pin': (1340, 530, 1420, 580),
     'barcode': (1222, 318, 1552, 380), 'expires': (1300, 405, 1480, 430), 'ask': (1200, 460, 1590, 495),
     'terms': (1210, 520, 1592, 722)}
RINGS = [('stores', wt('n_what', 'Speedway') - .1, E['n_what'] + .35, 'gold'),
         ('wallet', wt('n_s1', 'Wallet') - .1, wt('n_s1', 'tap') - .05, 'gold'),
         ('deposit', wt('n_s1', 'Deposit') - .1, Tdep + .05, 'lime'),
         ('czcash', wt('n_s2', 'CoinZoom') - .1, Tmap + .05, 'lime'),
         ('map', wt('n_s3', 'map') - .1, wt('n_s3', 'store') - .1, 'lime'),
         ('pin', wt('n_s3', 'store') - .1, E['n_s3b'] + .35, 'gold'),
         ('barcode', wt('n_s4', 'barcode') - .1, wt('n_s4', 'cashier') - .05, 'lime'),
         ('ask', wt('n_s4', 'cashier') - .05, E['n_s4'] + .3, 'gold'),
         ('expires', wt('n_tip', 'timer') - .1, wt('n_tip', 'fee') - .1, 'gold'),
         ('terms', wt('n_tip', 'fee') - .1, E['n_tip'] + .4, 'lime')]
TAPS = [('deposit', wt('n_s1', 'Deposit') + .3), ('czcash', wt('n_s2', 'Cash') + .25)]
CHIPS = [('📍', 'Only CoinZoom Cash stores', wt('n_s3b', 'only'), E['n_s3b'] + .45, 'L'),
         ('⏱️', 'Your barcode has a timer', wt('n_tip', 'timer'), wt('n_tip', 'fee') - .1, 'L'),
         ('📋', 'Read the fee and limits', wt('n_tip', 'fee'), E['n_tip'] + .45, 'L')]
STEPS = [(1, [['Tap ', 0], ['Deposit', 1]], S['n_s1'] - .05, S['n_s2'] - .05),
         (2, [['Tap ', 0], ['CoinZoom Cash', 1]], S['n_s2'] - .05, S['n_s3'] - .05),
         (3, [['Pick a ', 0], ['store', 1]], S['n_s3'] - .05, S['n_s4'] - .05),
         (4, [['Show your ', 0], ['barcode', 1]], S['n_s4'] - .05, Tdone - .2)]

# privacy: CoinZoom's demo wallet balances and the one-time barcode are blurred in every frame they can show; how fully a
# screen is in is measured against a frame where it is fully in, so the labels fade with the clip's own transitions
from PIL import Image
def vis(rect, ref, frames):
    R = np.asarray(Image.open(os.path.join(HERE, 'src1080', f'f{ref:04d}.jpg')).convert('L').crop(rect), np.float32); out = {}
    for n in range(frames[0], frames[1] + 1):
        A = np.asarray(Image.open(os.path.join(HERE, 'src1080', f'f{n:04d}.jpg')).convert('L').crop(rect), np.float32)
        out[str(n)] = round(float(np.clip(1 - np.abs(A - R).mean() / 30, 0, 1)), 2)
    return out
MASKS = [dict(rect=(1180, 228, 1598, 262), label='Balance hidden', frames=(172, 312), full=(0, -1), alpha=vis((1180, 228, 1598, 262), 190, (172, 312))),
         dict(rect=(1455, 395, 1580, 915), label=None, frames=(172, 312), full=(0, -1)),
         dict(rect=(1222, 318, 1552, 380), label='Your barcode', frames=(414, 512), full=(0, -1), alpha=vis((1222, 318, 1552, 380), 456, (414, 512)))]
PLATE = dict(frame=157, x_cut=1140, frames=(176, 506))

# ---------------------------------------------------------------- panels
PLAN = dict(t0=Tin, t1=E['pause'] + .35, subtext='Load cash into your CoinZoom account',
            segs=[[['Tap ', 0], ['Deposit', 1]], [['Tap ', 0], ['CoinZoom Cash', 1]], [['Pick a ', 0], ['store', 1]], [['Show your ', 0], ['barcode', 1]]],
            rows=[wt('n_four', 'Deposit'), wt('n_four', 'CoinZoom'), wt('n_four', 'pick'), wt('n_four', 'show')],
            sub=S['n_in'] + .9, pause=wt('pause', 'pause') - .05)
RECAP = dict(t0=Trec + .15, t1=wt('n_turn2', 'Now') - .05,
             cards=[['🏦', 'Tap Deposit', 'In your Wallet'], ['💵', 'CoinZoom Cash', 'Load cash nearby'],
                    ['📍', 'Pick a store', 'On the map'], ['🧾', 'Cashier scans', 'Your barcode, then a receipt']],
             ticks=[wt('n_recap2', 'Deposit'), wt('n_recap2', 'CoinZoom'), wt('n_recap2', 'picked'), wt('n_recap2', 'scanned')])
TURN = dict(t0=wt('n_turn2', 'Now') - .1, t1=K['T_LINKS'] + .3, turn=wt('n_turn2', 'turn'),
            chip='Open your CoinZoom app: Deposit, CoinZoom Cash')
WIN = dict(out0=Trec, out1=Trec + .45)
EMOS = [(wt('hi', 'Hi'), '👋'), (wt('n_what', 'stores'), '🏪'), (wt('n_s1', 'Deposit') + .1, '👆'),
        (wt('n_s3', 'store'), '📍'), (wt('n_done', 'receipt'), '🎉'), (wt('n_turn2', 'turn'), '🚀')]

# ---------------------------------------------------------------- captions: one per line, the spoken word lit
CAPS = []
for i, k in enumerate(ORDER):
    nxt = S[ORDER[i + 1]] if i + 1 < len(ORDER) else T
    end = min(E[k] + .35, nxt - .02)
    if S[k] >= K['END_CARD']: break
    toks = L[k]['text'].split()                       # caption words as written (punctuation), timed by the word list
    shown = toks if [norm(x) for x in toks] == [norm(w['w']) for w in WD[k]] else [w['w'] for w in WD[k]]
    if shown is not toks: print('caption fallback (word list spelling):', k)
    CAPS.append(dict(k=k, t0=S[k], t1=min(end, K['END_CARD']), words=[dict(w=x, a=round(S[k] + w['a'], 3), b=round(S[k] + w['b'], 3)) for x, w in zip(shown, WD[k])]))

# ---------------------------------------------------------------- body sounds (the training's four)
sfx = dict(whoosh=[Tin, PLAN['t1'] - .3, Tw, Tdep, Tmap, Tbar, Tdone, Trec, TURN['t0']],
           tick=PLAN['rows'] + [PLAN['pause']] + RECAP['ticks'] + [c[2] for c in CHIPS] + [S['n_in'] + .9],
           pop=[e[0] for e in EMOS if e[1] in ('🎉', '🚀')] + [TURN['turn']],
           click=[tp[1] for tp in TAPS])
sfx = {k: sorted(round(x, 3) for x in v) for k, v in sfx.items()}

TL = dict(T=T, fps=FPS, S=S, E=E, SRC=SRC, CAM0=CAM0, CAM=CAM, B=B, RINGS=RINGS, TAPS=TAPS, CHIPS=CHIPS, STEPS=STEPS,
          MASKS=MASKS, PLATE=PLATE, PLAN=PLAN, RECAP=RECAP, TURN=TURN, WIN=WIN, EMOS=EMOS, CAPS=CAPS,
          END_CARD=K['END_CARD'], KIT_START=K['T_LINKS'], SRCDIR='src1080', SRC_W=1920, SRC_H=1080, SRC_N=539,
          SERIES='COINZOOM · LOAD CASH')
json.dump(TL, open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1, ensure_ascii=False)
json.dump(dict(cues=K, orient='h', nxt=None, links=False, T=T, fps=FPS), open(os.path.join(HERE, 'kitcues.json'), 'w'), indent=1)
json.dump(dict(spans=[[S[k], E[k]] for k in ORDER]), open(os.path.join(HERE, 'mixcues.json'), 'w'), indent=1)
json.dump(sfx, open(os.path.join(HERE, 'sfx_body.json'), 'w'))
print('T =', T, 's; ending from', K['T_LINKS'], 'end card', K['END_CARD'])
for k in ORDER: print(f'{k:10s} {S[k]:7.2f} {E[k]:7.2f}')
