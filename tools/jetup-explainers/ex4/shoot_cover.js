const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.join(__dirname, 'cover.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(__dirname, 'cover.png') }); await b.close(); })();
