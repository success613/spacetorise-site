/* SPACE TO RISE — tienda de audios: catálogo, ficha, carrito, checkout */
(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const fmt = (n) => n === 0 ? 'Gratis' : '$ ' + n.toLocaleString('es-CO');
  const KEY = 'str-cart-v2';
  let products = [];
  const cart = { items: JSON.parse(localStorage.getItem(KEY) || '[]') };
  const save = () => localStorage.setItem(KEY, JSON.stringify(cart.items));
  const CATS = { 'cuerpo-mente': 'Trabaja en ti: sana tu cuerpo y tu mente', 'liberate': 'Libérate de todo lo que no quieres', 'miedos': 'Supera tus miedos para que nada te detenga', 'profesional': 'Desarrollo profesional', 'proyectos': 'Proyectos de vida', 'kids': 'Kids · Para niños' };
  const VQ = (() => { const s = document.querySelector('script[src*="shop.js"]'); const m = s && s.src.match(/v=([^&]+)/); return m ? '?v=' + m[1] : ''; })();
  const load = () => fetch('/assets/data/products.json' + VQ, { cache: 'no-cache' }).then(r => r.json()).then(l => { products = l; let ch = false; cart.items.forEach(i => { const p = l.find(x => x.id === i.id); if (p && p.price !== i.price) { i.price = p.price; ch = true; } }); if (ch) save(); return l; });

  /* ---------- carrito ---------- */
  const drawer = $('.drawer'), scrim = $('.scrim'), count = $('.cart-btn .count');
  function render() {
    if (count) { const n = cart.items.length; count.textContent = n; count.classList.toggle('on', n > 0); }
    if (!drawer) return;
    const box = $('.drawer__items', drawer), tot = $('.drawer__total b', drawer), foot = $('.drawer__foot', drawer);
    if (!cart.items.length) { box.innerHTML = '<div class="drawer__empty">Tu carrito está vacío.<br>Elige un audio y empieza hoy.</div>'; foot.style.display = 'none'; return; }
    foot.style.display = '';
    box.innerHTML = cart.items.map(i => `<div class="citem"><img src="${i.cover}" alt=""><div><h5>${i.name}</h5><span class="small muted">${fmt(i.price)}</span></div><button class="rm" data-rm="${i.id}">Quitar</button></div>`).join('');
    tot.textContent = fmt(cart.items.reduce((a, b) => a + b.price, 0));
    $$('[data-rm]', box).forEach(b => b.addEventListener('click', () => { cart.items = cart.items.filter(i => i.id !== b.dataset.rm); save(); render(); }));
  }
  function openCart(o) { drawer && drawer.classList.toggle('open', o); scrim && scrim.classList.toggle('open', o); document.body.classList.toggle('no-scroll', o); }
  $('.cart-btn') && $('.cart-btn').addEventListener('click', () => openCart(true));
  $('.drawer__close') && $('.drawer__close').addEventListener('click', () => openCart(false));
  scrim && scrim.addEventListener('click', () => { openCart(false); closeModal(); });
  function add(p) { if (!cart.items.find(i => i.id === p.id)) cart.items.push({ id: p.id, name: p.name, price: p.price, cover: p.cover }); save(); render(); window.strToast && strToast('Añadido al carrito'); }
  render();

  /* ---------- catálogo ---------- */
  const grid = $('[data-shop]');
  if (grid) load().then(() => {
    const order = ['cuerpo-mente', 'liberate', 'miedos', 'profesional', 'proyectos', 'kids'];
    grid.innerHTML = order.map(c => {
      const items = products.filter(p => p.category === c);
      const body = items.length ? `<div class="discs stagger">${items.map(card).join('')}</div>`
        : `<div class="notice"><strong style="font-weight:500">Muy pronto.</strong> Audios de autohipnosis para niños: autoestima, sueño tranquilo, exámenes y ansiedad. Mientras tanto, conoce las <a href="/kids/" style="text-decoration:underline">sesiones RTT Kids</a>.</div>`;
      return `<div class="fade catgroup" id="${c}" data-catgroup="${c}"><div class="cat-title"><h3>${CATS[c]}</h3><span>${items.length ? items.length + ' audios' : 'próximamente'}</span></div>${body}</div>`;
    }).join('');
    $$('.fade', grid).forEach((el, i) => setTimeout(() => el.classList.add('in'), 80 + i * 90));
    $$('[data-open]', grid).forEach(el => el.addEventListener('click', () => openModal(el.dataset.open)));
    $$('[data-add]', grid).forEach(b => b.addEventListener('click', (e) => { e.stopPropagation(); add(products.find(p => p.id === b.dataset.add)); b.classList.add('added'); b.textContent = 'Añadido'; }));
    const m = location.hash.match(/p=([\w-]+)/); if (m) openModal(m[1]);
    /* filtros por categoría */
    const chips = $$('[data-chips] .chip');
    const applyCat = (c) => { chips.forEach(x => x.classList.toggle('on', x.dataset.cat === c)); $$('[data-catgroup]', grid).forEach(g => { g.style.display = (c === 'all' || g.dataset.catgroup === c) ? '' : 'none'; }); typeof ScrollTrigger !== 'undefined' && setTimeout(() => ScrollTrigger.refresh(), 300); };
    chips.forEach(ch => ch.addEventListener('click', () => { applyCat(ch.dataset.cat); history.replaceState(null, '', '#' + (ch.dataset.cat === 'all' ? 'audios' : ch.dataset.cat)); }));
    const h = location.hash.replace('#', ''); if (h && CATS[h]) { applyCat(h); setTimeout(() => document.getElementById('audios') && document.getElementById('audios').scrollIntoView({ behavior: 'smooth' }), 400); }
    typeof ScrollTrigger !== 'undefined' && setTimeout(() => ScrollTrigger.refresh(), 600);
  });
  const card = (p) => `<article class="disc">
    <a class="disc__art" href="/shop/${p.slug}/"><img src="${p.cover}" alt="${p.name}" loading="lazy"><span class="disc__hole"></span></a>
    <h4><a href="/shop/${p.slug}/">${p.name}</a></h4>
    <div class="price">${fmt(p.price)}</div>
    <button class="add" data-add="${p.id}">Añadir</button>
  </article>`;

  /* ---------- botones "añadir" fuera del catálogo (fichas de producto) ---------- */
  if (!grid && $('[data-add]')) load().then(() => { $$('[data-add]').forEach(b => b.addEventListener('click', (e) => { e.preventDefault(); const p = products.find(x => x.id === b.dataset.add); if (!p) return; add(p); openCart(true); })); });

  /* ---------- ficha ---------- */
  const modal = $('.modal');
  function openModal(id) {
    const p = products.find(x => x.id === id); if (!p || !modal) return;
    $('.modal__img', modal).innerHTML = `<img src="${p.cover}" alt="">`;
    $('.modal__body', modal).innerHTML = `<span class="kicker">Audio de autohipnosis · 15–20 min</span><h3>${p.name}</h3><div class="desc"><p>${p.description}</p><p class="small muted">Escúchalo 21 días seguidos: es lo que tarda la mente en crear nuevos hábitos. Después del pago recibes un enlace mágico a tu correo para entrar a tu espacio privado y escucharlo desde cualquier dispositivo.</p></div><div class="price-tag">${fmt(p.price)}<small>COP</small></div><div style="display:flex;gap:12px;flex-wrap:wrap"><button class="pill solid" data-madd="${p.id}"><span>Añadir al carrito</span></button><a class="pill" href="/checkout/?p=${p.id}"><span>Comprar ahora</span></a></div>`;
    $('[data-madd]', modal).addEventListener('click', () => { add(p); closeModal(); openCart(true); });
    modal.classList.add('open'); scrim && scrim.classList.add('open'); document.body.classList.add('no-scroll');
    history.replaceState(null, '', '#p=' + p.id);
  }
  function closeModal() { if (!modal || !modal.classList.contains('open')) return; modal.classList.remove('open'); if (!(drawer && drawer.classList.contains('open'))) { scrim && scrim.classList.remove('open'); document.body.classList.remove('no-scroll'); } history.replaceState(null, '', location.pathname); }
  modal && $('.modal__close', modal).addEventListener('click', closeModal);
  addEventListener('keydown', (e) => { if (e.key === 'Escape') { closeModal(); openCart(false); } });

  /* ---------- checkout ---------- */
  const co = $('[data-checkout]');
  if (co) load().then(() => {
    const q = new URLSearchParams(location.search).get('p');
    if (q && !cart.items.find(i => i.id === q)) { const p = products.find(x => x.id === q); if (p) { cart.items.push({ id: p.id, name: p.name, price: p.price, cover: p.cover }); save(); render(); } }
    const list = $('[data-co-items]'), total = $('[data-co-total]'), form = $('form', co), out = $('[data-co-result]');
    const paint = () => { list.innerHTML = cart.items.length ? cart.items.map(i => `<div class="citem"><img src="${i.cover}" alt=""><div><h5>${i.name}</h5><span class="small muted">${fmt(i.price)}</span></div><button class="rm" data-rm="${i.id}">Quitar</button></div>`).join('') : '<div class="drawer__empty">No hay audios en tu pedido. <a href="/shop/" style="text-decoration:underline">Volver a la tienda</a></div>'; total.textContent = fmt(cart.items.reduce((a, b) => a + b.price, 0)); $$('[data-rm]', list).forEach(b => b.addEventListener('click', () => { cart.items = cart.items.filter(i => i.id !== b.dataset.rm); save(); render(); paint(); })); };
    paint();
    const fail = new URLSearchParams(location.search).get('status');
    if (fail === 'failure') out.innerHTML = '<div class="notice err">El pago no se completó. Puedes intentarlo de nuevo cuando quieras; tu pedido sigue aquí.</div>';
    form.addEventListener('submit', async (e) => {
      e.preventDefault(); if (!cart.items.length) return;
      const btn = $('button[type=submit]', form); btn.disabled = true; btn.querySelector('span').textContent = 'Preparando tu pago…';
      try {
        const r = await fetch('/api/checkout', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: form.email.value.trim(), items: cart.items.map(i => ({ id: i.id })) }) });
        const j = await r.json(); if (!r.ok) throw new Error(j.error || 'Error');
        if (j.pay_url) { sessionStorage.setItem('str_pending', j.reference); btn.querySelector('span').textContent = 'Redirigiendo a Mercado Pago…'; location.href = j.pay_url; return; }
        cart.items = []; save(); render();
        co.querySelector('[data-co-form]').style.display = 'none';
        out.innerHTML = `<div class="notice"><p style="margin:0 0 6px"><strong style="font-weight:500">Pedido ${j.reference} creado.</strong></p><p style="margin:0">Total: ${fmt(j.total)}. Confirma el pago por WhatsApp con Andrea. Apenas se confirme, recibirás en <b style="font-weight:500">${form.email.value.trim()}</b> tu enlace mágico para escuchar los audios en tu espacio privado.</p></div><div style="margin-top:22px;display:flex;gap:12px;flex-wrap:wrap"><a class="pill solid" href="${j.whatsapp}" target="_blank" rel="noopener"><span>Confirmar pago por WhatsApp</span></a><a class="pill" href="/mi-cuenta/"><span>Ir a mi cuenta</span></a></div>`;
        out.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } catch (err) { out.innerHTML = `<div class="notice err">${err.message}</div>`; btn.disabled = false; btn.querySelector('span').textContent = 'Pagar con Mercado Pago'; }
    });
  });

  /* ---------- gracias (vuelta de Mercado Pago) ---------- */
  const g = $('[data-gracias]');
  if (g) {
    const ref = new URLSearchParams(location.search).get('ref') || sessionStorage.getItem('str_pending') || '';
    const st = $('[data-g-status]', g), box = $('[data-g-box]', g);
    cart.items = []; save(); render();
    let tries = 0;
    const check = async () => {
      try {
        const r = await fetch('/api/checkout-status?ref=' + encodeURIComponent(ref)); const j = await r.json();
        if (j.status === 'paid') { st.textContent = 'Pago confirmado'; box.innerHTML = `<div class="notice"><p style="margin:0 0 6px"><strong style="font-weight:500">¡Gracias! Tu pago quedó confirmado.</strong></p><p style="margin:0">Te enviamos a <b style="font-weight:500">${j.email}</b> un enlace mágico para entrar a tu espacio privado y escuchar: ${j.items.join(', ')}. Si no lo ves en unos minutos, revisa la carpeta de spam o entra desde <a href="/mi-cuenta/" style="text-decoration:underline">Mi cuenta</a> con el mismo correo.</p></div><div style="margin-top:22px;display:flex;gap:12px;flex-wrap:wrap"><a class="pill solid" href="/mi-cuenta/"><span>Ir a mi cuenta</span></a><a class="pill" href="/shop/"><span>Seguir explorando</span></a></div>`; sessionStorage.removeItem('str_pending'); return; }
        if (++tries < 20) { st.textContent = 'Confirmando tu pago con Mercado Pago…'; setTimeout(check, 3000); }
        else { st.textContent = 'Pago en proceso'; box.innerHTML = `<div class="notice"><p style="margin:0">Mercado Pago aún no nos confirma el pago (referencia <b style="font-weight:500">${ref}</b>). En cuanto lo apruebe, recibirás tu enlace mágico por correo. Si pagaste por PSE o efectivo, puede tardar un poco más. ¿Dudas? Escríbenos por WhatsApp.</p></div><div style="margin-top:22px;display:flex;gap:12px;flex-wrap:wrap"><a class="pill" href="/mi-cuenta/"><span>Mi cuenta</span></a></div>`; }
      } catch (e) { st.textContent = 'No pudimos verificar el pago'; box.innerHTML = `<div class="notice err">${e.message}</div>`; }
    };
    if (ref) check(); else { st.textContent = 'Sin pedido'; box.innerHTML = '<div class="notice">No encontramos una referencia de pedido. <a href="/shop/" style="text-decoration:underline">Volver a la tienda</a></div>'; }
  }
})();
