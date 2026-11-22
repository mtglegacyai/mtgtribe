"""Social preview images for every page of the ClickBaitPays guide (1200x630 JPEG, under 200 KB), MTG's formula (tools/og/README.md):
one big headline that says what the page gives you, one clear visual of its subject (the page's own video cover in the slim laptop,
or the tool itself), the exact address in a pill, the ClickBaitPays emblem. Run after covers.py:
NODE_PATH=$(npm root -g) python3 cbp/_build/og.py"""
import base64, json, os, subprocess, sys, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import build                                   # one source of truth: the pages, their addresses and their videos

OUT = os.path.join(ROOT, 'cbp', 'assets', 'og')
LOGO = os.path.join(ROOT, 'tools', 'cbp', 'brand', 'clickbaitpays-logo-disc-video.png')


def b64(path, mime='image/png'):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


logo64 = b64(LOGO)


def cov(code, w=640):
    """a video cover, made smaller for the preview"""
    im = Image.open(os.path.join(ROOT, 'cbp', 'assets', 'v', code + '.webp')).convert('RGB').resize((w, w * 9 // 16), Image.LANCZOS)
    p = os.path.join(tempfile.gettempdir(), f'cbp-og-{code}-{w}.jpg'); im.save(p, 'JPEG', quality=90)
    return b64(p, 'image/jpeg')


CSS = '''*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:630px;overflow:hidden;background:#080015}
body{font-family:Poppins,sans-serif;color:#fff}
.c{position:relative;width:1200px;height:630px;padding:50px 56px;overflow:hidden;
 background:radial-gradient(700px 480px at 0% 0%,rgba(255,0,255,.30),transparent 65%),radial-gradient(760px 560px at 100% 100%,rgba(0,229,255,.26),transparent 65%),linear-gradient(160deg,#0f0329,#080015 60%,#05000e)}
.c:after{content:"";position:absolute;inset:14px;border-radius:28px;border:2px solid rgba(0,229,255,.42);box-shadow:0 0 30px rgba(0,229,255,.18) inset;pointer-events:none}
.eye{display:inline-flex;align-items:center;gap:12px;padding:8px 18px 8px 8px;border-radius:999px;background:rgba(0,229,255,.12);border:2px solid rgba(0,229,255,.5);font:800 20px Orbitron;letter-spacing:.08em;color:#7ff4ff}
.eye img{width:40px;height:40px;border-radius:50%}
h1{margin-top:24px;font:900 50px/1.12 Orbitron,sans-serif;text-transform:uppercase;letter-spacing:.01em;max-width:520px}
h1 em{font-style:inherit;background:linear-gradient(180deg,#fff 5%,#9ff7ff 45%,#00e5ff 62%,#ff4dff 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{margin-top:16px;font:600 26px/1.35 Poppins;color:#e6e2f2;max-width:500px}
.pill{position:absolute;left:56px;bottom:46px;max-width:1088px;padding:12px 26px;border-radius:999px;background:linear-gradient(90deg,#00e5ff,#00ffee);color:#05000e;font:900 28px Orbitron;white-space:nowrap;box-shadow:0 0 34px rgba(0,229,255,.5)}
.vis{position:absolute;right:52px;top:50%;transform:translateY(-58%)}
.lap{width:560px}
.lap .d{padding:7px 7px 7px;border:2px solid transparent;border-radius:16px 16px 6px 6px;background:linear-gradient(#040404,#040404) padding-box,linear-gradient(140deg,#7a531c,#f6d88c 22%,#9a6a26 45%,#f2c66d 70%,#6b4615) border-box;box-shadow:0 0 60px rgba(0,229,255,.35),0 30px 60px rgba(0,0,0,.6)}
.lap .bar{display:flex;justify-content:space-between;padding:4px 6px 9px;font:700 15px Poppins;color:#d9d3ee}.lap .bar b{color:#ffd866}
.lap img{display:block;width:100%;aspect-ratio:16/9}
.lap .k{height:14px;margin:0 -22px;border-radius:0 0 20px 20px/0 0 12px 12px;background:linear-gradient(180deg,#e2c078,#8a6124 26%,#3a2a12 70%,#17110a)}
.fan{width:560px;height:360px}
.fan img{position:absolute;width:340px;border-radius:14px;border:2px solid rgba(255,216,102,.7);box-shadow:0 20px 40px rgba(0,0,0,.6),0 0 30px rgba(0,229,255,.3)}
.fan img:nth-child(1){left:0;top:0;z-index:1}.fan img:nth-child(2){left:110px;top:92px;z-index:2}.fan img:nth-child(3){left:220px;top:184px;z-index:3}
.fan .n{position:absolute;z-index:4;display:grid;place-items:center;width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,#00e5ff,#ff00ff);color:#05000e;font:900 22px Orbitron}
.grid4{display:grid;grid-template-columns:1fr 1fr;gap:14px;width:560px}
.grid4 img{width:100%;border-radius:12px;border:2px solid rgba(0,229,255,.5);box-shadow:0 14px 30px rgba(0,0,0,.5)}
.list{width:520px;padding:18px;border-radius:20px;background:rgba(16,5,37,.92);border:2px solid rgba(0,229,255,.45);display:grid;gap:9px}
.row{display:flex;align-items:center;gap:14px;font:600 21px Poppins}
.row i{flex:none;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#00e5ff,#ff00ff);color:#05000e;font:900 16px Orbitron;font-style:normal}
.calc{width:500px;padding:24px;border-radius:24px;background:rgba(16,5,37,.92);border:2px solid rgba(0,229,255,.5);display:grid;gap:12px}
.calc .t{display:flex;justify-content:space-between;align-items:baseline;padding:12px 16px;border-radius:14px;background:rgba(255,255,255,.05)}
.calc .t span{font:600 20px Poppins;color:#b6b2c5}.calc .t b{font:900 28px Orbitron}
.calc .t.big{background:linear-gradient(135deg,rgba(0,229,255,.2),rgba(255,0,255,.16))}.calc .t.big b{color:#00e5ff;font-size:36px}
.calc .eg{font:700 16px Poppins;color:#ffd866;letter-spacing:.06em;text-transform:uppercase}
.shield{width:300px;height:340px}
.br{width:500px;border-radius:18px;overflow:hidden;border:2px solid rgba(255,216,102,.55);background:#100525;box-shadow:0 30px 60px rgba(0,0,0,.5)}
.br .bb{display:flex;align-items:center;gap:10px;padding:14px 16px;background:#1d1238}
.br .bb i{width:13px;height:13px;border-radius:50%;background:#ff5f57}.br .bb i+i{background:#febc2e}.br .bb i+i+i{background:#28c840}
.br .url{flex:1;margin-left:10px;padding:8px 14px;border-radius:10px;background:#0b0220;font:700 19px Poppins;color:#fff}.br .url u{text-decoration:none;color:#ffd866}
.br .pg{display:grid;justify-items:center;gap:14px;padding:26px}
.br .pg img{width:120px;height:120px;border-radius:50%;box-shadow:0 0 0 4px rgba(0,229,255,.8)}
.br .pg .j{padding:12px 26px;border-radius:999px;background:linear-gradient(90deg,#00e5ff,#00ffee);color:#05000e;font:800 22px Poppins}
.price{display:inline-block;padding:10px 20px;border-radius:16px;background:rgba(255,216,102,.14);border:2px solid rgba(255,216,102,.6);font:900 32px Orbitron;color:#ffd866}.price small{font:700 20px Poppins;color:#fff}'''


def laptop(code):
    v = build.V[code]
    right = build.mmss(v['secs']) if build.playable(code) else build.STATUS[v['status']]
    return (f'<div class="vis lap"><div class="d"><div class="bar"><span>{v["label"]} · {v["short"]}</span><b>{right}</b></div>'
            f'<img src="{cov(code)}" alt=""></div><div class="k"></div></div>')


# page key: (headline, one line, visual)
VIDEO_OF = {'home': 'tour', 'what': 'welcome', 'grow': 'e1', 'legit': 'qa', 'how': 'presentation', 'join': 'e2', 'levels': 'e3', 'timeline': 'e4', 'plan': 'strategy',
            'daily': 't3', 'faq': 'qa', **{k: build.TUT[k].get('video', k) for k in build.TUT}}
COPY = {
    'landing': ('ClickBaitPays in <em>3 videos</em>', 'What it is, the strategy, the back office.'),
    'home': ('Your ClickBaitPays <em>dashboard</em>', 'Every topic and tutorial, in order.'),
    'what': ('What is <em>ClickBaitPays?</em>', 'Advertise your link, view ads, get paid in USDT.'),
    'how': ('How it works in <em>5 steps</em>', 'From free sign-up to your payout.'),
    'join': ('Join <em>free</em> in 3 steps', 'Through a member\'s link, and the house rules.'),
    'levels': ('All <em>7 levels</em> in one table', 'From 13 USDT. Activate a level once.'),
    'timeline': ('<em>12 + 7</em>: when it is yours', '12 click days, a 7-day hold, then your balance.'),
    'plan': ('The compensation <em>plan</em>', 'How you earn at every level, on video.'),
    'grow': ('Grow what you <em>promote</em>', 'Your link in front of members who already use crypto.'),
    'legit': ('Is it <em>legit?</em>', 'The facts, and how to check it yourself.'),
    'calc': ('ClickBaitPays <em>calculator</em>', 'What you pay today, your clicks and your payout date.'),
    'daily': ('Your <em>daily</em> routine', 'Log in, click, done. New clicks at 7:00 AM.'),
    'tutorials': ('7 step-by-step <em>tutorials</em>', 'Every ClickBaitPays job, in the right order.'),
    't1': ('Back office <em>tour</em>', 'Every menu item, so you know your way around.'),
    't2': ('Deposit <em>USDT</em>, safely', 'Amount, NOWPayments, a fresh address every time.'),
    't3': ('Your <em>first</em> campaign', 'Buy it, activate the level, click your ads.'),
    't4': ('<em>Another</em> campaign', 'No activation fee the second time.'),
    't5': ('How to <em>withdraw</em>', 'Once a week, 10 USDT minimum, 10% fee.'),
    't6': ('Create a <em>Login Ad</em>', '20 USDT, 30 days, seen by every member.'),
    't7': ('<em>Pay It Forward</em>', 'Send funds to a team member, safely.'),
    'videos': ('Every ClickBaitPays <em>video</em>', 'Watch today, and what is on the way.'),
    'faq': ('ClickBaitPays <em>FAQ</em>', '12 straight answers, and a live Q&amp;A.'),
    'copy': ('Get <em>this website</em>', 'Your link on every Join button. Pay only if you like it.'),
    'disc': ('The small print, in <em>plain words</em>', 'Independent guide, the referral link and your privacy.'),
}


def visual(key):
    if key == 'landing':
        return (f'<div class="vis fan"><img src="{cov("welcome", 480)}" alt=""><img src="{cov("strategy", 480)}" alt=""><img src="{cov("backoffice", 480)}" alt="">'
                '<span class="n" style="left:-18px;top:-14px">1</span><span class="n" style="left:92px;top:78px">2</span><span class="n" style="left:202px;top:170px">3</span></div>')
    if key == 'videos':
        return '<div class="vis grid4">' + ''.join(f'<img src="{cov(c, 480)}" alt="">' for c in ['welcome', 'strategy', 'backoffice', 'qa']) + '</div>'
    if key == 'tutorials':
        return '<div class="vis list">' + ''.join(f'<div class="row"><i>{i + 1}</i>{build.NAVD[k][2]}</div>' for i, k in enumerate(['t1', 't2', 't3', 't4', 't5', 't6', 't7'])) + '</div>'
    if key == 'calc':
        return ('<div class="vis calc"><div class="eg">Example: first Level 4 campaign</div><div class="t big"><span>Pay today</span><b>330 USDT</b></div>'
                '<div class="t"><span>Clicks a day</span><b>5</b></div><div class="t"><span>Platform figure</span><b>388.80</b></div><div class="t"><span>Click days</span><b>12 + 7</b></div></div>')
    if key == 'disc':
        return ('<div class="vis"><svg class="shield" viewBox="0 0 24 24" fill="none" stroke="#00e5ff" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">'
                '<path d="M12 2.5l8 3v6c0 5-3.5 8.6-8 10-4.5-1.4-8-5-8-10v-6z" fill="rgba(0,229,255,.12)"/><path d="M8.5 12l2.5 2.5 4.5-5" stroke="#46f2ad" stroke-width="1.8"/></svg></div>')
    if key == 'copy':
        return (f'<div class="vis br"><div class="bb"><i></i><i></i><i></i><span class="url">mtgtribe.com/cbp/<u>yourname</u></span></div>'
                f'<div class="pg"><img src="{logo64}" alt=""><span class="j">Join ClickBaitPays free</span><div class="price">R1,000 <small>or $50 once-off</small></div></div></div>')
    return laptop(VIDEO_OF[key])


FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@800;900'
         '&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">')


def address(key):
    path = '' if key == 'landing' else build.NAVD[key][1]
    return ('mtgtribe.com' + build.prod_url(path)).rstrip('/')


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp()
    jobs = []
    for key, (h, sub) in COPY.items():
        url = address(key)
        fs = min(28, int(1030 / (len(url) * 0.8)))
        page = (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body><div class="c">'
                f'<div class="eye"><img src="{logo64}" alt="">CLICKBAITPAYS GUIDE BY MTG</div><h1>{h}</h1><p class="sub">{sub}</p>{visual(key)}'
                f'<div class="pill" style="font-size:{fs}px">{url}</div></div></body></html>')
        p = os.path.join(tmp, key + '.html'); open(p, 'w', encoding='utf-8').write(page)
        jobs.append([p, os.path.join(tmp, key + '.png'), key])
    js = os.path.join(tmp, 'shot.js')
    open(js, 'w').write('''const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const jobs=%s;
for(const [h,o,k] of jobs){const p=await b.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});await p.goto('file://'+h);
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.evaluate(()=>{const h=document.querySelector('h1');let f=parseFloat(getComputedStyle(h).fontSize);const words=[...h.querySelectorAll('*')];while((h.scrollWidth>520||h.getBoundingClientRect().height>250)&&f>30){f-=2;h.style.fontSize=f+'px';}});
const r=await p.evaluate(()=>{const q=s=>document.querySelector(s).getBoundingClientRect();const h=q('h1'),s=q('.sub'),v=q('.vis'),pl=q('.pill');
 return {textRight:Math.round(Math.max(h.right,s.right)),visLeft:Math.round(v.left),subBottom:Math.round(s.bottom),pillTop:Math.round(pl.top),visBottom:Math.round(v.bottom),pillRight:Math.round(pl.right),visTop:Math.round(v.top)}});
const warn=(r.textRight>r.visLeft-10?' TEXT/VISUAL OVERLAP':'')+(r.subBottom>r.pillTop-8?' TEXT/PILL OVERLAP':'')+(r.visBottom>r.pillTop-6&&r.pillRight>r.visLeft?' VISUAL/PILL OVERLAP':'')+(r.visTop<20?' VISUAL TOO HIGH':'');
console.log(k,warn||'ok');await p.screenshot({path:o});await p.close();}await b.close();})();''' % json.dumps(jobs))
    subprocess.run(['node', js], check=True)
    for _, png, key in jobs:
        im = Image.open(png).convert('RGB')
        dst = os.path.join(OUT, f'cbp-{key}.jpg')
        for q in (86, 82, 78, 74, 70):
            im.save(dst, 'JPEG', quality=q, optimize=True, progressive=True)
            if os.path.getsize(dst) < 200_000:
                break
    print(len(jobs), 'previews in', OUT)


if __name__ == '__main__':
    main()
