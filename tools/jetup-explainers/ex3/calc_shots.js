// Real screenshots of MTG's Exposure Calculator for explainer #3 (needs `python3 -m http.server 8765` in the repo root).
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 980, height: 552 }, deviceScaleFactor: 2 });
  await p.goto('http://127.0.0.1:8765/jetup/tools/exposure-calculator/', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.documentElement.classList.add('side-off')); await p.addStyleTag({ content: '.rv,.rv-row{opacity:1!important;transform:none!important}.thumb,.totop,.jump,#jump{display:none!important}' });
  // a calm frame: no price move, so the result rows read "No move"
  await p.evaluate(() => { const m = document.querySelector('#exp-move'); m.value = 0; m.dispatchEvent(new Event('input', { bubbles: true })); });
  await p.evaluate(() => { const f = document.querySelector('#exp-form'); const r = f.getBoundingClientRect(); window.scrollBy(0, r.top - 84); });
  await p.waitForTimeout(400);
  const boxes = {}, vals = {};
  const shot = async (name) => { await p.waitForTimeout(300); await p.screenshot({ path: `calc/${name}.png` }); };
  const box = async (sel) => { const r = await p.locator(sel).first().boundingBox(); return r && [r.x, r.y, r.width, r.height].map(v => Math.round(v)); };
  const val = async () => (await p.locator('#exp-ex').first().innerText()).replace(/\s+/g, ' ').trim();
  boxes.training = await box('button[data-preset="150,100,24"]'); boxes.sonic = await box('button[data-preset="50,0,24"]'); boxes.promo = await box('button[data-preset="100,100,24"]');
  boxes.form = await box('#exp-form'); boxes.out = await box('.out');
  const exRow = await p.evaluate(() => { let e = document.querySelector('#exp-ex'); while (e && !e.classList.contains('res') && e.parentElement && !e.parentElement.classList.contains('out')) e = e.parentElement; const r = e.getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(Math.round); });
  boxes.ex = exRow;
  await shot('s0'); vals.s0 = await val();
  await p.click('button[data-preset="50,0,24"]'); await p.evaluate(() => { const m = document.querySelector('#exp-move'); m.value = 0; m.dispatchEvent(new Event('input', { bubbles: true })); });
  await shot('s1'); vals.s1 = await val();
  await p.click('button[data-preset="150,100,24"]'); await p.evaluate(() => { const m = document.querySelector('#exp-move'); m.value = 0; m.dispatchEvent(new Event('input', { bubbles: true })); });
  await shot('s2'); vals.s2 = await val();
  fs.writeFileSync('calc/boxes.json', JSON.stringify({ boxes, vals, vw: 980, vh: 552 }));
  console.log(JSON.stringify({ boxes, vals })); await b.close();
})();
