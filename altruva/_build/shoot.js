// usage: node shoot.js "path1,path2" outdir width height [full=1]
const { chromium } = require('playwright');
const pages = process.argv[2].split(',');
const out = process.argv[3];
const w = +process.argv[4] || 1440, h = +process.argv[5] || 900;
const full = process.argv[6] !== '0';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  const F = '/tmp/assets/fonts/';
  const css = [['Montserrat',600,'Montserrat-600'],['Montserrat',500,'Montserrat-600'],['Montserrat',700,'Montserrat-700'],['Montserrat',800,'Montserrat-800'],['Orbitron',700,'Orbitron-800'],['Orbitron',800,'Orbitron-800']]
    .map(([f,wt,file])=>`@font-face{font-family:'${f}';font-weight:${wt};font-display:swap;src:url(https://fonts.gstatic.com/local/${file}.ttf)}`).join('\n');
  await ctx.route('https://fonts.googleapis.com/**', r => r.fulfill({ contentType: 'text/css', body: css }));
  await ctx.route('https://fonts.gstatic.com/local/**', r => r.fulfill({ path: F + r.request().url().split('/').pop(), contentType: 'font/ttf' }));
  for (const p of pages) {
    const pg = await ctx.newPage();
    const errs = [];
    pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    pg.on('pageerror', e => errs.push('PAGEERR ' + e.message));
    pg.on('requestfailed', r => { if (!r.url().includes('coingecko')) errs.push('REQFAIL ' + r.url()); });
    await pg.goto('http://localhost:8765/altruva/' + p, { waitUntil: 'networkidle' });
    await pg.waitForTimeout(600);
    if (full) { await pg.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); }); await pg.waitForTimeout(700); }
    const sw = await pg.evaluate(() => document.documentElement.scrollWidth);
    const name = (p.replace(/\//g, '_').replace(/_$/, '') || 'landing');
    await pg.screenshot({ path: `${out}/${name}-${w}.png`, fullPage: full });
    console.log(name, w, 'scrollWidth', sw, errs.length ? ('ERR ' + errs.join(' | ')) : 'ok');
    await pg.close();
  }
  await b.close();
})();
