# Body sound effects of a tutorial part, mapped onto the training's palette: whoosh on the title, every step and every
# section card; tick on every list row, tick-off and label chip; click on every demonstrated tap.
import json, os, sys
D = sys.argv[1]; MC = json.load(open(os.path.join(D, 'mixcues.json'))); C = MC['cues']; K = json.load(open(os.path.join(D, 'kitcues.json')))
kit0 = K['cues']['T_LINKS']
wh = [0.15] + [s - 0.1 for s in MC['steps']] + [v[0] - 0.1 for k, v in MC['scenes'].items() if k in ('tip', 'tip2', 'mail', 'cam1', 'cam2', 'recap', 'next') and 0.5 < v[0] < kit0]
tick = [t - 0.05 for t in C.get('plan_in', [])] + [t - 0.03 for t in C.get('plan_tick', [])] + [t - 0.1 for t in C.get('nb', [])] + list(MC.get('chips', []))
click = list(MC.get('taps', []))
for k in ('linktap', 'mailtap'):
    if k in C and 0 < C[k] < kit0 and C[k] not in click: click.append(C[k])
body = dict(whoosh=sorted(t for t in wh if 0 <= t < kit0), tick=sorted(t for t in tick if 0 <= t < kit0), click=sorted(t for t in click if 0 <= t < kit0), pop=[])
json.dump(body, open(os.path.join(D, 'sfx_body.json'), 'w'))
print(D, {k: len(v) for k, v in body.items()})
