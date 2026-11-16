# Site update for JetUP explainer #10, "Know your numbers: the Exposure Calculator" (MTG: "Put it live", 14 Nov 2026).
# Placement: the top of the Exposure Calculator page (above the tool, teach first) and the Videos page (after Amplify 24x).
# VideoObject data on both pages; dashboard counts up by one; sitemap dates; a video return check case.
# Run from the repository root, then python3 jetup/_build/build.py.
import datetime, os, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
NAME, COVER = 'jetup-explainer-know-your-numbers', 'cover-explainer-know-your-numbers'
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
sub('jetup/_build/layout.py', [(" 'withdraw': dict(", f""" 'calc': dict(src='/jetup/media/{NAME}.mp4', poster='/jetup/img/{COVER}.webp', jpg='/jetup/img/{COVER}.jpg', dur='{d}', iso='{iso}', orient='h',
   title='Know your numbers: the Exposure Calculator, tap by tap',
   desc="MTG's {d} walkthrough of his free Exposure Calculator for JetUP and TAG Markets: tap the training example ($150 plus the $100 bonus), read the $250 balance and the $6,000 exposure (the size you trade with, not money you own), type your own numbers with 24x Amplify, drag a price move (1% on $6,000 is $60, either direction), and know your lines: 2.5% equals your own $150, about 4.2% the whole balance, and the loss limit of 10% of the starting balance (5% with a community token)."),
 'withdraw': dict(""")])
sub('jetup/_build/pages_tools.py', [
    ("""       [('MTG TRIBE', '/'), ('JetUP Guide', '/jetup/'), ('Exposure Calculator', None)], ped='lime')}
<section class="sec tight" style="padding-top:0"><div class="wrap toolgrid">""",
     f"""       [('MTG TRIBE', '/'), ('JetUP Guide', '/jetup/'), ('Exposure Calculator', None)], ped='lime')}}
<section class="sec tight" style="padding-top:0;padding-bottom:0"><div class="narrow rv" style="margin-bottom:22px">{{laptop('calc', 'New here? Watch the calculator, tap by tap ({d})', eager=True)}}</div></section>
<section class="sec tight" style="padding-top:0"><div class="wrap toolgrid">"""),
    ("[app, ld_video('amplify')],", "[app, ld_video('calc'), ld_video('amplify')],"),
    ("""made simple (2:13)')}<p class="small center" style="margin:8px 0 0">One market stall that trades the size of 24, the $155 money plan, and the calculator, tap by tap.</p></div>""",
     f"""made simple (2:13)')}}<p class="small center" style="margin:8px 0 0">One market stall that trades the size of 24, the $155 money plan, and the calculator, tap by tap.</p></div>
 <div class="rv" style="max-width:980px;margin:0 auto;width:100%"><p class="eyebrow" style="margin-bottom:14px">Know your numbers</p>{{laptop('calc', 'The Exposure Calculator, tap by tap ({d})')}}<p class="small center" style="margin:8px 0 0">Your map before you start: the $6,000 exposure, a 1% move both ways, and your lines to know.</p></div>"""),
    ("ld_video('split'), ld_video('amplify')", "ld_video('split'), ld_video('amplify'), ld_video('calc')"),
])
t = open('dashboard/index.html').read()
m = re.findall(r'(\d+) videos, 6-part training', t); assert len(m) == 1
t = t.replace(f'{m[0]} videos, 6-part training', f'{int(m[0]) + 1} videos, 6-part training')
m = re.findall(r'<b>JetUP explainers</b><small>(\d+) animated explainers</small>', t); assert len(m) == 1
t = t.replace(f'<b>JetUP explainers</b><small>{m[0]} animated explainers</small>', f'<b>JetUP explainers</b><small>{int(m[0]) + 1} animated explainers</small>')
t, n = re.subn(r'"dateModified":"\d{4}-\d\d-\d\d"', f'"dateModified":"{TODAY}"', t); assert n == 1
open('dashboard/index.html', 'w').write(t)
t = open('sitemap-home.xml').read()
for page in ('dashboard/', 'jetup/tools/exposure-calculator/', 'jetup/videos/'):
    t, n = re.subn(r'(<loc>https://mtgtribe\.com/' + re.escape(page) + r'</loc><lastmod>)\d{4}-\d\d-\d\d', r'\g<1>' + TODAY, t); assert n == 1, page
open('sitemap-home.xml', 'w').write(t)
sub('tools/qa/video-return-test.js', [("""  ['JetUP Videos, last video (pop-up)',""",
    """  ['JetUP Exposure Calculator, know your numbers (pop-up)', '/jetup/tools/exposure-calculator/', '[data-video$="know-your-numbers.mp4"]'],
  ['JetUP Videos, last video (pop-up)',""")])
print('explainer #10 placed,', d, iso)
