// Phone screenshots for the social preview thumbnails: node og/thumbs.js [key ...]
// 360x648 CSS phone at 2x (720x1296), the chosen section placed just under the sticky header.
const { chromium } = require('playwright');
const fs = require('fs');
const B = process.env.BASE || 'http://localhost:8765/altruva/';
const PLAN = JSON.parse(fs.readFileSync(__dirname + '/shots.json', 'utf8'));
const only = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({ env: { ...process.env, LANG: 'en_ZA.UTF-8', LC_ALL: 'en_ZA.UTF-8' } });
  const ctx = await b.newContext({ viewport: { width: 360, height: 648 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, locale: 'en-ZA', timezoneId: 'Africa/Johannesburg' });
  const F = '/tmp/assets/fonts/';
  const css = [['Montserrat', 500, 'Montserrat-600'], ['Montserrat', 600, 'Montserrat-600'], ['Montserrat', 700, 'Montserrat-700'], ['Montserrat', 800, 'Montserrat-800'], ['Orbitron', 700, 'Orbitron-800'], ['Orbitron', 800, 'Orbitron-800']]
    .map(([f, w, file]) => `@font-face{font-family:'${f}';font-weight:${w};src:url(https://fonts.gstatic.com/local/${file}.ttf)}`).join('\n');
  await ctx.route('https://fonts.googleapis.com/**', r => r.fulfill({ contentType: 'text/css', body: css }));
  await ctx.route('https://fonts.gstatic.com/local/**', r => r.fulfill({ path: F + r.request().url().split('/').pop(), contentType: 'font/ttf' }));
  await ctx.route('https://api.coingecko.com/**', r => r.fulfill({ contentType: 'application/json', body: JSON.stringify({ tether: { zar: 16.57, last_updated_at: Math.floor(Date.now() / 1000) - 90 } }) }));
  const pg = await ctx.newPage();
  for (const [key, [path, sel, setup]] of Object.entries(PLAN)) {
    if (only.length && !only.includes(key)) continue;
    await pg.goto(B + path, { waitUntil: 'networkidle' });
    await pg.evaluate((setup) => {
      try { localStorage.clear(); } catch (e) {}
      if (setup === 'watched') localStorage.setItem('alt-watched', JSON.stringify(['t1', 't2', 't3', 'e1', 'e2', 'e3', 'k1']));
      if (setup === 'clock') { const d = new Date(Date.now() - (12 * 3600 + 22 * 60 + 17) * 1000), z = (x) => (x < 10 ? '0' : '') + x;
        localStorage.setItem('alt-join', d.getFullYear() + '-' + z(d.getMonth() + 1) + '-' + z(d.getDate()) + 'T' + z(d.getHours()) + ':' + z(d.getMinutes()) + ':' + z(d.getSeconds())); }
    }, setup);
    if (setup === 'watched' || setup === 'clock') { await pg.reload({ waitUntil: 'networkidle' }); }
    await pg.addStyleTag({ content: '.side-toggle,.totop,.toast,.progress{display:none!important}html{scroll-behavior:auto!important}' });
    if (setup === 'starter') await pg.evaluate(() => document.querySelector('[data-amt="28"]').click());
    await pg.waitForTimeout(700);
    await pg.evaluate((s) => { if (s === 'TOP') { scrollTo(0, 0); return; } const e = document.querySelector(s); const top = e.getBoundingClientRect().top + scrollY; scrollTo(0, Math.max(0, top - 84)); }, sel);
    await pg.waitForTimeout(500);
    await pg.screenshot({ path: `${__dirname}/shots/${key}.png` });
    console.log('shot', key);
  }
  await b.close();
})();
