#!/usr/bin/env python3
"""Named cue times for a video, from its word timings: scenes are written against names, not seconds.

  python3 scripts/make_cues.py public/videos/05/words.json public/videos/05/anchors.json public/videos/05/cues.json

anchors.json: {"name": "phrase"} or {"name": ["phrase", occurrence]} (occurrence 1 = first time the phrase is said) or
{"name": ["phrase", occurrence, "end"]} for the END of the phrase. Each cue is the start of the phrase's first word.
"""
import json, re, sys
words = json.load(open(sys.argv[1]))['words']
anchors = json.load(open(sys.argv[2]))
norm = lambda s: re.sub(r"[^\w']", '', s).lower()
toks = [norm(w['text']) for w in words]
cues = {}
for name, spec in anchors.items():
    if isinstance(spec, str):
        phrase, occ, edge = spec, 1, 'start'
    else:
        phrase, occ, edge = spec[0], (spec[1] if len(spec) > 1 else 1), (spec[2] if len(spec) > 2 else 'start')
    p = [norm(t) for t in phrase.split(' ')]
    hits = [i for i in range(len(toks) - len(p) + 1) if toks[i:i + len(p)] == p]
    if len(hits) < occ:
        sys.exit(f'cue "{name}": phrase "{phrase}" (occurrence {occ}) not found in the words')
    i = hits[occ - 1]
    cues[name] = words[i]['start'] if edge == 'start' else words[i + len(p) - 1]['end']
cues['END'] = words[-1]['end']
json.dump(cues, open(sys.argv[3], 'w'), indent=1)
print(len(cues), 'cues ->', sys.argv[3])
