# Site update for JetUP explainer #8, "Getting your money out" (MTG: "Put it live", 12 Nov 2026).
# Placement: How it works "Withdrawals" (top of the section), the 5 Checks page check 5 "Can I get out?", the Videos page
# (after the partner plan), and a link from the FAQ answer "How do withdrawals work?". VideoObject data on the three
# pages with a player. Run from the repository root, then python3 jetup/_build/build.py.
import os, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
NAME = 'jetup-explainer-getting-your-money-out'
shutil.copy(os.path.join(HERE, NAME + '.mp4'), f'jetup/media/{NAME}.mp4')
shutil.copy(os.path.join(HERE, f'cover-explainer-getting-your-money-out.jpg'), 'jetup/img/cover-explainer-getting-your-money-out.jpg')
shutil.copy(os.path.join(HERE, f'cover-explainer-getting-your-money-out.webp'), 'jetup/img/cover-explainer-getting-your-money-out.webp')
s = int(round(float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'jetup/media/{NAME}.mp4']).decode())))
d, iso = f'{s // 60}:{s % 60:02d}', f'PT{s // 60}M{s % 60}S'

def sub(path, pairs):
    t = open(path).read()
    for a, b in pairs:
        if t.count(a) != 1: raise SystemExit(f'{path}: expected once ({t.count(a)}): {a[:90]}')
        t = t.replace(a, b)
    open(path, 'w').write(t)

sub('jetup/_build/layout.py', [(" '5checks': dict(", f""" 'withdraw': dict(src='/jetup/media/{NAME}.mp4', poster='/jetup/img/cover-explainer-getting-your-money-out.webp', jpg='/jetup/img/cover-explainer-getting-your-money-out.jpg', dur='{d}', iso='{iso}', orient='h',
   title="Getting your money out: profits any time, and the promo's 12 months",
   desc="MTG's {d} explainer with a fruit tree in your own backyard: your TAG Markets account is in your own name, the tree is your own money and the fruit is your profit, which can be withdrawn any time. The promo's $100 bonus is released after 12 months, and taking your own money out before then ends the promo. Withdrawals go through the broker to your crypto wallet, on the same network on both sides, in about 48 hours on average (JetUP's one-pager). Start with one small withdrawal."),
 '5checks': dict(""")])

sub('jetup/_build/pages_learn.py', [
    # 5 Checks page, check 5: the player under the list, the way check 4 carries the Amplify player
    (""" <li>📲 Promo amounts change, so <b>check the current rules in your dashboard</b> before you start.</li>
</ul>
<div class="call lime">""",
     f""" <li>📲 Promo amounts change, so <b>check the current rules in your dashboard</b> before you start.</li>
</ul>
<div style="margin:16px 0 18px">{{laptop('withdraw', 'Watch it: getting your money out ({d})')}}</div>
<div class="call lime">"""),
    ("[ld_video('5checks'), ld_video('amplify'), ld_faq(faq, SITE + path)]",
     "[ld_video('5checks'), ld_video('amplify'), ld_video('withdraw'), ld_faq(faq, SITE + path)]"),
    # How it works, "Withdrawals": the player at the top of the section, like Amplify 24x
    (""" {section('withdraw', 'Getting money out', 'Withdrawals', '''
<ul>""",
     f""" {{section('withdraw', 'Getting money out', 'Withdrawals', f'''
<div style="margin:4px 0 18px">{{laptop('withdraw', 'Getting your money out, explained by MTG ({d})')}}</div>
<ul>"""),
    ("[ld_video('who'), ld_video('split'), ld_video('amplify'), ld_video('sonic')]",
     "[ld_video('who'), ld_video('split'), ld_video('amplify'), ld_video('withdraw'), ld_video('sonic')]"),
])

sub('jetup/_build/pages_tools.py', [
    # Videos page: after the partner plan
    ("""Ten glass floors and an access card: how partner levels open, and what open levels pay.</p></div>""",
     f"""Ten glass floors and an access card: how partner levels open, and what open levels pay.</p></div>
 <div class="rv" style="max-width:980px;margin:0 auto;width:100%"><p class="eyebrow" style="margin-bottom:14px">Getting your money out</p>{{laptop('withdraw', 'Getting your money out, explained by MTG ({d})')}}<p class="small center" style="margin:8px 0 0">A fruit tree in your own backyard: withdraw profits any time, the promo's 12-month rule, and a small withdrawal first.</p></div>"""),
    ("ld_video('partnerplan'), ld_video('5checks')", "ld_video('partnerplan'), ld_video('withdraw'), ld_video('5checks')"),
    # FAQ: a link to the explainer, the way "What is Amplify 24x?" links to its explainer
    ("""With the Dennis promo, taking your own money out before 12 months ends the promo. Test a small withdrawal early."),""",
     f"""With the Dennis promo, taking your own money out before 12 months ends the promo. Test a small withdrawal early. <a href='/jetup/how-it-works/#withdraw'>Watch the {d} explainer</a>."),"""),
])
print('explainer #8 placed,', d, iso)
