# Put BIX's 10-second card video at the top of /jetup/bix-card/ (MTG, 8 Nov 2026). Usage: python3 bix_site_edits.py <repo>
import sys, os
R = sys.argv[1]

def edit(rel, pairs):
    p = os.path.join(R, rel); s = open(p).read()
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a[:70])
        s = s.replace(a, b)
    open(p, 'w').write(s)

edit('jetup/_build/layout.py', [(
" '5checks': dict(",
""" 'bix': dict(src='/jetup/media/bix-card-in-10-seconds.mp4', poster='/jetup/img/cover-bix-card.webp', jpg='/jetup/img/cover-bix-card.jpg', dur='0:10', iso='PT10S', orient='v',
   title="The BIX Card in 10 seconds: BIX's own clip",
   desc="BIX's own short clip: the lime BIX Visa card and the BixPay app, the self-custody crypto wallet listed in the JetUP portal."),
 '5checks': dict(""")])

edit('jetup/_build/pages_learn.py', [
 ("""<section class="sec tight" style="padding-top:0"><div class="narrow stack" style="gap:20px">
 <div class="call info rv">{icon('i-info2')}<p><b>MTG's BIX Card link is coming.</b> Until then, install BixPay from the official bix.fi website. A full BIX Card video is planned.</p></div>""",
  """<section class="sec tight" style="padding-top:0"><div class="narrow stack" style="gap:20px">
 <div class="card pad rv vrow" id="bix-video">
  <div>{phone('bix')}</div>
  <div><p class="eyebrow">BIX's own clip · 0:10</p><h2 class="h2" style="margin:10px 0 12px;font-size:clamp(1.7rem,3.4vw,2.3rem)">See the BIX Card <span class="grad">in 10 seconds</span></h2>
   <p class="lede">The lime BIX Visa card and the BixPay app. Top up the card from your self-custody crypto wallet, then pay anywhere Visa works, or add it to Apple Pay or Google Pay.</p>
   <p class="small" style="margin-top:12px">This is BIX's own promo clip. The balance and the purchases on the screen are BIX's demo, not a real account.</p>
   <div class="ctas" style="margin-top:16px"><a class="btn btn-pri" href="#setup">{icon('i-rocket2')}Set it up in 5 steps</a><a class="btn btn-ghost" href="#link">{icon('i-link')}Link it to JetUP</a></div></div>
 </div>
 <div class="call info rv">{icon('i-info2')}<p><b>MTG's BIX Card link is coming.</b> Until then, install BixPay from the official bix.fi website. A step-by-step BIX Card video is planned.</p></div>"""),
 ("""                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('BIX Card', None)],
                keywords='BIX Card,""",
  """                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('BIX Card', None)], [ld_video('bix')],
                keywords='BIX Card,"""),
])
print('bix site edits applied to', R)
