"""Validate social preview tags on every built page: python3 og/validate.py [root]"""
import glob, os, re, sys, html
from PIL import Image
R = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/site/out/prod'
SITE = 'https://mtgtribe.com'
pages = sorted(glob.glob(R + '/altruva/**/index.html', recursive=True)) + [R + '/index.html', R + '/group/index.html']
need = ['og:title', 'og:description', 'og:url', 'og:image', 'og:image:secure_url', 'og:image:type', 'og:image:width', 'og:image:height',
        'og:image:alt', 'og:type', 'og:site_name', 'twitter:card', 'twitter:title', 'twitter:description', 'twitter:image']
bad = 0; seen = {}
for p in pages:
    s = open(p).read()
    tags = {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<meta (?:property|name)="([^"]+)" content="([^"]*)"', s)}
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    rel = p[len(R):]
    miss = [n for n in need if n not in tags]
    img = tags.get('og:image', '')
    f = R + img.split('?')[0][len(SITE):] if img.startswith(SITE) else None
    problems = []
    if miss: problems.append('missing ' + ','.join(miss))
    if not img.startswith('https://'): problems.append('image not absolute https')
    if f and not os.path.exists(f): problems.append('image file missing ' + f)
    if f and os.path.exists(f):
        im = Image.open(f); kb = os.path.getsize(f) / 1024
        if im.size != (1200, 630) or im.format != 'JPEG': problems.append(f'image {im.size} {im.format}')
        if kb > 300: problems.append(f'image {kb:.0f} KB')
    if tags.get('twitter:card') != 'summary_large_image': problems.append('twitter card')
    if canon and tags.get('og:url') != canon.group(1): problems.append('og:url != canonical')
    if tags.get('twitter:image') != img: problems.append('twitter:image differs')
    key = img.split('/')[-1].split('?')[0]
    if key in seen and key != 'og-altruva-guide.jpg': problems.append(f'same image as {seen[key]}')
    seen.setdefault(key, rel)
    print(('OK  ' if not problems else 'BAD ') + f'{rel:58s} {key:22s} ' + '; '.join(problems))
    bad += bool(problems)
print(f'{len(pages)} pages, {bad} with problems')
