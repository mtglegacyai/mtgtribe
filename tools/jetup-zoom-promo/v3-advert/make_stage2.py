# JetUP Zoom INVITATION promo v2 (9:16, 1080x1920): writes stage/stage.html. No photo of MTG (his request), his voice only.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, '..', 'parts.txt')
bgchart, hero, f_za, f_ng, f_in = open(P).read().split('\n=====\n')
gold_svg = re.search(r'<svg viewBox="0 0 338 250">.*?</svg>', hero, re.S).group(0)


def uniq(svg, sfx):
    for i in set(re.findall(r'id="([^"]+)"', svg)):
        svg = svg.replace(f'id="{i}"', f'id="{i}{sfx}"').replace(f'url(#{i})', f'url(#{i}{sfx})')
    return svg


IC = {
    'video': '<path d="m16 13 5.2 3.5a.5.5 0 0 0 .8-.4V7.9a.5.5 0 0 0-.8-.4L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'tap': '<path d="M22 14a8 8 0 0 1-8 8"/><path d="M18 11v-1a2 2 0 0 0-2-2a2 2 0 0 0-2 2"/><path d="M14 10V9a2 2 0 0 0-2-2a2 2 0 0 0-2 2v1"/><path d="M10 9.5V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v10"/><path d="M18 11a2 2 0 1 1 4 0v3a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>',
    'help': '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
    'flame': '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    'check': '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    'chat': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M9 10h.01M12 10h.01M15 10h.01"/>',
    'gold': '<path d="M2.5 20h19l-3.2-6.5H5.7z"/><path d="M6.8 13.5 9 8.5h6l2.2 5"/><path d="M9.5 17h5"/>',
    'gift': '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C10 3 12 8 12 8s2-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    'steps': '<path d="M3 20h5v-5h5v-5h5V5h3"/>',
    'alert': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    'book': '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="M8 7h6"/>',
    'down': '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
    'send': '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    'cal': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
}
def ic(k, cls='i'): return f'<svg class="{cls}" viewBox="0 0 24 24">{IC[k]}</svg>'
def flag(f, s): return uniq(f, s)

CSS = r"""
:root{--bg:#0b0912;--text:#f6f3ff;--body:#cfc8e6;--muted:#9c95b8;--vio:#9b7cff;--pink:#e371fc;--lime:#cbfb61;--gold:#e8c25a;--gold-hi:#ffe08f;--red:#ff5f7a;
 --grad:linear-gradient(100deg,#8c6ce7 0%,#b56cf6 45%,#e371fc 100%);--goldg:linear-gradient(180deg,#fff1bf 0%,#ffe08f 35%,#e8c25a 70%,#c99a3a 100%);
 --f-d:'Anton',Impact,sans-serif;--f-b:'Manrope',system-ui,sans-serif;--emoji:'Noto Color Emoji'}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--bg)}
body{font-family:var(--f-b);color:var(--text);-webkit-font-smoothing:antialiased}
#v{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--bg)}
.glow{position:absolute;border-radius:50%;pointer-events:none}
#g1{left:-260px;top:120px;width:900px;height:700px;background:radial-gradient(closest-side,rgba(140,108,231,.34),transparent)}
#g2{right:-300px;top:900px;width:900px;height:800px;background:radial-gradient(closest-side,rgba(232,194,90,.18),transparent)}
#g3{left:90px;bottom:-320px;width:900px;height:600px;background:radial-gradient(closest-side,rgba(227,113,252,.20),transparent)}
#grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:60px 60px;
 -webkit-mask-image:radial-gradient(900px 1200px at 50% 45%,#000 30%,transparent 80%)}
#bgc .bgchart{position:absolute;left:-40px;width:1160px;top:1060px;height:520px;opacity:.07}
.ab{position:absolute;will-change:transform,opacity}
.c{left:0;right:0;text-align:center}
svg.i{fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.em{font-family:var(--emoji);font-weight:400}
.goldtxt{background:var(--goldg);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 6px 30px rgba(232,194,90,.35))}
.card{border-radius:32px;background:linear-gradient(160deg,rgba(40,33,60,.95),rgba(20,17,30,.95));box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.10),0 18px 40px rgba(0,0,0,.38)}
.kick{display:flex;align-items:center;justify-content:center;gap:16px;font:800 30px/1 var(--f-b);letter-spacing:.22em;color:var(--lime)}
.kick img{width:50px;height:50px}

/* top bar */
#top{left:56px;right:56px;top:70px;height:84px;display:flex;align-items:center;justify-content:space-between}
.who b{display:block;font:800 30px/1 var(--f-b)}
.who small{display:block;margin-top:6px;font:700 21px/1 var(--f-b);color:var(--muted);letter-spacing:.04em}
.live{display:inline-flex;align-items:center;gap:12px;height:54px;padding:0 24px 0 20px;border-radius:999px;background:var(--lime);color:#14110b;font:800 22px/1 var(--f-b);letter-spacing:.14em;
 box-shadow:0 0 0 6px rgba(203,251,97,.12),0 10px 30px rgba(203,251,97,.18)}
.live i{width:13px;height:13px;border-radius:50%;background:#e0263f}

/* captions */
#cap{left:90px;right:90px;top:1450px;display:flex;justify-content:center}
#capbox{max-width:900px;padding:16px 28px;border-radius:24px;background:rgba(11,9,18,.66);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.08);font:800 50px/1.28 var(--f-b);text-align:center;color:#fff}
#capbox span{display:inline-block;margin:0 .13em}
#capbox span.on{color:var(--lime)}
#capbox span.todo{color:rgba(255,255,255,.55)}

/* S0 hook */
.hk{font:400 160px/.95 var(--f-d);text-transform:uppercase}
#h1{top:300px;color:#fff;text-shadow:0 8px 50px rgba(155,124,255,.35)}
#h2{top:458px}
#hbar{left:230px;top:660px;width:620px;height:459px}
#hbar svg{width:100%;height:100%;overflow:visible}
#hsub{top:1140px;font:800 54px/1.1 var(--f-b);color:#fff}
#hpill{left:110px;right:110px;top:1250px;height:96px;border-radius:999px;display:flex;align-items:center;justify-content:center;gap:16px;
 background:rgba(203,251,97,.10);box-shadow:inset 0 0 0 3px var(--lime);font:800 36px/1 var(--f-b);letter-spacing:.06em;color:var(--lime)}

/* S1 invitation */
#crown1{top:215px;font-size:96px;line-height:1}
#mono1{top:320px;font:400 150px/1 var(--f-d);letter-spacing:.02em}
#arch1{top:480px;font:800 34px/1 var(--f-b);letter-spacing:.16em;color:var(--body)}
#tk{left:80px;right:80px;top:570px;height:720px;border-radius:44px;padding:4px;background:linear-gradient(135deg,#fae496,#e8c25a 45%,#c48e2c);
 box-shadow:0 0 90px rgba(232,194,90,.30),0 30px 80px rgba(0,0,0,.55)}
#tki{position:relative;width:100%;height:100%;border-radius:40px;background:radial-gradient(500px 300px at 50% 0%,rgba(155,124,255,.30),transparent 70%),linear-gradient(170deg,#1d1730,#120f1d);overflow:hidden}
#tki:before,#tki:after{content:"";position:absolute;top:404px;width:64px;height:64px;border-radius:50%;background:var(--bg);box-shadow:inset 0 0 0 4px #d9ad48}
#tki:before{left:-36px}#tki:after{right:-36px}
#tk1{top:70px;font:400 120px/1 var(--f-d);letter-spacing:.02em}
#tk2{top:226px;display:flex;align-items:center;justify-content:center;gap:16px;font:800 46px/1 var(--f-b)}
#tk2 img{width:58px;height:58px}
#tk3{left:0;right:0;top:310px;display:flex;justify-content:center}
#tk3 span{display:inline-flex;align-items:center;gap:14px;height:72px;padding:0 28px 0 16px;border-radius:999px;background:rgba(45,140,255,.16);box-shadow:inset 0 0 0 2px rgba(45,140,255,.7);font:800 34px/1 var(--f-b);letter-spacing:.12em}
#tk3 .zi{display:grid;place-items:center;width:50px;height:50px;border-radius:14px;background:#2d8cff;color:#fff}
#tk3 .zi svg{width:30px;height:30px}
#tkd{left:60px;right:60px;top:436px;border-top:4px dashed rgba(232,194,90,.45)}
#tk4{top:490px;font:400 150px/1 var(--f-d);color:var(--lime);letter-spacing:.03em;text-shadow:0 0 40px rgba(203,251,97,.35)}
#tk4 b{display:inline-block;padding:6px 34px;border:6px solid var(--lime);border-radius:26px;font-weight:400}

/* S2 times */
#k2{top:240px}
#dt2{top:310px;display:flex;align-items:center;justify-content:center;gap:16px;font:800 40px/1 var(--f-b);letter-spacing:.12em}
#dt2 svg{width:44px;height:44px;color:var(--gold-hi)}
#tc{left:80px;right:80px;top:410px;padding:14px 36px}
.tr{display:flex;align-items:center;gap:26px;height:190px;border-radius:26px;padding:0 10px;transition:none}
.tr+.tr{border-top:1.5px solid rgba(255,255,255,.08)}
.tr.on{background:rgba(203,251,97,.07);box-shadow:inset 0 0 0 2.5px rgba(203,251,97,.75)}
.flag{flex:0 0 auto;width:96px;height:96px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px rgba(255,255,255,.9),0 6px 16px rgba(0,0,0,.4)}
.flag svg{display:block;width:100%;height:100%}
.cn{flex:1;font:800 40px/1 var(--f-b);letter-spacing:.03em;white-space:nowrap}
.cn i{display:block;margin-top:10px;font-style:normal;font:700 28px/1 var(--f-b);letter-spacing:.14em;color:var(--muted)}
.tm{font:400 112px/1 var(--f-d);color:var(--gold-hi);letter-spacing:.02em}

/* S3 why */
.bub{left:80px;max-width:760px;display:flex;align-items:center;gap:20px;padding:30px 38px;border-radius:40px 40px 40px 10px;
 background:linear-gradient(160deg,rgba(155,124,255,.30),rgba(155,124,255,.14));box-shadow:inset 0 0 0 2px rgba(155,124,255,.55);font:800 52px/1.1 var(--f-b)}
.bub svg{flex:0 0 auto;width:60px;height:60px;color:#fff}
#b1{top:280px}#b2{top:470px}
.ans{right:80px;max-width:820px;display:flex;align-items:center;gap:22px;padding:30px 38px;border-radius:40px 40px 10px 40px;
 background:linear-gradient(160deg,rgba(203,251,97,.20),rgba(203,251,97,.08));box-shadow:inset 0 0 0 2.5px rgba(203,251,97,.8);font:800 52px/1.1 var(--f-b)}
.ans svg{flex:0 0 auto;width:62px;height:62px;color:var(--lime)}
#a1{top:760px}#a2{top:950px}
#why{top:670px;font:800 34px/1 var(--f-b);letter-spacing:.2em;color:var(--gold-hi)}

/* S4 three things */
#lh{top:230px;font:400 104px/1 var(--f-d);letter-spacing:.02em}
#lh b{color:var(--lime);font-weight:400}
.lc{left:70px;right:70px;height:236px;display:flex;align-items:center;gap:30px;padding:0 36px}
.lc .n{flex:0 0 auto;font:400 150px/1 var(--f-d);color:var(--lime);width:90px;text-align:center}
.lc .ti{flex:0 0 auto;display:grid;place-items:center;width:100px;height:100px;border-radius:26px;color:#14110b;background:var(--goldg)}
.lc .ti svg{width:58px;height:58px}
.lc p{font:800 44px/1.18 var(--f-b)}
.lc p small{display:block;margin-top:8px;font:700 32px/1.1 var(--f-b);color:var(--muted)}
.lc.foc{box-shadow:inset 0 0 0 3px rgba(203,251,97,.85),0 0 0 10px rgba(203,251,97,.10),0 18px 40px rgba(0,0,0,.38)}
#l1{top:400px}#l2{top:666px}#l3{top:932px}

/* S5 decide */
.dc{left:110px;right:110px;height:170px;display:flex;align-items:center;gap:28px;padding:0 40px;font:800 50px/1.1 var(--f-b)}
.dc svg{flex:0 0 auto;width:76px;height:76px}
#d1{top:360px}#d1 svg{color:var(--red)}
#d2{top:640px}#d2 svg{color:var(--gold-hi)}
#d3{top:920px}#d3 svg{color:var(--lime)}
#d3{box-shadow:inset 0 0 0 3px rgba(203,251,97,.85),0 0 0 10px rgba(203,251,97,.10),0 18px 40px rgba(0,0,0,.38)}
.dar{left:510px;width:60px;height:100px;color:var(--lime);display:grid;place-items:center}
.dar svg{width:50px;height:50px}
#da1{top:540px}#da2{top:820px}

/* S6 join + share */
#j1{top:250px;display:flex;align-items:center;justify-content:center;gap:20px;font:400 120px/1 var(--f-d);letter-spacing:.02em}
#j1 .zi{display:grid;place-items:center;width:112px;height:112px;border-radius:30px;background:#2d8cff;color:#fff;box-shadow:0 10px 30px rgba(45,140,255,.4)}
#j1 .zi svg{width:66px;height:66px}
.url{left:50px;right:50px;height:200px;border-radius:38px;display:flex;flex-direction:column;justify-content:center;align-items:center;
 background:linear-gradient(100deg,rgba(140,108,231,.42),rgba(181,108,246,.26) 50%,rgba(227,113,252,.32));box-shadow:inset 0 0 0 3px rgba(203,251,97,.85),0 0 0 10px rgba(203,251,97,.10),0 24px 60px rgba(0,0,0,.45)}
.url small{font:700 30px/1 var(--f-b);letter-spacing:.08em;color:var(--body)}
.url b{margin-top:14px;font:800 68px/1 var(--f-b);letter-spacing:-.015em;color:#fff;white-space:nowrap}
.url b i{font-style:normal;color:var(--lime)}
#u6{top:420px}
#ucur{display:inline-block;width:6px;height:62px;margin-left:4px;vertical-align:-6px;background:var(--lime)}
#rip{left:560px;top:540px;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;border:5px solid var(--lime)}
#hand{left:700px;top:580px;width:130px;height:130px;color:#fff;filter:drop-shadow(0 8px 16px rgba(0,0,0,.6))}
#hand svg{width:100%;height:100%;stroke-width:1.6}
#early{left:170px;right:170px;top:680px;height:92px;border-radius:26px;display:flex;align-items:center;justify-content:center;gap:16px;background:var(--lime);color:#14110b;font:800 40px/1 var(--f-b)}
#early svg{width:46px;height:46px}
#share{left:80px;right:80px;top:880px;height:250px;display:flex;align-items:center;gap:30px;padding:0 40px;border-radius:36px;
 background:linear-gradient(160deg,rgba(37,211,102,.20),rgba(37,211,102,.06));box-shadow:inset 0 0 0 2.5px rgba(37,211,102,.75)}
#share .wa{flex:0 0 auto;position:relative;display:grid;place-items:center;width:130px;height:130px;border-radius:50%;background:#25d366;color:#fff;box-shadow:0 10px 30px rgba(37,211,102,.35)}
#share .wa svg{width:70px;height:70px}
#share p{font:800 46px/1.15 var(--f-b)}
#plane{left:150px;top:970px;width:70px;height:70px;color:#fff}
#plane svg{width:100%;height:100%}

/* S7 end card */
#e1{top:250px;font:400 150px/.95 var(--f-d);letter-spacing:.02em}
#chips{left:50px;right:50px;top:570px;display:flex;justify-content:center;gap:18px}
.chip{display:flex;align-items:center;gap:14px;height:92px;padding:0 24px 0 14px;border-radius:999px;background:rgba(36,30,54,.92);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.12);font:400 54px/1 var(--f-d);color:var(--gold-hi)}
.chip .flag{width:62px;height:62px;box-shadow:0 0 0 2px rgba(255,255,255,.9)}
#u7{top:710px;height:184px}
#u7 b{font-size:64px}
#e2{top:950px;font:800 40px/1 var(--f-b);color:var(--body);letter-spacing:.1em}
#e2 .sep{font-family:Inter,sans-serif;font-weight:300;color:var(--gold);margin:0 10px}
#e3{top:1030px;font:400 90px/1 var(--f-d);letter-spacing:.01em;white-space:nowrap}
#e3 .em{font-size:76px;vertical-align:4px}
#disc{top:1170px;font:600 28px/1.3 var(--f-b);color:var(--muted)}
#fade{inset:0;background:#000}
"""

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>JetUP Zoom invitation stage</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&display=block" rel="stylesheet">
<style>{CSS}</style></head><body><div id="v">
<div class="glow" id="g1"></div><div class="glow" id="g2"></div><div class="glow" id="g3"></div><div id="grid"></div>
<div class="ab" id="bgc" style="inset:0">{bgchart}</div>
<div class="ab" id="sc" style="inset:0;transform-origin:540px 760px">

<!-- S0 hook -->
<div class="ab c hk" id="h1">Automated</div>
<div class="ab c hk" id="h2"><span class="goldtxt">Gold trading</span></div>
<div class="ab" id="hbar">{uniq(gold_svg, 'A')}</div>
<div class="ab c" id="hsub">See how it really works</div>
<div class="ab" id="hpill">BEFORE YOU PUT IN A SINGLE CENT</div>

<!-- S1 invitation -->
<div class="ab c em" id="crown1">👑</div>
<div class="ab c" id="mono1"><span class="goldtxt">MTG</span></div>
<div class="ab c" id="arch1">YOUR DIGITAL ARCHITECT</div>
<div class="ab" id="tk"><div id="tki">
  <div class="ab c" id="tk1"><span class="goldtxt">YOU'RE INVITED</span></div>
  <div class="ab c" id="tk2"><img src="jetup-mark.png" alt="">Live JetUP presentation</div>
  <div class="ab" id="tk3"><span><i class="zi">{ic('video')}</i>ON ZOOM</span></div>
  <div class="ab" id="tkd"></div>
  <div class="ab c" id="tk4"><b>TONIGHT</b></div>
</div></div>

<!-- S2 times -->
<div class="ab c kick" id="k2">TONIGHT, LIVE ON ZOOM</div>
<div class="ab c" id="dt2">{ic('cal')}SATURDAY 7 NOVEMBER 2026</div>
<div class="ab card" id="tc">
  <div class="tr" id="tr1">{flag(f_za, 'a')}<span class="cn">SOUTH AFRICA<i>SAST</i></span><span class="tm">8:00 PM</span></div>
  <div class="tr" id="tr2">{flag(f_ng, 'a')}<span class="cn">NIGERIA<i>WAT</i></span><span class="tm">7:00 PM</span></div>
  <div class="tr" id="tr3">{flag(f_in, 'a')}<span class="cn">INDIA<i>IST</i></span><span class="tm">11:30 PM</span></div>
</div>

<!-- S3 why come -->
<div class="ab bub" id="b1">{ic('help')}Curious about JetUP?</div>
<div class="ab bub" id="b2">{ic('flame')}Burned before?</div>
<div class="ab c" id="why">THEN COME AND</div>
<div class="ab ans" id="a1">{ic('check')}See the facts</div>
<div class="ab ans" id="a2">{ic('chat')}Ask your questions live</div>

<!-- S4 three things you'll learn -->
<div class="ab c" id="lh"><b>3</b> THINGS YOU'LL LEARN</div>
<div class="ab card lc" id="l1"><span class="n">1</span><span class="ti">{ic('gold')}</span><p>What JetUP is, and how the automated gold trading works</p></div>
<div class="ab card lc" id="l2"><span class="n">2</span><span class="ti">{ic('gift')}</span><p>The $100 Fast Start bonus, and its rules</p></div>
<div class="ab card lc" id="l3"><span class="n">3</span><span class="ti">{ic('steps')}</span><p>How to get started, step by step<small>If it's right for you</small></p></div>

<!-- S5 learn first, then decide -->
<div class="ab card dc" id="d1">{ic('alert')}Trading carries risk</div>
<div class="ab dar" id="da1">{ic('down')}</div>
<div class="ab card dc" id="d2">{ic('book')}Learn first</div>
<div class="ab dar" id="da2">{ic('down')}</div>
<div class="ab card dc" id="d3">{ic('check')}Then decide for yourself</div>

<!-- S6 join + share -->
<div class="ab c" id="j1"><span class="zi">{ic('video')}</span>JOIN THE CALL</div>
<div class="ab url" id="u6"><small>Tap or type</small><b><span id="ut"></span><span id="ucur"></span></b></div>
<div class="ab" id="rip"></div>
<div class="ab" id="hand">{ic('tap')}</div>
<div class="ab" id="early">{ic('clock')}Log in 10 minutes early</div>
<div class="ab" id="share"><span class="wa">{ic('send')}</span><p>Send this to someone who should be there</p></div>
<div class="ab" id="plane">{ic('send')}</div>

<!-- S7 end card -->
<div class="ab c" id="e1">SEE YOU<br><span class="goldtxt">TONIGHT</span></div>
<div class="ab" id="chips">
  <span class="chip" id="ch1">{flag(f_za, 'b')}8:00 PM</span><span class="chip" id="ch2">{flag(f_ng, 'b')}7:00 PM</span><span class="chip" id="ch3">{flag(f_in, 'b')}11:30 PM</span>
</div>
<div class="ab url" id="u7"><small>Join tonight on Zoom</small><b>mtgtribe.com/<i>JetUpZoom</i></b></div>
<div class="ab c" id="e2">MTG <span class="em">👑</span><span class="sep">|</span>YOUR DIGITAL ARCHITECT</div>
<div class="ab c" id="e3"><span class="goldtxt">Let's Get This Crypto!</span> <span class="em">💪</span></div>
<div class="ab c" id="disc">Education only, not financial advice. Trading carries risk.</div>

</div>
<div class="ab" id="flash" style="inset:0;background:#fff"></div>
<!-- always on -->
<div class="ab" id="top"><div class="who"><b>MTG <span class="em">👑</span></b><small>Your Digital Architect</small></div><span class="live"><i id="dot"></i>LIVE ON ZOOM</span></div>
<div class="ab" id="cap"><div id="capbox"></div></div>
<div class="ab" id="fade"></div>
</div>
<script src="timing.js"></script>
<script src="engine.js"></script>
</body></html>"""
open(os.path.join(HERE, 'stage', 'stage.html'), 'w').write(HTML)
print('stage.html', len(HTML))
