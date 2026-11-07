#!/usr/bin/env python3
"""Canton Weekly report builder for mtgtribe.com.

Usage (from the repo root):
    python3 tools/canton-weekly/build.py tools/canton-weekly/data/2026-11-01.json

Reads the master page design from cntn/index.html (CSS, icons,
header, footer, back-to-top), writes:
    canton-weekly/<date>/index.html    the report
    canton-weekly/index.html           the hub (latest report + archive)
and adds both URLs to sitemap-home.xml.
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
        return f'''<div class="vstage"><div class="vreal"><video controls playsinline preload="metadata" poster="{esc(v["poster"])}" aria-label="{esc(v["title"])}"><source src="{esc(v["src"])}" type="video/mp4"></video></div><div class="floor" aria-hidden="true"></div></div>'''
    return '''<div class="vstage">
   <div class="vph" id="tutorial" role="img" aria-label="Weekly technical analysis video coming soon">
    <span class="vbadge"><i aria-hidden="true"></i>Weekly analysis video</span>
    <div class="vin"><span class="vplay" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.2v13.6L19 12z" fill="currentColor"/></svg></span>
     <p class="vt">Video coming soon</p><p class="vs">MTG walks through the chart, the key levels and the three scenarios for the week.</p></div>
    <div class="vbar" aria-hidden="true"><span></span>0:00</div>
   </div><div class="floor" aria-hidden="true"></div></div>'''

def report(d, head, sprite, header, footer):
    date = d["date"]; url = f"{SITE}/canton-weekly/{date}/"
    og = url + "og.jpg" if d.get("og") else SITE + "/cc/img/og-how-to-buy-canton-coin.jpg"
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
def HUB_HEADER(header):
    return header.replace('<a class="mn-btn mn-dash" href="/canton-weekly/">', '<a class="mn-btn mn-dash" href="/dashboard/">')

def hub(reports, head, sprite, header, footer):
    url = SITE + "/canton-weekly/"
    latest = reports[0]
    title = "Canton Coin (CC) Weekly Analysis and Price Report | MTG"
    desc = "Every Sunday: Canton Coin price, chart levels, three scenarios, fundamentals and CNTN stock news, in plain English. By MTG."
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": url + "#page", "url": url, "name": "Canton Weekly", "description": desc, "inLanguage": "en-ZA", "hasPart": [{"@type": "Article", "headline": f"Canton Coin weekly report: {r['date_h']}", "url": f"{SITE}/canton-weekly/{r['date']}/", "datePublished": r["date"]} for r in reports]}
    h = set_head(head, url, title, desc, "Canton Coin weekly report by MTG", desc, SITE + "/cc/img/og-how-to-buy-canton-coin.jpg", "Canton Coin weekly reports by MTG", ld, latest["date"])
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
 <section class="answer" aria-labelledby="qa"><h2 id="qa">Latest: {esc(latest["date_h"])}</h2><p>{latest["summary"]}</p></section>
 {learn_cards()}
 <section class="sec" aria-labelledby="cc-live-h"><h2 id="cc-live-h">Canton Coin right now</h2><p>The live CC price and the last month, between reports.</p>{CC_CARD}</section>
 <section class="sec" aria-labelledby="cl-h"><h2 id="cl-h">CNTN stock right now</h2><p>Canton Strategic Holdings (Nasdaq: CNTN) holds Canton Coin, so its share price tends to follow CC. Here is the live price and the last month.</p>{CNTN_CARD}</section>
 <section class="sec" aria-labelledby="ar-h"><h2 id="ar-h">All reports</h2><ul class="arch">{arch}</ul></section>
 <section class="join" aria-labelledby="join-h"><div><h2 id="join-h">Get it first every Sunday</h2><p>Join the MTG TRIBE on WhatsApp and the new report lands in the group first.</p></div>
  <span class="cta-w"><span class="halo" aria-hidden="true"></span><a class="cta" href="/group/"><span class="wa"><svg class="ic" aria-hidden="true" focusable="false"><use href="#i-whatsapp"/></svg></span>Join the MTG TRIBE{arrow}</a></span></section>
 <p class="disc">Education only, not financial advice. Always do your own research.</p>
</div></div>
</main>
{footer}'''
    return h + body

def update_sitemap(urls):
    p = os.path.join(ROOT, "sitemap-home.xml")
    if not os.path.exists(p):
        return
    s = open(p, encoding="utf-8").read()
    for u in urls:
        if f"<loc>{u}</loc>" not in s:
            s = s.replace("</urlset>", f"  <url><loc>{u}</loc></url>\n</urlset>")
    open(p, "w", encoding="utf-8").write(s)

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
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(DATA_DIR, "*.json")))
    latest = max(os.path.basename(p) for p in glob.glob(os.path.join(DATA_DIR, "*.json")))
    for p in paths:
        d = json.load(open(p, encoding="utf-8"))
        out = os.path.join(ROOT, "canton-weekly", d["date"])
        os.makedirs(out, exist_ok=True)
        page = link_html(report(d, head, sprite, header, footer))
        assert "—" not in page and "–" not in page, "dash found"
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
        print("built", out)
        if os.path.basename(p) == latest:
            refresh_guides(d)
    reports = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(DATA_DIR, "*.json")), reverse=True)]
    os.makedirs(os.path.join(ROOT, "canton-weekly"), exist_ok=True)
    open(os.path.join(ROOT, "canton-weekly", "index.html"), "w", encoding="utf-8").write(link_html(hub(reports, head, sprite, HUB_HEADER(header), footer)))
    update_sitemap([SITE + "/canton-weekly/"] + [f"{SITE}/canton-weekly/{r['date']}/" for r in reports])
    print("hub built,", len(reports), "reports")

if __name__ == "__main__":
    main()
