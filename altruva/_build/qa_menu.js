// Menu show/hide: desktop gold arrow, phone menu button, phone gold arrow, tap beside the menu
const { chromium } = require('playwright');
const B = process.env.BASE || 'http://localhost:8765/altruva/';
let bad = 0; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) bad++; };
(async () => {
  const b = await chromium.launch();
  const d = await b.newPage({ viewport: { width: 1280, height: 720 } }); const errs = []; d.on('pageerror', e => errs.push(e.message));
  await d.goto(B + 'dashboard/', { waitUntil: 'networkidle' });
  ok(await d.isVisible('#side-toggle'), 'desktop: gold arrow visible');
  await d.click('#side-toggle'); await d.waitForTimeout(500);
  ok(await d.evaluate(() => document.documentElement.classList.contains('side-off')), 'desktop: arrow hides the menu');
  ok(await d.getAttribute('#side-toggle', 'aria-label') === 'Show the menu', 'desktop: label says Show the menu');
  await d.reload({ waitUntil: 'networkidle' });
  ok(await d.evaluate(() => document.documentElement.classList.contains('side-off')), 'desktop: hidden menu remembered after reload');
  await d.click('#side-toggle'); await d.waitForTimeout(500);
  ok(!(await d.evaluate(() => document.documentElement.classList.contains('side-off'))), 'desktop: arrow shows the menu again');
  for (const [w, h, name] of [[390, 780, 'phone'], [820, 1180, 'tablet']]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, isMobile: true, hasTouch: true }); p.on('pageerror', e => errs.push(e.message));
    await p.goto(B + 'dashboard/', { waitUntil: 'networkidle' });
    const open = () => p.evaluate(() => document.querySelector('#side').classList.contains('open'));
    const tog = () => p.evaluate(() => { const r = document.querySelector('#side-toggle').getBoundingClientRect(); return [r.left, r.width]; });
    ok(!(await open()), `${name}: menu starts hidden`);
    const [l0, w0] = await tog(); ok(l0 === 0 && w0 >= 22, `${name}: gold arrow on the left edge, ${w0}px wide`);
    await p.tap('#menu-btn'); await p.waitForTimeout(600); ok(await open(), `${name}: Menu button opens it`);
    const sw = await p.evaluate(() => document.querySelector('#side').getBoundingClientRect().width);
    const [l1] = await tog(); ok(Math.abs(l1 - (sw - 17)) < 2, `${name}: gold arrow sits on the menu's edge (${l1} vs ${sw - 17})`);
    ok(await p.getAttribute('#side-toggle', 'aria-label') === 'Hide the menu' && await p.getAttribute('#side-toggle', 'aria-expanded') === 'true', `${name}: arrow labelled Hide the menu`);
    await p.tap('#side-toggle'); await p.waitForTimeout(600); ok(!(await open()), `${name}: gold arrow hides it`);
    await p.tap('#side-toggle'); await p.waitForTimeout(600); ok(await open(), `${name}: gold arrow opens it`);
    await p.mouse.click(w - 20, h / 2 + 150); await p.waitForTimeout(600); ok(!(await open()), `${name}: tap beside the menu hides it`);
    ok(await p.getAttribute('#side-toggle', 'aria-label') === 'Show the menu', `${name}: arrow labelled Show the menu`);
  }
  ok(errs.length === 0, 'no page errors ' + errs.join(' | '));
  await b.close();
  console.log(bad ? bad + ' FAILED' : 'ALL PASSED');
})();
