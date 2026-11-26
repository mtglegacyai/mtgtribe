"""Private preview of a few mtgtribe.com pages: copies them with the files they use into a folder with relative links.

Usage: python3 -I tools/qa/preview_bundle.py <repo> <out dir> "index.html,jetup/index.html,bw/dashboard/index.html"
Then add a guide page as <out>/index.html and publish it with every other file as a supporting file (README: Private preview link)."""
import os, re, shutil, posixpath, sys
REPO, OUT = sys.argv[1], sys.argv[2]
PAGES = sys.argv[3].split(',')
LIVE = 'https://mtgtribe.com'
SKIP_EXT = ('.mp4', '.webm', '.mov', '.ics', '.pdf', '.zip')
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
included, todo_css, skipped = set(), [], set()
page_set = {('/' + p).rsplit('index.html', 1)[0] for p in PAGES}   # '/jetup/' etc
def rel(from_file, target):  # both repo-relative paths without leading slash
    return posixpath.relpath(target, posixpath.dirname(from_file) or '.')
def resolve(from_file, url):
    if not url.startswith('/') or url.startswith('//'): return None
    path, _, frag = url.partition('#'); path = path.split('?')[0]
    if path in page_set: return rel(from_file, 'site' + path + 'index.html') + ('#' + frag if frag else '')
    fs = REPO + path
    if path.endswith('/') or os.path.isdir(fs) or path.lower().endswith(SKIP_EXT) or not os.path.isfile(fs):
        if path.lower().endswith(SKIP_EXT): skipped.add(path)
        return LIVE + url
    included.add(path)
    if path.endswith('.css'): todo_css.append(path)
    return rel(from_file, 'site' + path)
ATTR = re.compile(r'''((?:src|href|poster|data-src|data-poster|data-bg|data-index|action)\s*=\s*)(["'])(/[^"']*)\2''')
SRCSET = re.compile(r'''(srcset\s*=\s*)(["'])([^"']*)\2''')
CSSURL = re.compile(r'''url\(\s*(["']?)(/[^"')]+)\1\s*\)''')
def fix_html(page, html):
    me = 'site/' + page
    html = ATTR.sub(lambda m: m.group(1) + m.group(2) + (resolve(me, m.group(3)) or m.group(3)) + m.group(2), html)
    def ss(m):
        parts = []
        for item in m.group(3).split(','):
            bits = item.strip().split()
            if bits and bits[0].startswith('/'): bits[0] = resolve(me, bits[0]) or bits[0]
            parts.append(' '.join(bits))
        return m.group(1) + m.group(2) + ', '.join(parts) + m.group(2)
    html = SRCSET.sub(ss, html)
    html = CSSURL.sub(lambda m: 'url(' + m.group(1) + (resolve(me, m.group(2)) or m.group(2)) + m.group(1) + ')', html)
    return html
for page in PAGES:
    html = open(REPO + '/' + page, encoding='utf-8').read()
    os.makedirs(os.path.dirname(OUT + '/site/' + page), exist_ok=True)
    open(OUT + '/site/' + page, 'w', encoding='utf-8').write(fix_html(page, html))
done = set()
while todo_css:
    c = todo_css.pop()
    if c in done: continue
    done.add(c)
    css = open(REPO + c, encoding='utf-8').read()
    me = 'site' + c
    css = CSSURL.sub(lambda m: 'url(' + m.group(1) + (resolve(me, m.group(2)) or m.group(2)) + m.group(1) + ')', css)
    os.makedirs(os.path.dirname(OUT + '/site' + c), exist_ok=True)
    open(OUT + '/site' + c, 'w', encoding='utf-8').write(css)
for f in sorted(included):
    if f.endswith('.css'): continue
    os.makedirs(os.path.dirname(OUT + '/site' + f), exist_ok=True)
    shutil.copy(REPO + f, OUT + '/site' + f)
tot = sum(os.path.getsize(os.path.join(d, x)) for d, _, fs in os.walk(OUT) for x in fs)
big = sorted(((os.path.getsize(os.path.join(d, x)), os.path.join(d, x).replace(OUT + '/', '')) for d, _, fs in os.walk(OUT) for x in fs), reverse=True)[:6]
print(f'{len(PAGES)} pages, {len(included)} files, {tot/1e6:.1f} MB total; skipped (left on live site): {sorted(skipped)}')
for s, n in big: print(f'  {s/1e6:6.2f} MB {n}')
