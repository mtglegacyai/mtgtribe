# JetUP Zoom invitation v4 (3D): writes stage4/index.html. Crisp text, captions and the top bar are HTML on top of the 3D canvas.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
bgchart, hero, f_za, f_ng, f_in = open(os.path.join(HERE, '..', 'parts.txt')).read().split('\n=====\n')
def uniq(svg, s):
    for i in set(re.findall(r'id="([^"]+)"', svg)): svg = svg.replace(f'id="{i}"', f'id="{i}{s}"').replace(f'url(#{i})', f'url(#{i}{s})')
    return svg
IC = {
    'video': '<path d="m16 13 5.2 3.5a.5.5 0 0 0 .8-.4V7.9a.5.5 0 0 0-.8-.4L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'help': '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
    'flame': '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    'check': '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    'chat': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M9 10h.01M12 10h.01M15 10h.01"/>',
    'send': '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    'cal': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
}
def ic(k): return f'<svg class="i" viewBox="0 0 24 24">{IC[k]}</svg>'

CSS = r"""
@font-face{font-family:'Anton';src:url(Anton-Regular.ttf) format('truetype');font-display:block}
:root{--bg:#0b0912;--body:#cfc8e6;--muted:#9c95b8;--lime:#cbfb61;--gold:#e8c25a;--gold-hi:#ffe08f;--red:#ff5f7a;
 --goldg:linear-gradient(180deg,#fff1bf 0%,#ffe08f 35%,#e8c25a 70%,#c99a3a 100%);--f-d:'Anton',Impact,sans-serif;--f-b:'Manrope',system-ui,sans-serif;--emoji:'Noto Color Emoji'}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--bg)}
body{font-family:var(--f-b);color:#f6f3ff;-webkit-font-smoothing:antialiased}
#v{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--bg)}
.glow{position:absolute;border-radius:50%;pointer-events:none}
#g1{left:-260px;top:120px;width:900px;height:700px;background:radial-gradient(closest-side,rgba(140,108,231,.36),transparent)}
#g2{right:-300px;top:900px;width:900px;height:800px;background:radial-gradient(closest-side,rgba(232,194,90,.18),transparent)}
#g3{left:90px;bottom:-320px;width:900px;height:600px;background:radial-gradient(closest-side,rgba(227,113,252,.22),transparent)}
#grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:60px 60px;
 -webkit-mask-image:radial-gradient(900px 1200px at 50% 45%,#000 30%,transparent 80%)}
#bgc .bgchart{position:absolute;left:-40px;width:1160px;top:1060px;height:520px;opacity:.06}
#wrap{position:absolute;inset:0;transform-origin:540px 800px}
#glwrap{position:absolute;inset:0}
#glwrap canvas{display:block;width:1080px;height:1920px}
.ab{position:absolute;will-change:transform,opacity}
.c{left:0;right:0;text-align:center}
svg.i{fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.em{font-family:var(--emoji);font-weight:400}
.goldtxt{background:var(--goldg);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 6px 30px rgba(232,194,90,.4))}
.sh{text-shadow:0 6px 30px rgba(0,0,0,.65)}
.kick{display:flex;align-items:center;justify-content:center;gap:16px;font:800 30px/1 var(--f-b);letter-spacing:.22em;color:var(--lime)}
#top{left:56px;right:56px;top:70px;height:84px;display:flex;align-items:center;justify-content:space-between}
.who b{display:block;font:800 30px/1 var(--f-b)}
.who small{display:block;margin-top:6px;font:700 21px/1 var(--f-b);color:var(--muted);letter-spacing:.04em}
.live{display:inline-flex;align-items:center;gap:12px;height:54px;padding:0 24px 0 20px;border-radius:999px;background:var(--lime);color:#14110b;font:800 22px/1 var(--f-b);letter-spacing:.14em;box-shadow:0 0 0 6px rgba(203,251,97,.12),0 10px 30px rgba(203,251,97,.18)}
.live i{width:13px;height:13px;border-radius:50%;background:#e0263f}
#cap{left:90px;right:90px;top:1450px;display:flex;justify-content:center}
#capbox{max-width:900px;padding:16px 28px;border-radius:24px;background:rgba(11,9,18,.7);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.08);font:800 50px/1.28 var(--f-b);text-align:center;color:#fff}
#capbox span{display:inline-block;margin:0 .13em}
#capbox span.on{color:var(--lime)}
#capbox span.todo{color:rgba(255,255,255,.55)}
/* S0 */
.hk{font:400 156px/.95 var(--f-d);text-transform:uppercase}
#h1{top:225px;color:#fff;text-shadow:0 8px 50px rgba(155,124,255,.45)}
#h2{top:378px}
#hsub{top:560px;font:800 52px/1.1 var(--f-b)}
#hpill{left:110px;right:110px;top:1330px;height:92px;border-radius:999px;display:flex;align-items:center;justify-content:center;background:rgba(11,9,18,.88);box-shadow:inset 0 0 0 3px var(--lime);font:800 36px/1 var(--f-b);letter-spacing:.06em;color:var(--lime)}
/* S1 */
#mono1{top:325px;font:400 130px/1 var(--f-d);letter-spacing:.02em}
#arch1{top:470px;font:800 34px/1 var(--f-b);letter-spacing:.16em;color:var(--body)}
/* S2 */
#k2{top:225px}
#dt2{top:290px;display:flex;align-items:center;justify-content:center;gap:16px;font:800 40px/1 var(--f-b);letter-spacing:.12em}
#dt2 svg{width:44px;height:44px;color:var(--gold-hi)}
.tr{left:430px;right:50px;height:190px;display:flex;flex-direction:column;justify-content:center;gap:12px}
.tr .cn{display:flex;align-items:center;gap:16px;font:800 40px/1 var(--f-b);letter-spacing:.04em}
.tr .cn i{font-style:normal;font:700 26px/1 var(--f-b);letter-spacing:.14em;color:var(--muted)}
.flag{flex:0 0 auto;display:inline-block;width:60px;height:60px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px rgba(255,255,255,.9)}
.flag svg{display:block;width:100%;height:100%}
.tr .tm{font:400 132px/1 var(--f-d);color:var(--gold-hi);letter-spacing:.02em;text-shadow:0 8px 40px rgba(232,194,90,.35)}
#tr1{top:445px}#tr2{top:785px}#tr3{top:1125px}
/* S3 */
.bub{left:70px;max-width:760px;display:flex;align-items:center;gap:18px;padding:24px 34px;border-radius:36px 36px 36px 10px;background:rgba(155,124,255,.22);box-shadow:inset 0 0 0 2px rgba(155,124,255,.65);font:800 48px/1.1 var(--f-b)}
.bub svg{width:54px;height:54px}
#b1{top:240px}#b2{top:390px}
.ans{right:70px;max-width:840px;display:flex;align-items:center;gap:20px;padding:24px 34px;border-radius:36px 36px 10px 36px;background:rgba(203,251,97,.14);box-shadow:inset 0 0 0 2.5px rgba(203,251,97,.85);font:800 50px/1.1 var(--f-b)}
.ans svg{width:58px;height:58px;color:var(--lime)}
#a1{top:1060px}#a2{top:1210px}
/* S4 */
#lh{top:215px;font:400 100px/1 var(--f-d);letter-spacing:.02em}
#lh b{color:var(--lime);font-weight:400}
#pc{left:60px;right:60px;top:330px;display:flex;justify-content:center;gap:14px}
.pc{display:flex;align-items:center;gap:10px;height:66px;padding:0 22px 0 10px;border-radius:999px;background:rgba(36,30,54,.9);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.12);font:800 28px/1 var(--f-b);color:var(--muted)}
.pc b{display:grid;place-items:center;width:46px;height:46px;border-radius:50%;background:rgba(255,255,255,.1);font:400 30px/1 var(--f-d);color:#fff}
.pc.on{color:#fff;box-shadow:inset 0 0 0 2.5px var(--lime)}.pc.on b{background:var(--lime);color:#14110b}
.pc.done{color:var(--body)}.pc.done b{background:rgba(203,251,97,.25);color:var(--lime)}
.lt{left:70px;right:70px;top:1080px;text-align:center;font:800 56px/1.15 var(--f-b)}
.lt small{display:block;margin-top:12px;font:700 36px/1.1 var(--f-b);color:var(--muted)}
.lt em{font-style:normal;color:var(--gold-hi)}
/* S5 */
.dl{left:420px;right:50px;height:160px;display:flex;align-items:center;font:800 58px/1.1 var(--f-b)}
#d1{top:400px}#d2{top:730px}#d3{top:1060px;color:var(--lime)}
/* S6 */
#j1{top:200px;display:flex;align-items:center;justify-content:center;gap:20px;font:400 116px/1 var(--f-d);letter-spacing:.02em}
#j1 .zi{display:grid;place-items:center;width:108px;height:108px;border-radius:30px;background:#2d8cff;color:#fff;box-shadow:0 10px 30px rgba(45,140,255,.4)}
#j1 .zi svg{width:62px;height:62px}
#early{left:170px;right:170px;top:1320px;height:88px;border-radius:26px;display:flex;align-items:center;justify-content:center;gap:16px;background:var(--lime);color:#14110b;font:800 38px/1 var(--f-b)}
#early svg{width:44px;height:44px}
#share{left:560px;right:50px;top:560px;display:flex;flex-direction:column;align-items:flex-start;gap:26px;padding:34px;border-radius:36px;background:rgba(37,211,102,.14);box-shadow:inset 0 0 0 2.5px rgba(37,211,102,.75)}
#share .wa{display:grid;place-items:center;width:110px;height:110px;border-radius:50%;background:#25d366;color:#fff}
#share .wa svg{width:60px;height:60px}
#share p{font:800 50px/1.15 var(--f-b)}
/* S7 */
#chips{left:50px;right:50px;top:690px;display:flex;justify-content:center;gap:18px}
.chip{display:flex;align-items:center;gap:14px;height:92px;padding:0 24px 0 14px;border-radius:999px;background:rgba(36,30,54,.92);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.12);font:400 54px/1 var(--f-d);color:var(--gold-hi)}
.chip .flag{width:62px;height:62px}
.url{left:50px;right:50px;height:180px;border-radius:38px;display:flex;flex-direction:column;justify-content:center;align-items:center;
 background:linear-gradient(100deg,rgba(140,108,231,.5),rgba(181,108,246,.3) 50%,rgba(227,113,252,.38));box-shadow:inset 0 0 0 3px rgba(203,251,97,.85),0 0 0 10px rgba(203,251,97,.10),0 24px 60px rgba(0,0,0,.45)}
.url small{font:700 30px/1 var(--f-b);letter-spacing:.08em;color:var(--body)}
.url b{margin-top:14px;font:800 66px/1 var(--f-b);letter-spacing:-.015em;color:#fff;white-space:nowrap}
.url b i{font-style:normal;color:var(--lime)}
#u7{top:810px}
#e2{top:1030px;font:800 38px/1 var(--f-b);color:var(--body);letter-spacing:.1em}
#e2 .sep{font-family:Inter,sans-serif;font-weight:300;color:var(--gold);margin:0 10px}
#e3{top:1100px;font:400 92px/1 var(--f-d);letter-spacing:.01em;white-space:nowrap}
#e3 .em{font-size:78px;vertical-align:4px}
#disc{top:1240px;font:600 28px/1.3 var(--f-b);color:var(--muted)}
#flash{inset:0;background:#fff}
#fade{inset:0;background:#000}
"""

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>JetUP Zoom invitation 3D stage</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&display=block" rel="stylesheet">
<script type="importmap">{{"imports":{{"three":"../node_modules/three/build/three.module.js","three/addons/":"../node_modules/three/examples/jsm/"}}}}</script>
<style>{CSS}</style></head><body><div id="v">
<div class="glow" id="g1"></div><div class="glow" id="g2"></div><div class="glow" id="g3"></div><div id="grid"></div>
<div class="ab" id="bgc" style="inset:0">{bgchart}</div>
<div id="wrap">
<div id="glwrap"></div>

<div class="ab c hk" id="h1">Automated</div>
<div class="ab c hk" id="h2"><span class="goldtxt">Gold trading</span></div>
<div class="ab c sh" id="hsub">See how it really works</div>
<div class="ab" id="hpill">BEFORE YOU PUT IN A SINGLE CENT</div>

<div class="ab c" id="mono1"><span class="goldtxt">MTG</span></div>
<div class="ab c" id="arch1">YOUR DIGITAL ARCHITECT</div>

<div class="ab c kick" id="k2">TONIGHT, LIVE ON ZOOM</div>
<div class="ab c" id="dt2">{ic('cal')}SATURDAY 7 NOVEMBER 2026</div>
<div class="ab tr" id="tr1"><span class="cn"><span class="flag">{uniq(f_za, 'a')}</span>SOUTH AFRICA<i>SAST</i></span><span class="tm">8:00 PM</span></div>
<div class="ab tr" id="tr2"><span class="cn"><span class="flag">{uniq(f_ng, 'a')}</span>NIGERIA<i>WAT</i></span><span class="tm">7:00 PM</span></div>
<div class="ab tr" id="tr3"><span class="cn"><span class="flag">{uniq(f_in, 'a')}</span>INDIA<i>IST</i></span><span class="tm">11:30 PM</span></div>

<div class="ab bub" id="b1">{ic('help')}Curious about JetUP?</div>
<div class="ab bub" id="b2">{ic('flame')}Burned before?</div>
<div class="ab ans" id="a1">{ic('check')}See the facts</div>
<div class="ab ans" id="a2">{ic('chat')}Ask your questions live</div>

<div class="ab c" id="lh"><b>3</b> THINGS YOU'LL LEARN</div>
<div class="ab" id="pc"><span class="pc" id="pc1"><b>1</b>How it works</span><span class="pc" id="pc2"><b>2</b>$100 bonus</span><span class="pc" id="pc3"><b>3</b>Get started</span></div>
<div class="ab lt" id="lt1">What JetUP is, and how the <em>automated gold trading</em> works</div>
<div class="ab lt" id="lt2">The <em>$100 Fast Start bonus</em>, and its rules</div>
<div class="ab lt" id="lt3">How to <em>get started</em>, step by step<small>If it's right for you</small></div>

<div class="ab dl" id="d1">Trading carries risk</div>
<div class="ab dl" id="d2">Learn first</div>
<div class="ab dl" id="d3">Then decide for yourself</div>

<div class="ab c" id="j1"><span class="zi">{ic('video')}</span>JOIN THE CALL</div>
<div class="ab" id="early">{ic('clock')}Log in 10 minutes early</div>
<div class="ab" id="share"><span class="wa">{ic('send')}</span><p>Send this to someone who should be there</p></div>

<div class="ab" id="chips"><span class="chip" id="ch1"><span class="flag">{uniq(f_za, 'b')}</span>8:00 PM</span><span class="chip" id="ch2"><span class="flag">{uniq(f_ng, 'b')}</span>7:00 PM</span><span class="chip" id="ch3"><span class="flag">{uniq(f_in, 'b')}</span>11:30 PM</span></div>
<div class="ab url" id="u7"><small>Join tonight on Zoom</small><b>mtgtribe.com/<i>JetUpZoom</i></b></div>
<div class="ab c" id="e2">MTG <span class="em">👑</span><span class="sep">|</span>YOUR DIGITAL ARCHITECT</div>
<div class="ab c" id="e3"><span class="goldtxt">Let's Get This Crypto!</span> <span class="em">💪</span></div>
<div class="ab c" id="disc">Education only, not financial advice. Trading carries risk.</div>
</div>

<div class="ab" id="top"><div class="who"><b>MTG <span class="em">👑</span></b><small>Your Digital Architect</small></div><span class="live"><i id="dot"></i>LIVE ON ZOOM</span></div>
<div class="ab" id="cap"><div id="capbox"></div></div>
<div class="ab" id="flash"></div>
<div class="ab" id="fade"></div>
</div>
<script src="timing.js"></script>
<script src="dom.js"></script>
<script type="module" src="app3d.js"></script>
</body></html>"""
open(os.path.join(HERE, 'stage4', 'index.html'), 'w').write(HTML)
print('index.html', len(HTML))
