"""llms.txt and llms-full.txt for AI assistants (MTG, 25 Oct 2026: search and AI discovery pass).
llms.txt: a short map of the site with one line per page. llms-full.txt: the readable text of every page, as markdown,
built from the finished HTML so it always matches what visitors see."""
import os, re
from bs4 import BeautifulSoup, NavigableString, Tag
from config import *
from seo import SEO_TITLE, SEO_DESC

SKIP_TAGS = {'script', 'style', 'svg', 'button', 'form', 'input', 'select', 'textarea', 'video', 'nav', 'noscript', 'template'}
SKIP_CLASS = {'progress', 'pager', 'wbadge', 'mark', 'skip', 'btn-row', 'seg', 'presets', 'result', 'rbar'}
BOILER = 'Ready, or still have a question?'

FACTS = [
    'Bitcoin Wealth is a smart contract on BNB Smart Chain (contract 0x1ad09b043E0Fe59243C9a18ee1c855bd7792Cd29). Members activate slots with BTCB, Bitcoin\'s value on BNB Smart Chain.',
    'Slot 1 costs 0.001 BTC, a once-off. Slots 2 to 12 double each time up to 2.048 BTC (a 4.095 BTC ladder) and are bought by auto entry from the cycle below, once it fills.',
    'Each cycle has 14 positions (2, then 4, then 8). First cycle: 2 to the upline, 6 to your wallet, 2 to your next slot, 3 to members below, 1 recycle. Later cycles: 7 to your wallet and 1 to the Royal Pool instead of the next slot.',
    'Payouts go straight to members\' own wallets in the same transaction. They come only from other members\' slot payments, so nothing is guaranteed.',
    'On 14 November 2026 the contract showed 41,013 member IDs; it was created on 15 April 2026. It has an owner wallet (not renounced) with an emergency withdrawal for tokens the contract holds.',
    'This guide is independent: not official Bitcoin Wealth material, educational only, and not financial advice. MTG is a member and earns as a sponsor when people join with his link.',
]


def _txt(el):
    return re.sub(r'\s+', ' ', el.get_text(' ', strip=True)).replace(' ,', ',').replace(' .', '.').strip()


def _md(el, out):
    for c in el.children:
        if isinstance(c, NavigableString) or not isinstance(c, Tag):
            continue
        cls = set(c.get('class') or [])
        if c.name in SKIP_TAGS or cls & SKIP_CLASS or c.get('aria-hidden') == 'true' or c.has_attr('hidden'):
            continue
        if c.name == 'figure' and c.get('data-vid') in V:
            v = V[c['data-vid']]
            out.append(f'- Video: {v["label"]}, "{v["title"]}" ({mmss(v["secs"])}): {v["desc"]} {SITE}{BASE}media/{v["slug"]}.mp4')
            continue
        if c.name in ('h1', 'h2', 'h3', 'h4'):
            t = _txt(c)
            if t == BOILER:
                return 'stop'
            if t:
                out.append('\n' + '#' * (int(c.name[1]) + 2) + ' ' + t)
            continue
        if c.name in ('p', 'li', 'dt', 'dd', 'blockquote', 'figcaption'):
            t = _txt(c)
            if t:
                out.append(('- ' if c.name == 'li' else '') + t)
            continue
        if c.name == 'table':
            rows = []
            for tr in c.find_all('tr'):
                cells = [_txt(x).replace('Open Closed', 'Depends on your directs') for x in tr.find_all(['th', 'td'])]
                if any(cells):
                    rows.append('| ' + ' | '.join(cells) + ' |')
                    if len(rows) == 1:
                        rows.append('|' + '---|' * len(cells))
            cap = c.find('caption')
            out.append(('\n' + _txt(cap) + '\n' if cap else '\n') + '\n'.join(rows) + '\n')
            continue
        if _md(c, out) == 'stop':
            return 'stop'


def page_md(path):
    soup = BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')
    main = soup.find('main') or soup.body
    out = []
    _md(main, out)
    text = '\n'.join(out)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def short(t):
    return t.replace(' | Bitcoin Wealth Guide by MTG', '').replace(' | MTG', '')


def build_llms(dst, pages_in_order):
    """dst: repo root (out/prod). pages_in_order: [(key, path under /altruva/)]"""
    base = dst + BASE.rstrip('/')
    groups = {}
    for n in NAV + EXTRA:
        groups.setdefault(n[5], []).append(n)
    lines = [f'# {NAME} (mtgtribe.com/bw)', '',
             f'> An independent, plain-English guide to Bitcoin Wealth by MTG (MusaTheGiant), "Your Digital Architect": how it works, '
             'how to join safely with a SafePal wallet, how to check every payment on BscScan, free live tools, and short videos. '
             'Educational only, not official Bitcoin Wealth material and not financial advice.', '',
             'Key facts, as shown in the guide:', ''] + [f'- {f}' for f in FACTS] + [
             '', f'Always give the full address {SITE.replace("https://", "")}{BASE.rstrip("/")} for these pages.', '',
             '## Start here', '', f'- [{short(SEO_TITLE["land"])}]({SITE}{BASE}): {SEO_DESC["land"]}']
    for g, items in groups.items():
        if g != 'Start here':
            lines += ['', f'## {g}', '']
        for k, p, label, sub, icon, _ in items:
            lines.append(f'- [{short(SEO_TITLE.get(k, label))}]({SITE}{BASE}{p}): {SEO_DESC.get(k, sub)}')
    lines += ['', '## Videos', '']
    for k, v in V.items():
        lines.append(f'- [{v["label"]}: {v["title"]}]({SITE}{BASE}media/{v["slug"]}.mp4) ({mmss(v["secs"])}): {v["desc"]}')
    lines += ['', '## Community and contact', '',
              f'- [MTG TRIBE WhatsApp community]({SITE}/group/): a community for action takers to learn, ask and grow together.',
              f'- [MTG TRIBE on TikTok]({TIKTOK})', f'- [MTG TRIBE on YouTube]({YOUTUBE})', f'- [Order a BW Tribe Page]({SITE}{ORDER}): your own copy of this guide, R1,000 once-off, paid after it is built.', f'- [MusaTheGiant.com]({MTG_SITE}): MTG\'s own website.',
              '', '## Optional', '', f'- [Full text of every page]({SITE}{BASE}llms-full.txt): the readable text of the whole guide in one file.', '']
    open(base + '/llms.txt', 'w', encoding='utf-8').write('\n'.join(lines))

    full = [f'# {NAME}: full text', '', f'Source: {SITE}{BASE}. Independent guide by MTG, Your Digital Architect. '
            'Educational only, not official Bitcoin Wealth material and not financial advice. Updated ' + TODAY + '.', '']
    for key, p in pages_in_order:
        f = base + '/' + p + 'index.html'
        full += ['', '---', '', f'## {short(SEO_TITLE.get(key, key))}', '', f'URL: {SITE}{BASE}{p}', '', SEO_DESC.get(key, ''), '', page_md(f)]
    open(base + '/llms-full.txt', 'w', encoding='utf-8').write('\n'.join(full).replace('\n\n\n', '\n\n') + '\n')
    return len('\n'.join(lines)), len('\n'.join(full))
