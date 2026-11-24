/* Bitcoin Wealth guide by MTG | site behaviour. No tracking, no cookies. Stores only: watched videos, menu state. */
(function () {
  'use strict';
  var d = document, html = d.documentElement, BW = window.BW || {}, BWV = window.BWV || {};
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
  var lastFocus = null, savedY = 0;
  var sheetHist = false, maxHist = false, skipPop = 0;   // our own Back steps (a sheet, a player covering the window) and our own history.back() calls
  function ownBack() { skipPop++; try { history.back(); } catch (e) { skipPop--; } }
  /* while a sheet is open, the page behind it is out of reach for the keyboard and for screen readers */
  function hush(yes) {
    $$('body > *').forEach(function (c) {
      if (c.classList.contains('sheet') || c.classList.contains('pl') || c.id === 'toast') return;
      if (yes) c.setAttribute('inert', ''); else c.removeAttribute('inert');
    });
  }
  function openSheet(el) {
    if (!el) return;
    if (!$('.sheet.on')) { lastFocus = d.activeElement; savedY = window.scrollY || 0; }
    clearTimeout(el._t); el._at = Date.now();
    el.hidden = false; void el.offsetWidth; el.classList.add('on');
    d.body.style.overflow = 'hidden'; hush(true);
    if (!sheetHist) { try { history.pushState({ bwSheet: 1 }, ''); sheetHist = true; } catch (e) {} }
    var f = $('[data-close],[data-pl-x]', el); if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 30);
  }
  function closeSheet(el, fromPop) {
    if (!el || el.hidden || !el.classList.contains('on')) return;
    el.classList.remove('on'); d.body.style.overflow = ''; hush(false);
    var pl = el.id === 'player' ? $('#pl-pop') : null;      // the pop-up player: leave full screen, stop, and empty it
    if (pl) { var v = $('video', pl); if (v) v.pause(); leaveMax(pl); }
    el._t = setTimeout(function () { el.hidden = true; if (pl) plShut(pl); }, 260);
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus({ preventScroll: true }); } catch (e) {} }
    var y = savedY;
    if (Math.abs((window.scrollY || 0) - y) > 2) window.scrollTo(0, y);
    setTimeout(function () { if (Math.abs((window.scrollY || 0) - y) > 2) window.scrollTo(0, y); }, 400);
    if (sheetHist && !fromPop) { sheetHist = false; ownBack(); }
  }
  /* the phone's Back button undoes the newest step first: a player covering the window, then an open sheet */
  on(window, 'popstate', function () {
    if (skipPop) { skipPop--; return; }
    if (maxHist) { maxHist = false; if (maxed && maxed._hold) coverWindow(maxed, false, true); return; }
    if (sheetHist) { sheetHist = false; $$('.sheet.on').forEach(function (s) { closeSheet(s, true); }); }
  });
  $$('.sheet').forEach(function (s) {
    on(s, 'click', function (e) {
      if (e.target === s && Date.now() - (s._at || 0) < 500) return;      // the second tap of a double tap must not close what the first one opened
      if (e.target === s || e.target.closest('[data-close]')) closeSheet(s);
    });
  });
  on(d, 'keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (maxed && maxed._hold) return leaveMax(maxed);       // first out of a player that covers the window
    $$('.sheet.on').forEach(function (s) { closeSheet(s); });
    closeDrawer();
  });

  /* ------------------------------------------------------------ copy buttons */
  var COPY = {
    signup: {
      text: function () { return BW.ref; }, title: 'Sign-up link copied', fail: 'Copy the sign-up link',
      sub: "This is MTG's Bitcoin Wealth referral link. Introduced by someone else? Use their link instead, so they stay your sponsor.",
      steps: ['Open <b>SafePal</b> and tap the <b>Browser</b> (Explore) tab.', 'Paste the link in the top bar, choose <b>BNB Smart Chain</b> and connect your wallet.', 'Have 0.001 BTC worth of BTCB plus a little BNB for fees, then approve the exact amount and activate slot 1.'],
      note: 'Learn first, and only use money you can afford to lose.',
      acts: function () { return '<a class="btn btn-gold btn-sm" href="' + BW.join + '"><span class="lbl">Join Step-By-Step</span></a><a class="btn btn-ghost btn-sm" href="' + BW.tut + '"><span class="lbl">Tutorial Videos</span></a>'; }
    },
    share: { text: function () { var b = $('.sharebox'); return b ? b.value : ''; }, quiet: 'Message copied ✓' },
    contract: { text: function () { return '0x1ad09b043E0Fe59243C9a18ee1c855bd7792Cd29'; }, quiet: 'Contract address copied ✓' }
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
    mbtn && mbtn.setAttribute('aria-expanded', 'true'); syncToggle();
    var cur = $('[aria-current="page"]', side) || $('a', side);
    setTimeout(function () { cur && cur.focus({ preventScroll: false }); }, 60);
  }
  function closeDrawer() {
    if (!side || !side.classList.contains('open')) return;
    side.classList.remove('open'); scrim && scrim.classList.remove('on');
    mbtn && mbtn.setAttribute('aria-expanded', 'false'); syncToggle();
  }
  function syncToggle() {
    if (!tog) return;
    var off = html.classList.contains('side-off');
    tog.setAttribute('aria-expanded', mobile() ? String(side.classList.contains('open')) : String(!off));
    tog.setAttribute('aria-label', mobile() ? (side.classList.contains('open') ? 'Hide the menu' : 'Show the menu') : (off ? 'Show the menu' : 'Hide the menu'));
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
  var watched = {}, toastLater = '';
  try { (JSON.parse(get('bw-watched') || '[]') || []).forEach(function (k) { watched[k] = 1; }); } catch (e) {}
  function paintWatched() {
    $$('[data-vid]').forEach(function (el) { el.classList.toggle('watched', !!watched[el.getAttribute('data-vid')]); });
    var n = Object.keys(watched).filter(function (k) { return BWV[k]; }).length;
    $$('[data-ring]').forEach(function (r) { r.style.setProperty('--v', n / Math.max(1, Object.keys(BWV).length)); var x = $('[data-k="n"]', r); if (x) x.textContent = n; });
  }
  /* quietly: while a video plays, the "watched" note waits until the player has closed, so it never lies on the picture */
  function markWatched(k, quietly) {
    if (!k || watched[k]) return;
    watched[k] = 1; set('bw-watched', JSON.stringify(Object.keys(watched)));
    paintWatched();
    var m = (BWV[k] ? BWV[k].st : 'Video') + ': watched ✓';
    if (quietly) toastLater = m; else toast(m);
  }
  on(d, 'click', function (e) { var m = e.target.closest('[data-mark]'); if (m) markWatched(m.getAttribute('data-mark')); });
  paintWatched();

  /* ------------------------------------------------------------ video players
     One player (.pl) for every video: in the page, in the pop-up and full screen (MTG, 16 Nov 2026: "displayed in
     full, nothing hidden, but not too big ... even when maximized ... and the close button is still there").
     The screen has the video's own shape and nothing lies on the picture; Full Screen and Close sit in the bar.
     The words "Full Screen" always show, so a visitor knows what the button does (MTG, 16 Nov 2026).
       cover  the poster and the play button
       .on    playing: the bar shows Full Screen and Close
       .max   full screen: the bar and the whole video, nothing else
     A video that plays to the end closes itself; /assets/video-return.js then puts the page back where they were. */
  var maxed = null, wantMax = null;                     // the player that is full screen now; the one that asked for it
  var IPHONE = /iP(hone|od)/.test(navigator.userAgent || '');
  function fsElement() { return d.fullscreenElement || d.webkitFullscreenElement || null; }
  function quiet(p) { if (p && p.catch) p.catch(function () {}); }
  function hdrHeight() { return parseFloat(getComputedStyle(html).getPropertyValue('--hdr')) || 66; }
  function footHeight() {                               // a page's fixed bottom bar (the landing page's quick menu on phones)
    var n = $('.bnav'); return n && getComputedStyle(n).position === 'fixed' ? n.getBoundingClientRect().height : 0;
  }
  /* old browsers without svh and dvh: give the styles the real visible height */
  if (!(window.CSS && CSS.supports && CSS.supports('height', '100svh'))) {
    var vhFix = function () { var h = (window.innerHeight || html.clientHeight) + 'px'; html.style.setProperty('--svh', h); html.style.setProperty('--dvh', h); };
    vhFix(); on(window, 'resize', vhFix);
  }
  function setMax(pl, yes) {
    pl.classList.toggle('max', yes);
    var b = $('[data-pl-max]', pl); if (b) b.setAttribute('aria-label', yes ? 'Exit Full Screen' : 'Full Screen');
    if (yes) maxed = pl; else if (maxed === pl) maxed = null;
    // a wide video turns the phone on its side while it is full screen (where the phone allows it)
    try {
      var o = window.screen && screen.orientation;
      if (o && yes && o.lock && pl.classList.contains('pl-h') && fsElement()) quiet(o.lock('landscape'));
      else if (o && !yes && o.unlock) o.unlock();
    } catch (e) {}
  }
  /* where the browser has no full screen for a page element (some in-app browsers), the player itself covers the window */
  function coverWindow(pl, yes, fromPop) {
    var v = $('video', pl), playing = v && !v.paused, f = d.activeElement;
    if (yes && !pl._hold) {
      var h = d.createElement('div'); h.className = 'pl-hold'; h.style.height = pl.offsetHeight + 'px';
      pl.parentNode.insertBefore(h, pl); pl._hold = h; d.body.appendChild(pl); pl.classList.add('cover-win'); html.classList.add('pl-lock');
      if (!maxHist) { try { history.pushState({ bwMax: 1 }, ''); maxHist = true; } catch (e) {} }      // Back leaves it, like real full screen
    } else if (!yes && pl._hold) {
      pl._hold.parentNode.replaceChild(pl, pl._hold); pl._hold = null; pl.classList.remove('cover-win'); html.classList.remove('pl-lock');
      if (maxHist && !fromPop) { maxHist = false; ownBack(); }
    }
    setMax(pl, yes);
    if (playing && v.paused) quiet(v.play());           // moving a video pauses it: carry on
    if (f && f !== d.activeElement && pl.contains(f)) { try { f.focus({ preventScroll: true }); } catch (e) {} }
  }
  function maxFailed() { var pl = wantMax; wantMax = null; if (pl && pl.classList.contains('on') && !fsElement()) coverWindow(pl, true); }
  function enterMax(pl) {
    var v = $('video', pl), req = pl.requestFullscreen || pl.webkitRequestFullscreen;
    if (req && (d.fullscreenEnabled || d.webkitFullscreenEnabled)) {
      wantMax = pl;
      try { var r = req.call(pl); if (r && r.catch) r.catch(maxFailed); } catch (e) { maxFailed(); }
      setTimeout(function () { if (wantMax === pl) maxFailed(); }, 1200);      // some browsers never say that it failed
    } else if (IPHONE && v && v.webkitEnterFullscreen) {  // iPhone: its own full screen player, which has its own Close
      try { v.webkitEnterFullscreen(); } catch (e) { coverWindow(pl, true); }
    } else coverWindow(pl, true);
  }
  function leaveMax(pl) {
    var v = pl && $('video', pl);
    if (wantMax === pl) wantMax = null;
    try {
      if (fsElement()) { if (d.exitFullscreen) quiet(d.exitFullscreen()); else if (d.webkitExitFullscreen) d.webkitExitFullscreen(); }
      if (v && v.webkitDisplayingFullscreen && v.webkitExitFullscreen) v.webkitExitFullscreen();
    } catch (e) {}
    if (pl && pl._hold) coverWindow(pl, false);
  }
  /* run fn once full screen has really ended (it ends a moment after it is asked to); 1.2 s at most */
  function whenOut(v, fn) {
    if (!fsElement() && !(v && v.webkitDisplayingFullscreen)) return fn();
    var done = false, evs = ['fullscreenchange', 'webkitfullscreenchange'], t = setTimeout(go, 1200);
    function go() { if (done) return; done = true; clearTimeout(t); evs.forEach(function (e) { d.removeEventListener(e, chk); }); if (v) v.removeEventListener('webkitendfullscreen', go); fn(); }
    function chk() { if (!fsElement()) go(); }
    evs.forEach(function (e) { d.addEventListener(e, chk); }); if (v) v.addEventListener('webkitendfullscreen', go);
  }
  ['fullscreenchange', 'webkitfullscreenchange'].forEach(function (ev) {
    on(d, ev, function () {
      var el = fsElement();
      if (el) wantMax = null;
      $$('.pl.max').forEach(function (p) { if (p !== el && !p._hold) setMax(p, false); });
      if (el && el.classList && el.classList.contains('pl')) setMax(el, true);
    });
  });
  ['fullscreenerror', 'webkitfullscreenerror'].forEach(function (ev) { on(d, ev, maxFailed); });

  /* a 16:9 video has a light file for phones and a 1080p file for big screens */
  function pickSrc(src, hd) {
    var c = navigator.connection || {};
    return (hd && !c.saveData && Math.max(window.innerWidth || 0, (window.screen && screen.width) || 0) >= 1200) ? hd : src;
  }
  /* while an open player is on screen, the floating buttons step aside (nothing may lie on the picture) */
  var plSeen = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) { es.forEach(function (en) { en.target._seen = en.isIntersecting; }); syncPlaying(); }) : null;
  function syncPlaying() { html.classList.toggle('pl-playing', $$('.pl.on').some(function (p) { return p._seen !== false; })); }
  function plShut(pl) {                                 // back to the cover: no video left in the player
    var v = $('video', pl);
    if (v) { try { v.pause(); } catch (e) {} v.removeAttribute('src'); try { v.load(); } catch (e) {} if (v.parentNode) v.parentNode.removeChild(v); }
    pl.classList.remove('on');
    if (plSeen) plSeen.unobserve(pl);
    syncPlaying();
    if (toastLater && !$('.pl.on')) { toast(toastLater); toastLater = ''; }
  }
  function plClose(pl) {                                // Close, or the video ended: out of full screen first, then back to the cover
    var v = $('video', pl);
    if (v) { try { v.pause(); } catch (e) {} }
    leaveMax(pl);
    whenOut(v, function () {
      var sheet = pl.id === 'pl-pop' ? $('#player') : null;
      if (sheet) return closeSheet(sheet);
      var had = pl.contains(d.activeElement) || d.activeElement === d.body || !d.activeElement;
      plShut(pl);
      var b = $('.vplay', pl); if (b && had) { try { b.focus({ preventScroll: true }); } catch (e) {} }
    });
  }
  function plOpen(pl, k, src, poster) {
    plShut(pl);
    var v = d.createElement('video');
    v.controls = true; v.playsInline = true; v.setAttribute('playsinline', ''); v.preload = 'auto';
    v.setAttribute('controlslist', 'nofullscreen nodownload noremoteplayback');   // our own Full Screen keeps Close on screen
    v.setAttribute('disablepictureinpicture', '');
    v.setAttribute('aria-label', (BWV[k] || {}).t || 'Video');
    if (poster) v.poster = poster;
    v.src = src;
    v.style.pointerEvents = 'none'; setTimeout(function () { v.style.pointerEvents = ''; }, 450);      // the second tap of a double tap must not pause it
    $('.pl-scr', pl).appendChild(v);
    pl.classList.add('on'); pl._seen = true; if (plSeen) plSeen.observe(pl); syncPlaying();
    on(v, 'timeupdate', function () { if (v.duration && v.currentTime / v.duration > 0.9) markWatched(k, true); });
    on(v, 'play', function () { $$('.pl video').forEach(function (o) { if (o !== v && !o.paused) o.pause(); }); });
    on(v, 'ended', function () { markWatched(k, true); if ($('video', pl) === v) plClose(pl); });
    quiet(v.play());
    return v;
  }
  /* bring the whole player on screen, under the site's top bar and above a fixed bottom bar */
  function plIntoView(pl) {
    var r = pl.getBoundingClientRect(), top = hdrHeight() + 10, bot = (window.innerHeight || html.clientHeight) - footHeight() - 8;
    var dy = r.top < top ? r.top - top : (r.bottom > bot ? Math.min(r.bottom - bot, r.top - top) : 0);
    if (Math.abs(dy) > 2) { try { window.scrollBy({ top: dy, behavior: RM ? 'auto' : 'smooth' }); } catch (e) { window.scrollBy(0, dy); } }
  }
  /* the height a player may take: the visible screen between the page's fixed bars (the pop-up has the whole screen) */
  function plRoom(pl) { return (window.innerHeight || html.clientHeight) - (pl.id === 'pl-pop' ? 16 : hdrHeight() + footHeight()); }
  /* a screen too short for the smallest frame (a phone on its side): straight to full screen, where the whole video always fits */
  function fitOrMax(pl) {
    if (pl.getBoundingClientRect().height > plRoom(pl)) enterMax(pl); else if (pl.id !== 'pl-pop') plIntoView(pl);
  }
  var fitT;
  on(window, 'resize', function () {                    // the phone was turned while a video is open
    clearTimeout(fitT); fitT = setTimeout(function () { var pl = $('.pl.on:not(.max)'); if (pl && pl.getBoundingClientRect().height > plRoom(pl)) enterMax(pl); }, 350);
  });
  /* a cover in the page: it plays in place */
  function startInline(btn) {
    var pl = btn.closest('.pl'); if (!pl) return;
    var img = $('.pl-scr img', pl);
    var v = plOpen(pl, btn.getAttribute('data-code'), pickSrc(btn.getAttribute('data-src'), btn.getAttribute('data-src-hd')), img ? (img.currentSrc || img.src) : '');
    try { v.focus({ preventScroll: true }); } catch (e) {}
    fitOrMax(pl);
  }
  /* a video in the pop-up: the phone for 9:16, the laptop for 16:9. at: start at this second (a step picked from a video's page) */
  function openPop(k, at) {
    var info = BWV[k], sheet = $('#player'), pop = $('#pl-pop'); if (!info || !sheet || !pop) return;
    var open = $('.sheet.on'); if (open && open !== sheet) { open.classList.remove('on'); open.hidden = true; d.body.style.overflow = ''; }
    pop.classList.toggle('pl-h', info.o === 'h'); pop.classList.toggle('pl-v', info.o !== 'h');
    sheet.setAttribute('aria-label', info.t + ' (' + info.d + ')');
    openSheet(sheet);
    var v = plOpen(pop, k, pickSrc(info.s, info.hd), info.pb || info.p);
    if (at > 0) seekTo(v, at);
    fitOrMax(pop);
  }
  function seekTo(v, at) {
    var go = function () { try { if (isFinite(v.duration) && at < v.duration - 1) v.currentTime = at; } catch (e) {} };
    if (v.readyState >= 1) go(); else on(v, 'loadedmetadata', go);
  }
  on(d, 'click', function (e) {
    var t = e.target, b, pl;
    /* a cover in the laptop frame: a 16:9 video plays in place; a 9:16 video (its cover names it in data-play) opens the pop-up's phone */
    if ((b = t.closest('.vplay')) && !b.hasAttribute('data-play')) return startInline(b);
    if ((b = t.closest('[data-pl-max]'))) { pl = b.closest('.pl'); return pl.classList.contains('max') ? leaveMax(pl) : enterMax(pl); }
    if ((b = t.closest('[data-pl-x]'))) return plClose(b.closest('.pl'));
    /* a button beside a cover that starts that video: [data-start="code"] (a video that is already open just carries on) */
    if ((b = t.closest('[data-start]'))) {
      var c = $('.vplay[data-code="' + b.getAttribute('data-start') + '"]'), pv; pl = c && c.closest('.pl'); pv = pl && $('video', pl);
      if (c && c.hasAttribute('data-play')) return openPop(c.getAttribute('data-play'));
      if (pv) { quiet(pv.play()); plIntoView(pl); } else if (c) startInline(c);
      return;
    }
    /* any [data-play="code"] opens that video in the pop-up; data-at="seconds" starts it at that step */
    if ((b = t.closest('[data-play]'))) openPop(b.getAttribute('data-play'), parseFloat(b.getAttribute('data-at')) || 0);
  });
  /* a link to a moment of a video's own page (…?t=97): the video opens at that second, ready to play */
  (function () {
    var m = /[?&]t=(\d+)/.exec(location.search), c = $('[data-watch]');
    if (!m || !c) return;
    var k = c.getAttribute('data-watch'), at = parseInt(m[1], 10);
    if (!BWV[k] || !(at > 0)) return;
    setTimeout(function () { openPop(k, at); }, 350);
  })();

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


  /* ------------------------------------------------------------ count-up numbers (proof strip) */
  function fmt(n, dp) { return n.toLocaleString('en-US', { minimumFractionDigits: dp || 0, maximumFractionDigits: dp || 0 }); }
  var counts = $$('[data-count]');
  if (counts.length) {
    var runCount = function (el) {
      var end = +el.getAttribute('data-count'), dp = +(el.getAttribute('data-dp') || 0);
      if (RM) { el.textContent = fmt(end, dp); return; }
      var t0 = null;
      (function step(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 1600), e = 1 - Math.pow(1 - k, 3); el.textContent = fmt(end * e, dp); if (k < 1) requestAnimationFrame(step); })(performance.now());
    };
    if ('IntersectionObserver' in window) {
      var cio = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { runCount(en.target); cio.unobserve(en.target); } }); }, { threshold: .4 });
      counts.forEach(function (c) { cio.observe(c); });
    } else counts.forEach(runCount);
  }

  /* ------------------------------------------------------------ 3D tilt on glass cards (pointer only) */
  if (!RM && window.matchMedia && matchMedia('(hover:hover) and (pointer:fine)').matches) {
    $$('[data-tilt]').forEach(function (el) {
      on(el, 'pointermove', function (e) {
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        el.style.setProperty('--rx', (-y * 6).toFixed(2) + 'deg'); el.style.setProperty('--ry', (x * 8).toFixed(2) + 'deg');
        el.style.setProperty('--mx', ((x + .5) * 100).toFixed(1) + '%'); el.style.setProperty('--my', ((y + .5) * 100).toFixed(1) + '%');
      });
      on(el, 'pointerleave', function () { el.style.setProperty('--rx', '0deg'); el.style.setProperty('--ry', '0deg'); });
    });
  }

  /* ------------------------------------------------------------ hero: one payment, wallet to wallet */
  $$('[data-flow]').forEach(function (F) {
    var steps = $$('[data-fs]', F), n = steps.length, i = 0, tm = null, vis = false;
    function show(k) {
      i = k; F.setAttribute('data-step', k + 1);
      steps.forEach(function (s, j) { s.classList.toggle('on', j === k); s.classList.toggle('done', j < k); s.setAttribute('aria-current', j === k ? 'step' : 'false'); });
    }
    function tick() { show((i + 1) % n); tm = setTimeout(tick, i === n - 1 ? 3800 : 2700); }
    steps.forEach(function (s, j) { on(s, 'click', function () { clearTimeout(tm); show(j); if (!RM && vis) tm = setTimeout(tick, 5200); }); });
    show(0);
    if (RM) { F.classList.add('still'); return; }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        vis = es[0].isIntersecting; clearTimeout(tm);
        if (vis) tm = setTimeout(tick, 2400);
      }, { threshold: .35 }).observe(F);
    }
  });

  /* ------------------------------------------------------------ the 14 positions, filled one by one */
  $$('[data-mx]').forEach(function (M) {
    var seats = $$('.seat', M), bars = $$('[data-split] [data-part]', M), play = $('[data-mxplay]', M), cyc = $('.seg', M), tm = [], st = $('[data-k="mxs"]', M);
    var SPLIT = { c1: [2, 6, 2, 3, 1], cn: [2, 7, 1, 3, 1] };
    function setSplit(which) {
      var v = SPLIT[which];
      bars.forEach(function (b, j) { b.style.setProperty('--n', v[j]); var x = $('b', b); if (x) x.textContent = v[j]; });
      var lab = $$('[data-alt]', M); lab.forEach(function (l) { l.textContent = l.getAttribute(which === 'c1' ? 'data-c1' : 'data-cn'); });
      M.setAttribute('data-which', which);
    }
    function reset() { tm.forEach(clearTimeout); tm = []; seats.forEach(function (s) { s.classList.remove('on'); }); M.classList.remove('full'); }
    function run() {
      reset(); if (st) st.textContent = '0 of 14 positions filled';
      seats.forEach(function (s, j) {
        tm.push(setTimeout(function () { s.classList.add('on'); if (st) st.textContent = (j + 1) + ' of 14 positions filled'; if (j === seats.length - 1) { M.classList.add('full'); if (st) st.textContent = 'All 14 filled: the cycle completes'; } }, RM ? 0 : 160 + j * 230));
      });
    }
    on(play, 'click', run);
    if (cyc) seg(cyc, function (b) { setSplit(b.getAttribute('data-c')); });
    else setSplit('c1');
    if ('IntersectionObserver' in window && !RM) {
      var mio = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { run(); mio.disconnect(); } }, { threshold: .45 });
      mio.observe(M);
    } else { seats.forEach(function (s) { s.classList.add('on'); }); M.classList.add('full'); }
  });

  function seg(group, fn) {
    $$('button', group).forEach(function (b) {
      on(b, 'click', function () { $$('button', group).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); fn(b); });
    });
    var cur = $('[aria-pressed="true"]', group); if (cur) fn(cur);
  }

  /* ------------------------------------------------------------ fit check */
  var fit = $('[data-fitcheck]');
  if (fit) {
    var res = fit.parentNode.querySelector('.result'), total = $$('[data-fit]', fit).length;
    var score = function () {
      var boxes = $$('[data-fit]', fit), n = boxes.filter(function (x) { return x.checked; }).length;
      var afford = $('[data-fit="afford"]', fit).checked, msg;
      if (n === 0) msg = 'Tick the statements that are true for you.';
      else if (n === total) msg = 'A fair fit to keep learning and, if you choose, to start with the once-off 0.001 BTC. Next: the 14 positions.';
      else if (n >= 3) msg = 'Almost. What you left unticked is what to sort out first. There is no rush.';
      else msg = 'Not yet, and that is fine. Learning costs nothing. Keep watching and decide later, or not at all.';
      if (n > 0 && !afford) msg += ' Please never use money you need for rent, food or family.';
      $('[data-k="score"]', res).textContent = n + ' of ' + total;
      $('[data-k="msg"]', res).textContent = msg;
      res.classList.toggle('good', n === total);
    };
    $$('[data-fit]', fit).forEach(function (x) { on(x, 'change', score); });
  }

  /* ------------------------------------------------------------ glossary filter */
  var gq = $('[data-gfilter]');
  if (gq) {
    on(gq, 'input', function () {
      var q = gq.value.trim().toLowerCase(), shown = 0;
      $$('[data-term]').forEach(function (t) { var hit = !q || t.getAttribute('data-term').indexOf(q) > -1; t.hidden = !hit; if (hit) shown++; });
      $('[data-gempty]').hidden = shown > 0;
    });
  }

  /* ------------------------------------------------------------ live Bitcoin price (CoinGecko, shared by the tools) */
  var PRICE = null, PWAIT = [];
  function price(cb) {
    if (PRICE) return cb(PRICE);
    PWAIT.push(cb); if (PWAIT.length > 1) return;
    var ctl = window.AbortController ? new AbortController() : null, t = setTimeout(function () { ctl && ctl.abort(); }, 9000);
    fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,zar&include_last_updated_at=true', ctl ? { signal: ctl.signal } : {})
      .then(function (r) { if (!r.ok) throw 0; return r.json(); })
      .then(function (j) { clearTimeout(t); var b = j && j.bitcoin; if (!b || !b.usd || !b.zar) throw 0; PRICE = { usd: b.usd, zar: b.zar, at: b.last_updated_at ? b.last_updated_at * 1000 : Date.now(), live: true }; })
      .catch(function () { clearTimeout(t); PRICE = null; })
      .then(function () { var w = PWAIT; PWAIT = []; w.forEach(function (f) { f(PRICE); }); });
  }
  function when(ms) { return new Date(ms).toLocaleString('en-ZA', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }); }
  function rateNote(el, p) {
    if (!el) return;
    if (p) { el.className = 'ratebox ok'; el.innerHTML = '<span>Live price from CoinGecko: <b>$' + fmt(p.usd) + '</b> and <b>R' + fmt(p.zar) + '</b> per Bitcoin, updated ' + when(p.at) + '.</span>'; }
    else { el.className = 'ratebox bad'; el.innerHTML = "<span>Couldn't load the live price right now. Type today's Bitcoin price in rand below.</span>"; }
  }
  function num(v) { v = String(v || '').replace(/\s/g, '').replace(',', '.'); var x = parseFloat(v); return isFinite(x) ? x : NaN; }

  /* Bitcoin to Rand converter: BTC, USD and ZAR boxes stay in step */
  $$('[data-btc]').forEach(function (F) {
    var bx = $('[data-in="btc"]', F), ux = $('[data-in="usd"]', F), zx = $('[data-in="zar"]', F), px = $('[data-in="pz"]', F), st = $('[data-out="status"]', F), last = 'btc';
    function cur() { var pz = num(px.value); return { zar: pz, usd: PRICE && PRICE.zar ? pz * PRICE.usd / PRICE.zar : NaN }; }
    function go(from) {
      last = from || last; var p = cur(); if (!(p.zar > 0)) return;
      var btc = last === 'btc' ? num(bx.value) : last === 'usd' ? num(ux.value) / p.usd : num(zx.value) / p.zar;
      if (!(btc >= 0)) { ['btc', 'usd', 'zar'].forEach(function (k) { if (k !== last) $('[data-in="' + k + '"]', F).value = ''; }); return; }
      if (last !== 'btc') bx.value = +btc.toFixed(8);
      if (last !== 'usd') ux.value = isFinite(p.usd) ? (btc * p.usd).toFixed(2) : '';
      if (last !== 'zar') zx.value = (btc * p.zar).toFixed(2);
      var sat = $('[data-out="sats"]', F); if (sat) sat.textContent = fmt(Math.round(btc * 1e8)) + ' satoshis';
    }
    on(bx, 'input', function () { go('btc'); }); on(ux, 'input', function () { go('usd'); }); on(zx, 'input', function () { go('zar'); }); on(px, 'input', function () { go(); });
    $$('[data-amt]', F).forEach(function (b) { on(b, 'click', function () { bx.value = b.getAttribute('data-amt'); $$('[data-amt]', F).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); go('btc'); }); });
    on($('[data-reset]', F), 'click', function () { bx.value = '0.001'; go('btc'); bx.focus(); });
    function load() { st.className = 'ratebox'; st.innerHTML = '<span>Loading the live Bitcoin price…</span>'; PRICE = null; price(function (p) { rateNote(st, p); if (p) px.value = Math.round(p.zar); go(); }); }
    on($('[data-refresh]', F), 'click', load);
    if (!bx.value) bx.value = '0.001';
    load();
  });

  /* Slot calculator */
  $$('[data-slotcalc]').forEach(function (F) {
    var px = $('[data-in="pz"]', F), st = $('[data-out="status"]', F), slot = 1;
    function z(btc) { var pz = num(px.value); return pz > 0 ? 'R' + fmt(btc * pz) : '(type a price)'; }
    function go() {
      var p = +(0.001 * Math.pow(2, slot - 1)).toFixed(3);
      function put(k, v) { var e = $('[data-out="' + k + '"]', F); if (e) e.textContent = v; }
      put('slot', 'Slot ' + slot); put('price', p + ' BTC'); put('pricez', z(p));
      put('c1', +(6 * p).toFixed(3) + ' BTC'); put('c1z', z(6 * p));
      put('next', slot < 12 ? +(2 * p).toFixed(3) + ' BTC buys slot ' + (slot + 1) : 'Slot 12 is the top slot');
      put('cn', +(7 * p).toFixed(3) + ' BTC'); put('cnz', z(7 * p));
      put('paid', '14 members x ' + p + ' BTC = ' + +(14 * p).toFixed(3) + ' BTC');
      put('own', slot === 1 ? 'Yes: this is the once-off 0.001 BTC (plus network fees)' : 'No: auto entry, paid from your cycle at slot ' + (slot - 1));
    }
    seg($('.seg', F), function (b) { slot = +b.getAttribute('data-s'); go(); });
    on(px, 'input', go);
    function load() { st.className = 'ratebox'; st.innerHTML = '<span>Loading the live Bitcoin price…</span>'; PRICE = null; price(function (p) { rateNote(st, p); if (p) px.value = Math.round(p.zar); go(); }); }
    on($('[data-refresh]', F), 'click', load);
    load();
  });

  /* Halving countdown: live block height from mempool.space, 10 minutes per block on average */
  $$('[data-halving]').forEach(function (F) {
    var NEXT = 1050000, PREV = 840000, st = $('[data-out="status"]', F), h = 0, at = 0;
    function put(k, v) { var e = $('[data-out="' + k + '"]', F); if (e) e.textContent = v; }
    function paint() {
      if (!h) return;
      var left = NEXT - h, ms = left * 600000 - (Date.now() - at), eta = new Date(Date.now() + Math.max(0, ms));
      var dd = Math.max(0, Math.floor(ms / 864e5)), hh = Math.max(0, Math.floor(ms % 864e5 / 36e5)), mm = Math.max(0, Math.floor(ms % 36e5 / 6e4));
      put('h', fmt(h)); put('left', fmt(left)); put('d', fmt(dd)); put('hh', hh); put('mm', mm);
      put('eta', eta.toLocaleDateString('en-ZA', { month: 'long', year: 'numeric' }));
      F.style.setProperty('--ep', ((h - PREV) / (NEXT - PREV)).toFixed(4));
      put('ep', Math.round((h - PREV) / (NEXT - PREV) * 100) + '%');
    }
    function load() {
      st.className = 'ratebox'; st.innerHTML = '<span>Reading the live Bitcoin block height…</span>';
      fetch('https://mempool.space/api/blocks/tip/height').then(function (r) { if (!r.ok) throw 0; return r.text(); })
        .then(function (t) { h = parseInt(t, 10); if (!(h > PREV)) throw 0; at = Date.now(); st.className = 'ratebox ok'; st.innerHTML = '<span>Live block height from mempool.space: <b>' + fmt(h) + '</b>, read ' + when(at) + '.</span>'; paint(); })
        .catch(function () { st.className = 'ratebox bad'; st.innerHTML = "<span>Couldn't read the live block height right now. Showing an estimate from the average of one block every 10 minutes.</span>"; h = PREV + Math.floor((Date.now() - Date.UTC(2024, 3, 20, 0, 9)) / 600000); at = Date.now(); paint(); });
    }
    on($('[data-refresh]', F), 'click', load);
    load(); setInterval(paint, 30000);
  });

  /* ------------------------------------------------------------ order form (your own Bitcoin Wealth marketing website): builds a WhatsApp message */
  var OF = $('[data-order]');
  if (OF) {
    var slugIn = $('[name="slug"]', OF), prev = $('[data-out="addr"]', OF);
    function slugify(v) { return String(v || '').toLowerCase().replace(/[^a-z0-9]+/g, '').slice(0, 24); }
    function dom() { return 'bitcoinwealthpays.com/'; }      /* every copy lives at bitcoinwealthpays.com (MTG, 24 Nov 2026) */
    function paintAddr() { var s = slugify(slugIn.value) || 'yourname'; prev.textContent = dom() + s; }
    on(slugIn, 'input', paintAddr); paintAddr();
    on(OF, 'submit', function (e) {
      e.preventDefault();
      var bad = $$('[required]', OF).filter(function (x) { return x.type === 'radio' ? !$('[name="' + x.name + '"]:checked', OF) : !x.value.trim(); });
      $$('.field', OF).forEach(function (f) { f.classList.remove('err'); });
      var ref = $('[name="ref"]', OF);
      if (ref.value && !/^https?:\/\/\S+/.test(ref.value.trim())) bad.push(ref);
      if (bad.length) { bad.forEach(function (x) { var f = x.closest('.field'); if (f) f.classList.add('err'); }); bad[0].focus(); toast('Please complete the highlighted fields'); return; }
      function v(n) { var x = $('[name="' + n + '"]', OF); return x ? x.value.trim() : ''; }
      var pay = $('[name="pay"]:checked', OF);
      var lines = ['Hi MTG, I would like to order my own Bitcoin Wealth marketing website (R1,000 or $50 in USDT once-off, paid after it is built).', '',
        'Name: ' + v('name'), 'Page address: ' + dom() + (slugify(v('slug')) || '(to agree)'), 'My Bitcoin Wealth referral link: ' + v('ref'),
        'My WhatsApp number: ' + v('wa'), 'My WhatsApp group link: ' + (v('group') || 'none yet'),
        'TikTok: ' + (v('tiktok') || '-'), 'Facebook: ' + (v('fb') || '-'), 'YouTube: ' + (v('yt') || '-'), 'Telegram: ' + (v('tg') || '-'), 'Instagram: ' + (v('ig') || '-'),
        'VALR referral link: ' + (v('valr') || '-'), 'Binance referral link: ' + (v('bnb') || '-'),
        'How I would like to pay: ' + (pay ? pay.value : 'to agree on WhatsApp'), 'Notes: ' + (v('notes') || '-'), '',
        'I will send my profile photo here on WhatsApp.'];
      var url = BW.wa + '?text=' + encodeURIComponent(lines.join('\n'));
      var w = window.open(url, '_blank', 'noopener'); if (!w) location.href = url;
      var ok = $('[data-sent]'); if (ok) { ok.hidden = false; ok.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'center' }); }
    });
  }


  /* ------------------------------------------------------------ landing: live slot 1 price, gold dust */
  $$('[data-livep]').forEach(function (el) {
    price(function (p) { if (!p) return; $('[data-k="z"]', el).textContent = 'R' + fmt(p.zar * 0.001); el.hidden = false; el.title = 'Live price from CoinGecko, ' + when(p.at); });
  });
  $$('canvas[data-dust]').forEach(function (cv) {
    if (RM || !cv.getContext) return;
    var ctx = cv.getContext('2d'), W = 0, H = 0, DPR = Math.min(2, window.devicePixelRatio || 1), P = [], run = false;
    function size() { var r = cv.getBoundingClientRect(); W = r.width; H = r.height; cv.width = W * DPR; cv.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0); }
    function seed() { P = []; var n = Math.round(Math.min(70, W * H / 16000)); for (var i = 0; i < n; i++) P.push({ x: Math.random() * W, y: Math.random() * H, r: .6 + Math.random() * 1.8, v: .12 + Math.random() * .35, t: Math.random() * 6.3, g: Math.random() < .25 }); }
    function frame() {
      if (!run) return;
      ctx.clearRect(0, 0, W, H);
      P.forEach(function (q) {
        q.y -= q.v; q.x += Math.sin(q.t) * .15; q.t += .015;
        if (q.y < -6) { q.y = H + 6; q.x = Math.random() * W; }
        var a = .25 + .35 * (.5 + .5 * Math.sin(q.t * 2));
        ctx.fillStyle = q.g ? 'rgba(192,255,114,' + a * .6 + ')' : 'rgba(255,200,90,' + a + ')';
        ctx.beginPath(); ctx.arc(q.x, q.y, q.r, 0, 6.3); ctx.fill();
      });
      requestAnimationFrame(frame);
    }
    size(); seed(); on(window, 'resize', function () { size(); seed(); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { run = es[0].isIntersecting; if (run) requestAnimationFrame(frame); }).observe(cv);
    else { run = true; requestAnimationFrame(frame); }
  });
})();
