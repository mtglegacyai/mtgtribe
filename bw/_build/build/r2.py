"""Put the guide's videos on Cloudflare R2:  python3 r2.py [--check]

Every file the build made in out/_media goes to the bucket config.R2_BUCKET under config.R2_PREFIX (since 22 Nov 2026 MTG's own
Bitcoin Wealth Cloudflare account, bucket bitcoinwealth-media, folder videos/, served at media.bitcoinwealthpays.com). A file is
uploaded only when it is missing or differs (size, or MD5 against the stored object's ETag); afterwards every file is checked again
against the bucket's own listing. --check only checks. The Cloudflare API token is not in this code: the session's network proxy
adds it (it is saved on MTG's Default cloud environment, host api.cloudflare.com, and reaches both of his Cloudflare accounts).
"""
import os, sys, json, hashlib, subprocess, time, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import SCR, R2_BUCKET, R2_PREFIX

API = 'https://api.cloudflare.com/client/v4'
SRC = SCR + '/out/_media'


def get(url):
    return json.loads(subprocess.run(['curl', '-s', url], capture_output=True, text=True).stdout)


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def account():
    """the account that holds the bucket"""
    for a in get(API + '/accounts')['result']:
        r = get(f'{API}/accounts/{a["id"]}/r2/buckets')
        if r.get('success') and any(b['name'] == R2_BUCKET for b in r['result']['buckets']): return a['id']
    sys.exit(f'bucket {R2_BUCKET} not found in any account the token reaches')


def stored(acc):
    """{file name: (size, etag)} of what is in the bucket under the prefix"""
    out, cur = {}, ''
    while True:
        r = get(f'{API}/accounts/{acc}/r2/buckets/{R2_BUCKET}/objects?prefix={urllib.parse.quote(R2_PREFIX)}&per_page=1000' + (f'&cursor={cur}' if cur else ''))
        for o in r['result']: out[o['key'][len(R2_PREFIX):]] = (o['size'], o['etag'].strip('"'))
        cur = (r.get('result_info') or {}).get('cursor')
        if not (r.get('result_info') or {}).get('is_truncated'): return out


def upload(acc, name):
    url = f'{API}/accounts/{acc}/r2/buckets/{R2_BUCKET}/objects/{R2_PREFIX}{name}'
    for i in range(4):
        r = subprocess.run(['curl', '-s', '-X', 'PUT', url, '-H', 'Content-Type: video/mp4', '--data-binary', '@' + SRC + '/' + name, '--max-time', '900'], capture_output=True, text=True).stdout
        if '"success":true' in r: return True
        print('  retry', i + 1, name, r[:200]); time.sleep(5 * (i + 1))
    return False


if __name__ == '__main__':
    names = sorted(f for f in os.listdir(SRC) if f.endswith('.mp4'))
    acc = account(); have = stored(acc); local = {n: (os.path.getsize(SRC + '/' + n), md5(SRC + '/' + n)) for n in names}
    if '--check' not in sys.argv:
        for n in names:
            if have.get(n) != local[n]: print(('UPLOADED ' if upload(acc, n) else 'FAILED   ') + n)
        have = stored(acc)
    bad = [n for n in names if have.get(n) != local[n]]
    for n in names: print(('OK       ' if n not in bad else 'DIFFERS  ') + f'{n} ({local[n][0] / 1e6:.1f} MB)')
    print(f'{len(names) - len(bad)} of {len(names)} videos in {R2_BUCKET}/{R2_PREFIX} match the build' + (f'; NOT: {bad}' if bad else ''))
    sys.exit(1 if bad else 0)
