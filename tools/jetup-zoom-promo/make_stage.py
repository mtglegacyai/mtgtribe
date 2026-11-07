# JetUP Zoom promo (9:16, 1080x1920): writes stage/stage.html. Every frame is a pure function of time (engine at the end).
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
bgchart, hero, f_za, f_ng, f_in = open(os.path.join(HERE, 'parts.txt')).read().split('\n=====\n')
gold_svg = re.search(r'<svg viewBox="0 0 338 250">.*?</svg>', hero, re.S).group(0)


def uniq(svg, sfx):
    """Copy an SVG with its ids renamed, so the same artwork can appear twice in one page."""
    ids = set(re.findall(r'id="([^"]+)"', svg))
    for i in ids:
        svg = svg.replace(f'id="{i}"', f'id="{i}{sfx}"').replace(f'url(#{i})', f'url(#{i}{sfx})')
    return svg


def flag(f, sfx):
    return uniq(f, sfx)


IC = {
    'landmark': '<path d="M3 22h18"/><path d="M6 18v-7"/><path d="M10 18v-7"/><path d="M14 18v-7"/><path d="M18 18v-7"/><path d="m12 2 8 5H4z"/>',
    'id': '<rect width="20" height="14" x="2" y="5" rx="2"/><circle cx="8" cy="12" r="2.5"/><path d="M14 10h5"/><path d="M14 14h4"/>',
    'bot': '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
    'link': '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    'cal': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    'ban': '<circle cx="12" cy="12" r="10"/><path d="m4.9 4.9 14.2 14.2"/>',
    'alert': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    'video': '<path d="m16 13 5.2 3.5a.5.5 0 0 0 .8-.4V7.9a.5.5 0 0 0-.8-.4L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'shield': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    'tap': '<path d="M22 14a8 8 0 0 1-8 8"/><path d="M18 11v-1a2 2 0 0 0-2-2a2 2 0 0 0-2 2"/><path d="M14 10V9a2 2 0 0 0-2-2a2 2 0 0 0-2 2v1"/><path d="M10 9.5V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v10"/><path d="M18 11a2 2 0 1 1 4 0v3a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>',
    'down': '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
}


def ic(k, cls='i'):
    return f'<svg class="{cls}" viewBox="0 0 24 24">{IC[k]}</svg>'


GIFT = '''<svg viewBox="0 0 300 300" class="giftsvg"><defs>
<linearGradient id="gbx" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b56cf6"/><stop offset="1" stop-color="#6d4fd8"/></linearGradient>
<linearGradient id="glid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d48cff"/><stop offset="1" stop-color="#9b6cf0"/></linearGradient>
<linearGradient id="grib" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e8c25a"/><stop offset=".5" stop-color="#fff1bf"/><stop offset="1" stop-color="#e8c25a"/></linearGradient></defs>
<g class="gbody"><rect x="52" y="130" width="196" height="150" rx="14" fill="url(#gbx)"/><rect x="134" y="130" width="32" height="150" fill="url(#grib)"/>
<rect x="52" y="130" width="196" height="150" rx="14" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="2"/></g>
<g class="glid"><rect x="38" y="92" width="224" height="46" rx="12" fill="url(#glid)"/><rect x="134" y="92" width="32" height="46" fill="url(#grib)"/>
<path d="M150 92c-14-30-58-40-62-14-3 18 30 18 62 14zM150 92c14-30 58-40 62-14 3 18-30 18-62 14z" fill="none" stroke="url(#grib)" stroke-width="12" stroke-linecap="round"/></g></svg>'''

CSS = r"""
:root{--bg:#0b0912;--text:#f6f3ff;--body:#cfc8e6;--muted:#9c95b8;--vio:#9b7cff;--pink:#e371fc;--lime:#cbfb61;--gold:#e8c25a;--gold-hi:#ffe08f;--red:#ff5f7a;
 --grad:linear-gradient(100deg,#8c6ce7 0%,#b56cf6 45%,#e371fc 100%);--goldg:linear-gradient(180deg,#fff1bf 0%,#ffe08f 35%,#e8c25a 70%,#c99a3a 100%);
 --f-d:'Anton',Impact,sans-serif;--f-b:'Manrope',system-ui,sans-serif;--emoji:'Noto Color Emoji'}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--bg)}
body{font-family:var(--f-b);color:var(--text);-webkit-font-smoothing:antialiased}
#v{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--bg)}
.glow{position:absolute;border-radius:50%;filter:blur(10px);pointer-events:none}
#g1{left:-260px;top:120px;width:900px;height:700px;background:radial-gradient(closest-side,rgba(140,108,231,.34),transparent)}
#g2{right:-300px;top:900px;width:900px;height:800px;background:radial-gradient(closest-side,rgba(232,194,90,.18),transparent)}
#g3{left:90px;bottom:-320px;width:900px;height:600px;background:radial-gradient(closest-side,rgba(227,113,252,.20),transparent)}
#grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:60px 60px;
 -webkit-mask-image:radial-gradient(900px 1200px at 50% 45%,#000 30%,transparent 80%)}
.bgchart{position:absolute;left:-40px;width:1160px;top:1060px;height:520px;opacity:.07}
.ab{position:absolute;will-change:transform,opacity}
.c{left:0;right:0;text-align:center}
svg.i{fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.em{font-family:var(--emoji);font-weight:400}
.sep{font-family:Inter,sans-serif;font-weight:300;color:var(--gold);margin:0 8px}

/* top bar */
#top{left:56px;right:56px;top:70px;height:84px;display:flex;align-items:center;justify-content:space-between}
.who{display:flex;align-items:center;gap:16px}
.face{width:76px;height:76px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 3px #e8c25a,0 0 0 7px rgba(232,194,90,.18),0 8px 22px rgba(0,0,0,.5)}
.who b{display:block;font:800 30px/1 var(--f-b)}
.who small{display:block;margin-top:6px;font:700 21px/1 var(--f-b);color:var(--muted);letter-spacing:.04em}
.live{display:inline-flex;align-items:center;gap:12px;height:54px;padding:0 24px 0 20px;border-radius:999px;background:var(--lime);color:#14110b;font:800 22px/1 var(--f-b);letter-spacing:.14em;
 box-shadow:0 0 0 6px rgba(203,251,97,.12),0 10px 30px rgba(203,251,97,.18)}
.live i{width:13px;height:13px;border-radius:50%;background:#e0263f}

/* captions */
#cap{left:90px;right:90px;top:1450px;display:flex;justify-content:center}
#capbox{max-width:900px;padding:16px 28px;border-radius:24px;background:rgba(11,9,18,.66);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.08);
 font:800 50px/1.28 var(--f-b);text-align:center;color:#fff}
#capbox span{display:inline-block;margin:0 .13em;transition:none}
#capbox span.on{color:var(--lime)}
#capbox span.done{color:#fff}
#capbox span.todo{color:rgba(255,255,255,.55)}

/* hook */
.hk{font:400 156px/.95 var(--f-d);text-transform:uppercase;letter-spacing:.005em}
#h1{top:330px;color:#fff;text-shadow:0 8px 50px rgba(155,124,255,.35)}
#h2{top:490px}
.goldtxt{background:var(--goldg);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 6px 30px rgba(232,194,90,.35))}
#hbar{left:190px;top:700px;width:700px;height:518px}
#hbar svg,#gbar svg{width:100%;height:100%;overflow:visible}
#hsub{top:1270px;font:700 50px/1.2 var(--f-b);color:var(--body)}

/* intro */
#pc{left:170px;top:270px;width:740px;height:740px;border-radius:66px;padding:14px;background:linear-gradient(135deg,#fae496 0%,#e8c25a 45%,#c48e2c 100%);
 box-shadow:0 0 0 2px rgba(255,241,191,.4),0 0 90px rgba(232,194,90,.40),0 30px 80px rgba(0,0,0,.55)}
#pc img{display:block;width:100%;height:100%;border-radius:54px;object-fit:cover}
#n1{top:1060px;font:400 132px/1 var(--f-d);letter-spacing:.02em}
#n2{top:1210px;font:800 50px/1 var(--f-b);color:var(--body);letter-spacing:.03em}

/* the simple picture */
.kick{display:flex;align-items:center;justify-content:center;gap:16px;font:800 30px/1 var(--f-b);letter-spacing:.24em;color:var(--lime)}
.kick img{width:52px;height:52px}
#k2{top:212px}
.node{left:100px;width:880px;height:132px;border-radius:28px;display:flex;align-items:center;gap:26px;padding:0 30px;
 background:linear-gradient(160deg,rgba(40,33,60,.95),rgba(20,17,30,.95));box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.10),0 18px 40px rgba(0,0,0,.35)}
.node .ti{flex:0 0 auto;display:grid;place-items:center;width:84px;height:84px;border-radius:22px;color:#fff;background:var(--grad);box-shadow:0 10px 26px rgba(155,124,255,.35)}
.node .ti svg{width:46px;height:46px}
.node b{display:block;font:800 44px/1.05 var(--f-b)}
.node em{display:block;margin-top:8px;font:700 30px/1 var(--f-b);font-style:normal;color:var(--muted)}
.node em.hl{color:var(--gold-hi)}
.node .no{margin-left:auto;font:400 64px/1 var(--f-d);color:rgba(255,255,255,.14)}
.node.foc{box-shadow:inset 0 0 0 2.5px rgba(203,251,97,.75),0 0 0 8px rgba(203,251,97,.10),0 18px 40px rgba(0,0,0,.35)}
.arr{left:510px;width:60px;height:44px;color:var(--lime);display:grid;place-items:center}
.arr svg{width:40px;height:40px}
#gz{left:60px;right:60px;top:1000px;height:400px}
#gbar{left:0;top:40px;width:470px;height:348px}
#tick{left:520px;top:70px;height:120px;padding:0 30px;border-radius:26px;display:flex;align-items:center;gap:10px;background:rgba(232,194,90,.12);
 box-shadow:inset 0 0 0 2px rgba(232,194,90,.6);font:400 92px/1 var(--f-d);color:var(--gold-hi);letter-spacing:.02em}
#tick .cur{display:inline-block;width:6px;height:80px;background:var(--gold-hi);margin-left:4px}
#gl{left:520px;top:220px;width:440px;font:800 40px/1.2 var(--f-b);color:#fff}
#gl small{display:block;margin-top:8px;font:700 30px/1.2 var(--f-b);color:var(--muted)}
#tag{left:372px;top:132px;width:100px;height:100px;border-radius:50%;display:grid;place-items:center;background:var(--lime);color:#14110b;font:800 56px/1 var(--f-b);
 box-shadow:0 10px 30px rgba(203,251,97,.35);transform-origin:50% -40px}

/* promo */
#k3{top:250px}
#gift{left:330px;top:330px;width:420px;height:420px}
.giftsvg{width:100%;height:100%;overflow:visible}
#amt{top:770px;font:400 250px/1 var(--f-d);color:var(--lime);text-shadow:0 10px 60px rgba(203,251,97,.35)}
#amtl{top:1030px;font:800 44px/1 var(--f-b);color:var(--gold-hi);letter-spacing:.04em}
#rules{left:80px;right:80px;top:830px;border-radius:32px;padding:30px 34px;background:linear-gradient(160deg,rgba(40,33,60,.96),rgba(20,17,30,.96));
 box-shadow:inset 0 0 0 2px rgba(232,194,90,.55),0 24px 60px rgba(0,0,0,.45)}
#rules h3{display:flex;align-items:center;gap:14px;font:400 60px/1 var(--f-d);letter-spacing:.03em;color:var(--gold-hi)}
#rules h3 svg{width:48px;height:48px}
.rr{display:flex;align-items:center;gap:22px;margin-top:26px;padding:22px 24px;border-radius:22px;background:rgba(255,255,255,.04);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.08)}
.rr svg{flex:0 0 auto;width:54px;height:54px;color:var(--gold-hi)}
.rr p{font:700 38px/1.2 var(--f-b);color:#fff}
.rr p b{color:var(--gold-hi)}
.rr.warn{box-shadow:inset 0 0 0 2.5px rgba(255,95,122,.85),0 0 0 8px rgba(255,95,122,.10)}
.rr.warn svg{color:var(--red)}

/* event */
#k4{top:250px}
#tn{top:330px;font:400 250px/.95 var(--f-d);letter-spacing:.01em}
#dt{top:600px;font:800 40px/1 var(--f-b);letter-spacing:.14em;color:#fff}
#tc{left:90px;right:90px;top:690px;border-radius:32px;padding:10px 34px;background:linear-gradient(160deg,rgba(36,30,54,.92),rgba(20,17,30,.92));box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.10),0 18px 40px rgba(0,0,0,.35)}
.tr{display:flex;align-items:center;gap:24px;height:150px}
.tr+.tr{border-top:1.5px solid rgba(255,255,255,.08)}
.flag{flex:0 0 auto;width:78px;height:78px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px rgba(255,255,255,.9),0 6px 16px rgba(0,0,0,.4)}
.flag svg{display:block;width:100%;height:100%}
.cn{flex:1;font:800 42px/1 var(--f-b);letter-spacing:.04em}
.cn i{display:block;margin-top:8px;font-style:normal;font:700 26px/1 var(--f-b);letter-spacing:.14em;color:var(--muted)}
.tm{font:400 92px/1 var(--f-d);color:var(--gold-hi);letter-spacing:.02em}
#early{left:150px;right:150px;top:1200px;height:92px;border-radius:26px;display:flex;align-items:center;justify-content:center;gap:16px;background:var(--lime);color:#14110b;font:800 40px/1 var(--f-b)}
#early svg{width:44px;height:44px}

/* call to action */
#c5a{top:300px;font:800 38px/1 var(--f-b);letter-spacing:.14em;color:var(--gold-hi)}
#c5b{top:400px;display:flex;align-items:center;justify-content:center;gap:18px;font:400 104px/1 var(--f-d);letter-spacing:.02em}
#c5b .zi{display:grid;place-items:center;width:100px;height:100px;border-radius:26px;background:#2d8cff;color:#fff;box-shadow:0 10px 30px rgba(45,140,255,.4)}
#c5b .zi svg{width:58px;height:58px}
.url{left:60px;right:60px;height:190px;border-radius:36px;display:flex;flex-direction:column;justify-content:center;align-items:center;
 background:linear-gradient(100deg,rgba(140,108,231,.42),rgba(181,108,246,.26) 50%,rgba(227,113,252,.32));box-shadow:inset 0 0 0 3px rgba(203,251,97,.85),0 0 0 10px rgba(203,251,97,.10),0 24px 60px rgba(0,0,0,.45)}
.url small{font:700 30px/1 var(--f-b);letter-spacing:.08em;color:var(--body)}
.url b{margin-top:14px;font:800 66px/1 var(--f-b);letter-spacing:-.015em;color:#fff;white-space:nowrap}
.url b i{font-style:normal;color:var(--lime)}
#u5{top:560px}
#rip{left:540px;top:655px;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;border:5px solid var(--lime)}
#hand{left:700px;top:700px;width:120px;height:120px;color:#fff;filter:drop-shadow(0 8px 16px rgba(0,0,0,.6))}
#hand svg{width:100%;height:100%;stroke-width:1.6}
#chips{left:60px;right:60px;top:820px;display:flex;justify-content:center;gap:18px}
.chip{display:flex;align-items:center;gap:14px;height:86px;padding:0 24px 0 14px;border-radius:999px;background:rgba(36,30,54,.92);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.12);font:400 50px/1 var(--f-d);color:var(--gold-hi)}
.chip .flag{width:58px;height:58px;box-shadow:0 0 0 2px rgba(255,255,255,.9)}
#early5{left:170px;right:170px;top:950px;height:80px;border-radius:24px;display:flex;align-items:center;justify-content:center;gap:14px;background:var(--lime);color:#14110b;font:800 36px/1 var(--f-b)}
#early5 svg{width:40px;height:40px}
#nfa{top:1110px;display:flex;justify-content:center}
#nfa span{display:inline-flex;align-items:center;gap:14px;padding:16px 26px;border-radius:999px;background:rgba(255,255,255,.06);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.12);font:700 32px/1 var(--f-b);color:var(--body)}
#nfa svg{width:40px;height:40px;color:var(--lime)}

/* end card */
#pc6{left:290px;top:220px;width:500px;height:500px;border-radius:44px;padding:10px;background:linear-gradient(135deg,#fae496 0%,#e8c25a 45%,#c48e2c 100%);
 box-shadow:0 0 0 2px rgba(255,241,191,.4),0 0 70px rgba(232,194,90,.40),0 24px 60px rgba(0,0,0,.55)}
#pc6 img{display:block;width:100%;height:100%;border-radius:36px;object-fit:cover}
#e1{top:770px;font:800 46px/1 var(--f-b)}
#e2{top:870px;font:400 88px/1 var(--f-d);letter-spacing:.01em;white-space:nowrap}
#e2 .em{font-size:76px;vertical-align:4px}
#u6{top:1030px;height:176px}
#u6 b{font-size:64px}
#disc{top:1250px;font:600 28px/1.3 var(--f-b);color:var(--muted)}
#fade{inset:0;background:#000}
"""

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>JetUP Zoom promo stage</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&display=block" rel="stylesheet">
<style>{CSS}</style></head><body><div id="v">
<div class="glow" id="g1"></div><div class="glow" id="g2"></div><div class="glow" id="g3"></div><div id="grid"></div>
<div class="ab" id="bgc">{bgchart}</div>

<!-- S0 hook -->
<div class="ab c hk" id="h1">Automated</div>
<div class="ab c hk" id="h2"><span class="goldtxt">Gold trading?</span></div>
<div class="ab" id="hbar">{uniq(gold_svg, 'A')}</div>
<div class="ab c" id="hsub">Here's the simple picture.</div>

<!-- S1 intro -->
<div class="ab" id="pc"><img src="mtg-photo.jpg" alt=""></div>
<div class="ab c" id="n1">MTG <span class="em" style="font-size:112px">👑</span></div>
<div class="ab c" id="n2">Your Digital Architect</div>

<!-- S2 the simple picture -->
<div class="ab c kick" id="k2"><img src="jetup-mark.png" alt="">THE SIMPLE PICTURE</div>
<div class="ab node" id="nd1" style="top:290px"><span class="ti">{ic('landmark')}</span><div><b>TAG Markets</b><em id="nd1s">The broker</em></div><span class="no">1</span></div>
<div class="ab arr" id="ar1" style="top:426px">{ic('down')}</div>
<div class="ab node" id="nd2" style="top:474px"><span class="ti">{ic('id')}</span><div><b>Your trading account</b><em id="nd2s">In your own name</em></div><span class="no">2</span></div>
<div class="ab arr" id="ar2" style="top:610px">{ic('down')}</div>
<div class="ab node" id="nd3" style="top:658px"><span class="ti">{ic('link')}</span><div><b>CopyX</b><em id="nd3s">Connects a strategy</em></div><span class="no">3</span></div>
<div class="ab arr" id="ar3" style="top:794px">{ic('down')}</div>
<div class="ab node" id="nd4" style="top:842px"><span class="ti">{ic('bot')}</span><div><b>Sonic AI</b><em id="nd4s">The main strategy: trades gold</em></div><span class="no">4</span></div>
<div class="ab" id="gz">
  <div class="ab" id="gbar">{uniq(gold_svg, 'B')}</div>
  <div class="ab" id="tick"><span id="tickt"></span><span class="cur" id="tcur"></span></div>
  <div class="ab" id="gl">Gold, priced in<br>US dollars<small>Shown as XAU/USD</small></div>
  <div class="ab" id="tag">$</div>
</div>

<!-- S3 promo -->
<div class="ab c kick" id="k3"><img src="jetup-mark.png" alt="">JETUP FAST START PROMO</div>
<div class="ab" id="gift">{GIFT}</div>
<div class="ab c" id="amt">+$<span id="amtn">100</span></div>
<div class="ab c" id="amtl">Added by the promo</div>
<div class="ab" id="rules"><h3>{ic('alert')}THE RULES</h3>
  <div class="rr" id="rr1">{ic('cal')}<p>The bonus is released after <b>12 months</b></p></div>
  <div class="rr" id="rr2">{ic('ban')}<p>Take your own money out before then, and <b>the promo ends</b></p></div>
</div>

<!-- S4 event -->
<div class="ab c kick" id="k4"><img src="jetup-mark.png" alt="">JETUP PRESENTATION</div>
<div class="ab c" id="tn"><span class="goldtxt">Tonight</span></div>
<div class="ab c" id="dt">SATURDAY 7 NOVEMBER 2026</div>
<div class="ab" id="tc">
  <div class="tr" id="tr1">{flag(f_za, 'a')}<span class="cn">SOUTH AFRICA<i>SAST</i></span><span class="tm">8:00 PM</span></div>
  <div class="tr" id="tr2">{flag(f_ng, 'a')}<span class="cn">NIGERIA<i>WAT</i></span><span class="tm">7:00 PM</span></div>
  <div class="tr" id="tr3">{flag(f_in, 'a')}<span class="cn">INDIA<i>IST</i></span><span class="tm">11:30 PM</span></div>
</div>
<div class="ab" id="early">{ic('clock')}Log in 10 minutes early</div>

<!-- S5 call to action -->
<div class="ab c" id="c5a">TONIGHT, LIVE ON ZOOM</div>
<div class="ab c" id="c5b"><span class="zi">{ic('video')}</span>JOIN THE CALL</div>
<div class="ab url" id="u5"><small>Tap or type</small><b>mtgtribe.com/<i>JetUpZoom</i></b></div>
<div class="ab" id="rip"></div>
<div class="ab" id="hand">{ic('tap')}</div>
<div class="ab" id="chips">
  <span class="chip" id="ch1">{flag(f_za, 'b')}8:00 PM</span><span class="chip" id="ch2">{flag(f_ng, 'b')}7:00 PM</span><span class="chip" id="ch3">{flag(f_in, 'b')}11:30 PM</span>
</div>
<div class="ab" id="early5">{ic('clock')}Log in 10 minutes early</div>
<div class="ab c" id="nfa"><span>{ic('shield')}Not financial advice</span></div>

<!-- S6 end card -->
<div class="ab" id="pc6"><img src="mtg-photo.jpg" alt=""></div>
<div class="ab c" id="e1">MTG <span class="em">👑</span><span class="sep">|</span>Your Digital Architect</div>
<div class="ab c" id="e2"><span class="goldtxt">Let's Get This Crypto!</span> <span class="em">💪</span></div>
<div class="ab url" id="u6"><small>Join tonight on Zoom</small><b>mtgtribe.com/<i>JetUpZoom</i></b></div>
<div class="ab c" id="disc">Education only, not financial advice. Trading carries risk.</div>

<!-- always on -->
<div class="ab" id="top"><div class="who"><img class="face" src="mtg-face.jpg" alt=""><div><b>MTG <span class="em">👑</span></b><small>Your Digital Architect</small></div></div>
  <span class="live"><i id="dot"></i>LIVE ON ZOOM</span></div>
<div class="ab" id="cap"><div id="capbox"></div></div>
<div class="ab" id="fade"></div>
</div>
<script src="timing.js"></script>
<script src="engine.js"></script>
</body></html>"""

open(os.path.join(HERE, 'stage', 'stage.html'), 'w').write(HTML)
print('stage.html', len(HTML))
