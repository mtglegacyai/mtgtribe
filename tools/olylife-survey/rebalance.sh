#!/bin/bash
# kill running range workers, split the frames still missing (plus an optional forced list) over 4 list workers
cd "$(dirname "$0")"
pkill -f "render.js range"; pkill -f "render.js list"; sleep 1
python3 - "$@" <<'PY'
import os, json, sys
N = round(json.load(open('lines_out.json'))['T'] * 30)
have = {int(f[1:6]) for f in os.listdir('frames') if f.endswith('.jpg')}
force = set()
for a in sys.argv[1:]:
    x, y = map(int, a.split('-')); force |= set(range(x, y))
todo = sorted((set(range(N)) - have) | force)
# interleave so each worker gets the same mix of heavy and light frames
for i in range(4): json.dump(todo[i::4], open(f'todo{i}.json', 'w'))
print('todo', len(todo))
PY
for i in 0 1 2 3; do nohup node render.js list todo$i.json frames > l$i.log 2>&1 & done
