#!/usr/bin/env python3
"""Canton Weekly technical analysis video (16:9, 1920x1080) for mtgtribe.com.

Usage (from the repo root):
  python3 tools/canton-weekly/video.py DATA.json NARRATION.mp3 [MUSIC.mp3] [--silent SECONDS]

DATA.json needs "video_script": a list of {"scene": name, "text": narration, "caption": optional on-screen wording (write numbers as $0.1046, CNTN, mtgtribe.com)}.
Scenes: intro, price, trend, levels, scenarios, fundamentals, guides, bellver, outro.
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
<div class="sc" id="s-outro" style="align-items:center;text-align:center"><div class="k">Not financial advice · Do your own research</div><h1 class="g" style="font-size:110px">Let's Get This Crypto! 💪</h1><div style="margin-top:30px;font:800 40px 'DM Sans','Inter'">MTG 👑 | Your Digital Architect</div><div class="cta">Join the MTG TRIBE · mtgtribe.com/group</div></div>
<div id="cap"></div><div id="prog"></div></div>
<script>
const TL=__TL__, TOTAL=__TOTAL__, CL=__CLOSES__, LINES=__LINES__, PRICE=__PRICE__, CDL=__CANDLES__, BV=__BVCUES__;
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
function ease(x){return 1-Math.pow(1-Math.min(1,Math.max(0,x)),3)}
window.renderAt=function(t){let seg=TL.find(s=>t>=s.start&&t<s.end)||TL[TL.length-1];const p=(t-seg.start)/(seg.end-seg.start);
 document.querySelectorAll('.sc').forEach(e=>{const on=e.id=='s-'+seg.scene;e.style.display=on?'flex':'none';if(on){const a=ease(p*6);e.style.opacity=Math.min(a,ease((seg.end-t)*3));e.style.transform=`translateY(${(1-a)*40}px)`}});
 if(seg.scene=='price'){document.getElementById('px').textContent='$'+(PRICE*ease(p*2.5)).toFixed(4)}
 if(seg.scene=='trend'){if(CDL)candle(document.getElementById('chartwrap'),false,p,document.getElementById('pan1'));else chart(document.getElementById('chartwrap'),false,p)}
 if(seg.scene=='levels'){if(CDL)candle(document.getElementById('chartwrap2'),true,p,document.getElementById('pan2'));else chart(document.getElementById('chartwrap2'),true,p)}
 if(seg.scene=='bellver')bellver(p);
 document.querySelectorAll('.card').forEach((c,i)=>{const a=ease(p*4-i*.6);c.style.opacity=a;c.style.transform=`translateX(${(1-a)*80}px)`});
 const words=seg.text.split(/(?<=[.!?:])\s+/);let acc=0,tot=seg.text.length,cur=words[0];for(const w of words){if(p<=(acc+w.length)/tot){cur=w;break}acc+=w.length}document.getElementById('cap').textContent=cur;
 document.getElementById('prog').style.width=(t/TOTAL*100)+'%'};
</script></body></html>"""

def build_html(d, tl, total):
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
    bv = next((x for x in d["video_script"] if x["scene"] == "bellver"), None)
    cues = {}
    if bv:
        cap = bv.get("caption") or bv["text"]
        for k, ph in {"card": "Get the Bellver", "spend": "Fund it", "earn": "Then share", "team": "monthly rewards", "order": "Order yours"}.items():
            i = cap.find(ph)
            cues[k] = round(i / len(cap), 4) if i >= 0 else 0
    h = HTML
    for k, v in {"__DATE__": d["date_h"], "__TILES__": tiles, "__TREND_H__": s["trend_h"], "__SCEN__": scen, "__FUND__": fund, "__SCORE__": d["fund_score"],
                 "__TL__": json.dumps(tl), "__TOTAL__": str(total), "__CLOSES__": json.dumps(d["closes"]), "__LINES__": json.dumps(d["chart_lines"]), "__PRICE__": str(s["price"]), "__CANDLES__": json.dumps(cd) if cd else "null", "__LEGEND__": legend,
                 "__BVCUES__": json.dumps(cues), "__CARD__": CARD}.items():
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
    page = os.path.join(tmp, "v.html"); open(page, "w", encoding="utf-8").write(build_html(d, tl, total))
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
    print(json.dumps({"video": final, "poster": os.path.join(out, "poster.jpg"), "duration_iso": f"PT{secs//60}M{secs%60}S", "warnings": warn}))

if __name__ == "__main__":
    main()
