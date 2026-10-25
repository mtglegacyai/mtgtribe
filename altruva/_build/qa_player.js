// Player QA: never stuck. Close always visible, Back closes, end closes, inline close and end restore the poster.
const { chromium } = require('playwright');
const B = process.env.BASE || 'http://localhost:8765/altruva/';
let fails = 0; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };
(async () => {
  const b = await chromium.launch();
  for (const vp of [{ width: 360, height: 640 }, { width: 412, height: 780 }]) {
    const ctx = await b.newContext({ viewport: vp, isMobile: true, hasTouch: true });
    await ctx.route('https://fonts.googleapis.com/**', r => r.fulfill({ contentType: 'text/css', body: '' }));
    const pg = await ctx.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(B + 'dashboard/', { waitUntil: 'networkidle' });
    await pg.evaluate(() => window.scrollTo(0, 500)); await pg.waitForTimeout(200);
    const y0 = await pg.evaluate(() => scrollY);
    await pg.tap('.vtile[data-play="t1"]'); await pg.waitForTimeout(500);
    const bx = await pg.locator('#player .xbtn').boundingBox();
    ok(bx && bx.y >= 0 && bx.y + bx.height <= vp.height, `${vp.width}x${vp.height}: close button fully on screen (top ${bx && Math.round(bx.y)})`);
    const cb = await pg.locator('#player .prow [data-close]').boundingBox();
    ok(cb && cb.y + cb.height <= vp.height, `${vp.width}x${vp.height}: "Close video" button on screen`);
    await pg.tap('#player .xbtn'); await pg.waitForTimeout(500);
    ok(await pg.evaluate(() => !document.getElementById('player').classList.contains('on')), 'X closes the player');
    ok(Math.abs((await pg.evaluate(() => scrollY)) - y0) < 3, 'page is back where it was');
    ok(pg.url().endsWith('/dashboard/'), 'still on the same page');
    // Back button closes the player instead of leaving the page
    await pg.tap('.vtile[data-play="e1"]'); await pg.waitForTimeout(500);
    await pg.goBack(); await pg.waitForTimeout(600);
    ok(await pg.evaluate(() => !document.getElementById('player').classList.contains('on')), 'phone Back closes the player');
    ok(pg.url().endsWith('/dashboard/'), 'Back did not leave the page');
    // end of video closes the player and marks it watched
    await pg.tap('.vtile[data-play="e2"]'); await pg.waitForTimeout(500);
    await pg.evaluate(() => document.querySelector('#player video').dispatchEvent(new Event('ended'))); await pg.waitForTimeout(1500);
    ok(await pg.evaluate(() => !document.getElementById('player').classList.contains('on')), 'finished video closes itself');
    ok(await pg.evaluate(() => document.querySelector('.vtile[data-vid="e2"]').classList.contains('watched')), 'finished video is ticked');
    ok(await pg.evaluate(() => getComputedStyle(document.body).overflow !== 'hidden'), 'page can scroll again');
    // backdrop tap closes
    await pg.tap('.vtile[data-play="e3"]'); await pg.waitForTimeout(500);
    await pg.mouse.click(5, 5); await pg.waitForTimeout(500);
    ok(await pg.evaluate(() => !document.getElementById('player').classList.contains('on')), 'tap outside closes the player');
    // inline player
    await pg.goto(B + 'dashboard/how-it-works/', { waitUntil: 'networkidle' });
    await pg.tap('.vplay'); await pg.waitForTimeout(400);
    ok(!!(await pg.$('figure.vid .vbox video')) && !!(await pg.$('figure.vid .vbox .vclose')), 'inline video shows a close button');
    await pg.tap('figure.vid .vbox .vclose'); await pg.waitForTimeout(300);
    ok(!(await pg.$('figure.vid .vbox video')) && !!(await pg.$('figure.vid .vbox .vplay')), 'inline close returns to the poster');
    await pg.tap('.vplay'); await pg.waitForTimeout(300);
    await pg.evaluate(() => document.querySelector('figure.vid .vbox video').dispatchEvent(new Event('ended'))); await pg.waitForTimeout(1200);
    ok(!(await pg.$('figure.vid .vbox video')) && !!(await pg.$('figure.vid .vbox .vplay')), 'inline video returns to the poster when it ends');
    // playlist
    await pg.goto(B + 'dashboard/tutorials/', { waitUntil: 'networkidle' });
    await pg.tap('[data-pick="t2"]'); await pg.waitForTimeout(500);
    await pg.evaluate(() => document.querySelector('.now video').dispatchEvent(new Event('ended'))); await pg.waitForTimeout(1200);
    ok(!(await pg.$('.now video')) && !!(await pg.$('.now .vplay')), 'playlist video returns to the poster when it ends');
    ok(errs.length === 0, 'no page errors ' + errs.join('|'));
    await ctx.close();
  }
  console.log(fails ? fails + ' FAILED' : 'ALL PASSED');
  await b.close();
})();
