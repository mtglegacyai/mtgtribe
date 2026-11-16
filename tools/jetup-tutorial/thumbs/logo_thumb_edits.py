# Point the tutorial videos at the JetUP-logo thumbnails (MTG, 8 Nov 2026). Usage: python3 logo_thumb_edits.py <repo>
import sys, os
R = sys.argv[1]
p = os.path.join(R, 'jetup/_build/layout.py'); s = open(p).read()
for a, b in (("cover-tutorial-part-1-v2.", "cover-tutorial-part-1-v3."), ("cover-tutorial-part-2.", "cover-tutorial-part-2-v2."),
             ("cover-tutorial-part-3.", "cover-tutorial-part-3-v2.")):
    assert s.count(a) == 2, (a, s.count(a))
    s = s.replace(a, b)
open(p, 'w').write(s); print('posters updated in', R)
