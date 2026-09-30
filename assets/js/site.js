/* =====================================================================
   SPACE TO RISE — motor de experiencia
   GSAP + ScrollTrigger + Lenis. Lenguaje: una gota cae en agua quieta.
   ===================================================================== */
(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  const hasGsap = typeof gsap !== 'undefined';
  if (hasGsap && typeof ScrollTrigger !== 'undefined') gsap.registerPlugin(ScrollTrigger);

  /* ---------- Smooth scroll (Lenis) ---------- */
  let lenis = null;
  if (!reduce && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ lerp: 0.085, wheelMultiplier: 0.95, smoothWheel: true });
    lenis.on('scroll', () => hasGsap && ScrollTrigger.update());
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  const scrollTo = (y) => lenis ? lenis.scrollTo(y) : window.scrollTo({ top: y, behavior: 'smooth' });

  /* ---------- Loader: gota → anillos → logo ---------- */
  const loader = $('.loader');
  const seen = sessionStorage.getItem('str-seen');
  function buildRings() {
    const svg = $('.loader__rings'); if (!svg) return [];
    const cols = ['#D9A38F', '#EFBEB6', '#EAD7C0', '#B9D7D0', '#AFCCD1', '#92ADA4', '#7A6E5D'];
    const rings = [];
    for (let i = 0; i < 7; i++) {
      const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      c.setAttribute('cx', 100); c.setAttribute('cy', 100); c.setAttribute('r', 14 + i * 12);
      c.setAttribute('stroke', cols[i]); svg.appendChild(c); rings.push(c);
    }
    return rings;
  }
  function endLoader(fast) {
    document.body.classList.remove('no-scroll');
    if (!loader) return;
    if (fast || reduce || !hasGsap) { loader.style.display = 'none'; heroIn(); return; }
    gsap.to(loader, { clipPath: 'circle(0% at 50% 50%)', duration: 1.2, ease: 'expo.inOut', onComplete: () => { loader.style.display = 'none'; } });
    setTimeout(heroIn, 350);
  }
  function heroIn() {
    $$('.hero .lines').forEach(l => l.classList.add('in'));
    $$('.hero .fade').forEach(f => f.classList.add('in'));
    const m = $('.hero__media video, .hero__media img');
    if (m && hasGsap) gsap.fromTo(m, { scale: 1.12 }, { scale: 1.04, duration: 3.2, ease: 'expo.out' });
  }
  if (loader) {
    document.body.classList.add('no-scroll');
    loader.style.clipPath = 'circle(150% at 50% 50%)';
    if (seen || reduce || !hasGsap) { setTimeout(() => endLoader(true), 60); }
    else {
      const rings = buildRings();
      const tl = gsap.timeline({ defaults: { ease: 'power2.out' } });
      tl.to('.loader__drop', { opacity: 1, duration: .2 }, 0)
        .fromTo('.loader__drop', { y: -40 }, { y: 'min(35vmin,210px)', duration: .9, ease: 'power2.in' }, 0)
        .to('.loader__drop', { scaleY: .3, scaleX: 1.6, opacity: 0, duration: .25 }, .9)
        .to(rings, { opacity: 1, scale: 1, duration: 1.6, ease: 'expo.out', stagger: .07 }, .95)
        .to('.loader__heart', { opacity: 1, scale: 1, duration: .8, ease: 'back.out(2)' }, 1.5)
        .to('.loader__word', { opacity: 1, y: -8, duration: .9 }, 1.7)
        .add(() => { sessionStorage.setItem('str-seen', '1'); endLoader(false); }, 3.2);
    }
  } else heroIn();

  /* ---------- Cursor anillo ---------- */
  if (fine && !reduce) {
    const cur = document.createElement('div'); cur.className = 'cursor'; document.body.appendChild(cur);
    let x = innerWidth / 2, y = innerHeight / 2, cx = x, cy = y;
    addEventListener('mousemove', (e) => { x = e.clientX; y = e.clientY; cur.classList.add('on'); }, { passive: true });
    addEventListener('mouseleave', () => cur.classList.remove('on'));
    (function loop() { cx += (x - cx) * .18; cy += (y - cy) * .18; cur.style.transform = `translate(${cx}px,${cy}px) translate(-50%,-50%)`; requestAnimationFrame(loop); })();
    document.addEventListener('mouseover', (e) => { cur.classList.toggle('hover', !!e.target.closest('a,button,[data-open],.disc,.panel')); });
    // pequeña onda al hacer clic
    document.addEventListener('click', (e) => {
      if (e.target.closest('input,textarea')) return;
      const r = document.createElement('span');
      r.style.cssText = `position:fixed;left:${e.clientX}px;top:${e.clientY}px;width:10px;height:10px;border:1px solid #575756;border-radius:50%;transform:translate(-50%,-50%);pointer-events:none;z-index:1499;opacity:.7`;
      document.body.appendChild(r);
      gsap.to(r, { width: 90, height: 90, opacity: 0, duration: .9, ease: 'expo.out', onComplete: () => r.remove() });
    });
  }

  /* ---------- Header: se oculta al bajar, vuelve al subir ---------- */
  const header = $('.header');
  let lastY = 0;
  const onScroll = () => {
    const y = scrollY;
    if (header) { header.classList.toggle('hidden', y > lastY && y > 140 && !document.body.classList.contains('menu-open')); }
    lastY = y;
    const p = $('.progress'); if (p) p.classList.toggle('on', y > innerHeight * .6);
  };
  addEventListener('scroll', onScroll, { passive: true });
  // header oscuro sobre fondos oscuros
  if (header && hasGsap) {
    $$('[data-dark]').forEach(sec => ScrollTrigger.create({ trigger: sec, start: 'top 60px', end: 'bottom 60px', onToggle: (s) => { header.classList.toggle('dark', s.isActive); document.body.classList.toggle('on-dark', s.isActive); } }));
  }
  const menu = $('.menu'), mbtn = $('.menu-btn'), mclose = $('.menu-close');
  const toggleMenu = (o) => { menu && menu.classList.toggle('open', o); document.body.classList.toggle('menu-open', o); document.body.classList.toggle('no-scroll', o); };
  mbtn && mbtn.addEventListener('click', () => toggleMenu(true));
  mclose && mclose.addEventListener('click', () => toggleMenu(false));
  const here = location.pathname.replace(/\/+$/, '') || '/';
  $$('.nav a, .menu a').forEach(a => { const p = (a.getAttribute('href') || '').replace(/\/+$/, '') || '/'; if (p === here) a.setAttribute('aria-current', 'page'); });

  /* ---------- Espiral de progreso ---------- */
  const prog = $('.progress path.fill');
  if (prog) {
    const len = prog.getTotalLength(); prog.style.strokeDasharray = len; prog.style.strokeDashoffset = len;
    addEventListener('scroll', () => { const p = scrollY / (document.body.scrollHeight - innerHeight); prog.style.strokeDashoffset = len * (1 - Math.min(1, p)); }, { passive: true });
  }

  /* ---------- Split de líneas (para .lines) ---------- */
  $$('.lines').forEach(el => {
    if (el.dataset.split) return; el.dataset.split = '1';
    const html = (innerWidth < 700 ? el.innerHTML.replace(/<br class="d">/g, ' ') : el.innerHTML).split(/<br[^>]*>/i);
    el.innerHTML = html.map(l => `<span class="line"><span>${l.trim()}</span></span>`).join('');
  });

  /* ---------- Revelados ---------- */
  const io = new IntersectionObserver((es) => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .2, rootMargin: '0px 0px -8% 0px' });
  $$('.lines:not(.hero .lines), .fade:not(.hero .fade), .media').forEach(el => io.observe(el));

  /* ---------- Parallax suave en medios marcados ---------- */
  if (hasGsap && !reduce) {
    $$('[data-parallax]').forEach(el => {
      const amt = parseFloat(el.dataset.parallax) || 12;
      gsap.fromTo(el, { yPercent: -amt }, { yPercent: amt, ease: 'none', scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
  }

  /* ---------- Manifiesto (frases sobre video) ---------- */
  const man = $('.manifesto');
  if (man && hasGsap) {
    const phrases = $$('.manifesto__phrase', man); const idx = $('.manifesto__idx', man);
    const vid = $('video', man);
    gsap.set(phrases, { opacity: 0, y: 30 });
    const tl = gsap.timeline({ scrollTrigger: { trigger: man, start: 'top top', end: 'bottom bottom', scrub: .6,
      onUpdate: (s) => { const i = Math.min(phrases.length - 1, Math.floor(s.progress * phrases.length)); idx && (idx.textContent = `${i + 1} / ${phrases.length}`); man.classList.toggle('color', s.progress > .78); },
      onToggle: (s) => { if (vid) { s.isActive ? vid.play().catch(() => {}) : vid.pause(); } } } });
    phrases.forEach((p, i) => {
      tl.to(p, { opacity: 1, y: 0, duration: 1, ease: 'power2.out' }, i * 2)
        .to(p, { opacity: 0, y: -30, duration: 1, ease: 'power2.in' }, i * 2 + 1.2);
    });
    // la última se queda
    tl.to(phrases[phrases.length - 1], { opacity: 1, y: 0, duration: .01 }, phrases.length * 2 - .8);
  }

  /* ---------- Servicios en horizontal ---------- */
  const hs = $('.hscroll');
  if (hs && hasGsap && innerWidth > 900) {
    const track = $('.hscroll__track', hs);
    const dist = () => track.scrollWidth - innerWidth;
    gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: hs, start: 'top top', end: () => '+=' + dist(), pin: true, scrub: .8, invalidateOnRefresh: true, anticipatePin: 1,
      onUpdate: (s) => { const panels = $$('.panel:not(.intro)', hs); const i = Math.round(s.progress * (panels.length - 1)); panels.forEach((p, k) => p.classList.toggle('active', k === i)); } } });
  }

  /* ---------- Video Andrea (escala con scroll) ---------- */
  const reel = $('.reel');
  if (reel && hasGsap) {
    const fr = $('.reel__frame', reel), vid = $('video', reel), cap = $('.reel__caption', reel);
    gsap.fromTo(fr, { scale: .55, borderRadius: 24 }, { scale: 1, borderRadius: 0, ease: 'none', scrollTrigger: { trigger: reel, start: 'top top', end: '+=70%', scrub: .5,
      onUpdate: (s) => { cap && (cap.style.opacity = s.progress > .5 ? 0 : 1); if (vid) { if (s.progress > .4 && vid.paused && !reel.dataset.user) { vid.muted = true; vid.play().catch(() => {}); } } },
      onLeaveBack: () => { if (vid && !reel.dataset.user) vid.pause(); } } });
    const play = $('.reel__play', reel);
    play && play.addEventListener('click', () => { reel.dataset.user = '1'; vid.muted = false; vid.controls = true; vid.currentTime = 0; vid.play(); reel.classList.add('playing'); });
  }

  /* ---------- Baraja de testimonios ---------- */
  const deck = $('.deck');
  if (deck && hasGsap) {
    const cards = $$('.deck__card', deck);
    cards.forEach((c, i) => gsap.set(c, { y: 40 + i * 6, scale: 1 - i * .04, opacity: i < 3 ? 1 - i * .25 : 0, zIndex: cards.length - i, rotate: (i % 2 ? 1 : -1) * i * .6 }));
    const tl = gsap.timeline({ scrollTrigger: { trigger: deck, start: 'top top', end: 'bottom bottom', scrub: .5 } });
    cards.forEach((c, i) => {
      if (i === cards.length - 1) return;
      tl.to(c, { y: -140, rotate: (i % 2 ? -1 : 1) * 8, opacity: 0, duration: 1, ease: 'power1.in' }, i)
        .to(cards.slice(i + 1), { y: (k) => 40 + k * 6, scale: (k) => 1 - k * .04, opacity: (k) => k < 3 ? 1 - k * .25 : 0, rotate: (k) => ((i + 1 + k) % 2 ? 1 : -1) * k * .6, duration: 1 }, i);
    });
  }

  /* ---------- Acordeón ---------- */
  $$('.acc__item').forEach(item => $('.acc__q', item).addEventListener('click', () => {
    const open = item.classList.contains('open');
    $$('.acc__item.open', item.parentElement).forEach(i => i.classList.remove('open'));
    if (!open) item.classList.add('open');
    setTimeout(() => hasGsap && ScrollTrigger.refresh(), 900);
  }));

  /* ---------- Transición de página (anillo desde el clic) ---------- */
  const wipe = $('.wipe');
  if (wipe && !reduce) {
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href]'); if (!a) return;
      const href = a.getAttribute('href');
      if (!href || href.startsWith('#') || /^(https?:|mailto:|tel:)/.test(href) || a.target === '_blank' || a.hasAttribute('download') || e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      wipe.style.setProperty('--x', e.clientX + 'px'); wipe.style.setProperty('--y', e.clientY + 'px');
      wipe.classList.add('on');
      setTimeout(() => location.href = href, 750);
    });
    addEventListener('pageshow', (e) => { if (e.persisted) wipe.classList.remove('on'); });
  }

  /* ---------- Anclas suaves ---------- */
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', (e) => { const t = $(a.getAttribute('href')); if (t) { e.preventDefault(); scrollTo(t); } }));

  /* ---------- WhatsApp asoma ---------- */
  const wa = $('.wa'); if (wa) setTimeout(() => { wa.classList.add('peek'); setTimeout(() => wa.classList.remove('peek'), 3000); }, 6000);

  /* ---------- Toast ---------- */
  window.strToast = (m) => { let t = $('.toast'); if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); } t.textContent = m; t.classList.add('show'); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 2400); };

  /* ---------- Videos: solo se reproducen en pantalla ---------- */
  $$('video[data-lazy]').forEach(v => {
    const o = new IntersectionObserver((es) => es.forEach(e => { if (e.isIntersecting) { v.play().catch(() => {}); } else v.pause(); }), { threshold: .1 });
    o.observe(v);
  });

  addEventListener('load', () => hasGsap && ScrollTrigger.refresh());

  /* ---------- Formularios: agenda / empresas / newsletter → /api/lead ---------- */
  const sendLead = async (form, kind, out) => {
    const btn = form.querySelector('button[type=submit]'); const data = Object.fromEntries(new FormData(form).entries()); data.kind = kind;
    btn.disabled = true;
    try {
      const r = await fetch('/api/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
      const jr = await r.json(); if (!r.ok) throw new Error(jr.error || 'Error');
      return true;
    } catch (err) { if (out) out.innerHTML = `<div class="notice err">${err.message}</div>`; btn.disabled = false; return false; }
  };
  $$('form[data-lead]').forEach(form => form.addEventListener('submit', async (e) => {
    e.preventDefault(); const out = form.querySelector('[data-lead-out]');
    if (await sendLead(form, form.dataset.lead, out)) { form.querySelectorAll('.row, button, .pill').forEach(el => el.style.display = 'none'); out.innerHTML = '<div class="notice"><strong style="font-weight:500">¡Recibido!</strong> Gracias por escribirme. Te contacto muy pronto para agendar nuestra conversación.</div>'; }
  }));
  $$('form[data-newsletter]').forEach(form => form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (await sendLead(form, 'newsletter', null)) { form.innerHTML = '<p class="small" style="margin:0;color:var(--ivory)">¡Gracias! Revisa tu correo: pronto llega tu regalo de bienvenida.</p>'; } else window.strToast && strToast('No pudimos suscribirte. Inténtalo de nuevo.');
  }));
})();