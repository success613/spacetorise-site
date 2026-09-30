import { admin, json, readBody } from './_lib.js';
/** Recibe formularios del sitio: agenda (llamada inicial), empresas (propuesta) y newsletter. */
export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Método no permitido' });
  let b; try { b = readBody(req); } catch { return json(res, 400, { error: 'JSON inválido' }); }
  const kind = ['agenda', 'empresa', 'newsletter'].includes(b.kind) ? b.kind : null;
  const email = String(b.email || '').trim().toLowerCase();
  if (!kind || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json(res, 400, { error: 'Revisa el correo.' });
  if (b.website) return json(res, 200, { ok: true }); // honeypot
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
  await Promise.all(to.map(addr => fetch('https://formsubmit.co/ajax/' + encodeURIComponent(addr), {
    method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify({ _subject: `Space to Rise · ${labels[kind]}`, _template: 'table', _replyto: email, _captcha: 'false', Tipo: labels[kind], ...Object.fromEntries(lines) }),
  }).catch(() => null)));
  return json(res, 200, { ok: true });
}
