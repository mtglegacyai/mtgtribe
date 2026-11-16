# Part 3 (verify your identity, KYC): greeting, "In this video", the steps (fully voiced), recap, next video, outro.
# Exec'd by make_tl_p3.py. Times are output seconds; x, y are screen-recording pixels (720 x 1562); chip y is window pixels.
# The camera steps could not be recorded (the screen recorder blocks the camera), so they are recreated cards (cam1, cam2).
def ring(t0, t1, box, gold=False):
    rings.append(dict(t0=round(t0, 3), t1=round(t1, 3), x0=box[0], y0=box[1], x1=box[2], y1=box[3], gold=gold))
def tap(t, x, y):
    taps.append(dict(t=round(t, 3), x=x, y=y))
def chip(t0, t1, text, y, gold=False):
    chips.append(dict(t0=round(t0, 3), t1=round(t1, 3), text=text, y=y, gold=gold))
K = lambda s: f'<span class="k">{s}</span>'
CHK = '<span class="em">✅</span>'
BAR = (10, 96, 710, 180)

# ---- step 1: tap upload documents on the TAG Markets dashboard (P) ----
TAPU = cue('s_dash', 'upload') + .15
shot('P', 33.3, 37.8, 71.75 - (TAPU - 33.3), 1.0, [[33.3, 360, 560, 1.29]])
ring(33.45, 35.2, BAR)
chip(33.55, 35.2, 'Check the address: portal.tagmarkets.com', 520)
ring(35.25, TAPU + .25, (20, 560, 700, 698), gold=True)
tap(TAPU, 500, 649)

# ---- step 2: Sumsub's check for TAG Markets, Continue (Q) ----
TAPC = cue('s_cont', 'Continue') + .1
shot('Q', 37.8, 44.2, 104.95 - (TAPC - 37.8), 1.0, [[37.8, 360, 900, 1.29]], flash=True)
ring(cue('sumsub', 'identity') - .1, cue('s_cont', 'so') - .1, (80, 690, 640, 1090))
chip(cue('sumsub', 'identity'), cue('s_cont', 'so') - .1, 'Verification for TAG Markets Ltd', 1060)
ring(cue('s_cont', 'so') - .05, TAPC + .3, (70, 1112, 650, 1214), gold=True)
tap(TAPC, 360, 1163)

# ---- step 3: country of residence, Agree and continue (Q) ----
TAPA = cue('s_country', 'Agree') + .1
shot('Q', 44.2, 48.6, 112.0 - (TAPA - 44.2), 1.0, [[44.2, 360, 980, 1.29]])
ring(44.35, TAPA - .3, (50, 765, 670, 866))
chip(44.4, TAPA - .3, 'Your country of residence', 70)
ring(TAPA - .25, TAPA + .3, (50, 1200, 670, 1304), gold=True)
tap(TAPA, 360, 1252)

# ---- step 4: Sumsub ID with the same email, Start verification (Q, typing covered) ----
shot('Q', 48.6, 51.3, 113.6, 1.0, [[48.6, 360, 980, 1.29]])
ring(48.75, 51.25, (104, 945, 652, 1314))
chip(48.8, 51.25, 'Get verified faster with Sumsub ID', 70)
shot('Q', 51.3, 54.6, 129.3, (138.0 - 129.3) / 3.3, [[51.3, 360, 700, 1.29]])
chip(51.4, 54.5, 'The same email you used from the start', 1060, gold=True)
TAPS = 54.6 + (144.05 - 143.0)
shot('Q', 54.6, 57.4, 143.0, 1.0, [[54.6, 360, 600, 1.29]])
ring(54.7, TAPS + .2, (70, 580, 650, 688), gold=True)
tap(TAPS, 360, 634)

# ---- step 5: the 6-digit code from Sumsub (R, then S typing covered) ----
shot('R', 57.4, 61.0, 152.2, 1.0, [[57.4, 360, 900, 1.29]], flash=True)
ring(57.6, 60.9, (70, 1140, 650, 1250))
chip(cue('s_code', 'emails') - .1, 60.9, 'Check your email for the 6-digit code', 70)
shot('S', 61.0, 63.0, 182.45, 1.0, [[61.0, 360, 700, 1.29]])
chip(cue('s_code', 'never') - .1, 63.0, '🔒 Never share this code', 1060, gold=True)
shot('S', 63.0, 66.4, 190.75, (195.8 - 190.75) / 3.4, [[63.0, 360, 700, 1.29]])
chip(63.3, 66.3, 'Not in your inbox? Check spam or junk', 1060)

# ---- step 6: consent, Create my account, Sumsub ID created, Continue verification (T) ----
SP6 = (209.45 - 204.0) / 4.0
shot('T', 66.4, 70.4, 204.0, SP6, [[66.4, 360, 900, 1.29]], flash=True)
chip(66.6, cue('s_save', 'Create') - .1, 'Read the consent, then tick the box', 70)
TAPK = out_t(66.4, 204.0, SP6, 209.2)
ring(TAPK - .6, TAPK + .3, (60, 990, 660, 1100), gold=True)
tap(TAPK, 360, 1045)
TAPV = cue('s_created', 'Continue') + .1
shot('T', 70.4, 75.4, 221.6 - (TAPV - 70.4), 1.0, [[70.4, 360, 900, 1.29]])
C['suc_sumsub'] = cue('s_created', 'Sumsub')
ring(C['suc_sumsub'] - .1, TAPV - .4, (40, 750, 680, 890))
chip(C['suc_sumsub'], TAPV - .4, f'{CHK} Sumsub ID account created', 70)
ring(TAPV - .35, TAPV + .3, (70, 1112, 650, 1214), gold=True)
tap(TAPV, 360, 1163)

# ---- step 7: Identity Card, double-sided, Continue (U) ----
TAPI = cue('s_doc', 'Identity') + .1
shot('U', 75.4, 79.3, 231.8 - (TAPI - 75.4), 1.0, [[75.4, 360, 900, 1.29]], flash=True)
ring(75.55, TAPI - .2, (45, 715, 675, 865))
chip(75.6, TAPI - .2, 'Issuing country', 70)
ring(TAPI - .2, 79.25, (70, 1050, 650, 1144), gold=True)
tap(TAPI, 593, 1096)
TAPD = cue('s_double', 'tick') + .3
U0 = 243.2 - (TAPD - 79.3)
shot('U', 79.3, 84.6, U0, 1.0, [[79.3, 360, 820, 1.29]])
ring(79.45, TAPD + .4, (70, 1030, 680, 1080))
chip(79.5, TAPD + .4, 'Two sides? Tick double-sided', 70, gold=True)
TAPN = out_t(79.3, U0, 1.0, 246.1)
ring(TAPN - .5, min(TAPN + .3, 84.55), (70, 1112, 650, 1214), gold=True)
tap(TAPN, 360, 1163)

# ---- step 8: the tips, Continue; Allow the camera; the "can't ask for your permission" message (U, V) ----
SP8 = (249.6 - 246.7) / (91.6 - 84.6)
shot('U', 84.6, 91.6, 246.7, SP8, [[84.6, 360, 900, 1.29]])
ring(cue('s_ready', 'tips') - .1, cue('s_ready', 'Tap') - .2, (60, 690, 670, 1060))
chip(cue('s_ready', 'tips'), cue('s_ready', 'Tap') - .2, 'Well lit, no reflections, no edits', 70)
TAPR = cue('s_ready', 'Continue') + .1
ring(TAPR - .5, TAPR + .3, (70, 1152, 650, 1256), gold=True)
tap(TAPR, 360, 1204)
TAPL = cue('s_allow', 'Allow') + .1
shot('V', 91.6, 95.0, 277.4, 1.0, [[91.6, 360, 820, 1.29]], flash=True)
ring(91.75, TAPL - .3, (30, 480, 700, 1100))
chip(91.8, TAPL - .3, 'Your browser asks to use the camera', 70)
ring(TAPL - .3, 94.95, (500, 985, 660, 1050), gold=True)
tap(TAPL, 577, 1017)
shot('V', 95.0, 98.4, 262.0, .8, [[95.0, 360, 820, 1.29]], flash=True)
ring(95.15, 98.3, (25, 560, 695, 990))
chip(95.2, 98.3, '"This site can\'t ask for your permission"', 70)
# tip card 98.2 to 102.4 (s_bubble, second half)

# ---- step 9: scan the ID, front and back (cam1), the selfie (cam2), All set ----
C['shot1'] = cue('s_scan', 'itself') - .3
C['back'] = cue('s_scan', 'front') + .35
C['shot2'] = C['back'] + .6
C['hold'] = vstart['s_hold'] - .1
C['allset'] = cue('s_hold', 'All')
C['subdone'] = cue('s_done', 'TAG')
C['suc_allset'] = C['allset']
C['mailtap'] = -100

STEPS = [
    dict(t0=33.3, t1=37.8, n=1, title=f'Tap {K("upload documents")}', sub='On your TAG Markets dashboard, at portal.tagmarkets.com.'),
    dict(t0=37.8, t1=44.2, n=2, title=f'Tap {K("Continue")}', sub='Sumsub runs the identity check for TAG Markets.'),
    dict(t0=44.2, t1=48.6, n=3, title='Confirm your country', sub=f'Country of residence, then {K("Agree and continue")}.'),
    dict(t0=48.6, t1=57.4, n=4, title='Your Sumsub ID email', sub=f'The same email as always, then {K("Start verification")}.'),
    dict(t0=57.4, t1=66.4, n=5, title='Type the 6-digit code', sub='Sumsub emails it to you. Never share it.'),
    dict(t0=66.4, t1=75.4, n=6, title='Create your Sumsub ID', sub=f'Tick the consent, {K("Create my account")}, then Continue.'),
    dict(t0=75.4, t1=84.6, n=7, title=f'Choose {K("Identity Card")}', sub='Two sides? Tick "My document is double-sided".'),
    dict(t0=84.6, t1=102.4, n=8, title=f'Tap {K("Allow")} for the camera', sub='Read the tips first. Close screen recorders and chat bubbles.'),
    dict(t0=102.4, t1=126.4, n=9, title='Scan your ID, then a selfie', sub=f'Front, back, then your face. Hold still for {K("All set")}.'),
]
SCENES = dict(intro=[0, 33.5], tip=[98.2, 102.4], tip2=[126.4, 137.2], mail=[-10, -9], cam1=[102.4, 110.9], cam2=[110.7, 126.4],
              recap=[137.2, 153.4], next=[153.4, 182.6], outro=[182.6, T], prog=[33.3, 137.2])
WIN = [[33.3, 98.4]]
NOCAP = []

# the nine things this video covers (overview and recap), each with the word that brings it in
PLAN = [f'Tap {K("upload documents")}', f'Tap {K("Continue")}', 'Confirm your country', 'Verify your email',
        'Create your Sumsub ID', f'Choose your {K("ID card")}', f'{K("Allow")} the camera', 'Scan your ID',
        f'{CHK} Take a quick selfie']
C['plan_in'] = [cue('n_ov1', 'upload'), cue('n_ov1', 'Continue'), cue('n_ov1', 'confirm'), cue('n_ov2', 'verify'),
                cue('n_ov2', 'create'), cue('n_ov2', 'choose'), cue('n_ov3', 'allow'), cue('n_ov3', 'scan'), cue('n_ov3', 'selfie')]
C['plan_tick'] = [cue('r1', 'upload'), cue('r1', 'Continue'), cue('r1', 'confirmed'), cue('r2', 'verified'), cue('r2', 'created'),
                  cue('r2', 'chose'), cue('r3', 'allowed'), cue('r3', 'scanned'), cue('r3', 'selfie')]
C['inthis'] = vstart['n_inthis']
C['pause'] = vstart['takeyour']
C['recap'] = vstart['r_intro']
C['next'] = vstart['x1']
C['nb'] = [cue('x2', 'Deposit'), cue('x2', 'crypto'), cue('x2', 'send')]
C['links_url'] = cue('links', 'MTG')
C['every'] = vstart['l_every']
C['save'] = vstart['save']
C['share'] = vstart['share']
C['o_fin'] = vstart['o_fin']; C['o_thanks'] = vstart['o_thanks']; C['o_like'] = cue('o_thanks', 'like')
C['o_share'] = cue('o_thanks', 'share'); C['o_comment'] = cue('o_thanks', 'comment')
C['o_massive'] = vstart['o_massive']; C['o_best'] = vstart['o_best']; C['o_you'] = cue('o_best', 'YOU')
C['o_im'] = vstart['o_im']; C['o_lgtc'] = vstart['o_lgtc']
