const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  for (const n of process.argv.slice(2)) {
    await p.goto('file://' + path.join(__dirname, `thumb_p${n}.html`), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(__dirname, `thumb_p${n}.png`) });
    console.log('shot', n);
  } await b.close(); })();
