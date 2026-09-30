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
  return json(res, 200, { ok: true });
}
