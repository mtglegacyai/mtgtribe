// Click by click screenshots of mtgtribe.com for the Canton Weekly "income streams" scene (MTG, 24 Nov 2026).
// Usage: node tools/canton-weekly/menu_capture.js BASE_URL OUT_DIR
// BASE_URL is the site to capture: video.py serves this checkout on localhost, so the video always shows the menu as it is
// in the repo that week. Writes home.jpg, dash.jpg and menu.jpg (phone screen, 390 x 844 at 2x) and boxes.json: where to
// tap on each screen and where each income stream sits in the menu, so the video can highlight them one by one.
const {chromium} = require('playwright');
const fs = require('fs');
(async () => {
  const [base, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const ctx = await b.newContext({viewport: {width: 390, height: 844}, deviceScaleFactor: 2, isMobile: true, hasTouch: true, reducedMotion: 'reduce'});
  const p = await ctx.newPage();
  const box = async (loc) => { const r = await loc.boundingBox(); return r && {x: r.x, y: r.y, w: r.width, h: r.height}; };
  const calm = async () => { await p.addStyleTag({content: '*{animation-play-state:paused!important;transition:none!important;caret-color:transparent!important}#toast,.toast{display:none!important}'}); await p.waitForTimeout(600); };
  const boxes = {};
  // 1. The home page: tap Dashboard.
  await p.goto(base + '/', {waitUntil: 'load'}); await p.waitForTimeout(1500); await calm();
  boxes.dashboard = await box(p.locator('header .nav a[href="/dashboard/"]').first());
  await p.screenshot({path: out + '/home.jpg', type: 'jpeg', quality: 88});
  // 2. The dashboard: tap Menu.
  await p.goto(base + '/dashboard/', {waitUntil: 'load'}); await p.waitForTimeout(1500); await calm();
  boxes.menu = await box(p.locator('.md-menu').first());
  await p.screenshot({path: out + '/dash.jpg', type: 'jpeg', quality: 88});
  // 3. The menu is open: the Income streams, one by one.
  await p.locator('.md-menu').first().click(); await p.waitForTimeout(900);
  const label = p.locator('#mtg-menu .md-label', {hasText: 'Income streams'}).first();
  await label.evaluate(e => { const m = document.getElementById('mtg-menu'); m.scrollTop = Math.max(0, e.offsetTop - 120); });
  await p.waitForTimeout(400);
  boxes.label = await box(label);
  const items = await p.$$eval('#mtg-menu .md-label', ls => {
    const l = ls.find(x => /Income streams/i.test(x.textContent)); const out = []; let e = l && l.nextElementSibling;
    while (e && e.matches('.md-nav')) { const r = e.getBoundingClientRect(); out.push({name: e.querySelector('b').textContent.trim(), x: r.x, y: r.y, w: r.width, h: r.height}); e = e.nextElementSibling; }
    return out;
  });
  boxes.streams = items;
  await p.screenshot({path: out + '/menu.jpg', type: 'jpeg', quality: 88});
  fs.writeFileSync(out + '/boxes.json', JSON.stringify(boxes, null, 1));
  await b.close();
  if (items.length < 3) { console.error('menu_capture: found only ' + items.length + ' income streams'); process.exit(2); }
  console.log(JSON.stringify({streams: items.map(i => i.name)}));
})().catch(e => { console.error(e); process.exit(1); });
