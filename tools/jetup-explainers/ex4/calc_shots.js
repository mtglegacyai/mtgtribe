// The Profit Split Calculator, real page states for the demo scene: default, $10 profit, Myfxbook preset, typing 100.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 });
  await p.goto('http://127.0.0.1:8765/jetup/tools/profit-split-calculator/', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.documentElement.classList.add('side-off')); await p.addStyleTag({ content: '.rv,.rv-row{opacity:1!important;transform:none!important}.thumb,.totop,.jump,#jump{display:none!important}' });
  const form = p.locator('#ps-form'); await form.scrollIntoViewIfNeeded();
  await p.evaluate(() => { const f = document.querySelector('#ps-form'); const r = f.getBoundingClientRect(); window.scrollBy(0, r.top - 90); });
  await p.waitForTimeout(400);
  const boxes = {}; const shot = async (name) => { await p.waitForTimeout(250); await p.screenshot({ path: `calc/${name}.png` }); };
  const box = async (sel) => { const r = await p.locator(sel).first().boundingBox(); return r && [r.x, r.y, r.width, r.height].map(v => Math.round(v)); };
  boxes.ten = await box('button[data-preset="10,100"]'); boxes.myfx = await box('button[data-preset="50,30.1"]'); boxes.amt = await box('#ps-amt'); boxes.you = await box('#ps-you');
  await shot('s0');
  await p.click('button[data-preset="10,100"]'); await shot('s1');
  await p.click('button[data-preset="50,30.1"]'); await shot('s2');
  await p.fill('#ps-amt', ''); await shot('s3a');
  for (const [i, v] of [['b', '1'], ['c', '10'], ['d', '100']]) { await p.fill('#ps-amt', v); await p.dispatchEvent('#ps-amt', 'input'); await shot('s3' + i); }
  const vals = await p.evaluate(() => ['ps-gross', 'ps-you', 'ps-fee', 'ps-net'].map(i => document.getElementById(i).textContent));
  fs.writeFileSync('calc/boxes.json', JSON.stringify({ boxes, vals, vw: 1280, vh: 720 }));
  console.log(JSON.stringify({ boxes, vals })); await b.close();
})();
