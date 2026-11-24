#!/usr/bin/env python3
"""Get a Canton Weekly data file ready for the video (MTG, 24 Nov 2026). Run it right after writing the week's JSON,
BEFORE the narration is made:

    python3 tools/canton-weekly/prepare.py tools/canton-weekly/data/<DATE>.json

It does two things and saves the JSON:
1. "candles": daily CC/USD candles from Kraken's public market data (the same market as the live chart on the site),
   with the 20 and 50 day simple moving averages, RSI(14) and volume, for the video's 3D candlestick chart.
   The last 60 days up to the report date are kept; the averages and RSI use the full history.
2. The Bellver Card ad scene ("bellver") in "video_script", just before the outro, word for word as approved below.
   The narration is made from video_script, so the ad is in MTG's voice every week. If a "bellver" scene is already
   there it is replaced with the approved one, so the wording never drifts.

Safe to run again. Never invent candles: if Kraken cannot be reached, it stops with an error and nothing is saved.
"""
import json, sys, urllib.request, datetime

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
    vs = [s for s in d.get("video_script", []) if s.get("scene") != "bellver"]
    at = next((i for i, s in enumerate(vs) if s.get("scene") == "outro"), len(vs))
    vs.insert(at, dict(BELLVER))
    d["video_script"] = vs
    for s in (BELLVER["text"], BELLVER["caption"]):
        assert "—" not in s and "–" not in s
    out = json.dumps(d, indent=1, ensure_ascii=False)
    open(path, "w", encoding="utf-8").write(out + ("\n" if raw.endswith("\n") else ""))
    last = d["candles"]["rows"][-1]
    print(json.dumps({"candles": len(d["candles"]["rows"]), "last": last, "bellver_scene_at": at, "scenes": [s["scene"] for s in vs]}))


if __name__ == "__main__":
    main()
