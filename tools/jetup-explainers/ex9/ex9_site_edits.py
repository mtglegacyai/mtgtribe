# Site update for JetUP explainer #9, "What copying really means" (run only after MTG says "Put it live").
# Placement (the plan's "Placements"): How it works "What copying really means" (top of the section), get-started part 5
# "Connect Sonic AI" (above the community codes), the Videos page (right after the minibus taxi), "Watch the explainer"
# links in the FAQ answers "What are CopyX and Sonic AI?" and "How do I see my trades?", and a link on the get-started
# MetaTrader 5 card. VideoObject data on the three pages with a player. The dashboard counts go up by one, the sitemap
# dates move to today, and tools/qa/video-return-test.js gets the two new players.
# Run from the repository root, then python3 jetup/_build/build.py.
import datetime, os, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
NAME = 'jetup-explainer-what-copying-really-means'
COVER = 'cover-explainer-what-copying-really-means'
shutil.copy(os.path.join(HERE, NAME + '.mp4'), f'jetup/media/{NAME}.mp4')
for ext in ('jpg', 'webp'):
    shutil.copy(os.path.join(HERE, f'{COVER}.{ext}'), f'jetup/img/{COVER}.{ext}')
s = int(round(float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'jetup/media/{NAME}.mp4']).decode())))
d, iso = f'{s // 60}:{s % 60:02d}', f'PT{s // 60}M{s % 60}S'
TODAY = datetime.date.today().isoformat()

def sub(path, pairs):
    t = open(path).read()
    for a, b in pairs:
        if t.count(a) != 1: raise SystemExit(f'{path}: expected once ({t.count(a)}): {a[:90]}')
        t = t.replace(a, b)
    open(path, 'w').write(t)

sub('jetup/_build/layout.py', [(" 'withdraw': dict(", f""" 'copy': dict(src='/jetup/media/{NAME}.mp4', poster='/jetup/img/{COVER}.webp', jpg='/jetup/img/{COVER}.jpg', dur='{d}', iso='{iso}', orient='h',
   title='What "copying" really means: CopyX copy trading explained with a cooking class',
   desc="MTG's {d} explainer with a cooking class: the chef at the front is Sonic AI, the strategy, and your own pot is your own account at TAG Markets, in your name. CopyX copies the strategy's trades into your account automatically, so you don't even lift the spoon: you don't pick the trades. You pick the strategy, how much to put in, and when to stop. Check Sonic AI's track record on Myfxbook first, read the terms (a 30% performance fee, taken from profits only), and watch every trade in MetaTrader 5 with your investor password, read only."),
 'withdraw': dict(""")])

sub('jetup/_build/pages_learn.py', [
    # How it works, "What copying really means": the player at the top of the section, the way "Who does what" carries the taxi
    (""" {section('copy', 'Copy trading', 'What "copying" really means', '''
<p>When you connect Sonic AI on CopyX,""",
     f""" {{section('copy', 'Copy trading', 'What "copying" really means', '''
<div style="margin:4px 0 18px">''' + laptop('copy', 'What "copying" really means, explained by MTG ({d})') + '''</div>
<p>When you connect Sonic AI on CopyX,"""),
    ("[ld_video('who'), ld_video('split'), ld_video('amplify'), ld_video('withdraw'), ld_video('sonic')]",
     "[ld_video('who'), ld_video('copy'), ld_video('split'), ld_video('amplify'), ld_video('withdraw'), ld_video('sonic')]"),
])

sub('jetup/_build/pages_start.py', [
    # part 5: the player first, above the community codes, the way part 6 carries the promo player
    ("""      extra_before=codes,""",
     f"""      extra_before='<div style="margin:0 0 18px">' + laptop('copy', 'Watch first: what copying really means ({d})') + '</div>' + codes,"""),
    ("ld = [ld_video('training'), ld_video('tut1'), ld_video('tut2'), ld_video('tut3'), ld_video('promo'), howto]",
     "ld = [ld_video('training'), ld_video('tut1'), ld_video('tut2'), ld_video('tut3'), ld_video('copy'), ld_video('promo'), howto]"),
    # the MetaTrader 5 card keeps the set-up steps the video leaves out, and links to the glass lid
    ("""<p class="muted">A read-only view of your own account. You can watch, not trade or withdraw.</p>""",
     f"""<p class="muted">A read-only view of your own account. You can watch, not trade or withdraw. <a href="/jetup/how-it-works/#copy">Watch the glass lid, explained by MTG ({d})</a></p>"""),
])

sub('jetup/_build/pages_tools.py', [
    # Videos page: right after the minibus taxi, so who is who is followed by what copying does
    ("""JetUP, TAG Markets, CopyX, Sonic AI and you, as one minibus taxi.</p></div>""",
     f"""JetUP, TAG Markets, CopyX, Sonic AI and you, as one minibus taxi.</p></div>
 <div class="rv" style="max-width:980px;margin:0 auto;width:100%"><p class="eyebrow" style="margin-bottom:14px">The cooking class</p>{{laptop('copy', 'What "copying" really means ({d})')}}<p class="small center" style="margin:8px 0 0">A cooking class: the strategy's trades get copied into your own account, in your name, you make three choices, and MetaTrader 5 is your glass lid.</p></div>"""),
    ("ld_video('simple'), ld_video('who'), ld_video('promo')", "ld_video('simple'), ld_video('who'), ld_video('copy'), ld_video('promo')"),
    # FAQ: links to the explainer, the way "How do withdrawals work?" links to its explainer
    ("""and its track record is published on Myfxbook."),""",
     f"""and its track record is published on Myfxbook. <a href='/jetup/how-it-works/#copy'>Watch the {d} explainer</a>."),"""),
    ("""Sonic usually trades two or three times a day. Steps: mtgtribe.com/jetup/get-started/#mt5"),""",
     f"""Sonic usually trades two or three times a day. <a href='/jetup/how-it-works/#copy'>Watch the {d} explainer</a>. Steps: mtgtribe.com/jetup/get-started/#mt5"),"""),
])

# Dashboard: the JetUP card and the Learn tile count one more video
t = open('dashboard/index.html').read()
m = re.findall(r'(\d+) videos, 6-part training', t); assert len(m) == 1, m
t = t.replace(f'{m[0]} videos, 6-part training', f'{int(m[0]) + 1} videos, 6-part training')
m = re.findall(r'<b>JetUP explainers</b><small>(\d+) animated explainers</small>', t); assert len(m) == 1, m
t = t.replace(f'<b>JetUP explainers</b><small>{m[0]} animated explainers</small>', f'<b>JetUP explainers</b><small>{int(m[0]) + 1} animated explainers</small>')
t, n = re.subn(r'"dateModified":"\d{4}-\d\d-\d\d"', f'"dateModified":"{TODAY}"', t); assert n == 1, n
open('dashboard/index.html', 'w').write(t)

# Sitemap: the pages that changed
t = open('sitemap-home.xml').read()
for page in ('dashboard/', 'jetup/get-started/', 'jetup/how-it-works/', 'jetup/videos/', 'jetup/faq/'):
    t, n = re.subn(r'(<loc>https://mtgtribe\.com/' + re.escape(page) + r'</loc><lastmod>)\d{4}-\d\d-\d\d', r'\g<1>' + TODAY, t)
    assert n == 1, (page, n)
open('sitemap-home.xml', 'w').write(t)

# Video return check: the two new players
sub('tools/qa/video-return-test.js', [(
    """  ['JetUP Videos, last video (pop-up)',""",
    """  ['JetUP How It Works, what copying really means (pop-up)', '/jetup/how-it-works/', '[data-video$="what-copying-really-means.mp4"]'],
  ['JetUP Get started, part 5, what copying really means (pop-up)', '/jetup/get-started/', '#part-5 [data-video$="what-copying-really-means.mp4"]'],
  ['JetUP Videos, last video (pop-up)',""")])
print('explainer #9 placed,', d, iso)
