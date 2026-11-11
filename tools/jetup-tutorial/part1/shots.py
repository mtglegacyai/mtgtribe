# Shot list for part 1 (exec'd by make_tl.py). Times are output seconds; x, y are screen-recording pixels (720 x 1562).
def ring(t0, t1, box, gold=False):
    rings.append(dict(t0=round(t0, 3), t1=round(t1, 3), x0=box[0], y0=box[1], x1=box[2], y1=box[3], gold=gold))
def tap(t, x, y):
    taps.append(dict(t=round(t, 3), x=x, y=y))
def chip(t0, t1, text, y, gold=False):
    chips.append(dict(t0=round(t0, 3), t1=round(t1, 3), text=text, y=y, gold=gold))
K = lambda s: f'<span class="k">{s}</span>'
CHK = '<span class="em">✅</span>'

BAR = (10, 94, 710, 182)
# ---- step 2: Individual (the form, then MTG's tap) ----
shot('A', 13.9, 16.85, 46.0, 1.0, [[13.9, 360, 466, 1.30], [15.75, 360, 466, 1.30], [16.6, 300, 640, 1.75]])
ring(14.25, 15.75, BAR)
chip(14.35, 15.75, 'Check the address: jetup.ibportal.io', 1060)
TAP_IND = 50.0
shot('B', 16.85, 18.4, 49.6, 1.0, [[16.85, 300, 640, 1.75]])
tap(out_t(16.85, 49.6, 1.0, TAP_IND), 200, 623)
ring(C['individual'] - .1, 18.35, (44, 592, 345, 655))

# ---- step 3: name and email ----
shot('C', 18.4, 23.33, 54.6, 1.5, [[18.4, 300, 700, 1.75], [18.95, 360, 700, 1.5], [19.25, 360, 520, 1.5]], flash=True)
chip(18.9, 23.2, 'Real name, exactly as on your ID', 1000)
shot('D', 23.33, 28.4, 62.0, 1.3, [[23.33, 360, 520, 1.5], [26.4, 360, 520, 1.5], [26.9, 360, 800, 1.45]])
chip(23.6, 26.3, 'Your own email address', 1000)
ring(26.9, 28.35, (40, 798, 676, 896))

# ---- step 4: password and its rules ----
shot('E', 28.4, 38.6, 103.0, .42, [[28.4, 360, 760, 1.35], [29.6, 360, 760, 1.35], [30.4, 352, 930, 1.5]], flash=True)
ROWS = dict(least8=(52, 772, 330, 806), most12=(52, 822, 330, 856), upper=(52, 872, 380, 908), lower=(52, 921, 376, 955),
            number=(52, 971, 340, 1005), spaces=(52, 1026, 252, 1058), special=(52, 1071, 645, 1108))
chip(28.6, 30.0, 'Create it, then check the list', 1050)
ring(C['upper'] - .15, C['lower'] - .2, ROWS['upper'])
ring(C['lower'] - .15, C['number'] - .2, ROWS['lower'])
ring(C['number'] - .15, C['special'] - .2, ROWS['number'])
ring(C['special'] - .15, C['spaces'] - .2, ROWS['special'])
ring(C['spaces'] - .15, C['spaces'] + 1.0, ROWS['spaces'])
ring(C['spaces'] + 1.1, 38.55, (52, 772, 330, 856), gold=True)
chip(C['spaces'] + 1.2, 38.55, '8 to 12 characters. Keep it safe!', 1060, gold=True)

# ---- step 5: country and phone ----
shot('F', 38.6, 42.84, 109.9, 1.25, [[38.6, 360, 620, 1.45], [42.0, 360, 620, 1.45], [42.84, 360, 900, 1.45]], flash=True)
chip(38.9, 41.0, 'Search your country', 1060)
ring(out_t(38.6, 109.9, 1.25, 113.5), out_t(38.6, 109.9, 1.25, 114.9), (40, 608, 680, 688))
shot('G', 42.84, 49.9, 116.8, 1.25, [[42.84, 360, 640, 1.55]])
chip(43.3, 46.0, 'Leave out the first 0', 1060)
ring(C['code'] - .1, 48.4, (118, 594, 214, 638))
chip(C['code'] + .1, 49.8, '+27 is already there', 1060, gold=True)

# ---- step 6: security check, Register Now ----
TAP_REG = 138.4
H0 = TAP_REG - (C['register'] + .1 - 49.9)
shot('H', 49.9, 54.25, H0, 1.0, [[49.9, 360, 1000, 1.40], [52.6, 360, 1080, 1.40]], flash=True)
ring(C['security'] - .1, C['register'] - .25, (38, 1022, 682, 1114))
ring(C['register'] - .2, 54.2, (38, 1188, 682, 1264))
tap(out_t(49.9, H0, 1.0, TAP_REG), 440, 1226)

# ---- step 7: Registration Successful, Check your email, Return to Login ----
shot('J', 60.2, 65.6, 227.1, 1.0, [[60.2, 360, 620, 1.30]])
ring(60.9, 62.3, (16, 236, 704, 384))
ring(62.4, 65.5, (40, 668, 680, 842))
chip(60.9, 62.2, f'{CHK} Registration Successful', 1000)
TAP_RET = 241.2
shot('J', 65.6, 67.3, TAP_RET - .75, 1.0, [[65.6, 360, 760, 1.40]])
tap(65.6 + .75, 400, 965)
ring(65.7, 67.2, (78, 928, 642, 1002))

# ---- step 8: (email card) then Email Verified ----
shot('K', 73.45, 79.4, 286.25, 1.0, [[73.45, 360, 466, 1.30], [74.8, 360, 466, 1.30], [75.5, 360, 1000, 1.40]])
ring(73.8, 74.9, (10, 100, 710, 184))
chip(73.9, 74.9, 'The link opens IB Portal', 1060)
ring(75.4, 77.4, (168, 878, 552, 952))
chip(75.5, 77.4, f'{CHK} Email verified', 1240)
ring(77.5, 79.35, (112, 1156, 608, 1262), gold=True)
chip(77.6, 79.35, f'Then tap {K("Continue to Login")}', 1240, gold=True)

# ---- step 9: log in ----
L0, LS = 299.75, .9
shot('L', 79.4, 85.3, L0, LS, [[79.4, 360, 466, 1.30], [80.8, 360, 466, 1.30], [81.5, 360, 800, 1.30]], flash=True)
ring(79.6, 80.85, BAR)
chip(79.7, 80.85, 'jetup.ibportal.io, Log In', 1060)
chip(81.3, 83.6, 'Your email and password', 1060)
TOAST = out_t(79.4, L0, LS, 304.25)
ring(TOAST, 85.25, (20, 226, 704, 392))
chip(TOAST + .1, 85.25, f'{CHK} Login Successful', 1060)

# ---- step 10: profile ----
shot('M', 85.3, 97.7, 308.4, .4, [[85.3, 360, 466, 1.30], [86.6, 360, 466, 1.30], [87.6, 360, 1000, 1.30], [88.6, 330, 1100, 1.7]], flash=True)
ring(89.0, 97.6, (72, 1310, 402, 1368), gold=True)
chip(89.4, 97.6, f'{CHK} Account Type: Partner', 1060, gold=True)

STEPS = [
    dict(t0=3.0, t1=13.95, n=1, title='Open the Partner link', sub='From your sponsor. The Partner link, not the Client link.'),
    dict(t0=13.95, t1=18.4, n=2, title=f'Choose {K("Individual")}', sub='Sign up as an individual, with your real details.'),
    dict(t0=18.4, t1=28.4, n=3, title='Type your name and email', sub='First and last name exactly as on your ID. English letters only.'),
    dict(t0=28.4, t1=38.6, n=4, title='Create a password', sub='8 to 12 characters, with the mix shown on the list.'),
    dict(t0=38.6, t1=49.9, n=5, title='Country and phone number', sub='Search your country. Type your number without the first 0.'),
    dict(t0=49.9, t1=54.4, n=6, title=f'Tap {K("Register Now")}', sub='When the security check shows the green Success tick.'),
    dict(t0=60.4, t1=67.2, n=7, title='Check your email', sub=f'Then tap {K("Return to Login")}.'),
    dict(t0=67.2, t1=79.4, n=8, title='Verify your email', sub=f'Open the email from IB Portal and tap {K("Verify Account")}.'),
    dict(t0=79.4, t1=85.3, n=9, title='Log in', sub='With the email and password you just created.'),
    dict(t0=85.3, t1=97.6, n=10, title="You're in!", sub='Your profile shows Account Type: Partner.'),
]
SCENES = dict(title=[0, 3.0], link=[3.0, 14.15], tip=[54.4, 60.4], mail=[67.2, 73.7], end=[97.6, T])
WIN = [[13.9, 54.45], [60.2, 67.3], [73.45, 97.7]]
NOCAP = []
C['linktap'] = 13.35
C['suc_reg'] = 60.9
C['suc_mail'] = 75.5
C['suc_login'] = TOAST
C['suc_profile'] = 89.4
