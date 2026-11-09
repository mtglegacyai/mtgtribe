"""Check every page's social preview tags (MTG, 9 Nov 2026): python3 tools/og/check_og.py
Image exists, is a 1200x630 JPEG under 300 KB (WhatsApp skips bigger ones), the declared size matches, twitter:image
is the same image, og:url matches the canonical, and no two pages share an image (redirect links may reuse the
preview of the page they open)."""
import glob, html, os, re
from PIL import Image
SITE = 'https://mtgtribe.com'
pages = sorted(p for p in glob.glob('**/index.html', recursive=True) if not p.startswith(('tools/', 'node_modules/')) and '/_build/' not in p)
seen, bad = {}, 0
for p in pages:
    s = open(p).read()
    tags = {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<meta (?:property|name)="([^"]+)" content="([^"]*)"', s)}
    redirect = 'http-equiv="refresh"' in s
    img = tags.get('og:image', ''); probs = []
    if not img: probs.append('no og:image')
    else:
        f = img.split('?')[0][len(SITE) + 1:] if img.startswith(SITE) else None
        if not f or not os.path.exists(f): probs.append('image file missing')
        else:
            im = Image.open(f); kb = os.path.getsize(f) / 1024
            if im.format != 'JPEG': probs.append(im.format)
            if (str(im.size[0]), str(im.size[1])) != (tags.get('og:image:width'), tags.get('og:image:height')): probs.append(f'declared {tags.get("og:image:width")}x{tags.get("og:image:height")} real {im.size}')
            if im.size != (1200, 630) and 'JetUpZoom' not in p: probs.append(f'size {im.size}')
            if kb > 300: probs.append(f'{kb:.0f} KB')
        if tags.get('twitter:image') != img: probs.append('twitter:image differs')
        if tags.get('twitter:card') != 'summary_large_image': probs.append('twitter card')
        if not tags.get('og:image:alt'): probs.append('no alt')
        key = img.split('?')[0]
        if key in seen and not redirect: probs.append('same image as ' + seen[key])
        if not redirect: seen.setdefault(key, p)
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if canon and tags.get('og:url') and tags['og:url'] != canon.group(1) and not redirect: probs.append('og:url != canonical')
    if p == '404.html': continue
    print(('OK  ' if not probs else 'BAD ') + p.ljust(58) + img.split('/')[-1].split('?')[0] + ('  ' + '; '.join(probs) if probs else ''))
    bad += bool(probs)
print(f'{len(pages)} pages, {bad} with a problem')
