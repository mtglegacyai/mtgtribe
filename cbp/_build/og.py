"""Social preview images for the ClickBaitPays guide (1200x630 JPEG, under 200 KB), MTG's formula (tools/og/README.md):
one big headline that says what the page gives you, one clear visual of the subject, the exact address in a pill, the
ClickBaitPays emblem. Honest: examples labelled. Run: python3 cbp/_build/og.py  (needs node + the global Playwright)."""
import os, subprocess, tempfile, json, base64
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'cbp', 'assets', 'og')
LOGO = os.path.join(ROOT, 'tools', 'cbp', 'brand', 'clickbaitpays-logo-disc-video.png')
LEVELS = [(1, 13), (2, 77), (3, 150), (4, 300), (5, 600), (6, 1200), (7, 2400)]

logo64 = 'data:image/png;base64,' + base64.b64encode(open(LOGO, 'rb').read()).decode()

CSS = '''*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:630px;overflow:hidden;background:#080015}
body{font-family:Poppins,sans-serif;color:#fff}
.c{position:relative;width:1200px;height:630px;padding:54px 60px;overflow:hidden;
 background:radial-gradient(700px 480px at 0% 0%,rgba(255,0,255,.32),transparent 65%),radial-gradient(760px 560px at 100% 100%,rgba(0,229,255,.26),transparent 65%),linear-gradient(160deg,#0f0329,#080015 60%,#05000e)}
.c:after{content:"";position:absolute;inset:16px;border-radius:28px;border:2px solid rgba(0,229,255,.45);box-shadow:0 0 30px rgba(0,229,255,.2) inset}
.eye{display:inline-flex;align-items:center;gap:12px;padding:8px 18px;border-radius:999px;background:rgba(0,229,255,.14);border:2px solid rgba(0,229,255,.55);font:800 22px Orbitron;letter-spacing:.08em;color:#00e5ff}
.eye img{width:40px;height:40px;border-radius:50%}
h1{margin-top:26px;font:900 64px/1.06 Orbitron;letter-spacing:.005em;max-width:600px}
h1 em{font-style:normal;background:linear-gradient(90deg,#00e5ff,#ff00ff);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{margin-top:18px;font:600 28px/1.35 Poppins;color:#e6e2f2;max-width:600px}
.pill{position:absolute;left:60px;bottom:52px;padding:14px 28px;border-radius:999px;background:linear-gradient(90deg,#00e5ff,#00ffee);color:#05000e;font:900 30px Orbitron;box-shadow:0 0 34px rgba(0,229,255,.5)}
.vis{position:absolute;right:56px;top:50%;transform:translateY(-50%)}
.logo{width:200px;height:200px;border-radius:50%;box-shadow:0 0 0 5px rgba(0,229,255,.85),0 0 60px rgba(0,229,255,.55),0 0 120px rgba(255,0,255,.35)}
.lvls{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:16px;width:440px}
.lv{padding:6px 12px;border-radius:12px;text-align:left;background:rgba(16,5,37,.9);border:2px solid rgba(0,229,255,.4)}
.lv b{display:inline-block;width:84px;font:800 14px Orbitron;color:#00e5ff}.lv span{font:700 18px Poppins;white-space:nowrap}
.lv.w{grid-column:1/-1;border-color:rgba(255,216,102,.6)}.lv.w b{color:#ffd866}
.lap{width:420px}
.lap .s{aspect-ratio:16/9;border:12px solid #15151c;border-radius:18px 18px 4px 4px;background:linear-gradient(160deg,#1a0838,#08001a);padding:20px 24px;display:grid;gap:9px;align-content:center}
.lap .b{height:16px;margin:0 -26px;border-radius:0 0 20px 20px;background:linear-gradient(180deg,#c9ccd6,#3a3d48)}
.row{display:flex;align-items:center;gap:12px;font:600 18px Poppins}
.row i{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#00e5ff,#ff00ff);color:#05000e;font:900 15px Orbitron;font-style:normal}
.calc{width:440px;padding:24px;border-radius:24px;background:rgba(16,5,37,.92);border:2px solid rgba(0,229,255,.5);display:grid;gap:12px}
.calc .t{display:flex;justify-content:space-between;align-items:baseline;padding:12px 16px;border-radius:14px;background:rgba(255,255,255,.05)}
.calc .t span{font:600 20px Poppins;color:#b6b2c5}.calc .t b{font:900 28px Orbitron}
.calc .t.big{background:linear-gradient(135deg,rgba(0,229,255,.2),rgba(255,0,255,.16))}.calc .t.big b{color:#00e5ff;font-size:36px}
.calc .eg{font:700 16px Poppins;color:#ffd866;letter-spacing:.06em;text-transform:uppercase}
.shield{width:300px;height:340px}
.br{width:440px;border-radius:18px;overflow:hidden;border:2px solid rgba(255,216,102,.55);background:#100525;box-shadow:0 30px 60px rgba(0,0,0,.5)}
.br .bar{display:flex;align-items:center;gap:10px;padding:14px 16px;background:#1d1238}
.br .bar i{width:13px;height:13px;border-radius:50%;background:#ff5f57}.br .bar i+i{background:#febc2e}.br .bar i+i+i{background:#28c840}
.br .url{flex:1;margin-left:10px;padding:8px 14px;border-radius:10px;background:#0b0220;font:700 19px Poppins;color:#fff}
.br .url u{text-decoration:none;color:#ffd866}
.br .pg{display:grid;justify-items:center;gap:14px;padding:26px}
.br .pg img{width:130px;height:130px;border-radius:50%;box-shadow:0 0 0 4px rgba(0,229,255,.8)}
.br .pg .j{padding:12px 26px;border-radius:999px;background:linear-gradient(90deg,#00e5ff,#00ffee);color:#05000e;font:800 22px Poppins}
.price{display:inline-block;margin-top:4px;padding:10px 20px;border-radius:16px;background:rgba(255,216,102,.14);border:2px solid rgba(255,216,102,.6);font:900 34px Orbitron;color:#ffd866}
.price small{font:700 22px Poppins;color:#fff}'''

EYE = f'<div class="eye"><img src="{logo64}" alt="">CLICKBAITPAYS GUIDE BY MTG</div>'

SPECS = {
    'cbp-home': ('<h1>ClickBaitPays,<br><em>explained</em></h1><p class="sub">How it works, the 7 levels from 13 USDT and how to join free.</p>',
                 f'<div class="vis" style="text-align:center"><img class="logo" src="{logo64}" alt=""><div class="lvls">' +
                 ''.join(f'<div class="lv"><b>LEVEL {l}</b><span>{p:,} USDT</span></div>' for l, p in LEVELS[:6]) +
                 f'<div class="lv w"><b>LEVEL 7</b><span>2,400 USDT</span></div></div></div>', 'mtgtribe.com/cbp'),
    'cbp-dashboard': ('<h1>7 step-by-step <em>tutorials</em></h1><p class="sub">Every ClickBaitPays job, click by click, in the right order.</p>',
                      '<div class="vis lap"><div class="s">' + ''.join(f'<div class="row"><i>{i}</i>{t}</div>' for i, t in enumerate(
                          ['Back office tour', 'Deposit', 'Your first campaign', 'Another campaign', 'Withdraw', 'Login Ads', 'Pay It Forward'], 1)) +
                      '</div><div class="b"></div></div>', 'mtgtribe.com/cbp/dashboard'),
    'cbp-calculator': ('<h1>ClickBaitPays <em>calculator</em></h1><p class="sub">What you pay today, your clicks a day and your payout date.</p>',
                       '<div class="vis calc"><div class="eg">Example: first Level 4 campaign</div>'
                       '<div class="t big"><span>Pay today</span><b>330 USDT</b></div><div class="t"><span>Clicks a day</span><b>5</b></div>'
                       '<div class="t"><span>Platform figure</span><b>388.80</b></div><div class="t"><span>Click days</span><b>12 + 7</b></div></div>', 'mtgtribe.com/cbp/calculator'),
    'cbp-disclaimer': ('<h1>The small print, in <em>plain words</em></h1><p class="sub">Independent guide, referral link disclosure and your privacy.</p>',
                       '<div class="vis"><svg class="shield" viewBox="0 0 24 24" fill="none" stroke="#00e5ff" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">'
                       '<path d="M12 2.5l8 3v6c0 5-3.5 8.6-8 10-4.5-1.4-8-5-8-10v-6z" fill="rgba(0,229,255,.12)"/><path d="M8.5 12l2.5 2.5 4.5-5" stroke="#46f2ad" stroke-width="1.8"/></svg></div>',
                       'mtgtribe.com/cbp/disclaimer'),
    'cbp-copy': ('<h1>Your own <em>ClickBaitPays</em> guide</h1><p class="sub">This guide with your link on every Join button.</p>',
                 f'<div class="vis br"><div class="bar"><i></i><i></i><i></i><span class="url">mtgtribe.com/cbp/<u>yourname</u></span></div>'
                 f'<div class="pg"><img src="{logo64}" alt=""><span class="j">Join ClickBaitPays free</span><div class="price">R1,000 <small>or $50 once-off</small></div></div></div>', 'mtgtribe.com/cbpcopy'),
}

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@800;900&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">'


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp()
    jobs = []
    for key, (copy, vis, url) in SPECS.items():
        page = f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body><div class="c">{EYE}{copy}{vis}<div class="pill">{url}</div></div></body></html>'
        p = os.path.join(tmp, key + '.html'); open(p, 'w', encoding='utf-8').write(page)
        jobs.append((p, os.path.join(tmp, key + '.png'), key))
    js = os.path.join(tmp, 'shot.js')
    open(js, 'w').write('''const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const jobs=%s;
for(const [h,o] of jobs){const p=await b.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});await p.goto('file://'+h);
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);await p.screenshot({path:o});await p.close();}await b.close();})();''' % json.dumps([[a, b] for a, b, k in jobs]))
    subprocess.run(['node', js], check=True)
    for _, png, key in jobs:
        im = Image.open(png).convert('RGB')
        for q in (88, 84, 80, 76, 72):
            dst = os.path.join(OUT, key + '.jpg'); im.save(dst, 'JPEG', quality=q, optimize=True, progressive=True)
            if os.path.getsize(dst) < 200_000:
                break
        print(key, os.path.getsize(dst) // 1024, 'KB')


if __name__ == '__main__':
    main()
