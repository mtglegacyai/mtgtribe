// Shoots cover.html at 1920x1080 (and a 1280x720 copy is made with ffmpeg). Usage: node shoot.js <out.png>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'cover.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  await p.screenshot({ path: process.argv[2] });
  await b.close();
})();
