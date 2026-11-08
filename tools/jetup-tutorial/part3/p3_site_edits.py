# Apply the Part 3 (KYC) website changes to the JetUP builders in the repo given as argv[1]. Safe to run on main or on the
# working branch (independent of the Sonic video preview). Usage: python3 p3_site_edits.py /home/user/mtgtribe DUR ISO
import sys, os
R, DUR, ISO = sys.argv[1], sys.argv[2], sys.argv[3]

def edit(rel, pairs):
    p = os.path.join(R, rel); s = open(p).read()
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a[:70])
        s = s.replace(a, b)
    open(p, 'w').write(s)

edit('jetup/_build/layout.py', [(
" 'tut2': dict(",
""" 'tut3': dict(src='/jetup/media/jetup-tutorial-part-3-verify-identity.mp4', poster='/jetup/img/cover-tutorial-part-3.webp', jpg='/jetup/img/cover-tutorial-part-3.jpg', dur='%s', iso='%s', orient='v',
   title='JetUP step by step, part 3: verify your identity (KYC)',
   desc="MTG's own recording, tap by tap: upload documents on TAG Markets, Sumsub's check, your country, your Sumsub ID email and code, Create my account, Identity Card, double-sided, the tips, allow the camera, then the ID scan and the selfie."),
 'tut2': dict(""" % (DUR, ISO))])

OLD_P3_HEAD = """    p3 = part(3, 'Verify your identity', "TAG Markets asks a few questions, then checks your ID.", [
        'Answer TAG Markets\\' questions honestly: your income, your net worth, your investment goal, and whether you understand the risks.',
        'Read their reminder: not for residents of the European Union, you may have fewer protections than with a local provider, and %s of retail investor accounts lose money when trading CFDs.' % RETAIL_LOSS,
        'The identity check is by Sumsub. Tap ' + k('Continue') + ", scan your ID, driver's licence or passport, and do the face scan. Use your phone for this.",
      ], [('06', "TAG Markets' questions and reminder"), ('07', 'The Sumsub identity check')],
      'your KYC is accepted and you can log in to TAG Markets.',
      extra_after='<p class="call info" style="margin-top:12px">%s<span><b>CFD</b> means contract for difference: you trade a price movement without owning the asset.</span></p>' % icon('i-info2'))"""
NEW_P3 = """    p3 = part(3, 'Verify your identity', "Sumsub checks your ID and a selfie for TAG Markets.", [
        'On your TAG Markets dashboard (<b>portal.tagmarkets.com</b>), tap ' + k('upload documents') + ' in "Please complete your KYC verification in order to make a deposit".',
        'Sumsub runs the identity check for TAG Markets. You opened it from TAG Markets, so tap ' + k('Continue') + '.',
        'Confirm your country of residence and tap ' + k('Agree and continue') + '.',
        'Under "Get verified faster with Sumsub ID", enter <b>the same email you have used from the start</b> and tap ' + k('Start verification') + '. Type the 6-digit code Sumsub emails you (not in your inbox? check spam or junk). Never share this code with anyone.',
        'Read the consent, tick the box and tap ' + k('Create my account') + '. You see "Sumsub ID account successfully created": tap ' + k('Continue verification') + '.',
        'Choose your issuing country and your document (MTG chose ' + k('Identity Card') + '). If it has two sides, tick ' + k('My document is double-sided') + ' and tap ' + k('Continue') + '. Read the tips (a well lit room, no reflections, never edit the images) and tap ' + k('Continue') + '.',
        'When the browser asks to use the camera, tap ' + k('Allow') + '. Hold your ID inside the frame: it takes the photo by itself (move the phone back a little if it does not). Front, then back.',
        'Step 2 is a quick selfie: a well lit place, your face in the frame, no hat, glasses or mask. Hold still until you see ' + k('All set') + '.',
        'TAG Markets may also ask a few questions (your income, net worth, investment goal and whether you understand the risks): answer honestly. Read their reminder: not for residents of the European Union, you may have fewer protections than with a local provider, and %%s of retail investor accounts lose money when trading CFDs.' %% RETAIL_LOSS,
      ], [('06', "TAG Markets' questions and reminder"), ('07', 'The Sumsub identity check')],
      'you see "All set". TAG Markets reviews your documents, and once you are verified you can make your deposit (part 4).',
      extra_before='<div class="pvid">' + phone('tut3', "Watch MTG do part 3 (%s)") + '</div>',
      extra_after='<p class="call warn" style="margin-top:12px">%%s<span><b>"This site can\\'t ask for your permission"?</b> Close screen recorders and chat bubbles (for example WhatsApp), then tap Try again and Allow.</span></p><p class="call warn" style="margin-top:10px">%%s<span><b>"Documents submitted on another profile"?</b> You already have a TAG Markets profile with these documents. One person, one profile: do not open a second account. Ask your sponsor or TAG Markets support.</span></p><p class="call info" style="margin-top:10px">%%s<span><b>CFD</b> means contract for difference: you trade a price movement without owning the asset.</span></p>' %% (icon('i-alert'), icon('i-alert'), icon('i-info2')))""" % DUR

edit('jetup/_build/pages_start.py', [
 (OLD_P3_HEAD, NEW_P3),
 ("""    <div class="vpart">{phone('tut2')}<b>Part 2</b><small>Link JetUP to TAG Markets</small></div>
    <div class="vsoon"><b>Parts 3 to 6</b><small>KYC, deposit, Sonic AI and the promo: coming next.</small></div></div>""",
  """    <div class="vpart">{phone('tut2')}<b>Part 2</b><small>Link JetUP to TAG Markets</small></div>
    <div class="vpart">{phone('tut3')}<b>Part 3</b><small>Verify your identity (KYC)</small></div>
    <div class="vsoon"><b>Parts 4 to 6</b><small>Deposit, Sonic AI and the promo: coming next.</small></div></div>"""),
 ("ld_video('tut1'), ld_video('tut2'), howto]", "ld_video('tut1'), ld_video('tut2'), ld_video('tut3'), howto]"),
])

edit('jetup/_build/pages_tools.py', [
 ("""   <div class="vpart">{phone('tut2')}<b>Part 2</b><small>Link JetUP to TAG Markets</small></div>
   <div class="vsoon"><b>Parts 3 to 6</b><small>KYC, deposit, Sonic AI and the promo: coming next.</small></div></div>""",
  """   <div class="vpart">{phone('tut2')}<b>Part 2</b><small>Link JetUP to TAG Markets</small></div>
   <div class="vpart">{phone('tut3')}<b>Part 3</b><small>Verify your identity (KYC)</small></div>
   <div class="vsoon"><b>Parts 4 to 6</b><small>Deposit, Sonic AI and the promo: coming next.</small></div></div>"""),
 ("ld_video('tut1'), ld_video('tut2'), ", "ld_video('tut1'), ld_video('tut2'), ld_video('tut3'), "),
])
print('part 3 site edits applied to', R)
