// Renders cbp-webinar-flyer.html to a square PNG (2160x2160) and a share JPG (1080x1080).
// Usage: node render.js <out-basename>   (run with the playwright that is installed globally)
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || 'cbp-webinar-flyer';
  const browser = await chromium.launch();
  for (const [scale, ext] of [[2, 'png'], [1, 'jpg']]) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: scale });
    await page.goto('file://' + path.join(__dirname, 'cbp-webinar-flyer.html'));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(800);
    const file = path.join(__dirname, `${out}${scale === 2 ? '@2x' : ''}.${ext}`);
    await page.screenshot({ path: file, type: ext === 'jpg' ? 'jpeg' : 'png', quality: ext === 'jpg' ? 92 : undefined });
    console.log('wrote', file);
    await page.close();
  }
  await browser.close();
})();
