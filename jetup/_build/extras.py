# Five navigation and learning helpers for the JetUP guide (MTG, 7 November 2026):
#   1. the jump bar on long pages, 2. "continue where you left off" (data only, the page script does the rest),
#   3. the thumb bar on phones, 4. tap a word to see what it means + the glossary page, 5. search the guide.
# No em or en dashes anywhere in this file's text.
import hashlib, html, json, os, re

# ---------------------------------------------------------------- 4. glossary
# key, the word as shown in the glossary, the pattern that finds it in page text, the plain explanation, where to learn more
GLOSSARY = [
 ('2fa', '2FA', r'\b2FA\b', 'Two-factor authentication: a second code, usually from an app on your phone, that you enter when you log in.', '/jetup/bix-card/#setup'),
 ('amplify', 'Amplify (24x)', r'\bAmplify\b', "TAG Markets' setting that lets an account trade at 24 times its size. Gains and losses both get 24 times bigger.", '/jetup/how-it-works/#amplify'),
 ('cfd', 'CFD', r'\bCFDs?\b', 'Contract for difference: you trade a price movement without owning the thing itself.', '/jetup/#risk'),
 ('community-token', 'Community token', r'\b[Cc]ommunity token\b', "A code from your sponsor's team, entered when you connect Sonic AI. The training says that with it, the loss limit becomes 5%.", '/jetup/get-started/#part-5'),
 ('copyx', 'CopyX', r'\bCopyX\b', "TAG Markets' copy trading platform. It copies a strategy's trades into your account.", '/jetup/how-it-works/#copy'),
 ('cu-number', 'CU number', r'\bCU number\b', 'Your TAG Markets client number, shown under Profile. You need it to claim the JetUP promo.', '/jetup/promo/#claim'),
 ('exposure', 'Exposure', r'\b[Ee]xposure\b', 'The size you trade with, not money you own. $250 with 24x Amplify trades like $6,000.', '/jetup/how-it-works/#amplify'),
 ('fsc', 'FSC', r'\bFSC\b', 'Financial Services Commission of Mauritius: the regulator that licenses T.M. Financials Ltd, the company behind TAG Markets.', '/jetup/five-checks/#check-2'),
 ('fsca', 'FSCA', r'\bFSCA\b', "Financial Sector Conduct Authority: South Africa's financial regulator.", '/jetup/five-checks/#check-2'),
 ('kyc', 'KYC', r'\bKYC\b', 'Know Your Customer: proving who you are, usually with an ID document and sometimes a proof of address.', '/jetup/get-started/#part-3'),
 ('leverage', 'Leverage', r'\b[Ll]everage\b', "Trading with more than your own money, which makes gains and losses bigger. Amplify is TAG Markets' version of it.", '/jetup/how-it-works/#amplify'),
 ('liquidated', 'Liquidated', r'\b[Ll]iquidat(?:ed|es|ion)\b', 'Closed. The account is closed when the loss limit is reached.', '/jetup/how-it-works/#amplify'),
 ('lot', 'Lot', r'\blots?\b', "A standard trade size. JetUP's lot commission is counted per lot traded in your structure.", '/jetup/partner-plan/#lot'),
 ('mt5', 'MT5', r'\bMT5\b', 'MetaTrader 5: the trading app many brokers use. Your TAG Markets trading account is an MT5 account.', '/jetup/five-checks/#check-1'),
 ('myfxbook', 'Myfxbook', r'\bMyfxbook\b', "A website that publishes trading results, so you can look at a strategy's record before you deposit.", '/jetup/five-checks/#check-3'),
 ('network', 'Network', r'\bnetwork\b', 'The blockchain route a coin travels on, for example Tron (TRC20). The sending side and the receiving side must use the same network.', '/jetup/get-started/#part-4'),
 ('partner-link', 'Partner link', r'\bPartner link\b', 'The sign-up link for partners. Every member has a Partner link and a Client link: use the Partner link to join as a partner.', '/jetup/get-started/#part-1'),
 ('performance-fee', 'Performance fee', r'\b[Pp]erformance fee\b', 'The 30% of strategy profit that pays the broker, the strategy provider and the partner program. It is only taken from profits.', '/jetup/how-it-works/#split'),
 ('recovery-phrase', 'Recovery phrase', r'\b[Rr]ecovery phrase\b', 'The secret words that restore a self-custody wallet. Write them down offline and never share them with anyone.', '/jetup/bix-card/#setup'),
 ('self-custody', 'Self-custody', r'\b[Ss]elf-custody\b', 'You hold the keys to your own crypto wallet, so only you can move the funds.', '/jetup/bix-card/'),
 ('sonic-ai', 'Sonic AI', r'\bSonic AI\b', 'The strategy members connect on CopyX. It trades gold (XAU/USD), and its record is published on Myfxbook.', '/jetup/how-it-works/#copy'),
 ('usdt-usdc', 'USDT and USDC', r'\bUSD[TC]\b', 'Digital dollars (stablecoins) that you send from an exchange to fund your TAG Markets account.', '/jetup/get-started/#part-4'),
 ('xau-usd', 'XAU/USD', r'XAU/USD', 'Gold priced in US dollars: XAU means gold, USD means US dollar.', '/jetup/how-it-works/#copy'),
]
GL = {k: (name, pat, d, more) for k, name, pat, d, more in GLOSSARY}

# never put a word button inside these (headings, links, buttons, labels, code, the FAQ question line, table headers)
_SKIP = {'a', 'button', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'kbd', 'code', 'script', 'style', 'summary', 'label',
         'title', 'option', 'textarea', 'select', 'svg', 'th', 'figcaption', 'small', 'nav', 'dialog', 'caption'}

_VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

def mark_terms(page_html):
    """Turn the first use of each glossary word inside <main> into a small button that explains it. Returns (html, keys).
    Skips headings, links, buttons and the like, anything hidden from screen readers, and the moving ticker tape."""
    a, b = page_html.find('<main'), page_html.find('</main>')
    if a < 0 or b < 0:
        return page_html, []
    parts = re.split(r'(<[^>]+>)', page_html[a:b])
    stack, done, used = [], set(), []          # stack of (tag, skip) for every open element
    for i, part in enumerate(parts):
        if part.startswith('<'):
            m = re.match(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)', part)
            if not m or part.startswith('<!'):
                continue
            tag = m.group(2).lower()
            if m.group(1):                          # closing tag: pop back to its opening tag
                for j in range(len(stack) - 1, -1, -1):
                    if stack[j][0] == tag:
                        del stack[j:]
                        break
            elif tag not in _VOID and not part.endswith('/>'):
                skip = (tag in _SKIP or 'aria-hidden="true"' in part or re.search(r'class="[^"]*\b(tape|nogl)\b', part) is not None)
                stack.append((tag, skip))
            continue
        if not part.strip() or any(sk for _, sk in stack):
            continue
        # find every not-yet-used word in this piece of text first, then build the piece once,
        # so a button's own label can never be matched again
        hits = []
        for k, (name, pat, d, more) in GL.items():
            if k not in done:
                mm = re.search(pat, part)
                if mm:
                    hits.append((mm.start(), mm.end(), k))
        if not hits:
            continue
        hits.sort()
        out, pos = [], 0
        for s0, e0, k in hits:
            if s0 < pos:          # overlaps a word already marked in this piece: try it in a later piece
                continue
            done.add(k); used.append(k)
            word = part[s0:e0]
            out.append(part[pos:s0])
            out.append(('<button type="button" class="gl" data-g="%s" aria-expanded="false" aria-controls="glpop" '
                        'aria-label="%s: what does it mean?">%s</button>') % (k, html.escape(html.unescape(word), quote=True), word))
            pos = e0
        out.append(part[pos:])
        parts[i] = ''.join(out)
    return page_html[:a] + ''.join(parts) + page_html[b:], used

def gl_popover(keys):
    if not keys:
        return ''
    data = {k: [GL[k][0], GL[k][2], '/jetup/glossary/#g-' + k] for k in keys}
    return ('<div class="glpop" id="glpop" hidden><p class="glh"></p><p class="gld" aria-live="polite"></p>'
            '<a class="gll" href="/jetup/glossary/">See every word in the glossary</a>'
            '<button type="button" class="glx" aria-label="Close the explanation">&times;</button></div>'
            '<script type="application/json" id="gl-data">%s</script>') % json.dumps(data, ensure_ascii=False).replace('</', '<\\/')

# ---------------------------------------------------------------- FAQ: give every question an address, so search can open it
def faq_ids(page_html, prefix='q'):
    seen = set()
    def add(m):
        tag, q = m.group(1), m.group(2)
        if 'id=' in tag:
            return m.group(0)
        slug = re.sub(r'[^a-z0-9]+', '-', html.unescape(re.sub(r'<[^>]+>', '', q)).lower()).strip('-')[:48].strip('-')
        base, n = prefix + '-' + slug, 2
        sid = base
        while sid in seen:
            sid = '%s-%d' % (base, n); n += 1
        seen.add(sid)
        return '<details id="%s"%s<summary>%s</summary>' % (sid, tag[len('<details'):], q)
    return re.sub(r'(<details\b[^>]*>)<summary>(.*?)</summary>', add, page_html, flags=re.S)

# ---------------------------------------------------------------- 1. jump bar: the sections of each long page
JUMP = {
 '/jetup/': [('who', 'The simple picture'), ('split', 'The 70/30 split'), ('plan', '$155 and exposure'), ('checks', 'The 5 checks'),
             ('start', 'Sign up in 6 parts'), ('promo', 'The promo'), ('explore', 'Go deeper'), ('risk', 'Read before you deposit'),
             ('mtg', 'About MTG'), ('faq', 'Questions')],
 '/jetup/five-checks/': [('check-1', 'Who holds my money?'), ('check-2', 'Who regulates the broker?'), ('check-3', 'Are the results real?'),
                         ('check-4', 'What can go wrong?'), ('check-5', 'Can I get out?')],
 '/jetup/get-started/': [('part-1', 'Create your JetUP account'), ('part-2', 'Link JetUP to TAG Markets'), ('part-3', 'Verify your identity'),
                         ('part-4', 'Fund your account'), ('part-5', 'Connect Sonic AI'), ('part-6', 'Claim the promo')],
 '/jetup/how-it-works/': [('who', 'Who does what'), ('copy', 'What copying means'), ('split', 'The 70/30 split'),
                          ('amplify', 'Exposure'), ('withdraw', 'Withdrawals')],
 '/jetup/partner-plan/': [('qualify', 'The rule most people miss'), ('lot', 'Lot commission'), ('profit-share', 'Profit Share'),
                          ('infinity', 'Infinity Bonus'), ('pool', 'Global Pool'), ('rewards', 'Rewards')],
 '/jetup/bix-card/': [('setup', 'Five steps to your card'), ('link', 'Link it to JetUP'), ('prices', 'Prices')],
}
# pages whose sections can be ticked: the chip shows a tick when that item is done
JUMP_TICKS = {'/jetup/five-checks/': ('checks', 'c'), '/jetup/get-started/': ('parts', 'p')}

def jump_bar(path, icon):
    items = JUMP.get(path)
    if not items:
        return ''
    n = len(items)
    tick = JUMP_TICKS.get(path)
    chips = ''
    if n <= 6:
        chips = '<div class="jchips">%s</div>' % ''.join(
            '<a class="jc" href="#%s" data-i="%d"%s aria-label="%d of %d: %s"><span>%d</span></a>' % (
                sid, i, (' data-tick="%s%d"' % (tick[1], i + 1)) if tick else '', i + 1, n, html.escape(lab, quote=True), i + 1)
            for i, (sid, lab) in enumerate(items))
    lis = ''.join('<li><a href="#%s" data-i="%d"%s><span class="jn">%d</span><span class="jl">%s</span></a></li>' % (
        sid, i, (' data-tick="%s%d"' % (tick[1], i + 1)) if tick else '', i + 1, html.escape(lab)) for i, (sid, lab) in enumerate(items))
    tick_attr = (' data-ticks-key="jetup-%s"' % tick[0]) if tick else ''
    return ('<nav class="jump" id="jump" aria-label="On this page"%s>'
            '<div class="jump-in">'
            '<button class="jcur" type="button" aria-expanded="false" aria-controls="jlist">'
            '<span class="jpos"><b data-jn>1</b>/%d</span><span class="jt" data-jt>%s</span>%s</button>'
            '%s</div>'
            '<i class="jbar" aria-hidden="true"></i>'
            '<ol class="jlist" id="jlist" hidden>%s</ol>'
            '</nav>') % (tick_attr, n, html.escape(items[0][1]), icon('i-chev-d'), chips, lis)

# ---------------------------------------------------------------- 3. thumb bar on phones
def thumb_bar(path, icon, group):
    def cur(p):
        return ' aria-current="page"' if path == p else ''
    return ('<nav class="thumb" aria-label="Quick links">'
            '<a class="tb" href="/jetup/"%s>%s<span>Home</span></a>'
            '<button class="tb" type="button" data-menu aria-controls="side">%s<span>Menu</span></button>'
            '<a class="tb" href="/jetup/get-started/"%s>%s<span>Start</span></a>'
            '<a class="tb tb-join" href="%s">%s<span>Join</span></a>'
            '</nav>') % (cur('/jetup/'), icon('i-home'), icon('i-menu'), cur('/jetup/get-started/'), icon('i-rocket2'), group, icon('i-whatsapp'))

# ---------------------------------------------------------------- 5. search
def search_box(icon):
    return ('<div class="sfind" role="search">'
            '<label class="sr" for="sq">Search the guide</label>'
            '<input id="sq" type="search" placeholder="Search the guide" autocomplete="off" spellcheck="false" enterkeyhint="search" '
            'aria-controls="sres" data-index="/jetup/search-index.json?v=__SIDX__">%s'
            '<button class="sclear" type="button" aria-label="Clear the search" hidden>&times;</button></div>'
            '<div class="sres" id="sres" hidden></div>') % icon('i-search')

def _text(s):
    s = re.sub(r'<(script|style|svg|button)\b.*?</\1>', ' ', s, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

def build_index(root, order):
    """Write jetup/search-index.json from the built pages, then put its version into every JetUP page."""
    entries = []
    for href, ic, name, sub in order:
        f = os.path.join(root, href.strip('/'), 'index.html')
        s = open(f, encoding='utf-8').read()
        main = s[s.find('<main'):s.find('</main>')]
        entries.append({'u': href, 'p': name, 'h': name, 't': sub})
        if href == '/jetup/glossary/':
            continue
        # sections: every element with an id that holds a heading, and every FAQ question
        for m in re.finditer(r'<(section|article|div)\b[^>]*\bid="([^"]+)"[^>]*>', main):
            sid = m.group(2)
            if sid.startswith(('fill-', 'flow-')) or sid in ('wallets',):
                continue
            chunk = main[m.end():m.end() + 9000]
            h = re.search(r'<h[23][^>]*>(.*?)</h[23]>', chunk[:2500], re.S)
            if not h:
                continue
            body = _text(chunk)[:900]
            entries.append({'u': href + '#' + sid, 'p': name, 'h': _text(h.group(1)), 't': body})
        for m in re.finditer(r'<details id="([^"]+)"[^>]*><summary>(.*?)</summary>(.*?)</details>', main, re.S):
            entries.append({'u': href + '#' + m.group(1), 'p': name, 'h': _text(m.group(2)), 't': _text(m.group(3))[:600]})
    for k, name, pat, d, more in GLOSSARY:
        entries.append({'u': '/jetup/glossary/#g-' + k, 'p': 'Glossary', 'h': name, 't': d})
    data = json.dumps(entries, ensure_ascii=False, separators=(',', ':'))
    if re.search('[\u2013\u2014]', data):
        raise SystemExit('dash found in the search index')
    out = os.path.join(root, 'jetup', 'search-index.json')
    open(out, 'w', encoding='utf-8').write(data)
    v = hashlib.md5(data.encode()).hexdigest()[:8]
    for href, *_ in order:
        f = os.path.join(root, href.strip('/'), 'index.html')
        s = open(f, encoding='utf-8').read()
        if '__SIDX__' in s:
            open(f, 'w', encoding='utf-8').write(s.replace('__SIDX__', v))
    return out, len(entries), len(data)
