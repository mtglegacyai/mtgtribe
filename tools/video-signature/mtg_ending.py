# MTG's signature ending, the same one the 9:09 JetUP + TAG Markets sign-up training plays (MTG, 8 Nov 2026: "the best
# transitions, sound effects, animations, and my favourite line: We learn best when we teach others").
# Drawing helpers, easing, timings, scene order and sound effects are copied 1:1 from that training's engine
# (jetup-work/engine/tutorial/render_tut2.py), with two changes MTG asked for: the JetUP logo disc takes the place of his
# photo, and the layout also comes in 9:16 for the vertical tutorials.
#
# Scenes (each starts on its spoken cue, fades 0.35 s): links (+ fair-play sign-up), help someone start right
# (save / share), WE LEARN BEST WHEN WE TEACH OTHERS, IT PAYS TO PAY ATTENTION & TAKE ACTION, not financial advice,
# THANK YOU (like / share / comment), MASSIVE ACTION, YOU ARE THE BEST, Crypto-Regards signature, end card.
# Sound effects (synthesised): whoosh on every scene change, tick on list items, pop on engagement, click on taps.
import io, math, functools
import numpy as np, cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FD = '/usr/share/fonts/truetype/google-fonts/'
GV = '/home/claude/assets/fonts/GreatVibes-Regular.ttf'
ICONS = '/home/claude/assets/package/icons/'
EMOJI_FONT = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
LOGO = '/home/user/mtgtribe/tools/jetup-tutorial/jetup-disc.png'
lru = functools.lru_cache(maxsize=None)

PURPLE, PINK, LIME, ORANGE, TEAL = (140, 108, 231), (227, 113, 252), (203, 251, 97), (248, 115, 5), (4, 174, 146)
WHITE, GREY, ICE = (247, 246, 252), (170, 165, 190), (226, 220, 248)
GOLD, GOLD_L, GOLD_D = (232, 194, 90), (250, 228, 150), (196, 142, 44)
DARK = (15, 12, 25)

# ------------------------------------------------------------------ easing (from the ALTRUVA engine)
def ease_out(x): x = min(max(x, 0.0), 1.0); return 1 - (1 - x) ** 3
def ease_back(x):
    x = min(max(x, 0.0), 1.0); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def smooth(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def env(t, t0, t1, fin=0.3, fout=0.25):
    if t < t0 or t > t1: return 0.0, 0.0
    a_in = ease_out((t - t0) / fin) if fin > 0 else 1
    a_out = ease_out((t1 - t) / fout) if fout > 0 else 1
    return min(a_in, a_out), ease_back((t - t0) / (fin * 1.4)) if fin > 0 else 1
def pulse(t, t0, amp=0.08, dur=0.35): return 1 + amp * max(0.0, 1 - (t - t0) / dur) if t >= t0 else 1

# ------------------------------------------------------------------ drawing helpers (verbatim from the training engine)
@lru
def fnt(kind, size):
    if kind == 'sig': return ImageFont.truetype(GV, size)
    return ImageFont.truetype(FD + {'b': 'Poppins-Bold.ttf', 'sb': 'Poppins-SemiBold.ttf', 'm': 'Poppins-Medium.ttf',
                                    'r': 'Poppins-Regular.ttf'}.get(kind, 'Poppins-Bold.ttf'), size)

@lru
def icon(name, size, color=WHITE, sw=2.0, fill=None):
    s = open(ICONS + name + '.svg').read().replace('currentColor', '#%02x%02x%02x' % color).replace('stroke-width="2"', f'stroke-width="{sw}"')
    if fill is not None: s = s.replace('fill="none"', 'fill="#%02x%02x%02x"' % fill)
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(), output_width=size, output_height=size))).convert('RGBA')

@lru
def emo(ch, size):
    f = ImageFont.truetype(EMOJI_FONT, 109)
    im = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((size, int(size * im.height / im.width)), Image.LANCZOS)

@lru
def T(txt, size, col=WHITE, kind='b'):
    f = fnt(kind, size); bb = f.getbbox(txt)
    im = Image.new('RGBA', (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1]), txt, font=f, fill=col)
    return im

def glow(im, r=14, col=None, k=0.6):
    pad = r * 3; big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    solid = Image.new('RGBA', im.size, (col or (255, 255, 255)) + (255,)); solid.putalpha(im.getchannel('A'))
    big.paste(solid, (pad, pad), solid); g = big.filter(ImageFilter.GaussianBlur(r))
    ga = np.array(g.getchannel('A'), np.float32) * k; g.putalpha(Image.fromarray(np.clip(ga, 0, 255).astype(np.uint8)))
    o = Image.new('RGBA', big.size, (0, 0, 0, 0)); o.paste(im, (pad, pad), im); g.alpha_composite(o)
    return g

@lru
def G(txt, size, c1, c2, kind='b', glow_col=None, gr=14, gk=0.55):
    m = T(txt, size, (255, 255, 255), kind); w, h = m.size
    g = np.zeros((h, w, 3), np.float32)
    for i in range(3): g[:, :, i] = np.linspace(c1[i], c2[i], w)[None, :]
    out = Image.fromarray(g.astype(np.uint8)).convert('RGBA'); out.putalpha(m.getchannel('A'))
    return glow(out, gr, glow_col, gk) if glow_col else out

def rrect(size, r, fill, outline=None, width=0):
    im = Image.new('RGBA', size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=fill, outline=outline, width=width)
    return im

@lru
def ring_icon(name, d, col, emoji_ch=None):
    im = Image.new('RGBA', (d, d), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    dr.ellipse([0, 0, d - 1, d - 1], fill=(26, 20, 44, 255), outline=col + (255,), width=max(3, d // 28))
    ic = icon(name, int(d * 0.5), col, 2.2); im.alpha_composite(ic, ((d - ic.width) // 2, (d - ic.height) // 2))
    g = glow(im, max(8, d // 10), col, 0.55)
    if emoji_ch:
        e = emo(emoji_ch, int(d * 0.36)); g.alpha_composite(e, (g.width - e.width - int(d * 0.12), int(d * 0.12)))
    return g

@lru
def chip(txt, ic=None, col=LIME, size=32, emoji_ch=None, fill=(26, 20, 44, 240), tcol=WHITE):
    f = fnt('sb', size); tw = int(f.getlength(txt)); iw = int(size * 1.25) if (ic or emoji_ch) else 0
    h = int(size * 1.9); w = tw + 56 + (iw + 14 if iw else 0)
    im = rrect((w, h), h // 2, fill, outline=col + (255,), width=3); d = ImageDraw.Draw(im); x = 28
    if emoji_ch: e = emo(emoji_ch, iw); im.alpha_composite(e, (x, (h - e.height) // 2)); x += iw + 14
    elif ic: e = icon(ic, iw, col, 2.3); im.alpha_composite(e, (x, (h - iw) // 2)); x += iw + 14
    d.text((x, h / 2), txt, font=f, fill=tcol, anchor='lm')
    return im

@lru
def url_pill(url, size, bg=LIME, fg=DARK, glow_col=LIME):
    f = fnt('b', size); tw = int(f.getlength(url)); h = int(size * 1.55); w = tw + int(size * 1.1)
    im = rrect((w, h), h // 2, bg + (255,)); ImageDraw.Draw(im).text((w / 2, h / 2), url, font=f, fill=fg, anchor='mm')
    return glow(im, 22, glow_col, 0.6)

PLAT = {'tiktok': ('TikTok', '@joinmtgtribe', '🎵', (37, 244, 238)), 'youtube': ('YouTube', '@mtgtribe', '▶️', (255, 48, 48)),
        'whatsapp': ('WhatsApp', 'mtgtribe.com/group', '💬', (37, 211, 102)), 'telegram': ('Telegram', '@mtgtribe', '✈️', (34, 158, 217)),
        'facebook': ('Facebook', 'facebook.com/mtgtribe', '📘', (24, 119, 242))}

@lru
def plat_badge(key, w=760, h=84):
    name, handle, e, col = PLAT[key]
    im = rrect((w, h), h // 2, (24, 20, 38, 245), outline=col + (255,), width=3); d = ImageDraw.Draw(im)
    d.ellipse([10, 10, h - 10, h - 10], fill=tuple(int(c * 0.35) for c in col) + (255,), outline=col + (255,), width=3)
    em = emo(e, int(h * 0.46)); im.alpha_composite(em, (h // 2 - em.width // 2, h // 2 - em.height // 2))
    d.text((h + 14, h / 2), name, font=fnt('b', 32), fill=WHITE, anchor='lm')
    d.text((h + 14 + fnt('b', 32).getlength(name) + 18, h / 2 + 1), handle, font=fnt('m', 30), fill=col if key != 'tiktok' else ICE, anchor='lm')
    return im

@lru
def logo_card(size):
    """The JetUP logo disc in MTG's approved circle card (gold gradient ring, soft gold glow): replaces his photo card."""
    ring = max(4, size // 55); pad = max(14, size // 9); S = size + 2 * ring + 2 * pad
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0)); g = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([pad - 4, pad - 4, S - pad + 3, S - pad + 3], fill=(232, 194, 90, 170))
    out.alpha_composite(g.filter(ImageFilter.GaussianBlur(pad * 0.55)))
    K = 3; SS = S * K
    m = Image.new('L', (SS, SS), 0); ImageDraw.Draw(m).ellipse([pad * K, pad * K, SS - pad * K - 1, SS - pad * K - 1], fill=255)
    m = m.resize((S, S), Image.LANCZOS)
    grad = np.zeros((S, S, 4), np.uint8); tt = np.linspace(0, 1, S)[:, None] * 0.6 + np.linspace(0, 1, S)[None, :] * 0.4
    for i in range(3): grad[..., i] = (GOLD_L[i] * (1 - tt) + GOLD_D[i] * tt).astype(np.uint8)
    grad[..., 3] = np.array(m); out.alpha_composite(Image.fromarray(grad))
    D = size * K; src = Image.open(LOGO).convert('RGBA').resize((D, D), Image.LANCZOS)
    pm = Image.new('L', (D, D), 0); ImageDraw.Draw(pm).ellipse([0, 0, D - 1, D - 1], fill=255)
    src.putalpha(Image.fromarray(np.minimum(np.array(src.getchannel('A')), np.array(pm))))
    out.alpha_composite(src.resize((size, size), Image.LANCZOS), (pad + ring, pad + ring))
    return out

def paste(ov, im, x, y, a=1.0):
    if a <= 0.003: return
    if a < 1:
        im = im.copy(); im.putalpha(Image.fromarray((np.array(im.getchannel('A'), np.float32) * a).astype(np.uint8)))
    x, y = int(round(x)), int(round(y))
    if 0 <= x and 0 <= y and x + im.width <= ov.width and y + im.height <= ov.height: ov.alpha_composite(im, (x, y))
    else:
        tmp = Image.new('RGBA', ov.size, (0, 0, 0, 0)); tmp.paste(im, (x, y), im); ov.alpha_composite(tmp)

def paste_c(ov, im, cx, cy, a=1.0, s=1.0):
    if a <= 0.003: return
    if abs(s - 1) > 1e-3 and s > 0: im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
    paste(ov, im, cx - im.width / 2, cy - im.height / 2, a)

def burst(ov, cx, cy, t, t0, cols, n=12, r1=160, dur=0.65, rx=50, ry=None):
    """particles fly out from an ellipse (rx, ry) around the element, so they never cross its text"""
    u = (t - t0) / dur
    if not 0 <= u <= 1: return
    ry = rx if ry is None else ry; gx = int(rx + r1 + 40); gy = int(ry + r1 * 0.6 + 40)
    lay = Image.new('RGBA', (2 * gx, 2 * gy), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(n):
        ang = 2 * math.pi * k / n + 0.3; g = r1 * ease_out(u); rad = 9 * (1 - u) + 2
        x, y = gx + (rx + g) * math.cos(ang), gy + (ry + g * 0.6) * math.sin(ang); col = cols[k % len(cols)]
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=col + (int(255 * (1 - u)),))
    paste(ov, lay, cx - gx, cy - gy)

# ------------------------------------------------------------------ the ending
class Ending:
    """cues: absolute times (s) of the spoken words, see cue_names(). orient 'h' (1920x1080) or 'v' (1080x1920).
    nxt: the end card's "what to watch next" chip text. links: True when the "Everything I showed you" line is spoken."""
    def __init__(self, cues, orient='h', nxt=None, links=True):
        self.c, self.o, self.nxt, self.links = dict(cues), orient, nxt, links
        self.W, self.H = (1920, 1080) if orient == 'h' else (1080, 1920)
        self.CX = self.W // 2
        c = self.c
        self.SC = [(c['T_LINKS'], c['T_ENG'] + 0.3, self.links_scene), (c['T_ENG'], c['T_WE'] + 0.3, self.engage),
                   (c['T_WE'], c['T_SLOG'] + 0.3, self.we_learn), (c['T_SLOG'], c['T_OUT'] + 0.3, self.slogan),
                   (c['T_OUT'], c['END_CARD'] + 0.25, self.outro), (c['END_CARD'], 1e9, self.end_card)]
        self.start = c['T_LINKS']

    def overlay(self, t):
        ov = Image.new('RGBA', (self.W, self.H), (0, 0, 0, 0))
        for t0, t1, fn in self.SC:
            if t0 <= t < t1: fn(ov, t)
        return ov

    def header(self, ov, txt, t, t0, t1, y, c1=PURPLE, c2=PINK, size=64):
        a, p = env(t, t0, t1, 0.4, 0.3); paste_c(ov, G(txt, size, c1, c2, 'b', c2, 14, 0.5), self.CX, y + (1 - p) * 20, a)

    # ---- everything I showed you + my links, then the fair-play sign-up line (invited by someone else? use their link)
    def links_scene(self, ov, t):
        c, CX, v = self.c, self.CX, self.o == 'v'
        T0, T1 = c['T_LINKS'], c['T_ENG'] + 0.3; a0, _ = env(t, T0, T1, 0.35, 0.35)
        if a0 <= 0: return
        TF = c['T_FAIR']; mv = smooth((t - TF) / 0.5) if self.links else 1.0
        if self.links:
            ak, _ = env(t, T0 + 0.05, TF + 0.4, 0.35, 0.35)
            paste_c(ov, T('EVERYTHING I SHOWED YOU + MY LINKS', 34 if not v else 38, LIME), CX, 230 if not v else 560, ak * a0)
            tj = c['t_url'] - 0.1; aj, pj = env(t, tj, T1, 0.25, 0.3)
        else:
            tj = TF + 0.05; aj, pj = env(t, tj, T1, 0.25, 0.3)
        y0, y1 = (400, 175) if not v else (760, 330)
        s0, s1 = (104, 0.58) if not v else (84, 0.72)
        paste_c(ov, url_pill('mtgtribe.com/jetup', s0), CX, y0 + (y1 - y0) * mv, aj * a0, (1.18 - 0.18 * pj if mv < 1 else 1) * (1 - (1 - s1) * mv))
        af, pf = env(t, TF + 0.15, T1, 0.35, 0.3)
        if af <= 0: return
        if not v:
            paste_c(ov, ring_icon('users', 150, LIME, '🤝'), 470, 440, af * a0, 0.85 + 0.15 * pf)
            paste_c(ov, T('Invited by someone else?', 64), CX + 120, 380, af * a0)
            au, pu = env(t, c['t_their'] - 0.05, T1, 0.3, 0.3)
            paste_c(ov, chip('Use their link', None, LIME, 44, '🔗'), CX + 120, 500, au * a0, 0.9 + 0.1 * pu)
            ae, pe = env(t, c['t_every'] - 0.05, T1, 0.3, 0.3)
            paste_c(ov, G('THIS VIDEO IS FOR EVERY TEAM', 74, GOLD_L, GOLD_D, 'b', GOLD, 16, 0.55), CX, 680, ae * a0, 1.15 - 0.15 * pe)
            asf, psf = env(t, c['t_free'] - 0.05, T1, 0.3, 0.3)
            paste_c(ov, chip('Feel free to share it', None, PINK, 44, '📤'), CX, 820, asf * a0, 0.7 + 0.3 * psf)
            burst(ov, CX, 820, t, c['t_free'], [PINK, LIME, WHITE], 14, 120, 0.65, 300, 50)
        else:
            paste_c(ov, ring_icon('users', 170, LIME, '🤝'), CX, 560, af * a0, 0.85 + 0.15 * pf)
            paste_c(ov, T('Invited by', 66), CX, 730, af * a0); paste_c(ov, T('someone else?', 66), CX, 815, af * a0)
            au, pu = env(t, c['t_their'] - 0.05, T1, 0.3, 0.3)
            paste_c(ov, chip('Use their link', None, LIME, 46, '🔗'), CX, 945, au * a0, 0.9 + 0.1 * pu)
            ae, pe = env(t, c['t_every'] - 0.05, T1, 0.3, 0.3)
            paste_c(ov, G('THIS VIDEO IS', 84, GOLD_L, GOLD_D, 'b', GOLD, 16, 0.55), CX, 1130, ae * a0, 1.15 - 0.15 * pe)
            paste_c(ov, G('FOR EVERY TEAM', 84, GOLD_L, GOLD_D, 'b', GOLD, 16, 0.55), CX, 1240, ae * a0, 1.15 - 0.15 * pe)
            asf, psf = env(t, c['t_free'] - 0.05, T1, 0.3, 0.3)
            paste_c(ov, chip('Feel free to share it', None, PINK, 46, '📤'), CX, 1400, asf * a0, 0.7 + 0.3 * psf)
            burst(ov, CX, 1400, t, c['t_free'], [PINK, LIME, WHITE], 14, 120, 0.65, 260, 50)

    # ---- save / share (the training's "HELP SOMEONE START RIGHT")
    def engage(self, ov, t):
        c, CX, v = self.c, self.CX, self.o == 'v'
        T1 = c['T_WE'] + 0.3; a0, _ = env(t, c['T_ENG'], T1, 0.35, 0.35)
        if a0 <= 0: return
        if not v: self.header(ov, 'HELP SOMEONE START RIGHT', t, c['T_ENG'] + 0.05, T1, 175)
        else:
            self.header(ov, 'HELP SOMEONE', t, c['T_ENG'] + 0.05, T1, 330, size=76)
            self.header(ov, 'START RIGHT', t, c['T_ENG'] + 0.05, T1, 425, size=76)
        items = [('bookmark', '🔖', 'SAVE', "so it's here when you need it", GOLD, c['t_save'], c['t_soits']),
                 ('share-2', '📤', 'SHARE', "with someone who's ready to start", PINK, c['t_share'], c['t_ready'])]
        for k, (ic, e, lab, sub, col, tt, ts) in enumerate(items):
            x, y = (CX + (k - 0.5) * 560, 470) if not v else (CX, 700 + k * 520)
            if t < tt:
                paste_c(ov, ring_icon(ic, 210 if not v else 230, (80, 70, 110)), x, y, a0 * 0.55); continue
            ak, pk = env(t, tt - 0.05, T1, 0.2, 0.3)
            paste_c(ov, ring_icon(ic, 210 if not v else 230, col, e), x, y, ak * a0, (0.5 + 0.5 * pk) * pulse(t, tt + 0.25, 0.06))
            burst(ov, x, y, t, tt, [col, WHITE, LIME], 14, 170)
            paste_c(ov, T(lab, 54 if not v else 60, col), x, y + (170 if not v else 185), ak * a0)
            a2, _ = env(t, ts - 0.05, T1, 0.3, 0.3); paste_c(ov, T(sub, 30 if not v else 36, ICE, 'm'), x, y + (232 if not v else 255), a2 * a0)

    # ---- MTG's favourite line
    def we_learn(self, ov, t):
        c, CX, v = self.c, self.CX, self.o == 'v'
        T1 = c['T_SLOG'] + 0.3; a0, _ = env(t, c['T_WE'], T1, 0.35, 0.35)
        if a0 <= 0: return
        a1, p1 = env(t, c['T_WE'] + 0.05, T1, 0.4, 0.3)
        a2, p2 = env(t, c['t_teach'] - 0.05, T1, 0.35, 0.3)
        if not v:
            paste_c(ov, ring_icon('users', 180, GOLD, '🤝'), CX, 300, a1 * a0, 0.85 + 0.15 * p1)
            paste_c(ov, G('WE LEARN BEST', 92, WHITE, ICE, 'b', PURPLE, 16, 0.6), CX, 500, a1 * a0, 1.15 - 0.15 * p1)
            paste_c(ov, G('WHEN WE TEACH OTHERS', 92, GOLD_L, GOLD_D, 'b', GOLD, 18, 0.6), CX, 630, a2 * a0, 1.15 - 0.15 * p2)
        else:
            paste_c(ov, ring_icon('users', 200, GOLD, '🤝'), CX, 560, a1 * a0, 0.85 + 0.15 * p1)
            paste_c(ov, G('WE LEARN BEST', 96, WHITE, ICE, 'b', PURPLE, 16, 0.6), CX, 800, a1 * a0, 1.15 - 0.15 * p1)
            paste_c(ov, G('WHEN WE TEACH', 96, GOLD_L, GOLD_D, 'b', GOLD, 18, 0.6), CX, 960, a2 * a0, 1.15 - 0.15 * p2)
            paste_c(ov, G('OTHERS', 120, GOLD_L, GOLD_D, 'b', GOLD, 18, 0.6), CX, 1090, a2 * a0, 1.15 - 0.15 * p2)

    # ---- IT PAYS TO / PAY ATTENTION / & TAKE / ACTION
    def slogan(self, ov, t):
        c, CX, v = self.c, self.CX, self.o == 'v'
        T1 = c['T_OUT'] + 0.3; a0, _ = env(t, c['T_SLOG'], T1, 0.35, 0.35)
        if a0 <= 0: return
        if not v:
            rows = [('IT PAYS TO', WHITE, ICE, c['t_pays'], 270, 76), ('PAY ATTENTION', GOLD_L, GOLD_D, c['t_payatt'], 400, 124),
                    ('& TAKE', ICE, PINK, c['t_take'], 530, 76), ('ACTION', LIME, TEAL, c['t_action'], 680, 150)]
        else:
            rows = [('IT PAYS TO', WHITE, ICE, c['t_pays'], 500, 84), ('PAY ATTENTION', GOLD_L, GOLD_D, c['t_payatt'], 650, 112),
                    ('& TAKE', ICE, PINK, c['t_take'], 800, 84), ('ACTION', LIME, TEAL, c['t_action'], 975, 168)]
        for txt, c1, c2, tt, y, sz in rows:
            a, p = env(t, tt - 0.05, T1, 0.22, 0.3)
            paste_c(ov, G(txt, sz, c1, c2, 'b', c2, 16, 0.55), CX, y, a * a0, 1.25 - 0.25 * p)
        ta = c['t_action']; ya = 680 if not v else 975
        burst(ov, CX, ya, t, ta, [LIME, TEAL, GOLD, WHITE], 18, 160, 0.8, 360, 110)
        ae, pe = env(t, ta + 0.2, T1, 0.3, 0.3)
        if not v: paste_c(ov, logo_card(330), 240, 500, ae * a0, 0.7 + 0.3 * pe)
        else: paste_c(ov, logo_card(300), CX, 1330, ae * a0, 0.7 + 0.3 * pe)

    # ---- not financial advice, thank you, massive action, you are the best, signature
    def outro(self, ov, t):
        c, CX, v = self.c, self.CX, self.o == 'v'
        TH, TY, TWISH, TSIG = c['TH'], c['TY'], c['TWISH'], c['TSIG']
        t1 = c['END_CARD'] + 0.25; a0, _ = env(t, c['T_OUT'], t1, 0.3, 0.3)
        if a0 <= 0: return
        Y = (lambda h_, v_: h_) if not v else (lambda h_, v_: v_)
        if t < TH:
            a, p = env(t, c['T_OUT'] + 0.05, TH, 0.3, 0.25)
            paste_c(ov, ring_icon('shield-check', 170 if not v else 190, LIME), CX, Y(330, 600), a * a0, 0.85 + 0.15 * p)
            a1, p1 = env(t, c['t_none'] - 0.05, TH, 0.3, 0.25); paste_c(ov, T('Not financial advice', 76 if not v else 70), CX, Y(500, 800), a1 * a0, 1.1 - 0.1 * p1)
            a2, p2 = env(t, c['t_always'] - 0.05, TH, 0.3, 0.25)
            paste_c(ov, chip('Always do your own research', None, GOLD, 44, '🔎'), CX, Y(630, 950), a2 * a0, 0.9 + 0.1 * p2)
        elif t < TY:
            a, p = env(t, TH, TY, 0.3, 0.25); paste_c(ov, G('THANK YOU', 116 if not v else 124, PURPLE, PINK, 'b', PINK, 16, 0.55), CX, Y(230, 470), a * a0, 1.1 - 0.1 * p)
            for k, (ic, e, lab, col, ph) in enumerate([('thumbs-up', '👍', 'Like', LIME, 't_like'), ('share-2', '📤', 'Share', PINK, 't_share3'),
                                                         ('message-circle', '💬', 'Comment', GOLD, 't_comment')]):
                tt = c[ph]; x = CX + (k - 1) * (360 if not v else 310); yy = Y(500, 760); a2, p2 = env(t, tt - 0.04, TY, 0.18, 0.25)
                paste_c(ov, ring_icon(ic, 200 if not v else 210, col, e), x, yy, a2 * a0, (0.45 + 0.55 * p2) * pulse(t, tt + 0.2, 0.06))
                paste_c(ov, T(lab, 44, WHITE), x, yy + 160, a2 * a0); burst(ov, x, yy, t, tt, [col, WHITE], 12, 170 if not v else 130)
                if ph == 't_like':
                    for j in range(5):
                        u = (t - tt - 0.15 * j) / 1.4
                        if 0 <= u <= 1: paste_c(ov, emo('❤️', 40), x + 60 * math.sin(j * 2.1 + u * 3), yy - 80 - 220 * u, (1 - u) * a0)
            a3, p3 = env(t, c['t_support'] - 0.05, TY, 0.3, 0.25)
            paste_c(ov, chip('Your support means everything', None, PURPLE, 40, '🙏'), CX, Y(800, 1080), a3 * a0, 0.9 + 0.1 * p3)
        elif t < TWISH:
            a, p = env(t, TY, TWISH, 0.3, 0.25)
            paste_c(ov, T('Thank yourself', 80 if not v else 84), CX, Y(250, 470), a * a0); paste_c(ov, T('for taking', 52 if not v else 56, ICE, 'm'), CX, Y(345, 570), a * a0)
            tm = c['t_massive']; a2, p2 = env(t, tm - 0.05, TWISH, 0.22, 0.25)
            if not v:
                paste_c(ov, G('MASSIVE ACTION', 132, GOLD_L, GOLD_D, 'b', GOLD, 18, 0.6), CX, 490, a2 * a0, 1.25 - 0.25 * p2)
                burst(ov, CX, 490, t, tm, [GOLD, GOLD_L, WHITE], 16, 150, 0.8, 560, 105)
            else:
                paste_c(ov, G('MASSIVE', 150, GOLD_L, GOLD_D, 'b', GOLD, 18, 0.6), CX, 750, a2 * a0, 1.25 - 0.25 * p2)
                paste_c(ov, G('ACTION', 150, GOLD_L, GOLD_D, 'b', GOLD, 18, 0.6), CX, 910, a2 * a0, 1.25 - 0.25 * p2)
                burst(ov, CX, 830, t, tm, [GOLD, GOLD_L, WHITE], 16, 150, 0.8, 380, 200)
            a3, p3 = env(t, c['t_today'] - 0.05, TWISH, 0.3, 0.25)
            paste_c(ov, chip('today, to change your future!', None, LIME, 46, '🚀'), CX, Y(660, 1110), a3 * a0, 0.9 + 0.1 * p3)
        elif t < TSIG:
            a, p = env(t, TWISH, TSIG, 0.3, 0.25)
            if not v: paste_c(ov, T('I wish you nothing but the best,', 62), CX, 300, a * a0)
            else: paste_c(ov, T('I wish you nothing', 64), CX, 430, a * a0); paste_c(ov, T('but the best,', 64), CX, 515, a * a0)
            tb = c['t_because']; a2, p2 = env(t, tb - 0.05, TSIG, 0.22, 0.25)
            if not v:
                paste_c(ov, G('YOU ARE THE BEST', 138, LIME, TEAL, 'b', LIME, 18, 0.6), CX, 490, a2 * a0, 1.25 - 0.25 * p2)
                burst(ov, CX, 490, t, tb + 0.15, [LIME, GOLD, WHITE, PINK], 18, 150, 0.9, 640, 110); cy, rx, ry = 490, 640, 170
            else:
                paste_c(ov, G('YOU ARE', 150, LIME, TEAL, 'b', LIME, 18, 0.6), CX, 720, a2 * a0, 1.25 - 0.25 * p2)
                paste_c(ov, G('THE BEST', 150, LIME, TEAL, 'b', LIME, 18, 0.6), CX, 880, a2 * a0, 1.25 - 0.25 * p2)
                burst(ov, CX, 800, t, tb + 0.15, [LIME, GOLD, WHITE, PINK], 18, 150, 0.9, 400, 200); cy, rx, ry = 800, 440, 250
            for k in range(6):
                ang = k * math.pi / 3 + 0.4; tw = 0.6 + 0.4 * math.sin(t * 6 + k)
                paste_c(ov, emo('✨', 52), CX + rx * math.cos(ang), cy + ry * math.sin(ang), a2 * a0 * tw, 0.8 + 0.2 * tw)
            a3, p3 = env(t, tb + 0.3, TSIG, 0.3, 0.25); paste_c(ov, logo_card(230), CX, Y(755, 1180), a3 * a0, 0.8 + 0.2 * p3)
        else:
            a, p = env(t, TSIG, t1, 0.35, 0.25)
            a1, _ = env(t, c['t_arch'] - 0.05, t1, 0.35, 0.25)
            a2, p2 = env(t, c['t_see'] - 0.05, t1, 0.3, 0.25)
            if not v:
                paste_c(ov, logo_card(520), 560, 470, a * a0, 0.9 + 0.1 * p); RX_ = 1280
                paste_c(ov, T('Crypto-Regards,', 104, GOLD_L, 'sig'), RX_, 300, a * a0)
                paste_c(ov, G('MTG', 190, GOLD_L, GOLD_D, 'b', GOLD_D, 18, 0.6), RX_, 470, a * a0, 0.9 + 0.1 * p)
                paste_c(ov, T('Y O U R   D I G I T A L   A R C H I T E C T', 30, LIME), RX_, 610, a1 * a0)
                paste_c(ov, chip('See you on the next one', None, PINK, 40, '👋'), RX_, 730, a2 * a0, 0.9 + 0.1 * p2)
            else:
                paste_c(ov, logo_card(440), CX, 560, a * a0, 0.9 + 0.1 * p)
                paste_c(ov, T('Crypto-Regards,', 110, GOLD_L, 'sig'), CX, 900, a * a0)
                paste_c(ov, G('MTG', 200, GOLD_L, GOLD_D, 'b', GOLD_D, 18, 0.6), CX, 1070, a * a0, 0.9 + 0.1 * p)
                paste_c(ov, T('Y O U R   D I G I T A L   A R C H I T E C T', 30, LIME), CX, 1210, a1 * a0)
                paste_c(ov, chip('See you on the next one', None, PINK, 44, '👋'), CX, 1340, a2 * a0, 0.9 + 0.1 * p2)

    # ---- end card: stays to the last frame (the site address is visible to the end)
    def end_card(self, ov, t):
        c, CX, v = self.c, self.CX, self.o == 'v'; E = c['END_CARD']
        if t < E: return
        a0 = ease_out((t - E) / 0.45)
        a, p = env(t, E + 0.05, 1e9, 0.45, 0.1); a1, _ = env(t, E + 0.4, 1e9, 0.4, 0.1)
        a2, _ = env(t, E + 0.8, 1e9, 0.4, 0.1); a4, p4 = env(t, E + 0.3, 1e9, 0.35, 0.1)
        a5, p5 = env(t, E + 1.7, 1e9, 0.4, 0.1); a6, _ = env(t, E + 2.0, 1e9, 0.4, 0.1)
        LX = 470 if not v else CX
        Ys = (265, 462, 550, 627, 660) if not v else (330, 545, 640, 722, 762)
        paste_c(ov, logo_card(300 if not v else 280), LX, Ys[0], a * a0, 0.88 + 0.12 * p)
        paste_c(ov, T('Crypto-Regards,', 62, GOLD_L, 'sig'), LX, Ys[1], a * a0)
        paste_c(ov, G('MTG', 104, GOLD_L, GOLD_D, 'b', GOLD_D, 16, 0.6), LX, Ys[2], a * a0, 0.88 + 0.12 * p)
        paste_c(ov, T('YOUR DIGITAL ARCHITECT', 30, LIME), LX, Ys[3], a1 * a0)
        ly0 = Ys[4]
        lay = Image.new('RGBA', (self.W, self.H), (0, 0, 0, 0)); ImageDraw.Draw(lay).line([(LX - 190, ly0), (LX + 190, ly0)], fill=GOLD + (255,), width=3)
        paste(ov, lay, 0, 0, a1 * a0)
        sl = T("Let's Get This Crypto!", 56, WHITE)
        paste_c(ov, sl, LX - 36, ly0 + 80, a2 * a0); paste_c(ov, emo('💪', 70), LX - 36 + sl.width / 2 + 46, ly0 + 76 - 10 * abs(math.sin((t - E) * 4)), a2 * a0)
        if not v:
            RXc = 1370
            paste_c(ov, url_pill('mtgtribe.com/jetup', 72), RXc, 175, a4 * a0, 0.9 + 0.1 * p4)
            for k, key in enumerate(['tiktok', 'youtube', 'whatsapp', 'telegram', 'facebook']):
                ak, pk = env(t, E + 0.6 + 0.18 * k, 1e9, 0.35, 0.1)
                paste_c(ov, plat_badge(key, 760, 82), RXc + (1 - pk) * 40, 300 + k * 100, ak * a0)
            if self.nxt: paste_c(ov, chip(self.nxt, 'play', LIME, 32, '📺'), RXc, 850, a5 * a0, 0.9 + 0.1 * p5)
            paste_c(ov, T('Not financial advice. Trading involves risk. Only use money you can afford to lose.', 28, GREY, 'm'), CX, 1015, a6 * a0)
        else:
            paste_c(ov, url_pill('mtgtribe.com/jetup', 70), CX, 990, a4 * a0, 0.9 + 0.1 * p4)
            for k, key in enumerate(['tiktok', 'youtube', 'whatsapp', 'telegram', 'facebook']):
                ak, pk = env(t, E + 0.6 + 0.18 * k, 1e9, 0.35, 0.1)
                paste_c(ov, plat_badge(key, 760, 78), CX + (1 - pk) * 40, 1125 + k * 92, ak * a0)
            if self.nxt: paste_c(ov, chip(self.nxt, 'play', LIME, 32, '📺'), CX, 1610, a5 * a0, 0.9 + 0.1 * p5)
            paste_c(ov, T('Not financial advice. Trading involves risk.', 28, GREY, 'm'), CX, 1720, a6 * a0)
            paste_c(ov, T('Only use money you can afford to lose.', 28, GREY, 'm'), CX, 1762, a6 * a0)

    # ---- sound effect times for the ending (as in the training's sfx_times)
    def sfx(self):
        c = self.c
        wh = [c['T_LINKS'], c['T_ENG'], c['T_WE'], c['T_SLOG'], c['T_OUT'], c['TH'], c['TY'], c['TWISH'], c['TSIG'], c['END_CARD']]
        if self.links: wh.append(c['T_FAIR'])
        pops = [c['t_save'], c['t_share'], c['t_free'], c['t_action'], c['t_like'], c['t_share3'], c['t_comment'], c['t_massive'], c['t_because'] + 0.15]
        if self.links: pops.append(c['t_url'])
        return dict(whoosh=wh, pop=pops, tick=[c['t_their'], c['t_every']], click=[])

# ------------------------------------------------------------------ cue names and how to find them in the word list
def find_cues(words, links=True):
    """words: [{w, a, b}] absolute, in order. Returns the cue dict for Ending."""
    toks = [(__import__('re').sub(r'[^a-z0-9]', '', w['w'].lower()), w['a'], w['b']) for w in words]
    def S(phrase, after=0.0):
        ph = phrase.split()
        for i in range(len(toks) - len(ph) + 1):
            if toks[i][1] >= after - 1e-6 and all(toks[i + k][0] == ph[k] for k in range(len(ph))): return toks[i][1]
        raise KeyError(phrase)
    c = {}
    if links:
        c['T_LINKS'] = S('everything i showed you') - 0.25; c['t_url'] = S('mtgtribecomjetup', c['T_LINKS'])
    c['T_FAIR'] = S('invited by someone else') - 0.25
    if not links: c['T_LINKS'] = c['T_FAIR']
    c['t_their'] = S('use their link', c['T_FAIR']); c['t_every'] = S('this video is for every', c['T_FAIR']); c['t_free'] = S('share it', c['t_every'])
    c['T_ENG'] = S('save this video', c['T_FAIR']) - 0.25; c['t_save'] = S('save this video', c['T_FAIR']); c['t_soits'] = S('so its here', c['t_save'])
    c['t_share'] = S('share it with someone', c['t_save']); c['t_ready'] = S('whos ready', c['t_share'])
    c['T_WE'] = S('we learn best', c['t_share']) - 0.25; c['t_teach'] = S('when we teach', c['T_WE'])
    c['T_SLOG'] = S('it pays to pay attention', c['T_WE']) - 0.25; c['t_pays'] = S('it pays to', c['T_SLOG'])
    c['t_payatt'] = S('pay attention', c['t_pays'] + 0.2); c['t_take'] = S('and take', c['t_payatt']); c['t_action'] = S('action', c['t_take'])
    c['T_OUT'] = S('quick reminder', c['T_SLOG']) - 0.25; c['t_none'] = S('none of this', c['T_OUT']); c['t_always'] = S('always do your', c['T_OUT'])
    c['TH'] = S('thank you for tuning in', c['T_OUT']); c['t_like'] = S('like', c['TH']); c['t_share3'] = S('share', c['TH']); c['t_comment'] = S('comment', c['TH'])
    c['t_support'] = S('your support', c['TH']); c['TY'] = S('and thank yourself', c['TH']); c['t_massive'] = S('massive', c['TY']); c['t_today'] = S('today', c['TY'])
    c['TWISH'] = S('i wish you nothing', c['TY']); c['t_because'] = S('because you', c['TWISH'])
    c['TSIG'] = S('im mtg', c['TWISH']); c['t_arch'] = S('your digital architect', c['TSIG']); c['t_see'] = S('see you on the next one', c['TSIG'])
    c['t_lgtc'] = S('lets get this crypto', c['TSIG']); c['END_CARD'] = c['t_lgtc'] + 0.35
    return {k: round(v, 3) for k, v in c.items()}

# ------------------------------------------------------------------ the training's four sound effects (verbatim)
def sfx_bank(SR=48000, seed=7):
    from scipy.signal import butter, sosfilt
    rng = np.random.default_rng(seed)
    def whoosh():
        n = int(0.5 * SR); x = rng.standard_normal(n).astype(np.float32); o = np.zeros(n, np.float32)
        for k in range(10):
            a, b = k * n // 10, (k + 1) * n // 10; fc = 500 + 3500 * (k / 9)
            o[a:b] = sosfilt(butter(2, [fc * 0.6, fc * 1.4], btype='band', fs=SR, output='sos'), x)[a:b]
        o *= np.sin(np.pi * np.linspace(0, 1, n)) ** 2; return o / np.abs(o).max() * 0.08
    def tick():
        n = int(0.08 * SR); tt = np.arange(n) / SR
        x = (np.sin(2 * np.pi * 1760 * tt) + 0.4 * np.sin(2 * np.pi * 3520 * tt)) * np.exp(-tt * 55); return x / np.abs(x).max() * 0.07
    def pop():
        n = int(0.12 * SR); tt = np.arange(n) / SR; f = 380 + 700 * tt / tt[-1]
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 30); return x / np.abs(x).max() * 0.12
    def click():
        n = int(0.05 * SR); tt = np.arange(n) / SR
        x = rng.standard_normal(n) * np.exp(-tt * 180) + 0.6 * np.sin(2 * np.pi * 2200 * tt) * np.exp(-tt * 120)
        x = sosfilt(butter(2, [900, 6000], btype='band', fs=SR, output='sos'), x); return x / np.abs(x).max() * 0.10
    return dict(whoosh=whoosh, tick=tick, pop=pop, click=click)
# In the training these sit under a voice at about -19.6 LUFS; with the voice at -16 LUFS they are raised by the same 3.6 dB.
SFX_GAIN_AT_MINUS16 = 10 ** (3.6 / 20)
