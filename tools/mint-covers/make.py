# Writes one HTML per cover; shoot.js renders them.
import os
D = os.path.dirname(os.path.abspath(__file__))
BASE = r"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&display=block" rel="stylesheet">
<style>
@font-face{font-family:'Anton';src:url(Anton-Regular.ttf)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(W)spx;height:%(H)spx;overflow:hidden}
body{position:relative;font-family:Manrope,sans-serif;color:#fff;background:
 radial-gradient(%(gw)spx %(gh)spx at %(gx)s %(gy)s,rgba(64,228,168,.38),transparent 68%%),
 radial-gradient(600px 480px at 50%% 50%%,rgba(255,214,107,.14),transparent 70%%),
 radial-gradient(700px 520px at 4%% 0%%,rgba(255,206,96,.14),transparent 70%%),
 radial-gradient(900px 700px at 0%% 100%%,rgba(20,120,110,.45),transparent 70%%),
 linear-gradient(160deg,#0f4441,#0a2e2c 55%%,#051a19)}
.floor{position:absolute;left:-20%%;right:-20%%;bottom:-6%%;height:46%%;transform:perspective(700px) rotateX(62deg);transform-origin:50%% 100%%;
 background:linear-gradient(rgba(64,228,168,.22) 2px,transparent 2px) 0 0/100%% 70px,linear-gradient(90deg,rgba(64,228,168,.22) 2px,transparent 2px) 0 0/90px 100%%;
 -webkit-mask-image:linear-gradient(to top,#000 10%%,transparent 85%%);mask-image:linear-gradient(to top,#000 10%%,transparent 85%%);opacity:.75}
.vig{position:absolute;inset:0;background:radial-gradient(closest-side at 50%% 50%%,transparent 62%%,rgba(0,0,0,.42))}
.p{position:absolute;border-radius:50%%;background:radial-gradient(circle at 35%% 30%%,#fff6cf,#f2c14e 45%%,#a8730f);box-shadow:0 0 24px rgba(255,200,80,.6)}
.p.m{background:radial-gradient(circle at 35%% 30%%,#eafff6,#40e4a8 55%%,#127a5a);box-shadow:0 0 24px rgba(64,228,168,.6)}
.p.b{filter:blur(4px);opacity:.6}
.pill{position:absolute;display:inline-flex;align-items:center;gap:.5em;height:2.25em;padding:0 1.05em;border-radius:999px;font-weight:800;letter-spacing:.13em;white-space:nowrap}
.pill.lime{background:#cbfb61;color:#0a2422;box-shadow:0 0 44px rgba(203,251,97,.45)}
.pill.red{background:#ff3b5c;color:#fff;box-shadow:0 0 50px rgba(255,59,92,.5),0 10px 30px rgba(0,0,0,.35)}
.pill.red i,.pill.lime i{width:.55em;height:.55em;border-radius:50%%;background:currentColor;display:inline-block}
.pill.glass{background:rgba(5,26,25,.72);color:#ffe08f;box-shadow:inset 0 0 0 2px rgba(255,224,143,.6)}
.h{position:absolute;font-family:Anton;line-height:.9;text-transform:uppercase;white-space:nowrap;filter:drop-shadow(0 10px 30px rgba(0,0,0,.7))}
.h .k{color:#cbfb61;filter:drop-shadow(0 0 30px rgba(203,251,97,.45))}
.h .g{background:linear-gradient(180deg,#fffbe6,#ffe08f 45%%,#e9ad2f);-webkit-background-clip:text;background-clip:text;color:transparent}
.chips{position:absolute;display:flex;gap:.6em}
.chip{display:flex;align-items:center;gap:.45em;height:2.3em;padding:0 .8em 0 .35em;border-radius:.6em;background:#fff;color:#0a2422;font-weight:800;letter-spacing:.03em;box-shadow:0 16px 40px rgba(0,0,0,.45)}
.chip .ic{width:1.7em;height:1.7em;border-radius:.45em;display:grid;place-items:center;background:radial-gradient(circle at 50%% 30%%,#1d5a55,#0b2b29 75%%)}
.chip .ic i{font-style:normal;font-family:'Noto Color Emoji';font-size:1.05em;line-height:1}
.brand{position:absolute;font-weight:800;letter-spacing:.06em;white-space:nowrap;text-shadow:0 3px 14px rgba(0,0,0,.7)}
.brand .g{color:#ffe08f}.brand .e{font-family:'Noto Color Emoji'}
.robot{position:absolute;filter:drop-shadow(0 30px 50px rgba(0,0,0,.55)) drop-shadow(0 0 60px rgba(80,240,180,.22))}
.coin{position:absolute;display:grid;place-items:center;border-radius:50%%;font-weight:800;letter-spacing:.02em;color:#3b2604;
 background:radial-gradient(circle at 34%% 28%%,#fff6cf,#f6cd5c 40%%,#c58a16 78%%,#8a5c0c);box-shadow:inset 0 0 0 .09em rgba(255,246,207,.7),inset 0 -.12em .2em rgba(0,0,0,.25),0 18px 36px rgba(0,0,0,.45),0 0 40px rgba(255,200,80,.35)}
.coin.s{color:#1d2b2a;background:radial-gradient(circle at 34%% 28%%,#ffffff,#dfeeea 40%%,#9fb8b2 78%%,#6f8a84)}
.coin.m{color:#05231b;background:radial-gradient(circle at 34%% 28%%,#eafff6,#7cf2c6 40%%,#29b884 78%%,#137255);box-shadow:inset 0 0 0 .09em rgba(234,255,246,.7),0 18px 36px rgba(0,0,0,.45),0 0 40px rgba(64,228,168,.45)}
.coin.c{color:#2a1205;background:radial-gradient(circle at 34%% 28%%,#ffe1c4,#e59a5e 40%%,#a85a26 78%%,#6e3712)}
.phone{position:absolute;border-radius:7%%/3.4%%;padding:1.1%%;background:linear-gradient(145deg,#f5e3b0 0%%,#b8954f 22%%,#6d5a35 48%%,#d9c08a 72%%,#8f7443 100%%);box-shadow:0 40px 90px rgba(0,0,0,.6),0 0 60px rgba(64,228,168,.25)}
.phone .in{width:100%%;height:100%%;border-radius:6.2%%/3%%;overflow:hidden;background:#000;padding:2.2%%}
.phone img{width:100%%;height:100%%;object-fit:cover;border-radius:5%%/2.4%%;display:block}
.disc{position:absolute;border-radius:50%%;padding:.5%%;background:conic-gradient(from 210deg,#fff1b8,#c99a2e,#f7dd8d,#9c6f1f,#fff1b8);box-shadow:0 0 50px rgba(232,194,90,.45),0 20px 50px rgba(0,0,0,.55)}
.disc img{width:100%%;height:100%%;border-radius:50%%;display:block}
.win{position:absolute;border-radius:30px;padding:16px;background:linear-gradient(160deg,rgba(14,52,49,.96),rgba(4,20,19,.97));box-shadow:inset 0 0 0 2px rgba(255,224,143,.55),0 50px 100px rgba(0,0,0,.6),0 0 80px rgba(64,228,168,.2)}
.win .top{display:flex;align-items:center;gap:10px;height:44px;padding:0 6px;font-weight:800;letter-spacing:.08em;color:#cfe9e2;font-size:22px}
.win .top b{width:14px;height:14px;border-radius:50%%;background:#ff5f57}.win .top b:nth-child(2){background:#febc2e}.win .top b:nth-child(3){background:#28c840}
.win .top .rec{margin-left:auto;display:flex;align-items:center;gap:8px;color:#ff6b84}.win .top .rec:before{content:"";width:12px;height:12px;border-radius:50%%;background:#ff3b5c;box-shadow:0 0 14px #ff3b5c}
.grid{display:grid;gap:12px}
.tile{position:relative;border-radius:18px;overflow:hidden;background:radial-gradient(circle at 50%% 30%%,#1f6159,#0a2422 75%%)}
.tile .nm{position:absolute;left:12px;bottom:12px;padding:6px 12px;border-radius:10px;background:rgba(0,0,0,.6);font-weight:800;font-size:20px;letter-spacing:.03em}
.tile.main{box-shadow:inset 0 0 0 4px #40e4a8}
.tile svg{position:absolute;left:50%%;bottom:-6%%;width:70%%;transform:translateX(-50%%)}
.tool{display:flex;justify-content:center;gap:16px;padding-top:12px}
.tool i{width:46px;height:46px;border-radius:50%%;background:rgba(255,255,255,.12);display:block}.tool i.r{background:#ff3b5c;width:80px;border-radius:23px}
.shot{position:absolute;border-radius:26px;padding:12px;background:linear-gradient(140deg,#7a531c,#f6d88c 22%%,#9a6a26 45%%,#f2c66d 70%%,#6b4615);box-shadow:0 50px 100px rgba(0,0,0,.6),0 0 70px rgba(255,190,60,.25)}
.shot img{display:block;width:100%%;height:100%%;object-fit:cover;border-radius:16px}
.dur{position:absolute;padding:.35em .7em;border-radius:.5em;background:rgba(0,0,0,.72);font-weight:800;letter-spacing:.04em;font-variant-numeric:tabular-nums}
.addr{position:absolute;display:inline-flex;align-items:center;height:2.1em;padding:0 1em;border-radius:999px;background:#cbfb61;color:#0a2422;font-weight:800;letter-spacing:.02em;box-shadow:0 0 40px rgba(203,251,97,.5),0 12px 28px rgba(0,0,0,.4)}
%(css)s
</style></head><body><div class="floor"></div><div class="vig"></div>%(body)s</body></html>"""
PERSON = '<svg viewBox="0 0 100 90"><circle cx="50" cy="30" r="20" fill="%s"/><path d="M8 90c4-26 22-38 42-38s38 12 42 38z" fill="%s"/></svg>'
def person(a, b): return PERSON % (a, b)
DOTS = '<i class="p" style="left:760px;top:170px;width:16px;height:16px"></i><i class="p m b" style="left:1120px;top:880px;width:22px;height:22px"></i><i class="p b" style="left:640px;top:930px;width:12px;height:12px"></i><i class="p m" style="left:1180px;top:130px;width:10px;height:10px"></i>'
BRAND = '<div class="brand" style="left:92px;top:980px;font-size:30px">MTG <span class="e">👑</span> | <span class="g">YOUR DIGITAL ARCHITECT</span></div>'
V = {}
# 1. How it works (official, 1:25, vertical video)
V['hiw'] = dict(W=1920, H=1080, gx='80%', gy='55%', gw=900, gh=800, css='', body=DOTS + '''
<div class="pill lime" style="left:92px;top:100px;font-size:30px"><i></i>OFFICIAL VIDEO · 1:25</div>
<div class="h" style="left:88px;top:200px;font-size:186px">How<br><span class="k">MoveMint</span><br>works</div>
<div class="chips" style="left:92px;top:780px;font-size:34px"><span class="chip"><span class="ic"><i>🪙</i></span>HOLD</span><span class="chip"><span class="ic"><i>🔗</i></span>SHARE</span><span class="chip"><span class="ic"><i>👟</i></span>MOVE</span></div>
<img class="robot" src="robot.png" style="left:1210px;bottom:-60px;height:960px">
<div class="coin" style="left:1650px;top:150px;width:150px;height:150px;font-size:36px">AAPL</div>
<div class="coin s" style="left:1300px;top:120px;width:120px;height:120px;font-size:28px">SILVER</div>
<div class="coin m" style="left:1760px;top:430px;width:118px;height:118px;font-size:30px">NVDA</div>
<div class="coin" style="left:1180px;top:430px;width:110px;height:110px;font-size:28px">GOLD</div>''' + BRAND)
# 2. Trailer (official, 0:49, wide)
V['trailer'] = dict(W=1920, H=1080, gx='78%', gy='45%', gw=900, gh=700, css='', body=DOTS + '''
<div class="pill lime" style="left:92px;top:100px;font-size:30px"><i></i>OFFICIAL TRAILER · 0:49</div>
<div class="h" style="left:88px;top:200px;font-size:200px"><span class="k">MoveMint</span><br>in 49<br>seconds</div>
<div class="chips" style="left:92px;top:800px;font-size:32px"><span class="chip"><span class="ic"><i>📈</i></span>STOCKS</span><span class="chip"><span class="ic"><i>🥇</i></span>GOLD</span><span class="chip"><span class="ic"><i>🏦</i></span>TREASURIES</span></div>
<div class="shot" style="left:1190px;top:200px;width:690px;height:610px;transform:rotate(4deg)"><img src="rug.jpg" style="object-position:62% 50%"></div>
<div class="dur" style="left:1650px;top:760px;font-size:30px;transform:rotate(4deg)">0:49</div>''' + BRAND)
# 3. Founder presentation, website cover (middle clear)
CALL = lambda x, y, w, h, s: f'''<div class="win" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({s}deg)">
<div class="top"><b></b><b></b><b></b><span style="margin-left:10px">MOVEMINT · LIVE CALL</span><span class="rec">1:15:00</span></div>
<div class="grid" style="grid-template-columns:2.1fr 1fr;grid-template-rows:repeat(3,1fr);height:calc(100% - 120px)">
<div class="tile main" style="grid-row:1/4"><img src="robot.png" style="position:absolute;left:50%;bottom:-18%;height:118%;transform:translateX(-50%)"><span class="nm">🎙️ Founder</span></div>
<div class="tile">{person('#7cf2c6', '#29b884')}</div><div class="tile">{person('#ffe08f', '#c99a2e')}</div><div class="tile">{person('#cfe9e2', '#7fa7a0')}</div></div>
<div class="tool"><i></i><i></i><i></i><i class="r"></i></div></div>'''
V['founder'] = dict(W=1920, H=1080, gx='80%', gy='50%', gw=900, gh=800, css='.tile .nm{font-family:Manrope,"Noto Color Emoji"}', body=DOTS + '''
<div class="pill red" style="left:92px;top:100px;font-size:30px"><i></i>FOUNDER ZOOM · FULL CALL</div>
<div class="h" style="left:88px;top:200px;font-size:186px"><span class="k">MoveMint</span><br>explained</div>
<div class="h" style="left:92px;top:560px;font-size:96px"><span class="g">by the founder</span></div>
<div class="chips" style="left:92px;top:790px;font-size:32px"><span class="chip"><span class="ic"><i>📈</i></span>STOCKS</span><span class="chip"><span class="ic"><i>🥇</i></span>GOLD</span><span class="chip"><span class="ic"><i>👟</i></span>THE APP</span></div>''' + CALL(1190, 170, 700, 700, 3) + BRAND)
# 4/5. Tutorials
def part(n, l1, l2, ok, scr, dur):
    return dict(W=1920, H=1080, gx='80%', gy='55%', gw=900, gh=800, css='', body=DOTS + f'''
<div class="pill lime" style="left:92px;top:100px;font-size:30px"><i></i>STEP BY STEP · {dur}</div>
<div class="h" style="left:84px;top:190px;font-size:250px"><span class="g">Part {n}</span></div>
<div class="h" style="left:90px;top:440px;font-size:112px;line-height:.98">{l1}<br>{l2}</div>
<div class="chips" style="left:92px;top:780px;font-size:34px"><span class="chip"><span class="ic"><i>✅</i></span>{ok}</span></div>
<div class="phone" style="left:1400px;top:70px;width:420px;height:900px;transform:rotate(6deg)"><div class="in"><img src="{scr}" style="object-position:50% 30%"></div></div>
<img class="robot" src="robot.png" style="left:1180px;bottom:-50px;height:560px">''' + BRAND)
V['part1'] = part(1, 'Join &amp; make', 'your <span class="k">wallet</span>', "You're in. Wallet made.", 'screen1.jpg', '5:12')
V['part2'] = part(2, 'Fund, swap', '&amp; buy <span class="k">MINT</span>', 'Bonus collected.', 'screen2.jpg', '5:39')
# 6. YouTube thumbnail for the founder video (full, bold)
V['yt'] = dict(W=1920, H=1080, gx='76%', gy='50%', gw=1000, gh=900, css='.tile .nm{font-family:Manrope,"Noto Color Emoji"}', body='''
<i class="p" style="left:860px;top:120px;width:18px;height:18px"></i><i class="p m b" style="left:980px;top:930px;width:24px;height:24px"></i>
<div class="pill red" style="left:84px;top:80px;font-size:40px"><i></i>THE FOUNDER · FULL CALL</div>
<div class="h" style="left:76px;top:190px;font-size:250px"><span class="k">MoveMint</span></div>
<div class="h" style="left:80px;top:440px;font-size:212px">explained</div>
<div class="chips" style="left:84px;top:720px;font-size:40px"><span class="chip"><span class="ic"><i>📈</i></span>STOCKS</span><span class="chip"><span class="ic"><i>🥇</i></span>GOLD</span><span class="chip"><span class="ic"><i>🥈</i></span>SILVER</span></div>
<div class="h" style="left:84px;top:880px;font-size:84px"><span class="g">for holding MINT</span></div>''' + CALL(1110, 150, 760, 760, 3) + '''
<div class="coin" style="left:1010px;top:90px;width:160px;height:160px;font-size:40px">AAPL</div>
<div class="coin m" style="left:1000px;top:800px;width:140px;height:140px;font-size:36px">NVDA</div>
<div class="disc" style="left:1730px;top:870px;width:160px;height:160px"><img src="mtg-disc.png"></div>''')
# 7. Social preview for mtgtribe.com/mint (1200x630)
V['og'] = dict(W=1200, H=630, gx='78%', gy='52%', gw=640, gh=560, css='.floor{background-size:100% 46px,60px 100%}', body='''
<i class="p" style="left:560px;top:90px;width:12px;height:12px"></i><i class="p m b" style="left:640px;top:560px;width:16px;height:16px"></i>
<div class="pill lime" style="left:56px;top:46px;font-size:19px"><i></i>MOVEMINT (MINT) · START HERE</div>
<div class="h" style="left:52px;top:104px;font-size:112px;line-height:.92">Hold <span class="k">MINT</span>.<br>Get stocks<br><span class="g">in your wallet</span></div>
<div class="addr" style="left:56px;top:470px;font-size:30px">mtgtribe.com/mint</div>
<div class="brand" style="left:58px;top:570px;font-size:19px">MTG <span class="e">👑</span> | <span class="g">YOUR DIGITAL ARCHITECT</span></div>
<img class="robot" src="robot.png" style="left:760px;bottom:-40px;height:560px">
<div class="coin" style="left:1050px;top:70px;width:104px;height:104px;font-size:24px">AAPL</div>
<div class="coin s" style="left:790px;top:56px;width:84px;height:84px;font-size:19px">SILVER</div>
<div class="coin m" style="left:1080px;top:300px;width:92px;height:92px;font-size:23px">NVDA</div>
<div class="coin" style="left:690px;top:196px;width:80px;height:80px;font-size:19px">GOLD</div>''')
for k, v in V.items():
    open(os.path.join(D, k + '.html'), 'w').write(BASE % v)
print(' '.join(V))
