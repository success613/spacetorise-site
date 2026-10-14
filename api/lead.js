import { admin, json, readBody } from './_lib.js';
/** Recibe formularios del sitio: agenda (llamada inicial), empresas (propuesta) y newsletter. */
export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Método no permitido' });
  let b; try { b = readBody(req); } catch { return json(res, 400, { error: 'JSON inválido' }); }
  const kind = ['agenda', 'empresa', 'newsletter'].includes(b.kind) ? b.kind : null;
  const email = String(b.email || '').trim().toLowerCase();
  if (!kind || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json(res, 400, { error: 'Revisa el correo.' });
  if (b.website) return json(res, 200, { ok: true }); // honeypot
  if (kind !== 'newsletter' && !/^\+\d{1,3}[\d .-]{6,16}$/.test(String(b.phone || '').trim())) return json(res, 400, { error: 'Escribe tu número con el indicativo del país (ej. +57 300 123 4567).' });
  const row = {
    kind, email,
    name: String(b.name || '').slice(0, 120) || null,
    phone: String(b.phone || '').slice(0, 40) || null,
    company: String(b.company || '').slice(0, 120) || null,
    city: String(b.city || '').slice(0, 120) || null,
    service: String(b.service || '').slice(0, 80) || null,
    message: String(b.message || '').slice(0, 2000) || null,
    source: String(req.headers.referer || '').slice(0, 200) || null,
  };
  const { error } = await admin().from('leads').insert(row);
  if (error) return json(res, 500, { error: 'No pudimos guardar tu solicitud. Escríbenos por WhatsApp.' });
  // Aviso por correo (FormSubmit) a Andrea / Clicalto. NOTIFY_EMAILS separados por coma.
  const to = (process.env.NOTIFY_EMAILS || 'success@thrust-x.com').split(',').map(s => s.trim()).filter(Boolean);
  const labels = { agenda: 'Nueva solicitud de cita', empresa: 'Nueva solicitud de propuesta (empresa)', newsletter: 'Nueva suscripción al newsletter' };
  const lines = Object.entries({ Nombre: row.name, Correo: row.email, WhatsApp: row.phone, Empresa: row.company, 'País y ciudad': row.city, 'Servicio / interés': row.service, Mensaje: row.message }).filter(([, v]) => v);
  const subject = `Space to Rise · ${labels[kind]}`;
  let notified = 'none';
  if (process.env.RESEND_API_KEY) {
    // Correo transaccional propio (Resend, dominio clicalto.com verificado). Responder al correo va directo a la persona.
    const esc = s => String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
    const rows = lines.map(([k, v]) => `<tr><td style="padding:8px 12px;color:#7A6E5D;font-size:12px;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;vertical-align:top">${k}</td><td style="padding:8px 12px;color:#3A3A39;font-size:15px">${esc(v)}</td></tr>`).join('');
    const htmlBody = `<div style="font-family:Helvetica,Arial,sans-serif;background:#F9F5ED;padding:32px"><div style="max-width:560px;margin:0 auto;background:#fff;border-radius:16px;padding:28px 32px"><p style="margin:0 0 4px;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:#7A6E5D">spacetorise.com</p><h1 style="margin:0 0 18px;font-weight:400;font-size:22px;color:#3A3A39">${labels[kind]}</h1><table style="border-collapse:collapse;width:100%">${rows}</table><p style="margin:22px 0 0;font-size:13px;color:#7A6E5D">Responde a este correo para escribirle directamente a ${esc(row.name || row.email)}. Todas las solicitudes quedan guardadas en <a href="${(process.env.SITE_URL && !/vercel\.app/.test(process.env.SITE_URL)) ? process.env.SITE_URL : 'https://spacetorise.com'}/admin/" style="color:#7A6E5D">spacetorise.com/admin</a>.</p></div></div>`;
    const text = `${labels[kind]}\n\n` + lines.map(([k, v]) => `${k}: ${v}`).join('\n');
    try {
      const r = await fetch('https://api.resend.com/emails', {
        method: 'POST', headers: { Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify({ from: process.env.NOTIFY_FROM || 'Space to Rise <avisos@clicalto.com>', to, reply_to: email, subject, html: htmlBody, text }),
      });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(j.message || ('Resend ' + r.status));
      notified = 'resend:' + j.id;
    } catch (e) { console.error('resend', e.message); notified = 'resend-error'; }
  }
  if (notified !== 'none' && !notified.startsWith('resend:')) notified = 'resend-error';
  if (!notified.startsWith('resend:')) {
    // Respaldo: FormSubmit (requiere activación previa de cada correo destino).
    await Promise.all(to.map(addr => fetch('https://formsubmit.co/ajax/' + encodeURIComponent(addr), {
      method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ _subject: subject, _template: 'table', _replyto: email, _captcha: 'false', Tipo: labels[kind], ...Object.fromEntries(lines) }),
    }).catch(() => null)));
    if (notified === 'none') notified = 'formsubmit';
  }
  return json(res, 200, { ok: true, notified });
}
