// Interaction QA for the ALTRUVA guide (local prod build on :8765)
const { chromium } = require('playwright');
const S = process.argv[2];
const B = process.env.BASE || 'http://localhost:8765/altruva/';
let fails = 0;
function ok(cond, msg) { console.log((cond ? 'PASS ' : 'FAIL ') + msg); if (!cond) fails++; }
async function fonts(ctx) {
  const F = '/tmp/assets/fonts/';
  const css = [['Montserrat', 600, 'Montserrat-600'], ['Montserrat', 500, 'Montserrat-600'], ['Montserrat', 700, 'Montserrat-700'], ['Montserrat', 800, 'Montserrat-800'], ['Orbitron', 700, 'Orbitron-800'], ['Orbitron', 800, 'Orbitron-800']]
    .map(([f, wt, file]) => `@font-face{font-family:'${f}';font-weight:${wt};src:url(https://fonts.gstatic.com/local/${file}.ttf)}`).join('\n');
  await ctx.route('https://fonts.googleapis.com/**', r => r.fulfill({ contentType: 'text/css', body: css }));
  await ctx.route('https://fonts.gstatic.com/local/**', r => r.fulfill({ path: F + r.request().url().split('/').pop(), contentType: 'font/ttf' }));
  await ctx.route('https://api.coingecko.com/**', r => r.abort());
}
async function txt(pg, sel) { return (await pg.textContent(sel)).trim(); }
async function type(pg, sel, v) { await pg.fill(sel, ''); await pg.type(sel, v); }

(async () => {
  const b = await chromium.launch();
  // ---------------- phone
  const ph = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, permissions: ['clipboard-read', 'clipboard-write'] });
  await fonts(ph);
  let pg = await ph.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto(B + 'dashboard/', { waitUntil: 'networkidle' });
  await pg.click('.dtop [data-copy="signup"]');
  await pg.waitForTimeout(500);
  ok(await pg.isVisible('#sheet.on'), 'Sign Up opens the copy sheet');
  ok((await pg.inputValue('#sheet .linkbox')) === 'https://altruva.io/app/packages?ref=0x2731c9Ffa7bb6d226Ba0D6a8320CaD2d5E723997', 'sheet shows exact referral link');
  let clip = ''; try { clip = await pg.evaluate(() => navigator.clipboard.readText()); } catch (e) { clip = 'ERR ' + e.message; }
  ok(clip === 'https://altruva.io/app/packages?ref=0x2731c9Ffa7bb6d226Ba0D6a8320CaD2d5E723997', 'clipboard holds exact referral link (' + clip.slice(0, 40) + ')');
  ok(await pg.evaluate(() => document.querySelector('.dtop [data-copy="signup"]').classList.contains('is-copied')), 'button shows Copied ✓');
  await pg.screenshot({ path: S + '/qa-sheet-390.png' });
  await pg.keyboard.press('Escape'); await pg.waitForTimeout(400);
  ok(await pg.evaluate(() => document.getElementById('sheet').hidden), 'Escape closes the sheet');
  await pg.click('.dtop [data-copy="login"]'); await pg.waitForTimeout(400);
  ok((await pg.inputValue('#sheet .linkbox')) === 'https://altruva.io/app', 'Login copies altruva.io/app');
  await pg.click('#sheet [data-close]'); await pg.waitForTimeout(400);
  await pg.click('#menu-btn'); await pg.waitForTimeout(500);
  ok(await pg.evaluate(() => document.getElementById('side').classList.contains('open')), 'Menu button opens the drawer');
  ok((await pg.getAttribute('#menu-btn', 'aria-expanded')) === 'true', 'menu button aria-expanded true');
  await pg.screenshot({ path: S + '/qa-drawer-390.png' });
  await pg.mouse.click(380, 400); await pg.waitForTimeout(500);
  ok(!(await pg.evaluate(() => document.getElementById('side').classList.contains('open'))), 'Tap outside closes the drawer');
  await pg.click('.vtile[data-play="e1"]'); await pg.waitForTimeout(800);
  ok(await pg.isVisible('#player.on'), 'Progress tile opens the video player');
  ok((await pg.getAttribute('#player video', 'src')).endsWith('media/altruva-explainer-1-where-every-dollar-goes.mp4'), 'player loads Explainer 1');
  await pg.screenshot({ path: S + '/qa-player-390.png' });
  await pg.click('#player [data-mark]'); await pg.waitForTimeout(300);
  await pg.keyboard.press('Escape'); await pg.waitForTimeout(400);
  ok((await txt(pg, '[data-ring] [data-k="n"]')) === '1', 'Mark as watched updates the progress ring to 1');
  ok(await pg.evaluate(() => document.querySelector('.vtile[data-vid="e1"]').classList.contains('watched')), 'tile ticked');
  await pg.reload({ waitUntil: 'networkidle' });
  ok((await txt(pg, '[data-ring] [data-k="n"]')) === '1', 'progress persists after reload');

  // calculators
  await pg.goto(B + 'dashboard/tools/withdraw-split-calculator/', { waitUntil: 'networkidle' });
  ok((await txt(pg, '[data-out="wallet"]')) === '11.81 USDT', 'split default = real example 11.81 (' + await txt(pg, '[data-out="wallet"]') + ')');
  await pg.click('text=Total deposit 6,000'); ok((await txt(pg, '[data-out="wallet"]')) === '120.00 USDT' && (await txt(pg, '[data-out="re"]')) === '80.00 USDT', 'split 200 at 6,000 = 120 / 80');
  await pg.click('text=Total deposit 60,000'); ok((await txt(pg, '[data-out="wallet"]')) === '700.00 USDT', 'split 1000 at 60,000 = 700');
  await type(pg, '#bal', '23,63'); await type(pg, '#tot', '5 000'); ok((await txt(pg, '[data-out="wallet"]')) === '11.81 USDT', 'decimal comma and space thousands parse');
  await type(pg, '#tot', '5000.5'); ok((await txt(pg, '[data-out="tier"]')) === '60% / 40%', 'just above 5,000 is 60/40');
  await type(pg, '#bal', 'abc'); ok((await txt(pg, '[data-err="bal"]')).length > 0, 'invalid input shows an error');
  await pg.screenshot({ path: S + '/qa-split-390.png', fullPage: false });

  await pg.goto(B + 'dashboard/tools/working-level-calculator/', { waitUntil: 'networkidle' });
  ok((await txt(pg, '[data-out="earn"]')) === '10.00 USDT', 'WL default: direct buys Elite = 10.00');
  await pg.click('text=A level 7 deposit'); ok((await txt(pg, '[data-out="earn"]')) === '1.00 USDT', 'WL level 7 with 3 directs = 1.00');
  await pg.click('text=Same, 2 directs'); ok((await txt(pg, '[data-out="earn"]')) === '0.00 USDT' && (await txt(pg, '[data-out="stay"]')) === '1.00 USDT', 'WL level 7 with 2 directs stays in contract');
  ok((await txt(pg, '[data-pay="7"]')).startsWith('Closed'), 'closed level shows Closed under its field');
  await pg.click('text=A level 7 deposit'); ok((await txt(pg, '[data-pay="7"]')) === '1% = 1.00', 'open level shows what it pays under its field');

  await pg.goto(B + 'dashboard/tools/matching-calculator/', { waitUntil: 'networkidle' });
  ok((await txt(pg, '[data-out="earn"]')) === '7.94 USDT', 'matching day 22 = 7.94 (' + await txt(pg, '[data-out="earn"]') + ')');
  await pg.click('details.mini summary'); await type(pg, '#biz', '124304.01'); await type(pg, '#all', '391251.10');
  ok((await txt(pg, '[data-out="rate2"]')).includes('0.079427'), 'rate tool gives 0.079427');

  await pg.goto(B + 'dashboard/tools/usdt-to-rand/', { waitUntil: 'networkidle' });
  await pg.waitForTimeout(600);
  ok((await txt(pg, '[data-out="status"]')).includes("Couldn't load"), 'rate failure is explained');
  await type(pg, '#zrate', '18.5'); ok((await txt(pg, '[data-out="main"]')) === 'R1,850.00', '100 USDT at 18.5 = R1,850.00');
  await type(pg, '#fee', '15'); ok((await txt(pg, '[data-out="net"]')) === 'R1,835.00', 'after R15 fee = R1,835.00');
  await pg.click('[data-amt="28"]'); ok((await txt(pg, '[data-out="main"]')) === 'R518.00', 'Starter + BNB sets 28 USDT = R518.00 at 18.5');
  ok((await txt(pg, '[data-out="pkres"]')).includes('R518.00'), 'package box shows the rand result right under the buttons');
  await pg.click('[data-amt="105"]'); ok((await pg.inputValue('#amt')) === '105', 'Elite + BNB sets 105');
  await pg.click('[data-dir="z2u"]'); await type(pg, '#amt', '1000');
  ok(await pg.evaluate(() => document.querySelector('[data-pkgs]').offsetParent === null), 'package buttons hide in Rand to USDT mode'); ok((await txt(pg, '[data-out="main"]')) === '54.86 USDT', 'R1000 + R15 fee needs 54.86 USDT');
  await pg.screenshot({ path: S + '/qa-zar-390.png', fullPage: false });

  await pg.goto(B + 'dashboard/is-it-right-for-me/', { waitUntil: 'networkidle' });
  for (const k of ['afford', 'phone', 'watch', 'risk', 'teach']) await pg.click(`.fit-q:has([data-fit="${k}"])`);
  ok((await txt(pg, '[data-k="score"]')) === '5 of 5', 'fit check counts 5 of 5');
  await pg.goto(B + 'dashboard/glossary/', { waitUntil: 'networkidle' });
  await type(pg, '[data-gfilter]', 'renounced');
  ok((await pg.$$eval('[data-term]', ts => ts.filter(t => !t.hidden).length)) >= 1, 'glossary filter finds renounced');
  await pg.goto(B + 'dashboard/tutorials/#t3', { waitUntil: 'networkidle' });
  ok((await pg.getAttribute('.now .vid', 'data-vid')) === 't3', 'playlist opens #t3 from the link');
  await pg.click('[data-pick="t5"]'); await pg.waitForTimeout(500);
  ok(!/^\d+$/.test(await txt(pg, '[data-k="desc"]')) && (await txt(pg, '[data-k="desc"]')).length > 20, 'playlist shows the video description, not its number');
  ok((await pg.$$('[data-pick]')).length === 12, 'tutorials page lists 7 tutorials and 5 tool trainings');
  ok((await pg.getAttribute('.now .vid', 'data-vid')) === 't5' && !!(await pg.$('.now video')), 'playlist item plays in the main player');
  for (const [u, k] of [['tools/usdt-to-rand/', 'k1'], ['tools/withdraw-split-calculator/', 'k2'], ['tools/working-level-calculator/', 'k3'], ['tools/matching-calculator/', 'k4']]) {
    await pg.goto(B + 'dashboard/' + u, { waitUntil: 'domcontentloaded' });
    ok(!!(await pg.$(`figure.vid[data-vid="${k}"]`)), `${u} shows its tool training video`);
  }
  await pg.goto(B + 'dashboard/first-72-hours/', { waitUntil: 'domcontentloaded' });
  ok(!!(await pg.$('[data-play="k5"]')), '72-hour page links its clock training');
  await pg.goto(B + 'dashboard/global-leg/', { waitUntil: 'networkidle' });
  await pg.click('[data-leg] [data-w="10"]'); ok((await pg.$$eval('.seats i.on', x => x.length)) === 20, 'Starter window lights 20 seats');
  await pg.goto(B + 'dashboard/working-levels/', { waitUntil: 'networkidle' });
  await pg.click('[data-wl] [data-d="1"]'); ok((await txt(pg, '[data-wl] [data-k="pc"]')) === '16', '1 direct opens 16% of the 25%');
  ok(errs.length === 0, 'no page errors on phone (' + errs.join(' | ') + ')');

  // ---------------- desktop
  const dk = await b.newContext({ viewport: { width: 1440, height: 900 } });
  await fonts(dk);
  pg = await dk.newPage(); pg.on('pageerror', e => errs.push(e.message));
  await pg.goto(B + 'dashboard/packages/', { waitUntil: 'networkidle' });
  await pg.click('#side-toggle'); await pg.waitForTimeout(500);
  ok(await pg.evaluate(() => document.documentElement.classList.contains('side-off')), 'collapse pill hides the menu');
  await pg.screenshot({ path: S + '/qa-collapsed-1440.png' });
  await pg.goto(B + 'dashboard/faq/', { waitUntil: 'networkidle' });
  ok(await pg.evaluate(() => document.documentElement.classList.contains('side-off')), 'menu state remembered on the next page');
  await pg.click('#side-toggle');
  await pg.goto(B, { waitUntil: 'networkidle' });
  await pg.click('.stn [data-play="t1"]'); await pg.waitForTimeout(600);
  ok(await pg.isVisible('#player.on'), 'landing station opens Tutorial 1 in the player');
  await pg.keyboard.press('Escape'); await pg.waitForTimeout(300);
  await pg.click('.hero-cta a'); await pg.waitForLoadState('networkidle');
  ok(pg.url().endsWith('/altruva/dashboard/'), 'Enter the dashboard goes to /altruva/dashboard/');
  // reduced motion
  const rm = await b.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' });
  await fonts(rm); pg = await rm.newPage();
  await pg.goto(B, { waitUntil: 'networkidle' });
  ok((await pg.$$eval('.rv.pre', x => x.length)) === 0, 'reduced motion: nothing hidden for reveal');
  ok(errs.length === 0, 'no page errors overall');
  console.log(fails ? `${fails} FAILED` : 'ALL PASSED');
  await b.close();
})();
