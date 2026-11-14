"""Add explainer #9's voice to MTG's voice bank (branch jetup-video-work), the way explainer #8 was banked.
Usage: python3 bank_ex9.py <voice-bank worktree root> <ex9 build dir>   (run lines_ex9.py first, so the v_*.wav exist)"""
import json, os, re, shutil, subprocess, sys
VB, EX9 = sys.argv[1], sys.argv[2]
BANK = os.path.join(VB, 'jetup-work', 'voice-bank'); EXP = os.path.join(BANK, 'explainers'); PACK = os.path.join(EXP, 'ex9-pack')
os.makedirs(PACK, exist_ok=True)
toks = lambda t: re.findall(r"[A-Za-z0-9']+", t)
ALIGN = {'nauto': .21, 'nyours': .19, 'nlid': .19, 'nrecap': .19}   # measured 13 Nov 2026 (lines_ex9.py)
NEW = ['nhook', 'ncook', 'ntwist', 'npot', 'nauto', 'nyours', 'nlid', 'nrecap']
REC = ['deposit', 'copyx', 'terms', 'perf']

L = json.load(open(os.path.join(EX9, 'lines.json'))); W = json.load(open(os.path.join(EX9, 'words.json')))
raw = json.load(open(os.path.join(EX9, 'voice', 'ex9v3_raw.json')))

# 1. the take as delivered, the text sent, HeyGen's reply with the cut points
shutil.copy(os.path.join(EX9, 'voice', 'ex9v3.flac'), os.path.join(EXP, 'ex9v3.flac'))
shutil.copy(os.path.join(EX9, 'voice', 'ex9v3.txt'), os.path.join(EXP, 'ex9v3.txt'))
tts = dict(audio_url=raw['audio_url'], duration=raw['duration'], original_words=raw['original_words'],
           voice_id=raw['voice_id'], voice_name=raw['voice_name'], model=raw['model'], engine_in_reply=None,
           credits=raw['credits'], date=raw['date'], approved_by=raw['approved_by'],
           note="original_characters were not kept. HeyGen's word times for nauto, nyours, nlid and nrecap run ahead of the "
                "audio by the seconds in word_time_offsets (measured on the pauses and with faster-whisper); add them to those "
                "lines' word times.",
           word_time_offsets=ALIGN,
           lines={k: dict(file=f'v_{k}.wav', src='explainers/ex9v3', a=L[k]['a'], b=L[k]['b'], dur=L[k]['dur'], text=L[k]['text']) for k in NEW})
json.dump(tts, open(os.path.join(EXP, 'ex9v3_tts.json'), 'w'), indent=1)

# 2. the cut pack: the eight new lines and the four recorded lines newly cut for explainer #9 (FLAC, 48 kHz mono)
for k in NEW + REC:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(EX9, L[k]['file']), '-c:a', 'flac', os.path.join(PACK, f'v_{k}.flac')], check=True)
json.dump({k: L[k] for k in NEW + REC}, open(os.path.join(PACK, 'lines.json'), 'w'), indent=1)
json.dump({k: W[k] for k in NEW + REC}, open(os.path.join(PACK, 'words.json'), 'w'))

# 3. sentences.tsv: explainer #9's eight V3 lines, on their word times
tsv_p = os.path.join(BANK, 'sentences.tsv'); tsv = open(tsv_p).read()
assert 'explainers/ex9v3.flac' not in tsv
rows, ww, i = [], raw['original_words'], 0
for k in NEW:
    seg = ww[i:i + len(toks(L[k]['text']))]; i += len(seg); sh = ALIGN.get(k, 0.0)
    assert [re.sub(r"[^a-z0-9']", '', w['text'].lower()) for w in seg] == [t.lower() for t in toks(L[k]['text'])], k
    rows.append(f"explainers/ex9v3.flac\t{seg[0]['start_time'] + sh:.3f}\t{seg[-1]['end_time'] + sh:.3f}\t{L[k]['text']}")
assert i == len(ww)
open(tsv_p, 'w').write(tsv.rstrip('\n') + '\n' + '\n'.join(rows) + '\n')

# 4. the pack's README
open(os.path.join(PACK, 'README.md'), 'w').write("""# Explainer #9 working pack (what copying really means: the cooking class), 13 Nov 2026

MTG approved eight new lines on 13 Nov 2026 ("Yes, record (1 credit)"). One request in **MTG Master Voice V3**
(`65f1b9ff3f1e418496de5715a801e7dd`), no model or engine override, one paragraph per line, 1 credit (44 before, 43 after,
resets 3 Dec 2026). The whole take is `../ex9v3.flac` with its text (`../ex9v3.txt`) and HeyGen's reply with word times
and the cut points (`../ex9v3_tts.json`).

The eight new lines, cut with their edges snapped to the silence and levelled to -18.5 LUFS like MTG's other V3 lines:
`v_nhook`, `v_ncook`, `v_ntwist`, `v_npot`, `v_nauto`, `v_nyours`, `v_nlid`, `v_nrecap`. HeyGen's word times for nauto,
nyours, nlid and nrecap ran 0.19 to 0.21 s ahead of the audio; `words.json` here already has them shifted. Useful on
their own: "You don't pick the trades.", "You pick the strategy, how much to put in, and when to stop." (the How it works
page's own sentence), "With your investor password, you can watch every trade, read-only." (said "reed only", measured).

Four recorded lines newly cut for explainer #9 (0 credits): `v_deposit` ("Your deposit goes into an M T five account at
TAG Markets, in your name.") and `v_copyx` ("Then you connect a strategy through CopyX.") from the 5 Checks take o1 on
its forced-alignment word times, and `v_terms` ("Read the terms.") and `v_perf` ("A thirty percent performance fee, taken
from profits only.") from `signup-training/t3.mp3`: one stretch split in its own silence, so play `v_perf` straight after
`v_terms` with no gap.

Every line was checked with faster-whisper ("Your pot" reads as "Your part" when cut on its own and as "pot" after the
cooking class line). `lines.json` and `words.json` hold the cut points and word times. Decode each to `v_<key>.wav`
(48 kHz mono) next to `tools/jetup-explainers/ex9/`:

    for f in v_*.flac; do ffmpeg -v error -y -i "$f" -ar 48000 -ac 1 "${f%.flac}.wav"; done

The Myfxbook line, the greeting, the close, the fair-play lines and the signature ending come from `../ex4-pack/`.
Facts: `tools/learning-system/jetup-facts.md`.
""")
print('banked:', len(NEW), 'new lines,', len(REC), 'recorded cuts,', len(rows), 'index rows')
