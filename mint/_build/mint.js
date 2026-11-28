/* mtgtribe.com/mint page script: menu, the section you are in, copy buttons, Up and Down, reveal, 3D tilt, founder call moments. */
(function () {
  'use strict';
  var d = document, w = window, html = d.documentElement;
  var RM = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, r) { return (r || d).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); }

  /* menu (phones) */
  var mb = $('.menu-b');
  function menu(open) { html.classList.toggle('menu-open', open); if (mb) mb.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  if (mb) mb.addEventListener('click', function () { menu(!html.classList.contains('menu-open')); });
  $$('.drop a').forEach(function (a) { a.addEventListener('click', function () { menu(false); }); });
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape') menu(false); });

  /* the section you are in lights up in the top menu and the bottom bar */
  var secs = $$('main section[id]');
  var links = $$('.nav a[href^="#"], .qbar a[href^="#"], .drop a[href^="#"]');
  function spy() {
    var y = (w.scrollY || 0) + (w.innerHeight * 0.35), cur = 'top';
    secs.forEach(function (s) { if (s.offsetTop <= y) cur = s.id; });
    links.forEach(function (a) {
      var h = a.getAttribute('href').slice(1);
      var on = h === cur || (a.getAttribute('data-also') || '').split(' ').indexOf(cur) > -1;
      a.classList.toggle('on', on);
      if (on) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
  }

  /* Up and Down: Up goes to the top, Down to the next section, then the footer */
  var up = $('[data-up]'), dn = $('[data-down]');
  function stops() { return secs.map(function (s) { return s.getBoundingClientRect().top + w.scrollY; }).concat([$('.foot').getBoundingClientRect().top + w.scrollY]); }
  function hdr() { var t = $('.top'); return t ? t.getBoundingClientRect().height : 64; }
  function go(y) { w.scrollTo({ top: Math.max(0, y), behavior: RM ? 'auto' : 'smooth' }); }
  if (up) up.addEventListener('click', function () { go(0); });
  if (dn) dn.addEventListener('click', function () {
    var now = w.scrollY + hdr() + 12, list = stops();
    for (var i = 0; i < list.length; i++) if (list[i] > now) return go(list[i] - hdr() - 6);
    go(html.scrollHeight);
  });
  function ud() {
    var y = w.scrollY || 0, max = html.scrollHeight - w.innerHeight, long = html.scrollHeight > w.innerHeight * 2.2;
    if (up) up.classList.toggle('on', long && y > w.innerHeight * 0.6);
    if (dn) dn.classList.toggle('on', long && y < max - 40);
  }
  var tick = false;
  function onScroll() { if (tick) return; tick = true; requestAnimationFrame(function () { tick = false; spy(); ud(); }); }
  w.addEventListener('scroll', onScroll, { passive: true });
  w.addEventListener('resize', onScroll);
  spy(); ud();

  /* copy buttons (the contract address, MTG's invite link) */
  var toast = $('#toast'), tt;
  function say(msg) { if (!toast) return; toast.textContent = msg; toast.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { toast.classList.remove('on'); }, 2600); }
  function fallback(txt) {
    var t = d.createElement('textarea'); t.value = txt; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0'; d.body.appendChild(t); t.select();
    var ok = false; try { ok = d.execCommand('copy'); } catch (e) {} d.body.removeChild(t); return ok;
  }
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var txt = b.getAttribute('data-copy'), msg = b.getAttribute('data-copied') || 'Copied';
      function done(ok) {
        say(ok ? msg : 'Press and hold the text to copy it');
        if (ok) { var l = $('.lbl', b); if (l) { var was = l.textContent; l.textContent = 'Copied'; b.classList.add('done'); setTimeout(function () { l.textContent = was; b.classList.remove('done'); }, 2000); } }
      }
      if (navigator.clipboard && w.isSecureContext) navigator.clipboard.writeText(txt).then(function () { done(true); }, function () { done(fallback(txt)); });
      else done(fallback(txt));
    });
  });

  /* reveal on scroll */
  if ('IntersectionObserver' in w && !RM) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    $$('.rv').forEach(function (el) { io.observe(el); });
  }

  /* 3D tilt on cards and the hero (mouse and pen only) */
  if (!RM && w.matchMedia && w.matchMedia('(hover:hover) and (pointer:fine)').matches) {
    $$('[data-tilt]').forEach(function (el) {
      var max = parseFloat(el.getAttribute('data-tilt')) || 6, inner = el.querySelector('.tilt') || el;
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        inner.style.transform = 'rotateX(' + (-y * max).toFixed(2) + 'deg) rotateY(' + (x * max).toFixed(2) + 'deg)';
      });
      el.addEventListener('pointerleave', function () { inner.style.transform = ''; });
    });
  }

  /* founder call: each moment starts the video in the laptop at that moment (on YouTube when the page cannot embed it) */
  $$('[data-at]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var pl = $('#founder-video .pl'), at = parseInt(a.getAttribute('data-at'), 10);
      if (!pl || w.MTG_PREVIEW) return;                         // the link itself opens YouTube at that moment
      e.preventDefault();
      function seek() { try { pl._yt.seekTo(at, true); pl._yt.playVideo(); return true; } catch (x) { return false; } }
      if (pl._yt && typeof pl._yt.seekTo === 'function' && seek()) return pl.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'center' });
      var b = $('.vplay', pl); if (b) b.click();
      var n = 0, t = setInterval(function () { if ((pl._yt && typeof pl._yt.seekTo === 'function' && typeof pl._yt.getPlayerState === 'function' && seek()) || ++n > 60) clearInterval(t); }, 200);
    });
  });
})();
