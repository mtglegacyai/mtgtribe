"""The ClickBaitPays presentation slides as a free PDF download (MTG, 22 Nov 2026: "Place the slide deck where those who would
like to download it in PDF, and publish that too").

python3 cbp/_build/deck.py [path/to/ClickBaitPays PowerPoint.pptx]     (default /home/user/cbp-deck/deck.pptx, from MTG's Drive)

Each slide of the deck is one picture; they become the pages of the PDF, 16:9, in order, except the referral slide ("Share &
Earn", slide 9): it shows the old rule (10% of campaign completion value), and since 1 Oct 2026 the official FAQ says 10% of
the purchase price, paid at once, as the guide says. A last page adds the way forward: the guide, MTG's Join link with the
fair-play line, tappable. Writes cbp/_build/deck/clickbaitpays-presentation-slides.pdf and deck-cover.webp (the first slide),
which the builder puts on the How It Works and Compensation Plan pages of both addresses.
"""
import base64, io, os, re, subprocess, sys, tempfile, zipfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build                                    # MTG's Join link and the guide's address, from the one source of truth

SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/user/cbp-deck/deck.pptx'
OUT = os.path.join(HERE, 'deck')
PDF = 'clickbaitpays-presentation-slides.pdf'
SKIP = {9}                                       # the out-of-date referral slide
LOGO = os.path.join(build.BRAND, 'clickbaitpays-logo-disc-video.png')


def slides():
    z = zipfile.ZipFile(SRC)
    n = len([x for x in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', x)])
    out = []
    for i in range(1, n + 1):
        rel = z.read(f'ppt/slides/_rels/slide{i}.xml.rels').decode()
        img = re.findall(r'Target="\.\./media/([^"]+)"', rel)[0]
        out.append((i, Image.open(io.BytesIO(z.read('ppt/media/' + img))).convert('RGB')))
    return out


def jpeg64(im, q=84):
    b = io.BytesIO()
    im.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


def last_page():
    logo = 'data:image/png;base64,' + base64.b64encode(open(LOGO, 'rb').read()).decode()
    guide = build.SITE + build.BASE
    return f'''<section class="pg last"><div class="in">
<img class="logo" src="{logo}" alt="">
<p class="k">CLICKBAITPAYS GUIDE BY MTG</p>
<h1>Got a link? <em>Get it seen.</em></h1>
<p class="lead">Put any program with a link in front of real people who open it, and get paid in USDT to view their ads while it happens.</p>
<div class="row">
 <a class="btn join" href="{build.OWNER['ref']}">Join ClickBaitPays Free</a>
 <a class="btn guide" href="{guide}">Every Step On Video: {build.SITE_LABEL}</a>
</div>
<p class="fair">Free account. Invited by someone else? Please use their link.</p>
<p class="sig">MTG | Your Digital Architect</p>
<p class="risk">An independent guide, not official ClickBaitPays material and not financial advice. You are paid only for the ads you view; nothing is guaranteed.</p>
</div></section>'''


CSS = '''@page{size:13.333in 7.5in;margin:0}*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#080015}body{font-family:Poppins,system-ui,sans-serif;color:#fff}
.pg{width:13.333in;height:7.5in;page-break-after:always;break-after:page;overflow:hidden;position:relative}
.pg>img{width:100%;height:100%;object-fit:contain;display:block;background:#080015}
.last{background:radial-gradient(60% 70% at 50% 40%,rgba(0,229,255,.18),transparent 70%),radial-gradient(50% 60% at 90% 10%,rgba(255,0,255,.18),transparent 70%),#080015}
.last .in{position:absolute;inset:0;display:grid;justify-items:center;align-content:center;gap:16px;text-align:center;padding:0 1in}
.logo{width:1.3in;height:1.3in;border-radius:50%;box-shadow:0 0 0 5px #ffd866,0 0 40px rgba(255,216,102,.5)}
.k{font:800 15px Orbitron,sans-serif;letter-spacing:.2em;color:#00e5ff}
h1{font:900 58px/1.05 Orbitron,sans-serif;text-transform:uppercase}h1 em{font-style:normal;color:#ffd866}
.lead{font-size:20px;line-height:1.5;max-width:9in;color:#e6e2f2}
.row{display:flex;gap:18px;margin-top:6px}
.btn{display:inline-block;padding:16px 30px;border-radius:999px;font:800 20px Poppins,sans-serif;text-decoration:none}
.join{background:linear-gradient(90deg,#00e5ff,#00ffee);color:#05000e;box-shadow:0 0 30px rgba(0,229,255,.5)}
.guide{border:2px solid #ff4dff;color:#fff;background:rgba(255,0,255,.12)}
.fair{font-size:16px;color:#cfc8e6}.sig{font:800 18px Orbitron,sans-serif;color:#ffd866;margin-top:6px}
.risk{font-size:12px;color:#9a93b5;max-width:9in}'''


def main():
    os.makedirs(OUT, exist_ok=True)
    pages = slides()
    first = pages[0][1]
    first.resize((640, round(640 * first.height / first.width)), Image.LANCZOS).save(os.path.join(OUT, 'deck-cover.webp'), 'WEBP', quality=82, method=6)
    body = ''.join(f'<section class="pg"><img src="{jpeg64(im)}" alt="Slide {i}"></section>' for i, im in pages if i not in SKIP) + last_page()
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>ClickBaitPays: the presentation slides</title>'
            f'<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@800;900&family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body>{body}</body></html>')
    tmp = tempfile.mkdtemp()
    hp = os.path.join(tmp, 'deck.html')
    open(hp, 'w', encoding='utf-8').write(html)
    js = os.path.join(tmp, 'pdf.js')
    out = os.path.join(OUT, PDF)
    open(js, 'w').write(f'''const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}',{{waitUntil:'networkidle'}});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await p.pdf({{path:'{out}',width:'13.333in',height:'7.5in',printBackground:true,preferCSSPageSize:true}});await b.close();}})();''')
    subprocess.run(['node', js], check=True)
    n = len([1 for i, _ in pages if i not in SKIP]) + 1
    print(f'{PDF}: {n} pages, {os.path.getsize(out) / 1e6:.1f} MB; cover deck-cover.webp')


if __name__ == '__main__':
    main()
