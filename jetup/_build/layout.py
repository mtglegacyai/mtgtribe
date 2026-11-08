# JetUP and TAG Markets guide by MTG: shared layout (head, top bar, side menu, footer, player).
# Run build.py to write every page. No em or en dashes anywhere in the output.
import hashlib, json, os, re
from phone_tables import label_tables   # phones never scroll sideways (MTG, 6 Nov 2026)
from extras import JUMP, jump_bar, thumb_bar, search_box, mark_terms, gl_popover, faq_ids   # MTG, 7 Nov 2026

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SITE = 'https://mtgtribe.com'
TODAY = '2026-11-06'

# One place for facts that may need a quick change
RETAIL_LOSS = '88%'   # TAG Markets' reminder, as in the approved videos (MTG confirmed 88%, 6 Nov 2026).
VALR = 'https://www.valr.com/invite/VAKM6VZY'
BINANCE = 'https://accounts.binance.com/register?ref=11139868'
WA_MTG = 'https://wa.me/27721714626'
WA_PARTNER = WA_MTG + '?text=' + 'Hi%20MTG%2C%20I%20watched%20your%20JetUP%20training.%20Please%20send%20me%20your%20JetUP%20Partner%20link.'
GROUP = '/group/'
# MTG's JetUP Partner link (sent by MTG 7 Nov 2026). Every "Join JetUP" button on the guide uses this one constant.
JETUP_JOIN = 'https://jetup.ibportal.io/auth/register?e=y0ylqkMzz0m1XW_OPx2MYQWc4ZKJrNQWbP0Vz6aATbI&a=1'
JOIN_NOTE = ("Join JetUP opens JetUP's sign-up page with MTG's Partner link, so MTG becomes your sponsor. "
             "Invited by someone else? Use their Partner link instead, so you join their team.")
YT = 'https://www.youtube.com/@mtgtribe'
TT = 'https://www.tiktok.com/@joinmtgtribe'
TG = 'https://t.me/mtgtribez'
FB = 'https://www.facebook.com/Musa.TheMTG'

def ver(path):
    with open(os.path.join(ROOT, path.lstrip('/')), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

ICONS = json.load(open(os.path.join(os.path.dirname(__file__), 'icons.json')))
def _sym(i, body, fill=False):
    a = 'fill="currentColor"' if fill else 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    return '<symbol id="%s" viewBox="0 0 24 24" %s>%s</symbol>' % (i, a, body)
ICONS.update({
 'i-menu': _sym('i-menu', '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>'),
 'i-alert': _sym('i-alert', '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>'),
 'i-lock': _sym('i-lock', '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>'),
 'i-door': _sym('i-door', '<path d="M13 4h3a2 2 0 0 1 2 2v14"/><path d="M2 20h3"/><path d="M13 20h9"/><path d="M10 12v.01"/><path d="M13 4.56v16.16a1 1 0 0 1-1.24.97L5 20V5.56a2 2 0 0 1 1.52-1.94l4-1A2 2 0 0 1 13 4.56Z"/>'),
 'i-search': _sym('i-search', '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>'),
 'i-gift': _sym('i-gift', '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C10 3 12 8 12 8s2-5 4.5-5a2.5 2.5 0 0 1 0 5"/>'),
 'i-home': _sym('i-home', '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .71-1.53l7-6a2 2 0 0 1 2.58 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'),
 'i-zoom': _sym('i-zoom', '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/><path d="M11 8v6"/><path d="M8 11h6"/>'),
 'i-file': _sym('i-file', '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>'),
 'i-mail': _sym('i-mail', '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>'),
 'i-id': _sym('i-id', '<rect width="20" height="14" x="2" y="5" rx="2"/><circle cx="8" cy="12" r="2.5"/><path d="M14 10h5"/><path d="M14 14h4"/>'),
 'i-key': _sym('i-key', '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>'),
 'i-phone': _sym('i-phone', '<rect width="14" height="20" x="5" y="2" rx="2"/><path d="M12 18h.01"/>'),
 'i-chart': _sym('i-chart', '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>'),
 'i-check2': _sym('i-check2', '<path d="M20 6 9 17l-5-5"/>'),
 'i-chev-l': _sym('i-chev-l', '<path d="m15 18-6-6 6-6"/>'),
 'i-chev-r': _sym('i-chev-r', '<path d="m9 18 6-6-6-6"/>'),
 'i-up': _sym('i-up', '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>'),
 'i-chev-d': _sym('i-chev-d', '<path d="m6 9 6 6 6-6"/>'),
 'i-book': _sym('i-book', '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/><path d="M9 7h7"/><path d="M9 11h5"/>'),
 'i-x2': _sym('i-x2', '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>'),
 'i-play2': _sym('i-play2', '<path d="M7 4.5v15a1 1 0 0 0 1.52.85l12-7.5a1 1 0 0 0 0-1.7l-12-7.5A1 1 0 0 0 7 4.5Z"/>', fill=True),
 'i-arrow2': _sym('i-arrow2', '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>'),
 'i-ext2': _sym('i-ext2', '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'),
 'i-copy2': _sym('i-copy2', '<rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>'),
 'i-dl2': _sym('i-dl2', '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>'),
 'i-wallet2': _sym('i-wallet2', '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>'),
 'i-calc2': _sym('i-calc2', '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M8 6h8"/><path d="M16 14v4"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/>'),
 'i-split': _sym('i-split', '<path d="M21 12a9 9 0 1 1-9-9v9z"/><path d="M12 3a9 9 0 0 1 9 9h-9z"/>'),
 'i-bus': _sym('i-bus', '<path d="M8 6v6"/><path d="M15 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/><circle cx="7" cy="18" r="2"/><path d="M9 18h5"/><circle cx="16" cy="18" r="2"/>'),
 'i-users2': _sym('i-users2', '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
 'i-landmark': _sym('i-landmark', '<path d="M3 22h18"/><path d="M6 18v-7"/><path d="M10 18v-7"/><path d="M14 18v-7"/><path d="M18 18v-7"/><path d="m12 2 8 5H4z"/>'),
 'i-copyx': _sym('i-copyx', '<rect width="8" height="8" x="2" y="2" rx="2"/><rect width="8" height="8" x="14" y="14" rx="2"/><path d="M14 6h4a2 2 0 0 1 2 2v4"/><path d="M10 18H6a2 2 0 0 1-2-2v-4"/><path d="m17 9 3 3 3-3" transform="translate(-3 0)"/>'),
 'i-bot': _sym('i-bot', '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>'),
 'i-coins2': _sym('i-coins2', '<circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18"/><path d="M7 6h1v4"/><path d="m16.71 13.88.7.71-2.82 2.82"/>'),
 'i-trophy2': _sym('i-trophy2', '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>'),
 'i-card2': _sym('i-card2', '<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20"/>'),
 'i-film2': _sym('i-film2', '<path d="m16 13 5.22 3.48a.5.5 0 0 0 .78-.42V7.87a.5.5 0 0 0-.75-.43L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>'),
 'i-help': _sym('i-help', '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>'),
 'i-compass2': _sym('i-compass2', '<circle cx="12" cy="12" r="10"/><path d="m16.24 7.76-2.12 6.36-6.36 2.12 2.12-6.36z"/>'),
 'i-rocket2': _sym('i-rocket2', '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>'),
 'i-shield2': _sym('i-shield2', '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>'),
 'i-scale2': _sym('i-scale2', '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>'),
 'i-trend2': _sym('i-trend2', '<path d="M16 7h6v6"/><path d="m22 7-8.5 8.5-5-5L2 17"/>'),
 'i-percent2': _sym('i-percent2', '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>'),
 'i-info2': _sym('i-info2', '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>'),
 'i-refresh2': _sym('i-refresh2', '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>'),
 'i-layers2': _sym('i-layers2', '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>'),
 'i-timer2': _sym('i-timer2', '<path d="M10 2h4"/><path d="M12 14l3-3"/><circle cx="12" cy="14" r="8"/>'),
 'i-candle2': _sym('i-candle2', '<path d="M9 5v4"/><rect width="4" height="6" x="7" y="9" rx="1"/><path d="M9 15v2"/><path d="M17 3v2"/><rect width="4" height="8" x="15" y="5" rx="1"/><path d="M17 13v3"/><path d="M3 3v18h18"/>'),
})

def icon(name, cls='ic'):
    return '<svg class="%s" aria-hidden="true" focusable="false"><use href="#%s"/></svg>' % (cls, name)

# ---------------------------------------------------------------- the menu
MENU = [
 ('Start here', [
   ('/jetup/', 'i-compass2', 'Overview', 'The whole picture, in one page'),
   ('/jetup/five-checks/', 'i-shield2', 'The 5 checks', 'Burned before? Start here'),
   ('/jetup/get-started/', 'i-rocket2', 'Sign-up training', 'Every tap, in 6 parts'),
 ]),
 ('Understand it', [
   ('/jetup/how-it-works/', 'i-layers2', 'How it works', 'Who holds what, 70/30, Amplify'),
   ('/jetup/partner-plan/', 'i-users2', 'Partner plan', "JetUP's four incomes, honestly"),
   ('/jetup/promo/', 'i-gift', 'Dennis Fast Start Promo', 'The rules, and how to claim'),
   ('/jetup/bix-card/', 'i-card2', 'BIX Card', 'Crypto wallet and Visa card'),
 ]),
 ('Tools', [
   ('/jetup/tools/exposure-calculator/', 'i-candle2', 'Exposure Calculator', 'See what 24x Amplify means', 'tool'),
   ('/jetup/tools/profit-split-calculator/', 'i-split', 'Profit Split Calculator', 'Your 70%, the 30% fee', 'tool'),
 ]),
 ('Library', [
   ('/jetup/videos/', 'i-film2', 'Videos', 'Trainings and explainers'),
   ('/jetup/downloads/', 'i-dl2', 'Downloads', 'Guides, decks and videos'),
   ('/jetup/faq/', 'i-help', 'FAQ', 'Straight answers'),
   ('/jetup/glossary/', 'i-book', 'Glossary', 'Every word, explained'),
 ]),
]

def side_menu(path):
    out = ['<aside class="side" id="side" aria-label="JetUP guide menu">',
           ' <div class="side-top"><img src="/jetup/img/jetup-mark-128.webp" width="64" height="64" alt="JetUP"><span><b>JetUP <span class="lime">×</span> TAG</b>Independent guide by MTG 👑</span>',
           '  <button class="menu-btn side-x" type="button" data-menu-x aria-label="Close the menu">%s</button></div>' % icon('i-x2'),
           ' ' + search_box(icon),
           ' <nav aria-label="Guide pages">']
    for label, items in MENU:
        out.append('  <div role="group" aria-label="%s"><p class="slabel">%s</p>' % (label, label))
        for it in items:
            href, ic, name, sub = it[:4]
            cls = ' tool' if len(it) > 4 else ''
            cur = ' aria-current="page"' if href == path else ''
            out.append('   <a class="snav%s" href="%s"%s><span class="si">%s</span><span class="stx"><b>%s</b><small>%s</small></span></a>' % (cls, href, cur, icon(ic), name, sub))
        out.append('  </div>')
    out.append(' </nav>')
    out.append(' <div class="side-bot">')
    out.append('  <a class="btn btn-pri btn-sm" href="%s" target="_blank" rel="sponsored noopener" data-join>%sJoin JetUP</a>' % (JETUP_JOIN, icon('i-rocket2')))
    out.append('  <a class="btn btn-lime btn-sm" href="%s"><span class="emo" aria-hidden="true">💬</span>Join the MTG TRIBE</a>' % GROUP)
    out.append('  <div class="row"><a class="slink" href="/jetup/"><span aria-hidden="true">🏡</span>JetUP home</a><a class="slink" href="/dashboard/"><span aria-hidden="true">📊</span>Dashboard</a></div>')
    out.append('  <a class="sfine" href="/jetup/disclaimer/">Disclaimer · Education only, not financial advice</a>')
    out.append(' </div>')
    out.append('</aside>')
    return '\n'.join(out)

def top_bar(docked):
    first = '<button class="menu-btn open-m" type="button" data-menu aria-label="Open the menu" aria-controls="side">%s</button>' % icon('i-menu')
    return '\n'.join([
     '<header class="top">',
     ' ' + first,
     ' <a class="brand" href="/jetup/" aria-label="JetUP and TAG Markets guide home"><img src="/jetup/img/jetup-mark-64.webp" width="38" height="38" alt=""><span class="bt"><b>JetUP <span>×</span> TAG Markets</b><small>Independent guide by MTG 👑</small></span></a>',
     ' <div class="acts"><a class="btn btn-pri btn-sm hide-s" href="/jetup/get-started/">%sStart the training</a><a class="btn btn-lime btn-sm tjoin" href="%s" target="_blank" rel="sponsored noopener" data-join>Join JetUP</a><a class="btn btn-ghost btn-sm" href="/jetup/" aria-label="JetUP and TAG Markets home" title="JetUP and TAG Markets home"><span class="emo" aria-hidden="true">🏡</span><span class="hide-s">JetUP home</span></a></div>' % (icon('i-rocket2'), JETUP_JOIN),
     '</header>'])

def footer():
    return '''<footer class="foot"><div class="wrap">
 <img class="flogo" src="/jetup/img/jetup-logo-240.webp" width="120" height="95" alt="JetUP logo" loading="lazy">
 <p class="slog"><span class="mtg-gold">Let's Get This Crypto!</span> <span aria-hidden="true">💪</span></p>
 <p class="brandline">MTG 👑 | Your Digital Architect</p>
 <div class="socials">
  <a class="soc" href="%s">%sMTG TRIBE on WhatsApp</a>
  <a class="soc" href="%s" target="_blank" rel="noopener">%sYouTube @mtgtribe</a>
  <a class="soc" href="%s" target="_blank" rel="noopener">%sTikTok @joinmtgtribe</a>
  <a class="soc" href="%s" target="_blank" rel="noopener">%sTelegram</a>
  <a class="soc" href="%s" target="_blank" rel="noopener">%sFacebook</a>
 </div>
 <div class="flinks"><a href="/jetup/">JetUP guide</a><a href="/jetup/get-started/">Sign-up training</a><a href="/jetup/five-checks/">The 5 checks</a><a href="/jetup/faq/">FAQ</a><a href="/jetup/disclaimer/">Disclaimer</a><a href="/dashboard/">Dashboard</a><a href="/">mtgtribe.com</a></div>
 <p class="fine">Independent guide by MTG. Not official JetUP or TAG Markets material. Education only, not financial advice: always do your own research. Trading forex, CFDs and copy trading is high risk, and you can lose all the money you deposit. TAG Markets' own reminder says %s of retail investor accounts lose money when trading CFDs. Past results never promise future ones. The VALR and Binance buttons are MTG's referral links.</p>
 <p class="made">Made with ❤️ by MTG 👑 | Your Digital Architect · © 2026 MTG</p>
</div></footer>''' % (GROUP, icon('i-whatsapp'), YT, icon('i-youtube'), TT, icon('i-tiktok'), TG, icon('i-telegram'), FB, icon('i-facebook'), RETAIL_LOSS)

# Previous and next page, in menu order, then the disclaimer (MTG, 6 Nov 2026)
ORDER = [it[:4] for _, items in MENU for it in items] + [('/jetup/disclaimer/', 'i-scale2', 'Disclaimer', 'Education only, and the risks')]

def page_name(path):
    for o in ORDER:
        if o[0] == path:
            return o[2]
    return 'JetUP guide'

def pager(path):
    paths = [o[0] for o in ORDER]
    if path not in paths:
        return ''
    i, n = paths.index(path), len(ORDER)
    def card(o, cls, key, rel):
        href, ic, name, sub = o
        chev = icon('i-chev-l' if cls == 'prev' else 'i-chev-r')
        k = (chev + key) if cls == 'prev' else (key + chev)
        return ('<a class="pg %s" href="%s"%s><span class="pg-k">%s</span>'
                '<span class="pg-t"><span class="si">%s</span><b>%s</b></span><small>%s</small></a>') % (cls, href, rel, k, icon(ic), name, sub)
    prev = card(ORDER[i - 1], 'prev', 'Previous', ' rel="prev"') if i > 0 else '<span class="pg pg-none" aria-hidden="true"></span>'
    if i < n - 1:
        nxt = card(ORDER[i + 1], 'next', 'Next', ' rel="next"')
    else:
        nxt = card(('/jetup/', 'i-home', 'Back to the start', 'The JetUP and TAG Markets home'), 'next', 'Start again', '')
    return ('<nav class="pager" aria-label="Previous and next page"><div class="wrap">'
            '<p class="pg-pos"><span>Page %d of %d</span><i style="--p:%.3f" aria-hidden="true"></i></p>'
            '<div class="pg-row">%s%s</div></div></nav>') % (i + 1, n, (i + 1) / n, prev, nxt)

TOTOP = ('<button class="totop" id="totop" type="button" aria-label="Back to the top" title="Back to the top">'
         '<svg class="ring" viewBox="0 0 52 52" aria-hidden="true" focusable="false"><circle class="bg" cx="26" cy="26" r="24"/>'
         '<circle class="fg" cx="26" cy="26" r="24"/></svg>%s</button>') % icon('i-up')

PLAYER = '''<dialog class="vm" id="vm" aria-label="Video player">
 <div class="vm-bg" aria-hidden="true"></div>
 <div class="vm-box">
  <div class="vm-vid laptop" id="vm-dev">
   <span class="dev-btn l1" aria-hidden="true"></span><span class="dev-btn l2" aria-hidden="true"></span><span class="dev-btn l3" aria-hidden="true"></span><span class="dev-btn r1" aria-hidden="true"></span>
   <div class="scr"><video id="vm-video" controls playsinline preload="none"></video><span class="isl" aria-hidden="true"></span></div>
   <span class="base" aria-hidden="true"><i></i></span>
   <button class="vm-x" type="button" id="vm-x" aria-label="Close the video">%s</button>
  </div>
  <p class="vm-t" id="vm-title"></p>
 </div>
</dialog>''' % icon('i-x2')

LIGHTBOX = '''<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Screenshot, zoomed in"><div><img alt=""><p></p></div><button class="vm-x" type="button" aria-label="Close the screenshot">%s</button></div>''' % icon('i-x2')

def crumbs(items):
    lis = ''.join('<li>%s</li>' % ('<a href="%s">%s</a>' % (h, n) if h else '<span aria-current="page">%s</span>' % n) for n, h in items)
    return '<ol class="crumbs">%s</ol>' % lis

def ld_crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (h or '')} for i, (n, h) in enumerate(items)]}

def ld_faq(qas, pid):
    def strip(s): return re.sub(r'<[^>]+>', '', s)
    return {"@type": "FAQPage", "@id": pid + "#faq", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qas]}

VIDEOS = {
 'tut1': dict(src='/jetup/media/jetup-tutorial-part-1-create-account.mp4', poster='/jetup/img/cover-tutorial-part-1-v2.webp', jpg='/jetup/img/cover-tutorial-part-1-v2.jpg', dur='3:38', iso='PT3M38S', orient='v',
   title='JetUP step by step, part 1: create your JetUP account',
   desc="MTG's own recording, tap by tap: the Partner link, Individual, your real name, a password of 8 to 12 characters, country and phone, Register Now, verify your email, log in and check Account Type: Partner."),
 'tut3': dict(src='/jetup/media/jetup-tutorial-part-3-verify-identity.mp4', poster='/jetup/img/cover-tutorial-part-3.webp', jpg='/jetup/img/cover-tutorial-part-3.jpg', dur='3:29', iso='PT3M29S', orient='v',
   title='JetUP step by step, part 3: verify your identity (KYC)',
   desc="MTG's own recording, tap by tap: upload documents on TAG Markets, Sumsub's check, your country, your Sumsub ID email and code, Create my account, Identity Card, double-sided, the tips, allow the camera, then the ID scan and the selfie."),
 'tut2': dict(src='/jetup/media/jetup-tutorial-part-2-link-tag-markets.mp4', poster='/jetup/img/cover-tutorial-part-2.webp', jpg='/jetup/img/cover-tutorial-part-2.jpg', dur='3:35', iso='PT3M35S', orient='v',
   title='JetUP step by step, part 2: link JetUP to TAG Markets',
   desc="MTG's own recording, tap by tap: log in to JetUP, tap Register CopyX on the CopyX banner, enter your JetUP password, tick the boxes, Sync Account, wait for User Active, log in to TAG Markets and confirm your email."),
 '5checks': dict(src='/jetup/media/jetup-5-checks-mtg-v5.mp4', poster='/jetup/img/cover-5-checks-v5.webp', jpg='/jetup/img/cover-5-checks-v5.jpg', dur='5:25', iso='PT5M25S', orient='h',
   title='JetUP 5 Checks: lost money before? Check these 5 things before you try again',
   desc="MTG's honest explainer: who holds your money, who regulates TAG Markets, whether Sonic AI's results are real, what can go wrong with 24x Amplify, and how to get out."),
 'training': dict(src='/jetup/media/jetup-tag-markets-signup-training-mtg.mp4', poster='/jetup/img/cover-signup-training.webp', jpg='/jetup/img/cover-signup-training.jpg', dur='9:09', iso='PT9M9S', orient='h',
   title='JetUP and TAG Markets sign-up training: every tap shown',
   desc='Step-by-step training by MTG: create your JetUP account, link TAG Markets, verify your identity, fund your account, connect Sonic AI and claim the Dennis Fast Start Promo.'),
 'profitshare': dict(src='/jetup/media/jetup-profit-share-explained.mp4', poster='/jetup/img/cover-profit-share.webp', jpg='/jetup/img/cover-profit-share.webp', dur='1:14', iso='PT1M14S', orient='v',
   title="Profit Share explained: JetUP's own 74-second video",
   desc="JetUP's official short explainer of the Sonic AI Profit Share across 10 levels, and how direct partners unlock them."),
}

def ld_video(k):
    v = VIDEOS[k]
    return {"@type": "VideoObject", "name": v['title'], "description": v['desc'], "thumbnailUrl": SITE + v['jpg'], "uploadDate": TODAY,
            "duration": v['iso'], "contentUrl": SITE + v['src'], "inLanguage": "en-ZA"}

def video_btn(k, cls='vcard', inner=None, label=None):
    v = VIDEOS[k]
    lab = label or ('Play: %s (%s)' % (v['title'], v['dur']))
    return '<button type="button" class="%s" data-video="%s" data-poster="%s" data-orient="%s" data-title="%s" aria-label="%s">%s</button>' % (
        cls, v['src'], v['poster'], v['orient'], v['title'].replace('"', '&quot;'), lab.replace('"', '&quot;'), inner or '')

def laptop(k, caption=None, eager=False):
    v = VIDEOS[k]
    load = '' if eager else ' loading="lazy"'
    inner = ('<span class="laptop"><span class="scr"><span class="media"><img src="%s" width="1280" height="720" alt=""%s><span class="vplay">%s</span><span class="vdur">%s</span></span></span><span class="base"><i></i></span></span>'
             % (v['poster'], load, icon('i-play2', ''), v['dur']))
    out = video_btn(k, 'vcard', inner)
    if caption:
        out += '<p class="vcap">%s%s</p>' % (icon('i-film2'), caption)
    return out

def phone(k, caption=None):
    v = VIDEOS[k]
    inner = '<span class="ps"><img src="%s" width="480" height="848" alt="" loading="lazy"><span class="isl" aria-hidden="true"></span><span class="vplay">%s</span><span class="vdur">%s</span></span>' % (v['poster'], icon('i-play2', ''), v['dur'])
    out = video_btn(k, 'phone-card', inner)
    if caption:
        out += '<p class="vcap">%s%s</p>' % (icon('i-film2'), caption)
    return out

def page(path, title, desc, main, crumbs_list=None, ld_extra=None, docked=True, og_img='/jetup/img/cover-5-checks-v5.jpg', og_alt='JetUP and TAG Markets guide by MTG', lightbox=False, keywords=None):
    url = SITE + path
    kw = keywords or 'JetUP, JetUp, TAG Markets, JetUp TAG Markets, TAG Markets copy trading, JetUp review, TAG Markets review, TAG Markets South Africa, how to join JetUp, CopyX, Sonic AI, MTG TRIBE'
    graph = [{"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "en-ZA",
              "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/altruva/#mtg"}, "datePublished": TODAY, "dateModified": TODAY,
              "about": [{"@type": "Organization", "name": "TAG Markets", "url": "https://tagmarkets.com/"}, {"@type": "Organization", "name": "JetUP", "url": "https://jet-up.ai/"}],
              "primaryImageOfPage": SITE + og_img}]
    if crumbs_list:
        graph[0]["breadcrumb"] = ld_crumbs(crumbs_list)
    graph += (ld_extra or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(',', ':'))
    body = main
    used = set(re.findall(r'#(i-[a-z0-9-]+)', body + side_menu(path) + top_bar(docked) + footer() + PLAYER + pager(path) + TOTOP + jump_bar(path, icon) + thumb_bar(path, icon, JETUP_JOIN) + (LIGHTBOX if lightbox else ''))) | {'i-chev-l', 'i-search'}
    syms = ''.join(ICONS[u] for u in sorted(used) if u in ICONS)
    missing = [u for u in used if u not in ICONS]
    if missing:
        raise SystemExit('missing icons: %s' % missing)
    css, js = ver('/jetup/assets/jetup.css'), ver('/jetup/assets/jetup.js')
    side_js = "try{if(localStorage.getItem('jetup-side')==='off')document.documentElement.classList.add('side-off')}catch(e){}" if docked else ''
    html = f'''<!doctype html>
<html lang="en-ZA" class="{'docked' if docked else 'landing'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="MTG">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0b0912">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website"><meta property="og:site_name" content="MTG TRIBE">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:locale" content="en_ZA">
<meta property="og:image" content="{SITE}{og_img}"><meta property="og:image:width" content="1280"><meta property="og:image:height" content="720"><meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SITE}{og_img}">
<link rel="icon" type="image/png" sizes="32x32" href="/jetup/img/favicon-32.png">
<link rel="apple-touch-icon" href="/jetup/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap">
<link rel="stylesheet" href="/jetup/assets/jetup.css?v={css}">
<script>if(location.protocol==='http:'&&location.hostname==='mtgtribe.com')location.replace('https:'+location.href.slice(5));document.documentElement.classList.add('js');{side_js}</script>
<script type="application/ld+json">{ld}</script>
</head>
<body data-page="{page_name(path)}">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{syms}</defs></svg>
<a class="skip" href="#main">Skip to content</a>
{top_bar(docked)}
{side_menu(path)}
<div class="scrim" id="scrim" aria-hidden="true"></div>
{jump_bar(path, icon)}
<button class="side-tog" id="side-tog" type="button" aria-controls="side" aria-expanded="{'true' if docked else 'false'}" aria-label="{'Close the menu' if docked else 'Open the menu'}" title="{'Close the menu' if docked else 'Open the menu'}">{icon('i-chev-l', '')}</button>
<div class="page">
<main id="main">
{body}
{pager(path)}
</main>
{footer()}
</div>
{PLAYER}
{LIGHTBOX if lightbox else ''}
{thumb_bar(path, icon, JETUP_JOIN)}
{TOTOP}
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="/jetup/assets/jetup.js?v={js}" defer></script>
</body>
</html>
'''
    if re.search('[\u2013\u2014]', html):
        bad = re.findall('.{0,40}[\u2013\u2014].{0,40}', html)
        raise SystemExit('dash found in %s: %s' % (path, bad[:3]))
    if re.search(r'\bluno\b', html, re.I):
        raise SystemExit('Luno mentioned in %s' % path)
    html = label_tables(html)
    html = faq_ids(html)
    if path != '/jetup/glossary/':
        html, gl_keys = mark_terms(html)
        html = html.replace('<button class="totop"', gl_popover(gl_keys) + '\n<button class="totop"', 1)
    if re.search('[\u2013\u2014]', html):
        raise SystemExit('dash found in %s after the glossary and FAQ steps' % path)
    out = os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        f.write(html)
    return out

def phead(icon_name, eyebrow, h1, lede, crumbs_list, chips=None, ped='', extra=''):
    ch = ''
    if chips:
        ch = '<ul class="chips">%s</ul>' % ''.join('<li class="chip">%s</li>' % c for c in chips)
    return f'''<section class="phead"><div class="wrap">
 {crumbs(crumbs_list)}
 <div class="phead-in"><span class="ped {ped}"><b>{icon(icon_name)}</b></span><div>
  <p class="eyebrow">{eyebrow}</p>
  <h1 style="margin-top:12px">{h1}</h1>
  <p class="lede">{lede}</p>
  {ch}{extra}
 </div></div>
</div></section>'''

def join_btn(label='Join JetUP', cls='btn btn-pri'):
    return f'<a class="{cls}" href="{JETUP_JOIN}" target="_blank" rel="sponsored noopener" data-join>{icon("i-rocket2")}{label}</a>'

def join_note(extra=''):
    return f'<p class="jnote">{icon("i-alert")}<span>{JOIN_NOTE}{extra}</span></p>'

def join_cta(title='Ready to start? <span class="lime">Join JetUP.</span>', text='Learn first, then decide for yourself. When you are ready, create your account and follow the sign-up training one tap at a time.'):
    return f'''<section class="sec tight"><div class="wrap"><div class="card tribe joincta rv">
 <span class="wa jw" aria-hidden="true"><img src="/jetup/img/jetup-mark-128.webp" width="54" height="54" alt=""></span>
 <div><h2>{title}</h2><p>{text}</p>{join_note(' Trading is risky: ' + RETAIL_LOSS + ' of retail investor accounts lose money when trading CFDs.')}</div>
 {join_btn()}
</div></div></section>'''

def tribe_cta(title='Don\'t learn this <span class="lime">alone.</span>', text='Action takers learn together. Join the MTG TRIBE on WhatsApp for new trainings, straight answers and the next step, the moment it lands.', join=True):
    return (join_cta() if join else '') + f'''<section class="sec tight"><div class="wrap"><div class="card tribe rv">
 <span class="wa" aria-hidden="true">{icon('i-whatsapp')}</span>
 <div><h2>{title}</h2><p>{text}</p></div>
 <a class="btn btn-lime" href="{GROUP}"><span class="emo" aria-hidden="true">💬</span>Join the tribe, free</a>
</div></div></section>'''
