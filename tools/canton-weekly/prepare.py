#!/usr/bin/env python3
"""Get a Canton Weekly data file ready for the video (MTG, 24 Nov 2026). Run it right after writing the week's JSON,
BEFORE the narration is made:

    python3 tools/canton-weekly/prepare.py tools/canton-weekly/data/<DATE>.json

It does three things and saves the JSON:
1. "candles": daily CC/USD candles from Kraken's public market data (the same market as the live chart on the site),
   with the 20 and 50 day simple moving averages, RSI(14) and volume, for the video's 3D candlestick chart.
   The last 60 days up to the report date are kept; the averages and RSI use the full history.
2. The fixed scenes MTG says in every report (24 Nov 2026), word for word as approved below:
   "burn" (universal burn, CIP-0129) and "halving" (the Canton Coin minting curve) after the fundamentals,
   then "tribe" (thank the MTG TRIBE WhatsApp group, invite everyone else) and "streams" (where the money comes from:
   his income streams, read from the Income streams list of the mtgtribe.com dashboard menu, so a new stream is named
   automatically) before the Bellver ad.
3. The Bellver Card ad scene ("bellver") just before the outro.
   The narration is made from video_script, so all of this is in MTG's voice every week. Fixed scenes already there
   are replaced with the approved ones, so the wording never drifts.

Safe to run again. Never invent candles: if Kraken cannot be reached, it stops with an error and nothing is saved.
"""
import json, os, re, sys, urllib.request, datetime

KRAKEN = "https://api.kraken.com/0/public/OHLC?pair=CCUSD&interval=1440"
KEEP = 60

# The approved Bellver Card ad for every weekly video (MTG, 24 Nov 2026). Figures and wording from bellveraffiliates.com.
# "text" is spoken (numbers as words), "caption" is shown, one caption sentence per spoken sentence so they stay in step.
BELLVER = {
    "scene": "bellver",
    "text": ("Before you go. Want to spend your crypto like cash? Get the Bellver crypto debit card, the card that can pay your bills. "
             "Fund it with crypto and spend in any currency, anywhere in the world. "
             "Then share it, and you can earn from ten to five hundred dollars for every card ordered through your link, plus monthly rewards as your team grows. "
             "Order yours, or become a partner, at Bellver affiliates dot com. Earnings are not guaranteed."),
    "caption": ("Before you go. Want to spend your crypto like cash? Get the Bellver crypto debit card, the card that can pay your bills. "
                "Fund it with crypto and spend in any currency, anywhere in the world. "
                "Then share it, and earn $10 to $500 for every card ordered through your link, plus monthly rewards as your team grows. "
                "Order yours, or become a partner, at bellveraffiliates.com. Earnings are not guaranteed."),
}


# Universal burn and halving (MTG, 24 Nov 2026). Facts checked on 24 Nov 2026 against official sources:
# - CIP-0129 "Universal Burn and Synchronizer Pricing", status Approved (23 Oct 2026). Phase 1, universal burn, "Q1 2027";
#   phase 2, volume pricing, "Q3 2027": the authors call these "ambitious estimates", not deadlines.
#   https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md
# - Minting curve (Canton Coin white paper, MainNet live June 2024): up to 40 billion CC a year for the first 6 months,
#   20 billion to 18 months, 10 billion to year 5, 5 billion to year 10, then 2.5 billion a year for good.
#   CIP-0105: the next step down (halving) is "currently forecast to occur late summer 2029". Year 10 is about 2034.
# FACTS_UNTIL: after these dates the wording is out of date. prepare.py then warns, and the weekly task must check the
# sources above, update the text (spoken and caption), and tell MTG what changed.
FACTS_UNTIL = {"burn": "2027-01-01", "halving": "2029-06-01"}

BURN = {
    "scene": "burn",
    "text": ("Now, the universal burn. Canton's Super Validators approved it in October. "
             "Soon every Canton synchronizer running real business, not only the Global Synchronizer, will burn C C for its traffic. "
             "The first phase is expected in early twenty twenty seven. "
             "More use, more C C burned, fewer coins in circulation. "
             "If demand keeps growing, that is a real positive for the price."),
    "caption": ("Now, the universal burn. Canton's Super Validators approved it in October (CIP-0129). "
                "Soon every Canton synchronizer running real business, not only the Global Synchronizer, will burn CC for its traffic. "
                "The first phase is expected in early 2027 (an estimate). "
                "More use, more CC burned, fewer coins in circulation. "
                "If demand keeps growing, that is a real positive for the price."),
}

HALVING = {
    "scene": "halving",
    "text": ("And the Canton halving. New C C supply steps down over time, and it has already been cut from forty billion to ten billion coins a year. "
             "The next halving, to five billion, is forecast for late summer twenty twenty nine. "
             "The one after, around twenty thirty four, takes it to two and a half billion a year, for good. "
             "The burn takes coins out, the halving slows new coins in. "
             "With growing demand, that is a positive for the price, and that is why I keep accumulating."),
    "caption": ("And the Canton halving. New CC supply steps down over time, and it has already been cut from 40 billion to 10 billion coins a year. "
                "The next halving, to 5 billion, is forecast for late summer 2029. "
                "The one after, around 2034, takes it to 2.5 billion a year, for good. "
                "The burn takes coins out, the halving slows new coins in. "
                "With growing demand, that is a positive for the price, and that is why I keep accumulating."),
}

TRIBE = {
    "scene": "tribe",
    "text": ("A big thank you to everyone in my M T G TRIBE WhatsApp group. You are the best. "
             "Not in the group yet? That is where I post my updates first. "
             "Join us at M T G tribe dot com slash group."),
    "caption": ("A big thank you to everyone in my MTG TRIBE WhatsApp group. You are the best. "
                "Not in the group yet? That is where I post my updates first. "
                "Join us at mtgtribe.com/group."),
}

# Streams MTG does not want named in the weekly video, even while they are still in the dashboard menu
# (MTG, 24 Nov 2026: "please remove ALTRUVA, I no longer want it there as one of my income streams").
# video.py hides them in the menu screenshots too.
EXCLUDE_STREAMS = {"ALTRUVA"}

NUM = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]


def income_streams():
    """The Income streams list of the mtgtribe.com dashboard menu, in its order (dashboard/index.html)."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    h = open(os.path.join(root, "dashboard", "index.html"), encoding="utf-8").read()
    i = h.index('id="mtg-menu"')
    j = h.index('Income streams</p>', i)
    k = h.index('<p class="md-label">', j)
    names = [re.sub(r"<[^>]+>", "", n).replace("&amp;", "&").strip() for n in re.findall(r'class="md-nav[^"]*"[^>]*>.*?<b>(.*?)</b>', h[j:k])]
    names = [n for n in names if n not in EXCLUDE_STREAMS]
    if not 3 <= len(names) <= 10:
        raise SystemExit(f"Found {len(names)} income streams in the dashboard menu: check dashboard/index.html")
    return names


def streams_scene():
    names = income_streams()
    say = lambda n: n.replace(" · ", " and ").replace("·", " and ").replace("PRENET", "Prenet")   # a word, not P R E N E T
    show = lambda n: n.replace(" · ", " and ")
    lst_t = " ".join(f"{NUM[i]}, {say(n)}." for i, n in enumerate(names))
    lst_c = " ".join(f"{NUM[i]}, {show(n)}." for i, n in enumerate(names))
    return {
        "scene": "streams",
        "streams": names,
        "text": ("Where does my money come from? "
                 "I buy C C and C N T N with cash flow from my multiple streams of income. "
                 "Go to M T G tribe dot com, tap Dashboard, then Menu, and look under Income streams. "
                 f"{lst_t} "
                 "That is how I generate my cash flow. See one you like? "
                 "Join, test drive it, and let's keep stacking C C and C N T N together."),
        "caption": ("Where does my money come from? "
                    "I buy CC and CNTN with cash flow from my multiple streams of income. "
                    "Go to mtgtribe.com, tap Dashboard, then Menu, and look under Income streams. "
                    f"{lst_c} "
                    "That is how I generate my cash flow. See one you like? "
                    "Join, test drive it, and let's keep stacking CC and CNTN together."),
    }


FIXED = ("burn", "halving", "tribe", "streams", "bellver")


def place_fixed(script):
    """Put the fixed scenes in their places: burn and halving right after the fundamentals (or the scenarios),
    tribe, streams and bellver right before the outro. Order: ... fundamentals, burn, halving, guides, tribe,
    streams, bellver, outro."""
    vs = [s for s in script if s.get("scene") not in FIXED]
    names = [s.get("scene") for s in vs]
    after = next((n for n in ("fundamentals", "scenarios", "levels") if n in names), None)
    at = names.index(after) + 1 if after else max(0, len(vs) - 1)
    vs[at:at] = [dict(BURN), dict(HALVING)]
    end = next((i for i, s in enumerate(vs) if s.get("scene") == "outro"), len(vs))
    vs[end:end] = [dict(TRIBE), streams_scene(), dict(BELLVER)]
    return vs


def fact_warnings(date):
    return [f"The {k} scene's facts are dated: today is past {v}. Check the sources in prepare.py, update the {k.upper()} "
            f"wording (text and caption), and tell MTG what changed." for k, v in FACTS_UNTIL.items() if date >= v]


def sma(vals, n, i):
    return round(sum(vals[i - n + 1:i + 1]) / n, 6) if i >= n - 1 else None


def rsi_series(closes, n=14):
    out = [None] * len(closes)
    if len(closes) <= n:
        return out
    gains = [max(0.0, closes[i] - closes[i - 1]) for i in range(1, len(closes))]
    losses = [max(0.0, closes[i - 1] - closes[i]) for i in range(1, len(closes))]
    ag, al = sum(gains[:n]) / n, sum(losses[:n]) / n
    for i in range(n, len(closes)):
        if i > n:
            ag = (ag * (n - 1) + gains[i - 1]) / n
            al = (al * (n - 1) + losses[i - 1]) / n
        out[i] = round(100.0 if al == 0 else 100 - 100 / (1 + ag / al), 2)
    return out


def candles(report_date):
    req = urllib.request.Request(KRAKEN, headers={"User-Agent": "mtgtribe-canton-weekly"})
    data = json.load(urllib.request.urlopen(req, timeout=30))
    if data.get("error"):
        raise SystemExit(f"Kraken error: {data['error']}")
    rows = [r for k, r in data["result"].items() if k != "last"][0]
    day = lambda r: datetime.datetime.fromtimestamp(int(r[0]), datetime.timezone.utc).date().isoformat()
    rows = [r for r in rows if day(r) <= report_date]
    if len(rows) < 60:
        raise SystemExit(f"Kraken returned only {len(rows)} daily candles up to {report_date}: not enough for MA50 and RSI")
    closes = [float(r[4]) for r in rows]
    rsi = rsi_series(closes)
    out = []
    for i, r in enumerate(rows):
        out.append({"d": day(r), "o": float(r[1]), "h": float(r[2]), "l": float(r[3]), "c": float(r[4]), "v": round(float(r[6]), 2),
                    "ma20": sma(closes, 20, i), "ma50": sma(closes, 50, i), "rsi": rsi[i]})
    return {"source": "Kraken CC/USD, daily candles", "asof": report_date, "rows": out[-KEEP:]}


def main():
    path = sys.argv[1]
    raw = open(path, encoding="utf-8").read()
    d = json.loads(raw)
    d["candles"] = candles(d["date"])
    vs = place_fixed(d.get("video_script", []))
    d["video_script"] = vs
    for x in vs:
        if x["scene"] in FIXED:
            for t in (x["text"], x["caption"]):
                assert "\u2014" not in t and "\u2013" not in t, "no em or en dashes"
                assert len(re.split(r"(?<=[.!?:])\s+", x["text"])) == len(re.split(r"(?<=[.!?:])\s+", x["caption"])), x["scene"]
    warn = fact_warnings(d["date"])
    out = json.dumps(d, indent=1, ensure_ascii=False)
    open(path, "w", encoding="utf-8").write(out + ("\n" if raw.endswith("\n") else ""))
    last = d["candles"]["rows"][-1]
    chars = sum(len(x["text"]) for x in vs)
    print(json.dumps({"candles": len(d["candles"]["rows"]), "last": last, "scenes": [s["scene"] for s in vs],
                      "estimated_length_s": round(chars / 17), "warnings": warn}))

if __name__ == "__main__":
    main()
