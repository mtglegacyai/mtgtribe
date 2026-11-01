#!/usr/bin/env python3
"""Canton Weekly technical analysis video (16:9, 1920x1080) for mtgtribe.com.

Usage (from the repo root):
  python3 tools/canton-weekly/video.py DATA.json NARRATION.mp3 [MUSIC.mp3] [--silent SECONDS]

DATA.json needs "video_script": a list of {"scene": name, "text": narration, "caption": optional on-screen wording (write numbers as $0.1046, CNTN, mtgtribe.com)}.
Scenes: intro, price, trend, levels, scenarios, fundamentals, guides, outro.
Segment timing: each segment's share of the narration is proportional to its
length in characters (the narration is generated from the same segments, joined
with short pauses), so visuals change when the matching sentence starts.
Music: the closing track starts at (duration - 50s), fades in, is ducked under the
voice and fades out with the video. Output: canton-weekly/<date>/video.mp4 + poster.jpg
"""
import json, os, re, subprocess, sys, tempfile

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
.sc{position:absolute;inset:150px 120px 210px;display:none;flex-direction:column;justify-content:center}
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
</style></head><body><div id="st">
<div class="brand"><i>👑</i>MTG TRIBE</div><div class="tag">Canton Weekly · __DATE__</div>
<div class="sc" id="s-intro"><div class="k">Weekly market report</div><h1>Canton Coin<br><span class="g">__DATE__</span></h1></div>
<div class="sc" id="s-price"><div class="k">Price snapshot</div><div class="big g" id="px">$0.0000</div>
 <div class="row">__TILES__</div></div>
<div class="sc" id="s-trend"><div class="k">The trend</div><h2>__TREND_H__</h2><div id="chartwrap"></div></div>
<div class="sc" id="s-levels"><div class="k">Key levels</div><h2>Where to watch</h2><div id="chartwrap2"></div></div>
<div class="sc" id="s-scenarios"><div class="k">Three scenarios this week</div>__SCEN__</div>
<div class="sc" id="s-fundamentals"><div class="k">Fundamentals: __SCORE__</div>__FUND__</div>
<div class="sc" id="s-guides"><div class="k">Learn step by step</div><h2>How to buy <span class="g">Canton Coin</span><br>and <span class="g">CNTN stock</span></h2><div style="font:700 72px 'JetBrains Mono',monospace;color:#ffe2aa">mtgtribe.com/cc<br>mtgtribe.com/cntn</div></div>
<div class="sc" id="s-outro" style="align-items:center;text-align:center"><div class="k">Not financial advice · Do your own research</div><h1 class="g" style="font-size:110px">Let's Get This Crypto! 💪</h1><div style="margin-top:30px;font:800 40px 'DM Sans','Inter'">MTG 👑 | Your Digital Architect</div><div class="cta">Join the MTG TRIBE · mtgtribe.com/group</div></div>
<div id="cap"></div><div id="prog"></div></div>
<script>
const TL=__TL__, TOTAL=__TOTAL__, CL=__CLOSES__, LINES=__LINES__, PRICE=__PRICE__;
function chart(el,showLines,p){const W=1640,H=520,L=110,R=30,T=20,B=50;const v=CL.map(c=>c[1]);const all=v.concat(LINES.map(l=>l.v));const lo=Math.min(...all)*.97,hi=Math.max(...all)*1.02;
 const xs=i=>L+i*(W-L-R)/(v.length-1),ys=x=>T+(hi-x)*(H-T-B)/(hi-lo);let s=`<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`;
 for(let g=Math.ceil(lo*100)/100;g<hi;g+=.01){s+=`<line x1="${L}" x2="${W-R}" y1="${ys(g)}" y2="${ys(g)}" stroke="rgba(255,255,255,.08)"/><text x="${L-14}" y="${ys(g)+8}" text-anchor="end" fill="#8a919b" font-size="24">$${g.toFixed(2)}</text>`}
 const n=Math.max(2,Math.round(v.length*Math.min(1,showLines?1:p*1.4)));const pts=v.slice(0,n).map((x,i)=>xs(i)+','+ys(x)).join(' ');
 if(showLines)LINES.forEach((l,i)=>{const a=Math.min(1,Math.max(0,p*LINES.length*1.3-i));const c=l.kind=='support'?'#3ddc84':'#ff7b6b';s+=`<g opacity="${a}"><line x1="${L}" x2="${W-R}" y1="${ys(l.v)}" y2="${ys(l.v)}" stroke="${c}" stroke-width="4" stroke-dasharray="14 10"/><rect x="${W-R-250}" y="${ys(l.v)-44}" width="250" height="38" rx="10" fill="#0b0d10" stroke="${c}"/><text x="${W-R-125}" y="${ys(l.v)-16}" text-anchor="middle" fill="${c}" font-size="24" font-weight="700">${l.kind=='support'?'Support':'Resistance'} $${l.v}</text></g>`});
 s+=`<polyline points="${pts}" fill="none" stroke="#f2ad3c" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>`;
 const lx=xs(n-1),ly=ys(v[n-1]);s+=`<circle cx="${lx}" cy="${ly}" r="${18+4*Math.sin(p*20)}" fill="#f2ad3c" opacity=".25"/><circle cx="${lx}" cy="${ly}" r="10" fill="#ffe2aa"/>`;
 s+=`<text x="${L}" y="${H-8}" fill="#8a919b" font-size="24">${CL[0][0]}</text><text x="${W-R}" y="${H-8}" text-anchor="end" fill="#8a919b" font-size="24">${CL[CL.length-1][0]}</text></svg>`;el.innerHTML=s}
function ease(x){return 1-Math.pow(1-Math.min(1,Math.max(0,x)),3)}
window.renderAt=function(t){let seg=TL.find(s=>t>=s.start&&t<s.end)||TL[TL.length-1];const p=(t-seg.start)/(seg.end-seg.start);
 document.querySelectorAll('.sc').forEach(e=>{const on=e.id=='s-'+seg.scene;e.style.display=on?'flex':'none';if(on){const a=ease(p*6);e.style.opacity=Math.min(a,ease((seg.end-t)*3));e.style.transform=`translateY(${(1-a)*40}px)`}});
 if(seg.scene=='price'){document.getElementById('px').textContent='$'+(PRICE*ease(p*2.5)).toFixed(4)}
 if(seg.scene=='trend')chart(document.getElementById('chartwrap'),false,p);
 if(seg.scene=='levels')chart(document.getElementById('chartwrap2'),true,p);
 document.querySelectorAll('.card').forEach((c,i)=>{const a=ease(p*4-i*.6);c.style.opacity=a;c.style.transform=`translateX(${(1-a)*80}px)`});
 const words=seg.text.split(/(?<=[.!?:])\s+/);let acc=0,tot=seg.text.length,cur=words[0];for(const w of words){if(p<=(acc+w.length)/tot){cur=w;break}acc+=w.length}document.getElementById('cap').textContent=cur;
 document.getElementById('prog').style.width=(t/TOTAL*100)+'%'};
</script></body></html>"""

def build_html(d, tl, total):
    s = d["video_vis"]
    tiles = "".join(f'<div class="tile"><span>{a}</span><b class="{c}">{b}</b></div>' for a, b, c in s["tiles"])
    scen = "".join(f'<div class="card"><b>{a}</b><span>{b}</span><em>{c}</em></div>' for a, b, c in s["scenarios"])
    fund = "".join(f'<div class="card" style="font-size:38px">{x}</div>' for x in s["fundamentals"])
    h = HTML
    for k, v in {"__DATE__": d["date_h"], "__TILES__": tiles, "__TREND_H__": s["trend_h"], "__SCEN__": scen, "__FUND__": fund, "__SCORE__": d["fund_score"],
                 "__TL__": json.dumps(tl), "__TOTAL__": str(total), "__CLOSES__": json.dumps(d["closes"]), "__LINES__": json.dumps(d["chart_lines"]), "__PRICE__": str(s["price"])}.items():
        h = h.replace(k, v)
    return h

def main():
    args = [a for a in sys.argv[1:]]
    silent = None
    if "--silent" in args:
        i = args.index("--silent"); silent = float(args[i + 1]); del args[i:i + 2]
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
    print(json.dumps({"video": final, "poster": os.path.join(out, "poster.jpg"), "duration_iso": f"PT{secs//60}M{secs%60}S"}))

if __name__ == "__main__":
    main()
