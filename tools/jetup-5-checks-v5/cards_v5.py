# JetUP 5 Checks v5: what appears on screen, and on which spoken word.
# Each card starts on its trigger phrase; each element inside it pops in on its own phrase ('at'), searched forward
# from the card start. Element kinds: kicker, head, sub, rows (row = emoji, text, colour, at), calc (lines), url,
# chip, strike, emoji (big), photo (MTG circle), num (CHECK n OF 5 title).
LIME, PURPLE, PINK, RED, GREEN, GOLD, WHITE = (203, 251, 97), (155, 124, 255), (227, 113, 252), (255, 95, 122), (47, 224, 160), (232, 194, 90), (246, 243, 255)

def R(e, t, at=None, c=None): return dict(e=e, t=t, at=at, c=c)

CARDS = [
 dict(at="if youve lost money", els=[
   dict(k='kicker', t='THIS VIDEO IS FOR YOU'),
   dict(k='head', t='Lost money before?', s=66),
   dict(k='rows', rows=[R('📉', 'A trading platform', 'trading platform'), R('🤖', 'A copy trading app', 'copy trading app'),
                        R('🎁', 'A program that promised the world', 'promised you the world')])]),
 dict(at="im not going to tell you", els=[
   dict(k='strike', old='"This one is different"', new='Check it yourself.', at2='instead')]),
 dict(at="five checks you can do", els=[
   dict(k='kicker', t='TODAY'),
   dict(k='head', t='5 checks you can do yourself', s=64),
   dict(k='sub', t='So whatever you decide, you decide with your eyes open.', at='whatever you decide')]),
 dict(at="hi im mtg", els=[
   dict(k='photo', d=330),
   dict(k='head', t='MTG', s=84, c=GOLD, center=True),
   dict(k='sub', t='Your Digital Architect', center=True, s=32, c=WHITE),
   dict(k='chip', t='⚠️  Stay to the end: check 4 is the one most people skip', at='check number four')]),
 dict(at="i know the feeling", els=[
   dict(k='kicker', t='SOUND FAMILIAR?'),
   dict(k='rows', rows=[R('⏳', 'The withdrawal that never came', 'withdrawal'), R('🔇', 'The group that went quiet', 'the group'),
                        R('📵', 'The leader who stopped answering', 'the leader')])]),
 dict(at="you are not foolish", els=[
   dict(k='emoji', e='❤️'),
   dict(k='head', t='You are not foolish for trying.', s=60, center=True),
   dict(k='sub', t='Trying means you want more for your family.', center=True, at='trying means')]),
 dict(at="the lesson is not", els=[
   dict(k='kicker', t='THE LESSON'),
   dict(k='strike', old='Stop trying', new='Verify first.', at2='verify first'),
   dict(k='chip', t='🔍  So let\'s verify, together', at='lets verify')]),
 dict(at="here is the simple picture", els=[
   dict(k='kicker', t='THE SIMPLE PICTURE'),
   dict(k='rows', s=29, rows=[R('👥', 'JetUP: community, training and AI tools. Does NOT trade or take your money', 'jetup is a community'),
                              R('🏦', 'TAG Markets: the broker. The account is in YOUR name', 'tag markets is the broker'),
                              R('🔗', 'CopyX: connect a strategy, like Sonic AI', 'connect a strategy')])]),
 dict(at="the main one", els=[
   dict(k='kicker', t='THE STRATEGY'),
   dict(k='head', t='Sonic AI trades gold', s=62),
   dict(k='head', t='XAU/USD', s=104, c=LIME, at='x a u'),
   dict(k='sub', t='XAU = gold. USD = US dollar. The price of gold in US dollars.', at='thats gold')]),
 dict(at="when the strategy makes a profit", els=[
   dict(k='kicker', t='THE PROFIT SPLIT'),
   dict(k='split', at2='thirty percent')]),
 dict(at="so if the strategy makes ten", els=[
   dict(k='kicker', t='EXAMPLE'),
   dict(k='calc', lines=[('$10 profit × 70%', 'ten dollars'), ('= $7 to you', 'seven dollars')])]),
 dict(at="and if it makes a loss", els=[
   dict(k='emoji', e='🛡️'),
   dict(k='head', t='A loss? No performance fee.', s=58, center=True, at='nobody charges'),
   dict(k='sub', t='The fee is taken from profits only.', center=True, at='on that loss')]),

 dict(at="check one", check=1, els=[dict(k='num', n=1, q='Who holds my money?', e='💼')]),
 dict(at="your deposit goes into", check=1, els=[
   dict(k='kicker', t='CHECK 1 · WHO HOLDS MY MONEY'),
   dict(k='rows', rows=[R('🏦', 'Your deposit sits in an MT5 account at TAG Markets', 'deposit goes'),
                        R('🪪', 'In YOUR name', 'in your name'),
                        R('📖', 'MT5 = MetaTrader 5, the trading app many brokers use', 'means metatrader')])]),
 dict(at="dont take my word", check=1, els=[
   dict(k='emoji', e='🔍'),
   dict(k='head', t='Log in yourself. See your own balance.', s=58, center=True, at='log in yourself')]),

 dict(at="check two", check=2, els=[dict(k='num', n=2, q='Who regulates the broker?', e='⚖️')]),
 dict(at="tag markets trading company", check=2, els=[
   dict(k='kicker', t='LICENCE 1 · MAURITIUS'),
   dict(k='rows', s=29, rows=[R('🏢', 'T.M. Financials Ltd, TAG Markets\' trading company', 'trading company'),
                              R('📜', 'FSC Mauritius · Licence GB21026474', 'licensed in mauritius'),
                              R('📖', 'FSC = Financial Services Commission, the Mauritius regulator', 'financial services commission')])]),
 dict(at="tag also has a south african", check=2, els=[
   dict(k='kicker', t='LICENCE 2 · SOUTH AFRICA'),
   dict(k='rows', s=29, rows=[R('🇿🇦', 'TM Financials SA (Pty) Ltd', 'south african company'),
                              R('📖', 'FSCA = Financial Sector Conduct Authority, our regulator', 'financial sector conduct'),
                              R('📜', 'FSCA authorised · FSP No. 55237', 'f s p number', LIME)])]),
 dict(at="but read the fine print", check=2, els=[
   dict(k='kicker', t='THE FINE PRINT · TAG\'S OWN WEBSITE'),
   dict(k='rows', rows=[R('📣', 'SA company: marketing services', 'marketing services'),
                        R('🏦', 'Trading accounts: held by the Mauritius company', 'trading accounts'),
                        R('❓', 'Know which regulator covers YOUR account', 'know which regulator', LIME)])]),
 dict(at="regulators in austria", check=2, els=[
   dict(k='kicker', t='PUBLISHED REGULATOR WARNINGS'),
   dict(k='rows', s=30, compact=True, rows=[R('🇦🇹', 'Austria · FMA', 'austria'), R('🇱🇺', 'Luxembourg · CSSF', 'luxembourg'),
                                           R('🇸🇮', 'Slovenia · ATVP', 'slovenia'), R('🇷🇺', 'Russia · Central Bank', 'russia'),
                                           R('🇨🇦', 'Quebec, Canada · AMF', 'quebec')]),
   dict(k='sub', t='Warnings that TAG Markets is not authorised in those countries.', at='published warnings')]),
 dict(at="im telling you this", check=2, els=[
   dict(k='emoji', e='🤝'),
   dict(k='head', t='You deserve the whole picture.', s=60, center=True)]),
 dict(at="search tag markets", check=2, els=[
   dict(k='kicker', t='CHECK IT YOURSELF'),
   dict(k='head', t='Search "TAG Markets" on IOSCO I-SCAN', s=50),
   dict(k='url', t='iosco.org/i-scan', at='regulator warning list'),
   dict(k='sub', t='The global list of regulator warnings. The link is on mtgtribe.com/jetup', at='ive put the link')]),

 dict(at="check three", check=3, els=[dict(k='num', n=3, q='Are the results real?', e='📊')]),
 dict(at="sonic ai publishes", check=3, els=[
   dict(k='kicker', t='CHECK 3 · ARE THE RESULTS REAL'),
   dict(k='rows', rows=[R('📈', 'Sonic AI\'s track record is public on Myfxbook', 'track record'),
                        R('👀', 'Look BEFORE you deposit', 'look before', LIME)])]),
 dict(at="it shows plus thirty", check=3, els=[
   dict(k='kicker', t='PUBLISHED RESULT'),
   dict(k='count', to=30.1, fmt='+{:.1f}%', s=140, c=GREEN, center=True, at='thirty point one'),
   dict(k='sub', t='3 Nov 2024 to 4 Oct 2026', center=True, at='november', s=32, c=WHITE),
   dict(k='chip', t='GROSS: before the 70/30 split', at='before the seventy')]),
 dict(at="so thirty point one times", check=3, els=[
   dict(k='kicker', t='YOUR SHARE'),
   dict(k='calc', lines=[('30.1% × 70%', 'thirty point one'), ('= 21.07%', 'twenty-one percent'), ('≈ 21% over ~23 months', 'twenty-three months')]),
   dict(k='sub', t='Before fees. Not a forecast.', center=True, at='before fees')]),
 dict(at="not forty percent", check=3, els=[
   dict(k='rows', rows=[R('❌', 'NOT 40% a month', 'forty percent', RED), R('❌', 'NOT a fixed return', 'fixed return', RED),
                        R('⚠️', 'Past results never guarantee the future', 'past results', LIME)])]),

 dict(at="check four", check=4, els=[dict(k='num', n=4, q='What can go wrong?', e='⚠️', note='The one most people skip.', note_at='most people skip')]),
 dict(at="latest start promo", check=4, els=[
   dict(k='kicker', t='THE START PROMO'),
   dict(k='calc', lines=[('$150 yours', 'hundred and fifty'), ('+ $100 promo', 'promo adds'), ('= $250', 'two hundred and fifty')])]),
 dict(at="amplify it twenty four", check=4, els=[
   dict(k='kicker', t='AMPLIFY 24x'),
   dict(k='calc', lines=[('$250 × 24', 'amplify it'), ('= $6,000 exposure', 'six thousand')]),
   dict(k='sub', t='Exposure = the size you trade with. NOT money you own.', center=True, at='thats exposure')]),
 dict(at="bigger exposure means", check=4, els=[
   dict(k='kicker', t='THE RISK'),
   dict(k='rows', rows=[R('↕️', 'Bigger exposure = bigger swings, up AND down', 'bigger swings'),
                        R('🔻', 'You can lose your whole deposit', 'lose your whole', RED)])]),
 dict(at="and the brokers insolvency cover", check=4, els=[
   dict(k='kicker', t='INSOLVENCY COVER'),
   dict(k='count', to=1000000, fmt='${:,.0f} TOTAL', s=70, c=LIME, at='one million'),
   dict(k='rows', rows=[R('👥', 'For ALL clients together, not per person', 'all clients'),
                        R('🚫', 'Trading losses NOT covered', 'trading losses', RED)]),
   dict(k='sub', t='Insolvency = the broker itself going bust.')]),

 dict(at="check five", check=5, els=[dict(k='num', n=5, q='Can I get out?', e='🚪')]),
 dict(at="profits can be withdrawn", check=5, els=[
   dict(k='kicker', t='THE PROMO RULES'),
   dict(k='rows', s=29, rows=[R('💵', 'Profits: withdraw any time', 'profits can be'),
                              R('📅', 'Bonus: released after 12 months', 'twelve months'),
                              R('⛔', 'Your own money out before 12 months = promo ends', 'taking your own', RED),
                              R('📲', 'Check the current rules in your dashboard', 'check the current', LIME)])]),
 dict(at="my advice", check=5, els=[
   dict(k='kicker', t='MTG\'S ADVICE'),
   dict(k='rows', rows=[R('🌱', 'Start small', 'start small'), R('🧪', 'Test a small withdrawal early', 'small withdrawal'),
                        R('✅', 'Let the system prove itself to you', 'prove itself', GREEN)])]),

 dict(at="so why would anyone still", els=[
   dict(k='kicker', t='WHY SOME STILL GIVE IT A SHOT'),
   dict(k='rows', s=29, rows=[R('✅', 'You can check before you deposit', 'check before you deposit'), R('✅', 'You can start small', 'you can start small'),
                              R('✅', 'The account is in your name', 'account is in your name'),
                              R('✅', 'Their own warning: "what a partner earns can be zero"', 'what a partner earns')]),
   dict(k='chip', t='That kind of honesty is worth noticing 👏', at='that kind of honesty')]),
 dict(at="one more truth", els=[
   dict(k='kicker', t='FROM JETUP\'S OWN FOUNDER'),
   dict(k='head', t='The big money comes from building a team,', s=56, at='the big money'),
   dict(k='sub', t='not from the trading percentage. Know that going in.', at='not from the trading', s=32, c=WHITE)]),
 dict(at="if you check all five", els=[
   dict(k='kicker', t='YOUR MOVE'),
   dict(k='head', t='Checked all 5? Feels right?', s=58),
   dict(k='head', t='Start small.', s=96, c=LIME, at='start small'),
   dict(k='sub', t='Only with money you can afford to lose.', at='afford to lose')]),
 dict(at="everything i showed you", els=[
   dict(k='kicker', t='EVERYTHING + MY LINKS'),
   dict(k='url', t='mtgtribe.com/jetup', at='mtg tribe dot com'),
   dict(k='sub', t='The 5 checks, the sources, the step-by-step training and how to join.', center=True)]),
 # full-screen voice-over scene 1 (new line): see render.py SCENES
 dict(at="it pays to pay attention", els=[dict(k='slogan')]),
 dict(at="if you believe in multiple", els=[
   dict(k='kicker', t='IS THIS YOU?'),
   dict(k='rows', rows=[R('💡', 'Multiple streams of income', 'multiple streams'), R('📚', 'Learn before you earn', 'learning before'),
                        R('🧺', 'Never all your eggs in one basket', 'eggs in one basket')])]),
 dict(at="join my tribe at", els=[
   dict(k='kicker', t='JOIN THE MTG TRIBE'),
   dict(k='url', t='mtgtribe.com/group', at='slash group'),
   dict(k='rows', rows=[R('✈️', 'Telegram: @mtgtribe', 'telegram'), R('📲', 'Check my bio', 'check my bio', LIME)])]),
 dict(at="save this video", els=[
   dict(k='kicker', t='HELP SOMEONE CHECK FIRST'),
   dict(k='rows', rows=[R('🔖', 'SAVE this video: keep the 5 checks', 'save this', LIME), R('📤', 'SHARE it with someone who got burned', 'share it'),
                        R('🎓', 'We learn best when we teach others', 'we learn best')])]),
 # full-screen voice-over scene 2 (new line): comment 1 to 5
 dict(at="quick reminder", els=[
   dict(k='kicker', t='QUICK REMINDER'),
   dict(k='head', t='Not financial advice.', s=70),
   dict(k='sub', t='Always do your own research.', at='always do your own', s=34, c=WHITE)]),
 dict(at="thank you for tuning in", els=[
   dict(k='emoji', e='🙏'),
   dict(k='head', t='Thank you for every like, share and comment.', s=54, center=True),
   dict(k='sub', t='Your support means everything.', center=True, at='your support', s=32, c=WHITE)]),
 dict(at="and thank yourself", els=[
   dict(k='emoji', e='🚀'),
   dict(k='head', t='Thank yourself for taking MASSIVE ACTION today', s=56, center=True)]),
 dict(at="i wish you nothing", els=[
   dict(k='emoji', e='👑'),
   dict(k='head', t='YOU are the best.', s=84, c=LIME, center=True, at='because you are')]),
 dict(at="im mtg your digital architect", els=[
   dict(k='photo', d=300),
   dict(k='sig', t='Crypto-Regards, MTG'),
   dict(k='sub', t='See you on the next one 👋', center=True, at='see you on', s=34, c=WHITE),
   dict(k='head', t="Let's Get This Crypto! 💪", s=50, c=LIME, center=True, at='lets get this crypto')]),
]

# small purposeful pops beside MTG (never over his face or the captions): (trigger phrase, emoji)
POPS = [('lost money', '💸'), ('for your family', '❤️'), ('verify together', '🔍'), ('trades gold', '🥇'),
        ('seventy percent is yours', '✅'), ('see your own balance', '👀'), ('whole picture', '🤝'),
        ('look before you deposit', '👀'), ('lose your whole deposit', '⚠️'), ('start small and do', '🌱'),
        ('building a team', '👥'), ('save this video', '🔖'), ('share it with someone', '📤'),
        ('every like', '👍'), ('share and comment', '📤'), ('and comment', '💬'), ('massive action', '🚀'), ('you are the best', '👑'),
        ('telegram at', '✈️')]
