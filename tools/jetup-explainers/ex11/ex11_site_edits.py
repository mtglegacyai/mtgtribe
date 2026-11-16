# Site update for JetUP explainer #11, "The Infinity Bonus: two strong wheels" (MTG: "Put it live", 15 Nov 2026).
# Placement: the Partner Plan "Infinity Bonus" section (top) and the Videos page (after the partner plan). VideoObject data
# on both pages; dashboard counts up by one; sitemap dates; a video return check case.
# Run from the repository root, then python3 jetup/_build/build.py.
import datetime, os, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
NAME, COVER = 'jetup-explainer-infinity-bonus', 'cover-explainer-infinity-bonus'
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
sub('jetup/_build/layout.py', [(" 'withdraw': dict(", f""" 'infinity': dict(src='/jetup/media/{NAME}.mp4', poster='/jetup/img/{COVER}.webp', jpg='/jetup/img/{COVER}.jpg', dur='{d}', iso='{iso}', orient='h',
   title='The Infinity Bonus: two strong wheels, the 50% rule and the difference rule',
   desc="MTG's {d} explainer of JetUP's Infinity Bonus with a bicycle with gears: a leadership bonus on top of the Profit Share, from level 1 with no depth limit; the rate is set by the team's new volume each month, from 1.5% at $50K to 7.5% at $40M, paid once a month; the 50% rule (the strongest line counts for at most half, so Infinity needs two strong lines) and the difference rule (3% minus a partner's 1.5% leaves 1.5% on their structure). JetUP's own figures."),
 'withdraw': dict(""")])
sub('jetup/_build/pages_learn.py', [
    ("""{section('infinity', 'Income 3 · Infinity Bonus', 'A leadership bonus, no depth limit', f'''
<p>An extra percentage""",
     f"""{{section('infinity', 'Income 3 · Infinity Bonus', 'A leadership bonus, no depth limit', f'''
<div style="margin:4px 0 18px">{{laptop('infinity', 'The Infinity Bonus, explained by MTG ({d})')}}</div>
<p>An extra percentage"""),
    ("ld_video('partnerplan'), ld_video('profitshare')", "ld_video('partnerplan'), ld_video('infinity'), ld_video('profitshare')"),
])
sub('jetup/_build/pages_tools.py', [
    ("""what open levels pay.</p></div>""",
     f"""what open levels pay.</p></div>
 <div class="rv" style="max-width:980px;margin:0 auto;width:100%"><p class="eyebrow" style="margin-bottom:14px">The Infinity Bonus</p>{{laptop('infinity', 'The Infinity Bonus: two strong wheels ({d})')}}<p class="small center" style="margin:8px 0 0">A bicycle with gears: no depth limit, a monthly rate from 1.5% to 7.5%, the 50% rule and the difference rule.</p></div>"""),
    ("ld_video('partnerplan'), ld_video('withdraw')", "ld_video('partnerplan'), ld_video('infinity'), ld_video('withdraw')"),
])
t = open('dashboard/index.html').read()
m = re.findall(r'(\d+) videos, 6-part training', t); assert len(m) == 1
t = t.replace(f'{m[0]} videos, 6-part training', f'{int(m[0]) + 1} videos, 6-part training')
m = re.findall(r'<b>JetUP explainers</b><small>(\d+) animated explainers</small>', t); assert len(m) == 1
t = t.replace(f'<b>JetUP explainers</b><small>{m[0]} animated explainers</small>', f'<b>JetUP explainers</b><small>{int(m[0]) + 1} animated explainers</small>')
t, n = re.subn(r'"dateModified":"\d{4}-\d\d-\d\d"', f'"dateModified":"{TODAY}"', t); assert n == 1
open('dashboard/index.html', 'w').write(t)
t = open('sitemap-home.xml').read()
for page in ('dashboard/', 'jetup/partner-plan/', 'jetup/videos/'):
    t, n = re.subn(r'(<loc>https://mtgtribe\.com/' + re.escape(page) + r'</loc><lastmod>)\d{4}-\d\d-\d\d', r'\g<1>' + TODAY, t); assert n == 1, page
open('sitemap-home.xml', 'w').write(t)
sub('tools/qa/video-return-test.js', [("""  ['JetUP Videos, last video (pop-up)',""",
    """  ['JetUP Partner Plan, the Infinity Bonus (pop-up)', '/jetup/partner-plan/', '[data-video$="infinity-bonus.mp4"]'],
  ['JetUP Videos, last video (pop-up)',""")])
print('explainer #11 placed,', d, iso)
