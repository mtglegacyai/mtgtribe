const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const n = process.argv[2];
 const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
 await p.goto('file://' + path.join(__dirname, n + '.html'), { waitUntil: 'networkidle' });
 for (const f of ['400 100px Anton', '800 40px Manrope', '40px "Noto Color Emoji"']) await p.evaluate(f => document.fonts.load(f), f);
 await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150); await p.screenshot({ path: path.join(__dirname, n + '.png') }); await b.close(); })();
