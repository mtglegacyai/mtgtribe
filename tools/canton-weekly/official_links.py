"""Official website links for every company, exchange, wallet and tool named on the Canton pages.

Why: visitors should never have to search for a name and risk landing on a copycat or scam site.
Every page gets (1) the first mention of each name in each section linked to its official site and
(2) on the two guides, an "Official websites" table that shows the exact address to check.

Sources used to verify each address (checked 2 November 2026):
- Canton Network's official ecosystem directory (cantonecosystem.com, linked from canton.network)
- Canton Wiki project pages, and each project's own homepage
- The company's own site for exchanges, brokers and tax offices
Add a new name here (with its source) before writing it on a page. Never guess an address.

Usage:
    from official_links import link_html, directory_table
    page = link_html(page)                 # idempotent: safe to run on every build
    html = directory_table(["Binance", ...])
"""
import re

# key: (url, address shown to readers, what it is, rel)
OFFICIAL = {
    # Canton wallets
    "5N Loop": ("https://wallet.looptech.io/", "wallet.looptech.io", "Canton wallet in your browser, by Five North", "noopener"),
    "Console": ("https://consolewallet.io/", "consolewallet.io", "Canton wallet (browser extension and mobile)", "noopener"),
    "Nightly": ("https://nightly.app/", "nightly.app", "Multichain wallet extension that supports Canton", "noopener"),
    "Bron": ("https://bron.org/", "bron.org", "Canton wallet app with no seed phrase", "noopener"),
    "Zoro": ("https://www.zorowallet.com/", "zorowallet.com", "Canton wallet", "noopener"),
    "Send": ("https://send.app/", "send.app", "Payments app that works with Canton DEXs", "noopener"),
    "Ledger": ("https://www.ledger.com/", "ledger.com", "Hardware wallet", "noopener"),
    "Cypherock": ("https://www.cypherock.com/", "cypherock.com", "Hardware wallet", "noopener"),
    # Exchanges (Binance and VALR use MTG's referral links, which open on their official sites)
    "Binance": ("https://accounts.binance.com/register?ref=11139868", "binance.com", "Exchange: buy USDT with local money", "sponsored noopener"),
    "VALR": ("https://www.valr.com/invite/VAKM6VZY", "valr.com", "South African exchange: buy USDT with rand", "sponsored noopener"),
    "Kraken": ("https://www.kraken.com/", "kraken.com", "Exchange that lists CC", "noopener"),
    "Bybit": ("https://www.bybit.com/", "bybit.com", "Exchange that lists CC", "noopener"),
    "KuCoin": ("https://www.kucoin.com/", "kucoin.com", "Exchange that lists CC", "noopener"),
    "Gate": ("https://www.gate.com/", "gate.com", "Exchange that lists CC", "noopener"),
    "MEXC": ("https://www.mexc.com/", "mexc.com", "Exchange that lists CC", "noopener"),
    # Canton DEXs and assets
    "OneSwap": ("https://www.oneswap.cc/", "oneswap.cc", "Canton DEX (swap from your wallet)", "noopener"),
    "Cantex": ("https://www.cantex.io/", "cantex.io", "Canton DEX, built by CaviarNine", "noopener"),
    "CaviarNine": ("https://www.caviarnine.com/", "caviarnine.com", "Team behind Cantex", "noopener"),
    "CBTC": ("https://www.bitsafe.finance/", "bitsafe.finance", "Bitcoin on Canton, issued by BitSafe", "noopener"),
    "Rocky": ("https://rocky.exchange/", "rocky.exchange", "Trading platform on Canton", "noopener"),
    "Ligero": ("https://github.com/canton-foundation/canton-dev-fund/blob/main/proposals/2026-07-Ligero-proof_of_supply_cap_compliance.md",
               "github.com/canton-foundation", "Canton Foundation grant proposal (official record)", "noopener"),
    # Companies and organisations
    "Canton Network": ("https://www.canton.network/", "canton.network", "The network's official website", "noopener"),
    "Digital Asset": ("https://www.digitalasset.com/", "digitalasset.com", "Company that built Canton Network", "noopener"),
    "Canton Strategic Holdings": ("https://www.cantonstrategic.com/", "cantonstrategic.com", "The company behind CNTN stock", "noopener"),
    "DTCC": ("https://www.dtcc.com/", "dtcc.com", "US market infrastructure company", "noopener"),
    "CoinGecko": ("https://www.coingecko.com/en/coins/canton-network", "coingecko.com", "Canton Coin price data", "noopener"),
    "CoinMarketCap": ("https://coinmarketcap.com/currencies/canton-network/", "coinmarketcap.com", "Canton Coin price data", "noopener"),
    # Brokers and markets
    "Interactive Brokers": ("https://www.interactivebrokers.com/", "interactivebrokers.com", "Broker for US shares (most countries)", "noopener"),
    "Robinhood": ("https://robinhood.com/", "robinhood.com", "US broker", "noopener"),
    "SoFi": ("https://www.sofi.com/", "sofi.com", "US broker", "noopener"),
    "EasyEquities": ("https://www.easyequities.co.za/", "easyequities.co.za", "South African investing platform", "noopener"),
    "Nasdaq": ("https://www.nasdaq.com/market-activity/stocks/cntn", "nasdaq.com", "Stock exchange where CNTN is listed", "noopener"),
    "SEC": ("https://www.sec.gov/", "sec.gov", "US markets regulator", "noopener"),
    # Tax offices
    "SARS": ("https://www.sars.gov.za/", "sars.gov.za", "South African tax office", "noopener"),
    "HMRC": ("https://www.gov.uk/government/organisations/hm-revenue-customs", "gov.uk", "UK tax office", "noopener"),
    "IRS": ("https://www.irs.gov/", "irs.gov", "US tax office", "noopener"),
}

# Name patterns as they appear in the text. Case sensitive, longest names first.
PATTERNS = [
    ("Canton Strategic Holdings", r"\bCanton Strategic Holdings\b"),
    ("Interactive Brokers", r"\bInteractive Brokers\b"),
    ("Canton Network", r"\bCanton Network\b"),
    ("Digital Asset", r"\bDigital Asset\b"),
    ("5N Loop", r"\b5N Loop\b|\bLoop\b"),
    ("Console", r"\bConsole(?: Wallet)?\b"),
    ("Zoro", r"\bZoro(?: Wallet)?\b"),
    ("Send", r"(?<=Nightly, )Send\b"),
    ("Binance", r"\bBinance(?:\.com)?\b"),
    ("Nasdaq", r"\bNasdaq\b(?!\.com)"),
    ("Gate", r"\bGate\b"),
] + [(k, r"\b" + re.escape(k) + r"\b") for k in (
    "Nightly", "Bron", "Ledger", "Cypherock", "VALR", "Kraken", "Bybit", "KuCoin", "MEXC", "OneSwap", "Cantex",
    "CaviarNine", "CBTC", "Rocky", "Ligero", "DTCC", "CoinGecko", "CoinMarketCap", "Robinhood", "SoFi",
    "EasyEquities", "SEC", "SARS", "HMRC", "IRS")]
_RX = [(k, re.compile(p)) for k, p in PATTERNS]

# Never link inside these elements (links, headings, FAQ questions, buttons, code, scripts).
_SKIP = {"a", "summary", "h1", "h2", "h3", "h4", "button", "script", "style", "title", "label", "option", "svg", "code", "th"}
_VOID = {"br", "img", "input", "meta", "link", "hr", "source", "use", "path", "wbr", "col", "area", "base", "embed", "track", "param"}
_TOKEN = re.compile(r"<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>|[^<]+", re.S | re.I)


def _anchor(key, text):
    url, _, _, rel = OFFICIAL[key]
    return f'<a class="tx" href="{url}" target="_blank" rel="{rel}">{text}</a>'


def _link_text(text, done):
    out, pos = [], 0
    while True:
        best = None
        for key, rx in _RX:
            if key in done:
                continue
            m = rx.search(text, pos)
            if m and (best is None or m.start() < best[1].start() or (m.start() == best[1].start() and m.end() > best[1].end())):
                best = (key, m)
        if not best:
            break
        key, m = best
        out.append(text[pos:m.start()])
        out.append(_anchor(key, m.group(0)))
        done.add(key)
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


def link_html(page):
    """Link the first mention of each official name in every section of <main>. Safe to run again."""
    if "<main" not in page:
        return page
    start = page.index("<main")
    end = page.index("</main>")
    head, body, tail = page[:start], page[start:end], page[end:]
    out, stack, done, href = [], [], set(), None
    for tok in _TOKEN.findall(body):
        if tok.startswith("<!--") or re.match(r"<(script|style)\b", tok, re.I):
            out.append(tok)
            continue
        if tok.startswith("<"):
            m = re.match(r"<\s*(/)?\s*([a-zA-Z0-9]+)", tok)
            if m:
                closing, name = m.group(1), m.group(2).lower()
                if not closing and (name == "h2" or (name == "article" and 'class="step"' in tok)):
                    done = set()  # new section: link each name once again
                if name == "a":
                    h = re.search(r'href="([^"]*)"', tok)
                    href = None if closing or not h else h.group(1)
                if closing:
                    if name in stack or "nolink:" + name in stack:
                        while stack and stack.pop() not in (name, "nolink:" + name):
                            pass
                elif name not in _VOID and not tok.rstrip().endswith("/>"):
                    stack.append("nolink:" + name if "data-nolink" in tok else name)
            out.append(tok)
            continue
        if any(t in _SKIP or t.startswith("nolink:") for t in stack):
            if "a" in stack and href:  # a name already linked to its own official site counts as linked
                for key, rx in _RX:
                    if OFFICIAL[key][0] == href and rx.search(tok):
                        done.add(key)
            out.append(tok)
            continue
        out.append(_link_text(tok, done))
    return head + "".join(out) + tail


def directory_table(keys, caption_note=""):
    """'Official websites' table: name, what it is, and the exact address readers should see."""
    rows = "".join(
        f'<tr><td data-label="Name"><b>{k}</b></td><td data-label="What it is">{OFFICIAL[k][2]}</td>'
        f'<td data-label="Official site"><a class="tx" href="{OFFICIAL[k][0]}" target="_blank" rel="{OFFICIAL[k][3]}">{OFFICIAL[k][1]}</a></td></tr>'
        for k in keys)
    return ('<div class="tw" data-nolink><table><thead><tr><th scope="col">Name</th><th scope="col">What it is</th>'
            f'<th scope="col">Official site</th></tr></thead><tbody>{rows}</tbody></table></div>')
