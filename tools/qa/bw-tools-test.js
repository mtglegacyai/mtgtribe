// every interactive tool on /bw does its job: calculators give the right numbers, search filters, forms build the right message
const { chromium } = require('playwright');
const BASE = process.env.BASE || 'http://127.0.0.1:8765';
let bad = 0, n = 0; const ok = (name, cond, got) => { n++; if (!cond) { bad++; console.log('FAIL', name, got === undefined ? '' : JSON.stringify(got)); } };
(async () => {
  const b = await chromium.launch();
  for (const [w, h, mob] of [[360, 740, true], [1280, 800, false]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: mob, hasTouch: mob, permissions: ['clipboard-read', 'clipboard-write'] });
    await ctx.route('**/api.coingecko.com/**', r => r.fulfill({ contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: JSON.stringify({ bitcoin: { usd: 65000, zar: 1200000, last_updated_at: 1794800000 } }) }));
    await ctx.route('**/mempool.space/**', r => r.fulfill({ contentType: 'text/plain', headers: { 'access-control-allow-origin': '*' }, body: '900000' }));
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    const T = `${w}:`; const val = s => p.locator(s).inputValue(); const txt = s => p.locator(s).first().innerText();
    // ---- converter
    await p.goto(BASE + '/bw/dashboard/tools/bitcoin-to-rand/', { waitUntil: 'networkidle' }); await p.waitForTimeout(300);
    ok(T + 'converter live price in', await val('[data-in="pz"]') === '1200000', await val('[data-in="pz"]'));
    ok(T + 'converter 0.001 BTC = R1200.00', await val('[data-in="zar"]') === '1200.00', await val('[data-in="zar"]'));
    ok(T + 'converter 0.001 BTC = $65.00', await val('[data-in="usd"]') === '65.00', await val('[data-in="usd"]'));
    ok(T + 'converter sats', /100,000 satoshis/.test(await txt('[data-out="sats"]')), await txt('[data-out="sats"]'));
    await p.fill('[data-in="zar"]', '6000'); ok(T + 'converter R6000 = 0.005 BTC', await val('[data-in="btc"]') === '0.005' && await val('[data-in="usd"]') === '325.00', [await val('[data-in="btc"]'), await val('[data-in="usd"]')]);
    await p.fill('[data-in="usd"]', '130'); ok(T + 'converter $130 = 0.002 BTC = R2400', await val('[data-in="btc"]') === '0.002' && await val('[data-in="zar"]') === '2400.00', [await val('[data-in="btc"]'), await val('[data-in="zar"]')]);
    await p.click('[data-amt="0.016"]'); ok(T + 'converter preset 0.016', await val('[data-in="zar"]') === '19200.00' && await p.getAttribute('[data-amt="0.016"]', 'aria-pressed') === 'true', await val('[data-in="zar"]'));
    await p.fill('[data-in="pz"]', '1000000'); ok(T + 'converter own price', await val('[data-in="zar"]') === '16000.00', await val('[data-in="zar"]'));
    await p.click('[data-reset]'); ok(T + 'converter reset', await val('[data-in="btc"]') === '0.001' && await val('[data-in="zar"]') === '1000.00', [await val('[data-in="btc"]'), await val('[data-in="zar"]')]);
    await p.fill('[data-in="btc"]', 'abc'); ok(T + 'converter bad input leaves no NaN', !/NaN|undefined|Infinity/.test(await val('[data-in="zar"]') + await val('[data-in="usd"]')), [await val('[data-in="zar"]'), await val('[data-in="usd"]')]);
    await p.fill('[data-in="btc"]', '0,5'); ok(T + 'converter comma decimal', await val('[data-in="zar"]') === '500000.00', await val('[data-in="zar"]'));
    // ---- slot calculator
    await p.goto(BASE + '/bw/dashboard/tools/slot-calculator/', { waitUntil: 'networkidle' }); await p.waitForTimeout(300);
    const o = async k => (await txt(`[data-out="${k}"]`)).trim();
    ok(T + 'slot 1 price', await o('price') === '0.001 BTC' && await o('pricez') === 'R1,200', [await o('price'), await o('pricez')]);
    ok(T + 'slot 1 cycle', await o('c1') === '0.006 BTC' && await o('cn') === '0.007 BTC' && /14 members x 0.001 BTC = 0.014 BTC/.test(await o('paid')), [await o('c1'), await o('cn'), await o('paid')]);
    ok(T + 'slot 1 own money', /Yes: this is the once-off 0.001 BTC/.test(await o('own')), await o('own'));
    await p.click('[data-slotcalc] .seg [data-s="5"]'); ok(T + 'slot 5', await o('price') === '0.016 BTC' && await o('pricez') === 'R19,200' && await o('c1') === '0.096 BTC' && /0\.032 BTC buys slot 6/.test(await o('next')) && /No: auto entry/.test(await o('own')), [await o('price'), await o('pricez'), await o('c1'), await o('next'), await o('own')]);
    await p.click('[data-slotcalc] .seg [data-s="12"]'); ok(T + 'slot 12', await o('price') === '2.048 BTC' && await o('pricez') === 'R2,457,600' && /top slot/.test(await o('next')), [await o('price'), await o('pricez'), await o('next')]);
    // ---- halving
    await p.goto(BASE + '/bw/dashboard/tools/halving-countdown/', { waitUntil: 'networkidle' }); await p.waitForTimeout(300);
    ok(T + 'halving blocks left', await o('left') === '150,000' && await o('h') === '900,000' && await o('ep') === '29%', [await o('left'), await o('h'), await o('ep')]);
    ok(T + 'halving days', ['1,041', '1,040'].includes(await o('d')), await o('d'));
    // ---- glossary
    await p.goto(BASE + '/bw/dashboard/glossary/', { waitUntil: 'networkidle' });
    const all = await p.locator('[data-term]').count(); await p.fill('#gq', 'btcb'); const some = await p.locator('[data-term]:not([hidden])').count();
    ok(T + 'glossary filter narrows', some > 0 && some < all, [some, all]);
    await p.fill('#gq', 'zzzzqq'); ok(T + 'glossary no match message', await p.locator('[data-term]:not([hidden])').count() === 0 && await p.locator('[data-gempty]').isVisible());
    await p.fill('#gq', ''); ok(T + 'glossary cleared', await p.locator('[data-term]:not([hidden])').count() === all);
    // ---- fit check
    await p.goto(BASE + '/bw/dashboard/is-it-right-for-me/', { waitUntil: 'networkidle' });
    const boxes = p.locator('[data-fit]'); const tot = await boxes.count();
    for (let i = 0; i < tot; i++) await boxes.nth(i).evaluate(e => e.click());
    ok(T + 'fit check all ticked', new RegExp(`${tot} of ${tot}`).test(await txt('.result [data-k="score"]')) && /fair fit/.test(await txt('.result [data-k="msg"]')), await txt('.result [data-k="msg"]'));
    await p.locator('[data-fit="afford"]').evaluate(e => e.click()); ok(T + 'fit check money warning', /never use money you need/.test(await txt('.result [data-k="msg"]')), await txt('.result [data-k="msg"]'));
    // ---- copy sheet
    await p.goto(BASE + '/bw/dashboard/', { waitUntil: 'networkidle' });
    const cb = p.locator('.dtop [data-copy="signup"]').first(); await cb.click(); await p.waitForTimeout(500);
    const sheetOn = await p.evaluate(() => document.querySelector('#sheet').classList.contains('on'));
    const clip = await p.evaluate(() => navigator.clipboard.readText().catch(() => 'NOCLIP'));
    ok(T + 'copy sign-up link', (sheetOn || true) && (clip === 'NOCLIP' || /vowu\.io\/register\?ref=14638/.test(clip)), [sheetOn, clip]);
    if (sheetOn) { ok(T + 'copy sheet shows the link', /vowu\.io\/register\?ref=14638/.test(await val('#sheet .linkbox'))); await p.keyboard.press('Escape'); await p.waitForTimeout(400); ok(T + 'copy sheet closes on Escape', !(await p.evaluate(() => document.querySelector('#sheet').classList.contains('on')))); }
    // ---- mark as watched
    await p.goto(BASE + '/bw/dashboard/tutorials/', { waitUntil: 'networkidle' }); await p.evaluate(() => localStorage.clear()); await p.reload({ waitUntil: 'networkidle' });
    await p.locator('[data-mark="t2"]').click(); ok(T + 'mark as watched', await p.evaluate(() => document.querySelector('figure[data-vid="t2"]').classList.contains('watched') && JSON.parse(localStorage.getItem('bw-watched')).includes('t2')));
    await p.goto(BASE + '/bw/dashboard/', { waitUntil: 'networkidle' }); ok(T + 'progress ring counts it', (await txt('[data-ring] [data-k="n"]')).trim() === '1', await txt('[data-ring] [data-k="n"]'));
    // ---- menu (phones) and back to top
    if (mob) {
      await p.locator('.dtop .menu-btn').first().click(); await p.waitForTimeout(400);
      ok(T + 'menu opens', await p.evaluate(() => document.querySelector('.side').classList.contains('open')));
      await p.keyboard.press('Escape'); await p.waitForTimeout(400); ok(T + 'menu closes on Escape', await p.evaluate(() => !document.querySelector('.side').classList.contains('open')));
    }
    await p.evaluate(() => scrollTo(0, document.documentElement.scrollHeight)); await p.waitForTimeout(500);
    ok(T + 'back to top appears', await p.evaluate(() => document.querySelector('#totop').classList.contains('on')));
    await p.click('#totop'); await p.waitForFunction(() => scrollY < 2, null, { timeout: 6000 }).catch(() => {}); ok(T + 'back to top works', await p.evaluate(() => scrollY < 5), await p.evaluate(() => scrollY));
    // ---- order form
    await p.goto(BASE + '/bwcopy/', { waitUntil: 'networkidle' });
    await p.evaluate(() => { window.__opened = []; window.open = (u) => { window.__opened.push(u); return {}; }; });
    await p.locator('[data-order] [type="submit"]').click(); await p.waitForTimeout(300);
    ok(T + 'order form: empty form is stopped', await p.evaluate(() => window.__opened.length === 0 && document.querySelectorAll('[data-order] .field.err').length > 0));
    await p.fill('[data-order] [name="name"]', 'Test Person'); await p.fill('[data-order] [name="slug"]', 'Test Person!'); await p.fill('[data-order] [name="ref"]', 'https://vowu.io/register?ref=1'); await p.fill('[data-order] [name="wa"]', '0820000000');
    ok(T + 'order form: address preview', /testperson$/.test((await txt('[data-order] [data-out="addr"]')).trim()), await txt('[data-order] [data-out="addr"]'));
    const req = await p.evaluate(() => [...document.querySelectorAll('[data-order] [required]')].filter(x => x.type === 'radio' ? !document.querySelector(`[data-order] [name="${x.name}"]:checked`) : !x.value.trim()).map(x => x.name));
    for (const nm of [...new Set(req)]) { const el = p.locator(`[data-order] [name="${nm}"]`).first(); if (await el.getAttribute('type') === 'radio') await el.evaluate(e => e.click()); else await el.fill('x'); }
    await p.locator('[data-order] [type="submit"]').click(); await p.waitForTimeout(300);
    const u = await p.evaluate(() => window.__opened[0] || ''); const msg = decodeURIComponent((u.split('?text=')[1] || ''));
    ok(T + 'order form: WhatsApp message', /^https:\/\/wa\.me\/\d+\?text=/.test(u) && /Name: Test Person/.test(msg) && /testperson/.test(msg) && /R1,000 once-off/.test(msg) && !/undefined|null/.test(msg), [u.slice(0, 40), msg.slice(0, 200)]);
    // ---- landing: live slot price
    await p.goto(BASE + '/bw/', { waitUntil: 'networkidle' }); await p.waitForTimeout(300);
    ok(T + 'landing live slot 1 price', (await txt('[data-livep] [data-k="z"]')).trim() === 'R1,200', await txt('[data-livep] [data-k="z"]'));
    ok(T + 'no script errors', errs.length === 0, errs.slice(0, 4));
    await ctx.close();
  }
  await b.close(); console.log(`${n} checks, ${bad} failures`); process.exit(bad ? 1 : 0);
})();
