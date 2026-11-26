// Things lying on top of each other (MTG, 22 Nov 2026: "the top right button that takes the visitor to the dashboard is
// overlapping the website title ... look for any other areas ... that might have some objects overlapping each other").
// For every page, at phone widths and with Android's larger text, it finds text, icons, pictures and buttons whose boxes
// overlap when they should not. Designed overlays (a play button on its cover, a badge inside its card) are not overlaps:
// one box contains the other in the page's structure, or the element is marked data-overlay.
// Usage: node tools/qa/overlap.js pages.txt [widths] [text scales]      (BASE=http://127.0.0.1:8765/ by default)
const { chromium } = require('playwright');
const fs = require('fs');
const B = process.env.BASE || 'http://127.0.0.1:8765/';
const pages = fs.readFileSync(process.argv[2], 'utf8').split('\n').map(s => s.trim().replace(/index\.html$/, '')).filter(Boolean);
const WIDTHS = (process.argv[3] || '320,360,375,384,390,412,430,768').split(',').map(Number);
const SCALES = (process.argv[4] || '1,1.15,1.3').split(',').map(Number);
(async () => {
  const b = await chromium.launch();
  let views = 0, bad = 0;
  const seen = new Set();
  for (const w of WIDTHS) for (const sc of SCALES) {
    const ctx = await b.newContext({ viewport: { width: w, height: 800 }, isMobile: w < 1000, hasTouch: w < 1000, deviceScaleFactor: 1 });
    const p = await ctx.newPage();
    for (const path of pages) {
      try { await p.goto(B + path, { waitUntil: 'networkidle', timeout: 30000 }); } catch (e) { console.log('ERR', path, String(e).slice(0, 80)); continue; }
      await p.evaluate(() => document.fonts && document.fonts.ready);
      if (sc !== 1) await p.evaluate(sc => { const els = [...document.querySelectorAll('body, body *')]; const f = els.map(e => parseFloat(getComputedStyle(e).fontSize));
        els.forEach((e, i) => { if (f[i]) e.style.setProperty('font-size', (f[i] * sc) + 'px', 'important'); }); }, sc);
      await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelectorAll('.rv,.pre').forEach(e => e.classList.remove('pre')); });
      await p.waitForTimeout(250);
      const found = await p.evaluate(() => {
        const skip = el => (el.closest('details:not([open])') && !el.closest('summary')) || el.closest('defs,symbol,.pl-scr,.sheet,.toast,.ud,.md-toggle,.md-scrim,.sr,[hidden],[aria-hidden="true"]:not(svg),.skip,[data-overlay],.qbar,.tbar');
        const shown = el => { for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false; } return true; };
        const off = r => r.width < 1 || r.height < 1 || r.right < 0 || r.left > innerWidth;
        const boxes = [];
        const side = document.querySelector('.md-side');
        const sideOpen = side && side.classList.contains('open');
        for (const el of document.querySelectorAll('body *')) {
          if (skip(el)) continue;
          if (side && !sideOpen && innerWidth <= 1060 && side.contains(el)) continue;       // the closed drawer is off screen
          let rs = null;
          const cs = getComputedStyle(el);
          if (el.matches('img,svg.ic,input,select,textarea') || cs.textOverflow === 'ellipsis') rs = [el.getBoundingClientRect()];     // a shortened label: its box
          else {
            const tn = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim());
            if (!tn.length) continue;
            const rg = document.createRange(); rg.setStartBefore(tn[0]); rg.setEndAfter(tn[tn.length - 1]);
            rs = [...rg.getClientRects()].filter(q => q.width > 1 && q.height > 1);                    // one box per line of text
          }
          rs = rs.filter(q => !off(q));
          if (!rs.length || !shown(el)) continue;
          boxes.push({ el, rs: rs.map(q => ({ l: q.left, t: q.top + scrollY, r: q.right, b: q.bottom + scrollY })) });
        }
        const name = el => el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '') + (el.textContent.trim() ? ' "' + el.textContent.trim().slice(0, 24) + '"' : '');
        const out = [];
        for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
          const A = boxes[i], C = boxes[j];
          if (A.el.contains(C.el) || C.el.contains(A.el)) continue;
          const under = el => !!el.closest('.md-bot,[data-scroll-under]');          // a sticky panel the list scrolls under, by design
          if (under(A.el) !== under(C.el) && A.el.closest('.md-side,aside') && C.el.closest('.md-side,aside')) continue;
          let hit = null;
          for (const a of A.rs) for (const q of C.rs) {
            const x = Math.min(a.r, q.r) - Math.max(a.l, q.l), y = Math.min(a.b, q.b) - Math.max(a.t, q.t);
            if (x <= 1 || y <= 1) continue;
            const area = x * y, small = Math.min((a.r - a.l) * (a.b - a.t), (q.r - q.l) * (q.b - q.t));
            if (area >= 12 && area >= small * 0.12) { hit = Math.max(a.t, q.t); break; }
          }
          if (hit === null) continue;
          out.push(name(A.el) + '  ON  ' + name(C.el) + '  at y ' + Math.round(hit));
          if (out.length > 6) return out;
        }
        return out;
      });
      views++;
      if (found.length) {
        bad++;
        for (const f of found) { const k = path + ' ' + f.replace(/at y \d+/, ''); if (seen.has(k)) continue; seen.add(k); console.log(`${w}px x${sc} /${path}: ${f}`); }
      }
    }
    await ctx.close();
  }
  await b.close();
  console.log(`${views} page views, ${bad} with an overlap`);
})();
