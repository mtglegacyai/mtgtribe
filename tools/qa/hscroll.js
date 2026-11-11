// Sideways-scroll audit for every page on the site, on phone widths, at normal and enlarged text.
// Finds: (1) the page itself scrolling sideways, (2) any box inside the page that scrolls sideways,
// (3) visible text cut off by the screen edge. Usage: node hscroll.js pages.txt out.json [widths] [scales]
const { chromium } = require('playwright');
const fs = require('fs');
const B = process.env.BASE || 'http://127.0.0.1:8765/';   // BASE=https://mtgtribe.com/ checks the live site
const pages = fs.readFileSync(process.argv[2], 'utf8').split('\n').filter(Boolean).map(p => p.replace(/index\.html$/, ''));
const OUT = process.argv[3];
const WIDTHS = (process.argv[4] || '320,360,375,390,412,430').split(',').map(Number);
const SCALES = (process.argv[5] || '1,1.3').split(',').map(Number);
(async () => {
  const b = await chromium.launch(); const res = [];
  for (const w of WIDTHS) for (const sc of SCALES) {
    const ctx = await b.newContext({ viewport: { width: w, height: 800 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
    await ctx.route(/coingecko|binance|googletagmanager|google-analytics/, r => r.abort());
    const p = await ctx.newPage();
    for (const path of pages) {
      try { await p.goto(B + path, { waitUntil: 'networkidle', timeout: 30000 }); } catch (e) { res.push({ w, sc, path, err: String(e).slice(0, 120) }); continue; }
      await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
      if (sc !== 1) {   // like Android "text size": every text gets bigger, the screen stays the same width
        await p.evaluate(sc => { const els = [...document.querySelectorAll('body, body *')]; const fs = els.map(e => parseFloat(getComputedStyle(e).fontSize));
          els.forEach((e, i) => { if (fs[i]) e.style.setProperty('font-size', (fs[i] * sc) + 'px', 'important'); }); }, sc);
        await p.waitForTimeout(400);
      }
      const r = await p.evaluate(sc => {
        document.querySelectorAll('.rv,[class*="reveal"]').forEach(e => e.classList.add('in', 'is-in', 'visible', 'shown'));
        // the real screen width: in phone mode innerWidth grows with a page that is too wide, which used to hide exactly that fault
        const W = document.documentElement.clientWidth, out = { page: document.documentElement.scrollWidth - W, scrollers: [], cut: [] };
        const name = e => { let s = e.tagName.toLowerCase(); if (e.id) s += '#' + e.id; if (e.classList.length) s += '.' + [...e.classList].slice(0, 3).join('.'); return s; };
        const path = e => { const a = []; for (let x = e; x && x !== document.body && a.length < 4; x = x.parentElement) a.unshift(name(x)); return a.join(' > '); };
        // not shown: hidden boxes, and text kept for screen readers only (clipped to nothing, the way Canton tables keep their column headers on phones)
        const shown = e => { for (let x = e; x; x = x.parentElement) { const cs = getComputedStyle(x); if (cs.display === 'none' || cs.visibility === 'hidden' || x.hasAttribute('inert') || x.getAttribute('aria-hidden') === 'true'
          || (cs.position === 'absolute' && /^rect\(0px,? 0px,? 0px,? 0px\)$/.test(cs.clip))) return false; } return true; };
        for (const e of document.querySelectorAll('body *')) {
          const cs = getComputedStyle(e);
          if (/(auto|scroll)/.test(cs.overflowX) && e.scrollWidth > e.clientWidth + 2 && e.clientWidth > 0 && shown(e))
            out.scrollers.push({ el: path(e), over: e.scrollWidth - e.clientWidth, text: (e.innerText || '').trim().slice(0, 60) });
        }
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
        while ((n = walker.nextNode())) {
          if (!n.textContent.trim()) continue; const e = n.parentElement; if (!e || !shown(e)) continue;
          const rg = document.createRange(); rg.selectNodeContents(n);
          for (const q of rg.getClientRects()) {
            if (q.width < 2) continue;
            if ((q.right > W + 1 && q.left < W) || (q.left < -1 && q.right > 0)) { out.cut.push({ el: path(e), text: n.textContent.trim().slice(0, 50), x: Math.round(q.left), r: Math.round(q.right) }); break; }
          }
        }
        return out;
      }, sc);
      res.push({ w, sc, path, ...r });
    }
    await ctx.close();
  }
  await b.close(); fs.writeFileSync(OUT, JSON.stringify(res, null, 1));
  const bad = res.filter(r => r.err || r.page > 1 || r.scrollers.length || r.cut.length);
  console.log(`${res.length} page views, ${bad.length} with a problem`);
})();
