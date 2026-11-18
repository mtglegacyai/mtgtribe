# Part 1 v2: greeting, "In this video" overview, the steps (fully voiced), recap, next video, signature outro.
# Exec'd by make_tl2.py. Times are output seconds; x, y are screen-recording pixels (720 x 1562).
def ring(t0, t1, box, gold=False):
    rings.append(dict(t0=round(t0, 3), t1=round(t1, 3), x0=box[0], y0=box[1], x1=box[2], y1=box[3], gold=gold))
def tap(t, x, y):
    taps.append(dict(t=round(t, 3), x=x, y=y))
def chip(t0, t1, text, y, gold=False):
    chips.append(dict(t0=round(t0, 3), t1=round(t1, 3), text=text, y=y, gold=gold))
K = lambda s: f'<span class="k">{s}</span>'
CHK = '<span class="em">✅</span>'
BAR = (10, 94, 710, 182)

# ---- step 1: the Partner link (cards) 31.5 to 42.65 ----
C['linktap'] = vstart['ifme'] + 4.3
# ---- step 2: Individual ----
shot('A', 42.4, 45.35, 46.0, 1.0, [[42.4, 360, 466, 1.30], [44.25, 360, 466, 1.30], [45.1, 300, 640, 1.75]])
ring(42.75, 44.25, BAR)
chip(42.85, 44.25, 'Check the address: jetup.ibportal.io', 1060)
shot('B', 45.35, 46.9, 49.6, 1.0, [[45.35, 300, 640, 1.75]])
tap(out_t(45.35, 49.6, 1.0, 50.0), 200, 623)
ring(C['individual'] - .1, 46.85, (44, 592, 345, 655))

# ---- step 3: name and email ----
C3 = 46.9
shot('C', C3, C3 + 9.87, 54.6, .75, [[C3, 300, 700, 1.75], [C3 + .9, 360, 700, 1.5], [C3 + 1.25, 360, 520, 1.5]], flash=True)
chip(cue('s_name', 'Use') - .1, C3 + 9.8, 'Real name, exactly as on your ID', 1000)
D3 = C3 + 9.87
shot('D', D3, D3 + 4.92, 62.0, 1.3, [[D3, 360, 520, 1.5], [D3 + 3.08, 360, 520, 1.5], [D3 + 3.58, 360, 800, 1.45]])
chip(D3 + .3, D3 + 3.0, 'Your own email address', 1000)
ring(D3 + 3.6, D3 + 4.87, (40, 798, 676, 896))

# ---- step 4: password and its rules ----
S4 = D3 + 4.92
shot('E', S4, 75.4, 103.0, .32, [[S4, 360, 760, 1.35], [S4 + 1.2, 360, 760, 1.35], [S4 + 2.0, 352, 930, 1.5]], flash=True)
ROWS = dict(upper=(52, 872, 380, 908), lower=(52, 921, 376, 955), number=(52, 971, 340, 1005), spaces=(52, 1026, 252, 1058),
            special=(52, 1071, 645, 1108))
chip(S4 + .2, S4 + 1.6, 'Create it, then check the list', 1050)
ring(C['upper'] - .15, C['lower'] - .2, ROWS['upper'])
ring(C['lower'] - .15, C['number'] - .2, ROWS['lower'])
ring(C['number'] - .15, C['special'] - .2, ROWS['number'])
ring(C['special'] - .15, C['spaces'] - .2, ROWS['special'])
ring(C['spaces'] - .15, cue('s_pw12', 'Your') - .2, ROWS['spaces'])
ring(cue('s_pw12', 'twelve') - .3, 75.35, (52, 772, 330, 856), gold=True)
chip(cue('s_pw12', 'twelve') - .2, 75.35, '8 to 12 characters. Keep it safe!', 1060, gold=True)

# ---- step 5: country and phone (75.4 to 86.7) ----
S5 = 75.4
shot('F', S5, S5 + 4.24, 109.9, 1.25, [[S5, 360, 620, 1.45], [S5 + 3.4, 360, 620, 1.45], [S5 + 4.24, 360, 900, 1.45]], flash=True)
chip(S5 + .3, S5 + 2.4, 'Search your country', 1060)
ring(out_t(S5, 109.9, 1.25, 113.5), out_t(S5, 109.9, 1.25, 114.9), (40, 608, 680, 688))
shot('G', S5 + 4.24, 86.7, 116.8, 1.25, [[S5 + 4.24, 360, 640, 1.55]])
chip(S5 + 4.7, S5 + 7.4, 'Leave out the first 0', 1060)
ring(C['code'] - .1, C['code'] + 2.2, (118, 594, 214, 638))
chip(C['code'] + .1, 86.6, '+27 is already there', 1060, gold=True)

# ---- step 6: security check, Register Now (86.7 to 91.2) ----
S6 = 86.7
TAP_REG = 138.4
H0 = TAP_REG - (C['register'] + .1 - S6)
shot('H', S6, 91.25, H0, 1.0, [[S6, 360, 1000, 1.40], [S6 + 2.7, 360, 1080, 1.40]], flash=True)
ring(C['security'] - .1, C['register'] - .25, (38, 1022, 682, 1114))
ring(C['register'] - .2, 91.2, (38, 1188, 682, 1264))
tap(out_t(S6, H0, 1.0, TAP_REG), 440, 1226)

# ---- tip card 91.2 to 97.2 (voice s_tip) ----
# ---- step 7: Registration Successful, Check your email, Return to Login ----
S7 = 97.0
shot('J', S7, S7 + 5.4, 227.1, 1.0, [[S7, 360, 620, 1.30]])
ring(S7 + .7, S7 + 2.1, (16, 236, 704, 384))
chip(S7 + .7, S7 + 2.0, f'{CHK} Registration Successful', 1000)
ring(S7 + 2.2, S7 + 5.3, (40, 668, 680, 842))
TAP_RET = 241.2
shot('J', S7 + 5.4, S7 + 7.1, TAP_RET - .75, 1.0, [[S7 + 5.4, 360, 760, 1.40]])
tap(S7 + 5.4 + .75, 400, 965)
ring(S7 + 5.5, S7 + 7.0, (78, 928, 642, 1002))
C['suc_reg'] = S7 + .7

# ---- step 8: the email (card 104.0 to 112.0), then Email Verified ----
C['mailtap'] = cue('s_open', 'Verify') + .05
S8 = 111.75
shot('K', S8, 119.05, 286.25, 1.0, [[S8, 360, 466, 1.30], [S8 + 1.35, 360, 466, 1.30], [S8 + 2.05, 360, 1000, 1.40]])
ring(S8 + .35, S8 + 1.45, (10, 100, 710, 184))
chip(S8 + .45, S8 + 1.45, 'The link opens IB Portal', 1060)
ring(cue('s_verified', 'Your') - .2, cue('s_verified', 'Tap') - .2, (168, 878, 552, 952))
chip(cue('s_verified', 'Your') - .1, cue('s_verified', 'Tap') - .2, f'{CHK} Email verified', 1240)
ring(cue('s_verified', 'Tap') - .1, 118.95, (112, 1156, 608, 1262), gold=True)
chip(cue('s_verified', 'Tap'), 118.95, f'Then tap {K("Continue to Login")}', 1240, gold=True)
C['suc_mail'] = cue('s_verified', 'Your') - .1

# ---- step 9: log in (119.0 to 124.9) ----
S9 = 119.0
L0, LS = 299.75, .9
shot('L', S9, 124.9, L0, LS, [[S9, 360, 466, 1.30], [S9 + 1.4, 360, 466, 1.30], [S9 + 2.1, 360, 800, 1.30]], flash=True)
ring(S9 + .2, S9 + 1.45, BAR)
chip(S9 + .3, S9 + 1.45, 'jetup.ibportal.io, Log In', 1060)
chip(S9 + 1.9, S9 + 4.2, 'Your email and password', 1060)
TOAST = out_t(S9, L0, LS, 304.25)
ring(TOAST, 124.85, (20, 226, 704, 392))
chip(TOAST + .1, 124.85, f'{CHK} Login Successful', 1060)
C['suc_login'] = TOAST

# ---- step 10: profile (124.9 to 133.6) ----
S10 = 124.9
shot('M', S10, 133.7, 308.4, .4, [[S10, 360, 466, 1.30], [S10 + 1.3, 360, 466, 1.30], [S10 + 2.3, 360, 1000, 1.30], [S10 + 3.3, 330, 1100, 1.7]], flash=True)
ring(cue('s_in', 'Account') - .3, 133.55, (72, 1310, 402, 1368), gold=True)
chip(cue('s_in', 'Account') - .2, 133.55, f'{CHK} Account Type: Partner', 1060, gold=True)
C['suc_profile'] = cue('s_in', 'Account') - .2

STEPS = [
    dict(t0=31.5, t1=42.45, n=1, title='Open the Partner link', sub='From your sponsor. The Partner link, not the Client link.'),
    dict(t0=42.45, t1=46.9, n=2, title=f'Choose {K("Individual")}', sub='Sign up as an individual, with your real details.'),
    dict(t0=46.9, t1=S4, n=3, title='Type your name and email', sub='First and last name exactly as on your ID. English letters only.'),
    dict(t0=S4, t1=75.4, n=4, title='Create a password', sub='8 to 12 characters, with the mix shown on the list.'),
    dict(t0=75.4, t1=86.7, n=5, title='Country and phone number', sub='Search your country. Type your number without the first 0.'),
    dict(t0=86.7, t1=91.2, n=6, title=f'Tap {K("Register Now")}', sub='When the security check shows the green Success tick.'),
    dict(t0=97.2, t1=104.0, n=7, title='Check your email', sub=f'Then tap {K("Return to Login")}.'),
    dict(t0=104.0, t1=119.0, n=8, title='Verify your email', sub=f'Open the email from IB Portal and tap {K("Verify Account")}.'),
    dict(t0=119.0, t1=124.9, n=9, title='Log in', sub='With the email and password you just created.'),
    dict(t0=124.9, t1=133.6, n=10, title="You're in!", sub='Your profile shows Account Type: Partner.'),
]
SCENES = dict(intro=[0, 31.6], link=[31.5, 42.65], tip=[91.2, 97.2], mail=[104.0, 112.0], recap=[133.6, 154.2],
              next=[154.2, 179.0], outro=[179.0, T])
WIN = [[42.4, 91.3], [97.0, 104.1], [111.75, 133.7]]
NOCAP = []

# the nine things this video covers (overview and recap), each with the word that brings it in
PLAN = ['Open the Partner link', f'Choose {K("Individual")}', 'Your real name and email', 'A password (8 to 12 characters)',
        'Country and phone number', f'Tap {K("Register Now")}', 'Verify your email', 'Log in',
        f'{CHK} Account Type: Partner']
C['plan_in'] = [cue('n_ov1', 'Partner'), cue('n_ov1', 'Individual'), cue('n_ov1', 'name'), cue('n_ov2', 'password'),
                cue('n_ov2', 'country'), cue('n_ov2', 'Register'), cue('n_ov3', 'verify'), cue('n_ov3', 'log'),
                cue('n_ov3', 'profile')]
C['plan_tick'] = [cue('r1', 'Partner'), cue('r1', 'Individual'), cue('r2', 'name'), cue('r2', 'password'), cue('r3', 'country'),
                  cue('r3', 'Register'), cue('r4', 'verified'), cue('r4', 'logged'), cue('r4', 'Account')]
C['inthis'] = vstart['n_inthis']
C['pause'] = vstart['takeyour']
C['recap'] = vstart['r_intro']
C['next'] = vstart['x1']
C['nb'] = [cue('x2', 'sync'), cue('x2', 'confirm'), cue('x2', 'log')]
C['links_url'] = cue('links', 'MTG')
C['save'] = vstart['save']
C['share'] = vstart['share']
C['o_fin'] = vstart['o_fin']; C['o_thanks'] = vstart['o_thanks']; C['o_like'] = cue('o_thanks', 'like')
C['o_share'] = cue('o_thanks', 'share'); C['o_comment'] = cue('o_thanks', 'comment')
C['o_massive'] = vstart['o_massive']; C['o_best'] = vstart['o_best']; C['o_you'] = cue('o_best', 'YOU')
C['o_im'] = vstart['o_im']; C['o_lgtc'] = vstart['o_lgtc']
