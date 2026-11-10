# Build the calmer version of the JetUP Zoom flyer: fewer words, more space.
# Reuses the artwork (background candles, gold bar, flags) from flyer.html.
import os
here = os.path.dirname(os.path.abspath(__file__))
bgchart, hero, f_za, f_ng, f_in = open(os.path.join(here, 'parts.txt')).read().split('\n=====\n')

CSS = """
:root{
  --bg:#0b0912; --text:#f6f3ff; --body:#cfc8e6; --muted:#9c95b8;
  --vio:#9b7cff; --pink:#e371fc; --lime:#cbfb61; --gold:#e8c25a; --gold-hi:#ffe08f;
  --grad:linear-gradient(100deg,#8c6ce7 0%,#b56cf6 45%,#e371fc 100%);
  --f-d:'Anton',Impact,sans-serif; --f-b:'Manrope',system-ui,sans-serif; --emoji:'Noto Color Emoji';
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1080px;background:var(--bg);overflow:hidden}
body{font-family:var(--f-b);color:var(--text);-webkit-font-smoothing:antialiased}
.f{position:relative;width:1080px;height:1080px;padding:66px 68px 58px;overflow:hidden;display:flex;flex-direction:column;
  background:
    radial-gradient(640px 440px at 14% 26%,rgba(140,108,231,.30),transparent 70%),
    radial-gradient(560px 460px at 86% 62%,rgba(232,194,90,.17),transparent 70%),
    radial-gradient(720px 380px at 50% 110%,rgba(227,113,252,.16),transparent 70%),
    var(--bg)}
.f:before{content:"";position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);
  background-size:54px 54px;-webkit-mask-image:radial-gradient(900px 700px at 50% 40%,#000 30%,transparent 80%);mask-image:radial-gradient(900px 700px at 50% 40%,#000 30%,transparent 80%)}
.f:after{content:"";position:absolute;inset:14px;border-radius:30px;pointer-events:none;
  border:1.5px solid transparent;background:linear-gradient(135deg,rgba(155,124,255,.55),rgba(255,255,255,.06) 35%,rgba(232,194,90,.10) 65%,rgba(232,194,90,.55)) border-box;
  -webkit-mask:linear-gradient(#000 0 0) padding-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}
.bgchart{position:absolute;left:0;right:0;bottom:230px;height:420px;opacity:.07;pointer-events:none}
.z{position:relative;z-index:2;display:flex;flex-direction:column;flex:1}
svg.i{fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}

.top{display:flex;align-items:center;justify-content:space-between}
.pill{display:inline-flex;align-items:center;gap:12px;height:50px;padding:0 24px 0 20px;border-radius:999px;background:var(--lime);color:#14110b;
  font:800 22px/1 var(--f-b);letter-spacing:.14em;box-shadow:0 0 0 6px rgba(203,251,97,.12),0 10px 30px rgba(203,251,97,.18)}
.pill .dot{width:12px;height:12px;border-radius:50%;background:#e0263f;box-shadow:0 0 0 4px rgba(224,38,63,.22)}
.date{display:inline-flex;align-items:center;gap:12px;font:800 23px/1 var(--f-b);letter-spacing:.12em;color:var(--text)}
.date svg{width:27px;height:27px;color:var(--gold-hi)}

.kick{display:flex;align-items:center;gap:14px;margin-top:52px;font:800 23px/1 var(--f-b);letter-spacing:.24em;color:var(--lime)}
.kick img{width:44px;height:44px}
h1{margin-top:18px;font:400 92px/.96 var(--f-d);letter-spacing:.005em;text-transform:uppercase;white-space:nowrap}
h1 span{display:block}
h1 .w{color:#fff;text-shadow:0 6px 40px rgba(155,124,255,.25)}
h1 .g{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{margin-top:20px;font:600 29px/1.3 var(--f-b);color:var(--body)}
.sub b{color:var(--gold-hi);font-weight:800}

.mid{display:grid;grid-template-columns:500px 1fr;gap:20px;align-items:center;margin-top:auto}
.times{border-radius:26px;padding:8px 26px;background:linear-gradient(160deg,rgba(36,30,54,.85),rgba(20,17,30,.85));
  box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.10),0 18px 40px rgba(0,0,0,.35)}
.tr{display:flex;align-items:center;gap:18px;height:80px}
.tr+.tr{border-top:1.5px solid rgba(255,255,255,.08)}
.flag{flex:0 0 auto;width:46px;height:46px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 2px rgba(255,255,255,.85),0 4px 12px rgba(0,0,0,.4)}
.flag svg{display:block;width:100%;height:100%}
.cn{flex:1;font:800 23px/1 var(--f-b);letter-spacing:.05em;color:#fff}
.cn i{display:block;font-style:normal;font-weight:700;color:var(--muted);letter-spacing:.14em;font-size:15px;margin-top:6px}
.tm{font:400 50px/1 var(--f-d);letter-spacing:.02em;color:var(--gold-hi)}
.hero{position:relative;height:300px}
.hero svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}

.url{display:flex;align-items:center;gap:22px;margin-top:40px;padding:16px 28px;border-radius:26px;
  background:linear-gradient(100deg,rgba(140,108,231,.30),rgba(181,108,246,.18) 50%,rgba(227,113,252,.22));box-shadow:inset 0 0 0 1.5px rgba(155,124,255,.5)}
.url .gi{flex:0 0 auto;display:grid;place-items:center;width:62px;height:62px;border-radius:50%;background:rgba(255,255,255,.1);color:#fff}
.url .gi svg{width:34px;height:34px}
.ul{font:700 21px/1 var(--f-b);letter-spacing:.06em;color:var(--body)}
.uv{margin-top:8px;font:800 54px/1 var(--f-b);letter-spacing:-.01em;color:#fff}
.uv b{color:var(--lime);font-weight:800}

.foot{display:flex;align-items:center;justify-content:space-between;margin-top:30px;padding:0 6px;font:800 24px/1 var(--f-b);color:#fff}
.foot .slo{color:var(--gold-hi)}
.em{font-family:var(--emoji);font-weight:400}
.sep{font-family:Inter,sans-serif;font-weight:300;color:var(--gold);margin:0 6px;position:relative;top:-1px}
.disc{margin-top:14px;text-align:center;font:600 17px/1.2 var(--f-b);color:var(--muted)}
"""

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>JetUP Zoom Flyer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@500;600;700;800&display=block" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="f" id="flyer">
  {bgchart}
  <div class="z">
    <div class="top">
      <span class="pill"><i class="dot"></i>LIVE ON ZOOM</span>
      <span class="date"><svg class="i" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>SATURDAY 7 NOVEMBER 2026</span>
    </div>

    <div class="kick"><img src="jetup-mark-128.webp" alt="">JETUP PRESENTATION</div>
    <h1><span class="w">Automated gold trading,</span><span class="g">explained live</span></h1>
    <p class="sub">How it works, and the <b>$100 Fast Start bonus</b> rules.</p>

    <div class="mid">
      <div class="times">
        <div class="tr">{f_za}<span class="cn">SOUTH AFRICA<i>SAST</i></span><span class="tm">8:00 PM</span></div>
        <div class="tr">{f_ng}<span class="cn">NIGERIA<i>WAT</i></span><span class="tm">7:00 PM</span></div>
        <div class="tr">{f_in}<span class="cn">INDIA<i>IST</i></span><span class="tm">11:30 PM</span></div>
      </div>
      {hero}
    </div>

    <div class="url">
      <span class="gi"><svg class="i" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg></span>
      <div><div class="ul">Read the guide first</div><div class="uv">mtgtribe.com/<b>JetUp</b></div></div>
    </div>

    <div class="foot">
      <span>MTG <span class="em">👑</span> <span class="sep">|</span> Your Digital Architect</span>
      <span class="slo">Let's Get This Crypto! <span class="em">💪</span></span>
    </div>
    <p class="disc">Education only, not financial advice. Trading carries risk.</p>
  </div>
</div>
</body>
</html>
"""
open(os.path.join(here, 'flyer.html'), 'w').write(HTML)
print('written', len(HTML))
