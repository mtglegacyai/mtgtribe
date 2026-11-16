"""Static scan of the built /bw pages (python3 tools/qa/bw-static-scan.py): broken links and anchors, missing files, unclosed tags,
duplicate ids, pictures without alt or size, meta and social tags, JSON-LD, heading order, buttons without a name, dashes."""
import os, re, sys, json, html
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import glob
pages = sorted(os.path.relpath(f, ROOT) for f in glob.glob(ROOT + '/bw/**/index.html', recursive=True) + [ROOT + '/bwcopy/index.html'] if '/_build/' not in f)
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.tags=[]; s.ids={}; s.links=[]; s.imgs=[]; s.stack=[]; s.err=[]; s.meta={}; s.ld=[]; s._ld=False; s.h=[]; s.btn=[]; s._cur=None; s.text=[]; s.inbody=False
    def handle_starttag(s, tag, attrs):
        a=dict(attrs); s.tags.append((tag,a))
        if 'id' in a: s.ids[a['id']]=s.ids.get(a['id'],0)+1
        if tag in('a','link') and 'href' in a: s.links.append((tag,a['href'],a))
        if tag in('script','img','source','video','audio','iframe') and a.get('src'): s.links.append((tag,a['src'],a))
        if tag=='img':
            s.imgs.append(a)
            for part in (a.get('srcset') or '').split(','):
                u=part.strip().split(' ')[0]
                if u: s.links.append(('srcset',u,a))
        if tag=='use' and a.get('href'): s.links.append(('use',a['href'],a))
        if tag=='meta': s.meta[a.get('name') or a.get('property') or a.get('http-equiv') or ('charset' if 'charset' in a else '?')]=a.get('content', a.get('charset'))
        if tag=='script' and a.get('type')=='application/ld+json': s._ld=True; s.ld.append('')
        if re.fullmatch(r'h[1-6]',tag): s.h.append(int(tag[1]))
        if tag in ('button','a'): s._cur=[tag,a,'']; 
        if tag=='body': s.inbody=True
        if tag not in VOID: s.stack.append(tag)
    def handle_endtag(s, tag):
        if tag=='script': s._ld=False
        if tag in ('button','a') and s._cur: s.btn.append(tuple(s._cur)); s._cur=None
        if tag in VOID: return
        if not s.stack or s.stack[-1]!=tag:
            if tag in s.stack:
                while s.stack and s.stack[-1]!=tag: s.err.append(f'unclosed <{s.stack.pop()}> before </{tag}> at line {s.getpos()[0]}')
                s.stack.pop()
            else: s.err.append(f'stray </{tag}> at line {s.getpos()[0]}')
        else: s.stack.pop()
    def handle_data(s, d):
        if s._ld: s.ld[-1]+=d
        if s._cur: s._cur[2]+=d
        if s.inbody and s.stack and s.stack[-1] not in('script','style'): s.text.append(d)
probs=[]; allids={}; parsed={}
for pg in pages:
    src=open(f'{ROOT}/{pg}',encoding='utf-8').read(); p=P(); p.feed(src); parsed[pg]=(p,src)
def exists(path): return os.path.exists(path) or os.path.exists(path.rstrip('/')+'/index.html')
for pg,(p,src) in parsed.items():
    base=os.path.dirname(pg); E=lambda m: probs.append(f'{pg}: {m}')
    for e in p.err: E('HTML '+e)
    if p.stack and p.stack!=[]: E('HTML left open: '+','.join(p.stack[-5:]))
    for i,n in p.ids.items():
        if n>1: E(f'duplicate id "{i}" x{n}')
    for tag,u,a in p.links:
        if u.startswith(('http://','https://','mailto:','tel:','data:','whatsapp:','javascript:')):
            if u.startswith('http') and tag=='a' and a.get('target')=='_blank' and 'noopener' not in (a.get('rel') or ''): E(f'external link without rel=noopener: {u[:60]}')
            if u.startswith('http://'): E('http link: '+u[:70])
            continue
        if u.startswith('#'):
            if tag=='use':
                if u[1:] not in p.ids: E('icon not in sprite: '+u)
            elif len(u)>1 and u[1:] not in p.ids: E('anchor without target: '+u)
            continue
        pr=urlparse(u); path=unquote(pr.path)
        tgt=os.path.normpath(os.path.join(ROOT, path.lstrip('/')) if path.startswith('/') else os.path.join(ROOT,base,path))
        if not exists(tgt): E(f'missing file: {u}'); continue
        if pr.fragment and tag=='a':
            t=tgt if tgt.endswith('.html') else tgt.rstrip('/')+'/index.html'
            rel=os.path.relpath(t,ROOT)
            if rel in parsed and pr.fragment not in parsed[rel][0].ids: E(f'link to missing anchor: {u}')
    for a in p.imgs:
        if 'alt' not in a: E('img without alt: '+(a.get('src') or '')[-50:])
        if not a.get('width') or not a.get('height'): E('img without width/height: '+(a.get('src') or '')[-50:])
    m=p.meta
    title=re.search(r'<title>(.*?)</title>',src,re.S); 
    if not title: E('no <title>')
    for k in ('description','viewport','og:title','og:description','og:image','og:url','twitter:card'):
        if not m.get(k): E('meta missing: '+k)
    if 'rel="canonical"' not in src: E('no canonical link')
    if m.get('description') and not (70<=len(m['description'])<=170): E(f'description length {len(m["description"])}')
    if not re.search(r'<html[^>]* lang="en', src): E('no lang on <html>')
    for i,l in enumerate(p.ld):
        try: json.loads(l)
        except Exception as e: E(f'JSON-LD {i} does not parse: {e}')
    if p.h.count(1)!=1: E(f'{p.h.count(1)} h1 headings')
    for a,b in zip(p.h,p.h[1:]):
        if b>a+1: E(f'heading jumps h{a} to h{b}'); break
    for tag,a,t in p.btn:
        if not (t.strip() or a.get('aria-label') or a.get('title')): 
            E(f'{tag} without a name: {str(a)[:80]}')
        if tag=='button' and 'type' not in a: E('button without type: '+(t.strip() or str(a))[:50])
    txt=html.unescape(' '.join(p.text))
    for ch,name in (('—','em dash'),('–','en dash')):
        if ch in src: E(f'{name} in page x{src.count(ch)}')
    if re.search(r'lorem ipsum|TODO|FIXME|undefined|NaN\b', txt): E('placeholder text: '+re.search(r'.{20}(lorem ipsum|TODO|FIXME|undefined|NaN\b).{20}', txt).group(0))
print(len(pages),'pages,',len(probs),'findings')
import collections
c=collections.Counter(re.sub(r'^[^:]+: ','',x) for x in probs)
for k,v in c.most_common(40): print(v,k[:150])
for x in probs: print(' ', x)
