"""Put the ClickBaitPays guide's videos on Cloudflare R2:  python3 cbp/_build/r2.py [--check]

Every .mp4 in MEDIA_DIR goes to the bucket clickbaitpays-media under videos/ (ClickBaitPays' own Cloudflare account, set up with
MTG on 22 Nov 2026, served at https://media.clickbaitpaysus.com/videos/, tools/cbp/CLOUDFLARE.md). A file is uploaded only when it
is missing or differs (size, or MD5 against the stored object's ETag); afterwards every file is checked again against the bucket's
own listing, and cbp/_build/media.json records each file's version (the first 8 characters of its MD5), which the builder puts
on the video's address (?v=) so a replaced video is never served from an old cache. --check only checks.

The files themselves never go into this repository (MTG's videos are made in MEDIA_DIR, outside it): for each video, a 720p file
for phones (<code>.mp4) and a 1080p file for screens 1200 px and wider (<code>-1080p.mp4). The Cloudflare API token is not in this
code: the session's network proxy adds it (saved on MTG's Default cloud environment, host api.cloudflare.com; his Bellver login
is a member of the ClickBaitPays account, so the same token reaches it).
"""
import hashlib, json, os, subprocess, sys, time, urllib.parse

API = 'https://api.cloudflare.com/client/v4'
BUCKET, PREFIX = 'clickbaitpays-media', 'videos/'
MEDIA_DIR = os.environ.get('CBP_MEDIA_DIR', '/home/user/cbp-media')
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media.json')


def get(url):
    return json.loads(subprocess.run(['curl', '-s', url], capture_output=True, text=True).stdout)


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def account():
    """the account that holds the bucket"""
    for a in get(API + '/accounts')['result']:
        r = get(f'{API}/accounts/{a["id"]}/r2/buckets')
        if r.get('success') and any(b['name'] == BUCKET for b in r['result']['buckets']):
            return a['id']
    sys.exit(f'bucket {BUCKET} not found in any account the token reaches')


def stored(acc):
    """{file name: (size, etag)} of what is in the bucket under the prefix"""
    out, cur = {}, ''
    while True:
        r = get(f'{API}/accounts/{acc}/r2/buckets/{BUCKET}/objects?prefix={urllib.parse.quote(PREFIX)}&per_page=1000' + (f'&cursor={cur}' if cur else ''))
        for o in r['result']:
            out[o['key'][len(PREFIX):]] = (o['size'], o['etag'].strip('"'))
        cur = (r.get('result_info') or {}).get('cursor')
        if not (r.get('result_info') or {}).get('is_truncated'):
            return out


def upload(acc, name):
    url = f'{API}/accounts/{acc}/r2/buckets/{BUCKET}/objects/{PREFIX}{name}'
    for i in range(4):
        r = subprocess.run(['curl', '-s', '-X', 'PUT', url, '-H', 'Content-Type: video/mp4', '--data-binary', '@' + os.path.join(MEDIA_DIR, name),
                            '--max-time', '900'], capture_output=True, text=True).stdout
        if '"success":true' in r:
            return True
        print('  retry', i + 1, name, r[:200])
        time.sleep(5 * (i + 1))
    return False


if __name__ == '__main__':
    names = sorted(f for f in os.listdir(MEDIA_DIR) if f.endswith('.mp4') and not f.startswith('_')) if os.path.isdir(MEDIA_DIR) else []
    acc = account()
    have = stored(acc)
    local = {n: (os.path.getsize(os.path.join(MEDIA_DIR, n)), md5(os.path.join(MEDIA_DIR, n))) for n in names}
    if '--check' not in sys.argv:
        for n in names:
            if have.get(n) != local[n]:
                print(('UPLOADED ' if upload(acc, n) else 'FAILED   ') + n)
        have = stored(acc)
    bad = [n for n in names if have.get(n) != local[n]]
    for n in names:
        print(('OK       ' if n not in bad else 'DIFFERS  ') + f'{n} ({local[n][0] / 1e6:.1f} MB)')
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    man.update({n: local[n][1][:8] for n in names if n not in bad})
    for n, (size, etag) in have.items():         # files already in the bucket that are not on this machine keep their version
        if n.endswith('.mp4') and not n.startswith('_') and n not in man:
            man[n] = etag[:8]
    json.dump(dict(sorted(man.items())), open(MANIFEST, 'w'), indent=1)
    print(f'{len(names) - len(bad)} of {len(names)} local videos in {BUCKET}/{PREFIX} match; versions in {os.path.relpath(MANIFEST)}' + (f'; NOT: {bad}' if bad else ''))
    sys.exit(1 if bad else 0)
