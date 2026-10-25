"""Search and AI readiness check for the built site (out/prod): run after every build.
Checks titles, descriptions, canonical vs og:url, robots, one h1, structured data, sitemap URLs, internal links, crawl files."""
import glob, json, os, re, sys, xml.dom.minidom
ROOT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/site/out/prod'
SITE = 'https://mtgtribe.com'
bad, rows = [], []


def path_of(url):
    p = url.replace(SITE, '').split('?')[0].split('#')[0]
    f = ROOT + p + ('index.html' if p.endswith('/') else '')
    return f


for f in sorted(glob.glob(ROOT + '/**/*.html', recursive=True)):
    rel = f.replace(ROOT, '')
    s = open(f, encoding='utf-8').read()
    hd = s[:s.find('</head>')]
    rob = re.search(r'<meta name="robots" content="([^"]+)"', hd)
    if rob and 'noindex' in rob.group(1):
        continue
    t = re.search(r'<title>(.*?)</title>', hd, re.S); d = re.search(r'<meta name="description" content="([^"]*)"', hd)
    can = re.search(r'<link rel="canonical" href="([^"]+)"', hd); ogu = re.search(r'<meta property="og:url" content="([^"]+)"', hd)
    t = t.group(1) if t else ''; d = d.group(1) if d else ''
    if rel == '/index.html':
        if not can or can.group(1) != SITE + '/altruva/':
            bad.append('root canonical should point at /altruva/')
        continue
    if len(t) > 60: bad.append(f'{rel}: title {len(t)} chars')
    if not 110 <= len(d) <= 160: bad.append(f'{rel}: description {len(d)} chars')
    if not can or not ogu or can.group(1) != ogu.group(1): bad.append(f'{rel}: canonical and og:url differ')
    if can and not os.path.exists(path_of(can.group(1))): bad.append(f'{rel}: canonical file missing')
    if 'max-snippet:-1' not in (rob.group(1) if rob else ''): bad.append(f'{rel}: robots meta')
    if len(re.findall(r'<h1[\s>]', s)) != 1: bad.append(f'{rel}: h1 count')
    if '_code' in s: bad.append(f'{rel}: _code left in data')
    types = []
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        g = json.loads(m)
        for n in g.get('@graph', [g]):
            types.append(n['@type'])
            for k, v in n.items():
                if isinstance(v, str) and ('—' in v or '–' in v): bad.append(f'{rel}: dash in {n["@type"]}.{k}')
            if n['@type'] == 'VideoObject':
                if not os.path.exists(path_of(n['contentUrl'])): bad.append(f'{rel}: video file missing {n["contentUrl"]}')
                if not os.path.exists(path_of(n['thumbnailUrl'][0])): bad.append(f'{rel}: thumbnail missing')
    for href in re.findall(r'href="(/altruva/[^"#?]*)', s):
        if not os.path.exists(path_of(SITE + href)): bad.append(f'{rel}: broken link {href}')
    rows.append((rel, len(t), len(d), sorted(set(types))))

# sitemaps
for sm in ('/sitemap.xml', '/altruva/sitemap.xml'):
    xml.dom.minidom.parse(ROOT + sm)
locs = re.findall(r'<loc>([^<]+)</loc>', open(ROOT + '/altruva/sitemap.xml').read())
for u in locs:
    if not os.path.exists(path_of(u)): bad.append(f'sitemap URL missing: {u}')
for u in re.findall(r'<video:(?:content|thumbnail)_loc>([^<]+)<', open(ROOT + '/altruva/sitemap.xml').read()):
    if not os.path.exists(path_of(u)): bad.append(f'sitemap video file missing: {u}')
indexed = {r[0] for r in rows}
for u in locs:
    if u.replace(SITE, '') + 'index.html' not in indexed: bad.append(f'sitemap URL not an indexable page: {u}')
# crawl files
rb = open(ROOT + '/robots.txt').read()
if 'Disallow: /\n' in rb: bad.append('robots blocks the site')
for need in ('Sitemap: https://mtgtribe.com/sitemap.xml', 'OAI-SearchBot', 'Claude-SearchBot', 'PerplexityBot', 'Googlebot', 'Bingbot'):
    if need not in rb: bad.append(f'robots missing {need}')
for f in ('llms.txt', 'llms-full.txt'):
    s = open(ROOT + '/' + f).read()
    if '—' in s or '–' in s: bad.append(f'dash in {f}')
keys = [f for f in os.listdir(ROOT) if re.fullmatch(r'[0-9a-f]{32}\.txt', f)]
if len(keys) != 1 or open(ROOT + '/' + keys[0]).read() != keys[0][:-4]: bad.append('IndexNow key file')
print(f'{len(rows)} indexable pages, {len(locs)} sitemap URLs, '
      f'{open(ROOT + "/altruva/sitemap.xml").read().count("<video:video>")} sitemap videos')
print('\n'.join(bad) if bad else 'SEO CHECK OK')
