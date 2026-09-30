/* SPACE TO RISE — portal privado: enlace mágico, mis audios, panel de Andrea */
(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  if (typeof supabase === 'undefined') return;
  const sb = supabase.createClient(window.STR_SUPABASE_URL, window.STR_SUPABASE_KEY);
  const fmtTime = (s) => { s = Math.floor(s || 0); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; };
  const notice = (el, msg, err) => { el.innerHTML = `<div class="notice${err ? ' err' : ''}">${msg}</div>`; };

  /* ---------- /mi-cuenta: enlace mágico ---------- */
  const login = $('[data-login]');
  if (login) {
    const form = $('form', login), out = $('[data-login-out]');
    sb.auth.getSession().then(({ data }) => { if (data.session) location.replace('/mis-audios/'); });
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = form.email.value.trim(); const btn = $('button[type=submit]', form); btn.disabled = true;
      const { error } = await sb.auth.signInWithOtp({ email, options: { emailRedirectTo: location.origin + '/mis-audios/' } });
      btn.disabled = false;
      if (error) notice(out, 'No pudimos enviar el enlace: ' + error.message, true);
      else { form.style.display = 'none'; notice(out, `<strong style="font-weight:500">Revisa tu correo.</strong> Te enviamos un enlace mágico a <b style="font-weight:500">${email}</b>. Ábrelo desde este mismo dispositivo para entrar a tu espacio.`); }
    });
  }

  /* ---------- /mis-audios ---------- */
  const my = $('[data-my-audios]');
  if (my) {
    const list = $('[data-tracks]', my), who = $('[data-who]', my), out = $('[data-my-out]', my);
    const player = $('.player'), audio = new Audio(); let current = null;
    async function init() {
      // Supabase deja el token en el hash (#access_token=...) al volver del enlace mágico
      const { data: { session } } = await sb.auth.getSession();
      if (!session) { await new Promise(r => setTimeout(r, 900)); const s2 = await sb.auth.getSession(); if (!s2.data.session) { location.replace('/mi-cuenta/'); return; } }
      const { data: { user } } = await sb.auth.getUser();
      who.textContent = user.email;
      const { data: purchases, error } = await sb.from('purchases').select('product_id,created_at').eq('status', 'paid');
      if (error) return notice(out, error.message, true);
      const products = await fetch('/assets/data/products.json').then(r => r.json());
      const mine = (purchases || []).map(p => products.find(x => x.id === p.product_id)).filter(Boolean);
      if (!mine.length) { list.innerHTML = ''; return notice(out, 'Aún no hay audios en tu cuenta. Si ya pagaste, tu acceso se activa apenas Andrea confirme el pago. <a href="/shop/" style="text-decoration:underline">Ver audios</a>.'); }
      list.innerHTML = mine.map(p => `<div class="track" data-id="${p.id}"><img src="${p.cover}" alt=""><div><h4>${p.name}</h4><p class="small muted" style="margin:0">Escúchalo 21 días seguidos, en un lugar tranquilo y con audífonos.</p></div><div style="display:flex;gap:10px;align-items:center"><button class="play" data-play="${p.id}" aria-label="Escuchar"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></button><a class="small muted" data-dl="${p.id}" href="#" style="text-decoration:underline">Descargar</a></div></div>`).join('');
      $$('[data-play]', list).forEach(b => b.addEventListener('click', () => play(b.dataset.play, session)));
      $$('[data-dl]', list).forEach(a => a.addEventListener('click', async (e) => { e.preventDefault(); const u = await signed(a.dataset.dl); if (u) { const l = document.createElement('a'); l.href = u.url; l.download = u.name + '.mp3'; l.target = '_blank'; document.body.appendChild(l); l.click(); l.remove(); } }));
    }
    async function signed(id) {
      const { data: { session } } = await sb.auth.getSession();
      const r = await fetch('/api/audio-url?product=' + encodeURIComponent(id), { headers: { Authorization: 'Bearer ' + session.access_token } });
      const j = await r.json(); if (!r.ok) { notice(out, j.error || 'Error', true); return null; } return j;
    }
    async function play(id) {
      const btn = $(`[data-play="${id}"]`);
      if (current === id) { audio.paused ? audio.play() : audio.pause(); return; }
      const u = await signed(id); if (!u) return;
      current = id; audio.src = u.url; audio.play();
      $('.player .title').textContent = u.name; player.classList.add('on');
      $$('.track').forEach(t => t.classList.toggle('playing', t.dataset.id === id));
    }
    audio.addEventListener('timeupdate', () => { const p = audio.duration ? audio.currentTime / audio.duration : 0; $('.player .bar i').style.width = (p * 100) + '%'; $('.player .time').textContent = fmtTime(audio.currentTime) + ' / ' + fmtTime(audio.duration); });
    $('.player .bar') && $('.player .bar').addEventListener('click', (e) => { const r = e.currentTarget.getBoundingClientRect(); audio.currentTime = ((e.clientX - r.left) / r.width) * (audio.duration || 0); });
    $('.player .toggle') && $('.player .toggle').addEventListener('click', () => audio.paused ? audio.play() : audio.pause());
    $('[data-logout]') && $('[data-logout]').addEventListener('click', async () => { await sb.auth.signOut(); location.href = '/'; });
    init();
  }

  /* ---------- /admin: panel de Andrea ---------- */
  const adm = $('[data-admin]');
  if (adm) {
    const out = $('[data-admin-out]', adm), form = $('form', adm), tbl = $('[data-admin-orders]', adm), prodSel = $('[data-admin-products]', adm);
    (async () => {
      const { data: { session } } = await sb.auth.getSession();
      if (!session) { await new Promise(r => setTimeout(r, 900)); if (!(await sb.auth.getSession()).data.session) { location.replace('/mi-cuenta/?next=admin'); return; } }
      const tok = (await sb.auth.getSession()).data.session.access_token;
      const products = await fetch('/assets/data/products.json').then(r => r.json());
      prodSel.innerHTML = products.map(p => `<label style="display:flex;gap:10px;align-items:center;padding:6px 0"><input type="checkbox" name="pid" value="${p.id}"> ${p.name}</label>`).join('');
      const r = await fetch('/api/admin/orders', { headers: { Authorization: 'Bearer ' + tok } }); const j = await r.json();
      if (!r.ok) return notice(out, j.error, true);
      tbl.innerHTML = j.orders.length ? j.orders.map(o => `<div class="track" style="grid-template-columns:1fr auto"><div><h4 style="font-size:1rem">${o.reference} · ${o.email}</h4><p class="small muted" style="margin:0">${o.items.map(i => i.name).join(', ')} · $ ${o.total.toLocaleString('es-CO')} · <b style="font-weight:500">${o.status === 'paid' ? 'pagado' : 'pendiente'}</b> · ${new Date(o.created_at).toLocaleDateString('es-CO')}</p></div>${o.status !== 'paid' ? `<button class="pill" data-mark="${o.reference}" data-email="${o.email}" data-ids="${o.items.map(i => i.id).join(',')}"><span>Marcar pagado</span></button>` : ''}</div>`).join('') : '<p class="muted">Aún no hay pedidos.</p>';
      const lt = $('[data-admin-leads]', adm), K = { agenda: 'Cita', empresa: 'Empresa', newsletter: 'Newsletter' };
      if (lt) lt.innerHTML = (j.leads || []).length ? j.leads.map(l => `<div class="track" style="grid-template-columns:1fr"><div><h4 style="font-size:1rem">${K[l.kind] || l.kind} · ${l.name || ''} <a href="mailto:${l.email}" style="text-decoration:underline;font-weight:300">${l.email}</a></h4><p class="small muted" style="margin:0">${[l.company, l.phone, l.city, l.service].filter(Boolean).join(' · ')}${l.message ? ' · “' + l.message + '”' : ''} · ${new Date(l.created_at).toLocaleDateString('es-CO')}</p></div></div>`).join('') : '<p class="muted">Aún no hay solicitudes.</p>';
      $$('[data-mark]', tbl).forEach(b => b.addEventListener('click', () => grant(b.dataset.email, b.dataset.ids.split(','), b.dataset.mark, tok)));
      form.addEventListener('submit', (e) => { e.preventDefault(); const ids = $$('input[name=pid]:checked', form).map(i => i.value); grant(form.email.value.trim(), ids, null, tok); });
    })();
    async function grant(email, ids, reference, tok) {
      if (!email || !ids.length) return notice(out, 'Indica el correo y al menos un audio.', true);
      const r = await fetch('/api/admin/grant', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + tok }, body: JSON.stringify({ email, product_ids: ids, reference, send_link: true }) });
      const j = await r.json();
      if (!r.ok) return notice(out, j.error, true);
      notice(out, `Acceso otorgado a <b style="font-weight:500">${email}</b> (${j.granted} audio${j.granted > 1 ? 's' : ''}). ${j.link_sent ? 'Le enviamos su enlace mágico.' : 'No se pudo enviar el enlace; puede pedirlo en /mi-cuenta.'}`);
      setTimeout(() => location.reload(), 2500);
    }
  }
})();
