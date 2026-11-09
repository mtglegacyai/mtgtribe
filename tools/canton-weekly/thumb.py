#!/usr/bin/env python3
"""Canton Weekly video thumbnail (1920x1080 poster.jpg) for mtgtribe.com.

Usage (from the repo root, after video.py, before build.py):
    python3 tools/canton-weekly/thumb.py tools/canton-weekly/data/<DATE>.json

Writes canton-weekly/<date>/poster.jpg (the cover shown before the video plays) and canton-weekly/<date>/og.jpg, the
1200x630 social preview that WhatsApp, Facebook, X and Telegram show when the report link is shared (MTG, 9 Nov 2026:
every page gets its own preview). A week without a video: add --og-only to write only og.jpg.

Reads from the JSON: date_h, price_short, closes, chart_lines, and the optional "thumb" block:
    "thumb": {"hook": "Holding support after the SEC letter", "move": "-5%", "move_label": "this week"}
Without "thumb", the hook comes from "headline" and the move from the "7 days" snapshot row.

Canton logo rules (canton.network/brand-kit-trademark-use): the official white logo
(/assets/canton/canton-logo-white.svg, unchanged file) is shown as supplied: never recoloured, rotated,
skewed or stretched, kept apart from MTG's own branding, and the report page carries the trademark note.
No em or en dashes in any text.
"""
import html, json, os, re, subprocess, sys, tempfile

W, H = 1920, 1080
ROOT = os.getcwd()
LOGO = os.path.join(ROOT, "assets", "canton", "canton-logo-white.svg")
PHOTO = os.path.join(ROOT, "assets", "tribe", "mtg-photo-round-720.webp")


def esc(s):
    return html.escape(str(s), quote=True)


def move_from(d):
    t = d.get("thumb") or {}
    if t.get("move"):
        return t["move"], t.get("move_label", "this week")
    for label, val in d.get("snapshot", []):
        if label.lower().startswith("7 days"):
            m = re.search(r"([+-]?\d+(?:\.\d+)?)%", re.sub(r"<[^>]+>", "", val))
            if m:
                v = m.group(1)
                return (v if v.startswith(("+", "-")) else "+" + v) + "%", "this week"
    return "", ""


def hook_from(d):
    t = d.get("thumb") or {}
    h = t.get("hook") or d.get("headline", "")
    return h[:1].upper() + h[1:]


def chart(d, W=W, H=H, box=None):
    closes = [c[1] for c in d["closes"]]
    lines = d.get("chart_lines", [])
    vals = closes + [l["v"] for l in lines]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.18
    lo, hi = lo - pad, hi + pad
    x0, x1, y0, y1 = box or (60, W - 170, 600, 1000)
    def X(i): return x0 + (x1 - x0) * i / (len(closes) - 1)
    def Y(v): return y1 - (y1 - y0) * (v - lo) / (hi - lo)
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(closes))
    area = f"M{X(0):.1f},{y1} L" + " L".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(closes)) + f" L{X(len(closes)-1):.1f},{y1} Z"
    ls = ""
    for l in lines:
        c = "#3ddc84" if l["kind"] == "support" else "#ff8a7a"
        ls += f'<line x1="0" x2="{W}" y1="{Y(l["v"]):.1f}" y2="{Y(l["v"]):.1f}" stroke="{c}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="10 12"/>'
    lx, ly = X(len(closes) - 1), Y(closes[-1])
    return f'''<svg class="chart" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">
 <defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2ad3c" stop-opacity=".32"/><stop offset="1" stop-color="#f2ad3c" stop-opacity="0"/></linearGradient>
 <linearGradient id="gl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f2ad3c" stop-opacity=".15"/><stop offset=".55" stop-color="#f2ad3c" stop-opacity=".75"/><stop offset="1" stop-color="#ffd47c"/></linearGradient>
 <filter id="glow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="8"/></filter></defs>
 {ls}<path d="{area}" fill="url(#ga)"/>
 <polyline points="{pts}" fill="none" stroke="#f2ad3c" stroke-opacity=".55" stroke-width="10" filter="url(#glow)"/>
 <polyline points="{pts}" fill="none" stroke="url(#gl)" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
 <circle cx="{lx:.1f}" cy="{ly:.1f}" r="22" fill="#f2ad3c" fill-opacity=".25"/><circle cx="{lx:.1f}" cy="{ly:.1f}" r="10" fill="#ffe2aa"/></svg>'''


def page(d):
    move, move_label = move_from(d)
    down = move.startswith("-")
    arrow = "▼" if down else "▲"
    mv = move.lstrip("+-")
    hook = hook_from(d)
    date_short = re.sub(r"(\d+) (\w{3})\w* (\d{4})", lambda m: f"{m.group(1)} {m.group(2).upper()} {m.group(3)}", d["date_h"])
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700;800&family=Outfit:wght@700;800;900&family=JetBrains+Mono:wght@700&display=swap');
*{{box-sizing:border-box}}html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#040506;color:#fff;font-family:'DM Sans',system-ui,sans-serif}}
.bg{{position:absolute;inset:0;background:
 radial-gradient(900px 620px at 8% -6%,rgba(242,173,60,.30),transparent 62%),
 radial-gradient(760px 560px at 92% 88%,rgba(242,173,60,.20),transparent 64%),
 linear-gradient(180deg,#0a0b0d 0%,#050607 100%)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:80px 80px;-webkit-mask-image:linear-gradient(180deg,#000 20%,transparent 92%)}}
.chart{{position:absolute;inset:0;width:100%;height:100%}}
.vig{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(4,5,6,.92) 0%,rgba(4,5,6,.55) 52%,rgba(4,5,6,0) 78%)}}
.frame{{position:absolute;inset:22px;border-radius:30px;border:2px solid rgba(242,173,60,.38);box-shadow:inset 0 0 120px rgba(242,173,60,.07)}}
.logo{{position:absolute;top:84px;left:96px;height:78px;width:auto}}
.pill{{position:absolute;top:92px;right:96px;display:flex;align-items:center;gap:14px;padding:16px 28px;border-radius:999px;border:2px solid rgba(242,173,60,.7);background:rgba(10,8,4,.72);color:#ffe2aa;font:800 26px/1 'DM Sans';letter-spacing:.14em}}
.pill i{{width:14px;height:14px;border-radius:50%;background:#f2ad3c;box-shadow:0 0 16px #f2ad3c}}
.main{{position:absolute;left:96px;top:250px;width:1200px}}
.k{{margin:0 0 6px;color:#e8b862;font:800 34px/1 'DM Sans';letter-spacing:.22em}}
.price-row{{display:flex;align-items:flex-end;gap:34px}}
.price{{margin:0;font:900 250px/.92 'Outfit';letter-spacing:-.045em;background:linear-gradient(180deg,#fff6dd 0%,#ffd47c 38%,#f2ad3c 70%,#c27a14 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 18px 50px rgba(242,173,60,.35))}}
.move{{flex:none;margin-bottom:40px;display:inline-flex;flex-direction:column;align-items:flex-start;gap:10px;padding:18px 26px;border-radius:20px;font:900 58px/1 'Outfit';letter-spacing:-.01em;white-space:nowrap}}
.move.dn{{color:#ffb4a2;background:rgba(255,110,90,.14);border:2px solid rgba(255,138,122,.55)}}
.move.up{{color:#9ff5c6;background:rgba(61,220,132,.13);border:2px solid rgba(61,220,132,.5)}}
.move small{{font:800 21px/1 'DM Sans';letter-spacing:.16em;opacity:.9}}
.hook{{margin:34px 0 0;max-width:1080px;font:900 82px/1.02 'Outfit';letter-spacing:-.02em;text-transform:uppercase;color:#fff;text-shadow:0 6px 30px rgba(0,0,0,.6)}}
.hook b{{color:#ffd47c}}
.mtg{{position:absolute;right:120px;top:300px;display:flex;flex-direction:column;align-items:center;gap:22px}}
.ring{{width:400px;height:400px;border-radius:50%;padding:10px;background:conic-gradient(from 210deg,#7a4a0c,#ffe2aa,#f2ad3c,#c27a14,#ffe2aa,#7a4a0c);box-shadow:0 0 0 6px rgba(4,5,6,.9),0 0 80px rgba(242,173,60,.45),0 30px 80px rgba(0,0,0,.7)}}
.ring img{{display:block;width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:50% 30%}}
.who{{padding:14px 26px;border-radius:16px;background:rgba(6,6,7,.82);border:2px solid rgba(242,173,60,.45);font:800 30px/1 'Outfit';letter-spacing:.02em;white-space:nowrap}}
.who span{{color:#e8b862}}
</style></head><body>
<div class="bg"></div><div class="grid"></div>{chart(d)}<div class="vig"></div><div class="frame"></div>
<img class="logo" src="file://{LOGO}" alt="">
<div class="pill"><i></i>WEEKLY MARKET REPORT · {esc(date_short)}</div>
<div class="main">
 <p class="k">CANTON COIN (CC)</p>
 <div class="price-row"><p class="price">{esc(d["price_short"])}</p>{f'<span class="move {"dn" if down else "up"}"><span>{arrow} {esc(mv)}</span><small>{esc(move_label.upper())}</small></span>' if move else ''}</div>
 <p class="hook">{esc(hook)}</p>
</div>
<div class="mtg"><div class="ring"><img src="file://{PHOTO}" alt=""></div><div class="who">MTG 👑 <span>| Your Digital Architect</span></div></div>
</body></html>'''


def og_page(d):
    """Social preview for the report page (og:image, 1200x630, MTG 9 Nov 2026): the week's price, move and hook."""
    OW, OH = 1200, 630
    move, move_label = move_from(d)
    down = move.startswith("-")
    mv = move.lstrip("+-")
    hook = hook_from(d)
    date_short = re.sub(r"(\d+) (\w{3})\w* (\d{4})", lambda m: f"{m.group(1)} {m.group(2).upper()} {m.group(3)}", d["date_h"])
    mvh = f'<span class="move {"dn" if down else "up"}">{"▼" if down else "▲"} {esc(mv)}<small>{esc(move_label.upper())}</small></span>' if move else ""
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700;800&family=Outfit:wght@700;800;900&display=block');
*{{box-sizing:border-box;margin:0;padding:0}}html,body{{width:{OW}px;height:{OH}px;overflow:hidden;background:#040506;color:#fff;font-family:'DM Sans',sans-serif}}
.bg{{position:absolute;inset:0;background:radial-gradient(700px 480px at 6% -8%,rgba(242,173,60,.30),transparent 62%),radial-gradient(600px 440px at 94% 92%,rgba(242,173,60,.20),transparent 64%),linear-gradient(180deg,#0a0b0d,#050607)}}
.chart{{position:absolute;inset:0;width:100%;height:100%}}
.vig{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(4,5,6,.94) 0%,rgba(4,5,6,.6) 50%,rgba(4,5,6,.05) 80%)}}
.frame{{position:absolute;inset:14px;border-radius:30px;box-shadow:inset 0 0 0 2px rgba(242,173,60,.4)}}
.logo{{position:absolute;left:56px;top:48px;height:44px;width:auto}}
.pill{{position:absolute;top:50px;right:56px;display:flex;align-items:center;gap:10px;height:42px;padding:0 20px;border-radius:999px;border:2px solid rgba(242,173,60,.7);background:rgba(10,8,4,.75);color:#ffe2aa;font:800 17px/1 'DM Sans';letter-spacing:.14em}}
.pill i{{width:10px;height:10px;border-radius:50%;background:#f2ad3c;box-shadow:0 0 12px #f2ad3c}}
.k{{position:absolute;left:56px;top:128px;color:#e8b862;font:800 22px/1 'DM Sans';letter-spacing:.2em}}
.row{{position:absolute;left:52px;top:160px;display:flex;align-items:flex-end;gap:22px}}
.price{{font:900 150px/.92 'Outfit';letter-spacing:-.045em;background:linear-gradient(180deg,#fff6dd,#ffd47c 38%,#f2ad3c 70%,#c27a14);-webkit-background-clip:text;background-clip:text;color:transparent}}
.move{{margin-bottom:16px;display:inline-flex;flex-direction:column;gap:6px;padding:12px 18px;border-radius:16px;font:900 38px/1 'Outfit';white-space:nowrap}}
.move small{{font:800 14px/1 'DM Sans';letter-spacing:.16em}}
.move.dn{{color:#ffb4a2;background:rgba(255,110,90,.14);border:2px solid rgba(255,138,122,.55)}}
.move.up{{color:#9ff5c6;background:rgba(61,220,132,.13);border:2px solid rgba(61,220,132,.5)}}
.hook{{position:absolute;left:56px;top:330px;width:700px;font:900 48px/1.04 'Outfit';letter-spacing:-.015em;text-transform:uppercase;text-shadow:0 6px 24px rgba(0,0,0,.6)}}
.url{{position:absolute;left:56px;bottom:50px;display:inline-flex;align-items:center;gap:12px;height:56px;padding:0 24px 0 10px;border-radius:999px;background:linear-gradient(180deg,#ffe2aa,#f2ad3c);color:#1a1205;font:800 22px/1 'DM Sans';white-space:nowrap;box-shadow:0 10px 30px rgba(242,173,60,.28)}}
.url i{{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:#1a1205;color:#ffe2aa;font:900 16px/1 'DM Sans';font-style:normal}}
.mtg{{position:absolute;right:70px;top:150px;display:flex;flex-direction:column;align-items:center;gap:14px}}
.ring{{width:250px;height:250px;border-radius:50%;padding:8px;background:conic-gradient(from 210deg,#7a4a0c,#ffe2aa,#f2ad3c,#c27a14,#ffe2aa,#7a4a0c);box-shadow:0 0 0 5px rgba(4,5,6,.9),0 0 60px rgba(242,173,60,.45),0 24px 60px rgba(0,0,0,.7)}}
.ring img{{display:block;width:100%;height:100%;border-radius:50%;object-fit:cover}}
.who{{padding:10px 18px;border-radius:12px;background:rgba(6,6,7,.85);border:2px solid rgba(242,173,60,.45);font:800 19px/1 'Outfit';white-space:nowrap}}
.who span{{color:#e8b862}}
</style></head><body>
<div class="bg"></div>{chart(d, OW, OH, (40, OW - 60, 400, 600))}<div class="vig"></div><div class="frame"></div>
<img class="logo" src="file://{LOGO}" alt="">
<div class="pill"><i></i>WEEKLY REPORT · {esc(date_short)}</div>
<p class="k">CANTON COIN (CC)</p>
<div class="row"><p class="price">{esc(d["price_short"])}</p>{mvh}</div>
<p class="hook">{esc(hook)}</p>
<div class="url"><i>▶</i>mtgtribe.com/canton-weekly/{esc(d["date"])}</div>
<div class="mtg"><div class="ring"><img src="file://{PHOTO}" alt=""></div><div class="who">MTG 👑 <span>| Your Digital Architect</span></div></div>
</body></html>'''


def shoot(h, w, hh, out):
    """Render one HTML page with Playwright and save it as a JPEG."""
    assert "\u2014" not in h and "\u2013" not in h, "dash in image text"
    tmp = tempfile.mkdtemp()
    f = os.path.join(tmp, "t.html")
    open(f, "w", encoding="utf-8").write(h)
    png = os.path.join(tmp, "t.png")
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:{w},height:{hh}}}}});
await p.goto('file://{f}');await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
await p.screenshot({{path:'{png}'}});await b.close()}})();"""
    jsf = os.path.join(tmp, "r.js")
    open(jsf, "w").write(js)
    subprocess.run(["node", jsf], check=True)
    q = "2" if w > 1500 else "4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", png, "-q:v", q, out], check=True)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    og_only = "--og-only" in sys.argv
    d = json.load(open(args[0], encoding="utf-8"))
    out = os.path.join(ROOT, "canton-weekly", d["date"])
    os.makedirs(out, exist_ok=True)
    res = {}
    if not og_only:
        res["poster"] = shoot(page(d), W, H, os.path.join(out, "poster.jpg"))
    res["og"] = shoot(og_page(d), 1200, 630, os.path.join(out, "og.jpg"))
    print(json.dumps(res))


if __name__ == "__main__":
    main()
