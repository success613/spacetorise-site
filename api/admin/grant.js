import { admin, anon, getUser, isAdmin, json, readBody, SITE_URL, SERVICE_KEY } from '../_lib.js';
/** POST /api/admin/grant { email, product_ids:[...] , send_link:true } — solo administradoras.
 *  Registra las compras como pagadas y envía el enlace mágico al cliente. */
export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Método no permitido' });
  try {
    const user = await getUser(req);
    if (!isAdmin(user)) return json(res, 403, { error: 'Solo administradoras.' });
    if (!SERVICE_KEY) return json(res, 500, { error: 'Falta SUPABASE_SERVICE_ROLE_KEY.' });
    const { email, product_ids, send_link = true, reference } = readBody(req);
    if (!email || !Array.isArray(product_ids) || !product_ids.length) return json(res, 400, { error: 'Faltan datos.' });
    const db = admin();
    const rows = product_ids.map(pid => ({ email: email.toLowerCase(), product_id: pid, status: 'paid', source: 'manual', reference: reference || null }));
    const { error } = await db.from('purchases').upsert(rows, { onConflict: 'email,product_id' });
    if (error) return json(res, 500, { error: error.message });
    if (reference) await db.from('orders').update({ status: 'paid' }).eq('reference', reference);
    let sent = false;
    if (send_link) {
      const { error: e2 } = await anon().auth.signInWithOtp({ email: email.toLowerCase(), options: { emailRedirectTo: SITE_URL + '/mis-audios/', shouldCreateUser: true } });
      sent = !e2;
    }
    return json(res, 200, { ok: true, granted: product_ids.length, link_sent: sent });
  } catch (e) { return json(res, 500, { error: e.message }); }
}
