/* ALTRUVA guide by MTG | site behaviour. No tracking, no cookies. Stores only: watched videos, menu state. */
(function () {
  'use strict';
  var d = document, html = d.documentElement, ALT = window.ALT || {}, ALTV = window.ALTV || {};
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, r) { return (r || d).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); }
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function on(el, ev, fn, o) { if (el) el.addEventListener(ev, fn, o || false); }

  /* ------------------------------------------------------------ toast */
  var toastT;
  function toast(msg) {
    var t = $('#toast'); if (!t) return;
    t.textContent = msg; t.classList.add('on');
    clearTimeout(toastT); toastT = setTimeout(function () { t.classList.remove('on'); }, 2600);
  }

  /* ------------------------------------------------------------ sheets (copy sheet, video player) */
  /* A sheet never traps anyone: Close is always on screen, tapping outside, Escape and the phone's Back button
     all close it, and a finished video closes itself and returns the visitor to exactly where they were. */
  var lastFocus = null, savedY = 0, sheetHist = false;
  function exitFs(v) {
    try {
      if (d.fullscreenElement && d.exitFullscreen) d.exitFullscreen();
      else if (d.webkitFullscreenElement && d.webkitExitFullscreen) d.webkitExitFullscreen();
      if (v && v.webkitDisplayingFullscreen && v.webkitExitFullscreen) v.webkitExitFullscreen();
    } catch (e) {}
  }
  function openSheet(el) {
    if (!el) return;
    if (!$('.sheet.on')) { lastFocus = d.activeElement; savedY = window.scrollY || 0; }
    el.hidden = false; void el.offsetWidth; el.classList.add('on');
    d.body.style.overflow = 'hidden';
    if (!sheetHist) { try { history.pushState({ altSheet: 1 }, ''); sheetHist = true; } catch (e) {} }
    var f = $('[data-close]', el); if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 30);
  }
  function closeSheet(el, fromPop) {
    if (!el || el.hidden || !el.classList.contains('on')) return;
    el.classList.remove('on'); d.body.style.overflow = '';
    var v = $('video', el); if (v) { exitFs(v); v.pause(); }
    setTimeout(function () { el.hidden = true; if (v) { v.removeAttribute('src'); v.load(); } }, 260);
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus({ preventScroll: true }); } catch (e) {} }
    var y = savedY;
    if (Math.abs((window.scrollY || 0) - y) > 2) window.scrollTo(0, y);
    setTimeout(function () { if (Math.abs((window.scrollY || 0) - y) > 2) window.scrollTo(0, y); }, 400);
    if (sheetHist && !fromPop) { sheetHist = false; try { history.back(); } catch (e) {} }
  }
  on(window, 'popstate', function () {
    if (!sheetHist) return;
    sheetHist = false;
    $$('.sheet.on').forEach(function (s) { closeSheet(s, true); });
  });
  $$('.sheet').forEach(function (s) {
    on(s, 'click', function (e) { if (e.target === s || e.target.closest('[data-close]')) closeSheet(s); });
  });
  on(d, 'keydown', function (e) {
    if (e.key !== 'Escape') return;
    $$('.sheet.on').forEach(closeSheet);
    closeDrawer();
  });

  /* ------------------------------------------------------------ copy buttons */
  var COPY = {
    signup: {
      text: function () { return ALT.ref; }, title: 'Sign-up link copied', fail: 'Copy the sign-up link',
      sub: "This is MTG's ALTRUVA referral link. Introduced by someone else? Use their link instead, so they stay your sponsor.",
      steps: ['Open SafePal (or your Web3 wallet) and tap <b>Explore</b>.', 'Paste the link in the top bar and choose <b>BNB Chain</b>.', 'Pick your package, then approve and sign. Tutorial 3 shows every tap.'],
      note: 'Learn first, and only use money you can afford to lose.',
      acts: function () { return '<button type="button" class="btn btn-blue btn-sm" data-play="t3"><span class="lbl">Watch Tutorial 3</span></button><a class="btn btn-ghost btn-sm" href="' + ALT.join + '"><span class="lbl">Join step by step</span></a>'; }
    },
    login: {
      text: function () { return ALT.login; }, title: 'Login link copied', fail: 'Copy the login link',
      sub: 'Members log in by connecting their Web3 wallet. There is no username or password.',
      steps: ['Open your wallet and tap <b>Explore</b> (SafePal) or its browser.', 'Paste the link and choose <b>BNB Chain</b>.', 'Connect your wallet.'],
      note: 'On a computer with a browser wallet like MetaMask? You can open it here instead.',
      acts: function () { return '<a class="btn btn-ghost btn-sm" href="' + ALT.login + '" target="_blank" rel="noopener"><span class="lbl">Open here</span></a>'; }
    },
    share: { text: function () { var b = $('.sharebox'); return b ? b.value : ''; }, quiet: 'Message copied ✓' }
  };
  function legacyCopy(text) {
    var ta = d.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0'; ta.style.top = '0';
    d.body.appendChild(ta); ta.select(); ta.setSelectionRange(0, text.length);
    var ok = false; try { ok = d.execCommand('copy'); } catch (e) {}
    d.body.removeChild(ta); return ok;
  }
  function showCopySheet(c, text, ok) {
    var s = $('#sheet'); if (!s) return;
    $('[data-k="title"]', s).textContent = ok ? c.title : c.fail;
    $('#sheet-h .ic', s).style.display = ok ? '' : 'none';
    $('[data-k="sub"]', s).textContent = ok ? c.sub : 'Your browser blocked copying. Press and hold the link below, then tap Copy.';
    var box = $('.linkbox', s); box.value = text;
    $('[data-k="steps"]', s).innerHTML = c.steps.map(function (x) { return '<li>' + x + '</li>'; }).join('');
    $('[data-k="note"]', s).textContent = c.note || '';
    $('[data-k="acts"]', s).innerHTML = c.acts ? c.acts() : '';
    openSheet(s);
    if (!ok) setTimeout(function () { box.focus(); box.select(); }, 60);
  }
  function flag(b) {
    b.classList.add('is-copied');
    clearTimeout(b._t); b._t = setTimeout(function () { b.classList.remove('is-copied'); }, 2600);
  }
  on(d, 'click', function (e) {
    var b = e.target.closest('[data-copy]'); if (!b) return;
    var c = COPY[b.getAttribute('data-copy')]; if (!c) return;
    var text = c.text();
    function done(ok) {
      if (ok) flag(b);
      if (c.quiet) { if (ok) toast(c.quiet); else { var x = $('.sharebox'); if (x) { x.focus(); x.select(); toast('Press and hold to copy'); } } return; }
      showCopySheet(c, text, ok);
    }
    if (navigator.clipboard && window.isSecureContext !== false) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(legacyCopy(text)); });
    } else { done(legacyCopy(text)); }
  });
  on($('.linkbox'), 'focus', function () { this.select(); });

  /* ------------------------------------------------------------ side menu */
  var side = $('#side'), scrim = $('#scrim'), mbtn = $('#menu-btn'), tog = $('#side-toggle');
  function mobile() { return innerWidth <= 1060; }
  function openDrawer() {
    if (!side) return;
    side.classList.add('open'); scrim && scrim.classList.add('on');
    mbtn && mbtn.setAttribute('aria-expanded', 'true');
    var cur = $('[aria-current="page"]', side) || $('a', side);
    setTimeout(function () { cur && cur.focus({ preventScroll: false }); }, 60);
  }
  function closeDrawer() {
    if (!side || !side.classList.contains('open')) return;
    side.classList.remove('open'); scrim && scrim.classList.remove('on');
    mbtn && mbtn.setAttribute('aria-expanded', 'false');
  }
  function syncToggle() {
    if (!tog) return;
    var off = html.classList.contains('side-off');
    tog.setAttribute('aria-expanded', mobile() ? String(side.classList.contains('open')) : String(!off));
    tog.setAttribute('aria-label', mobile() ? 'Open the menu' : (off ? 'Show the menu' : 'Hide the menu'));
  }
  on(mbtn, 'click', function () { side.classList.contains('open') ? closeDrawer() : openDrawer(); });
  on(scrim, 'click', closeDrawer);
  on(tog, 'click', function () {
    if (mobile()) { side.classList.contains('open') ? closeDrawer() : openDrawer(); return syncToggle(); }
    var off = html.classList.toggle('side-off');
    set('mtg-side', off ? 'off' : 'on'); syncToggle();
  });
  on(window, 'resize', function () { if (!mobile()) closeDrawer(); syncToggle(); });
  syncToggle();
  // keep the current item visible in a long menu
  var cur = side && $('[aria-current="page"]', side);
  if (cur && side.scrollHeight > side.clientHeight) { side.scrollTop = Math.max(0, cur.offsetTop - side.clientHeight / 2); }

  /* ------------------------------------------------------------ watched videos */
  var watched = {};
  try { (JSON.parse(get('alt-watched') || '[]') || []).forEach(function (k) { watched[k] = 1; }); } catch (e) {}
  function paintWatched() {
    $$('[data-vid]').forEach(function (el) { el.classList.toggle('watched', !!watched[el.getAttribute('data-vid')]); });
    var n = Object.keys(watched).filter(function (k) { return ALTV[k]; }).length;
    $$('[data-ring]').forEach(function (r) { r.style.setProperty('--v', n / Math.max(1, Object.keys(ALTV).length)); var x = $('[data-k="n"]', r); if (x) x.textContent = n; });
    var p = $('#player'); if (p) p.classList.toggle('watched', !!watched[$('[data-mark]', p).getAttribute('data-mark')]);
  }
  function markWatched(k) {
    if (!k || watched[k]) return;
    watched[k] = 1; set('alt-watched', JSON.stringify(Object.keys(watched)));
    paintWatched(); toast((ALTV[k] ? ALTV[k].st : 'Welcome tour') + ': watched ✓');
  }
  function track(v, k) {
    on(v, 'timeupdate', function () { if (v.duration && v.currentTime / v.duration > 0.9) markWatched(k); });
    on(v, 'ended', function () { markWatched(k); });
    on(v, 'play', function () { $$('video').forEach(function (o) { if (o !== v && !o.paused) o.pause(); }); });
  }
  on(d, 'click', function (e) { var m = e.target.closest('[data-mark]'); if (m) markWatched(m.getAttribute('data-mark')); });
  paintWatched();

  /* inline poster players */
  function startInline(btn) {
    var box = btn.parentNode, k = btn.getAttribute('data-code');
    var v = d.createElement('video');
    v.controls = true; v.playsInline = true; v.setAttribute('playsinline', ''); v.preload = 'auto';
    v.src = btn.getAttribute('data-src');
    var img = $('img', box); if (img) v.poster = img.currentSrc || img.src;
    box.replaceChild(v, btn); track(v, k);
    // a close button on the video, and back to the poster when it ends
    var x = d.createElement('button');
    x.type = 'button'; x.className = 'vclose'; x.setAttribute('aria-label', 'Close the video');
    x.innerHTML = '<svg class="ic" aria-hidden="true"><use href="#i-x"/></svg>';
    box.appendChild(x);
    var startY = window.scrollY || 0;
    function restore(back) {
      exitFs(v); v.pause();
      if (v.parentNode === box) box.replaceChild(btn, v);
      if (x.parentNode === box) box.removeChild(x);
      v.removeAttribute('src'); try { v.load(); } catch (e) {}
      // back to exactly where they pressed play (fullscreen can move the page)
      if (back) setTimeout(function () { if (Math.abs((window.scrollY || 0) - startY) > 2) window.scrollTo(0, startY); }, 350);
    }
    on(x, 'click', function () { restore(false); });
    on(v, 'ended', function () { exitFs(v); setTimeout(function () { restore(true); }, 600); });
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  }
  on(d, 'click', function (e) { var b = e.target.closest('.vplay'); if (b) startInline(b); });

  /* modal player for any [data-play] */
  on(d, 'click', function (e) {
    var b = e.target.closest('[data-play]'); if (!b) return;
    var k = b.getAttribute('data-play'), info = ALTV[k], pl = $('#player'); if (!info || !pl) return;
    var open = $('.sheet.on'); if (open && open !== pl) { open.classList.remove('on'); open.hidden = true; d.body.style.overflow = ''; }
    $('[data-k="title"]', pl).textContent = info.t + ' (' + info.d + ')';
    $('[data-mark]', pl).setAttribute('data-mark', k);
    var v = $('video', pl);
    v.poster = info.p.replace('-360.webp', '.webp'); v.src = info.s;
    if (!v._tracked) { v._tracked = 1; on(v, 'timeupdate', function () { if (v.duration && v.currentTime / v.duration > 0.9) markWatched($('[data-mark]', pl).getAttribute('data-mark')); }); on(v, 'ended', function () { exitFs(v); markWatched($('[data-mark]', pl).getAttribute('data-mark')); setTimeout(function () { closeSheet(pl); }, 800); }); on(v, 'play', function () { $$('video').forEach(function (o) { if (o !== v && !o.paused) o.pause(); }); }); }
    paintWatched(); openSheet(pl);
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  });

  /* playlists */
  $$('[data-playlist]').forEach(function (pl) {
    var fig = $('.now .vid', pl), desc = $('[data-k="desc"]', pl);
    function pick(k, play) {
      var info = ALTV[k]; if (!info) return;
      $$('[data-pick]', pl).forEach(function (b) { b.setAttribute('aria-current', b.getAttribute('data-pick') === k ? 'true' : 'false'); });
      var box = $('.vbox', fig), old = $('video', box);
      if (old) { old.pause(); }
      var big = info.p.replace('-360.webp', '.webp');
      box.innerHTML = '<img src="' + info.p + '" srcset="' + info.p + ' 360w, ' + big + ' 720w" sizes="(max-width:760px) 90vw, 340px" width="720" height="1280" alt="">' +
        '<button type="button" class="vplay" data-src="' + info.s + '" data-code="' + k + '" aria-label="Play ' + info.t + ' (' + info.d + ')"><span class="pbtn">' +
        '<svg class="ic" aria-hidden="true"><use href="#i-play"/></svg></span><span class="dur">' + info.d + '</span></button>';
      fig.setAttribute('data-vid', k);
      var cap = $('.vcap span', fig); if (cap) cap.innerHTML = '<b>' + info.t + '</b><br>' + info.l + ', ' + info.d;
      var mk = $('[data-mark]', fig); if (mk) mk.setAttribute('data-mark', k);
      var src = $('[data-pick="' + k + '"] .pt', pl); if (desc && src) desc.textContent = src.getAttribute('title') || '';
      paintWatched();
      if (play) {
        startInline($('.vplay', box));
        if (innerWidth <= 820) fig.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'center' });
      }
    }
    on(pl, 'click', function (e) {
      var b = e.target.closest('[data-pick]'); if (!b) return;
      var k = b.getAttribute('data-pick'); pick(k, true);
      try { history.replaceState(null, '', '#' + k); } catch (x) {}
    });
    var h = (location.hash || '').slice(1);
    if (h && $('[data-pick="' + h + '"]', pl)) pick(h, false);
  });

  /* ------------------------------------------------------------ scroll: progress bar, back to top, route map */
  var prog = $('.progress'), top = $('#totop'), route = $('[data-route]'), ticking = false;
  var stns = route ? $$('.stn', route) : [];
  function onScroll() {
    ticking = false;
    var h = d.documentElement, max = h.scrollHeight - innerHeight, sp = max > 0 ? Math.min(1, scrollY / max) : 0;
    if (prog) prog.style.setProperty('--sp', sp);
    if (top) { top.style.setProperty('--sp', sp); top.classList.toggle('on', scrollY > 700); }
    if (route) {
      var r = route.getBoundingClientRect(), line = innerHeight * 0.62;
      var p = Math.max(0, Math.min(1, (line - r.top - 24) / Math.max(1, r.height - 48)));
      route.style.setProperty('--p', p);
      stns.forEach(function (s) {
        var dot = $('.dot', s).getBoundingClientRect();
        s.classList.toggle('on', dot.top + 14 < line);
      });
    }
  }
  on(window, 'scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  on(window, 'resize', onScroll); onScroll();
  on(top, 'click', function () { scrollTo({ top: 0, behavior: RM ? 'auto' : 'smooth' }); var m = $('#main'); if (m) m.focus({ preventScroll: true }); });

  /* reveal for the route stations only (the one orchestrated moment) */
  if ('IntersectionObserver' in window && !RM) {
    var rv = $$('.rv').filter(function (el) { return el.getBoundingClientRect().top > innerHeight * 0.9; });
    rv.forEach(function (el) { el.classList.add('pre'); });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.remove('pre'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------------------ welcome video stage: a living route map */
  var stage = $('#stage'), cv = stage && $('canvas', stage);
  if (cv && cv.getContext) {
    var ctx = cv.getContext('2d'), W = 0, H = 0, DPR = Math.min(2, window.devicePixelRatio || 1), run = false, t0 = 0;
    var P = [[.06, .78], [.2, .62], [.32, .7], [.44, .46], [.58, .54], [.7, .32], [.84, .4], [.95, .2]];
    var B = [[.44, .46], [.5, .22], [.62, .14]];
    function size() { var r = cv.getBoundingClientRect(); W = r.width; H = r.height; cv.width = W * DPR; cv.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0); draw(t0); }
    function pt(a) { return [a[0] * W, a[1] * H]; }
    function path(pts) { ctx.beginPath(); pts.forEach(function (p, i) { var q = pt(p); i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); }); }
    function along(pts, f) {
      var L = [], tot = 0;
      for (var i = 1; i < pts.length; i++) { var a = pt(pts[i - 1]), b = pt(pts[i]), l = Math.hypot(b[0] - a[0], b[1] - a[1]); L.push(l); tot += l; }
      var dd = f * tot;
      for (var j = 0; j < L.length; j++) { if (dd <= L[j] && L[j] > 0) { var a2 = pt(pts[j]), b2 = pt(pts[j + 1]), k = dd / L[j]; return [a2[0] + (b2[0] - a2[0]) * k, a2[1] + (b2[1] - a2[1]) * k]; } dd -= L[j]; }
      return pt(pts[pts.length - 1]);
    }
    function glow(x, y, r, c, a) { var g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, c.replace('A', a)); g.addColorStop(1, c.replace('A', 0)); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); }
    function draw(t) {
      if (!W || !H) return;
      ctx.clearRect(0, 0, W, H);
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.strokeStyle = 'rgba(238,189,92,.42)'; ctx.lineWidth = Math.max(3, W / 160); path(P); ctx.stroke();
      ctx.strokeStyle = 'rgba(12,225,242,.35)'; ctx.lineWidth = Math.max(2, W / 240); path(B); ctx.stroke();
      P.forEach(function (p, i) { var q = pt(p), pulse = .5 + .5 * Math.sin(t / 900 + i); ctx.fillStyle = 'rgba(250,234,156,' + (.35 + .3 * pulse) + ')'; ctx.beginPath(); ctx.arc(q[0], q[1], Math.max(3, W / 170), 0, 7); ctx.fill(); });
      var f = (t / 9000) % 1, a = along(P, f), b = along(B, (t / 6000) % 1);
      glow(a[0], a[1], W / 18, 'rgba(238,189,92,A)', .55); glow(b[0], b[1], W / 26, 'rgba(12,225,242,A)', .45);
    }
    function loop(t) { if (!run) return; t0 = t; draw(t); requestAnimationFrame(loop); }
    size(); on(window, 'resize', size);
    if (!RM && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { run = es[0].isIntersecting; if (run) requestAnimationFrame(loop); }).observe(stage);
    } else { draw(3000); }
  }

  /* ------------------------------------------------------------ interactive diagrams */
  function seg(group, fn) {
    $$('button', group).forEach(function (b) {
      on(b, 'click', function () { $$('button', group).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); fn(b); });
    });
    var cur = $('[aria-pressed="true"]', group); if (cur) fn(cur);
  }
  // global leg window
  $$('[data-leg]').forEach(function (L) {
    seg($('.seg', L), function (b) {
      var w = +b.getAttribute('data-w');
      $$('.seats i', L).forEach(function (s) { var dd = +s.getAttribute('data-d'); s.classList.toggle('on', dd > 0 && dd <= w); });
      $('[data-k="w"]', L).textContent = w; $('[data-k="w2"]', L).textContent = w; $('[data-k="n"]', L).textContent = w * 2;
    });
  });
  // working level table
  var RATES = [10, 4, 2, 2, 2, 2, 1, 1, 1];
  $$('[data-wl]').forEach(function (W) {
    seg($('.seg', W), function (b) {
      var n = Math.min(9, +b.getAttribute('data-d') * 3), pc = 0;
      $$('tr[data-lv]', W).forEach(function (r) { var lv = +r.getAttribute('data-lv'), o = lv <= n; r.classList.toggle('is-open', o); if (o) pc += RATES[lv - 1]; });
      $('[data-k="lv"]', W).textContent = n; $('[data-k="pc"]', W).textContent = pc;
    });
  });
  // packages shopping list
  var pk = $$('[data-pkg]');
  pk.forEach(function (b) {
    on(b, 'click', function () {
      pk.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      $('.shop [data-k="name"]').textContent = $('.nm', b).textContent;
      $('.shop [data-k="usdt"]').textContent = (+b.getAttribute('data-price') + 1);
    });
  });
  // fit check
  var fit = $('[data-fitcheck]');
  if (fit) {
    var res = fit.parentNode.querySelector('.result');
    function score() {
      var boxes = $$('[data-fit]', fit), n = boxes.filter(function (x) { return x.checked; }).length;
      var afford = $('[data-fit="afford"]', fit).checked, msg;
      if (n === 0) msg = 'Tick the statements that are true for you.';
      else if (n === 5) msg = 'Looks like a fair fit to keep learning and, if you choose, to test-drive ALTRUVA with an amount you can afford to lose. Start with the explainers.';
      else if (n >= 3) msg = 'Almost. Look at what you left unticked: those are the things to sort out first. There is no rush.';
      else msg = 'Not yet, and that is fine. Learning costs nothing. Keep watching and decide later, or not at all.';
      if (n > 0 && !afford) msg += ' Please never use money you need for rent, food or family.';
      $('[data-k="score"]', res).textContent = n + ' of 5';
      $('[data-k="msg"]', res).textContent = msg;
      res.classList.toggle('good', n === 5);
    }
    $$('[data-fit]', fit).forEach(function (x) { on(x, 'change', score); });
  }
  // glossary filter
  var gq = $('[data-gfilter]');
  if (gq) {
    on(gq, 'input', function () {
      var q = gq.value.trim().toLowerCase(), shown = 0;
      $$('[data-term]').forEach(function (t) { var hit = !q || t.getAttribute('data-term').indexOf(q) > -1; t.hidden = !hit; if (hit) shown++; });
      $('[data-gempty]').hidden = shown > 0;
    });
  }

  /* ------------------------------------------------------------ 72-hour clock (saved on this device only) */
  var c72 = $('[data-clock72]');
  if (c72) {
    var jin = $('[data-join]', c72), left = $('[data-k="left"]', c72), stt = $('[data-k="status"]', c72), unt = $('[data-k="until"]', c72), tmr = null;
    function pad(x) { return (x < 10 ? '0' : '') + x; }
    function localVal(dt) { return dt.getFullYear() + '-' + pad(dt.getMonth() + 1) + '-' + pad(dt.getDate()) + 'T' + pad(dt.getHours()) + ':' + pad(dt.getMinutes()) + ':' + pad(dt.getSeconds()); }
    function paint72() {
      var v = jin.value, cd = $('.cd', c72);
      if (!v) { left.textContent = '72:00:00'; stt.textContent = 'Set your join time to start your clock'; unt.textContent = 'Saved on this device only.'; cd.classList.remove('closed', 'live'); return; }
      var start = new Date(v), end = new Date(start.getTime() + 72 * 3600 * 1000), ms = end - Date.now();
      if (isNaN(start)) return;
      var opts = { weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' };
      if (ms <= 0) {
        left.textContent = '00:00:00'; stt.textContent = 'Your 72-hour window has closed';
        unt.textContent = 'It closed ' + end.toLocaleString([], opts) + '. The global leg, working levels and matching keep working.';
        cd.classList.add('closed'); cd.classList.remove('live'); return;
      }
      if (ms > 72 * 3600 * 1000) { left.textContent = '72:00:00'; stt.textContent = 'That time is in the future'; unt.textContent = 'Check the date and time you joined.'; return; }
      var s = Math.floor(ms / 1000);
      left.textContent = pad(Math.floor(s / 3600)) + ':' + pad(Math.floor(s % 3600 / 60)) + ':' + pad(s % 60);
      stt.textContent = 'left in your 72-hour window';
      unt.textContent = 'Your window closes ' + end.toLocaleString([], opts) + '. Saved on this device only.';
      cd.classList.add('live'); cd.classList.remove('closed');
    }
    var saved = get('alt-join'); if (saved) jin.value = saved;
    on(jin, 'input', function () { set('alt-join', jin.value); paint72(); });
    on($('[data-now]', c72), 'click', function () { jin.value = localVal(new Date()); set('alt-join', jin.value); paint72(); toast('Your 72-hour clock has started ✓'); });
    on($('[data-clearjoin]', c72), 'click', function () { jin.value = ''; try { localStorage.removeItem('alt-join'); } catch (e) {} paint72(); });
    paint72(); tmr = setInterval(paint72, 1000);
  }

  /* ------------------------------------------------------------ calculators */
  function num(s) {
    s = String(s == null ? '' : s).trim().replace(/[\s R$]/g, '').replace(/USDT|ZAR/gi, '');
    if (!s) return null;
    if (s.indexOf('.') > -1 && s.indexOf(',') > -1) s = s.replace(/,/g, '');
    else if (s.indexOf(',') > -1) { var parts = s.split(','); s = (parts.length === 2 && parts[1].length !== 3) ? parts[0] + '.' + parts[1] : s.replace(/,/g, ''); }
    if (!/^-?\d*\.?\d+$/.test(s) && !/^-?\d+\.?$/.test(s)) return NaN;
    return parseFloat(s);
  }
  function f2(n, dp) { dp = dp == null ? 2 : dp; return n.toLocaleString('en-US', { minimumFractionDigits: dp, maximumFractionDigits: dp }); }
  function cut2(n) { return Math.floor(n * 100 + 1e-7) / 100; }
  function val(F, id) {
    var el = $('[data-in="' + id + '"]', F), err = $('[data-err="' + id + '"]', F), v = num(el.value);
    var bad = v !== null && (isNaN(v) || v < 0);
    el.classList.toggle('bad', bad); el.setAttribute('aria-invalid', bad ? 'true' : 'false');
    if (err) err.textContent = bad ? 'Type a number of zero or more, like ' + (el.getAttribute('placeholder') || '100') + '.' : '';
    return bad ? NaN : v;
  }
  function out(R, k, txt) { var el = $('[data-out="' + k + '"]', R); if (el) el.textContent = txt; }
  function bars(R, a, b) { var x = $('[data-bar="a"]', R), y = $('[data-bar="b"]', R); if (x) x.style.width = a + '%'; if (y) y.style.width = b + '%'; }

  var CALC = {
    split: function (F, R) {
      var bal = val(F, 'bal'), tot = val(F, 'tot');
      if (bal === null || tot === null || isNaN(bal) || isNaN(tot)) {
        out(R, 'wallet', '0.00 USDT'); out(R, 're', '0.00 USDT'); out(R, 'tier', '50% / 50%'); out(R, 'after', '0.00 USDT'); bars(R, 50, 50);
        out(R, 'how', 'Type your balance and total deposit.'); return;
      }
      var w = tot <= 5000 ? .5 : (tot < 50000 ? .6 : .7), band = tot <= 5000 ? 'up to 5,000' : (tot < 50000 ? 'between 5,001 and 49,999' : '50,000 or more');
      var toW = cut2(bal * w), re = cut2(bal * (1 - w));
      out(R, 'wallet', f2(toW) + ' USDT'); out(R, 're', f2(re) + ' USDT');
      out(R, 'tier', Math.round(w * 100) + '% / ' + Math.round((1 - w) * 100) + '%');
      out(R, 'after', f2(tot + bal * (1 - w)) + ' USDT'); bars(R, w * 100, (1 - w) * 100);
      out(R, 'how', 'Your total deposit of ' + f2(tot) + ' is ' + band + ', so the split is ' + Math.round(w * 100) + '/' + Math.round((1 - w) * 100) + '. ' +
        f2(bal) + ' × ' + Math.round(w * 100) + '% = ' + f2(toW) + ' to your wallet, and ' + f2(bal) + ' × ' + Math.round((1 - w) * 100) + '% = ' + f2(re) + ' reinvested.');
    },
    wl: function (F, R) {
      var dSel = $('.seg [aria-pressed="true"]', F), dirs = dSel ? +dSel.getAttribute('data-d') : 1, open = Math.min(9, dirs * 3);
      var earn = 0, stay = 0, list = '', any = false, bad = false;
      for (var i = 1; i <= 9; i++) {
        var a = val(F, 'l' + i), pay = $('[data-pay="' + i + '"]', F);
        if (pay) { pay.textContent = ''; pay.className = 'lvpay'; }
        if (a !== null && isNaN(a)) { bad = true; continue; }
        if (!a) continue; any = true;
        var part = a * RATES[i - 1] / 100, o = i <= open;
        if (pay) { pay.textContent = o ? RATES[i - 1] + '% = ' + f2(part) : 'Closed: stays in the contract'; pay.className = 'lvpay ' + (o ? 'o' : 'c'); }
        if (o) earn += part; else stay += part;
        list += '<li class="' + (o ? 'o' : 'c') + '"><span>Level ' + i + ': ' + RATES[i - 1] + '% of ' + f2(a) + '</span><b>' + f2(part) + (o ? '' : ' (closed, stays in the contract)') + '</b></li>';
      }
      out(R, 'earn', f2(earn) + ' USDT'); out(R, 'stay', f2(stay) + ' USDT'); out(R, 'open', open + ' of 9');
      $('[data-out="list"]', R).innerHTML = list;
      out(R, 'how', bad ? 'Fix the highlighted level first.' : (any ? 'With ' + (dirs === 3 ? '3 or more directs' : dirs + ' direct' + (dirs === 1 ? '' : 's')) + ', levels 1 to ' + open + ' are open' + (open ? '' : ' (none yet)') + '. Closed levels pay nobody: that share stays in the contract.' : 'Type an amount on any level.'));
      if (!open) out(R, 'how', any ? 'With no directs, every level is closed: each share stays in the contract.' : 'Type an amount on any level.');
    },
    match: function (F, R) {
      var s1 = val(F, 's1'), s2 = val(F, 's2'), rate = val(F, 'rate');
      var biz = val(F, 'biz'), all = val(F, 'all');
      if (biz && all && !isNaN(biz) && !isNaN(all)) out(R.parentNode, 'rate2', 'Rate = 25% of ' + f2(biz) + ' ÷ ' + f2(all) + ' = ' + (0.25 * biz / all).toFixed(6) + ' per unit.');
      else out(R.parentNode, 'rate2', "Rate = 25% of the day's business ÷ everyone's matched.");
      if ([s1, s2, rate].some(function (x) { return x === null || isNaN(x); })) { out(R, 'earn', '0.00 USDT'); out(R, 'matched', '0'); out(R, 'extra', '0'); bars(R, 0, 0); out(R, 'how', 'Type both sides and a rate.'); return; }
      var m = Math.min(s1, s2), big = Math.max(s1, s2), e = m * rate;
      out(R, 'earn', f2(e) + ' USDT'); out(R, 'matched', f2(m)); out(R, 'extra', f2(big - m));
      bars(R, big ? m / big * 100 : 0, big ? (big - m) / big * 100 : 0);
      out(R, 'how', 'The smaller side is ' + f2(m) + '. ' + f2(m) + ' × ' + rate + ' = ' + f2(e) + ' USDT for the day. The rate is different every day.');
    },
    zar: function (F, R) {
      var dirB = $('[data-dir][aria-pressed="true"]', F), u2z = !dirB || dirB.getAttribute('data-dir') === 'u2z';
      $('[data-in="amt"]', F).nextElementSibling.textContent = u2z ? 'USDT' : 'ZAR';
      var pk = $('[data-pkgs]', F), pr = $('[data-out="pkres"]', F); if (pk) pk.hidden = !u2z; if (pr) pr.innerHTML = '';
      var amt = val(F, 'amt'), rate = val(F, 'zrate'), fee = val(F, 'fee') || 0;
      if (amt === null || rate === null || isNaN(amt) || isNaN(rate) || isNaN(fee) || !rate) {
        out(R, 'biglab', u2z ? 'Value in rand' : 'USDT needed'); out(R, 'main', u2z ? 'R0.00' : '0.00 USDT'); out(R, 'net', u2z ? 'R0.00' : 'R0.00');
        out(R, 'how', rate === 0 ? 'The rate must be more than zero.' : 'Type an amount and a rate.'); return;
      }
      if (u2z) {
        var g = amt * rate, n = Math.max(0, g - fee);
        if (pr) pr.innerHTML = f2(amt) + ' USDT is about <b>R' + f2(g) + '</b> before fees.';
        out(R, 'biglab', 'Value in rand'); out(R, 'main', 'R' + f2(g)); out(R, 'netlab', 'After R' + f2(fee) + ' fees'); out(R, 'net', 'R' + f2(n));
        out(R, 'how', f2(amt) + ' USDT × R' + f2(rate, 4) + ' = R' + f2(g) + (fee ? ', minus R' + f2(fee) + ' fees = R' + f2(n) : '') + '.');
      } else {
        var need = (amt + fee) / rate;
        out(R, 'biglab', 'USDT needed'); out(R, 'main', f2(need) + ' USDT'); out(R, 'netlab', 'To receive R' + f2(amt) + ' after fees of'); out(R, 'net', 'R' + f2(fee));
        out(R, 'how', '(R' + f2(amt) + ' + R' + f2(fee) + ' fees) ÷ R' + f2(rate, 4) + ' = ' + f2(need) + ' USDT.');
      }
    }
  };

  $$('[data-calc]').forEach(function (F) {
    var kind = F.getAttribute('data-calc'), R = F.parentNode.querySelector('[data-result]'), fn = CALC[kind];
    function go() { fn(F, R); }
    $$('input', F).forEach(function (i) { on(i, 'input', go); });
    var dseg = $('.seg:not(.presets)', F);
    if (dseg && kind !== 'zar') seg(dseg, go);
    if (kind === 'zar') seg($('.seg', F), go);
    $$('[data-preset]', F).forEach(function (b) {
      on(b, 'click', function () {
        var p = JSON.parse(b.getAttribute('data-preset'));
        $$('input', F).forEach(function (i) { if (i.getAttribute('data-in') !== 'rate' && i.getAttribute('data-in') !== 'biz' && i.getAttribute('data-in') !== 'all') i.value = ''; });
        Object.keys(p).forEach(function (k) {
          if (k === 'd') { var t = $('.seg [data-d="' + p[k] + '"]', F); if (t) t.click(); return; }
          var i = $('[data-in="' + k + '"]', F); if (i) i.value = p[k];
        });
        go();
      });
    });
    var clr = $('[data-clear]', F);
    on(clr, 'click', function () { $$('input', F).forEach(function (i) { i.value = ''; }); go(); var first = $('input', F); first && first.focus(); });
    var ur = $('[data-userate]', F);
    on(ur, 'click', function () {
      var biz = num($('[data-in="biz"]', F).value), all = num($('[data-in="all"]', F).value);
      if (biz && all) { $('[data-in="rate"]', F).value = (0.25 * biz / all).toFixed(6); go(); toast('Rate updated ✓'); }
    });
    if (kind === 'zar') zarLive(F, go);
    $$('[data-amt]', F).forEach(function (b) {
      on(b, 'click', function () { $('[data-in="amt"]', F).value = b.getAttribute('data-amt'); go(); });
    });
    var empty = $$('input', F).every(function (i) { return !i.value; }), firstP = $('[data-preset]', F);
    if (empty && firstP) firstP.click(); else go();
    if (kind === 'zar' && !$('[data-in="amt"]', F).value) { $('[data-in="amt"]', F).value = '100'; go(); }
  });

  function zarLive(F, go) {
    var st = $('[data-out="status"]', F), rateIn = $('[data-in="zrate"]', F), own = false, ic = '<svg class="ic" aria-hidden="true"><use href="#i-refresh-cw"/></svg> ';
    on(rateIn, 'input', function () { own = true; });
    function load(force) {
      st.innerHTML = ic + '<span>Loading the live rate…</span>'; st.className = 'ratebox';
      var ctl = window.AbortController ? new AbortController() : null, tm = setTimeout(function () { ctl && ctl.abort(); }, 8000);
      fetch('https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=zar&include_last_updated_at=true', ctl ? { signal: ctl.signal } : {})
        .then(function (r) { if (!r.ok) throw 0; return r.json(); })
        .then(function (j) {
          clearTimeout(tm);
          var r = j && j.tether && j.tether.zar, at = j && j.tether && j.tether.last_updated_at;
          if (!r) throw 0;
          if (!own || force) { rateIn.value = r.toFixed(4); own = false; }
          var when = at ? new Date(at * 1000) : new Date(), old = at && (Date.now() / 1000 - at > 7200);
          st.className = 'ratebox ok' + (old ? ' old' : '');
          st.innerHTML = ic + '<span>Live rate from CoinGecko: <b>R' + f2(r, 4) + '</b> per USDT, updated ' + when.toLocaleString([], { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) + (old ? '. It may be out of date.' : '.') + '</span>';
          go();
        })
        .catch(function () {
          clearTimeout(tm);
          st.className = 'ratebox bad';
          st.innerHTML = ic + "<span>Couldn't load the live rate right now. Type the rate your exchange shows.</span>";
          go();
        });
    }
    on($('[data-refresh]', F), 'click', function () { load(true); });
    load(false);
  }
})();
