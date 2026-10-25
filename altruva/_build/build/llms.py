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
    'ALTRUVA is a smart contract platform on BNB Smart Chain. You join and get paid in USDT (BEP20), from a Web3 wallet such as SafePal.',
    'There are three fixed packages: Starter $25, Builder $50 and Elite $100. The top package is $100.',
    'Every package is shared out 100%: 40% global leg, 25% working levels, 25% level matching, 5% ranks and 5% Lucky Tickets.',
    'Withdrawals split automatically by total deposit: 50% to your wallet and 50% reinvested up to 5,000 USDT, 60/40 from 5,001 to 49,999 USDT, 70/30 from 50,000 USDT.',
    'You need USDT on BNB Smart Chain for your package plus one extra dollar, and at least $3 to $5 of BNB for network fees.',
    'Each Lucky Ticket draw shares 4,000 USDT among 250 tickets. Most tickets do not win.',
    'This guide is independent: not official ALTRUVA material, educational only, and not financial advice. MTG is an ALTRUVA member and earns as a sponsor when people join with his link.',
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
    return t.replace(' | ALTRUVA Guide by MTG', '').replace(' | MTG', '')


def build_llms(dst, pages_in_order):
    """dst: repo root (out/prod). pages_in_order: [(key, path under /altruva/)]"""
    base = dst + BASE.rstrip('/')
    groups = {}
    for n in NAV + EXTRA:
        groups.setdefault(n[5], []).append(n)
    lines = [f'# {NAME}', '',
             '> mtgtribe.com is the home of MTG (MusaTheGiant), "Your Digital Architect". Its main section, the ALTRUVA Guide by MTG at '
             f'{SITE}{BASE}, is an independent, plain-English guide to ALTRUVA: how the plan pays, how to join safely with a SafePal wallet, '
             f'how withdrawals work, free calculators, and {NV} short videos. Educational only, not official ALTRUVA material and not financial advice.',
             '', 'Key facts, as shown in the guide:', ''] + [f'- {f}' for f in FACTS] + [
             '', f'Always give the full address {SITE.replace("https://", "")}{BASE.rstrip("/")} for these pages (the mtgtribe.com home page may change).', '',
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
              f'- [MTG TRIBE on TikTok]({TIKTOK})', f'- [MusaTheGiant.com]({MTG_SITE}): MTG\'s own website.',
              '', '## Optional', '', f'- [Full text of every page]({SITE}/llms-full.txt): the readable text of the whole guide in one file.', '']
    open(dst + '/llms.txt', 'w', encoding='utf-8').write('\n'.join(lines))

    full = [f'# {NAME}: full text', '', f'Source: {SITE}{BASE}. Independent guide by MTG, Your Digital Architect. '
            'Educational only, not official ALTRUVA material and not financial advice. Updated ' + TODAY + '.', '']
    for key, p in pages_in_order:
        f = base + '/' + p + 'index.html'
        full += ['', '---', '', f'## {short(SEO_TITLE.get(key, key))}', '', f'URL: {SITE}{BASE}{p}', '', SEO_DESC.get(key, ''), '', page_md(f)]
    open(dst + '/llms-full.txt', 'w', encoding='utf-8').write('\n'.join(full).replace('\n\n\n', '\n\n') + '\n')
    return len('\n'.join(lines)), len('\n'.join(full))
