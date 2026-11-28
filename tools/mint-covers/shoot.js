const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
 for (const n of process.argv.slice(2)) {
  const og = n === 'og'; const p = await b.newPage({ viewport: og ? { width: 1200, height: 630 } : { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, n + '.html'), { waitUntil: 'networkidle' });
  for (const f of ['400 100px Anton', '800 40px Manrope', '40px "Noto Color Emoji"']) await p.evaluate(f => document.fonts.load(f), f);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150); await p.screenshot({ path: path.join(__dirname, n + '.png') }); await p.close(); }
 await b.close(); })();
