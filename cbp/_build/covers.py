"""Wide video covers for the ClickBaitPays guide (1280x720 and 640x360 WebP), MTG's cover rules (CLAUDE.md, 16 and 17 Nov 2026):
every video shows on the page as a 16:9 cover in the laptop frame, the MIDDLE of the cover stays clear for the play button
(headline above, one clear visual below, no address pill), every line short and compelling, labels a phone can read.

Run: NODE_PATH=$(npm root -g) python3 cbp/_build/covers.py      (needs node and the global Playwright)
Writes cbp/assets/v/<code>.webp (1280x720) and <code>-640.webp (640x360), the files the pages use."""
import base64, json, os, random, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'cbp', 'assets', 'v')
LOGO = os.path.join(ROOT, 'tools', 'cbp', 'brand', 'clickbaitpays-logo-disc-video.png')
logo64 = 'data:image/png;base64,' + base64.b64encode(open(LOGO, 'rb').read()).decode()

CSS = '''*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1280px;height:720px;overflow:hidden;background:#07001a}
body{font-family:Poppins,sans-serif;color:#fff}
.c{position:relative;width:1280px;height:720px;overflow:hidden;
 background:radial-gradient(520px 300px at 50% 50%,rgba(0,229,255,.16),transparent 70%),radial-gradient(760px 520px at 0% 0%,rgba(255,0,255,.22),transparent 62%),
 radial-gradient(800px 560px at 100% 100%,rgba(0,229,255,.22),transparent 62%),linear-gradient(165deg,#120434,#07001a 55%,#030010)}
.c svg.cir{position:absolute;inset:0;width:1280px;height:720px}
.top{position:absolute;left:0;right:0;top:34px;display:grid;justify-items:center;gap:14px;text-align:center}
.kick{display:inline-flex;align-items:center;gap:14px;padding:8px 24px 8px 10px;border-radius:999px;background:rgba(7,0,26,.78);border:2px solid rgba(0,229,255,.6);
 box-shadow:0 0 24px rgba(0,229,255,.35);font:800 27px Orbitron;letter-spacing:.1em;color:#7ff4ff}
.kick img{width:46px;height:46px;border-radius:50%}
h1{font:900 88px/1.02 Orbitron,sans-serif;letter-spacing:.01em;text-transform:uppercase;white-space:nowrap;
 background:linear-gradient(180deg,#ffffff 8%,#9ff7ff 46%,#00e5ff 62%,#ff4dff 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 0 18px rgba(0,229,255,.45)) drop-shadow(0 6px 0 rgba(60,0,90,.9))}
h1 .w{display:block;font-size:.56em;line-height:1.15;letter-spacing:.04em;background:none;color:#fff;-webkit-text-fill-color:#fff}
h1.sm{font-size:76px}
.mid{position:absolute;left:50%;top:360px;width:330px;height:330px;margin:-165px 0 0 -165px;border-radius:50%;
 background:radial-gradient(circle,rgba(0,229,255,.18),rgba(255,0,255,.06) 55%,transparent 70%)}
.bot{position:absolute;left:0;right:0;bottom:30px;display:flex;justify-content:center;align-items:flex-end;gap:22px}
.chip{display:inline-flex;align-items:center;gap:14px;padding:15px 28px;border-radius:20px;background:rgba(10,2,34,.88);border:2px solid rgba(0,229,255,.55);
 box-shadow:0 0 26px rgba(0,229,255,.25),inset 0 0 18px rgba(0,229,255,.12);font:800 34px/1 Orbitron,sans-serif;text-transform:uppercase;letter-spacing:.03em}
.chip.p{border-color:rgba(255,0,255,.6);box-shadow:0 0 26px rgba(255,0,255,.3),inset 0 0 18px rgba(255,0,255,.12)}
.chip.g{border-color:rgba(255,216,102,.7);color:#ffe28a;box-shadow:0 0 26px rgba(255,216,102,.28)}
.chip svg{width:44px;height:44px;flex:none}
.chip b{font-weight:900;color:#00e5ff}.chip.p b{color:#ff6bff}
.arrow{font:900 46px Orbitron,sans-serif;color:#ffd866;filter:drop-shadow(0 0 10px rgba(255,216,102,.6));align-self:center}
.bars{display:flex;align-items:flex-end;gap:14px;height:200px}
.bars i{display:grid;align-content:end;justify-items:center;width:78px;border-radius:12px 12px 4px 4px;font:900 30px Orbitron;font-style:normal;color:#07001a;padding-bottom:8px;
 background:linear-gradient(180deg,#7ff4ff,#00e5ff 40%,#ff00ff);box-shadow:0 0 22px rgba(0,229,255,.45)}
.dots{display:flex;align-items:center;gap:9px;padding:16px 22px;border-radius:22px;background:rgba(10,2,34,.88);border:2px solid rgba(0,229,255,.4)}
.dots i{width:34px;height:34px;border-radius:50%;background:#00e5ff;box-shadow:0 0 12px #00e5ff}
.dots i.h{background:#ff00ff;box-shadow:0 0 12px #ff00ff;width:30px;height:30px}
.dots i.e{display:grid;place-items:center;width:52px;height:52px;background:#46f2ad;box-shadow:0 0 18px #46f2ad;font:900 30px Poppins;font-style:normal;color:#03140c}
.keys{display:flex;gap:40px;font:800 32px Orbitron,sans-serif;text-transform:uppercase}
.keys span:nth-child(1){color:#00e5ff}.keys span:nth-child(2){color:#ff6bff}.keys span:nth-child(3){color:#46f2ad}
.stack{display:grid;justify-items:center;gap:16px}
.dash{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;width:1000px}
.dash .k{padding:16px 18px;border-radius:18px;background:rgba(10,2,34,.9);border:2px solid rgba(0,229,255,.45);text-align:left}
.dash .k small{display:block;font:800 27px Poppins;color:#b9b2d6}.dash .k b{display:block;margin-top:4px;font:900 36px Orbitron;color:#00e5ff;letter-spacing:.1em}
.dash .k:nth-child(2) b{color:#ff6bff}.dash .k:nth-child(3) b{color:#46f2ad}.dash .k:nth-child(4) b{color:#ffd866}
.av{display:grid;place-items:center;width:120px;height:120px;border-radius:50%;background:rgba(10,2,34,.9);border:3px solid #00e5ff;box-shadow:0 0 24px rgba(0,229,255,.5)}
.av svg{width:64px;height:64px}
.av.p{border-color:#ff00ff;box-shadow:0 0 24px rgba(255,0,255,.5)}
.br{width:760px;border-radius:16px;overflow:hidden;border:2px solid rgba(0,229,255,.55);background:#0b0224;box-shadow:0 0 26px rgba(0,229,255,.25)}
.br .t{display:flex;gap:9px;padding:10px 14px;background:#1a0b3d}.br .t i{width:14px;height:14px;border-radius:50%;background:#ff5f57}.br .t i+i{background:#febc2e}.br .t i+i+i{background:#28c840}
.br .b{display:grid;grid-template-columns:200px 1fr;gap:14px;padding:14px}
.br .s{display:grid;gap:9px}.br .s i{height:22px;border-radius:7px;background:rgba(0,229,255,.25)}.br .s i:first-child{background:#00e5ff}
.br .m{display:grid;grid-template-columns:1fr 1fr;gap:10px}.br .m i{height:46px;border-radius:10px;background:rgba(255,0,255,.22);border:1px solid rgba(255,0,255,.4)}
'''

I = {   # simple line icons (Lucide shapes), drawn in the chips
    'cursor': '<path d="M4 4l7 17 2.5-7.5L21 11z"/>',
    'eye': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    'coins': '<circle cx="8" cy="8" r="6"/><path d="M18.1 10.4A6 6 0 1 1 10.4 18.1"/><path d="M7 6h1v4"/>',
    'mega': '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    'link': '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    'user': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6M22 11h-6"/>',
    'play': '<polygon points="6 3 20 12 6 21 6 3"/>',
    'wallet': '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'cal': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'heart': '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/>',
    'chat': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22z"/>',
    'help': '<circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
    'layers': '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
    'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
    'rocket': '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="m12 15-3-3a22 22 0 0 1 2-4A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/>',
    'trend': '<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
    'repeat': '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
}


def svg(name, color='#00e5ff'):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg>'


def chip(icon, text, cls=''):
    col = {'p': '#ff6bff', 'g': '#ffd866'}.get(cls, '#00e5ff')
    return f'<span class="chip {cls}">{svg(icon, col) if icon else ""}{text}</span>'


def circuits(seed):
    """neon circuit lines that come in from both sides and stay out of the middle"""
    r = random.Random(seed)
    out = ['<svg class="cir" viewBox="0 0 1280 720"><defs><filter id="g"><feGaussianBlur stdDeviation="3"/></filter></defs>']
    for side in (0, 1):
        col = '#00e5ff' if side == 0 else '#ff00ff'
        for k in range(9):
            y = 60 + k * 72 + r.randint(-14, 14)
            x0 = 0 if side == 0 else 1280
            d = r.choice([1, -1])
            l1 = r.randint(60, 210)
            l2 = r.randint(30, 70)
            l3 = r.randint(30, 140)
            sx = 1 if side == 0 else -1
            p = [(x0, y), (x0 + sx * l1, y), (x0 + sx * (l1 + l2), y + d * l2), (x0 + sx * (l1 + l2 + l3), y + d * l2)]
            pts = ' '.join(f'{a},{b}' for a, b in p)
            ex, ey = p[-1]
            op = r.choice([.35, .5, .7])
            out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3" opacity="{op}" filter="url(#g)"/>'
                       f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="1.6" opacity="{op + .2}"/>'
                       f'<circle cx="{ex}" cy="{ey}" r="6" fill="none" stroke="{col}" stroke-width="2.4" opacity="{op + .2}"/>')
    for k in range(70):                       # a few stars
        x, y = r.randint(0, 1280), r.randint(0, 720)
        if 360 < x < 920 and 230 < y < 490:
            continue
        out.append(f'<circle cx="{x}" cy="{y}" r="{r.choice([1, 1.4, 2])}" fill="#fff" opacity="{r.choice([.25, .4, .6])}"/>')
    return ''.join(out) + '</svg>'


def kick(text):
    return f'<span class="kick"><img src="{logo64}" alt="">{text}</span>'


def headline(small, big, cls=''):
    return f'<h1 class="{cls}"><span class="w">{small}</span>{big}</h1>' if small else f'<h1 class="{cls}">{big}</h1>'


def bars(labels):
    hs = [70, 90, 110, 130, 150, 175, 200]
    return '<div class="bars">' + ''.join(f'<i style="height:{hs[k]}px">{t}</i>' for k, t in enumerate(labels)) + '</div>'


def dots():
    return '<div class="dots">' + '<i></i>' * 12 + '<i class="h"></i>' * 7 + '<i class="e">✓</i></div>'


# code: (kicker, small line, big line, bottom visual, headline class)
COVERS = {
    'welcome': ('VIDEO 1 · START HERE', 'Welcome to', 'ClickBaitPays',
                chip('cursor', 'Click') + chip('eye', 'Watch', 'p') + chip('coins', 'Earn', 'g'), ''),
    'strategy': ('VIDEO 2 · THE MONEY VIDEO', 'Income strategy &', 'Compensation plan', '<div class="stack">' + bars(['1', '2', '3', '4', '5', '6', '7']) + '</div>', ''),
    'backoffice': ('VIDEO 3 · LOOK AROUND', 'Back office', 'Walkthrough',
                   '<div class="dash"><span class="k"><small>Ads to click</small><b>•••</b></span><span class="k"><small>Earned wallet</small><b>•••</b></span>'
                   '<span class="k"><small>Available</small><b>•••</b></span><span class="k"><small>Campaigns</small><b>•••</b></span></div>', ''),
    'qa': ('LIVE Q&amp;A · 29 AUG 2026', 'Your questions', 'Answered', chip('chat', 'Clicks') + chip('help', 'Payouts', 'p') + chip('check', 'Proof', 'g'), ''),
    'presentation': ('PRESENTATION · 14 SEPT 2026', 'The full', 'Presentation', chip('mega', 'Ads') + chip('layers', 'Campaigns', 'p') + chip('wallet', 'Withdrawals', 'g'), ''),
    'tour': ('SITE TOUR · START HERE', 'How to use', 'This guide',
             '<div class="br"><div class="t"><i></i><i></i><i></i></div><div class="b"><div class="s"><i></i><i></i><i></i><i></i></div><div class="m"><i></i><i></i><i></i><i></i></div></div></div>', 'sm'),
    'e1': ('EXPLAINER · YOUR TRAFFIC SOURCE', 'Grow what you', 'Promote', chip('link', 'Your link') + '<span class="arrow">➜</span>' + chip('eye', 'Real eyes', 'p') + '<span class="arrow">➜</span>' + chip('trend', 'Growth', 'g'), ''),
    'e2': ('EXPLAINER · GET STARTED', 'How to', 'Join free', chip('link', '1 Tap Join') + chip('user', '2 Sign up', 'p') + chip('play', '3 Start', 'g'), ''),
    'e3': ('EXPLAINER · THE LEVELS', '7 levels', 'One activation', '<div class="stack">' + bars(['13', '77', '150', '300', '600', '1.2K', '2.4K']) + '</div>', 'sm'),
    'e4': ('EXPLAINER · THE TIMELINE', '12 click days', '+ 7 day hold', '<div class="stack">' + dots() + '<div class="keys"><span>Click</span><span>Hold</span><span>Yours</span></div></div>', 'sm'),
    't1': ('TUTORIAL 1', 'Your back office', 'Quick tour',
           '<div class="dash"><span class="k"><small>Click Ads</small><b>→</b></span><span class="k"><small>Campaigns</small><b>→</b></span>'
           '<span class="k"><small>Deposit</small><b>→</b></span><span class="k"><small>Withdraw</small><b>→</b></span></div>', ''),
    't2': ('TUTORIAL 2', 'How to', 'Deposit USDT', chip('wallet', 'Your wallet') + '<span class="arrow">➜</span>' + chip('coins', 'Your balance', 'g'), ''),
    't3': ('TUTORIAL 3', 'Your first', 'Campaign', chip('layers', 'Buy') + chip('rocket', 'Activate', 'p') + chip('cursor', 'Click', 'g'), ''),
    't4': ('TUTORIAL 4', 'Another', 'Campaign', chip('repeat', 'Same level') + chip('check', 'No activation fee', 'g'), ''),
    't5': ('TUTORIAL 5', 'How to', 'Withdraw', chip('coins', 'Available balance', 'g') + '<span class="arrow">➜</span>' + chip('wallet', 'Your wallet'), ''),
    't6': ('TUTORIAL 6', 'Create a', 'Login Ad', chip('clock', '30 seconds') + chip('cal', '30 days', 'p') + chip('eye', 'Every member', 'g'), ''),
    't7': ('TUTORIAL 7', 'How to', 'Pay It Forward',
           f'<span class="av">{svg("user")}</span><span class="arrow">➜</span>{chip("heart", "Help your team", "p")}<span class="arrow">➜</span><span class="av p">{svg("user", "#ff6bff")}</span>', 'sm'),
}

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;800;900'
         '&family=Poppins:wght@700;800&display=swap" rel="stylesheet">')


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp()
    jobs = []
    for n, (code, (k, small, big, vis, cls)) in enumerate(COVERS.items()):
        page = (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body><div class="c">{circuits(n + 7)}'
                f'<div class="mid"></div><div class="top">{kick(k)}{headline(small, big, cls)}</div><div class="bot">{vis}</div></div></body></html>')
        p = os.path.join(tmp, code + '.html')
        open(p, 'w', encoding='utf-8').write(page)
        jobs.append([p, os.path.join(tmp, code + '.png')])
    js = os.path.join(tmp, 'shot.js')
    open(js, 'w').write('''const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const jobs=%s;
for(const [h,o] of jobs){const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});await p.goto('file://'+h);
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);await p.evaluate(()=>{const h=document.querySelector('h1');let f=parseFloat(getComputedStyle(h).fontSize);while(h.scrollWidth>1180&&f>40){f-=2;h.style.fontSize=f+'px';}});
const over=await p.evaluate(()=>{const t=document.querySelector('.top').getBoundingClientRect(),b=document.querySelector('.bot').getBoundingClientRect();
 const w=[...document.querySelectorAll('.bot>*,.top>*')].some(e=>{const r=e.getBoundingClientRect();return r.left<0||r.right>1280});return {top:Math.round(t.bottom),bot:Math.round(b.top),wide:w}});
console.log(o.split('/').pop(),JSON.stringify(over));await p.screenshot({path:o});await p.close();}await b.close();})();''' % json.dumps(jobs))
    subprocess.run(['node', js], check=True)
    from PIL import Image
    for _, png in jobs:
        code = os.path.basename(png)[:-4]
        im = Image.open(png).convert('RGB')
        im.save(os.path.join(OUT, code + '.webp'), 'WEBP', quality=82, method=6)
        im.resize((640, 360), Image.LANCZOS).save(os.path.join(OUT, code + '-640.webp'), 'WEBP', quality=82, method=6)
    print(len(jobs), 'covers in', OUT)


if __name__ == '__main__':
    main()
