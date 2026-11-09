# The sign-up training page: mtgtribe.com/jetup/get-started/
from layout import *

def shot(p, alt):
    return ('<div><button type="button" class="shot" data-zoom="/jetup/img/steps/guide-p%s.webp" data-alt="%s"><img src="/jetup/img/steps/guide-p%s-640.webp" width="640" height="360" alt="%s" loading="lazy"></button>'
            '<p class="shot-cap">%sTap to zoom: %s</p></div>') % (p, alt, p, alt, icon('i-zoom'), alt)

def k(t):
    return '<kbd>%s</kbd>' % t

def part(n, title, sub, steps, shots, success, extra_before='', extra_after=''):
    st = ''.join('<li><span>%s</span></li>' % s for s in steps)
    sh = ''.join(shot(p, a) for p, a in shots)
    return f'''<article class="card pad partcard rv" id="part-{n}" aria-labelledby="p{n}-h">
 <div class="ph"><span class="pn">{n}</span><div><small>Part {n} of 6</small><h2 id="p{n}-h">{title}</h2></div></div>
 <p class="lede" style="margin:0 0 16px">{sub}</p>
 <div class="pgrid">
  <div>{extra_before}<ol class="steps">{st}</ol>{extra_after}
   <p class="success">{icon('i-check2')}<span>Success check: {success}</span></p>
   <div data-ticks="parts"><button type="button" class="tick ptick" data-id="p{n}" aria-pressed="false"><span class="bx">{icon('i-check2')}</span>I've done part {n}</button></div></div>
  <div class="shots">{sh}</div>
 </div>
</article>'''

def build_start():
    path = '/jetup/get-started/'
    wallets = [
     (VALR, 'VALR', 'First choice. MTG\'s referral link', '#2d6df6', '1st', True),
     (BINANCE, 'Binance', 'If you prefer Binance. MTG\'s referral link', '#f0b90b', '2nd', True),
     ('https://www.safepal.com/', 'SafePal', 'Web3 wallet. Official website', '#4a3df0', 'Web3', False),
     ('https://metamask.io/', 'MetaMask', 'Web3 wallet. Official website', '#f6851b', 'Web3', False),
    ]
    wal = ''.join('<a class="wal" style="--wb:%s;--wc:%s" href="%s" target="_blank" rel="%s"><span class="rank%s">%s</span><span class="wl">%s</span><span><b>%s</b><small>%s</small></span></a>' % (
        c, c, h, 'noopener sponsored' if ref else 'noopener', '' if r in ('1st',) else ' n', r, icon('i-wallet2'), name, sub) for h, name, sub, c, r, ref in wallets)
    ready = [
     ('r1', 'i-link', 'The Partner link from the person who invited you', 'If MTG invited you, tap any Join JetUP button on this guide: it opens his Partner link.'),
     ('r2', 'i-mail', 'Your email and your phone', 'Use the same email for JetUP, TAG Markets and the promo.'),
     ('r3', 'i-id', "Your ID, driver's licence or passport", 'For KYC, which means Know Your Customer: proving who you are.'),
     ('r4', 'i-wallet2', 'About $155 in USDT or USDC on VALR or Binance', 'Stablecoins: digital dollars. Keep a little extra for the network fee.'),
     ('r5', 'i-key', 'The two community token codes', 'You use them in part 5. They are shown big on this page.'),
    ]
    ready_html = ''.join('<button type="button" class="tick" data-id="%s" aria-pressed="false"><span class="bx">%s</span><span><b>%s</b><small>%s</small></span></button>' % (i, icon('i-check2'), t, s) for i, ic, t, s in ready)

    p1 = part(1, 'Create your JetUP account', 'Open the Partner link from your sponsor and fill in the sign-up form.', [
        "Open the <b>Partner</b> link from your sponsor. Every member has two links, Partner and Client: make sure it's the Partner link. If MTG invited you, tap any " + k('Join JetUP') + " button on this guide. Invited by someone else? Use their Partner link.",
        'On the sign-up form, choose ' + k('Individual') + '.',
        'Type your first name and last name <b>exactly as they are on your ID</b> (no nickname, or your KYC will not match), then your email and a password, using English letters only.',
        'Choose your country, then type your cell number <b>without the first 0</b>. The country code (for example +27) is already there.',
        'Your password: <b>8 to 12 characters</b>, with an uppercase letter, a lowercase letter, a number and a special character (! @ $ % _ # ( )), with no spaces. Write it down somewhere safe: you use the same password for TAG Markets.',
        'Wait for the security check to show the green ' + k('Success!') + ', then tap ' + k('Register Now') + '. If it says the email is already registered, use another email, or log in with that one.',
        'Check your email and tap the verification link. Not in your inbox? Check spam or junk mail.',
      ], [('01', "The sponsor's Partner link (top left) and Client link"), ('02', 'The JetUP sign-up form'), ('03', 'Check your email, then verify')],
      'you see "Registration Successful. You can now log in." After you verify your email and log in, your profile shows Account Type: Partner.',
      extra_before='<div class="pvid">' + phone('tut1', "Watch MTG do part 1 (3:46)") + '</div>')
    p2 = part(2, 'Link JetUP to TAG Markets', 'One tap inside JetUP creates and links your TAG Markets account.', [
        'Log in at <b>jetup.ibportal.io</b> with the email and password you created in part 1.',
        'On your profile, scroll down to the CopyX banner and tap ' + k('Register CopyX') + '.',
        'Enter the <b>same password</b> you created on JetUP, read and tick the three boxes, then tap ' + k('Sync Account') + '. You\'ll see ' + k('Syncing with Copy X...') + ', then ' + k('Sync Successful!') + '.',
        'Tick "I understand that I need to review my email and validate my password..." and tap ' + k('Close') + '. The banner now says ' + k('User Active') + ' and the button says ' + k('Login to CopyX') + '.',
        'Tap ' + k('Login to CopyX') + '. TAG Markets opens at <b>portal.tagmarkets.com</b>. Wait for the "Verify you are human" check, then log in with the <b>same email and exactly the same password</b>.',
        'Check your email for the TAG Markets email and tap ' + k('Confirm email address') + '. It can take a while: MTG\'s arrived after his first log in. Not in your inbox? Check spam or junk mail. You\'ll see "Verification successful". If the page does not move on, tap ' + k('click here') + ' and log in again.',
      ], [('04', 'The CopyX banner in your JetUP profile'), ('05', 'Syncing with Copy X')],
      'the banner says "User Active" (with your CU number), and you are on your TAG Markets dashboard with your email confirmed.',
      extra_before='<div class="pvid">' + phone('tut2', "Watch MTG do part 2 (3:42)") + '</div>',
      extra_after='<p class="call info" style="margin-top:12px">%s<span><b>Register through JetUP, not directly on CopyX,</b> so your account links to your team.</span></p><p class="call info" style="margin-top:10px">%s<span><b>"Username and/or Password are incorrect"?</b> Use exactly the password you created on JetUP, with the same capitals, numbers and symbols.</span></p>' % (icon('i-alert'), icon('i-info2')))
    p3 = part(3, 'Verify your identity', "Sumsub checks your ID and a selfie for TAG Markets.", [
        'On your TAG Markets dashboard (<b>portal.tagmarkets.com</b>), tap ' + k('upload documents') + ' in "Please complete your KYC verification in order to make a deposit".',
        'Sumsub runs the identity check for TAG Markets. You opened it from TAG Markets, so tap ' + k('Continue') + '.',
        'Confirm your country of residence and tap ' + k('Agree and continue') + '.',
        'Under "Get verified faster with Sumsub ID", enter <b>the same email you have used from the start</b> and tap ' + k('Start verification') + '. Type the 6-digit code Sumsub emails you (not in your inbox? check spam or junk). Never share this code with anyone.',
        'Read the consent, tick the box and tap ' + k('Create my account') + '. You see "Sumsub ID account successfully created": tap ' + k('Continue verification') + '.',
        'Choose your issuing country and your document (MTG chose ' + k('Identity Card') + '). If it has two sides, tick ' + k('My document is double-sided') + ' and tap ' + k('Continue') + '. Read the tips (a well lit room, no reflections, never edit the images) and tap ' + k('Continue') + '.',
        'When the browser asks to use the camera, tap ' + k('Allow') + '. Hold your ID inside the frame: it takes the photo by itself (move the phone back a little if it does not). Front, then back.',
        'Step 2 is a quick selfie: a well lit place, your face in the frame, no hat, glasses or mask. Hold still until you see ' + k('All set') + '.',
        'TAG Markets may also ask a few questions (your income, net worth, investment goal and whether you understand the risks): answer honestly. Read TAG Markets\' short reminder (for example, the service is not for residents of the European Union), then continue.',
      ], [('06', "TAG Markets' questions and reminder"), ('07', 'The Sumsub identity check')],
      'you see "All set". TAG Markets reviews your documents, and once you are verified you can make your deposit (part 4).',
      extra_before='<div class="pvid">' + phone('tut3', "Watch MTG do part 3 (3:37)") + '</div>',
      extra_after='<p class="call info" style="margin-top:12px">%s<span><b>"This site can\'t ask for your permission"?</b> Close screen recorders and chat bubbles (for example WhatsApp), then tap Try again and Allow.</span></p><p class="call info" style="margin-top:10px">%s<span><b>"Documents submitted on another profile"?</b> You already have a TAG Markets profile with these documents. One person, one profile: do not open a second account. Ask your sponsor or TAG Markets support.</span></p><p class="call info" style="margin-top:10px">%s<span><b>CFD</b> means contract for difference: you trade a price movement without owning the asset.</span></p>' % (icon('i-info2'), icon('i-info2'), icon('i-info2')))
    p4 = part(4, 'Fund your account', 'Send $155 from your exchange to your TAG Markets deposit address.', [
        'Log in at <b>portal.tagmarkets.com</b> with the same email and password.',
        'Under ' + k('My wallet balances') + ', tap ' + k('Deposit') + '.',
        'Choose ' + k('USD') + ', tap ' + k('Other') + ' and type ' + k('155') + '.',
        'Tap ' + k('Next') + ', choose ' + k('Crypto') + ' and tap ' + k('Submit') + '.',
        'Pick the coin <b>and</b> the network you are sending from (see the network ranking above). Copy the deposit address and the exact amount. The price is held for about 15 minutes, so keep moving.',
        'Open your exchange (the example is VALR). Choose withdraw, paste the address and choose the <b>same network</b>.',
        'Enter the amount and look at the fee. In the example it is 0.71 USDC on Ethereum: 155.00 + 0.71 = 155.71 USDC in total.',
        'For recipient details choose ' + k('Individual') + ', then ' + k('Self-hosted Wallet') + '. Check the address matches TAG Markets exactly, then tap ' + k('CONFIRM WITHDRAWAL') + '.',
        'Open the email VALR sends you and tap ' + k('Authorize Transaction') + '.',
      ], [('08', 'Log in to TAG Markets, tap Deposit'), ('09', 'Other, 155, Crypto, Submit'), ('11', 'In VALR: withdraw on the same network'), ('12', 'Self-hosted wallet, confirm, authorise'), ('13', 'Payment found, then payment successful')],
      'back in TAG Markets you see "Payment found!", then "Payment successful." In the example it took about 3 minutes.',
      extra_after='<p class="call info" style="margin-top:12px">%s<span><b>Match the network on both sides</b> (for example BEP20 to BEP20), so your funds arrive safely.</span></p>' % icon('i-info2'))
    codes = f'''<div class="codes">
     <div class="code"><small>Code 1, then Verify</small><b>#9M</b><span class="then">Hashtag, nine, capital M</span><button type="button" class="copy" data-copy="#9M">{icon('i-copy2')}<span class="lbl">Copy #9M</span><span class="done">Copied ✓</span></button></div>
     <div class="code"><small>Code 2, then Submit</small><b>9MPromo</b><span class="then">Capital M, capital P</span><button type="button" class="copy" data-copy="9MPromo">{icon('i-copy2')}<span class="lbl">Copy 9MPromo</span><span class="done">Copied ✓</span></button></div>
    </div><p class="small" style="margin:0 0 14px;font-weight:700">Both codes are case sensitive. They come from MTG's team.</p>'''
    p5 = part(5, 'Connect Sonic AI', 'The part most people rush. Slow down here.', [
        'Open the menu, tap ' + k('CopyX') + ', find <b>SONIC</b> (the first one in the list) and tap ' + k('Details') + ', then ' + k('Connect') + '. <b>Don\'t pick any other trader.</b>',
        'Read the terms: a 30% performance fee taken from profits only, no management fee, no join fee, a one month minimum, and an Amplify account.',
        'In ' + k('Investment') + ' type ' + k('50') + '. <b>Only 50.</b> The screen shows a $10 minimum, but 50 is the plan. Leave the other $100 in your balance for the promo.',
        '<b>Read the account rules on this screen:</b> the account closes if the trader\'s loss passes 10% of the starting balance. With a community token, that limit becomes 5%.',
        'Tap the arrow next to ' + k('Community Token') + '. Enter code 1, ' + k('#9M') + ', and tap ' + k('Verify') + '.',
        'A second field opens. Enter code 2, ' + k('9MPromo') + ', tap ' + k('Submit') + ' and wait for the tick.',
        'Tick both agreements. The second one says CopyX trades come from traders who are not part of TAG Markets. Then tap ' + k('Copy Now') + '.',
      ], [('14', 'Menu, CopyX, Sonic, Details, Connect'), ('15', 'Investment 50, then the community token'), ('16', '#9M, Verify, 9MPromo, Submit, the tick'), ('17', 'Copy Now, Success, then Profile')],
      'you see "Success". Your $50 Sonic account is connected.',
      extra_before=codes,
      extra_after='<p class="call info" style="margin-top:12px">%s<span><b>Why the plan starts with $50:</b> 24x Amplify makes every move bigger, in both directions, so a small start lets you learn how it moves.</span></p><p class="call info" style="margin-top:10px">%s<span><b>New to Sonic AI?</b> Watch <a href="/jetup/how-it-works/#copy">JetUP\'s own 64-second Sonic AI video</a> first: what it trades, and why your money stays in your own account.</span></p>' % (icon('i-info2'), icon('i-film2')))
    p6 = part(6, 'Claim the Dennis Fast Start Promo', 'Your CU number unlocks the $100 promo bonus.', [
        'In TAG Markets open the menu, tap ' + k('Profile') + ' and write down your <b>CU number</b>.',
        'Go to <b>jet-up.ai</b> and tap the orange ' + k('Dennis Fast Start Promo') + ' tile.',
        'Enter your name, email and CU number exactly as in TAG Markets, then tap ' + k('Join the promo') + '.',
        "You'll see " + k('Application received!') + ' Approval usually takes a few minutes and can take up to 24 hours. Wait for the confirmation email.',
        'When it arrives, open ' + k('CopyX') + ', then ' + k('Follower Hub') + ', then ' + k('Strategies') + '.',
        "You'll see two Sonic accounts: your $50 account ($50 × 24 = $1,200) and your $200 promo account ($200 × 24 = $4,800).",
      ], [('18', 'jet-up.ai: the orange Dennis Fast Start Promo tile and form'), ('20', 'Follower Hub, Strategies, both accounts (balances blurred)')],
      'both Sonic accounts show under Strategies.',
      extra_before='<div style="margin:0 0 18px">' + laptop('promo', "Watch the promo explained (2:18)") + '</div>',
      extra_after='<p class="call info" style="margin-top:12px">%s<span><b>Know the promo rules:</b> profits can be withdrawn any time. The $100 bonus is released after 12 months. Taking your own money out before then ends the promo. Rules can change, so check your dashboard. <a href="/jetup/promo/">All the promo rules</a></span></p>' % icon('i-info2'))

    AFTER = f'''<section class="sec tight" id="after" aria-labelledby="after-h">
 <div class="wrap stack" style="gap:22px">
  <div class="center rv"><p class="eyebrow">After you're set up</p><h2 class="h2" id="after-h">Three things you'll want <span class="grad">next</span></h2></div>
  <div class="grid3">
   <article class="card pad rv" id="mt5" aria-labelledby="mt5-h">
    <span class="ped" style="display:inline-grid;margin-bottom:12px"><b>{icon('i-candle2')}</b></span><h3 id="mt5-h" style="margin:0 0 6px;font:800 1.3rem/1.25 var(--f-b)">See every trade in MetaTrader 5</h3>
    <p class="muted">A read-only view of your own account. You can watch, not trade or withdraw.</p>
    <ol class="steps">
     <li><span>Install <b>MetaTrader 5</b> (MT5) from the App Store or Google Play.</span></li>
     <li><span>Tap {k('New account')} (or add an account) and search for <b>TM Financials</b>, the company behind TAG Markets.</span></li>
     <li><span>In TAG Markets open {k('CopyX')}, then {k('Follower Hub')}, then {k('Strategies')}, and tap the eye icon on one account.</span></li>
     <li><span>Copy the <b>account number</b> (your MT5 login) and the <b>investor password</b>. Paste them into MT5 and tap {k('Continue')}.</span></li>
     <li><span>Open {k('History')}. Add your other account the same way.</span></li>
    </ol>
    <p class="success">{icon('i-check2')}<span>Success check: your account opens in MT5. Sonic usually trades only two or three times a day, so a new account's history can be empty at first.</span></p>
   </article>
   <article class="card pad rv" id="more" aria-labelledby="more-h">
    <span class="ped" style="display:inline-grid;margin-bottom:12px"><b>{icon('i-layers2')}</b></span><h3 id="more-h" style="margin:0 0 6px;font:800 1.3rem/1.25 var(--f-b)">Open another strategy later</h3>
    <p class="muted">Your JetUP membership stays. Each new deposit can become its own Sonic account.</p>
    <ol class="steps">
     <li><span>In TAG Markets tap {k('Deposit')} and fund your balance the same way as part 4.</span></li>
     <li><span>Open {k('CopyX')}, find <b>SONIC</b>, tap {k('Details')}, then {k('Connect')}, and type the amount.</span></li>
     <li><span>Enter the two community codes again, exactly as in part 5. They set the Amplify, so don't skip them.</span></li>
    </ol>
    <p class="call info" style="margin-top:12px">{icon('i-info2')}<span>The Dennis Fast Start Promo is <b>one time only</b>. New strategies don't get another $100 bonus. Every account follows the same rules: 24x Amplify, the 10% loss limit (5% with a community token) and a one month minimum.</span></p>
   </article>
   <article class="card pad rv" id="earnings" aria-labelledby="earn-h">
    <span class="ped" style="display:inline-grid;margin-bottom:12px"><b>{icon('i-wallet2')}</b></span><h3 id="earn-h" style="margin:0 0 6px;font:800 1.3rem/1.25 var(--f-b)">Withdraw or reinvest</h3>
    <p class="muted">Profits, and partner earnings if you share JetUP. <a href="/jetup/partner-plan/">See how the partner plan pays</a>.</p>
    <ol class="steps">
     <li><span>In the JetUP portal (jetup.ibportal.io) open your <b>Wallet</b> to see partner earnings. Tap {k('Withdraw')} and choose your <b>TAG wallet</b> or one of your MT5 accounts.</span></li>
     <li><span>To send money out, first add your own crypto wallet address under {k('Wallets')} (for example VALR, Binance, SafePal or your BIX wallet), then choose it when you withdraw.</span></li>
     <li><span>In CopyX, {k('Reinvest')} adds a strategy's profit back into that same strategy. It starts a new one month minimum for that account.</span></li>
    </ol>
    <p class="call lime" style="margin-top:12px">{icon('i-shield2')}<span>Start small and test a small withdrawal early. Fees, limits and timing are the broker's terms, so check them in your account.</span></p>
   </article>
  </div>
 </div>
</section>
'''
    main = f'''
{phead('i-rocket2', 'Sign-up training', 'JetUP + TAG Markets, <span class="grad">one tap at a time</span>',
       "Grab your phone. We're going to do this together: your JetUP account, your TAG Markets account, your first deposit, the Sonic AI strategy and the Dennis Fast Start Promo. Take your time. You can pause any step and follow along.",
       [('MTG TRIBE', '/'), ('JetUP Guide', '/jetup/'), ('Sign-Up Training', None)],
       [icon('i-film2') + '9:09 training', icon('i-layers2') + '6 parts', icon('i-phone') + 'Phone friendly'])}

<section class="sec tight" style="padding-top:0" aria-label="The training video">
 <div class="wrap">
  <div style="max-width:980px;margin:0 auto" class="rv">{laptop('training', 'Watch it once all the way, then follow the parts below at your own pace', eager=True)}</div>
  <div class="block rv vstrip" id="videos">
   <p class="eyebrow" style="margin-bottom:6px">Step-by-step videos, one per part</p>
   <p class="small" style="margin:0 0 16px">MTG records each part on his phone, tap by tap. Each video also sits at the top of its part below.</p>
   <div class="vlist"><div class="vpart">{phone('tut1')}<b>Part 1</b><small>Create your JetUP account</small></div>
    <div class="vpart">{phone('tut2')}<b>Part 2</b><small>Link JetUP to TAG Markets</small></div>
    <div class="vpart">{phone('tut3')}<b>Part 3</b><small>Verify your identity (KYC)</small></div>
    <div class="vsoon"><b>Parts 4 to 6</b><small>Deposit, Sonic AI and the promo: coming next.</small></div></div>
  </div>
  <div class="block rv" id="wallets">
   <p class="eyebrow" style="margin-bottom:14px">Need USDT or USDC? Start here</p>
   <div class="wallets">{wal}</div>
   <p class="small" style="margin:12px 0 0">VALR and Binance are MTG's referral links. SafePal and MetaMask go to their official websites.</p>
  </div>
 </div>
</section>

<section class="sec tight" aria-labelledby="ready-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap grid2" style="align-items:start">
  <div class="rv">
   <p class="eyebrow">Before we start</p>
   <h2 class="h2" style="margin:12px 0 18px" id="ready-h">Get these <span class="grad">5 things</span> ready</h2>
   <div class="ready" data-ticks="ready">{ready_html}</div>
   <div class="prog" style="justify-content:flex-start"><span class="ring" data-ring="ready"><svg viewBox="0 0 72 72" aria-hidden="true"><circle class="bg" cx="36" cy="36" r="30"/><circle class="fg" cx="36" cy="36" r="30"/></svg><b>0</b></span>
    <p data-msg="of 5 ready. Your ticks stay on this phone only." data-done="All 5 ready. Let's go! 🚀" aria-live="polite">of 5 ready.</p></div>
   <div class="joinrow" style="margin:16px 0 0">{join_btn('Join JetUP', 'btn btn-lime')}<a class="btn btn-ghost" href="{WA_MTG}" target="_blank" rel="noopener">{icon('i-whatsapp')}Questions? Ask MTG</a></div>
   {join_note()}
  </div>
  <div class="stack">
   <div class="card pad rv" style="--d:1">
    <p class="eyebrow">Networks, in order</p>
    <h3 class="h3" style="margin:10px 0 14px">Pick one, and use the same one on both sides</h3>
    <div class="stack">
     <div class="card net" style="background:rgba(255,255,255,.03)"><div class="top2"><b>USDT · BEP20</b><span class="medal">1</span></div><p>BNB Smart Chain, Binance's blockchain. First choice, with low fees, when your exchange offers it.</p><span class="fee lo">Low fees</span></div>
     <div class="card net n2" style="background:rgba(255,255,255,.03)"><div class="top2"><b>USDT · TRC20</b><span class="medal">2</span></div><p>The Tron network. Second choice.</p><span class="fee lo">Low fees</span></div>
     <div class="card net n3" style="background:rgba(255,255,255,.03)"><div class="top2"><b>USDC · ERC20</b><span class="medal">3</span></div><p>The Ethereum network. Fine if you prefer it, but the most expensive of the three.</p><span class="fee hi">Highest fees</span></div>
    </div>
    <p class="call info" style="margin-top:14px">{icon('i-info2')}<span><b>Use the same network on both sides,</b> and your funds arrive safely.</span></p>
   </div>
   <div class="card pad rv" style="--d:2">
    <p class="eyebrow">You'll use three websites</p>
    <ul class="plist" style="margin-top:14px">
     <li><span class="e" aria-hidden="true">🚪</span><span><b>jetup.ibportal.io</b>: your JetUP portal, the community's front door</span></li>
     <li><span class="e" aria-hidden="true">🏦</span><span><b>portal.tagmarkets.com</b>: TAG Markets, the broker, where your money sits in your own name</span></li>
     <li><span class="e" aria-hidden="true">🎁</span><span><b>jet-up.ai</b>: JetUP's hub, where you claim the promo</span></li>
    </ul>
   </div>
  </div>
 </div>
</section>

<section class="sec tight" aria-label="The six parts">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap stack" style="gap:22px">
  {p1}{p2}{p3}{p4}{p5}{p6}
  <div class="card pad rv center" style="display:grid;justify-items:center;gap:14px">
   <p class="eyebrow">Done, one tap at a time</p>
   <h2 class="h2">Account. Identity. Deposit. <span class="grad">Strategy. Promo.</span></h2>
   <p class="lede" style="max-width:40rem">Screens change over time, so if yours looks a little different, look for the same words. Save this page, so it's here when you need it, and share it with someone who's ready to start.</p>
   <div class="ctas" style="justify-content:center"><a class="btn btn-pri" href="{GROUP}">{icon('i-whatsapp')}Stuck? Ask in the tribe</a><a class="btn btn-ghost" href="/jetup/five-checks/">{icon('i-shield2')}Do the 5 checks</a></div>
  </div>
 </div>
</section>
{AFTER}
{tribe_cta('Comment <span class="lime">DONE</span> when you\'re set up.', 'Stuck on a step? Comment the part number under the video on YouTube or TikTok, and the step most of you ask about becomes my next video. Or ask the tribe on WhatsApp.')}
'''
    crumbs_l = [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('Sign-Up Training', None)]
    howto = {"@type": "HowTo", "name": "How to join JetUP and TAG Markets, connect Sonic AI and claim the Dennis Fast Start Promo",
             "totalTime": "PT45M", "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": SITE + path + '#part-%d' % (i + 1)} for i, n in enumerate(
              ['Create your JetUP account', 'Link JetUP to TAG Markets', 'Verify your identity', 'Fund your TAG Markets account', 'Connect Sonic AI', 'Claim the Dennis Fast Start Promo'])]}
    ld = [ld_video('training'), ld_video('tut1'), ld_video('tut2'), ld_video('tut3'), ld_video('promo'), howto]
    return page(path, 'How to Join JetUP and TAG Markets: Step-by-Step Training | MTG',
                'Join JetUP and TAG Markets one tap at a time: sign up, link CopyX, KYC, the TAG Markets deposit (BEP20, TRC20, ERC20), connect Sonic AI with the community codes and claim the Dennis promo.',
                main, crumbs_l, ld, og_img='/jetup/img/cover-signup-training-v4-4.jpg', og_alt='Join JetUP + TAG Markets: every tap shown, 6 parts, phone friendly', lightbox=True)
