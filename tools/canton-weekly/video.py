#!/usr/bin/env python3
"""Canton Weekly technical analysis video (16:9, 1920x1080) for mtgtribe.com.

Usage (from the repo root):
  python3 tools/canton-weekly/video.py DATA.json NARRATION.mp3 [MUSIC.mp3] [--silent SECONDS]

DATA.json needs "video_script": a list of {"scene": name, "text": narration, "caption": optional on-screen wording (write numbers as $0.1046, CNTN, mtgtribe.com)}.
Scenes: intro, price, trend, levels, scenarios, fundamentals, burn, halving, guides, tribe, streams, bellver, outro.
The streams scene shows phone screenshots of mtgtribe.com taken at render time (menu_capture.js, this checkout on localhost).
Run prepare.py first: it adds the daily candles ("candles", for the 3D candlestick chart with MA20, MA50, volume
and RSI) and the approved Bellver Card ad scene. Without "candles" the chart falls back to the old line chart.
Check frames without a full render: --silent 120 --stills 20,40,60 writes PNG stills next to the video.
Segment timing: each segment's share of the narration is proportional to its
length in characters (the narration is generated from the same segments, joined
with short pauses), so visuals change when the matching sentence starts.
Music: the closing track starts at (duration - 50s), fades in, is ducked under the
voice and fades out with the video. Output: canton-weekly/<date>/video.mp4 + poster.jpg
"""
import json, os, re, subprocess, sys, tempfile

ROOT = os.getcwd()
CARD = os.path.join(ROOT, "assets", "tribe", "bellver-card-640.webp")

FPS = 25
W, H = 1920, 1080

def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path]).strip())

def timeline(segs, total):
    w = [max(20, len(re.sub(r"<[^>]+>", "", s["text"]))) for s in segs]
    t, out = 0.0, []
    for s, x in zip(segs, w):
        d = total * x / sum(w)
        out.append({"scene": s["scene"], "start": t, "end": t + d, "text": s.get("caption") or re.sub(r"<[^>]+>", "", s["text"])})
        t += d
    return out

HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700;800&family=Outfit:wght@800;900&family=JetBrains+Mono:wght@500;700&display=swap');
*{box-sizing:border-box}body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#040506;color:#f7f8fa;font-family:'DM Sans','Inter',sans-serif}
#st{position:absolute;inset:0;background:radial-gradient(ellipse at 50% -10%,rgba(242,173,60,.22),transparent 45%),linear-gradient(180deg,#0a0c0e,#040506)}
#st:before{content:"";position:absolute;inset:0;background:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px) 0 0/80px 80px,linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px) 0 0/80px 80px}
.brand{position:absolute;top:48px;left:72px;display:flex;align-items:center;gap:16px;font:800 26px 'Outfit','Inter';letter-spacing:.16em}
.brand i{display:grid;place-items:center;width:58px;height:58px;border-radius:50%;border:2px solid #f2ad3c;font-style:normal;letter-spacing:0;font-size:28px;box-shadow:0 0 30px rgba(242,173,60,.35)}
.tag{position:absolute;top:58px;right:72px;padding:12px 22px;border:2px solid rgba(242,173,60,.5);border-radius:999px;color:#f2c56b;font:800 22px 'DM Sans','Inter';letter-spacing:.14em;text-transform:uppercase}
.sc{position:absolute;inset:140px 120px 200px;display:none;flex-direction:column;justify-content:center}
.k{color:#f2c56b;font:800 26px 'DM Sans','Inter';letter-spacing:.2em;text-transform:uppercase;margin-bottom:20px}
h1{margin:0;font:900 120px/1 'Outfit','Inter Display','Inter';letter-spacing:-.04em}
h2{margin:0 0 30px;font:900 84px/1.05 'Outfit','Inter Display','Inter';letter-spacing:-.035em}
.g{background:linear-gradient(180deg,#fff2d2,#ffd47c 40%,#f2ad3c 75%);-webkit-background-clip:text;color:transparent}
.big{font:700 190px/1 'JetBrains Mono',monospace;letter-spacing:-.04em}
.row{display:flex;gap:28px;margin-top:40px}
.tile{flex:1;padding:30px 34px;border-radius:28px;border:2px solid rgba(255,255,255,.1);background:rgba(255,255,255,.03)}
.tile span{display:block;color:#8a919b;font:800 22px 'DM Sans','Inter';letter-spacing:.12em;text-transform:uppercase}
.tile b{display:block;margin-top:12px;font:700 58px 'JetBrains Mono',monospace}
.dn{color:#ff8a7a}.up{color:#3ddc84}
.card{display:flex;align-items:center;gap:30px;padding:30px 36px;margin-bottom:22px;border-radius:26px;border:2px solid rgba(255,255,255,.1);background:rgba(255,255,255,.03);font-size:40px}
.card b{font:800 44px 'Outfit','Inter'}.card em{font-style:normal;color:#c3c7cd;margin-left:auto;font:600 36px 'JetBrains Mono',monospace}
.cta{display:inline-flex;margin-top:30px;padding:26px 40px;border-radius:22px;background:linear-gradient(180deg,#f6bd59,#ca8318);color:#1b1102;font:800 40px 'DM Sans','Inter';letter-spacing:.04em;text-transform:uppercase;box-shadow:0 12px 0 rgba(113,67,6,.45),0 0 60px rgba(242,173,60,.3)}
#cap{position:absolute;left:50%;bottom:56px;transform:translateX(-50%);max-width:1560px;padding:18px 32px;border-radius:18px;background:rgba(0,0,0,.72);color:#fff;font:700 40px/1.3 'DM Sans','Inter';text-align:center}
#prog{position:absolute;left:0;bottom:0;height:8px;background:linear-gradient(90deg,#f2ad3c,#ffe2aa)}
svg text{font-family:'JetBrains Mono',monospace}
#s-trend h2,#s-levels h2{font-size:58px;margin:0 0 12px}
.legend{display:flex;gap:16px;margin:0 0 16px;font:700 24px 'DM Sans','Inter'}
.legend span{display:inline-flex;align-items:center;gap:10px;padding:8px 16px;border-radius:999px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04)}
.legend i{width:26px;height:6px;border-radius:3px}
.stage3d{perspective:2000px;perspective-origin:50% 30%}
.panel3d{position:relative;transform-style:preserve-3d;border-radius:26px;padding:18px 22px 8px;border:1.5px solid rgba(242,173,60,.38);background:linear-gradient(160deg,rgba(26,22,14,.92),rgba(9,10,12,.95) 55%);box-shadow:0 60px 90px -30px rgba(0,0,0,.85),0 0 0 1px rgba(255,255,255,.04) inset,0 0 70px rgba(242,173,60,.14)}
.panel3d:after{content:"";position:absolute;left:6%;right:6%;bottom:-46px;height:46px;border-radius:50%;background:radial-gradient(ellipse,rgba(242,173,60,.28),transparent 70%);filter:blur(6px);transform:translateZ(-40px)}
#s-bellver{flex-direction:row!important;align-items:center;gap:70px}
#bv-card{flex:0 0 760px;perspective:1600px;display:grid;place-items:center;position:relative}
#bv-card:before{content:"";position:absolute;left:12%;right:12%;bottom:-30px;height:60px;border-radius:50%;background:radial-gradient(ellipse,rgba(242,173,60,.45),transparent 70%);filter:blur(8px)}
#bv-card img{width:100%;filter:drop-shadow(40px 50px 50px rgba(0,0,0,.7)) drop-shadow(0 0 40px rgba(242,173,60,.25))}
#s-bellver .k:before{content:"";display:inline-block;width:14px;height:14px;margin-right:14px;border-radius:50%;background:#f2ad3c;box-shadow:0 0 14px #f2ad3c;vertical-align:2px}
#s-bellver h2{font-size:96px;margin:0 0 26px}
.bvchips{display:flex;flex-direction:column;gap:14px;align-items:flex-start}
.bvchips span{padding:14px 26px;border-radius:999px;border:2px solid rgba(242,173,60,.4);background:rgba(242,173,60,.08);color:#f1e3c4;font:800 34px 'DM Sans','Inter'}
.bvcta{display:inline-flex;margin-top:30px;padding:22px 40px;border-radius:20px;background:linear-gradient(180deg,#f6bd59,#ca8318);color:#1b1102;font:800 44px 'DM Sans','Inter';letter-spacing:.02em;box-shadow:0 12px 0 rgba(113,67,6,.45),0 0 70px rgba(242,173,60,.45)}
.bvsmall{margin-top:18px;color:#8a919b;font:600 24px 'DM Sans','Inter'}

.chips{display:flex;flex-direction:column;gap:14px;align-items:flex-start}
.chips span{padding:14px 26px;border-radius:999px;border:2px solid rgba(242,173,60,.4);background:rgba(242,173,60,.08);color:#f1e3c4;font:800 32px 'DM Sans','Inter'}
.src{margin-top:20px;color:#8a919b;font:600 22px 'DM Sans','Inter'}
#s-burn,#s-halving{flex-direction:row!important;align-items:center;gap:60px}
#s-burn h2,#s-halving h2{font-size:72px;margin:0 0 26px}
#s-halving .chips span{font-size:29px}
#furnace{flex:0 0 620px;height:700px;position:relative}
#furnace .fl{position:absolute;left:50%;bottom:40px;border-radius:50% 50% 46% 46%/62% 62% 38% 38%;transform-origin:50% 100%;filter:blur(6px)}
#furnace .base{position:absolute;left:8%;right:8%;bottom:0;height:90px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,120,40,.55),transparent 70%);filter:blur(10px)}
.coin{position:absolute;left:0;top:0;width:96px;height:96px;margin:-48px 0 0 -48px;border-radius:50%;display:grid;place-items:center;font:900 34px 'Outfit','Inter';color:#3a2604;background:radial-gradient(circle at 35% 30%,#fff2d2,#f6c35d 40%,#b8761a 80%);border:4px solid #ffe2aa;box-shadow:0 10px 30px rgba(0,0,0,.5),0 0 30px rgba(242,173,60,.45)}
#hv-chart{flex:0 0 1000px}
#hv-chart svg text{font-family:'DM Sans','Inter',sans-serif}
#s-tribe{align-items:center;text-align:center}
#wa{width:220px;height:220px;border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle at 35% 30%,#5af08f,#25d366 55%,#128c4a);box-shadow:0 0 0 0 rgba(37,211,102,.5),0 30px 60px rgba(0,0,0,.5);position:relative;margin-bottom:30px}
#wa svg{width:120px;height:120px;fill:#fff}
#wa .rg{position:absolute;inset:0;border-radius:50%;border:4px solid rgba(37,211,102,.7)}
#s-tribe h1{font-size:112px}
#trl{margin-top:24px;font:800 40px 'DM Sans','Inter';color:#d9f7e4}
#trcta{display:inline-flex;align-items:center;gap:18px;margin-top:34px;padding:24px 44px;border-radius:22px;background:linear-gradient(180deg,#3be37f,#169c4f);color:#03170a;font:800 46px 'DM Sans','Inter';box-shadow:0 12px 0 rgba(8,70,34,.55),0 0 70px rgba(37,211,102,.45)}
.pop{position:absolute;font-size:80px;filter:drop-shadow(0 8px 16px rgba(0,0,0,.5))}
#s-streams{inset:104px 110px 136px!important;flex-direction:row!important;align-items:center;gap:80px}
#ph{flex:0 0 auto;position:relative;width:398px;height:840px;border-radius:64px;padding:14px;background:linear-gradient(145deg,#f7e2b0,#b98a3c 30%,#5b4320 50%,#d9b46a 75%,#8a6428);box-shadow:0 50px 80px -20px rgba(0,0,0,.85),0 0 80px rgba(242,173,60,.25)}
#ph:before{content:"";position:absolute;right:-5px;top:180px;width:5px;height:90px;border-radius:0 4px 4px 0;background:#b98a3c}
#ph .scr{position:relative;width:370px;height:812px;border-radius:52px;overflow:hidden;background:#000;border:3px solid #050505}
#ph .scr img{position:absolute;left:0;top:44px;width:370px;height:801px;transform-origin:0 0}
#ph .scr:before{content:"";position:absolute;left:0;right:0;top:0;height:44px;background:#000;z-index:3}
#ph .isl{position:absolute;left:50%;top:22px;width:110px;height:32px;margin-left:-55px;border-radius:20px;background:#000;z-index:5}
#ph .tap{position:absolute;width:80px;height:80px;margin:-40px 0 0 -40px;border-radius:50%;border:5px solid #ffe2aa;background:rgba(242,173,60,.25);z-index:6;opacity:0}
#ph .hl{position:absolute;border:4px solid #f2ad3c;border-radius:16px;box-shadow:0 0 0 4px rgba(242,173,60,.25),0 0 40px rgba(242,173,60,.8);z-index:4;opacity:0}
#st-r{flex:1;min-width:0}
#st-r h2{font-size:64px;margin:0 0 20px}
#st-path{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:22px}
#st-path span{padding:10px 20px;border-radius:12px;border:2px solid rgba(255,255,255,.14);color:#c3c7cd;font:800 28px 'DM Sans','Inter';transition:none}
#st-path span.on{border-color:#f2ad3c;color:#1b1102;background:linear-gradient(180deg,#f6bd59,#ca8318)}
#st-list{display:flex;flex-direction:column;gap:10px}
#st-list div{display:flex;align-items:center;gap:22px;padding:8px 22px;border-radius:18px;border:2px solid rgba(255,255,255,.08);background:rgba(255,255,255,.03);font:800 34px 'Outfit','Inter'}
#st-list div b{display:grid;place-items:center;width:48px;height:48px;border-radius:14px;background:rgba(242,173,60,.14);color:#f2c56b;font:900 32px 'Outfit','Inter'}
#st-list div.on{border-color:#f2ad3c;background:linear-gradient(90deg,rgba(242,173,60,.22),rgba(242,173,60,.04));box-shadow:0 0 40px rgba(242,173,60,.25)}
#st-cta{display:inline-flex;margin-top:20px;padding:14px 30px;border-radius:18px;background:linear-gradient(180deg,#f6bd59,#ca8318);color:#1b1102;font:800 36px 'DM Sans','Inter';box-shadow:0 10px 0 rgba(113,67,6,.45),0 0 60px rgba(242,173,60,.4)}
#st-sm{display:inline-block;margin-left:22px;vertical-align:middle;color:#8a919b;font:600 22px/1.3 'DM Sans','Inter';max-width:420px}
</style></head><body><div id="st">
<div class="brand"><i>👑</i>MTG TRIBE</div><div class="tag">Canton Weekly · __DATE__</div>
<div class="sc" id="s-intro"><div class="k">Weekly market report</div><h1>Canton Coin<br><span class="g">__DATE__</span></h1></div>
<div class="sc" id="s-price"><div class="k">Price snapshot</div><div class="big g" id="px">$0.0000</div>
 <div class="row">__TILES__</div></div>
<div class="sc" id="s-trend"><div class="k">The trend</div><h2>__TREND_H__</h2>__LEGEND__<div class="stage3d"><div class="panel3d" id="pan1"><div id="chartwrap"></div></div></div></div>
<div class="sc" id="s-levels"><div class="k">Key levels</div><h2>Where to watch</h2>__LEGEND__<div class="stage3d"><div class="panel3d" id="pan2"><div id="chartwrap2"></div></div></div></div>
<div class="sc" id="s-scenarios"><div class="k">Three scenarios this week</div>__SCEN__</div>
<div class="sc" id="s-fundamentals"><div class="k">Fundamentals: __SCORE__</div>__FUND__</div>
<div class="sc" id="s-guides"><div class="k">Learn step by step</div><h2>How to buy <span class="g">Canton Coin</span><br>and <span class="g">CNTN stock</span></h2><div style="font:700 72px 'JetBrains Mono',monospace;color:#ffe2aa">mtgtribe.com/cc<br>mtgtribe.com/cntn</div></div>
<div class="sc" id="s-bellver"><div id="bv-card"><img id="bvimg" src="file://__CARD__" alt=""></div><div style="flex:1;min-width:0"><div class="k">Bellver crypto debit card</div><h2 id="bvh">The card that can <span class="g">pay your bills</span></h2><div class="bvchips"><span>💳 Spend your crypto worldwide</span><span>💸 Earn $10 to $500 per referral</span><span>👥 Monthly rewards from your team</span></div><div class="bvcta" id="bvcta">bellveraffiliates.com</div><div class="bvsmall" id="bvsm">Order your card or become a partner. Earnings are not guaranteed.</div></div></div>
<div class="sc" id="s-burn"><div id="furnace"><div class="base"></div><div class="fl" id="fl1" style="width:420px;height:520px;margin-left:-210px;background:radial-gradient(ellipse at 50% 80%,rgba(255,90,30,.95),rgba(255,60,20,.5) 50%,transparent 72%)"></div><div class="fl" id="fl2" style="width:300px;height:400px;margin-left:-150px;background:radial-gradient(ellipse at 50% 80%,rgba(255,190,60,.95),rgba(255,130,30,.6) 50%,transparent 72%)"></div><div class="fl" id="fl3" style="width:170px;height:250px;margin-left:-85px;background:radial-gradient(ellipse at 50% 80%,#fff6d8,rgba(255,220,120,.85) 45%,transparent 72%)"></div><div id="coins"></div></div>
 <div style="flex:1;min-width:0"><div class="k">Universal burn · CIP-0129</div><h2 id="bnh">Every synchronizer <span class="g">burns CC</span></h2><div class="chips" id="bnc"><span>✅ Approved by the Super Validators, 23 Oct 2026</span><span>🔗 Private synchronizers burn CC too</span><span>📅 First phase expected Q1 2027 (an estimate)</span><span>🔥 More use, more CC burned</span><span>📉 Fewer coins in circulation</span></div><div class="src" id="bns">Source: Canton Foundation, CIP-0129</div></div></div>
<div class="sc" id="s-halving"><div style="flex:0 0 600px"><div class="k">The Canton halving</div><h2 id="hvh">New CC <span class="g">keeps shrinking</span></h2><div class="chips" id="hvc"><span>🔥 The burn takes coins out</span><span>🐢 The halving slows new coins in</span><span>💎 Why I keep accumulating</span></div><div class="src">Sources: Canton Coin white paper, CIP-0105. Dates are forecasts.</div></div><div id="hv-chart"></div></div>
<div class="sc" id="s-tribe"><div id="wa"><i class="rg" id="rg1"></i><i class="rg" id="rg2"></i><svg viewBox="0 0 24 24"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.47-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35m-5.42 7.4h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.69 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.41Z"/></svg></div><h1>Thank you, <span class="g">MTG TRIBE</span> 🙏</h1><div id="trl">My updates are posted in the WhatsApp group first</div><div id="trcta">Join us: mtgtribe.com/group</div><div id="pops"></div></div>
<div class="sc" id="s-streams"><div id="ph"><div class="scr" id="phs"><div class="isl"></div><img id="im0" src="file://__M_HOME__" alt=""><img id="im1" src="file://__M_DASH__" alt=""><img id="im2" src="file://__M_MENU__" alt=""><div class="hl" id="phl"></div><div class="tap" id="tap"></div></div></div>
 <div id="st-r"><div class="k">Where my money comes from</div><h2>My multiple <span class="g">streams of income</span></h2><div id="st-path"><span>mtgtribe.com</span><span>Dashboard</span><span>Menu</span><span>Income streams</span></div><div id="st-list">__ST_LIST__</div><div id="st-cta">Test drive one: mtgtribe.com</div><div id="st-sm">This is how MTG generates his cash flow. Results differ for everyone.</div></div></div>
<div class="sc" id="s-outro" style="align-items:center;text-align:center"><div class="k">Not financial advice · Do your own research</div><h1 class="g" style="font-size:110px">Let's Get This Crypto! 💪</h1><div style="margin-top:30px;font:800 40px 'DM Sans','Inter'">MTG 👑 | Your Digital Architect</div><div class="cta">Join the MTG TRIBE · mtgtribe.com/group</div></div>
<div id="cap"></div><div id="prog"></div></div>
<script>
const TL=__TL__, TOTAL=__TOTAL__, CL=__CLOSES__, LINES=__LINES__, PRICE=__PRICE__, CDL=__CANDLES__, CUES=__CUES__, MB=__MBOX__, HV=__HV__;const BV=CUES.bellver||{};
function chart(el,showLines,p){const W=1640,H=520,L=110,R=30,T=20,B=50;const v=CL.map(c=>c[1]);const all=v.concat(LINES.map(l=>l.v));const lo=Math.min(...all)*.97,hi=Math.max(...all)*1.02;
 const xs=i=>L+i*(W-L-R)/(v.length-1),ys=x=>T+(hi-x)*(H-T-B)/(hi-lo);let s=`<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`;
 for(let g=Math.ceil(lo*100)/100;g<hi;g+=.01){s+=`<line x1="${L}" x2="${W-R}" y1="${ys(g)}" y2="${ys(g)}" stroke="rgba(255,255,255,.08)"/><text x="${L-14}" y="${ys(g)+8}" text-anchor="end" fill="#8a919b" font-size="24">$${g.toFixed(2)}</text>`}
 const n=Math.max(2,Math.round(v.length*Math.min(1,showLines?1:p*1.4)));const pts=v.slice(0,n).map((x,i)=>xs(i)+','+ys(x)).join(' ');
 if(showLines)LINES.forEach((l,i)=>{const a=Math.min(1,Math.max(0,p*LINES.length*1.3-i));const c=l.kind=='support'?'#3ddc84':'#ff7b6b';s+=`<g opacity="${a}"><line x1="${L}" x2="${W-R}" y1="${ys(l.v)}" y2="${ys(l.v)}" stroke="${c}" stroke-width="4" stroke-dasharray="14 10"/><rect x="${W-R-250}" y="${ys(l.v)-44}" width="250" height="38" rx="10" fill="#0b0d10" stroke="${c}"/><text x="${W-R-125}" y="${ys(l.v)-16}" text-anchor="middle" fill="${c}" font-size="24" font-weight="700">${l.kind=='support'?'Support':'Resistance'} $${l.v}</text></g>`});
 s+=`<polyline points="${pts}" fill="none" stroke="#f2ad3c" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>`;
 const lx=xs(n-1),ly=ys(v[n-1]);s+=`<circle cx="${lx}" cy="${ly}" r="${18+4*Math.sin(p*20)}" fill="#f2ad3c" opacity=".25"/><circle cx="${lx}" cy="${ly}" r="10" fill="#ffe2aa"/>`;
 s+=`<text x="${L}" y="${H-8}" fill="#8a919b" font-size="24">${CL[0][0]}</text><text x="${W-R}" y="${H-8}" text-anchor="end" fill="#8a919b" font-size="24">${CL[CL.length-1][0]}</text></svg>`;el.innerHTML=s}

function f4(x){return '$'+x.toFixed(4)}
function candle(el,showLines,p,pan){const R=CDL.rows,W=1600,H=530,L=118,RT=150,T=14,PB=262,VT=282,VB=336,RS=366,RB=492;
 const n=R.length,step=(W-L-RT)/n,bw=Math.max(4,step*.62);
 let lo=Math.min(...R.map(r=>r.l)),hi=Math.max(...R.map(r=>r.h));R.forEach(r=>{if(r.ma20){lo=Math.min(lo,r.ma20);hi=Math.max(hi,r.ma20)}if(r.ma50){lo=Math.min(lo,r.ma50);hi=Math.max(hi,r.ma50)}});
 if(showLines)LINES.forEach(l=>{lo=Math.min(lo,l.v);hi=Math.max(hi,l.v)});const pad=(hi-lo)*.06;lo-=pad;hi+=pad;
 const x=i=>L+step*(i+.5),y=v=>T+(hi-v)*(PB-T)/(hi-lo),vmax=Math.max(...R.map(r=>r.v)),vy=v=>VB-(v/vmax)*(VB-VT),ry=v=>RS+(100-v)*(RB-RS)/100;
 const shown=showLines?n:Math.max(2,Math.round(n*Math.min(1,.15+p*1.5)));
 let s=`<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><defs><linearGradient id="rsiF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2aa" stop-opacity=".25"/><stop offset="1" stop-color="#ffe2aa" stop-opacity="0"/></linearGradient></defs>`;
 for(let k=0;k<=4;k++){const v=lo+(hi-lo)*k/4;s+=`<line x1="${L}" x2="${W-RT}" y1="${y(v)}" y2="${y(v)}" stroke="rgba(255,255,255,.06)"/><text x="${L-14}" y="${y(v)+8}" text-anchor="end" fill="#8a919b" font-size="21">${f4(v)}</text>`}
 for(let i=0;i<shown;i++){const r=R[i],up=r.c>=r.o,c=up?'#3ddc84':'#ff6b5b';s+=`<rect x="${x(i)-bw/2}" y="${vy(r.v)}" width="${bw}" height="${VB-vy(r.v)}" rx="1.5" fill="${c}" opacity=".45"/>`}
 for(let i=0;i<shown;i++){const r=R[i],up=r.c>=r.o,c=up?'#3ddc84':'#ff6b5b',top=y(Math.max(r.o,r.c)),bh=Math.max(2,Math.abs(y(r.o)-y(r.c)));
  s+=`<line x1="${x(i)}" x2="${x(i)}" y1="${y(r.h)}" y2="${y(r.l)}" stroke="${c}" stroke-width="2.4"/><rect x="${x(i)-bw/2}" y="${top}" width="${bw}" height="${bh}" rx="2" fill="${up?'rgba(61,220,132,.9)':'rgba(255,107,91,.95)'}" stroke="${c}"/>`}
 const path=(k)=>{let d='';for(let i=0;i<shown;i++){const v=R[i][k];if(v==null)continue;d+=(d?'L':'M')+x(i)+','+y(v)}return d};
 s+=`<path d="${path('ma50')}" fill="none" stroke="#7cc4ff" stroke-width="4" stroke-linejoin="round" opacity=".95"/><path d="${path('ma20')}" fill="none" stroke="#f2ad3c" stroke-width="4" stroke-linejoin="round"/>`;
 if(showLines){const LS=LINES.map((l,i)=>({l,i,ly:y(l.v)})).sort((a,b)=>a.ly-b.ly);for(let k=1;k<LS.length;k++)if(LS[k].ly-LS[k-1].ly<40)LS[k].ly=LS[k-1].ly+40;const ov=LS.length?Math.max(0,LS[LS.length-1].ly-(PB-6)):0;LS.forEach(o=>o.ly-=ov);LS.forEach(({l,i,ly})=>{const a=Math.min(1,Math.max(0,p*LINES.length*1.4-i));const c=l.kind=='support'?'#3ddc84':'#ff7b6b';s+=`<g opacity="${a}"><line x1="${L}" x2="${W-RT}" y1="${y(l.v)}" y2="${y(l.v)}" stroke="${c}" stroke-width="3" stroke-dasharray="12 9"/><line x1="${W-RT}" x2="${W-RT+8}" y1="${y(l.v)}" y2="${ly}" stroke="${c}" stroke-width="2"/><rect x="${W-RT+8}" y="${ly-18}" width="${RT-10}" height="36" rx="9" fill="#0b0d10" stroke="${c}"/><text x="${W-RT+8+(RT-10)/2}" y="${ly+8}" text-anchor="middle" fill="${c}" font-size="20" font-weight="700">${f4(l.v)}</text></g>`})}
 const last=R[shown-1];if(!showLines||true){const ly=y(last.c);s+=`<line x1="${x(shown-1)}" x2="${W-RT}" y1="${ly}" y2="${ly}" stroke="#ffe2aa" stroke-opacity=".5" stroke-dasharray="3 6"/>`;if(!showLines)s+=`<rect x="${W-RT+8}" y="${ly-20}" width="${RT-10}" height="40" rx="10" fill="#f2ad3c"/><text x="${W-RT+8+(RT-10)/2}" y="${ly+8}" text-anchor="middle" fill="#1b1102" font-size="21" font-weight="700">${f4(last.c)}</text>`}
 s+=`<rect x="${L}" y="${ry(70)}" width="${W-L-RT}" height="${ry(30)-ry(70)}" fill="rgba(255,255,255,.035)"/>`;
 [70,50,30].forEach(v=>{s+=`<line x1="${L}" x2="${W-RT}" y1="${ry(v)}" y2="${ry(v)}" stroke="rgba(255,255,255,${v==50?.06:.16})" stroke-dasharray="${v==50?'2 6':'8 8'}"/>${v==50?'':`<text x="${L-14}" y="${ry(v)+7}" text-anchor="end" fill="#8a919b" font-size="19">${v}</text>`}`});
 let rd='',ra='';for(let i=0;i<shown;i++){const v=R[i].rsi;if(v==null)continue;rd+=(rd?'L':'M')+x(i)+','+ry(v)}
 s+=`<path d="${rd}" fill="none" stroke="#ffe2aa" stroke-width="3.5" stroke-linejoin="round"/>`;
 if(last.rsi!=null)s+=`<rect x="${W-RT+8}" y="${ry(last.rsi)-18}" width="${RT-10}" height="36" rx="9" fill="#14110b" stroke="#ffe2aa"/><text x="${W-RT+8+(RT-10)/2}" y="${ry(last.rsi)+7}" text-anchor="middle" fill="#ffe2aa" font-size="19" font-weight="700">RSI ${last.rsi.toFixed(0)}</text>`;
 
 const dl=i=>{const d=new Date(R[i].d+'T00:00:00Z');return d.toLocaleDateString('en-GB',{day:'numeric',month:'short',timeZone:'UTC'})};
 [0,Math.floor(n/2),n-1].forEach((i,k)=>{s+=`<text x="${x(i)}" y="${H-2}" text-anchor="${k==0?'start':k==2?'end':'middle'}" fill="#8a919b" font-size="20">${dl(i)}</text>`});
 s+=`</svg>`;el.innerHTML=s;
 const ry3=(showLines?-9:-14)+p*7;pan.style.transform=`rotateX(${14-p*4}deg) rotateY(${ry3}deg) rotateZ(${showLines?0.6:1.2}deg) translateZ(0)`}
function bellver(p){const cue=k=>BV[k]||0,on=(c,d=.06)=>ease((p-c)/d);
 const img=document.getElementById('bvimg');const a=ease(p*8);img.style.transform=`rotateY(${-28+16*a+4*Math.sin(p*9)}deg) rotateX(${10-4*a}deg) rotateZ(${-6+3*a}deg) translateY(${(1-a)*60+10*Math.sin(p*12)}px) scale(${.85+.15*a})`;img.style.opacity=a;
 const h=document.getElementById('bvh');const ah=on(cue('card'));h.style.opacity=ah;h.style.transform=`translateY(${(1-ah)*30}px)`;
 document.querySelectorAll('.bvchips span').forEach((c,i)=>{const ac=on(cue(['spend','earn','team'][i]));c.style.opacity=ac;c.style.transform=`translateX(${(1-ac)*60}px)`});
 const cta=document.getElementById('bvcta'),ak=on(cue('order'));cta.style.opacity=ak;cta.style.transform=`scale(${(.9+.1*ak)*(1+.035*Math.sin(p*40)*ak)})`;
 document.getElementById('bvsm').style.opacity=on(cue('order')+.04)}

function cueOf(sc,k){return (CUES[sc]||{})[k]||0}
function burn(p){const on=(k,d=.05)=>ease((p-cueOf('burn',k))/d);
 const t=p*40;[1,2,3].forEach(i=>{const f=document.getElementById('fl'+i);f.style.transform=`scaleY(${1+.08*Math.sin(t*(1.3+i*.4)+i)}) scaleX(${1+.05*Math.sin(t*(1.7+i*.3))}) rotate(${2*Math.sin(t*.9+i)}deg)`});
 let c='';for(let i=0;i<7;i++){const ph=((p*5+i/7)%1),x=310+Math.sin(i*2.1)*150*(1-ph),y=-40+ph*560,o=ph<.72?1:Math.max(0,1-(ph-.72)/.2),sc=ph<.72?1:Math.max(.2,1-(ph-.72)*2.5);c+=`<div class="coin" style="transform:translate(${x}px,${y}px) rotate(${12*Math.sin(p*20+i)}deg) rotateY(${Math.sin(p*14+i)*35}deg) scale(${sc});opacity:${o}">CC</div>`}
 document.getElementById('coins').innerHTML=c;
 const h=document.getElementById('bnh'),a=ease(p*8);h.style.opacity=a;h.style.transform=`translateY(${(1-a)*30}px)`;
 ['ok','all','when','more','fewer'].forEach((k,i)=>{const e=document.querySelectorAll('#bnc span')[i],v=on(k);e.style.opacity=v;e.style.transform=`translateX(${(1-v)*60}px) scale(${1+.04*Math.max(0,1-Math.abs(p-cueOf('burn',k)-.03)/.03)})`});
 document.getElementById('bns').style.opacity=on('ok')}
function halving(p){const on=(k,d=.05)=>ease((p-cueOf('halving',k))/d);
 const W=1000,H=640,L=40,B=110,T=120,bw=150,gap=(W-L*2-bw*5)/4,mx=40;const y=v=>H-B-(v/mx)*(H-B-T);
 const cu=cueOf('halving','cut'),grow=[ease(p*6),ease((p-cu)/.05),ease((p-cu-.04)/.05),on('h1'),on('h2')];
 let s=`<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><defs><linearGradient id="hg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2aa"/><stop offset=".5" stop-color="#f2ad3c"/><stop offset="1" stop-color="#8a5a14"/></linearGradient><linearGradient id="hf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7cc4ff"/><stop offset="1" stop-color="#1d4f7a"/></linearGradient></defs>`;
 s+=`<text x="${L}" y="34" fill="#c3c7cd" font-size="26" font-weight="800">Most new CC that can be minted per year</text><line x1="${L}" x2="${W-L}" y1="${H-B}" y2="${H-B}" stroke="rgba(255,255,255,.25)" stroke-width="2"/>`;
 HV.forEach((b,i)=>{const g=grow[i],x=L+i*(bw+gap),top=y(b.v*g),fut=i>=3;
  s+=`<g opacity="${Math.min(1,g*1.5)}"><rect x="${x}" y="${top}" width="${bw}" height="${H-B-top}" rx="14" fill="url(#${fut?'hf':'hg'})" ${fut?'stroke="#bfe3ff" stroke-width="3" stroke-dasharray="10 8"':''}/>`;
  s+=`<text x="${x+bw/2}" y="${top-16}" text-anchor="middle" fill="#fff" font-size="40" font-weight="800">${b.l}</text>`;
  s+=`<text x="${x+bw/2}" y="${H-B+42}" text-anchor="middle" fill="#c3c7cd" font-size="24" font-weight="700">${b.w}</text>`;
  if(b.tag)s+=`<rect x="${x-8}" y="${H-B+60}" width="${bw+16}" height="40" rx="20" fill="${b.today?'#f2ad3c':'#0e2233'}" stroke="${b.today?'#f2ad3c':'#7cc4ff'}" stroke-width="2"/><text x="${x+bw/2}" y="${H-B+88}" text-anchor="middle" fill="${b.today?'#1b1102':'#bfe3ff'}" font-size="22" font-weight="800">${b.tag}</text>`;
  s+=`</g>`});
 for(let i=1;i<HV.length;i++){const g=grow[i];if(g<.5)continue;const x=L+i*(bw+gap)-gap/2,yy=y(HV[i-1].v)-6;{const ty=Math.max(T+10,y(HV[i].v)-78);s+=`<g opacity="${(g-.5)*2}"><rect x="${x-42}" y="${ty-26}" width="84" height="36" rx="18" fill="#2a0f0c" stroke="#ff9a8a" stroke-width="2"/><text x="${x}" y="${ty}" text-anchor="middle" fill="#ffb3a6" font-size="24" font-weight="800">−50%</text></g>`}}
 s+=`</svg>`;document.getElementById('hv-chart').innerHTML=s;
 const h=document.getElementById('hvh'),a=ease(p*8);h.style.opacity=a;h.style.transform=`translateY(${(1-a)*30}px)`;
 ['both','slow','acc'].forEach((k,i)=>{const e=document.querySelectorAll('#hvc span')[i],v=on(k);e.style.opacity=v;e.style.transform=`translateX(${(1-v)*60}px)`})}
function tribe(p){const on=(k,d=.06)=>ease((p-cueOf('tribe',k))/d);const a=ease(p*6);
 const w=document.getElementById('wa');w.style.transform=`scale(${(.6+.4*a)*(1+.04*Math.sin(p*30))})`;
 [1,2].forEach(i=>{const ph=(p*4+i*.5)%1,r=document.getElementById('rg'+i);r.style.transform=`scale(${1+ph*.9})`;r.style.opacity=1-ph});
 const l=document.getElementById('trl'),c=document.getElementById('trcta');l.style.opacity=on('first');c.style.opacity=on('join');c.style.transform=`scale(${(.9+.1*on('join'))*(1+.03*Math.sin(p*40)*on('join'))})`;
 const E=['💛','🙌','🔥','💪','🙏','👑'],P=[[230,140],[1450,120],[140,520],[1520,480],[360,660],[1330,650]];let s='';const b=on('best',.03);
 E.forEach((e,i)=>{const d=ease((p-cueOf('tribe','thanks')-i*.02)/.05);s+=`<span class="pop" style="left:${P[i][0]}px;top:${P[i][1]+10*Math.sin(p*14+i)}px;opacity:${d};transform:scale(${d*(1+.25*b*Math.max(0,Math.sin((p-cueOf('tribe','best'))*30)))})">${e}</span>`});
 document.getElementById('pops').innerHTML=s}
function streams(p){const c=k=>cueOf('streams',k),SW=370/390;
 const ims=[0,1,2].map(i=>document.getElementById('im'+i)),tap=document.getElementById('tap'),hl=document.getElementById('phl');
 const st=p<c('dash')+.035?0:p<c('menu')+.035?1:2;ims.forEach((m,i)=>{m.style.opacity=i==st?1:0});
 const t1=(p-c('dash'))/.035,t2=(p-c('menu'))/.035;let tb=null,tt=-1;if(t1>=0&&t1<1.6){tb=MB.dashboard;tt=t1}else if(t2>=0&&t2<1.6){tb=MB.menu;tt=t2}
 if(tb){tap.style.left=(tb.x+tb.w/2)*SW+'px';tap.style.top=((tb.y+tb.h/2)*SW+44)+'px';tap.style.opacity=tt<1?1:Math.max(0,1-(tt-1)/.6);tap.style.transform=`scale(${tt<.5?1-tt*.6:.7+(tt-.5)*.8})`}else tap.style.opacity=0;
 const n=MB.streams.length;let cur=-1;for(let i=0;i<n;i++)if(p>=c('s'+i))cur=i;const all=p>=c('cash');
 let z=1,oy=0;if(st==2){const zt=ease((p-c('s0')+.03)/.05);z=1+.32*zt;const a=MB.streams[0],b=MB.streams[n-1];const cy=(a.y+b.y+b.h)/2*SW;oy=zt*(cy*z+44-406)}
 const ox=Math.min(0,Math.max(370-370*z,185-142*z));ims[2].style.transform=`translate(${ox}px,${-oy}px) scale(${z})`;
 if(st==2&&(cur>=0)){const r=all?{x:MB.streams[0].x,y:MB.streams[0].y,w:MB.streams[0].w,h:MB.streams[n-1].y+MB.streams[n-1].h-MB.streams[0].y}:MB.streams[cur];const k=SW*z;
  hl.style.left=(r.x*k+ox-4)+'px';hl.style.top=(r.y*k-oy+44-4)+'px';hl.style.width=(r.w*k+8)+'px';hl.style.height=(r.h*k+8)+'px';hl.style.opacity=1}else hl.style.opacity=0;
 const ps=document.querySelectorAll('#st-path span');[['home'],['dash'],['menu'],['menu']].forEach((k,i)=>{const v=p>=c(k[0])+(i==3?.04:0);ps[i].className=v?'on':''});
 document.querySelectorAll('#st-list div').forEach((e,i)=>{const v=ease((p-c('s'+i))/.04);e.style.opacity=.18+.82*v;e.style.transform=`translateX(${(1-v)*50}px)`;e.className=(i==cur&&!all)||(all&&v>0)?'on':''});
 const ct=document.getElementById('st-cta'),cv=ease((p-c('join'))/.05);ct.style.opacity=cv;ct.style.transform=`scale(${(.9+.1*cv)*(1+.03*Math.sin(p*40)*cv)})`;document.getElementById('st-sm').style.opacity=ease((p-c('cash'))/.05)}
function ease(x){return 1-Math.pow(1-Math.min(1,Math.max(0,x)),3)}
window.renderAt=function(t){let seg=TL.find(s=>t>=s.start&&t<s.end)||TL[TL.length-1];const p=(t-seg.start)/(seg.end-seg.start);
 document.querySelectorAll('.sc').forEach(e=>{const on=e.id=='s-'+seg.scene;e.style.display=on?'flex':'none';if(on){const a=ease(p*6);e.style.opacity=Math.min(a,ease((seg.end-t)*3));e.style.transform=`translateY(${(1-a)*40}px)`}});
 if(seg.scene=='price'){document.getElementById('px').textContent='$'+(PRICE*ease(p*2.5)).toFixed(4)}
 if(seg.scene=='trend'){if(CDL)candle(document.getElementById('chartwrap'),false,p,document.getElementById('pan1'));else chart(document.getElementById('chartwrap'),false,p)}
 if(seg.scene=='levels'){if(CDL)candle(document.getElementById('chartwrap2'),true,p,document.getElementById('pan2'));else chart(document.getElementById('chartwrap2'),true,p)}
 if(seg.scene=='bellver')bellver(p);
 if(seg.scene=='burn')burn(p);
 if(seg.scene=='halving')halving(p);
 if(seg.scene=='tribe')tribe(p);
 if(seg.scene=='streams')streams(p);
 document.querySelectorAll('.card').forEach((c,i)=>{const a=ease(p*4-i*.6);c.style.opacity=a;c.style.transform=`translateX(${(1-a)*80}px)`});
 const words=seg.text.split(/(?<=[.!?:])\s+/);let acc=0,tot=seg.text.length,cur=words[0];for(const w of words){if(p<=(acc+w.length)/tot){cur=w;break}acc+=w.length}const cp=document.getElementById('cap');cp.textContent=cur;cp.style.left=seg.scene=='streams'?'1199px':'50%';cp.style.maxWidth=seg.scene=='streams'?'1180px':'1560px';
 document.getElementById('prog').style.width=(t/TOTAL*100)+'%'};
</script></body></html>"""

# Where each picture changes, by the phrase in the scene's caption (so the visuals follow MTG's voice).
CUE_PHRASES = {
    "bellver": {"card": "Get the Bellver", "spend": "Fund it", "earn": "Then share", "team": "monthly rewards", "order": "Order yours"},
    "burn": {"ok": "approved it", "all": "Soon every", "when": "The first phase", "more": "More use", "fewer": "fewer coins"},
    "halving": {"cut": "it has already", "h1": "The next halving", "h2": "The one after", "both": "The burn takes", "slow": "the halving slows", "acc": "that is why"},
    "tribe": {"thanks": "A big thank", "best": "You are the best", "first": "Not in the group", "join": "Join us"},
    "streams": {"home": "Go to mtgtribe", "dash": "tap Dashboard", "menu": "then Menu", "cash": "That is how", "join": "See one you like"},
}
NUM = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
# The Canton Coin minting curve (white paper; next step down forecast for late summer 2029 in CIP-0105). Keep in step with
# the HALVING wording in prepare.py.
HALVING_BARS = [{"v": 40, "l": "40B", "w": "Launch 2024"}, {"v": 20, "l": "20B", "w": "+6 months"},
                {"v": 10, "l": "10B", "w": "+18 months", "tag": "Today", "today": True},
                {"v": 5, "l": "5B", "w": "Summer 2029", "tag": "Next halving"}, {"v": 2.5, "l": "2.5B", "w": "About 2034", "tag": "Then for good"}]
MENU_FALLBACK = os.path.join(ROOT, "tools", "canton-weekly", "assets", "menu")


def capture_menu(tmp):
    """Click by click phone screenshots of this checkout's mtgtribe.com (home, dashboard, open menu), served on
    localhost, so the streams scene always shows the menu as it is today. Falls back to the stored copies."""
    import socket, time
    out = os.path.join(tmp, "menu"); os.makedirs(out, exist_ok=True)
    so = socket.socket(); so.bind(("127.0.0.1", 0)); port = so.getsockname()[1]; so.close()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    warn = None
    try:
        time.sleep(1)
        subprocess.run(["node", os.path.join(ROOT, "tools", "canton-weekly", "menu_capture.js"), f"http://127.0.0.1:{port}", out], check=True, timeout=180)
    except Exception as e:
        warn = f"menu capture failed ({e}): the streams scene used the stored screenshots in {MENU_FALLBACK}"
        out = MENU_FALLBACK
    finally:
        srv.terminate()
    m = {k: os.path.join(out, k + ".jpg") for k in ("home", "dash", "menu")}
    m["boxes"] = json.load(open(os.path.join(out, "boxes.json")))
    m["warn"] = warn
    return m


def build_html(d, tl, total, menu):
    s = d["video_vis"]
    tiles = "".join(f'<div class="tile"><span>{a}</span><b class="{c}">{b}</b></div>' for a, b, c in s["tiles"])
    scen = "".join(f'<div class="card"><b>{a}</b><span>{b}</span><em>{c}</em></div>' for a, b, c in s["scenarios"])
    fund = "".join(f'<div class="card" style="font-size:38px">{x}</div>' for x in s["fundamentals"])
    cd = d.get("candles")
    legend = ""
    if cd:
        last = cd["rows"][-1]
        rsi = f': {last["rsi"]:.0f}' if last.get("rsi") is not None else ""
        legend = ('<div class="legend"><span><i style="background:#f2ad3c"></i>MA 20</span><span><i style="background:#7cc4ff"></i>MA 50</span>'
                  f'<span><i style="background:rgba(61,220,132,.5)"></i>Volume</span><span><i style="background:#ffe2aa"></i>RSI 14{rsi}</span>'
                  f'<span style="border:0;background:none;color:#8a919b;font-weight:600">{cd["source"]}</span></div>')
    cues = {}
    for sc, phrases in CUE_PHRASES.items():
        x = next((x for x in d["video_script"] if x["scene"] == sc), None)
        if not x:
            continue
        cap = x.get("caption") or x["text"]
        if sc == "streams":
            phrases = dict(phrases, **{f"s{i}": f"{NUM[i]}, " for i in range(len(menu["boxes"]["streams"]))})
        cues[sc] = {}
        for k, ph in phrases.items():
            i = cap.find(ph)
            cues[sc][k] = round(i / len(cap), 4) if i >= 0 else 0
    st_list = "".join(f"<div><b>{i + 1}</b>{n['name']}</div>" for i, n in enumerate(menu["boxes"]["streams"]))
    h = HTML
    for k, v in {"__DATE__": d["date_h"], "__TILES__": tiles, "__TREND_H__": s["trend_h"], "__SCEN__": scen, "__FUND__": fund, "__SCORE__": d["fund_score"],
                 "__TL__": json.dumps(tl), "__TOTAL__": str(total), "__CLOSES__": json.dumps(d["closes"]), "__LINES__": json.dumps(d["chart_lines"]), "__PRICE__": str(s["price"]), "__CANDLES__": json.dumps(cd) if cd else "null", "__LEGEND__": legend,
                 "__CUES__": json.dumps(cues), "__CARD__": CARD, "__MBOX__": json.dumps(menu["boxes"]), "__HV__": json.dumps(HALVING_BARS),
                 "__M_HOME__": menu["home"], "__M_DASH__": menu["dash"], "__M_MENU__": menu["menu"], "__ST_LIST__": st_list}.items():
        h = h.replace(k, v)
    return h

def main():
    args = [a for a in sys.argv[1:]]
    silent = None
    if "--silent" in args:
        i = args.index("--silent"); silent = float(args[i + 1]); del args[i:i + 2]
    stills = None
    if "--stills" in args:
        i = args.index("--stills"); stills = [float(x) for x in args[i + 1].split(",")]; del args[i:i + 2]
    data, narr = args[0], args[1] if len(args) > 1 else None
    music = args[2] if len(args) > 2 else None
    d = json.load(open(data, encoding="utf-8"))
    out = os.path.join(os.getcwd(), "canton-weekly", d["date"]); os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    if silent:
        narr = os.path.join(tmp, "silence.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", str(silent), narr], check=True)
    total = dur(narr) + 0.8
    tl = timeline(d["video_script"], total - 0.8)
    tl[-1]["end"] = total
    menu = capture_menu(tmp)
    page = os.path.join(tmp, "v.html"); open(page, "w", encoding="utf-8").write(build_html(d, tl, total, menu))
    if stills:
        sj = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:{W},height:{H}}}}});
await p.goto('file://{page}');await p.waitForTimeout(1500);for(const t of {json.dumps(stills)}){{await p.evaluate(t=>renderAt(t),t);await p.screenshot({{path:'{out}/still-'+t+'.png'}})}};await b.close()}})();"""
        sf = os.path.join(tmp, "s.js"); open(sf, "w").write(sj); subprocess.run(["node", sf], check=True)
        print(json.dumps({"stills": [os.path.join(out, f"still-{t}.png") for t in stills], "timeline": [[x["scene"], round(x["start"], 1), round(x["end"], 1)] for x in tl]}))
        return
    frames = os.path.join(tmp, "f"); os.makedirs(frames)
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:{W},height:{H}}}}});
await p.goto('file://{page}');await p.waitForTimeout(1200);const n={int(total*FPS)};
for(let i=0;i<n;i++){{await p.evaluate(t=>renderAt(t),i/{FPS});await p.screenshot({{path:'{frames}/'+String(i).padStart(5,'0')+'.jpg',type:'jpeg',quality:90}})}}
await p.evaluate(t=>renderAt(t),{tl[1]['start']+1.2});await p.screenshot({{path:'{out}/poster.jpg',type:'jpeg',quality:88}});await b.close()}})();"""
    jsf = os.path.join(tmp, "r.js"); open(jsf, "w").write(js)
    subprocess.run(["node", jsf], check=True)
    vid = os.path.join(tmp, "v.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{frames}/%05d.jpg", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", vid], check=True)
    final = os.path.join(out, "video.mp4")
    if music:
        st = max(0.0, total - 50)
        fc = (f"[1:a]atrim=0:{total-st},asetpts=PTS-STARTPTS,afade=t=in:d=2,afade=t=out:st={max(0,total-st-3)}:d=3,volume=0.55,adelay={int(st*1000)}|{int(st*1000)}[m];"
              f"[2:a]asplit=2[v1][v2];[m][v1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];[v2][md]amix=inputs=2:duration=first:normalize=0[a]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", music, "-i", narr, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
    else:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", narr, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
    secs = int(round(total))
    warn = []
    if not d.get("candles"):
        warn.append("no candles: run prepare.py first (the chart fell back to the old line chart)")
    if not any(x["scene"] == "bellver" for x in d["video_script"]):
        warn.append("no bellver scene: run prepare.py BEFORE the narration (the Bellver Card ad is missing)")
    for sc in ("burn", "halving", "tribe", "streams"):
        if not any(x["scene"] == sc for x in d["video_script"]):
            warn.append(f"no {sc} scene: run prepare.py BEFORE the narration (MTG's fixed {sc} scene is missing)")
    if menu["warn"]:
        warn.append(menu["warn"])
    print(json.dumps({"video": final, "poster": os.path.join(out, "poster.jpg"), "duration_iso": f"PT{secs//60}M{secs%60}S", "warnings": warn}))

if __name__ == "__main__":
    main()
