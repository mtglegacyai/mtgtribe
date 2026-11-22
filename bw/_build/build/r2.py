"""Put the guide's videos on Cloudflare R2:  python3 r2.py [--check]

Every file the build made in out/_media goes to MTG's bucket bellveraffiliates-media under mtgtribe/bw/media/, served at
config.MEDIA_URL (media.bellveraffiliates.com). A file is uploaded only when it is missing online or differs (size or MD5 against
the object's ETag); afterwards every file is checked again. --check only checks. The Cloudflare API token is not in this code:
the session's network proxy adds it (it is saved on MTG's Default cloud environment, host api.cloudflare.com).
"""
import os, sys, json, hashlib, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import SCR, MEDIA_URL

API = 'https://api.cloudflare.com/client/v4'
BUCKET = 'bellveraffiliates-media'
PREFIX = 'mtgtribe/bw/media/'
SRC = SCR + '/out/_media'


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def online(name):
    """size and ETag of the public copy, or None (a HEAD on the public address, past Cloudflare's cache)"""
    r = subprocess.run(['curl', '-sI', '-H', 'Cache-Control: no-cache', MEDIA_URL + name + '?check=' + str(int(time.time()))], capture_output=True, text=True).stdout
    if not r.startswith('HTTP/') or ' 200' not in r.splitlines()[0]: return None
    hd = {l.split(':', 1)[0].lower(): l.split(':', 1)[1].strip() for l in r.splitlines()[1:] if ':' in l}
    return int(hd.get('content-length', -1)), hd.get('etag', '').strip('"')


def account():
    return json.loads(subprocess.run(['curl', '-s', API + '/accounts'], capture_output=True, text=True).stdout)['result'][0]['id']


def upload(acc, name):
    url = f'{API}/accounts/{acc}/r2/buckets/{BUCKET}/objects/{PREFIX}{name}'
    for i in range(4):
        r = subprocess.run(['curl', '-s', '-X', 'PUT', url, '-H', 'Content-Type: video/mp4', '--data-binary', '@' + SRC + '/' + name, '--max-time', '900'], capture_output=True, text=True).stdout
        if '"success":true' in r: return True
        print('  retry', i + 1, name, r[:200]); time.sleep(5 * (i + 1))
    return False


if __name__ == '__main__':
    names = sorted(f for f in os.listdir(SRC) if f.endswith('.mp4'))
    acc = None; bad = []
    for n in names:
        size, h = os.path.getsize(SRC + '/' + n), md5(SRC + '/' + n); o = online(n)
        same = o is not None and o[0] == size and o[1] == h
        if not same and '--check' not in sys.argv:
            acc = acc or account(); ok = upload(acc, n); o = online(n); same = ok and o is not None and o[0] == size and o[1] == h
            print(('UPLOADED ' if same else 'FAILED   ') + n)
        if not same: bad.append(n)
        else: print(f'OK       {n} ({size / 1e6:.1f} MB)')
    print(f'{len(names) - len(bad)} of {len(names)} videos on R2 match the build' + (f'; NOT: {bad}' if bad else ''))
    sys.exit(1 if bad else 0)
