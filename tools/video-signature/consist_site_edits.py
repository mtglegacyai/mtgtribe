# Site update for the consistency upgrade (MTG, 8 Nov 2026): every MTG video on the JetUP guide now ends, sounds and moves
# like the 9:09 sign-up training, and none shows his photo. New file names per version so caches refresh.
# Run from the repository root, on a checkout of main. Usage: python3 consist_site_edits.py
import os, re, shutil, subprocess
SP = '/tmp/claude-0/-home-user-mtgtribe/a6cc0db9-d96c-55e0-8645-be8a10935550/scratchpad'
MEDIA = {  # site file: (new source, old site file)
    'jetup-tutorial-part-1-create-account-v4.mp4': (f'{SP}/tutorial/p1/JetUP_Tutorial_Part1_Create_Account_v6_9x16.mp4', 'jetup-tutorial-part-1-create-account-v3.mp4'),
    'jetup-tutorial-part-2-link-tag-markets-v4.mp4': (f'{SP}/tutorial/p2b/JetUP_Tutorial_Part2_Link_TAG_Markets_v4_9x16.mp4', 'jetup-tutorial-part-2-link-tag-markets-v3.mp4'),
    'jetup-tutorial-part-3-verify-identity-v4.mp4': (f'{SP}/tutorial/p3b/JetUP_Tutorial_Part3_Verify_Identity_v4_9x16.mp4', 'jetup-tutorial-part-3-verify-identity-v3.mp4'),
    'jetup-explainer-the-simple-picture-v2.mp4': (f'{SP}/ex1/JetUP_Explainer_1_Simple_Picture_v2_16x9.mp4', 'jetup-explainer-the-simple-picture.mp4'),
    'jetup-tag-markets-signup-training-mtg-v4-4.mp4': (f'{SP}/consist/tr/JetUP_TAG_SignUp_Training_MTG_v4.4.mp4', 'jetup-tag-markets-signup-training-mtg.mp4'),
    'jetup-5-checks-mtg-v5-3.mp4': (f'{SP}/v5/out/JetUP_5_Checks_MTG_v5.3_web.mp4', 'jetup-5-checks-mtg-v5.mp4'),
}
for new, (src, old) in MEDIA.items():
    shutil.copy(src, f'jetup/media/{new}')
    if os.path.exists(f'jetup/media/{old}'): subprocess.run(['git', 'rm', '-q', f'jetup/media/{old}'], check=True)
# posters with the JetUP logo badge in place of MTG's face (training: its cover frame; 5 Checks: its first frame)
def poster(src_video, t, name, old):
    tmp = f'{SP}/consist/{name}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', src_video, '-frames:v', '1', '-vf', 'scale=1280:720:flags=lanczos', tmp], check=True)
    from PIL import Image
    im = Image.open(tmp).convert('RGB'); im.save(f'jetup/img/{name}.jpg', quality=88); im.save(f'jetup/img/{name}.webp', quality=82)
    for ext in ('jpg', 'webp'):
        if os.path.exists(f'jetup/img/{old}.{ext}'): subprocess.run(['git', 'rm', '-q', f'jetup/img/{old}.{ext}'], check=True)
poster(MEDIA['jetup-tag-markets-signup-training-mtg-v4-4.mp4'][0], 0.4, 'cover-signup-training-v4-4', 'cover-signup-training')
poster(MEDIA['jetup-5-checks-mtg-v5-3.mp4'][0], 0.5, 'cover-5-checks-v5-3', 'cover-5-checks-v5')
def dur(f):
    s = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'jetup/media/{f}']).decode())
    s = int(round(s)); return f'{s // 60}:{s % 60:02d}', f'PT{s // 60}M{s % 60}S' if s % 60 else f'PT{s // 60}M'
def mb(f): return round(os.path.getsize(f'jetup/media/{f}') / 1e6)
D = {k: dur(k) for k in MEDIA}
def sub(path, pairs):
    s = open(path).read()
    for a, b in pairs:
        if a not in s: raise SystemExit(f'{path}: not found: {a[:80]}')
        s = s.replace(a, b)
    open(path, 'w').write(s)
t1, t2, t3, ex, tr, c5 = (D[k] for k in MEDIA)
sub('jetup/_build/layout.py', [
    ("src='/jetup/media/jetup-tutorial-part-1-create-account-v3.mp4', poster='/jetup/img/cover-tutorial-part-1-v3.webp', jpg='/jetup/img/cover-tutorial-part-1-v3.jpg', dur='3:38', iso='PT3M38S'",
     f"src='/jetup/media/jetup-tutorial-part-1-create-account-v4.mp4', poster='/jetup/img/cover-tutorial-part-1-v3.webp', jpg='/jetup/img/cover-tutorial-part-1-v3.jpg', dur='{t1[0]}', iso='{t1[1]}'"),
    ("src='/jetup/media/jetup-tutorial-part-3-verify-identity-v3.mp4', poster='/jetup/img/cover-tutorial-part-3-v2.webp', jpg='/jetup/img/cover-tutorial-part-3-v2.jpg', dur='3:29', iso='PT3M29S'",
     f"src='/jetup/media/jetup-tutorial-part-3-verify-identity-v4.mp4', poster='/jetup/img/cover-tutorial-part-3-v2.webp', jpg='/jetup/img/cover-tutorial-part-3-v2.jpg', dur='{t3[0]}', iso='{t3[1]}'"),
    ("src='/jetup/media/jetup-tutorial-part-2-link-tag-markets-v3.mp4', poster='/jetup/img/cover-tutorial-part-2-v2.webp', jpg='/jetup/img/cover-tutorial-part-2-v2.jpg', dur='3:35', iso='PT3M35S'",
     f"src='/jetup/media/jetup-tutorial-part-2-link-tag-markets-v4.mp4', poster='/jetup/img/cover-tutorial-part-2-v2.webp', jpg='/jetup/img/cover-tutorial-part-2-v2.jpg', dur='{t2[0]}', iso='{t2[1]}'"),
    ("src='/jetup/media/jetup-explainer-the-simple-picture.mp4', poster='/jetup/img/cover-explainer-simple-picture.webp', jpg='/jetup/img/cover-explainer-simple-picture.jpg', dur='1:32', iso='PT1M32S'",
     f"src='/jetup/media/jetup-explainer-the-simple-picture-v2.mp4', poster='/jetup/img/cover-explainer-simple-picture.webp', jpg='/jetup/img/cover-explainer-simple-picture.jpg', dur='{ex[0]}', iso='{ex[1]}'"),
    ("MTG's 92-second explainer:", f"MTG's {ex[0]} explainer:"),
    ("src='/jetup/media/jetup-5-checks-mtg-v5.mp4', poster='/jetup/img/cover-5-checks-v5.webp', jpg='/jetup/img/cover-5-checks-v5.jpg', dur='5:25', iso='PT5M25S'",
     f"src='/jetup/media/jetup-5-checks-mtg-v5-3.mp4', poster='/jetup/img/cover-5-checks-v5-3.webp', jpg='/jetup/img/cover-5-checks-v5-3.jpg', dur='{c5[0]}', iso='{c5[1]}'"),
    ("src='/jetup/media/jetup-tag-markets-signup-training-mtg.mp4', poster='/jetup/img/cover-signup-training.webp', jpg='/jetup/img/cover-signup-training.jpg', dur='9:09', iso='PT9M9S'",
     f"src='/jetup/media/jetup-tag-markets-signup-training-mtg-v4-4.mp4', poster='/jetup/img/cover-signup-training-v4-4.webp', jpg='/jetup/img/cover-signup-training-v4-4.jpg', dur='{tr[0]}', iso='{tr[1]}'"),
])
sub('jetup/_build/pages_home.py', [("The simple picture, in 1:32", f"The simple picture, in {ex[0]}")])
sub('jetup/_build/pages_tools.py', [
    ("the simple picture (1:32)", f"the simple picture ({ex[0]})"),
    ("('5checks', 'JetUP 5 Checks, by MTG', '5:25 · 1080p · 82 MB', 'jetup-5-checks-mtg-v5.mp4')",
     f"('5checks', 'JetUP 5 Checks, by MTG', '{c5[0]} · 1080p · {mb('jetup-5-checks-mtg-v5-3.mp4')} MB', 'jetup-5-checks-mtg-v5-3.mp4')"),
    ("('training', 'Sign-up training, by MTG', '9:09 · 1080p · 45 MB', 'jetup-tag-markets-signup-training-mtg.mp4')",
     f"('training', 'Sign-up training, by MTG', '{tr[0]} · 1080p · {mb('jetup-tag-markets-signup-training-mtg-v4-4.mp4')} MB', 'jetup-tag-markets-signup-training-mtg-v4-4.mp4')"),
])
sub('jetup/_build/pages_start.py', [
    ('Watch MTG do part 1 (3:38)', f'Watch MTG do part 1 ({t1[0]})'), ('Watch MTG do part 2 (3:35)', f'Watch MTG do part 2 ({t2[0]})'),
    ('Watch MTG do part 3 (3:29)', f'Watch MTG do part 3 ({t3[0]})'),
])
print({k: v for k, v in D.items()})
# every other reference (share images, sitemap) follows the new names
REN = [('/jetup/img/cover-5-checks-v5.jpg', '/jetup/img/cover-5-checks-v5-3.jpg'), ('/jetup/img/cover-signup-training.jpg', '/jetup/img/cover-signup-training-v4-4.jpg'),
       ('/jetup/media/jetup-5-checks-mtg-v5.mp4', '/jetup/media/jetup-5-checks-mtg-v5-3.mp4'),
       ('/jetup/media/jetup-tag-markets-signup-training-mtg.mp4', '/jetup/media/jetup-tag-markets-signup-training-mtg-v4-4.mp4')]
for path in ('jetup/_build/layout.py', 'jetup/_build/pages_home.py', 'jetup/_build/pages_learn.py', 'jetup/_build/pages_start.py', 'sitemap-home.xml'):
    s = open(path).read(); n = 0
    for a, b in REN: n += s.count(a); s = s.replace(a, b)
    open(path, 'w').write(s); print(path, n, 'references renamed')
left = subprocess.run(['grep', '-rln', '-e', 'cover-5-checks-v5\\.', '-e', 'cover-signup-training\\.', '-e', 'signup-training-mtg\\.mp4', '-e', 'checks-mtg-v5\\.mp4',
                       '-e', 'simple-picture\\.mp4', '-e', '-v3\\.mp4', 'jetup/_build', 'sitemap-home.xml'], capture_output=True, text=True).stdout
print('old names left:', left or 'none')
