"""Assets for the mtgtribe.com home (coming soon) page: video, poster and social preview image.
python3 home/make_assets.py  ->  home/src/ (copied to /assets/ at the site root by build.py)"""
import sys, shutil
sys.path.insert(0, '/tmp/tribe'); sys.path.insert(0, '/tmp/eng')
from PIL import Image, ImageDraw, ImageFilter
import tr
from tr import TG, T, CH, emoji, glow, paste, paste_c, rrect, MG, MG_L, CREAM, MUTE, WAG, INK, CHAR
OUT = '/home/claude/site/home/src/'
# the approved MTG TRIBE invite (v2), web copy: 720x1280, opens on its cover
shutil.copy('/home/claude/outputs/tribe/MTG_TRIBE_Invite_v2_share.mp4', OUT + 'mtg-tribe-invite.mp4')
cov = Image.open('/tmp/tribe/cover.png').convert('RGB')
cov.resize((720, 1280), Image.LANCZOS).save(OUT + 'mtg-tribe-invite-cover.webp', quality=86)

# social preview 1200x630: blueprint night, crown, MTG TRIBE, coming soon, phone with the invite cover
W, H = 1200, 630
import numpy as np
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
bg = np.zeros((H, W, 3), np.float32)
for i, (a, b) in enumerate(zip((12, 11, 9), (4, 4, 6))):
    bg[..., i] = a * (1 - yy / H) + b * (yy / H)
d = np.sqrt((xx - 260) ** 2 + (yy - 120) ** 2) / 700
bg += (np.clip(1 - d, 0, 1) ** 2 * 0.35)[..., None] * np.array(MG, np.float32)
grid = ((xx % 40 < 1.2) | (yy % 40 < 1.2)).astype(np.float32) * 10
bg += grid[..., None] * np.array([0.95, 0.75, 0.35])
im = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert('RGBA')
ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))


def tight(img):
    bb = img.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox()
    return img.crop(bb) if bb else img


def put(img, x, y):
    t = tight(img); paste(ov, t, x, y); return t


cr = put(emoji('👑', 48), 64, 54)
put(TG('MTG TRIBE', 34, 'orb8', g=0.5, tracking=4), 64 + cr.width + 14, 54 + (cr.height - 26) / 2)
pl = put(CH('COMING SOON', 'hammer', MG, 24, 400), 64, 132)
put(T('A new home for', 58, CREAM, 'orb8', tracking=1), 64, 222)
put(TG('the MTG TRIBE', 60, 'orb8', tracking=1), 64, 300)
put(T('Tutorials, explainers, free tools and honest', 26, MUTE, 'mon7'), 66, 398)
put(T('guides by MTG, Your Digital Architect.', 26, MUTE, 'mon7'), 66, 434)
site = put(T('mtgtribe.com', 30, MG, 'mon8'), 66, 540)
put(CH('Join: mtgtribe.com/group', 'whatsapp', WAG, 24, 460), 66 + site.width + 24, 528)
im.alpha_composite(ov)
# phone with the cover
ph_w, ph_h = 270, 480
scr = cov.resize((ph_w - 20, ph_h - 20), Image.LANCZOS)
frame = rrect((ph_w, ph_h), 36, (16, 16, 20, 255), outline=MG + (255,), width=3)
m = Image.new('L', scr.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, scr.width - 1, scr.height - 1], 28, fill=255)
frame.paste(scr, (10, 10), m)
g, _ = glow(frame, 26, MG, 0.55) if isinstance(glow(frame, 26, MG, 0.55), tuple) else (glow(frame, 26, MG, 0.55), None)
paste_c(im, g, 960, 315)
im.convert('RGB').save(OUT + 'og-home.jpg', quality=88, optimize=True)
print('assets ok', Image.open(OUT + 'og-home.jpg').size)

# crown favicons on the night background
for n, fn in ((32, 'favicon-32.png'), (180, 'apple-touch-icon.png'), (512, 'icon-512.png')):
    bgc = Image.new('RGBA', (n, n), (10, 10, 13, 255))
    e = emoji('👑', int(n * 0.74))
    e = tight(e) if 'tight' in globals() else e
    e.thumbnail((int(n * 0.8), int(n * 0.8)), Image.LANCZOS)
    bgc.alpha_composite(e, ((n - e.width) // 2, (n - e.height) // 2))
    if n >= 180:
        m = Image.new('L', (n, n), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, n - 1, n - 1], int(n * 0.22), fill=255)
        out = Image.new('RGBA', (n, n), (0, 0, 0, 0)); out.paste(bgc, (0, 0), m); bgc = out
    bgc.save(OUT + fn, optimize=True)
print('icons ok')

# header avatar (MTG's profile photo from musathegiant.com, images/mtg-profile.jpg), 96 px for a 38 px circle at 2x
_av = Image.open('/home/claude/mtglegacyai/musathegiant/images/mtg-profile.jpg').convert('RGB')
_av.resize((96, 96), Image.LANCZOS).save(OUT + 'mtg-avatar.webp', quality=88)
