"""Build the ALTRUVA guide: python3 build.py  ->  out/prod (repo layout) and out/preview (artifact layout)."""
import hashlib, os, re, shutil, subprocess, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import core
from config import *
from pages_learn import p_home, p_fit, p_diff, p_split, p_pkg, p_leg, p_wl, p_match, p_ranks, p_wd
from pages_do import (p_join, p_tut, p_exp, p_c_wd, p_c_wl, p_c_m, p_c_zar, p_faq, faq_ld, p_gloss, p_safe, p_dl,
                      p_card, p_tribe, p_disc)
from pages_land import landing

ROOT = '/home/claude/site'
SRC, OUT = ROOT + '/src', ROOT + '/out'
ASSETS = '/home/claude/altruva-assets'
SCR = '/tmp/claude-0/-home-claude/dc91e5da-c02d-54a0-a639-05ec78f3d408/scratchpad'

PAGES = {
    # key: (title, description, body fn, extra ld fn)
    'home': ('ALTRUVA Dashboard: start here', 'Your route through the independent ALTRUVA guide: 13 videos in order, your progress, and how to use the dashboard.', p_home, None),
    'fit': ('Is ALTRUVA right for me? An honest fit check', 'Five honest questions, who ALTRUVA suits and who it does not, and where the money really comes from.', p_fit, None),
    'diff': ('What makes ALTRUVA different', 'If a smart contract platform let you down before: what is different about ALTRUVA, what is the same, and the questions to ask any platform.', p_diff, None),
    'split': ('Where every ALTRUVA dollar goes: the 100% split', 'How every ALTRUVA package is shared: 40% global leg, 25% working levels, 25% level matching, 5% ranks, 5% Lucky Tickets.', p_split, ['e1']),
    'pkg': ('ALTRUVA packages: Starter, Builder, Elite', 'Compare ALTRUVA Starter $25, Builder $50 and Elite $100: global leg window, Lucky Tickets, ranks, and your shopping list.', p_pkg, None),
    'leg': ('ALTRUVA global leg explained (40%)', 'How the ALTRUVA global leg pays 1% per member inside your window of 10, 15 or 20 seats up and down.', p_leg, ['e2']),
    'wl': ('ALTRUVA working levels explained (25%)', 'ALTRUVA working levels 1 to 9: 10%, 4%, 2% and 1% rates, and how your directs open each group of levels.', p_wl, ['e3']),
    'match': ('ALTRUVA level matching explained (25%)', 'How ALTRUVA level matching works: the smaller side, the daily 25% pool and the real day 22 rate per unit.', p_match, ['e4']),
    'ranks': ('ALTRUVA ranks and Lucky Tickets explained', 'Nexus and Legacy Crown ranks, and how the ALTRUVA Lucky Ticket draw shares 4,000 USDT among 250 tickets.', p_ranks, ['e5']),
    'wd': ('ALTRUVA withdraw and reinvest explained', 'How ALTRUVA withdrawals split 50/50, 60/40 or 70/30 by total deposit, and why you claim first.', p_wd, ['e6']),
    'join': ('How to join ALTRUVA step by step with SafePal', 'Join ALTRUVA in five steps with SafePal: set up the wallet, get USDT and BNB, copy the sign-up link, join, and tour the app.', p_join, None),
    'tut': ('ALTRUVA tutorial videos', 'Seven step-by-step ALTRUVA tutorials: SafePal setup, funding, joining, claiming a prize, withdrawing and cashing out to your bank.', p_tut, TUT),
    'exp': ('ALTRUVA explainer videos', 'Six animated ALTRUVA explainers: the 100% split, global leg, working levels, level matching, ranks and Lucky Tickets, withdraw and reinvest.', p_exp, EXP),
    'c-wd': ('ALTRUVA Withdraw Split Calculator', 'Free ALTRUVA withdraw split calculator: see what goes to your wallet and what is reinvested, by total deposit.', p_c_wd, None),
    'c-wl': ('ALTRUVA Working Level Calculator', 'Free ALTRUVA working level calculator for levels 1 to 9, with open and closed levels by number of directs.', p_c_wl, None),
    'c-m': ('ALTRUVA Matching Calculator', 'Free ALTRUVA level matching calculator: smaller side times the daily rate, with a tool to work out the rate.', p_c_m, None),
    'c-zar': ('USDT to Rand Converter', 'Convert USDT to South African rand with a live rate and your own exchange fees.', p_c_zar, None),
    'faq': ('ALTRUVA FAQ: questions and myths', 'Straight answers to the most common ALTRUVA questions, and the myths checked against the live app.', p_faq, 'faq'),
    'gloss': ('ALTRUVA glossary: crypto words in plain English', 'Smart contract, Web3, renounced, BEP20, gas and more, explained in plain English with everyday examples.', p_gloss, None),
    'safe': ('ALTRUVA safety centre', 'Protect your wallet: six safety habits, scam patterns to walk away from, and how to check a smart contract on BscScan.', p_safe, None),
    'dl': ('ALTRUVA downloads: videos, quick guide, share kit', 'Download all 13 ALTRUVA videos, the two-page quick guide PDF, and a share message for WhatsApp.', p_dl, None),
    'card': ('Spend your USDT with a crypto card', 'A shorter road from USDT to spending: a crypto debit card for USDT and USDC on BNB Smart Chain.', p_card, None),
    'tribe': ('Join the MTG TRIBE', 'The MTG TRIBE: a WhatsApp community for action takers. Join the group, WhatsApp MTG, or follow on TikTok.', p_tribe, None),
    'disc': ('Disclaimer', 'This independent ALTRUVA guide is educational, not official and not financial advice. Affiliate links, risk and privacy explained.', p_disc, None),
}


def sh(*a):
    subprocess.run(a, check=True)


# ------------------------------------------------------------------ images
def images(dst):
    from PIL import Image, ImageFilter, ImageDraw, ImageFont
    os.makedirs(dst, exist_ok=True)
    logo = Image.open(ASSETS + '/altruva-logo-horizontal-616.png').convert('RGBA')
    logo.save(dst + '/altruva-logo-horizontal.png', optimize=True)
    for n in (192, 100):
        Image.open(ASSETS + f'/altruva-emblem-{n}.png').convert('RGBA').save(dst + f'/altruva-emblem-{n}.png', optimize=True)
    em = Image.open(ASSETS + '/altruva-emblem-192.png').convert('RGBA')
    em.resize((32, 32), Image.LANCZOS).save(dst + '/favicon-32.png', optimize=True)
    bg = Image.new('RGBA', (180, 180), (1, 8, 27, 255)); e = em.resize((150, 150), Image.LANCZOS); bg.alpha_composite(e, (15, 15))
    bg.convert('RGB').save(dst + '/apple-touch-icon.png', optimize=True)
    em.save(dst + '/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    # MTG's ticket, ID hidden
    t = Image.open(ASSETS + '/mtg-lucky-ticket-won.jpg').convert('RGB')
    box = (18, 44, 206, 92)
    r = t.crop(box).resize((12, 4), Image.BILINEAR).resize((box[2] - box[0], box[3] - box[1]), Image.BILINEAR).filter(ImageFilter.GaussianBlur(6))
    t.paste(r, box); t.save(dst + '/mtg-lucky-ticket-won.webp', quality=86, method=6)
    for f in os.listdir(ROOT + '/img'):
        shutil.copy(ROOT + '/img/' + f, dst + '/' + f)
    og(dst + '/og-altruva-guide.jpg', em)


def og(path, em):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), (1, 8, 27))
    g = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(g)
    d.ellipse((-300, -360, 700, 420), fill=(4, 60, 160)); d.ellipse((760, 300, 1500, 900), fill=(4, 80, 120))
    g = g.filter(ImageFilter.GaussianBlur(160)); im = Image.blend(im, g, .55)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 34):
        for y in range(0, H, 34):
            d.point((x, y), fill=(40, 62, 110))
    F = '/tmp/assets/fonts/'
    orb, mon, mon7 = ImageFont.truetype(F + 'Orbitron-800.ttf', 62), ImageFont.truetype(F + 'Montserrat-800.ttf', 30), ImageFont.truetype(F + 'Montserrat-700.ttf', 26)
    e = em.resize((150, 150), Image.LANCZOS); im.paste(e, (80, 80), e)
    d.text((80, 270), 'See every dollar move', font=orb, fill=(255, 255, 255))
    d.text((80, 345), 'before you move a dollar.', font=orb, fill=(205, 224, 240))
    d.text((80, 440), 'The independent ALTRUVA guide by MTG', font=mon, fill=(238, 189, 92))
    d.text((80, 486), '13 short videos, plain-English pages, 4 calculators', font=mon7, fill=(147, 169, 201))
    # gold route line with stations
    pts = [(80, 575), (330, 575), (430, 545), (700, 545), (800, 575), (1120, 575)]
    d.line(pts, fill=(238, 189, 92), width=8, joint='curve')
    for x, y in pts[1:-1] + [pts[-1]]:
        d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(250, 234, 156), outline=(1, 8, 27), width=4)
    d.text((1120, 520), 'mtgtribe.com/altruva', font=mon7, fill=(205, 224, 240), anchor='rs')
    im.save(path, quality=88, optimize=True, progressive=True)


# ------------------------------------------------------------------ quick guide PDF
def quick_guide(pdf):
    em = 'file://' + ASSETS + '/altruva-emblem-192.png'
    rows = ''.join(f'<tr><td><b>{n}</b></td><td>${p}</td><td>{w} up, {w} down</td><td>{t}</td><td>{r}</td></tr>' for n, p, w, t, r in [
        ('Starter', 25, 10, '1, once 2 directs join in 3 days', 'None'), ('Builder', 50, 15, '1', 'Nexus'), ('Elite', 100, 20, '2', 'Legacy Crown')])
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:O;src:url(file:///tmp/assets/fonts/Orbitron-800.ttf)}}
@font-face{{font-family:M;src:url(file:///tmp/assets/fonts/Montserrat-700.ttf);font-weight:700}}
@font-face{{font-family:M;src:url(file:///tmp/assets/fonts/Montserrat-800.ttf);font-weight:800}}
@font-face{{font-family:M;src:url(file:///tmp/assets/fonts/Montserrat-600.ttf);font-weight:400 600}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}body{{margin:0;font:600 10.5pt/1.5 M,sans-serif;color:#cde0f0;background:#01081b;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;padding:14mm 15mm 22mm;position:relative;overflow:hidden;page-break-after:always;background:radial-gradient(120mm 90mm at 0 0,rgba(4,72,182,.45),transparent),#01081b}}
h1{{font:800 22pt/1.1 O;color:#fff;margin:0}}h2{{font:800 12pt O;color:#eebd5c;margin:0 0 3mm;letter-spacing:.02em}}
.top{{display:flex;gap:6mm;align-items:center;margin-bottom:8mm}}.top img{{width:22mm}}.top p{{margin:2mm 0 0;color:#93a9c9}}
.card{{background:rgba(13,31,74,.75);border:1px solid rgba(120,170,255,.25);border-radius:4mm;padding:4.5mm 6mm;margin-bottom:4.5mm}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt}}th,td{{text-align:left;padding:2mm 2.5mm;border-bottom:1px solid rgba(120,170,255,.18)}}th{{color:#93a9c9;font-size:8.5pt}}td b{{color:#eebd5c}}
.bar{{display:flex;height:11mm;border-radius:3mm;overflow:hidden;margin:2mm 0 3mm;font:800 9pt O;color:#04122e}}.bar span{{display:flex;align-items:center;justify-content:center}}
.leg{{display:grid;grid-template-columns:1fr 1fr;gap:1.5mm 6mm;font-size:9.5pt}}.leg i{{display:inline-block;width:3mm;height:3mm;border-radius:1mm;margin-right:2mm}}
ol,ul{{margin:0;padding-left:5mm}}li{{margin:1.2mm 0}}b{{color:#fff}}
.honest{{border-color:rgba(238,189,92,.5);background:rgba(60,44,10,.45)}}
.foot{{position:absolute;left:15mm;right:15mm;bottom:10mm;font-size:8pt;color:#6a809f;display:flex;justify-content:space-between}}
.sig{{color:#eebd5c;font-weight:800}}.links td{{border:0;padding:1.2mm 0}}.links td:first-child{{color:#93a9c9;width:40mm}}
</style></head><body>
<div class="pg"><div class="top"><img src="{em}"><div><h1>ALTRUVA quick guide</h1><p>Independent guide by MTG 👑 | Your Digital Architect. mtgtribe.com/altruva</p></div></div>
<div class="card"><h2>The packages</h2><table><tr><th>Package</th><th>Price</th><th>Global leg window</th><th>Lucky Tickets</th><th>Rank it unlocks</th></tr>{rows}</table>
<p style="margin:3mm 0 0">Step up one package at a time or go straight to Elite. Each package once, never step down. The top package is $100.</p></div>
<div class="card"><h2>Where every $100 goes</h2><div class="bar"><span style="width:40%;background:#2f9ff9">40</span><span style="width:25%;background:#0ce1f2">25</span><span style="width:25%;background:#eebd5c">25</span><span style="width:5%;background:#8fb3ff"></span><span style="width:5%;background:#faea9c"></span></div>
<div class="leg"><span><i style="background:#2f9ff9"></i><b>$40 global leg:</b> 1% per member in your window</span><span><i style="background:#0ce1f2"></i><b>$25 working levels:</b> 10, 4, 2, 2, 2, 2, 1, 1, 1%</span><span><i style="background:#eebd5c"></i><b>$25 level matching:</b> the daily pool, smaller side</span><span><i style="background:#8fb3ff"></i><b>$5 ranks:</b> Nexus and Legacy Crown pools</span><span><i style="background:#faea9c"></i><b>$5 Lucky Tickets:</b> 4,000 USDT to 250 tickets per draw</span><span>Closed levels stay in the contract.</span></div></div>
<div class="card"><h2>Withdrawals</h2><table><tr><th>Your total deposit</th><th>To your wallet</th><th>Reinvested</th></tr><tr><td>Up to 5,000 USDT</td><td><b>50%</b></td><td>50%</td></tr><tr><td>5,001 to 49,999 USDT</td><td><b>60%</b></td><td>40%</td></tr><tr><td>50,000 USDT and up</td><td><b>70%</b></td><td>30%</td></tr></table>
<p style="margin:3mm 0 0"><b>Claim first, then withdraw.</b> A withdrawal always takes the whole balance. Working level income arrives without a claim. Lucky Ticket prizes go to your wallet in full.</p></div>
<div class="foot"><span>Figures checked against the live app on 24 Oct 2026. The app is always the final word.</span><span>1 of 2</span></div></div>
<div class="pg"><div class="card"><h2>Join in five steps</h2><ol>
<li><b>Set up SafePal</b> and write your recovery phrase on paper. (Tutorial 1)</li>
<li><b>Fund your wallet:</b> BNB on BNB Smart Chain, swap to USDT BEP20, keep $5 to $10 of BNB for fees. (Tutorial 2)</li>
<li><b>Copy the sign-up link</b> of the person who introduced you.</li>
<li><b>Join in SafePal Explore:</b> paste, choose BNB Chain, pick a package, approve and sign. (Tutorial 3)</li>
<li><b>Tour your dashboard</b> so every number makes sense. (Tutorial 7)</li></ol>
<p style="margin:3mm 0 0">Then: claim a prize (Tutorial 4), withdraw to SafePal (Tutorial 5), cash out to your bank (Tutorial 6).</p></div>
<div class="card"><h2>Six safety habits</h2><ul>
<li><b>Never share your recovery phrase.</b> Nobody genuine will ever ask for it.</li>
<li>Copy links only from the person who introduced you, and check it opens altruva.io.</li>
<li>Read every wallet screen before you tap Confirm.</li>
<li>Keep $5 to $10 of BNB for fees.</li>
<li>Only use money you can afford to lose, and withdraw regularly.</li>
<li>Hide balances and addresses before you share a screenshot.</li></ul></div>
<div class="card honest"><h2>The honest part</h2><p style="margin:0">Payouts come from members' packages and reinvestments. No outside revenue is named, so earnings depend on new deposits and are not guaranteed. You can lose what you put in. Learn first, start small if it fits, and judge it by what your own dashboard shows.</p></div>
<div class="card"><h2>Keep learning</h2><table class="links">
<tr><td>Full guide and 13 videos</td><td><b>mtgtribe.com/altruva</b></td></tr>
<tr><td>MTG TRIBE on WhatsApp</td><td><b>mtgtribe.com/group</b></td></tr>
<tr><td>WhatsApp MTG</td><td><b>{WA_NUM}</b> (messages and voice notes)</td></tr>
<tr><td>TikTok</td><td><b>@joinmtgtribe</b></td></tr>
<tr><td>Zoom presentations</td><td>Links are in the ALTRUVA WhatsApp groups. Ask the person who introduced you to add you.</td></tr></table></div>
<p style="font-size:8pt;color:#93a9c9;margin:0">Independent guide, not an official ALTRUVA document. Education only: not financial advice and not a recommendation to join or not to join. MTG is an ALTRUVA member and earns as a sponsor when people join with his link.</p>
<div class="foot" style="position:static;margin-top:3mm"><span class="sig">Let's Get This Crypto! 💪</span><span>2 of 2</span></div></div>
</body></html>'''
    src = SCR + '/quick-guide.html'
    open(src, 'w').write(html)
    js = f'''const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{src}');await p.waitForTimeout(400);await p.pdf({{path:'{pdf}',format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close();}})();'''
    open(SCR + '/qg.js', 'w').write(js)
    sh('node', SCR + '/qg.js')


# ------------------------------------------------------------------ pages
def render(mode, dst):
    core.MODE = mode
    if os.path.exists(dst):
        shutil.rmtree(dst)
    base = dst + ('/altruva' if mode == 'prod' else '')
    os.makedirs(base + '/assets', exist_ok=True)
    for f in ('altruva.css', 'altruva.js'):
        shutil.copy(SRC + '/assets/' + f, base + '/assets/' + f)
        core.HASH['assets/' + f] = hashlib.md5(open(SRC + '/assets/' + f, 'rb').read()).hexdigest()[:8]
    shutil.copytree(OUT + '/_img', base + '/img')
    os.makedirs(base + '/downloads', exist_ok=True)
    shutil.copy(OUT + '/_pdf/altruva-quick-guide-mtg.pdf', base + '/downloads/')
    # landing
    hd, body = landing()
    if mode == 'preview':
        hd = hd.replace('<title>ALTRUVA Guide by MTG: plan, videos and how to join</title>', '<title>ALTRUVA Guide by MTG</title>')
        open(base + '/index.html', 'w').write(core.wrap_doc(hd, body, 'landing', main_page=True))
        # same page as a full document too, for links back from inner pages opened outside the frame
    else:
        open(base + '/index.html', 'w').write(core.wrap_doc(hd, body, 'landing'))
    for key, (title, desc, fn, extra) in PAGES.items():
        here = NAVD[key][1]
        ld = None
        if extra == 'faq':
            ld = faq_ld()
        elif extra:
            ld = core.video_ld(extra, here)
        hd, content = core.dash_page(key, title, desc, fn, ld)
        os.makedirs(base + '/' + here, exist_ok=True)
        open(base + '/' + here + 'index.html', 'w').write(core.wrap_doc(hd, content, 'dashpage'))
    if mode == 'prod':
        # sitemap, robots, short links, case redirect
        urls = [''] + [NAVD[k][1] for k in PAGES]
        sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
            f'<url><loc>{SITE}{BASE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{"1.0" if u == "" else ("0.8" if u == "dashboard/" else "0.6")}</priority></url>\n' for u in urls) + '</urlset>\n'
        open(base + '/sitemap.xml', 'w').write(sm)
        open(dst + '/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}{BASE}sitemap.xml\n')
        redirect(dst + '/group/index.html', WA_GROUP, 'Join the MTG TRIBE on WhatsApp')
        notfound(dst + '/404.html')
        os.makedirs(base + '/media', exist_ok=True)
        for k, v in V.items():
            shutil.copy(ROOT + '/media/' + v['slug'] + '.mp4', base + '/media/')


def redirect(path, to, title):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={to}"><link rel="canonical" href="{to if to.startswith('http') else SITE + to}">
<style>body{{background:#01081b;color:#cde0f0;font:600 16px/1.6 system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0}}a{{color:#eebd5c}}</style>
<script>location.replace({json.dumps(to)})</script></head><body><p>Taking you there. <a href="{to}">Tap here</a> if nothing happens.</p></body></html>''')


def notfound(path):
    """GitHub Pages is case-sensitive: send /ALTRUVA (any case) to /altruva, otherwise a friendly 404."""
    open(path, 'w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found | mtgtribe.com</title><meta name="robots" content="noindex">
<script>(function(){{var p=location.pathname,l=p.toLowerCase();if(p!==l){{location.replace(l+location.search+location.hash);}}}})();</script>
<style>body{{background:#01081b;color:#cde0f0;font:600 16px/1.6 system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0;padding:16px;text-align:center}}h1{{color:#fff;margin:0 0 8px}}a{{color:#eebd5c}}</style></head>
<body><main><h1>This page isn't here</h1><p>Try the <a href="/altruva/">ALTRUVA guide</a> or its <a href="/altruva/dashboard/">dashboard</a>.</p></main></body></html>''')


def check(dst):
    bad = []
    for r, _, fs in os.walk(dst):
        for f in fs:
            if f.endswith(('.html', '.css', '.js', '.xml')):
                s = open(os.path.join(r, f), encoding='utf-8').read()
                for ch, nm in (('—', 'em dash'), ('–', 'en dash')):
                    if ch in s:
                        bad.append(f'{nm} in {os.path.join(r, f)}')
                for w in ('downline', 'recruits', 'downliner'):
                    for m in re.finditer(w, s, re.I):
                        bad.append(f'"{w}" in {os.path.join(r, f)}')
    return bad


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    if '--fast' not in sys.argv or not os.path.exists(OUT + '/_img'):
        if os.path.exists(OUT + '/_img'):
            shutil.rmtree(OUT + '/_img')
        images(OUT + '/_img')
        os.makedirs(OUT + '/_pdf', exist_ok=True)
        quick_guide(OUT + '/_pdf/altruva-quick-guide-mtg.pdf')
    render('prod', OUT + '/prod')
    render('preview', OUT + '/preview')
    probs = check(OUT + '/prod') + check(OUT + '/preview')
    print('\n'.join(probs) if probs else 'CHECK OK: no dashes, no banned words')
