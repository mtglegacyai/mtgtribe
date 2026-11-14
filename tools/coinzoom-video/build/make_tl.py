# CoinZoom: "How to Find Your Virtual CoinZoom Visa Debit Card in the App", narrated by MTG (14 Nov 2026).
# Builds the timeline from the voice: where every line plays, which source frame shows when, the camera, rings, taps,
# chips, step pills, panels, captions, emoji pops, the signature ending's cues and the body sounds.
# Writes timeline.json, voice.wav, kitcues.json, mixcues.json, sfx_body.json.
import json, os, re, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, HERE)
import mtg_ending as ME
SR, FPS = 48000, 30
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))

BODY = ['hi', 'n_thanks', 'n_in', 'n_three', 'takeyour', 'pause', 'n_once', 'n_s1', 'n_s1b', 'n_s2', 'n_s3', 'n_s3b',
        'n_there', 'n_copy', 'n_keep', 'n_recap', 'n_recap2', 'n_turn2']
ORDER = BODY + ['every', 'n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive',
                'o_best', 'o_im', 'o_see', 'o_lgtc']
GAP = {'hi': .35, 'n_thanks': .6, 'n_in': .4, 'n_three': .45, 'takeyour': .25, 'pause': .85, 'n_once': 1.05, 'n_s1': .4,
       'n_s1b': .85, 'n_s2': 1.15, 'n_s3': .3, 'n_s3b': 1.0, 'n_there': .4, 'n_copy': .75, 'n_keep': 1.35, 'n_recap': .3,
       'n_recap2': .5, 'n_turn2': .6, 'every': .5, 'n_save': .3, 'n_share': .4, 'n_we': .5, 'n_slog': .6, 'o_dyor': .35,
       'o_massive': .35, 'o_best': .35, 'o_see': .2}
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
Tin = S['n_in'] - .35                         # the plan panel arrives
Tact = E['pause'] + .15                       # "activated" scene: the source's cut to the hand photo
Ts1 = S['n_s1'] - 1.0                         # step 1: the source's cut to the green screen, the phone comes in
Treveal = wt('n_s2', 'Reveal')                # the Reveal tap
Tsheet = Treveal + .5                         # the confirm sheet slides up
Tdet = E['n_s3b'] + .3                        # crossfade to the card details
Tonly = wt('n_keep', 'only')                  # crossfade to the hand photo
Trec = S['n_recap'] - .3                      # the window leaves, the recap arrives
SRC = [(0, Tact, 1.0, 1.0),                                   # title card (cover, greeting, plan panel)
       (Tact, Tact + .95, 2.45, 3.40), (Tact + .95, Ts1, 3.40, 3.40),
       (Ts1, Ts1 + 1.55, 5.00, 6.55), (Ts1 + 1.55, S['n_s2'] - .2, 7.50, 7.50),
       (S['n_s2'] - .2, Tsheet, 11.0, 11.0),
       (Tsheet, Tsheet + .4, 12.42, 12.82), (Tsheet + .4, Tdet, 13.50, 13.50),
       (Tdet, Tdet + .3, 13.87, 14.17), (Tdet + .3, Tonly - .35, 14.60, 14.60),
       (Tonly - .35, Tonly - .35 + 1.93, 15.10, 17.03), (Tonly - .35 + 1.93, T, 17.03, 17.03)]

# ---------------------------------------------------------------- camera moves (t0, t1, cx, cy, z) in 720p source px
CAM0 = (640, 360, 1.0)
CAM = [(0, Tin, 640, 360, 1.045),                              # slow push on the title card
       (Tact, Tact + .05, 640, 360, 1.0), (Tact + .95, Ts1, 700, 330, 1.07),
       (Ts1, Ts1 + .05, 640, 360, 1.0),
       (S['n_s1'] + .35, S['n_s1'] + 1.35, 943, 470, 1.8),    # down to the tab bar
       (E['n_s1'] + .05, S['n_s1b'] + .45, 943, 330, 1.8),    # up to the card
       (E['n_s1b'] + .25, S['n_s2'] + .45, 943, 430, 1.8),    # Virtual Card, Reveal
       (Tsheet, Tsheet + .7, 943, 420, 1.8),                  # the confirm sheet
       (Tdet - .1, Tdet + .6, 943, 345, 1.75),                # the card details
       (Tonly - .95, Tonly - .38, 640, 360, 1.0),             # out to the photo (done before the source's crossfade)
       (Tonly + .3, Trec + .4, 700, 360, 1.05)]

# ---------------------------------------------------------------- rings, taps, chips, step pills (src rects, 720p)
B = {'spend_tab': (978, 620, 1027, 656), 'reveal': (808, 540, 940, 566), 'vcard': (810, 509, 940, 528),
     'card': (815, 203, 1076, 373), 'review': (840, 368, 1045, 388), 'face': (922, 400, 963, 440),
     'dbl': (880, 458, 1005, 477), 'num': (821, 346, 1064, 370), 'name': (821, 407, 1064, 432), 'exp': (821, 468, 951, 494),
     'cvv': (976, 468, 1066, 494), 'copy': (1031, 348, 1064, 369)}
RINGS = [('spend_tab', wt('n_s1', 'Spend') - .1, E['n_s1'] + .25, 'lime'),
         ('card', wt('n_s1b', 'card') - .15, E['n_s1b'] + .5, 'gold'),
         ('vcard', wt('n_s2', 'Virtual') - .1, wt('n_s2', 'then') + .1, 'lime'),
         ('reveal', Treveal - .1, Tsheet + .05, 'lime'),
         ('review', wt('n_s3', 'confirm') - .1, S['n_s3b'] - .05, 'gold'),
         ('dbl', wt('n_s3b', 'Double') - .1, Tdet, 'lime'),
         ('num', wt('n_there', 'number') - .15, wt('n_there', 'cardholder') - .1, 'lime'),
         ('name', wt('n_there', 'cardholder') - .1, wt('n_there', 'expiry') - .1, 'lime'),
         ('exp', wt('n_there', 'expiry') - .1, wt('n_there', 'CVV') - .1, 'lime'),
         ('cvv', wt('n_there', 'CVV') - .1, E['n_there'] + .35, 'lime'),
         ('copy', wt('n_copy', 'Copy') - .1, E['n_copy'] + .4, 'lime')]
TAPS = [('spend_tab', wt('n_s1', 'Spend') + .35), ('reveal', Treveal + .3),
        ('face', wt('n_s3b', 'Double') + .05), ('face', wt('n_s3b', 'Double') + .25), ('copy', wt('n_copy', 'Copy') + .3)]
CHIPS = [('✅', 'Card screen open', wt('n_s1b', 'opens'), E['n_s1b'] + .5),
         ('🔐', 'Confirm it is you', wt('n_s3', 'confirm'), Tdet),
         ('✅', 'Your virtual card details', wt('n_there', 'there'), wt('n_copy', 'Tap') - .1),
         ('📋', 'Tap Copy for the number', wt('n_copy', 'Copy'), E['n_copy'] + .45),
         ('🔒', 'Keep these details private', wt('n_keep', 'private') - .2, Tonly - .3)]
STEPS = [(1, [['Tap ', 0], ['Spend', 1]], S['n_s1'] - .05, S['n_s2'] - .05), (2, [['Tap ', 0], ['Reveal', 1]], S['n_s2'] - .05, S['n_s3'] - .05),
         (3, [['Double tap', 1], [' to confirm', 0]], S['n_s3'] - .05, Tonly - .3)]
# privacy: the card details screen (source frames 418 to 460) is blurred under labelled pills in every frame it shows
MASKS = [((821, 346, 1028, 370), 'Your card number'), ((821, 407, 1064, 432), 'Your name'), ((821, 468, 951, 494), 'MM/YY')]
MASK_FRAMES = (414, 462)                 # source frame numbers (1-based file names) with the blur on
LABEL_ALPHA = {418: .25, 419: .5, 420: .75, 456: .85, 457: .65, 458: .45, 459: .25, 460: .1}   # else 1 inside 421..455

# ---------------------------------------------------------------- panels
# the panel fades out over the source's own cut to the photo, so the bright title card never flashes back
PLAN = dict(t0=Tin, t1=Tact + .3, rows=[wt('n_three', 'Spend'), wt('n_three', 'Reveal'), wt('n_three', 'double')],
            sub=S['n_in'] + .9, pause=wt('pause', 'pause') - .05)
RECAP = dict(t0=Trec + .15, t1=wt('n_turn2', 'Now') - .05, ticks=[wt('n_recap2', 'Spend'), wt('n_recap2', 'Reveal'), wt('n_recap2', 'double')])
TURN = dict(t0=wt('n_turn2', 'Now') - .1, t1=K['T_LINKS'] + .3, turn=wt('n_turn2', 'turn'))
WIN = dict(out0=Trec, out1=Trec + .45)
EMOS = [(wt('hi', 'Hi'), '👋'), (wt('n_once', 'activated'), '💳'), (wt('n_s1', 'Spend') + .1, '👆'),
        (wt('n_there', 'there'), '🎉'), (wt('n_keep', 'private'), '🔒'), (wt('n_turn2', 'turn'), '🚀')]

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
sfx = dict(whoosh=[Tin, Tact, Ts1, S['n_s2'] - .05, S['n_s3'] - .05, Tdet, Tonly - .35, Trec, TURN['t0']],
           tick=PLAN['rows'] + [PLAN['pause']] + RECAP['ticks'] + [c[2] for c in CHIPS] + [S['n_in'] + .9],
           pop=[e[0] for e in EMOS if e[1] in ('🎉', '🚀')] + [TURN['turn']],
           click=[tp[1] for tp in TAPS])
sfx = {k: sorted(round(x, 3) for x in v) for k, v in sfx.items()}

TL = dict(T=T, fps=FPS, S=S, E=E, SRC=SRC, CAM0=CAM0, CAM=CAM, B=B, RINGS=RINGS, TAPS=TAPS, CHIPS=CHIPS, STEPS=STEPS,
          MASKS=MASKS, MASK_FRAMES=MASK_FRAMES, LABEL_ALPHA=LABEL_ALPHA, PLAN=PLAN, RECAP=RECAP, TURN=TURN, WIN=WIN,
          EMOS=EMOS, CAPS=CAPS, END_CARD=K['END_CARD'], KIT_START=K['T_LINKS'])
json.dump(TL, open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1, ensure_ascii=False)
json.dump(dict(cues=K, orient='h', nxt=None, links=False, T=T, fps=FPS), open(os.path.join(HERE, 'kitcues.json'), 'w'), indent=1)
json.dump(dict(spans=[[S[k], E[k]] for k in ORDER]), open(os.path.join(HERE, 'mixcues.json'), 'w'), indent=1)
json.dump(sfx, open(os.path.join(HERE, 'sfx_body.json'), 'w'))
print('T =', T, 's; ending from', K['T_LINKS'], 'end card', K['END_CARD'])
for k in ORDER: print(f'{k:10s} {S[k]:7.2f} {E[k]:7.2f}')
