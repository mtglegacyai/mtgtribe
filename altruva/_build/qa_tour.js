const { chromium } = require('playwright');
const B = process.env.BASE || 'http://localhost:8765/altruva/';
(async () => {
  const b = await chromium.launch(); let ok = true;
  const P = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) ok = false; };
  for (const [n, vp, mob] of [['desktop', { width: 1280, height: 720 }, false], ['phone', { width: 360, height: 640 }, true]]) {
    const ctx = await b.newContext({ viewport: vp, isMobile: mob, hasTouch: mob }); const p = await ctx.newPage();
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(B, { waitUntil: 'networkidle' });
    const r = await p.request.get(B + 'media/altruva-welcome-tour.mp4'); P(r.status() === 200, `${n}: video file 200 (${(await r.body()).length} bytes)`);
    const pr = await p.request.get(B + 'img/altruva-welcome-tour.webp'); P(pr.status() === 200, `${n}: poster 200`);
    const box = await p.evaluate(() => { const s = document.querySelector('#stage').getBoundingClientRect(); return [s.width, s.height]; });
    P(Math.abs(box[0] / box[1] - 16 / 9) < 0.03, `${n}: stage is 16:9 (${box.map(Math.round).join('x')})`);
    await p.click('#stage .vplay');
    await p.waitForTimeout(400);
    const v = await p.evaluate(() => { const v = document.querySelector('#stage video'); return v ? v.getAttribute('src') : null; });
    P(v && v.includes('altruva-welcome-tour.mp4'), `${n}: tapping play starts the welcome tour`);
    P(await p.isVisible('#stage .vclose'), `${n}: close X on the video`);
    await p.evaluate(() => document.querySelector('#stage video').dispatchEvent(new Event('ended')));
    await p.waitForTimeout(1200);
    P(await p.isVisible('#stage .vplay'), `${n}: back to the poster when it ends`);
    const toast = await p.evaluate(() => (document.querySelector('.toast') || {}).textContent || '');
    P(/Welcome tour: watched/.test(toast), `${n}: toast says "${toast.trim()}"`);
    await p.click('#stage .vplay'); await p.waitForTimeout(300); await p.click('#stage .vclose'); await p.waitForTimeout(300);
    P(await p.isVisible('#stage .vplay'), `${n}: X closes the video`);
    const ring = await p.evaluate(() => { try { return JSON.parse(localStorage.getItem('alt-watched') || '[]'); } catch (e) { return []; } });
    P(Array.isArray(ring), `${n}: watched list ${JSON.stringify(ring)}`);
    P(errs.length === 0, `${n}: no page errors ${errs.join(' | ')}`);
    await ctx.close();
  }
  await b.close(); console.log(ok ? 'ALL PASSED' : 'SOME FAILED');
})();
