// Render the flyer to PNG and report layout checks (fonts loaded, nothing overflowing, exact texts).
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname, scale = Number(process.argv[2] || 2), out = process.argv[3] || 'flyer-preview.png';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: scale });
  await p.goto('file://' + path.join(dir, 'flyer.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate(() => {
    const fonts = ['400 40px Anton', '800 20px Manrope', '700 20px "JetBrains Mono"', '20px "Noto Color Emoji"'].map(f => [f, document.fonts.check(f)]);
    const f = document.getElementById('flyer').getBoundingClientRect();
    const bad = [];
    document.querySelectorAll('#flyer .z *').forEach(e => {
      const r = e.getBoundingClientRect(); if (!r.width) return;
      if (r.right > f.right - 40 || r.left < f.left + 40 || r.bottom > f.bottom - 34) bad.push([e.tagName + '.' + e.className.baseVal === undefined ? e.className : '', Math.round(r.left), Math.round(r.right), Math.round(r.bottom)]);
      if (e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflow !== 'visible') bad.push(['clip', e.className, e.scrollWidth, e.clientWidth]);
    });
    const last = document.querySelector('.disc').getBoundingClientRect();
    return { fonts, bad: bad.slice(0, 12), discBottom: Math.round(last.bottom), h1: [...document.querySelectorAll('h1 span')].map(s => Math.round(s.getBoundingClientRect().width)), text: document.querySelector('.z').innerText };
  });
  console.log(JSON.stringify({ fonts: r.fonts, bad: r.bad, discBottom: r.discBottom, h1: r.h1 }));
  console.log(r.text);
  await p.screenshot({ path: path.join(dir, out) });
  await b.close();
})();
