"""YouTube research for MTG's videos: the most watched videos and Shorts on a topic, with real numbers.

Reads YouTube's public search page (and, with --details, each video's page) and prints a table you can paste into a
research brief: title, channel, views, age, length, rough views per month and link. Light use only: a few searches per
video, never bulk downloading. Python 3 standard library, no API key.

Usage:
    python3 yt_research.py "zimbabwe hyperinflation"                 most viewed first (default)
    python3 yt_research.py "did you know bitcoin" --sort relevance --limit 15
    python3 yt_research.py "yap stone money" --details               adds exact views, upload date, keywords
    python3 yt_research.py "bitcoin pizza" --json out.json            also saves the raw rows
Sort: views (default), relevance, date.

Numbers are YouTube's public counts on the day you run it; write the research date in the brief.
"""
import argparse
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
SORT = {'views': 'CAM%3D', 'date': 'CAI%3D', 'relevance': None}


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'en-US,en;q=0.9'})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return r.read().decode('utf-8', 'replace')


def initial_json(html, var):
    m = re.search(r'(?:var |window\["?)' + re.escape(var) + r'"?\]?\s*=\s*(\{.*?\});\s*(?:var |</script>)', html, re.S)
    return json.loads(m.group(1)) if m else {}


def walk(node, key):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == key:
                yield v
            yield from walk(v, key)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v, key)


def text(t):
    if not t:
        return ''
    if 'simpleText' in t:
        return t['simpleText']
    return ''.join(r.get('text', '') for r in t.get('runs', []))


def parse_count(s):
    """'9,835,611 views' -> 9835611; '1.2M views' -> 1200000."""
    if not s:
        return None
    s = s.replace(',', '').lower()
    m = re.search(r'([\d.]+)\s*([kmb]?)', s)
    if not m:
        return None
    n = float(m.group(1)) * {'': 1, 'k': 1e3, 'm': 1e6, 'b': 1e9}[m.group(2)]
    return int(n)


def months_ago(s):
    """'3 years ago' or '3y ago' -> 36; '5mo ago' -> 5; '2w ago' -> 0.5."""
    m = re.search(r'(\d+)\s*(years?|y|months?|mo|weeks?|w|days?|d|hours?|h)\b', s or '')
    if not m:
        return None
    n, unit = int(m.group(1)), m.group(2)
    unit = {'y': 'year', 'mo': 'month', 'w': 'week', 'd': 'day', 'h': 'hour'}.get(unit, unit.rstrip('s'))
    return max(n * {'hour': 1 / 720, 'day': 1 / 30, 'week': 0.25, 'month': 1, 'year': 12}[unit], 0.25)


def search(query, sort):
    url = 'https://www.youtube.com/results?search_query=' + urllib.parse.quote_plus(query)
    if SORT.get(sort):
        url += '&sp=' + SORT[sort]
    data = initial_json(fetch(url), 'ytInitialData')
    rows, seen = [], set()
    for v in walk(data, 'videoRenderer'):
        vid = v.get('videoId')
        if not vid or vid in seen:
            continue
        seen.add(vid)
        rows.append({
            'type': 'video', 'id': vid, 'title': text(v.get('title')),
            'channel': text(v.get('ownerText')) or text(v.get('longBylineText')),
            'views_text': text(v.get('viewCountText')), 'age': text(v.get('publishedTimeText')),
            'length': text(v.get('lengthText')), 'url': f'https://www.youtube.com/watch?v={vid}',
        })
    for s in walk(data, 'shortsLockupViewModel'):
        try:
            vid = s['onTap']['innertubeCommand']['reelWatchEndpoint']['videoId']
        except (KeyError, TypeError):
            continue
        if vid in seen:
            continue
        seen.add(vid)
        meta = s.get('overlayMetadata', {})
        rows.append({
            'type': 'short', 'id': vid, 'title': meta.get('primaryText', {}).get('content', ''), 'channel': '',
            'views_text': meta.get('secondaryText', {}).get('content', ''), 'age': '', 'length': '',
            'url': f'https://www.youtube.com/shorts/{vid}',
        })
    for r in rows:
        r['views'] = parse_count(r['views_text'])
        mo = months_ago(r['age'])
        r['views_per_month'] = int(r['views'] / mo) if r['views'] and mo else None
    return rows


def details(row):
    html = fetch(row['url'].replace('/shorts/', '/watch?v=') if '/shorts/' in row['url'] else row['url'])
    p = initial_json(html, 'ytInitialPlayerResponse')
    vd, mf = p.get('videoDetails', {}), p.get('microformat', {}).get('playerMicroformatRenderer', {})
    row.update({
        'views': int(vd['viewCount']) if vd.get('viewCount') else row.get('views'),
        'channel': row['channel'] or vd.get('author', ''),
        'length_s': int(vd['lengthSeconds']) if vd.get('lengthSeconds') else None,
        'published': mf.get('publishDate', ''),
        'keywords': vd.get('keywords', [])[:15],
        'description_start': (vd.get('shortDescription') or '')[:300],
    })
    return row


def fmt(n):
    if n is None:
        return '?'
    return f'{n / 1e6:.1f}M' if n >= 1e6 else f'{n / 1e3:.0f}K' if n >= 1e3 else str(n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('query')
    ap.add_argument('--sort', choices=list(SORT), default='views')
    ap.add_argument('--limit', type=int, default=12)
    ap.add_argument('--details', action='store_true')
    ap.add_argument('--json')
    a = ap.parse_args()
    try:
        rows = search(a.query, a.sort)
        if not rows:
            sys.exit('YouTube returned no results (the page may have changed or requests are limited). Do not guess numbers.')
    except Exception as e:  # network or page change: say so plainly, never guess numbers
        sys.exit(f'Could not read YouTube search ({e}). Use web search and links MTG supplies instead.')
    if a.sort == 'views':
        rows.sort(key=lambda r: r['views'] or 0, reverse=True)
    rows = rows[:a.limit]
    if a.details:
        for r in rows:
            time.sleep(1.5)  # be gentle: one page at a time
            try:
                details(r)
            except Exception as e:
                r['details_error'] = str(e)
                if '429' in str(e):
                    print('Note: YouTube is limiting requests (429), so exact details were skipped; the search numbers stand.\n')
                    break
    print(f'YouTube search: "{a.query}" (sorted by {a.sort})\n')
    print('| # | Type | Title | Channel | Views | Age | Length | Views per month | Link |')
    print('|---|---|---|---|---|---|---|---|---|')
    for i, r in enumerate(rows, 1):
        title = r['title'].replace('|', '/')[:80]
        print(f"| {i} | {r['type']} | {title} | {r['channel']} | {fmt(r['views'])} | {r.get('published') or r['age']} | "
              f"{r['length']} | {fmt(r['views_per_month'])} | {r['url']} |")
    if a.details:
        for i, r in enumerate(rows, 1):
            if r.get('keywords'):
                print(f"\n{i}. keywords: {', '.join(r['keywords'])}")
    if a.json:
        with open(a.json, 'w') as f:
            json.dump(rows, f, indent=1)


if __name__ == '__main__':
    main()
