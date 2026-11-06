# Card timeline: (trigger phrase as spoken, card spec). Each card shows from its trigger until the next card.
G = (232, 194, 90); R = (232, 86, 76); GR = (76, 200, 120)

CARDS = [
 ("if youve lost money", dict(kicker='THIS VIDEO IS FOR YOU', head='Lost money before?', rows=[
     ('📉', 'A trading platform'), ('🤖', 'A copy trading app'), ('🎁', 'A program that promised the world')])),
 ("im not going to tell you|im not gonna tell you", dict(strike=('"This one is different"', 'Check it yourself.'))),
 ("five checks you can do", dict(kicker='TODAY', head='5 checks you can do yourself', sub='So whatever you decide, you decide with your eyes open.')),
 ("hi im mtg", dict(big_emoji='👑', head='MTG', hc=G, hs=96, sub='Your Digital Architect · watch for check number 4', subc=True)),
 ("i know the feeling", dict(kicker='SOUND FAMILIAR?', rows=[
     ('⏳', 'The withdrawal that never came'), ('🔇', 'The group that went quiet'), ('📵', 'The leader who stopped answering')])),
 ("you are not foolish", dict(big_emoji='❤️', head='You are not foolish for trying.', hs=68,
     sub='Trying means you want more for your family.', subc=True)),
 ("the lesson is not", dict(kicker='THE LESSON', strike=('Stop trying', 'Verify first.'))),
 ("here is the simple picture", dict(kicker='THE SIMPLE PICTURE', rows=[
     ('👥', 'JetUP: community, training and AI tools. Does NOT trade or take your money'),
     ('🏦', 'TAG Markets: the broker. Account in YOUR name'),
     ('🥇', 'CopyX: connect a strategy, e.g. Sonic AI')], rs=36)),
 ("x a u u s d|xauusd|shown as", dict(kicker='DEFINITION', head='XAU/USD', hc=G, hs=110,
     sub='XAU = gold. USD = US dollar. XAU/USD = the price of gold in US dollars.')),
 ("when the strategy makes a profit", dict(kicker='PROFIT SPLIT', rows=[
     ('✅', '70% is yours', GR), ('⚙️', '30% pays the broker, the strategy provider and the partner program')])),
 ("so if the strategy makes ten", dict(kicker='EXAMPLE', calc=['$10 profit × 70%', '= $7 to you'])),
 ("and if it makes a loss", dict(big_emoji='🛡️', head='Loss = no performance fee', hs=68,
     sub='Performance fee = the cut taken from profits only.', subc=True)),

 ("check one", dict(kicker='CHECK 1 OF 5', head='Who holds my money?', hs=84, big_emoji='💼')),
 ("your deposit goes into", dict(kicker='CHECK 1', rows=[
     ('🏦', 'Your deposit sits in an MT5 account at TAG Markets'),
     ('🪪', 'In YOUR name'),
     ('📖', 'MT5 = MetaTrader 5, the trading app many brokers use')], rs=38)),
 ("dont take my word", dict(big_emoji='🔍', head='Log in yourself. See your own balance.', hs=66)),

 ("check two", dict(kicker='CHECK 2 OF 5', head='Who regulates the broker?', hs=84, big_emoji='⚖️')),
 ("licensed in mauritius", dict(kicker='LICENCE 1 · MAURITIUS', rows=[
     ('🏢', 'T.M. Financials Ltd (TAG Markets trading company)'),
     ('📜', 'FSC Mauritius · Licence GB21026474'),
     ('📖', 'FSC = Financial Services Commission, Mauritius regulator')], rs=36)),
 ("tag also has a south african", dict(kicker='LICENCE 2 · SOUTH AFRICA', rows=[
     ('🇿🇦', 'TM Financials SA (Pty) Ltd'),
     ('📜', 'FSCA authorised · FSP No. 55237'),
     ('📖', 'FSCA = Financial Sector Conduct Authority, SA regulator')], rs=36,
     sub='Verify: fsca.co.za > Regulated Entities > FSP 55237')),
 ("read the fine print", dict(kicker='THE FINE PRINT (TAG WEBSITE)', rows=[
     ('📣', 'SA company: marketing services'),
     ('🏦', 'Trading accounts: held by the Mauritius company'),
     ('❓', 'Know which regulator covers YOUR account', G)], rs=38)),
 ("regulators in austria", dict(kicker='PUBLISHED REGULATOR WARNINGS', rows=[
     ('🇦🇹', 'Austria · FMA'), ('🇱🇺', 'Luxembourg · CSSF'), ('🇸🇮', 'Slovenia · ATVP'),
     ('🇷🇺', 'Russia · Central Bank'), ('🇨🇦', 'Quebec, Canada · AMF')], rs=34, rmin=80,
     sub='Warnings that TAG Markets is not authorised in those countries.')),
 ("i'm telling you this|im telling you this", dict(kicker='CHECK IT YOURSELF', head='Search "TAG Markets"', hs=66,
     url='iosco.org/i-scan', us=60, sub='IOSCO I-SCAN = the global list of regulator warnings. Link on mtgtribe.com/jetup')),

 ("check three", dict(kicker='CHECK 3 OF 5', head='Are the results real?', hs=84, big_emoji='📊')),
 ("sonic ai publishes", dict(kicker='CHECK 3', rows=[
     ('📈', 'Sonic AI track record is public on Myfxbook'),
     ('👀', 'Look BEFORE you deposit')], rs=40, url='jet-up.ai/sonic', us=60)),
 ("it shows plus thirty", dict(kicker='PUBLISHED RESULT', head='+30.1%', hc=G, hs=130,
     sub='3 Nov 2024 to 4 Oct 2026 · GROSS, before the 70/30 split')),
 ("so thirty point one times", dict(kicker='YOUR SHARE', calc=['30.1% × 70%', '= 21.07%', '≈ 21% over ~23 months'],
     sub='Before fees. Not a forecast.', subc=True)),
 ("not forty percent", dict(rows=[('❌', 'NOT 40% a month', R), ('❌', 'NOT a fixed return', R),
     ('⚠️', 'Past results never guarantee the future', G)])),

 ("check four", dict(kicker='CHECK 4 OF 5', head='What can go wrong?', hs=84, big_emoji='⚠️',
     sub='The one most people skip.', subc=True)),
 ("latest start promo", dict(kicker='START PROMO', calc=['$150 yours', '+ $100 promo', '= $250'])),
 ("amplify it twenty four", dict(kicker='AMPLIFY 24x', calc=['$250 × 24', '= $6,000 exposure'],
     sub='Exposure = the size you trade with. NOT money you own.', subc=True)),
 ("thats exposure not money", dict(kicker='THE RISK', rows=[('↕️', 'Bigger exposure = bigger swings, up AND down'),
     ('🔻', 'You can lose your whole deposit', R)], rs=40)),
 ("insolvency cover", dict(kicker='INSOLVENCY COVER', head='$1,000,000 TOTAL', hc=G, hs=82, rows=[
     ('👥', 'For ALL clients together, not per person'), ('🚫', 'Trading losses NOT covered', R)], rs=38,
     sub='Insolvency = the broker itself going bust.')),

 ("check five", dict(kicker='CHECK 5 OF 5', head='Can I get out?', hs=84, big_emoji='🚪')),
 ("profits can be withdrawn", dict(kicker='PROMO RULES', rows=[
     ('💵', 'Profits: withdraw any time'),
     ('📅', 'Bonus: released after 12 months'),
     ('⛔', 'Take your own money out before 12 months = promo ends', R),
     ('📲', 'Check the current rules in your dashboard', G)], rs=36)),
 ("my advice", dict(kicker="MTG'S ADVICE", rows=[('🌱', 'Start small'), ('🧪', 'Test a small withdrawal early'),
     ('✅', 'Let the system prove itself to you', GR)])),

 ("why would anyone still", dict(kicker='WHY SOME STILL GIVE IT A SHOT', rows=[
     ('✅', 'You can check before you deposit'), ('✅', 'You can start small'),
     ('✅', 'The account is in your name'), ('✅', 'Their own warning: "what a partner earns can be zero"')], rs=36)),
 ("one more truth", dict(kicker="FROM JETUP'S OWN FOUNDER", head='The big money comes from building a team,', hs=60,
     sub='not from the trading percentage. Know that going in.')),
 ("if you check all five", dict(big_emoji='🌱', head='Start small.', hc=G, hs=90,
     sub='Only with money you can afford to lose.', subc=True)),
 ("everything i showed you", dict(kicker='EVERYTHING + MY LINKS', url='mtgtribe.com/jetup', us=72,
     sub='The 5 checks, the sources and how to join.', subc=True)),
 ("and if it doesnt feel right", dict(head="Doesn't feel right? That's a good decision too.", hs=62, center=True,
     sub='It pays to pay attention and take action.', subc=True)),
 ("if you believe in multiple", dict(kicker='IS THIS YOU?', rows=[('💡', 'Multiple streams of income'),
     ('📚', 'Learn before you earn'), ('🧺', 'Never all eggs in one basket')])),
 ("join my tribe at", dict(kicker='JOIN THE MTG TRIBE', url='mtgtribe.com/group', us=70, rows=[
     ('✈️', 'Telegram: @mtgtribe'), ('📲', 'Check my bio')])),
 ("save this video", dict(rows=[('🔖', 'SAVE this video: keep the 5 checks', G),
     ('📤', 'SHARE it with someone who got burned'), ('🎓', 'We learn best when we teach others')])),
 ("comment below", dict(big_emoji='💬', head='Which check surprised you most?', hs=66,
     sub='Tell me in the comments.', subc=True)),
 ("quick reminder", dict(kicker='QUICK REMINDER', head='Not financial advice.', hs=72,
     sub='Always do your own research.')),
 ("thank you for tuning in", dict(big_emoji='🙏', head='Thank you for every like, share and comment.', hs=60)),
 ("i wish you nothing but", dict(big_emoji='👑', head='YOU are the best.', hc=G, hs=88)),
]
