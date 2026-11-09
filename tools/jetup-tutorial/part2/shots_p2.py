# Part 2: greeting, "In this video", the steps (fully voiced), recap, next video, signature outro.
# Exec'd by make_tl_p2.py. Times are output seconds; x, y are screen-recording pixels (720 x 1562); chip y is window pixels.
def ring(t0, t1, box, gold=False):
    rings.append(dict(t0=round(t0, 3), t1=round(t1, 3), x0=box[0], y0=box[1], x1=box[2], y1=box[3], gold=gold))
def tap(t, x, y):
    taps.append(dict(t=round(t, 3), x=x, y=y))
def chip(t0, t1, text, y, gold=False):
    chips.append(dict(t0=round(t0, 3), t1=round(t1, 3), text=text, y=y, gold=gold))
K = lambda s: f'<span class="k">{s}</span>'
CHK = '<span class="em">✅</span>'
BAR = (10, 96, 710, 180)          # Brave address bar
TABBAR = (170, 96, 560, 180)      # the in-app tab opened from the email ("Tag Markets ... markets.com")

# ---- step 1: log in to JetUP (A: the profile, address bar visible) ----
shot('A', 33.9, 41.9, 12.0, 1.0, [[33.9, 360, 560, 1.29]])
ring(34.45, 38.1, BAR)
chip(34.55, 38.1, 'Check the address: jetup.ibportal.io', 1060)
chip(cue('s_same', 'same') - .1, 41.75, 'Same email and password as part 1', 1060, gold=True)

# ---- step 2: scroll down to the CopyX banner ----
shot('A', 41.9, 45.6, 22.9, 4.0 / 3.7, [[41.9, 360, 560, 1.29], [45.3, 360, 781, 1.29]])
shot('B', 45.6, 51.4, 29.5, 1.0, [[45.6, 360, 781, 1.29]], flash=True)
ring(45.75, cue('never', 'directly') - .1, (100, 540, 625, 1025))
chip(45.8, cue('never', 'directly') - .1, 'The CopyX banner', 70)
ring(cue('never', 'directly') - .05, 51.3, (70, 1140, 650, 1204), gold=True)
chip(cue('never', 'directly'), 51.3, 'Never register on CopyX directly', 70, gold=True)

# ---- step 3: tap Register CopyX ----
TAPR = cue('s_regcx', 'Register') + .1
shot('B', 51.4, TAPR + .45, 72.35 - (TAPR - 51.4), 1.0, [[51.4, 360, 781, 1.29]])
ring(51.45, TAPR + .15, (160, 1056, 558, 1136), gold=True)
tap(TAPR, 360, 1096)

# ---- step 4: the JetUP password ----
S4 = TAPR + .45
PWC = cue('s_pw', 'Enter') - .15
shot('C', S4, PWC, 77.0, 1.0, [[S4, 360, 700, 1.29]], flash=True)
shot('C', PWC, 58.2, 96.8, 1.0, [[PWC, 360, 700, 1.29]], flash=True)
ring(cue('s_pw', 'password') - .1, 58.1, (80, 818, 640, 898), gold=True)
chip(PWC + .05, 58.1, 'Same password as on JetUP', 1060, gold=True)

# ---- step 5: tick the three boxes, Sync Account, syncing ----
TS = cue('s_tick', 'Sync') - .05
SP5 = (113.6 - 108.0) / (TS - 58.2)
shot('C', 58.2, TS, 108.0, SP5, [[58.2, 360, 860, 1.29]])
for s_, y_ in ((108.9, 703), (109.5, 893), (109.9, 1043)):
    tap(out_t(58.2, 108.0, SP5, s_), 98, y_)
ring(TS - .9, TS + .2, (100, 1200, 620, 1272), gold=True)
tap(TS, 360, 1236)
T1 = round(TS + (118.0 - 113.6) / 1.4, 3)
shot('C', TS, T1, 113.6, 1.4, [[TS, 360, 860, 1.29]])
shot('D', T1, T1 + .5, 118.0, 1.4, [[T1, 360, 860, 1.29], [T1 + .5, 360, 640, 1.29]])

# ---- step 6: Sync Successful, tick, Close, User Active, Login to CopyX ----
S6 = T1 + .5
shot('D', S6, 68.6, 118.7, 1.0, [[S6, 360, 640, 1.29]])
C['suc_sync'] = cue('s_synced', 'Sync')
ring(C['suc_sync'] - .05, 68.5, (40, 300, 680, 760))
chip(C['suc_sync'], 68.5, f'{CHK} Sync Successful!', 1060)
TT = cue('s_close', 'box') + .05
D0 = 147.3 - (TT - 68.6)
shot('D', 68.6, 71.7, D0, 1.0, [[68.6, 360, 900, 1.29]])
ring(68.75, TT + .5, (50, 820, 680, 1150))
tap(TT, 154, 872)
TCL = out_t(68.6, D0, 1.0, 149.3)
ring(TT + .7, TCL + .15, (228, 1200, 492, 1272), gold=True)
tap(TCL, 360, 1236)
shot('D', 71.7, 72.5, 150.2, 1.0, [[71.7, 360, 680, 1.29]], flash=True)
TAP2 = cue('s_login', 'Tap') + .1
shot('E', 72.5, TAP2 + .1, 246.4 - (TAP2 - 72.5), 1.0, [[72.5, 360, 680, 1.29]])
C['suc_active'] = cue('active', 'User')
ring(C['suc_active'] - .1, 76.45, (400, 222, 645, 282), gold=True)
chip(C['suc_active'], 76.45, f'{CHK} User Active', 330)
ring(cue('active', 'C') - .1, 76.45, (405, 282, 650, 330))
ring(cue('s_login', 'Login') - .1, TAP2 + .1, (164, 1056, 556, 1136), gold=True)
chip(cue('s_login', 'Login'), TAP2 + .1, f'Now: {K("Login to CopyX")}', 330, gold=True)
tap(TAP2, 360, 1096)

# ---- step 7: log in to TAG Markets (checking, log in page, tip, Login, checking, please wait) ----
S7 = TAP2 + .1
shot('F', S7, 82.8, 248.8, (258.25 - 248.8) / (82.8 - S7), [[S7, 360, 560, 1.29]], flash=True)
shot('F', 82.8, 86.6, 259.2, 1.0, [[82.8, 360, 560, 1.29], [85.2, 360, 560, 1.29], [85.9, 360, 820, 1.29]], xfade=.35)
ring(82.9, 85.2, BAR)
chip(83.0, 85.2, 'Check the address: portal.tagmarkets.com', 520)
shot('G', 86.6, 88.6, 490.9, .28, [[86.6, 360, 700, 1.29]], flash=True)
ring(86.7, 88.5, (40, 600, 680, 832))
chip(cue('tagin', 'same') - .1, 88.5, 'Same email and password as JetUP', 160, gold=True)
# tip card 88.4 to 96.0 (voice s_tip)
shot('G', 95.8, 96.9, 490.9, 1.0, [[95.8, 360, 700, 1.29]])
ring(95.95, 96.55, (285, 985, 435, 1055), gold=True)
tap(96.4, 360, 1018)
shot('G', 96.9, 99.9, 492.8, (522.3 - 492.8) / 3.0, [[96.9, 360, 600, 1.29]], xfade=.35)
chip(cue('s_human', 'checks') - .1, 99.85, 'Verify you are human: just wait', 1060)
shot('G', 99.9, 101.9, 522.4, (527.6 - 522.4) / 2.0, [[99.9, 360, 600, 1.29]], xfade=.35)

# ---- step 8: the TAG Markets dashboard ----
shot('G', 101.9, 108.9, 527.8, (531.9 - 527.8) / 7.0, [[101.9, 360, 640, 1.29]])
C['suc_dash'] = cue('s_dash', 'dashboard')
chip(C['suc_dash'] - .1, cue('s_dash', 'asks') - .15, f'{CHK} Your TAG Markets dashboard', 1060)
ring(cue('s_dash', 'asks') - .1, 108.6, (22, 560, 698, 690), gold=True)
chip(cue('s_dash', 'asks'), 108.6, 'Part 3: upload documents (KYC)', 1060, gold=True)

# ---- step 9: confirm the email (card 108.7 to 122.4), validated, click here, log in again, dashboard ----
C['mailtap'] = cue('s_confirm', 'Confirm') + .05
TAP3 = cue('s_click', 'here') + .05
I0 = 688.6 - (TAP3 - 122.2)
shot('I', 122.2, TAP3 + .3, I0, 1.0, [[122.2, 360, 560, 1.29]])
ring(122.35, 123.7, TABBAR)
chip(122.4, 123.7, 'Opened from the TAG Markets email', 400)
C['suc_email'] = cue('s_valid', 'Verification')
ring(C['suc_email'] - .1, 125.75, (32, 570, 690, 780))
chip(C['suc_email'], 125.75, f'{CHK} Email validated', 1060)
ring(cue('s_click', 'click') - .15, TAP3 + .2, (108, 712, 184, 760), gold=True)
tap(TAP3, 146, 736)
X1 = round(TAP3 + .3 + (697.3 - 688.9) / 2.5, 3)
shot('I', TAP3 + .3, X1, 688.9, 2.5, [[TAP3 + .3, 360, 560, 1.29]])
X2 = round(X1 + (720.4 - 711.0) / 3.0, 3)
shot('J', X1, X2, 711.0, 3.0, [[X1, 360, 560, 1.29]], flash=True)
chip(TAP3 + .5, X2, 'Log in again: same email and password', 1060)
shot('J', X2, 139.4, 720.4, 1.0, [[X2, 360, 640, 1.29]])
C['suc_done'] = cue('s_done', 'confirmed')
chip(C['suc_done'] - .1, 139.2, f'{CHK} Email confirmed', 1060)

STEPS = [
    dict(t0=33.9, t1=41.9, n=1, title='Log in to JetUP', sub='At jetup.ibportal.io, with the email and password from part 1.'),
    dict(t0=41.9, t1=51.4, n=2, title='Find the CopyX banner', sub='Scroll down your profile. Never register on CopyX directly.'),
    dict(t0=51.4, t1=S4, n=3, title=f'Tap {K("Register CopyX")}', sub='On the CopyX banner in your JetUP profile.'),
    dict(t0=S4, t1=58.2, n=4, title='Enter your JetUP password', sub='The same password you created in part 1.'),
    dict(t0=58.2, t1=S6, n=5, title=f'Tick the boxes, tap {K("Sync Account")}', sub='Read the three boxes first, then wait for the sync.'),
    dict(t0=S6, t1=S7, n=6, title=f'Wait for {K("User Active")}', sub=f'Tick the box, tap Close, then tap {K("Login to CopyX")}.'),
    dict(t0=S7, t1=88.4, n=7, title='Log in to TAG Markets', sub='At portal.tagmarkets.com, with the same email and password.'),
    dict(t0=96.0, t1=101.9, n=7, title='Log in to TAG Markets', sub='At portal.tagmarkets.com, with the same email and password.'),
    dict(t0=101.9, t1=108.7, n=8, title='Your TAG Markets dashboard', sub='JetUP and TAG Markets are linked. KYC comes in part 3.'),
    dict(t0=108.7, t1=139.2, n=9, title='Confirm your email', sub=f'Open the TAG Markets email, tap {K("Confirm email address")}.'),
]
SCENES = dict(intro=[0, 34.1], tip=[88.4, 96.0], mail=[108.7, 122.4], recap=[139.2, 157.4], next=[157.4, 187.85],
              outro=[187.85, T], prog=[33.9, 139.2])
WIN = [[33.9, 88.6], [95.8, 108.9], [122.2, 139.4]]
NOCAP = []

# the nine things this video covers (overview and recap), each with the word that brings it in
PLAN = ['Log in to JetUP', 'Scroll down to the CopyX banner', f'Tap {K("Register CopyX")}', 'Enter your JetUP password',
        f'Tick the boxes, tap {K("Sync Account")}', f'{CHK} User Active', 'Log in to TAG Markets', 'Confirm your email',
        f'{CHK} Your TAG Markets dashboard']
C['plan_in'] = [cue('n_ov1', 'log'), cue('n_ov1', 'scroll'), cue('n_ov1', 'Register'), cue('n_ov2', 'password'),
                cue('n_ov2', 'tick'), cue('n_ov2', 'Active'), cue('n_ov3', 'log'), cue('n_ov3', 'confirm'), cue('n_ov3', 'dashboard')]
C['plan_tick'] = [cue('r1', 'logged'), cue('r1', 'scrolled'), cue('r1', 'Register'), cue('r2', 'password'), cue('r2', 'ticked'),
                  cue('r2', 'Active'), cue('r3', 'logged'), cue('r3', 'confirmed'), cue('r3', 'dashboard')]
C['inthis'] = vstart['n_inthis']
C['pause'] = vstart['takeyour']
C['recap'] = vstart['r_intro']
C['next'] = vstart['x1']
C['nb'] = [cue('x2', 'upload'), cue('x2', 'scan'), cue('x2', 'selfie')]
C['links_url'] = cue('links', 'MTG')
C['every'] = vstart['l_every']
C['save'] = vstart['save']
C['share'] = vstart['share']
C['o_fin'] = vstart['o_fin']; C['o_thanks'] = vstart['o_thanks']; C['o_like'] = cue('o_thanks', 'like')
C['o_share'] = cue('o_thanks', 'share'); C['o_comment'] = cue('o_thanks', 'comment')
C['o_massive'] = vstart['o_massive']; C['o_best'] = vstart['o_best']; C['o_you'] = cue('o_best', 'YOU')
C['o_im'] = vstart['o_im']; C['o_lgtc'] = vstart['o_lgtc']
