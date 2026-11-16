# Site update for JetUP explainer #6, "The partner plan: the rule most people miss" (MTG: "Put it live", 11 Nov 2026).
# Placement: top of the Partner Plan page, the Videos page, and a link from the FAQ answer "Do I have to build a team?".
import shutil, subprocess
from PIL import Image
X = '/tmp/claude-0/-home-user/a6cc0db9-d96c-55e0-8645-be8a10935550/scratchpad/ex6'
shutil.copy(f'{X}/JetUP_Explainer_6_Partner_Plan_16x9.mp4', 'jetup/media/jetup-explainer-partner-plan.mp4')
im = Image.open(f'{X}/cover.png').convert('RGB')
im.save('jetup/img/cover-explainer-partner-plan.jpg', quality=88); im.resize((1280, 720), Image.LANCZOS).save('jetup/img/cover-explainer-partner-plan.webp', quality=84)
s = int(round(float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'jetup/media/jetup-explainer-partner-plan.mp4']).decode())))
d, iso = f'{s // 60}:{s % 60:02d}', f'PT{s // 60}M{s % 60}S'
def sub(path, pairs):
    t = open(path).read()
    for a, b in pairs:
        if t.count(a) != 1: raise SystemExit(f'{path}: expected once ({t.count(a)}): {a[:90]}')
        t = t.replace(a, b)
    open(path, 'w').write(t)
sub('jetup/_build/layout.py', [(" '5checks': dict(", f""" 'partnerplan': dict(src='/jetup/media/jetup-explainer-partner-plan.mp4', poster='/jetup/img/cover-explainer-partner-plan.webp', jpg='/jetup/img/cover-explainer-partner-plan.jpg', dur='{d}', iso='{iso}', orient='h',
   title='The partner plan: the rule most people miss',
   desc="MTG's {d} explainer with ten glass floors and an access card: JetUP pays partners across 10 levels, but $250 of active trading opens 3. With 1 to 3 direct partners it stays 3; from the 4th direct partner each new one opens the next level, and 10 open all 10. Lot commission up to $8.00 per lot and Profit Share of 1.5% per open level, with JetUP's own figures."),
 '5checks': dict(""")])
sub('jetup/_build/pages_learn.py', [
    ("""<section class="sec tight" style="padding-top:0"><div class="narrow stack" style="gap:20px">
 <div class="call info rv">{icon('i-info2')}<p><b>Before any number:</b>""",
     f"""<section class="sec tight" style="padding-top:0"><div class="narrow stack" style="gap:20px">
 <div class="rv">{{laptop('partnerplan', 'The rule most people miss, explained by MTG ({d})', eager=True)}}</div>
 <div class="call info rv">{{icon('i-info2')}}<p><b>Before any number:</b>"""),
    ("[ld_faq(faq, SITE + path), ld_video('profitshare')]", "[ld_faq(faq, SITE + path), ld_video('partnerplan'), ld_video('profitshare')]"),
])
sub('jetup/_build/pages_tools.py', [
    ("""One market stall that trades the size of 24, the $155 money plan, and the calculator, tap by tap.</p></div>""",
     f"""One market stall that trades the size of 24, the $155 money plan, and the calculator, tap by tap.</p></div>
 <div class="rv" style="max-width:980px;margin:0 auto;width:100%"><p class="eyebrow" style="margin-bottom:14px">The partner plan</p>{{laptop('partnerplan', 'The partner plan: the rule most people miss ({d})')}}<p class="small center" style="margin:8px 0 0">Ten glass floors and an access card: how partner levels open, and what open levels pay.</p></div>"""),
    ("ld_video('split'), ld_video('amplify'), ld_video('5checks')", "ld_video('split'), ld_video('amplify'), ld_video('partnerplan'), ld_video('5checks')"),
    ("""JetUP's own founder says the big money comes from building a team. What a partner earns can be zero."),""",
     f"""JetUP's own founder says the big money comes from building a team. What a partner earns can be zero. <a href='/jetup/partner-plan/'>Watch how partner levels open ({d})</a>.\"),"""),
])
print('explainer #6 placed,', d, iso)
