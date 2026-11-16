// Real screenshots of MTG's Exposure Calculator (mtgtribe.com/jetup/tools/exposure-calculator/) for explainer #10.
// Needs the repo served on port 8770:  npx -y http-server@14.1.1 /home/user/mtgtribe -p 8770 -s -c-1
// Usage: node calc_shots.js   -> stage/calc/*.jpg (1280x800 page at device scale 2, so 2560x1600), stage/calc/boxes.json and boxes.js
// The page has no intro overlay, cookie bar, ticker or personal data. The guide's side menu is folded away (the page's own
// "side-off" state), and the floating bits (back-to-top, side toggle, toast) are hidden, so the calculator fills the screen.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const OUT = path.join(__dirname, 'stage', 'calc'), VW = 1280, VH = 800, DSF = 2;
const URL = 'http://127.0.0.1:8770/jetup/tools/exposure-calculator/';
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: VW, height: VH }, deviceScaleFactor: DSF });
  await p.goto(URL, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => document.documentElement.classList.add('side-off'));
  await p.addStyleTag({ content: '.rv,.rv-row{opacity:1!important;transform:none!important}.thumb,.totop,.jump,#jump,.side-tog,#toast{display:none!important}' +
    '*{caret-color:transparent!important;transition:none!important;animation:none!important}' });
  const move = v => p.evaluate(v => { const m = document.querySelector('#exp-move'); m.value = v; m.dispatchEvent(new Event('input', { bubbles: true })); }, v);
  const blur = () => p.evaluate(() => document.activeElement && document.activeElement.blur());
  const scrollTo = sel => p.evaluate(([sel]) => { const r = document.querySelector(sel).getBoundingClientRect(); window.scrollBy(0, r.top - 84); }, [sel]);
  const pressed = on => p.evaluate(on => document.querySelectorAll('[data-preset]').forEach(x => x.setAttribute('aria-pressed', String(on && x.dataset.preset === '150,100,24'))), on);
  const vals = async () => p.evaluate(() => Object.fromEntries(['exp-own', 'exp-bonus', 'exp-mult'].map(id => [id, document.getElementById(id).value])
    .concat(['exp-bal', 'exp-ex', 'exp-pl', 'exp-ofown', 'exp-eqown', 'exp-eqbal', 'exp-move-out', 'exp-meter-t'].map(id => [id, document.getElementById(id).innerText.trim()]))));
  // every tap and highlight target, in page px of the 1280x800 viewport at the moment of the shot
  const SEL = { training: 'button[data-preset="150,100,24"]', presets: '#exp-form .seg', own: '#exp-own', ownInp: '#exp-own', bonus: '#exp-bonus', mult: '#exp-mult',
    slider: '#exp-move', moveOut: '#exp-move-out', bal: '#exp-bal', ex: '#exp-ex', pl: '#exp-pl', ofown: '#exp-ofown', eqown: '#exp-eqown', eqbal: '#exp-eqbal',
    meter: '.meter', note: '.call.info', form: '#exp-form', out: '.out', h1: 'h1' };
  const boxesNow = () => p.evaluate(SEL => {
    const R = e => { const r = e.getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(v => Math.round(v)); };
    const o = {};
    for (const [k, s] of Object.entries(SEL)) {
      let e = document.querySelector(s); if (!e) continue;
      if (['own', 'bonus', 'mult'].includes(k)) e = e.closest('.field');                 // the whole field: label, small line, box
      if (['bal', 'ex', 'pl', 'ofown', 'eqown', 'eqbal'].includes(k)) e = e.closest('.res'); // the whole result card
      o[k] = R(e);
    }
    o.ownBox = R(document.querySelector('#exp-own').closest('.inp')); o.bonusBox = R(document.querySelector('#exp-bonus').closest('.inp'));
    o.multBox = R(document.querySelector('#exp-mult').closest('.inp'));
    // words inside the loss limit note, for the highlight boxes: "TAG Markets' built-in loss limit:", "10%", "5% with a community token"
    const note = document.querySelector('.call.info');
    const words = (txt, nth = 0) => {
      const w = document.createTreeWalker(note, NodeFilter.SHOW_TEXT); let n, seen = 0, acc = [];
      while ((n = w.nextNode())) acc.push(n);
      const full = acc.map(x => x.data).join(''); let i = -1;
      for (let k = 0; k <= nth; k++) i = full.indexOf(txt, i + 1);
      if (i < 0) return null;
      const rg = document.createRange(); let pos = 0;
      for (const x of acc) { const L = x.data.length;
        if (i >= pos && i < pos + L) rg.setStart(x, i - pos);
        if (i + txt.length > pos && i + txt.length <= pos + L) { rg.setEnd(x, i + txt.length - pos); break; }
        pos += L; }
      const rs = [...rg.getClientRects()]; const x0 = Math.min(...rs.map(r => r.left)), y0 = Math.min(...rs.map(r => r.top));
      return [x0, y0, Math.max(...rs.map(r => r.right)) - x0, Math.max(...rs.map(r => r.bottom)) - y0].map(Math.round);
    };
    o.nLimit = words("TAG Markets' built-in loss limit:"); o.n10 = words('10% of the starting balance'); o.n5 = words('5% with a community token');
    const th = document.querySelector('#exp-move'), r = th.getBoundingClientRect(), v = +th.value;   // the slider's thumb centre
    o.thumb = [Math.round(r.x + 8 + (r.width - 16) * (v + 10) / 20), Math.round(r.y + r.height / 2)];
    return o;
  }, SEL);
  const shots = {}, vv = {};
  const shot = async name => { await p.waitForTimeout(250); await p.screenshot({ path: path.join(OUT, name + '.jpg'), type: 'jpeg', quality: 90 }); shots[name] = await boxesNow(); vv[name] = await vals(); };

  // 1. the page as it opens (top), the calculator not moved yet; no example lit yet (it is tapped in Step 1)
  await move(0); await pressed(false); await blur(); await shot('top');
  // 2. the calculator in view, before the tap: no example lit, then after tapping "Training: $150 + $100" (150, 100, 24)
  await scrollTo('#exp-form'); await shot('pre');
  await p.click(SEL.training); await move(0); await blur(); await shot('calc');
  // 3. each field focused, as when you type your own
  for (const k of ['own', 'bonus', 'mult']) { await p.focus('#exp-' + (k === 'mult' ? 'mult' : k)); await shot('f_' + k); }
  await blur();
  // 4. the price move dragged, the page scrolled 150 px further so the slider sits mid-screen with the profit or loss row
  //    still in view: no move, then 0 to +1% and to -1% in 0.2 steps (frames for the drag), the page's own numbers in each
  await p.evaluate(() => window.scrollBy(0, 150)); await move(0); await shot('m00');
  for (let i = -5; i <= 5; i++) { if (!i) continue; const v = i / 5; await move(v); await shot('m' + (v > 0 ? 'p' : 'n') + String(Math.abs(i * 2)).padStart(2, '0')); }
  await move(0);
  // 5. scrolled down: the last two results and the page's loss limit note, the calculator at no move
  await p.evaluate(() => { const r = document.querySelector('#exp-eqown').closest('.res').getBoundingClientRect(); window.scrollBy(0, r.top - 148); });   // the note fully in view, the header clear of the rows
  await shot('lines');
  // 6. scrolled on, so the loss limit note sits mid-screen
  await p.evaluate(() => window.scrollBy(0, 300)); await shot('note');
  const data = JSON.stringify({ vw: VW, vh: VH, dsf: DSF, shots, vals: vv }, null, 0);
  fs.writeFileSync(path.join(OUT, 'boxes.json'), data); fs.writeFileSync(path.join(OUT, 'boxes.js'), 'window.BOXES = ' + data + ';\n');   // the stage reads boxes.js
  console.log(JSON.stringify(vv, null, 1));
  await b.close();
})();
