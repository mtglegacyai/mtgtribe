# Canton Weekly tracker

## Weekly log (newest first)

| Date | CC price | 7d | CNTN | Key event | Web page |
|---|---|---|---|---|---|
| 2026-11-22 | $0.0736 | -8% | $1.21 (20 Nov) | $0.075 support broke 20 Nov, low $0.071 (lowest since Dec 2025); CapConnect+ approved as Super Validator (CIP-0131, 18 Nov); CIP-0132 universal burn Phase 1 proposed; Talos, Marex, Broadridge tokenized Treasury plan; CNTN Q3 first positive adj. EBITDA | Published automatically |
| 2026-11-15 | $0.0801 | -14% | $1.71 (13 Nov) | Market-wide sell-off (BTC -14%, Fear and Greed 10), CC lowest since Dec 2025; Nomura approved as Super Validator (CIP-0130); DA and Progmat tokenized JGB MOU | Published automatically |
| 2026-11-08 | $0.0927 | -5% | $2.06 (6 Nov) | SEC staff no-action letter on CC (3 Nov), DTCC live on Canton, first tokenized CNTN trades on TSV (4 Nov) | Live |
| 2026-11-01 | $0.0962 | -5% | $1.98 (30 Oct) | CIP-0129 universal burn approved, tokenized CNTN announced | Live (first report) |

## Current levels (22 Nov 2026)

- Resistance: $0.075 (old support, broke 20 Nov), $0.081 (17 to 19 Nov closes), then the 20 day average near $0.087
- Support: $0.071 (21 Nov Kraken low, mid Dec 2025 base), $0.063 (6 to 8 Dec 2025 closes), $0.059 (all-time low)
- Indicators: RSI(14) about 30, MACD below signal and zero, 20d $0.087, 50d $0.100, 200d $0.123. Volume fading ($7 to 8M a day)
- Futures: at least $24M open interest across 11 venues (Binance $9.7M, Bybit $5.5M, CoinW $3.0M, OKX $2.2M, Hyperliquid $1.7M), down from $34M; funding flat.
  Binance and Bybit public APIs are geo-blocked here: use CoinGecko /derivatives/exchanges/<id>?include_tickers=unexpired per venue, OKX public API works
- Burn vs mint: supply 40.06B to 40.10B CC in a week; reports citing CantonScan put burn at about 80% of mint; cumulative burn 6.13B (16 Nov)

## Open questions

- Does $0.071 hold? A daily close below opens $0.063. A close back above $0.075 is the first sign of repair.
- Does CC keep moving with Bitcoin while the Fear and Greed Index sits at 10 to 12?
- Splice 0.10.1 MainNet upgrade listed for 23 Nov (time TBC): smooth or not?
- Validator application batch (Kiwoom, CSDBR, Circle Internet Group and others): objection period ends 25 Nov.
- CIP-0132 (dSync Paymaster, universal burn Phase 1): vote outcome; Q1 2027 burn start. Grant proposals filed: CIP-0127 locking 9.5M CC, Fairmint asset data feed 2.4M CC, BitDynamics devkit 4.8M CC.
- Fairmint TSV venue: launch date, who can access, South Africa? CNTN at a new 52 week low ($1.19); Q3 shows 3.83B CC held and $26.9M cash.
- Any CC spot listing on Binance or VALR? (None found 22 Nov: CoinGecko tickers show no Binance spot, VALR has no CC pair.) Digital Asset IPO: nothing found.

## Notes for the next run

- build.py needs Python 3.12 or newer (f-string syntax): run it with python3.12. check_og.py also needs python3.12 (PIL).
- Pages to update: none this week (no new listing).
