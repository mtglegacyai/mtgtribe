#!/usr/bin/env python3
"""Canton Weekly report builder for mtgtribe.com.

Usage (from the repo root):
    python3 tools/canton-weekly/build.py tools/canton-weekly/data/2026-11-01.json

Reads the master page design from cntn/index.html (CSS, icons,
header, footer, back-to-top), writes:
    canton-weekly/<date>/index.html    the report
    canton-weekly/index.html           the hub (latest report + archive)
and adds both URLs to sitemap-home.xml, with today's date as <lastmod> on every page this run changed
(the reports, the hub, /cc/ and /cntn/), so Google knows what to crawl again.
"""
import glob, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from official_links import link_html  # links every named company or tool to its verified official site

ROOT = os.getcwd()
SITE = "https://mtgtribe.com"
MASTER = os.path.join(ROOT, "cntn", "index.html")
DATA_DIR = os.path.join(ROOT, "tools", "canton-weekly", "data")
CC_GUIDE = "/cc/"
CNTN_GUIDE = "/cntn/"
VALR = "https://www.valr.com/invite/VAKM6VZY"

# Live CC price card: same script, data-symbol picks Kraken's CC/USD market (the same card as on /cc/)
CC_CARD = '<div class="cl" data-cntn-live data-symbol="KRAKEN:CCUSD" data-nolink><div class="cl-head"><span class="cl-t">CC live price<small>Canton Coin, CC/USD on Kraken</small></span><span class="cl-live"><i aria-hidden="true"></i>Live chart</span></div><div class="cl-body"></div><p class="cl-fb"><span class="cl-msg">Loading the live price.</span> You can also see <a href="https://www.coingecko.com/en/coins/canton-network" target="_blank" rel="noopener">Canton Coin on CoinGecko</a>.</p><p class="cl-foot">Price and chart by <a href="https://www.tradingview.com/symbols/CCUSD/?exchange=KRAKEN" target="_blank" rel="noopener nofollow">TradingView</a> (Kraken CC/USD market). Education only, not financial advice.</p></div>'

# Live CNTN price card (filled in the browser by /assets/tribe/cntn-live.js, loaded from the master page head)
CNTN_CARD = '<div class="cl" data-cntn-live><div class="cl-head"><span class="cl-t">CNTN live price<small>Canton Strategic Holdings, Nasdaq</small></span><span class="cl-live"><i aria-hidden="true"></i>Live chart</span></div><div class="cl-body"></div><p class="cl-fb"><span class="cl-msg">Loading the live price.</span> You can also see <a href="https://www.nasdaq.com/market-activity/stocks/cntn" target="_blank" rel="noopener">CNTN on Nasdaq.com</a>.</p><p class="cl-foot">Price and chart by <a href="https://www.tradingview.com/symbols/NASDAQ-CNTN/" target="_blank" rel="noopener nofollow">TradingView</a>, may be delayed by up to 15 minutes. Education only, not financial advice.</p></div>'

EXTRA_CSS = """
.cta{text-transform:uppercase;letter-spacing:.04em}
.learn{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:0 0 56px}
@media (max-width:640px){.learn{grid-template-columns:minmax(0,1fr)}}
.learn a{display:flex;flex-direction:column;gap:6px;padding:20px;border-radius:18px;border:1px solid rgba(242,173,60,.32);background:radial-gradient(420px circle at 0 0,rgba(242,173,60,.1),transparent 60%),rgba(255,255,255,.02);transition:border-color .2s,transform .2s}
.learn a:hover{border-color:rgba(242,173,60,.7);transform:translateY(-2px)}
.learn .k{color:var(--gold-t);font:800 11.5px/1.3 var(--f-b);letter-spacing:.14em;text-transform:uppercase}
.learn b{color:#fff;font:800 1.2rem/1.25 var(--f-d)}
.learn span.d{color:var(--body);font-size:15px}
.learn .go{display:inline-flex;align-items:center;gap:8px;margin-top:6px;color:var(--gold-t);font:800 13.5px/1 var(--f-b);letter-spacing:.05em;text-transform:uppercase}
.chartbox{margin:18px 0 8px;padding:16px 16px 8px;border-radius:18px;border:1px solid var(--line);background:rgba(255,255,255,.02)}
.chartbox svg{display:block;width:100%;height:auto}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin:0 0 6px;font-size:13px;color:var(--muted)}
.legend i{display:inline-block;width:14px;height:2px;margin-right:6px;vertical-align:middle;border-radius:2px}
.score{display:inline-flex;align-items:center;gap:8px;margin:0 0 14px;padding:8px 14px;border-radius:999px;border:1px solid rgba(242,173,60,.4);background:rgba(242,173,60,.08);color:var(--amber-l);font:800 13px/1 var(--f-b);letter-spacing:.08em;text-transform:uppercase}
.up{color:#3ddc84}.dn{color:#ff8a7a}
.vreal{position:relative;border-radius:24px;overflow:hidden;border:1px solid rgba(242,173,60,.45);background:#000;box-shadow:0 30px 80px rgba(0,0,0,.6),0 0 60px rgba(242,173,60,.12)}
.vreal video{display:block;width:100%;height:auto;aspect-ratio:16/9;background:#000}
.vcover{position:absolute;inset:0;display:grid;place-items:end start;padding:0 0 6.5% 5%;border:0;cursor:pointer;background:none;color:#1b1102}
.vcover[hidden]{display:none}
.vcover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.vcover:after{content:"";position:absolute;left:0;right:0;bottom:0;height:34%;background:linear-gradient(180deg,transparent,rgba(0,0,0,.35))}
.vgo{position:relative;z-index:1;display:flex;align-items:center;gap:clamp(10px,1.6vw,18px)}
.vgo-btn{position:relative;display:grid;place-items:center;width:clamp(38px,7.2vw,92px);height:clamp(38px,7.2vw,92px);flex:none;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff3d0 0%,#ffd47c 30%,#f2ad3c 62%,#c27a14 100%);box-shadow:0 0 0 6px rgba(242,173,60,.25),0 18px 50px rgba(0,0,0,.6),0 0 60px rgba(242,173,60,.55),inset 0 -6px 14px rgba(120,70,8,.45),inset 0 4px 10px rgba(255,255,255,.55);transition:transform .25s cubic-bezier(.16,1,.3,1)}
.vgo-btn svg{width:40%;height:40%;margin-left:8%;filter:drop-shadow(0 2px 2px rgba(255,255,255,.4))}
.vgo-btn:before{content:"";position:absolute;inset:-9px;border-radius:50%;border:2px solid rgba(255,212,124,.6)}
.vgo-lab{display:inline-flex;align-items:center;gap:10px;padding:9px 16px;border-radius:999px;background:rgba(6,6,7,.78);border:1px solid rgba(242,173,60,.55);color:#ffe2aa;font:800 13px/1 var(--f-b);letter-spacing:.14em;text-transform:uppercase;box-shadow:0 10px 30px rgba(0,0,0,.5)}
.vgo-lab b{color:#fff;font-weight:800}
.vcover:hover .vgo-btn,.vcover:focus-visible .vgo-btn{transform:scale(1.08)}
.vcover:focus-visible{outline:3px solid #f2ad3c;outline-offset:-3px}
@media (prefers-reduced-motion:no-preference){.vgo-btn:before{animation:vring 2.2s ease-out infinite}}
@keyframes vring{0%{transform:scale(.9);opacity:.9}100%{transform:scale(1.35);opacity:0}}
.vgo-short{display:none}
@media (max-width:560px){.vgo-lab{font-size:10px;padding:6px 10px;letter-spacing:.1em}.vgo-long{display:none}.vgo-short{display:inline}.vcover{padding:0 0 4.5% 4.5%}.vgo-btn:before{inset:-6px}}
.arch{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.arch a{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:16px 18px;border-radius:14px;border:1px solid var(--line);background:rgba(255,255,255,.025);font-weight:700}
.arch a:hover{border-color:rgba(242,173,60,.5)}
.arch small{color:var(--muted);font:600 13px/1.3 var(--f-m)}
"""

def esc(s):
    return html.escape(str(s), quote=True)

def master_parts():
    src = open(MASTER, encoding="utf-8").read()
    head = src[: src.index("<body")]
    body = src[src.index("<body") :]
    sprite = re.search(r'<svg width="0".*?</svg>', body, re.S).group(0)
    header = re.search(r'<a class="skip".*?</header>', body, re.S).group(0)
    footer = body[body.index('<footer class="foot">') :]
    head = head.replace("</style>", EXTRA_CSS + "</style>", 1)
    return head, sprite, header, footer

def set_head(head, url, title, desc, og_title, og_desc, og_img, og_alt, ld, published):
    h = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", head, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', h, count=1)
    h = re.sub(r'<meta name="keywords" content="[^"]*">', '<meta name="keywords" content="Canton Coin price, Canton Coin analysis, CC price prediction, Canton Network news, CNTN stock, Canton Coin South Africa">', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h, count=1)
    for prop, val in (("og:title", og_title), ("og:description", og_desc), ("og:url", url), ("og:image", og_img), ("og:image:secure_url", og_img), ("og:image:alt", og_alt)):
        h = re.sub(rf'(<meta property="{re.escape(prop)}" content=")[^"]*', lambda m: m.group(1) + esc(val), h, count=1)
    for name, val in (("twitter:title", og_title), ("twitter:description", og_desc), ("twitter:image", og_img)):
        h = re.sub(rf'(<meta name="{re.escape(name)}" content=")[^"]*', lambda m: m.group(1) + esc(val), h, count=1)
    h = re.sub(r'(<meta property="article:(?:published|modified)_time" content=")[^"]*', lambda m: m.group(1) + published + "T06:00:00+02:00", h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", h, count=1, flags=re.S)
    return h

def table(cols, rows):
    th = "".join(f'<th scope="col">{c}</th>' for c in cols)
    tr = "".join("<tr>" + "".join(f'<td data-label="{cols[i]}">{v}</td>' for i, v in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

INVESTORS_URL = "https://crypto-fundraising.info/projects/canton-network/"
INVESTORS_CARD = '<a class="rel-guide" style="margin:0 0 12px" href="https://crypto-fundraising.info/projects/canton-network/" target="_blank" rel="noopener" aria-label="See who has invested in Canton Network on Crypto-Fundraising (opens in a new tab)"><span><span class="k">Do your own research</span><b>Who has invested in Canton Network?</b><span class="upd">See every funding round behind Digital Asset, the company that built Canton Network. Lead investors include a16z crypto, Goldman Sachs, Blackstone, DRW and Tradeweb.</span></span><span class="go">See the investors<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-arrow-right"/></svg></span></a><p class="upd">These firms invested in Digital Asset, the company. Buying CC or CNTN does not make you a Digital Asset shareholder, and big backers do not guarantee any price.</p>'
INVESTORS_SRC = '<li><a class="tx" href="https://crypto-fundraising.info/projects/canton-network/" target="_blank" rel="noopener">Crypto-Fundraising: Canton Network (Digital Asset) funding rounds and investors</a></li>'

def tip(t, icon="bulb"):
    return f'<div class="tip"><svg class="ic" aria-hidden="true"><use href="#i-{icon}"/></svg><span>{t}</span></div>'

def learn_cards():
    arrow = '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-arrow-right"/></svg>'
    return f'''<nav class="learn" aria-label="Learn how to buy">
  <a href="{CC_GUIDE}"><span class="k">Step-by-step guide</span><b>How to buy Canton Coin (CC)</b><span class="d">Buy USDT on Binance or VALR, buy CC, then keep it in your own Canton wallet. mtgtribe.com/cc</span><span class="go">Learn how to buy CC{arrow}</span></a>
  <a href="{CNTN_GUIDE}"><span class="k">Step-by-step guide</span><b>How to buy CNTN stock</b><span class="d">The Nasdaq company that holds Canton Coin, from almost anywhere. mtgtribe.com/cntn</span><span class="go">Learn how to buy CNTN{arrow}</span></a>
 </nav>'''

def chart_svg(d):
    closes = d["closes"]; vals = [c[1] for c in closes]
    lines = d["chart_lines"]
    lo = min(vals + [l["v"] for l in lines]) * 0.97; hi = max(vals + [l["v"] for l in lines]) * 1.02
    W, H, L, R, T, B = 640, 250, 52, 14, 14, 28
    xs = lambda i: L + i * (W - L - R) / (len(vals) - 1)
    ys = lambda v: T + (hi - v) * (H - T - B) / (hi - lo)
    step = 0.01 if hi - lo > 0.025 else 0.005
    g = ""; v = (int(lo / step) + 1) * step
    while v < hi:
        g += f'<line x1="{L}" x2="{W-R}" y1="{ys(v):.1f}" y2="{ys(v):.1f}" stroke="rgba(255,255,255,.07)"/><text x="{L-8}" y="{ys(v)+4:.1f}" text-anchor="end" fill="#8a919b" font-size="11" font-family="JetBrains Mono,monospace">${v:.3f}</text>'
        v += step
    ln = "".join(f'<line x1="{L}" x2="{W-R}" y1="{ys(l["v"]):.1f}" y2="{ys(l["v"]):.1f}" stroke="{"#3ddc84" if l["kind"]=="support" else "#ff7b6b"}" stroke-dasharray="5 5" stroke-opacity=".8"/>' for l in lines)
    pts = " ".join(f"{xs(i):.1f},{ys(v):.1f}" for i, v in enumerate(vals))
    area = f"M{xs(0):.1f},{H-B} L" + " L".join(f"{xs(i):.1f},{ys(v):.1f}" for i, v in enumerate(vals)) + f" L{xs(len(vals)-1):.1f},{H-B} Z"
    n = len(vals) - 1
    xl = "".join(f'<text x="{xs(i):.1f}" y="{H-8}" text-anchor="{a}" fill="#8a919b" font-size="11" font-family="JetBrains Mono,monospace">{esc(closes[i][0])}</text>' for i, a in ((0, "start"), (n // 2, "middle"), (n, "end")))
    lx, ly = xs(n), ys(vals[-1])
    return f'''<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(d["chart_alt"])}"><defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2ad3c" stop-opacity=".3"/><stop offset="1" stop-color="#f2ad3c" stop-opacity="0"/></linearGradient></defs>{g}{ln}<path d="{area}" fill="url(#ar)"/><polyline points="{pts}" fill="none" stroke="#f2ad3c" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/><circle cx="{lx:.1f}" cy="{ly:.1f}" r="9" fill="#f2ad3c" fill-opacity=".25"/><circle cx="{lx:.1f}" cy="{ly:.1f}" r="4.5" fill="#ffe2aa"/><text x="{lx-12:.1f}" y="{ly+22:.1f}" text-anchor="end" fill="#ffe2aa" font-size="12" font-weight="700" font-family="JetBrains Mono,monospace">{esc(d["chart_live_label"])}</text>{xl}</svg>'''

def video_block(d):
    v = d.get("video")
    if v and v.get("src"):
        m = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", v.get("duration_iso", ""))
        dur = f"{int(m.group(1) or 0)}:{int(m.group(2) or 0):02d}" if m and (m.group(1) or m.group(2)) else ""
        lab = '<span class="vgo-long">Watch the analysis</span><span class="vgo-short">Watch</span>' + (f' · <b>{dur}</b>' if dur else '')
        play = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.6v14.8c0 .8.9 1.3 1.6.9l11.6-7.4c.6-.4.6-1.4 0-1.8L8.6 3.7C7.9 3.3 7 3.8 7 4.6z" fill="currentColor"/></svg>'
        # Gold play cover (MTG, 8 Nov 2026): hidden until the script runs, so without JavaScript the normal player still works.
        return (f'''<div class="vstage" id="video"><div class="vreal"><video controls playsinline preload="metadata" poster="{esc(v["poster"])}" aria-label="{esc(v["title"])}"><source src="{esc(v["src"])}" type="video/mp4"></video>'''
                f'''<button class="vcover" type="button" hidden aria-label="Play the video: {esc(v["title"])}{(", " + dur) if dur else ""}"><img src="{esc(v["poster"])}" alt="" width="1920" height="1080" decoding="async"><span class="vgo"><span class="vgo-btn">{play}</span><span class="vgo-lab">{lab}</span></span></button></div><div class="floor" aria-hidden="true"></div></div>'''
                '''<script>(function(){var s=document.currentScript.previousElementSibling,c=s&&s.querySelector('.vcover'),v=s&&s.querySelector('video');if(!c||!v)return;c.hidden=false;v.controls=false;c.addEventListener('click',function(){c.hidden=true;v.controls=true;var p=v.play();if(p&&p.catch)p.catch(function(){});v.focus()});v.addEventListener('ended',function(){if(document.fullscreenElement&&document.exitFullscreen)document.exitFullscreen();v.load();v.controls=false;c.hidden=false})})();</script>'''
                '<p class="upd" style="margin:10px 0 0;font-size:12.5px">Canton and the Canton logo are trademarks of Digital Asset (Switzerland) GmbH. Digital Asset is not affiliated with, and has not sponsored or endorsed, this report.</p>')
    return '''<div class="vstage">
   <div class="vph" id="tutorial" role="img" aria-label="Weekly technical analysis video coming soon">
    <span class="vbadge"><i aria-hidden="true"></i>Weekly analysis video</span>
    <div class="vin"><span class="vplay" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.2v13.6L19 12z" fill="currentColor"/></svg></span>
     <p class="vt">Video coming soon</p><p class="vs">MTG walks through the chart, the key levels and the three scenarios for the week.</p></div>
    <div class="vbar" aria-hidden="true"><span></span>0:00</div>
   </div><div class="floor" aria-hidden="true"></div></div>'''

def report(d, head, sprite, header, footer, nav_top="", nav_bottom=""):
    date = d["date"]; url = f"{SITE}/canton-weekly/{date}/"
    og = url + "og.jpg" if os.path.exists(os.path.join(ROOT, "canton-weekly", date, "og.jpg")) else SITE + "/assets/og/canton-weekly.jpg"
    s = d["snapshot"]
    title = f"Canton Coin (CC) Price Analysis {d['date_h']}: Weekly Report | MTG"
    desc = d["summary_plain"][:158]
    ogt = f"Canton Coin weekly report, {d['date_h']}: price, levels and scenarios"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": f"Canton Coin weekly report: {d['date_h']}", "description": desc, "image": [og], "datePublished": date + "T06:00:00+02:00", "dateModified": date + "T06:00:00+02:00", "inLanguage": "en-ZA", "mainEntityOfPage": url, "author": {"@id": SITE + "/altruva/#mtg"}, "publisher": {"@id": SITE + "/#tribe"}, "about": [{"@type": "Thing", "name": "Canton Coin", "alternateName": "CC"}, {"@type": "Corporation", "name": "Canton Strategic Holdings, Inc.", "tickerSymbol": "CNTN"}]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "MTG TRIBE", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Canton Weekly", "item": SITE + "/canton-weekly/"}, {"@type": "ListItem", "position": 3, "name": d["date_h"], "item": url}]}]}
    if d.get("video", {}).get("src"):
        v = d["video"]
        ld["@graph"].append({"@type": "VideoObject", "name": v["title"], "description": desc, "thumbnailUrl": [url + v["poster"]], "uploadDate": date + "T06:00:00+02:00", "duration": v["duration_iso"], "contentUrl": url + v["src"], "inLanguage": "en-ZA", "author": {"@id": SITE + "/altruva/#mtg"}})
    h = set_head(head, url, title, desc, ogt, desc, og, f"Canton Coin weekly report {d['date_h']} by MTG", ld, date)
    meta = "".join(f'<li><svg class="ic" aria-hidden="true"><use href="#i-{i}"/></svg>{t}</li>' for i, t in d["meta_chips"])
    alert = ""
    if d.get("listing_alert"):
        alert = f'<section class="answer" style="border-color:rgba(255,123,107,.5);background:rgba(255,123,107,.06)" aria-labelledby="al"><h2 id="al" style="color:#ffb4a2">🚨 New listing alert</h2><p>{d["listing_alert"]}</p></section>'
    tech = table(["Signal", "Reading"], d["technicals"])
    levels = table(["Level", "Price", "Why it matters"], d["levels"])
    scen = table(["Scenario", "Trigger", "What it could look like"], d["scenarios"])
    fund = "".join(f"<li>{x}</li>" for x in d["fundamentals"])
    cntn = table(["CNTN", "Value"], d["cntn_table"])
    cntn_notes = "".join(f"<li>{x}</li>" for x in d["cntn_notes"])
    changed = "".join(f"<li>{x}</li>" for x in d["changed"])
    bottom = "".join(f"<li>{x}</li>" for x in d["bottom_line"])
    src = "".join(f'<li><a class="tx" href="{esc(u)}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in d["sources"])
    legend = '<div class="legend"><span><i style="background:#f2ad3c"></i>Daily close (USD)</span><span><i style="background:#3ddc84"></i>Support</span><span><i style="background:#ff7b6b"></i>Resistance</span></div>'
    body = f'''<body>
{sprite}
{header}
<main id="main">
<section class="hero" aria-labelledby="h1">
 <div class="grid" aria-hidden="true"></div>
 <div class="hero-in wrap">
  <ol class="crumbs" aria-label="Breadcrumb"><li><a href="/">MTG TRIBE</a></li><li><a href="/canton-weekly/">Canton Weekly</a></li><li aria-current="page">{esc(d["date_h"])}</li></ol>
  <p class="kicker"><i class="dot" aria-hidden="true"></i>Weekly market report</p>
  <h1 id="h1"><span class="w">Canton Coin weekly</span>{esc(d["date_h"])}</h1>
  <p class="lede">{d["lede"]}</p>
  {video_block(d)}
  <ul class="meta">{meta}</ul>
 </div>
</section>
<div class="content"><div class="wrap narrow">
 {nav_top}
 {alert}
 <section class="answer" aria-labelledby="qa"><h2 id="qa">This week in one paragraph</h2><p>{d["summary"]}</p></section>
 {learn_cards()}
 <section class="sec" id="snapshot" aria-labelledby="snap-h"><h2 id="snap-h">Snapshot</h2>
  {table(["Canton Coin (CC)", d["date_h"]], s)}
  <div class="chartbox">{legend}{chart_svg(d)}</div>
  <p class="upd">{d["snapshot_note"]}</p>
  <h3 class="part">CC right now</h3><p class="upd">The numbers above are from {esc(d["date_h"])}. This chart is live, so you can compare.</p>{CC_CARD}
 </section>
 <section class="sec" id="changed" aria-labelledby="ch-h"><h2 id="ch-h">What changed since last week</h2><ul class="do">{changed}</ul></section>
 <section class="sec" id="technicals" aria-labelledby="t-h"><h2 id="t-h">Technical analysis</h2>{tech}<h3 class="part">Key levels</h3>{levels}</section>
 <section class="sec" id="scenarios" aria-labelledby="sc-h"><h2 id="sc-h">Three scenarios for the coming week</h2>{scen}{tip("Scenarios are possibilities, not predictions. Levels can break either way, so plan your risk before you act.")}</section>
 <section class="sec" id="fundamentals" aria-labelledby="f-h"><h2 id="f-h">Fundamentals</h2><p class="score">Score: {esc(d["fund_score"])}</p><ul class="do">{fund}</ul>{INVESTORS_CARD}</section>
 <section class="sec" id="cntn" aria-labelledby="c-h"><h2 id="c-h">CNTN stock</h2>{cntn}<ul class="do">{cntn_notes}</ul><h3 class="part">CNTN right now</h3>{CNTN_CARD}</section>
 <section class="sec" id="bottom-line" aria-labelledby="b-h"><h2 id="b-h">Bottom line</h2><ul class="do">{bottom}</ul></section>
 {nav_bottom}
 <section class="join" aria-labelledby="join-h">
  <div><h2 id="join-h">Want this every Sunday?</h2><p>Join the MTG TRIBE on WhatsApp. The new Canton report lands there first, and we learn and take action together.</p></div>
  <span class="cta-w"><span class="halo" aria-hidden="true"></span><a class="cta" href="/group/"><span class="wa"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-whatsapp"/></svg></span>Join the MTG TRIBE<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-arrow-right"/></svg></a></span>
 </section>
 <section class="sec" id="sources" aria-labelledby="src-h"><h2 id="src-h">Sources</h2><ul class="src">{src}{INVESTORS_SRC if INVESTORS_URL not in src else ""}</ul>
  <p class="upd" style="margin-top:20px"><a class="tx" href="/canton-weekly/">All Canton weekly reports</a></p></section>
 <p class="disc">Education only, not financial advice. MTG is not a financial adviser. Crypto and small-company shares are high risk: only use money you can afford to lose and always do your own research. The VALR and Bellver Card links are MTG's referral links: MTG may earn a commission at no extra cost to you.</p>
</div></div>
</main>
{footer}'''
    return h + body

# Dashboard button (MTG, 7 Nov 2026): on /cc/, /cntn/ and every report it opens Canton Weekly (the header is
# copied from cntn/index.html, which already points there). The hub itself keeps the main MTG dashboard,
# so its button never just reloads the page you are on.
# Report navigation (MTG, 8 Nov 2026): back to the first report and forward to the latest, from every Canton page.
# Styles: /assets/tribe/canton-nav.css (loaded from the master page head). main() rebuilds every report each run,
# so last week's report gets its "Next week" link as soon as a new one is built.
def short_date(dh):
    return re.sub(r"(\d+) (\w{3})\w* (\d{4})", r"\1 \2 \3", dh)

def series_strip(asc, i=None):
    """Slim bar. On a report (i given): previous, all reports, next. Elsewhere: latest, first, all reports."""
    url = lambda r: f"/canton-weekly/{r['date']}/"
    if i is None:
        latest, first = asc[-1], asc[0]
        items = [f'<a href="{url(latest)}">Latest report: <b>{esc(short_date(latest["date_h"]))}</b></a>']
        if first is not latest:
            items.append(f'<a href="{url(first)}">First report: <b>{esc(short_date(first["date_h"]))}</b></a>')
        items.append('<a href="/canton-weekly/#all">All reports</a>')
    else:
        prev = asc[i - 1] if i > 0 else None
        nxt = asc[i + 1] if i + 1 < len(asc) else None
        items = [(f'<a href="{url(prev)}" rel="prev">&#8592; Previous week: <b>{esc(short_date(prev["date_h"]))}</b></a>' if prev
                  else '<span class="cwn-off">This is the first report</span>'),
                 '<a href="/canton-weekly/#all">All reports</a>',
                 (f'<a href="{url(nxt)}" rel="next">Next week: <b>{esc(short_date(nxt["date_h"]))}</b> &#8594;</a>' if nxt
                  else '<span class="cwn-off">This is the latest report</span>')]
    return '<nav class="cwn" aria-label="Canton Weekly reports" data-nolink><span class="cwn-k">&#128197; Canton Weekly</span>' + "".join(items) + '</nav>'

def series_cards(asc, i):
    """Bottom of a report: previous and next week cards, then first, all and latest."""
    url = lambda r: f"/canton-weekly/{r['date']}/"
    prev = asc[i - 1] if i > 0 else None
    nxt = asc[i + 1] if i + 1 < len(asc) else None
    def card(r, cls, k):
        return (f'<a class="cwp-card {cls}" href="{url(r)}" rel="{"prev" if cls == "prev" else "next"}"><span class="cwp-k">{k}</span>'
                f'<span class="cwp-d">{esc(r["date_h"])}</span><span class="cwp-h">{esc(r["headline"][:1].upper() + r["headline"][1:])}. CC {esc(r["price_short"])}</span></a>')
    left = card(prev, "prev", "&#8592; Previous week") if prev else '<div class="cwp-card prev off"><span class="cwp-k">Previous week</span><span class="cwp-d">This is the first report</span><span class="cwp-h">Canton Weekly started here.</span></div>'
    right = card(nxt, "next", "Next week &#8594;") if nxt else '<div class="cwp-card next off"><span class="cwp-k">Next week</span><span class="cwp-d">This is the latest report</span><span class="cwp-h">A new report lands every Sunday.</span></div>'
    ends = []
    if i > 0:
        ends.append(f'<a href="{url(asc[0])}">&#9198; First report: <b>{esc(short_date(asc[0]["date_h"]))}</b></a>')
    ends.append('<a href="/canton-weekly/#all">All reports</a>')
    if i + 1 < len(asc):
        ends.append(f'<a href="{url(asc[-1])}">Latest report: <b>{esc(short_date(asc[-1]["date_h"]))}</b> &#9197;</a>')
    return (f'<nav class="cwp" aria-labelledby="cwp-h" data-nolink><h2 id="cwp-h">More Canton weekly reports</h2><div class="cwp-grid">{left}{right}</div>'
            f'<div class="cwn cwp-ends" style="border:0;background:none;padding:0">{"".join(ends)}</div></nav>')

GUIDE_NAV_RE = re.compile(r"<!-- canton-weekly-nav -->.*?<!-- /canton-weekly-nav -->", re.S)

def refresh_guide_nav(asc):
    """Keep the Latest / First / All reports strip on /cc/ and /cntn/ pointing at the right reports."""
    block = "<!-- canton-weekly-nav -->" + series_strip(asc) + "<!-- /canton-weekly-nav -->"
    for p in GUIDE_FILES.values():
        s = open(p, encoding="utf-8").read()
        s, n = GUIDE_NAV_RE.subn(lambda m: block, s)
        assert n == 1, f"{p}: canton-weekly-nav markers missing"
        open(p, "w", encoding="utf-8").write(s)

def hub_video(d):
    """Latest report's thumbnail on the hub, with the gold play button; opens the report at its video."""
    v = d.get("video")
    if not (v and v.get("src")):
        return ""
    m = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", v.get("duration_iso", ""))
    dur = f"{int(m.group(1) or 0)}:{int(m.group(2) or 0):02d}" if m and (m.group(1) or m.group(2)) else ""
    lab = '<span class="vgo-long">Watch the analysis</span><span class="vgo-short">Watch</span>' + (f' · <b>{dur}</b>' if dur else '')
    play = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.6v14.8c0 .8.9 1.3 1.6.9l11.6-7.4c.6-.4.6-1.4 0-1.8L8.6 3.7C7.9 3.3 7 3.8 7 4.6z" fill="currentColor"/></svg>'
    href = f"/canton-weekly/{d['date']}/#video"
    return (f'<div class="vstage" style="margin-top:0"><div class="vreal"><a class="vcover" style="position:relative;display:block" href="{href}" aria-label="Watch the video: {esc(v['title'])}{(', ' + dur) if dur else ''}">'
            f'<img src="/canton-weekly/{d["date"]}/{esc(v["poster"])}" alt="" width="1920" height="1080" loading="lazy" decoding="async" style="position:static;display:block;width:100%;height:auto">'
            f'<span class="vgo" style="position:absolute;left:5%;bottom:6.5%"><span class="vgo-btn">{play}</span><span class="vgo-lab">{lab}</span></span></a></div><div class="floor" aria-hidden="true"></div></div>')

def HUB_HEADER(header):
    return header.replace('<a class="mn-btn mn-dash" href="/canton-weekly/">', '<a class="mn-btn mn-dash" href="/dashboard/">')

def hub(reports, head, sprite, header, footer):
    url = SITE + "/canton-weekly/"
    latest = reports[0]
    title = "Canton Coin (CC) Weekly Analysis and Price Report | MTG"
    desc = "Every Sunday: Canton Coin price, chart levels, three scenarios, fundamentals and CNTN stock news, in plain English. By MTG."
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": url + "#page", "url": url, "name": "Canton Weekly", "description": desc, "inLanguage": "en-ZA", "hasPart": [{"@type": "Article", "headline": f"Canton Coin weekly report: {r['date_h']}", "url": f"{SITE}/canton-weekly/{r['date']}/", "datePublished": r["date"]} for r in reports]}
    h = set_head(head, url, title, desc, "Canton Coin weekly report by MTG", desc, SITE + "/assets/og/canton-weekly.jpg", "Canton Coin weekly reports by MTG", ld, latest["date"])
    arch = "".join(f'<li><a href="/canton-weekly/{r["date"]}/"><span>{esc(r["date_h"])}: {esc(r["headline"])}</span><small>CC {esc(r["price_short"])}</small></a></li>' for r in reports)
    arrow = '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-arrow-right"/></svg>'
    body = f'''<body>
{sprite}
{header}
<main id="main">
<section class="hero" aria-labelledby="h1"><div class="grid" aria-hidden="true"></div><div class="hero-in wrap">
  <ol class="crumbs" aria-label="Breadcrumb"><li><a href="/">MTG TRIBE</a></li><li aria-current="page">Canton Weekly</li></ol>
  <p class="kicker"><i class="dot" aria-hidden="true"></i>Every Sunday</p>
  <h1 id="h1"><span class="w">Canton Coin</span>Weekly Report</h1>
  <p class="lede">Price, chart levels, three scenarios, fundamentals and CNTN stock news, in plain English. New every Sunday morning.</p>
  <p style="margin-top:28px"><span class="cta-w"><span class="halo" aria-hidden="true"></span><a class="cta" href="/canton-weekly/{latest["date"]}/">Read this week's report{arrow}</a></span></p>
</div></section>
<div class="content"><div class="wrap narrow">
 {series_strip(list(reversed(reports)))}
 <section class="answer" aria-labelledby="qa"><h2 id="qa">Latest: {esc(latest["date_h"])}</h2><p>{latest["summary"]}</p></section>
 {hub_video(latest)}
 {learn_cards()}
 <section class="sec" aria-labelledby="cc-live-h"><h2 id="cc-live-h">Canton Coin right now</h2><p>The live CC price and the last month, between reports.</p>{CC_CARD}</section>
 <section class="sec" aria-labelledby="cl-h"><h2 id="cl-h">CNTN stock right now</h2><p>Canton Strategic Holdings (Nasdaq: CNTN) holds Canton Coin, so its share price tends to follow CC. Here is the live price and the last month.</p>{CNTN_CARD}</section>
 <section class="sec" id="all" aria-labelledby="ar-h"><h2 id="ar-h">All reports</h2><ul class="arch">{arch}</ul></section>
 <section class="join" aria-labelledby="join-h"><div><h2 id="join-h">Get it first every Sunday</h2><p>Join the MTG TRIBE on WhatsApp and the new report lands in the group first.</p></div>
  <span class="cta-w"><span class="halo" aria-hidden="true"></span><a class="cta" href="/group/"><span class="wa"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-whatsapp"/></svg></span>Join the MTG TRIBE{arrow}</a></span></section>
 <p class="disc">Education only, not financial advice. Always do your own research.</p>
</div></div>
</main>
{footer}'''
    return h + body

def read_or_none(p):
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None

def today_sa():
    """Today's date in South Africa, where MTG publishes (falls back to the computer's own date)."""
    import datetime
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("Africa/Johannesburg")).date().isoformat()
    except Exception:
        return datetime.date.today().isoformat()

def update_sitemap(changed):
    """changed: {url: True if this run changed the page}. New URLs are added; changed ones get today's <lastmod>.
    Pages that did not change keep their date, because Google only trusts lastmod when it is accurate."""
    p = os.path.join(ROOT, "sitemap-home.xml")
    if not os.path.exists(p):
        return
    s = open(p, encoding="utf-8").read()
    today = today_sa()
    for u, did_change in changed.items():
        entry = re.compile(r"(<url><loc>" + re.escape(u) + r"</loc>)(?:<lastmod>[^<]*</lastmod>)?")
        if not entry.search(s):
            s = s.replace("</urlset>", f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n</urlset>")
        elif did_change:
            s = entry.sub(lambda m: m.group(1) + f"<lastmod>{today}</lastmod>", s, count=1)
    open(p, "w", encoding="utf-8").write(s)
    idx = os.path.join(ROOT, "sitemap.xml")
    if any(changed.values()) and os.path.exists(idx):
        x = open(idx, encoding="utf-8").read()
        x = re.sub(r"(<loc>" + re.escape(SITE) + r"/sitemap-home\.xml</loc><lastmod>)[^<]*", lambda m: m.group(1) + today, x)
        open(idx, "w", encoding="utf-8").write(x)

GUIDE_FILES = {"cc": os.path.join(ROOT, "cc", "index.html"), "cntn": os.path.join(ROOT, "cntn", "index.html")}
GUIDE_KEYS = {"cc": ("date", "date_h", "price", "chg", "mcap", "ath", "supply"), "cntn": ("date", "price", "price_date", "range")}

def refresh_guides(d):
    """Copy this week's snapshot numbers into /cc/ and /cntn/ (the "guides" block of the JSON).

    cc  : the fallback table shown when the live CoinGecko price cannot load, plus its snapshot date.
    cntn: the dated price, 52 week range and the date that drives the "may be out of date" notice.
    Only elements marked data-snap="key" change, so the rest of each guide stays exactly as approved.
    """
    g = d.get("guides")
    if not g:
        print("no guides block, guides left as they are")
        return
    for name, keys in GUIDE_KEYS.items():
        vals = g.get(name)
        if not vals:
            continue
        missing = [k for k in keys if k not in vals]
        assert not missing, f"guides.{name} is missing {missing}"
        p = GUIDE_FILES[name]
        s = open(p, encoding="utf-8").read()
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", vals["date"]), f"guides.{name}.date must be YYYY-MM-DD"
        attr = "data-snap-date" if name == "cc" else "data-stale"
        s, n = re.subn(rf'{attr}="[0-9-]+"', f'{attr}="{vals["date"]}"', s)
        assert n >= 1, f"{name}: no {attr} found"
        for k in keys:
            if k == "date":
                continue
            s, n = re.subn(rf'(<(\w+)\b[^>]*\bdata-snap="{k}"[^>]*>).*?(</\2>)', lambda m: m.group(1) + vals[k] + m.group(3), s, flags=re.S)
            assert n >= 1, f"{name}: no data-snap=\"{k}\" found"
        if name == "cntn":
            plain = re.sub(r"<[^>]+>", "", vals["price"])
            s, n = re.subn(r"about \$[0-9.]+ at the \d{1,2} [A-Z][a-z]+ \d{4} close", f"about {plain} at the {vals['price_date']} close", s)
            assert n >= 1, "cntn: FAQ price sentence for structured data not found"
        s = link_html(s)
        assert "—" not in s and "–" not in s, f"dash found in {name}"
        open(p, "w", encoding="utf-8").write(s)
        print("refreshed", p)

def main():
    head, sprite, header, footer = master_parts()
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*.json")))
    wanted = {os.path.basename(p) for p in sys.argv[1:]} or {os.path.basename(p) for p in files}
    latest = os.path.basename(files[-1])
    asc = [json.load(open(p, encoding="utf-8")) for p in files]
    # Remember every page this run can touch, so only pages that really change get a new sitemap date.
    pages = {f"{SITE}/canton-weekly/{d['date']}/": os.path.join(ROOT, "canton-weekly", d["date"], "index.html") for d in asc}
    pages[SITE + "/canton-weekly/"] = os.path.join(ROOT, "canton-weekly", "index.html")
    pages.update({f"{SITE}/{name}/": p for name, p in GUIDE_FILES.items()})
    before = {u: read_or_none(p) for u, p in pages.items()}
    # Every report is rebuilt each run so its Previous / Next links always match the full list of weeks.
    for i, (p, d) in enumerate(zip(files, asc)):
        out = os.path.join(ROOT, "canton-weekly", d["date"])
        os.makedirs(out, exist_ok=True)
        page = link_html(report(d, head, sprite, header, footer, series_strip(asc, i), series_cards(asc, i)))
        assert "\u2014" not in page and "\u2013" not in page, "dash found"
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
        print("built", out)
        if os.path.basename(p) == latest and latest in wanted:
            refresh_guides(d)
    refresh_guide_nav(asc)
    reports = list(reversed(asc))
    os.makedirs(os.path.join(ROOT, "canton-weekly"), exist_ok=True)
    open(os.path.join(ROOT, "canton-weekly", "index.html"), "w", encoding="utf-8").write(link_html(hub(reports, head, sprite, HUB_HEADER(header), footer)))
    update_sitemap({u: read_or_none(p) != before[u] for u, p in pages.items()})
    print("hub built,", len(reports), "reports")

if __name__ == "__main__":
    main()
