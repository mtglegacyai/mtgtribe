#!/usr/bin/env python3
"""Social preview images (og:image, 1200x630) for mtgtribe.com pages (MTG, 9 Nov 2026).

MTG: "customize the preview thumbnail that appears when I paste any link on socials according to what the page is...
optimized for click-through rate." One designed image per page: a big, short headline that says what the page gives
you, one clear visual of the page's subject, and the exact address the link opens.

Usage, from the repo root:  python3 tools/og/make_og.py [slug ...]
Writes assets/og/<slug>.jpg (1200x630 JPEG, well under WhatsApp's 300 KB) and assets/og/sheet.jpg (all of them).
Families: JetUP (purple, lime, the JetUP logo disc, no photo of MTG, as in his JetUP videos), MTG TRIBE (black and gold,
MTG's whole photo in a gold-ringed circle) and Canton (black and gold, the official Canton logo kept apart from MTG's
branding). The weekly Canton reports make their own preview in tools/canton-weekly/thumb.py.
No em or en dashes anywhere. No income promises, no fake balances or messages.
"""
import html, json, os, subprocess, sys, tempfile
from PIL import Image

ROOT = os.getcwd()
OUT = os.path.join(ROOT, 'assets', 'og')
A = lambda p: 'file://' + os.path.join(ROOT, p)
DISC = A('tools/og/assets/jetup-disc.png')
FACE = A('assets/tribe/mtg-photo-round-720.webp')
CANTON = A('assets/canton/canton-logo-white.svg')
W, H = 1200, 630

FONTS = "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@600;700;800&family=JetBrains+Mono:wght@700&family=DM+Sans:wght@700;800&family=Outfit:wght@800;900&display=block');"

BASE = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:630px;overflow:hidden}
body{position:relative;font-family:'Manrope',sans-serif;color:var(--text);background:var(--bg)}
.ab{position:absolute}
.bg{position:absolute;inset:0;background:var(--bgimg)}
.grid{position:absolute;inset:0;opacity:.07;background-image:linear-gradient(rgba(255,255,255,.6) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.6) 1px,transparent 1px);background-size:60px 60px;-webkit-mask-image:radial-gradient(900px 560px at 70% 45%,#000 30%,transparent 85%)}
.frame{position:absolute;inset:14px;border-radius:30px;box-shadow:inset 0 0 0 2px var(--rim)}
.brand{position:absolute;left:56px;top:46px;display:flex;align-items:center;gap:14px}
.brand img{width:54px;height:54px;border-radius:50%}
.brand b{display:block;font:800 21px/1 'Manrope';letter-spacing:.14em;color:var(--text)}
.brand small{display:block;margin-top:6px;font:700 15px/1 'Manrope';letter-spacing:.1em;color:var(--acc2)}
.txt{position:absolute;left:56px;top:122px;width:600px;height:378px;overflow:hidden}
.eb{display:inline-flex;align-items:center;gap:10px;height:40px;padding:0 18px;border-radius:999px;background:var(--ebbg);box-shadow:inset 0 0 0 2px var(--acc);color:var(--acc);font:800 17px/1 'Manrope';letter-spacing:.16em;white-space:nowrap}
h1{margin-top:20px;font:400 var(--hs,96px)/.97 'Anton';text-transform:uppercase;letter-spacing:.005em;color:var(--text)}
h1 em{font-style:normal;color:var(--acc)}
h1 .g{background:var(--goldg);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{margin-top:18px;font:800 27px/1.28 'Manrope';color:var(--body)}
.sub b{color:var(--acc)}
.url{position:absolute;left:56px;bottom:50px;display:inline-flex;align-items:center;gap:12px;height:56px;padding:0 24px 0 10px;border-radius:999px;background:var(--urlbg);color:var(--urlc);font:800 23px/1 'Manrope';white-space:nowrap;box-shadow:0 10px 30px var(--urlsh)}
.url i{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--urlc);color:var(--urlbg);font:900 17px/1 'Manrope';font-style:normal}
.hero{position:absolute;left:660px;top:38px;width:500px;height:554px}
.e{font-family:'Noto Color Emoji';font-style:normal}
.card{position:absolute;border-radius:26px;background:var(--panel);box-shadow:inset 0 0 0 2px var(--line),0 24px 60px rgba(0,0,0,.5)}
.chip{position:absolute;display:inline-flex;align-items:center;gap:10px;height:52px;padding:0 20px;border-radius:999px;background:var(--chipbg);box-shadow:inset 0 0 0 2px var(--line),0 14px 34px rgba(0,0,0,.45);font:800 21px/1 'Manrope';color:var(--text);white-space:nowrap}
.chip .e{font-size:24px}
.row{display:flex;align-items:center;gap:16px;padding:0 22px;height:70px;border-radius:18px;background:rgba(255,255,255,.045);box-shadow:inset 0 0 0 1.5px var(--line);font:800 22px/1.15 'Manrope';color:var(--text)}
.row .e{font-size:30px;width:36px;text-align:center}
.row small{display:block;margin-top:4px;font:700 16px/1.2 'Manrope';color:var(--body)}
.tick{display:grid;place-items:center;flex:none;width:36px;height:36px;border-radius:50%;background:var(--acc);color:var(--bg);font:900 20px/1 'Manrope'}
.glow{position:absolute;border-radius:50%;filter:blur(10px)}
"""

FAM = {
 'jetup': """:root{--bg:#0b0912;--text:#f6f3ff;--body:#cfc8e6;--acc:#cbfb61;--acc2:#e8c25a;--panel:rgba(24,20,36,.94);--line:rgba(155,124,255,.45);--chipbg:rgba(19,15,30,.96);
 --ebbg:rgba(203,251,97,.10);--rim:rgba(155,124,255,.35);--urlbg:#cbfb61;--urlc:#14110b;--urlsh:rgba(203,251,97,.25);
 --goldg:linear-gradient(180deg,#fff3c4,#f3d27a 40%,#c99a2e);
 --bgimg:radial-gradient(760px 560px at 82% 30%,rgba(140,108,231,.40),transparent 70%),radial-gradient(620px 460px at 4% 100%,rgba(232,194,90,.18),transparent 70%),radial-gradient(500px 360px at 20% 10%,rgba(203,251,97,.07),transparent 70%),linear-gradient(160deg,#160d2e,#0b0912 55%,#07050f)}""",
 'tribe': """:root{--bg:#07060a;--text:#fffaf0;--body:#ddd3bf;--acc:#f3d27a;--acc2:#e8c25a;--panel:rgba(20,16,10,.94);--line:rgba(243,210,122,.40);--chipbg:rgba(18,14,8,.96);
 --ebbg:rgba(243,210,122,.10);--rim:rgba(243,210,122,.32);--urlbg:linear-gradient(180deg,#ffe9a8,#e8b84a);--urlc:#1a1205;--urlsh:rgba(243,210,122,.28);
 --goldg:linear-gradient(180deg,#fff3c4,#f3d27a 40%,#c99a2e);
 --bgimg:radial-gradient(700px 560px at 84% 34%,rgba(243,190,90,.22),transparent 70%),radial-gradient(600px 460px at 0% 100%,rgba(243,190,90,.12),transparent 70%),linear-gradient(160deg,#16110a,#08070a 55%,#050406)}
 .url i{background:#1a1205;color:#ffe9a8}""",
 'canton': """:root{--bg:#040506;--text:#ffffff;--body:#d8d2c4;--acc:#ffd47c;--acc2:#e8b862;--panel:rgba(12,11,9,.94);--line:rgba(242,173,60,.42);--chipbg:rgba(10,9,7,.96);
 --ebbg:rgba(242,173,60,.10);--rim:rgba(242,173,60,.38);--urlbg:linear-gradient(180deg,#ffe2aa,#f2ad3c);--urlc:#1a1205;--urlsh:rgba(242,173,60,.28);
 --goldg:linear-gradient(180deg,#fff6dd,#ffd47c 38%,#f2ad3c 70%,#c27a14);
 --bgimg:radial-gradient(760px 560px at 8% -6%,rgba(242,173,60,.26),transparent 62%),radial-gradient(700px 520px at 92% 88%,rgba(242,173,60,.18),transparent 64%),linear-gradient(180deg,#0a0b0d,#050607)}
 h1{font-family:'Outfit';font-weight:900;letter-spacing:-.02em;line-height:.98}
 .url i{background:#1a1205;color:#ffe2aa}""",
}

BRAND = {
 'jetup': f'<div class="brand"><img src="{DISC}" alt=""><div><b>JETUP GUIDE</b><small>BY MTG 👑 YOUR DIGITAL ARCHITECT</small></div></div>',
 'tribe': f'<div class="brand"><img src="{FACE}" alt="" style="box-shadow:0 0 0 3px #f3d27a"><div><b>MTG TRIBE</b><small>MTG 👑 YOUR DIGITAL ARCHITECT</small></div></div>',
 'canton': f'<div class="brand"><img src="{CANTON}" alt="" style="width:auto;height:44px;border-radius:0"></div>',
}

def img(p): return A(p)

# ---------------------------------------------------------------- page heroes (right half, 500 x 554)
def hero_jetup_home():
    return f'''<div class="glow" style="left:90px;top:110px;width:320px;height:320px;background:rgba(203,251,97,.20)"></div>
<img class="ab" src="{DISC}" alt="" style="left:95px;top:112px;width:310px;height:310px;filter:drop-shadow(0 26px 50px rgba(0,0,0,.6))">
<div class="chip" style="left:0;top:40px"><span class="e">🔒</span>Your own account</div>
<div class="chip" style="right:0;top:118px"><span class="e">🤖</span>Sonic AI</div>
<div class="chip" style="left:40px;top:420px"><span class="e">🔁</span>CopyX</div>
<div class="chip" style="right:6px;top:470px"><span class="e">✂️</span>The 70/30 split</div>'''

def hero_get_started():
    rows = [('done', 'Create your account'), ('done', 'Link TAG Markets'), ('done', 'Verify your identity'), ('now', 'Fund your account'), ('', 'Connect Sonic AI'), ('', 'Claim the $100 promo')]
    r = ''
    for i, (s, t) in enumerate(rows):
        mark = '<span class="tick">✓</span>' if s == 'done' else f'<span class="tick" style="background:{"#cbfb61" if s == "now" else "rgba(255,255,255,.12)"};color:{"#14110b" if s == "now" else "#cfc8e6"};font-size:18px">{i + 1}</span>'
        st = 'box-shadow:inset 0 0 0 3px #cbfb61,0 0 30px rgba(203,251,97,.25);background:rgba(203,251,97,.10)' if s == 'now' else ''
        r += f'<div class="row" style="height:52px;font-size:18px;padding:0 14px;gap:12px;{st}">{mark}{t}</div>'
    return f'''<div class="ab" style="left:80px;top:0;width:340px;height:484px;border-radius:52px;padding:12px;background:linear-gradient(145deg,#f7dd8d,#9c6f1f 40%,#fff1b8 60%,#9c6f1f);box-shadow:0 30px 70px rgba(0,0,0,.6)">
 <div style="width:100%;height:100%;border-radius:42px;background:#0f0b1a;padding:52px 18px 18px;display:flex;flex-direction:column;gap:10px;position:relative">
  <div style="position:absolute;left:50%;top:16px;width:90px;height:24px;margin-left:-45px;border-radius:14px;background:#000"></div>
  <p style="font:800 15px/1 'Manrope';letter-spacing:.16em;color:#e8c25a;margin:0 0 6px 4px">JOIN JETUP · 6 PARTS</p>{r}
 </div></div>
<div class="chip" style="left:140px;top:500px"><span class="e">👆</span>Every tap shown</div>'''

def hero_how():
    rows = [('🚀', 'JetUP', 'The community that trains you'), ('🏦', 'TAG Markets', 'The broker: your account, your name'), ('🔁', 'CopyX', 'Copies the trades into it'),
            ('🤖', 'Sonic AI', 'The strategy, trading gold'), ('🙋', 'You', 'You decide, you stay in control')]
    r = ''.join(f'<div class="row" style="height:84px"><span class="e">{e}</span><div>{t}<small>{s}</small></div></div>' for e, t, s in rows)
    return f'''<div class="card" style="left:10px;top:20px;width:480px;padding:22px;display:flex;flex-direction:column;gap:12px">
 <p style="font:800 15px/1 'Manrope';letter-spacing:.16em;color:#e8c25a;margin:0 0 2px 6px">5 NAMES, 1 PICTURE</p>{r}</div>'''

def hero_partner():
    rows = [('💼', 'Lot Commission', 'Over 10 levels'), ('📈', 'Profit Share', 'On Sonic AI at TAG Markets'), ('♾️', 'Infinity Bonus', 'Explained simply'), ('🌍', 'Global Pool', 'And the rewards')]
    r = ''.join(f'<div class="row" style="height:86px"><span class="e">{e}</span><div>{t}<small>{s}</small></div></div>' for e, t, s in rows)
    return f'''<div class="card" style="left:10px;top:30px;width:480px;padding:22px;display:flex;flex-direction:column;gap:12px">
 <p style="font:800 15px/1 'Manrope';letter-spacing:.16em;color:#e8c25a;margin:0 0 2px 6px">THE FOUR PARTS</p>{r}</div>
<div class="chip" style="left:60px;top:486px"><span class="e">✅</span>The $250 rule, explained</div>'''

def hero_promo():
    return '''<div class="glow" style="left:110px;top:30px;width:300px;height:300px;background:rgba(232,194,90,.28)"></div>
<div class="ab e" style="left:110px;top:24px;width:300px;text-align:center;font-size:230px;line-height:300px">🎁</div>
<div class="ab e" style="left:70px;top:40px;font-size:44px">✨</div><div class="ab e" style="left:420px;top:150px;font-size:40px">✨</div><div class="ab e" style="left:40px;top:250px;font-size:34px">✨</div>
<div class="card" style="left:0;top:350px;width:236px;height:130px;padding:22px 24px;box-shadow:inset 0 0 0 3px #9b7cff,0 24px 60px rgba(0,0,0,.5)">
 <p style="font:800 15px/1 'Manrope';letter-spacing:.14em;color:#cfc6ee">⚡ SONIC AI</p><p style="margin-top:10px;font:400 62px/1 'Anton';color:#c9b8ff">$50</p></div>
<div class="card" style="left:258px;top:350px;width:242px;height:130px;padding:22px 24px;background:rgba(40,30,12,.96);box-shadow:inset 0 0 0 3px #f3d27a,0 0 50px rgba(232,194,90,.3)">
 <p style="font:800 15px/1 'Manrope';letter-spacing:.14em;color:#f3d27a">🎁 PROMO ACCOUNT</p><p style="margin-top:10px;font:400 62px/1 'Anton';color:#f3d27a">$200</p></div>
<div class="chip" style="left:120px;top:500px"><span class="e">▶️</span>2:18 explainer video</div>'''

def hero_bix():
    return '''<div class="glow" style="left:60px;top:90px;width:380px;height:260px;background:rgba(203,251,97,.18)"></div>
<div class="ab" style="left:40px;top:96px;width:420px;height:264px;border-radius:26px;transform:rotate(-8deg);background:linear-gradient(135deg,#e4ff8a,#cbfb61 45%,#9ed636);box-shadow:0 34px 70px rgba(0,0,0,.6),inset 0 0 0 2px rgba(255,255,255,.4);padding:30px 32px">
 <div style="display:flex;justify-content:space-between;align-items:center"><span style="font:900 46px/1 'Manrope';color:#14110b;letter-spacing:.02em">BIX</span><span style="font:800 18px/1 'Manrope';color:#14110b;letter-spacing:.1em">CARD</span></div>
 <div style="margin-top:36px;width:62px;height:48px;border-radius:10px;background:linear-gradient(135deg,#fff1b8,#c99a2e)"></div>
 <p style="margin-top:28px;font:700 24px/1 'JetBrains Mono';color:#14110b;letter-spacing:.12em">•••• •••• ••••</p></div>
<div class="chip" style="left:0;top:400px"><span class="e">📱</span>BixPay wallet</div>
<div class="chip" style="right:0;top:400px"><span class="e">🔗</span>Link with a QR code</div>
<div class="chip" style="left:90px;top:470px"><span class="e">🏷️</span>Card prices explained</div>'''

def hero_checks():
    rows = ['Who holds your money', 'Who regulates TAG Markets', 'Are the results real?', 'What 24x Amplify does', 'How you take money out']
    r = ''.join(f'<div class="row" style="height:72px"><span class="tick">✓</span><span>{t}</span></div>' for t in rows)
    return f'''<div class="card" style="left:10px;top:34px;width:480px;padding:24px;display:flex;flex-direction:column;gap:12px">
 <p style="font:800 15px/1 'Manrope';letter-spacing:.16em;color:#e8c25a;margin:0 0 2px 6px">CHECK THESE 5 FIRST</p>{r}</div>'''

def hero_videos():
    def tile(src, x, y, w, h, r=16):
        return (f'<div class="ab" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px;overflow:hidden;box-shadow:0 0 0 2px rgba(155,124,255,.5),0 20px 50px rgba(0,0,0,.55)">'
                f'<img src="{img(src)}" alt="" style="width:100%;height:100%;object-fit:cover;display:block"></div>')
    play = lambda x, y, s: f'<div class="ab" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:rgba(255,255,255,.92);display:grid;place-items:center;box-shadow:0 10px 30px rgba(0,0,0,.5)"><span style="margin-left:{s//10}px;width:0;height:0;border-left:{s//3}px solid #14110b;border-top:{s//5}px solid transparent;border-bottom:{s//5}px solid transparent"></span></div>'
    return (tile('jetup/img/cover-signup-training-v4-4.jpg', 0, 30, 340, 191) + play(135, 90, 70)
            + tile('jetup/img/cover-explainer-100-promo.jpg', 0, 240, 165, 93, 12) + tile('jetup/img/cover-explainer-who-does-what.jpg', 175, 240, 165, 93, 12)
            + tile('jetup/img/cover-explainer-simple-picture-v3.jpg', 0, 345, 165, 93, 12) + tile('jetup/img/cover-tutorial-part-2-v2.jpg', 175, 345, 165, 93, 12)
            + f'<div class="ab" style="left:360px;top:20px;width:140px;height:250px;border-radius:24px;padding:6px;background:linear-gradient(145deg,#f7dd8d,#9c6f1f 40%,#fff1b8 60%,#9c6f1f);box-shadow:0 24px 60px rgba(0,0,0,.6)"><img src="{img("jetup/img/cover-tutorial-part-1-v3.jpg")}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:19px;display:block"></div>'
            + play(395, 110, 70)
            + '<div class="chip" style="left:40px;top:470px"><span class="e">🎬</span>10 videos, free</div>'
            + '<div class="chip" style="left:270px;top:470px"><span class="e">📱</span>Phone tutorials</div>')

def hero_faq():
    q = lambda t, y: f'<div class="ab" style="right:0;top:{y}px;max-width:420px;padding:18px 24px;border-radius:24px 24px 6px 24px;background:rgba(155,124,255,.22);box-shadow:inset 0 0 0 2px rgba(155,124,255,.55);font:800 25px/1.2 \'Manrope\';color:#f6f3ff">{t}</div>'
    return (q('How much do I need to start?', 30) + q('BEP20 or TRC20?', 130) + q('Can I take profits out?', 230)
            + '<div class="ab" style="left:0;top:340px;max-width:440px;padding:20px 26px;border-radius:24px 24px 24px 6px;background:#cbfb61;color:#14110b;font:800 26px/1.2 \'Manrope\';box-shadow:0 20px 50px rgba(203,251,97,.25)">✓ All 21 answered, in plain English</div>'
            + '<div class="chip" style="left:0;top:470px"><span class="e">🎁</span>The promo</div><div class="chip" style="left:180px;top:470px"><span class="e">📉</span>24x Amplify</div>')

def hero_glossary():
    words = ['AMPLIFY', 'CU NUMBER', 'KYC', 'COPYX', 'MT5', 'LOT', 'CFD', 'SONIC AI']
    w = ''.join(f'<span style="display:inline-flex;align-items:center;height:48px;padding:0 18px;border-radius:14px;background:rgba(255,255,255,.06);box-shadow:inset 0 0 0 2px rgba(155,124,255,.45);font:400 26px/1 \'Anton\';letter-spacing:.04em;color:#f6f3ff">{x}</span>' for x in words)
    return f'''<div class="card" style="left:10px;top:30px;width:480px;padding:28px 30px">
 <p style="font:800 15px/1 'Manrope';letter-spacing:.16em;color:#e8c25a">WORD OF THE DAY</p>
 <p style="margin-top:14px;font:400 70px/1 'Anton';color:#cbfb61">XAU/USD</p>
 <p style="margin-top:12px;font:800 26px/1.25 'Manrope';color:#f6f3ff">= the price of gold in US dollars. Sonic AI trades it.</p></div>
<div class="ab" style="left:10px;top:290px;width:480px;display:flex;flex-wrap:wrap;gap:12px">{w}</div>'''

def hero_downloads():
    doc = lambda x, y, r, t, c: (f'<div class="ab" style="left:{x}px;top:{y}px;width:230px;height:300px;border-radius:18px;transform:rotate({r}deg);background:#f6f3ff;box-shadow:0 24px 60px rgba(0,0,0,.55);padding:22px">'
                                 f'<span style="display:inline-block;padding:7px 12px;border-radius:8px;background:{c};color:#fff;font:800 17px/1 \'Manrope\';letter-spacing:.08em">PDF</span>'
                                 f'<p style="margin-top:16px;font:800 25px/1.15 \'Manrope\';color:#14110b">{t}</p>'
                                 + ''.join(f'<div style="margin-top:{14 if i == 0 else 9}px;height:9px;border-radius:5px;background:#ddd6ee;width:{w}%"></div>' for i, w in enumerate((100, 86, 94, 70, 88)))
                                 + '</div>')
    return (doc(10, 80, -10, 'BIX Card guide', '#9b7cff') + doc(135, 50, 4, 'Business plan', '#e371fc') + doc(250, 96, 12, 'Onboarding guide', '#8c6ce7')
            + '<div class="ab" style="left:350px;top:380px;width:110px;height:110px;border-radius:50%;background:#cbfb61;display:grid;place-items:center;box-shadow:0 18px 44px rgba(203,251,97,.35);font:900 56px/1 \'Manrope\';color:#14110b">↓</div>'
            + '<div class="chip" style="left:30px;top:470px"><span class="e">📄</span>7 PDFs, free</div>')

def hero_disclaimer():
    return '''<div class="glow" style="left:120px;top:60px;width:260px;height:260px;background:rgba(203,251,97,.16)"></div>
<div class="ab e" style="left:120px;top:40px;width:260px;text-align:center;font-size:210px;line-height:280px">🛡️</div>
<div class="chip" style="left:0;top:340px"><span class="e">📚</span>Education only</div>
<div class="chip" style="right:0;top:340px"><span class="e">🧭</span>Not financial advice</div>
<div class="chip" style="left:40px;top:412px"><span class="e">🔗</span>Referral links marked</div>
<div class="chip" style="left:110px;top:484px"><span class="e">⚠️</span>Risks said plainly</div>'''

def hero_exposure():
    return '''<div class="card" style="left:30px;top:30px;width:440px;padding:26px">
 <div style="border-radius:18px;background:#07050d;box-shadow:inset 0 0 0 2px rgba(203,251,97,.45);padding:20px 24px;text-align:right">
  <p style="font:800 16px/1 'Manrope';letter-spacing:.14em;color:#9c95b8">EXPOSURE</p><p style="margin-top:8px;font:400 84px/1 'Anton';color:#cbfb61">$1,200</p></div>
 <div class="row" style="margin-top:16px;justify-content:space-between"><span>Your deposit</span><span style="font:700 28px/1 'JetBrains Mono'">$50</span></div>
 <div class="row" style="margin-top:12px;justify-content:space-between"><span>Amplify</span><span style="font:700 28px/1 'JetBrains Mono';color:#e8c25a">× 24</span></div>
 <div class="row" style="margin-top:12px;justify-content:space-between;box-shadow:inset 0 0 0 2px rgba(203,251,97,.6)"><span>A 1% move in gold</span><span style="font:700 28px/1 'JetBrains Mono'">± $12</span></div></div>
<div class="chip" style="left:100px;top:486px"><span class="e">📱</span>Works on your phone</div>'''

def hero_split():
    return '''<div class="card" style="left:20px;top:40px;width:460px;padding:28px">
 <p style="font:800 16px/1 'Manrope';letter-spacing:.14em;color:#e8c25a">EXAMPLE: A $10 PROFIT</p>
 <div style="margin-top:20px;display:flex;height:96px;border-radius:18px;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,0,.4)">
  <div style="width:70%;background:#cbfb61;color:#14110b;display:flex;flex-direction:column;justify-content:center;padding-left:20px"><b style="font:400 46px/1 'Anton'">70%</b><span style="font:800 17px/1 'Manrope'">yours</span></div>
  <div style="width:30%;background:#9b7cff;color:#fff;display:flex;flex-direction:column;justify-content:center;padding-left:14px"><b style="font:400 46px/1 'Anton'">30%</b><span style="font:800 17px/1 'Manrope'">fee</span></div></div>
 <div class="row" style="margin-top:20px;justify-content:space-between"><span>You keep</span><span style="font:700 28px/1 'JetBrains Mono';color:#cbfb61">$7.00</span></div>
 <div class="row" style="margin-top:12px;justify-content:space-between"><span>Performance fee</span><span style="font:700 28px/1 'JetBrains Mono';color:#c9b8ff">$3.00</span></div></div>
<div class="chip" style="left:70px;top:470px"><span class="e">🙌</span>No fee on a losing trade</div>'''

def hero_dashboard():
    rows = [('Bellver Card', 'Spend your crypto like cash'), ('JetUP + TAG Markets', 'Copy trading, explained'), ('ClickBaitPays', 'Advertise and view ads'), ('Bitcoin Wealth', 'A way to stack Bitcoin'), ('ALTRUVA', 'Smart contract plan in USDT')]
    r = ''.join(f'<div class="row" style="height:70px"><span style="flex:none;width:44px;height:44px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(180deg,#ffe9a8,#e8b84a);color:#1a1205;font:400 28px/1 \'Anton\'">{i + 1}</span><div>{t}<small>{s}</small></div></div>' for i, (t, s) in enumerate(rows))
    return f'''<div class="card" style="left:10px;top:22px;width:480px;padding:22px;display:flex;flex-direction:column;gap:11px">
 <p style="font:800 15px/1 'Manrope';letter-spacing:.16em;color:#f3d27a;margin:0 0 2px 6px">OUR INCOME STREAMS, RANKED</p>{r}</div>
<div class="chip" style="left:20px;top:494px"><span class="e">📈</span>Live prices</div><div class="chip" style="left:200px;top:494px"><span class="e">🧮</span>Tools + tutorials</div>'''

def hero_group():
    return f'''<div class="ab" style="left:90px;top:40px;width:320px;height:320px;border-radius:50%;padding:10px;background:conic-gradient(from 210deg,#7a4a0c,#ffe2aa,#f2ad3c,#c27a14,#ffe2aa,#7a4a0c);box-shadow:0 0 70px rgba(243,190,90,.45),0 30px 70px rgba(0,0,0,.6)">
 <img src="{FACE}" alt="" style="width:100%;height:100%;border-radius:50%;display:block"></div>
<div class="chip" style="left:0;top:392px"><span class="e">💬</span>Ask questions</div>
<div class="chip" style="right:0;top:392px"><span class="e">📚</span>Learn together</div>
<div class="chip" style="left:100px;top:466px"><span class="e">🚀</span>Grow together, free</div>'''

def hero_canton_hub():
    pts = [(0, 250), (60, 200), (120, 285), (180, 225), (240, 300), (300, 205), (360, 265), (420, 180), (480, 235)]
    poly = ' '.join(f'{x},{y}' for x, y in pts)
    area = 'M0,420 L' + ' L'.join(f'{x},{y}' for x, y in pts) + ' L480,420 Z'
    return f'''<div class="card" style="left:10px;top:30px;width:480px;height:430px;overflow:hidden;padding:0">
 <svg viewBox="0 0 480 420" style="position:absolute;left:0;top:10px;width:480px;height:420px"><defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2ad3c" stop-opacity=".35"/><stop offset="1" stop-color="#f2ad3c" stop-opacity="0"/></linearGradient></defs>
  <line x1="0" x2="480" y1="140" y2="140" stroke="#ff8a7a" stroke-opacity=".6" stroke-width="3" stroke-dasharray="12 12"/><line x1="0" x2="480" y1="320" y2="320" stroke="#3ddc84" stroke-opacity=".6" stroke-width="3" stroke-dasharray="12 12"/>
  <path d="{area}" fill="url(#ga)"/><polyline points="{poly}" fill="none" stroke="#f2ad3c" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="472" cy="233" r="12" fill="#ffe2aa"/></svg>
 <span class="ab" style="left:20px;top:110px;font:800 16px/1 'DM Sans';letter-spacing:.12em;color:#ffb4a2">RESISTANCE</span>
 <span class="ab" style="left:20px;top:340px;font:800 16px/1 'DM Sans';letter-spacing:.12em;color:#9ff5c6">SUPPORT</span>
 <span class="ab" style="right:20px;top:24px;font:800 16px/1 'DM Sans';letter-spacing:.12em;color:#ffe2aa">CC / USD · WEEKLY</span></div>
<div class="chip" style="left:0;top:484px"><span class="e">📊</span>3 scenarios</div><div class="chip" style="left:206px;top:484px"><span class="e">📰</span>CNTN stock news</div>'''

# ---------------------------------------------------------------- the pages
SPECS = [
 dict(slug='jetup-home', fam='jetup', page='/jetup/', eb='JETUP + TAG MARKETS', h='Check first.<br><em>Then start.</em>', hs=112,
      sub='How it works, the risks and every step, in plain English.', url='mtgtribe.com/jetup', hero=hero_jetup_home,
      alt='JetUP and TAG Markets guide by MTG: check first, then start'),
 dict(slug='jetup-get-started', fam='jetup', page='/jetup/get-started/', eb='STEP BY STEP · 6 PARTS', h='Join JetUP,<br><em>one tap</em><br>at a time', hs=100,
      sub='From sign-up to the $100 promo.', url='mtgtribe.com/jetup/get-started', hero=hero_get_started,
      alt='How to join JetUP and TAG Markets in 6 parts, every tap shown'),
 dict(slug='jetup-how-it-works', fam='jetup', page='/jetup/how-it-works/', eb='HOW IT WORKS', h='5 names.<br><em>1 simple</em><br>picture.', hs=104,
      sub='Who does what, and where your money sits.', url='mtgtribe.com/jetup/how-it-works', hero=hero_how,
      alt='How JetUP, TAG Markets, CopyX and Sonic AI fit together'),
 dict(slug='jetup-partner-plan', fam='jetup', page='/jetup/partner-plan/', eb='PARTNER PLAN', h='The partner<br>plan, in<br><em>plain English</em>', hs=96,
      sub='Every part explained, rules included.', url='mtgtribe.com/jetup/partner-plan', hero=hero_partner,
      alt='The JetUP partner plan explained in plain English'),
 dict(slug='jetup-promo', fam='jetup', page='/jetup/promo/', eb='DENNIS FAST START PROMO', h='The <span class="g">$100</span><br>fast start<br><em>promo</em>', hs=104,
      sub='How it works and how to claim it.', url='mtgtribe.com/jetup/promo', hero=hero_promo,
      alt='The $100 Fast Start Promo: how it works and how to claim it'),
 dict(slug='jetup-bix-card', fam='jetup', page='/jetup/bix-card/', eb='BIX CARD + JETUP', h='The BIX Card,<br><em>set up right</em>', hs=100,
      sub='Wallet, card, fees and linking it to JetUP, step by step.', url='mtgtribe.com/jetup/bix-card', hero=hero_bix,
      alt='The BIX Card with JetUP: setup, fees and linking'),
 dict(slug='jetup-five-checks', fam='jetup', page='/jetup/five-checks/', eb='HONEST REVIEW', h='5 checks<br><em>before</em><br>you start', hs=108,
      sub='Lost money before? Start here.', url='mtgtribe.com/jetup/five-checks', hero=hero_checks,
      alt='JetUP and TAG Markets review: 5 checks before you start'),
 dict(slug='jetup-videos', fam='jetup', page='/jetup/videos/', eb='VIDEO LIBRARY', h='Watch it.<br><em>Then do it.</em>', hs=108,
      sub='Explainers, the 9:09 training and phone tutorials.', url='mtgtribe.com/jetup/videos', hero=hero_videos,
      alt='Every JetUP and TAG Markets video by MTG in one place'),
 dict(slug='jetup-faq', fam='jetup', page='/jetup/faq/', eb='21 QUESTIONS', h='Your JetUP<br><em>questions,</em><br>answered', hs=100,
      sub='Deposits, withdrawals and the promo.', url='mtgtribe.com/jetup/faq', hero=hero_faq,
      alt='JetUP and TAG Markets questions answered'),
 dict(slug='jetup-glossary', fam='jetup', page='/jetup/glossary/', eb='24 WORDS EXPLAINED', h='JetUP words,<br><em>made simple</em>', hs=100,
      sub='Every word in the guide, in plain English.', url='mtgtribe.com/jetup/glossary', hero=hero_glossary,
      alt='JetUP and TAG Markets glossary in plain English'),
 dict(slug='jetup-downloads', fam='jetup', page='/jetup/downloads/', eb='FREE DOWNLOADS', h='The PDF<br>guides,<br><em>free</em>', hs=112,
      sub='Guides, business plan and decks.', url='mtgtribe.com/jetup/downloads', hero=hero_downloads,
      alt='JetUP and TAG Markets PDF guides to download'),
 dict(slug='jetup-disclaimer', fam='jetup', page='/jetup/disclaimer/', eb='READ THIS FIRST', h='Independent<br><em>and honest</em>', hs=100,
      sub='What this guide is, what it is not, and which links are referral links.', url='mtgtribe.com/jetup/disclaimer', hero=hero_disclaimer,
      alt='Disclaimer for the independent JetUP and TAG Markets guide'),
 dict(slug='jetup-exposure-calculator', fam='jetup', page='/jetup/tools/exposure-calculator/', eb='FREE CALCULATOR', h='Exposure<br><em>calculator</em>', hs=108,
      sub='See what 24x Amplify does to a deposit before you start.', url='mtgtribe.com/jetup/tools/exposure-calculator', hero=hero_exposure,
      alt='Exposure Calculator: what 24x Amplify does to a deposit'),
 dict(slug='jetup-profit-split-calculator', fam='jetup', page='/jetup/tools/profit-split-calculator/', eb='FREE CALCULATOR', h='Profit split<br><em>calculator</em>', hs=104,
      sub='Your 70% of a Sonic AI profit, and the 30% fee.', url='mtgtribe.com/jetup/tools/profit-split-calculator', hero=hero_split,
      alt='Profit Split Calculator: the 70/30 on TAG Markets CopyX'),
 dict(slug='tribe-dashboard', fam='tribe', page='/dashboard/', eb='THE TRIBE DASHBOARD', h='5 income<br>streams.<br><span class="g">Ranked.</span>', hs=108,
      sub='Plus prices, tutorials and tools.', url='mtgtribe.com/dashboard', hero=hero_dashboard,
      alt='The MTG TRIBE dashboard: income streams ranked, prices, tutorials and tools'),
 dict(slug='tribe-whatsapp', fam='tribe', page='/group/', eb='MTG TRIBE ON WHATSAPP', h='Don\'t learn<br>this <span class="g">alone.</span>', hs=110,
      sub='Join the tribe: action takers who learn, ask and grow together.', url='mtgtribe.com/group', hero=hero_group,
      alt='Join the MTG TRIBE WhatsApp group'),
 dict(slug='canton-weekly', fam='canton', page='/canton-weekly/', eb='EVERY SUNDAY · BY MTG 👑', h='Canton Coin,<br>every <span class="g">Sunday</span>', hs=92,
      sub='Price, levels, 3 scenarios, CNTN news.', url='mtgtribe.com/canton-weekly', hero=hero_canton_hub,
      alt='Canton Coin weekly report by MTG, every Sunday'),
]

def page_html(s):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{BASE}{FAM[s['fam']]}</style></head>
<body style="--hs:{s.get('hs', 96)}px"><div class="bg"></div><div class="grid"></div><div class="frame"></div>
{BRAND[s['fam']]}
<div class="txt"><span class="eb">{s['eb']}</span><h1>{s['h']}</h1><p class="sub">{html.escape(s['sub'])}</p></div>
<div class="url"><i>▶</i>{s['url']}</div>
<div class="hero">{s['hero']()}</div>
<script>window.fit=()=>{{const t=document.querySelector('.txt');let v=parseFloat(getComputedStyle(document.body).getPropertyValue('--hs'));
while(t.scrollHeight>t.clientHeight+1&&v>60){{v-=2;document.body.style.setProperty('--hs',v+'px');}}
const u=document.querySelector('.url');let f=23;while(u.getBoundingClientRect().right>648&&f>15){{f-=1;u.style.fontSize=f+'px';}}return v;}};</script></body></html>'''

def render(specs):
    tmp = tempfile.mkdtemp(); jobs = []
    for s in specs:
        h = page_html(s)
        assert '\u2014' not in h and '\u2013' not in h, 'dash in ' + s['slug']
        f = os.path.join(tmp, s['slug'] + '.html'); open(f, 'w').write(h)
        jobs.append([f, os.path.join(tmp, s['slug'] + '.png')])
    js = os.path.join(tmp, 'r.js')
    open(js, 'w').write("""const {chromium}=require('playwright');const J=%s;(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});
for(const [f,o] of J){await p.goto('file://'+f,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));const v=await p.evaluate(()=>window.fit());console.log(f.split('/').pop(),'headline',v);await p.waitForTimeout(150);await p.screenshot({path:o});}
await b.close();})();""" % json.dumps(jobs))
    subprocess.run(['node', js], check=True)
    os.makedirs(OUT, exist_ok=True); res = []
    for s, (_, png) in zip(specs, jobs):
        out = os.path.join(OUT, s['slug'] + '.jpg'); im = Image.open(png).convert('RGB')
        for q in (88, 84, 80, 76):
            im.save(out, 'JPEG', quality=q, optimize=True, progressive=True)
            if os.path.getsize(out) < 200 * 1024: break
        res.append((s['slug'], os.path.getsize(out) // 1024))
    return res

def sheet():
    fs = [os.path.join(OUT, s['slug'] + '.jpg') for s in SPECS if os.path.exists(os.path.join(OUT, s['slug'] + '.jpg'))]
    cols = 3; w, h = 600, 315; sh = Image.new('RGB', (cols * w + (cols - 1) * 10, ((len(fs) + cols - 1) // cols) * (h + 10)), 'white')
    for i, f in enumerate(fs): sh.paste(Image.open(f).resize((w, h)), ((i % cols) * (w + 10), (i // cols) * (h + 10)))
    sh.save(os.path.join(ROOT, 'tools', 'og', 'sheet.jpg'), quality=82)

if __name__ == '__main__':
    want = set(sys.argv[1:])
    todo = [s for s in SPECS if not want or s['slug'] in want]
    for slug, kb in render(todo): print(f'{slug}: {kb} KB')
    sheet()
