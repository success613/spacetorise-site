import { admin, anon, json, readBody, SITE_URL, SERVICE_KEY } from './_lib.js';
import crypto from 'node:crypto';
/** POST /api/webhook-wompi — evento transaction.updated de Wompi.
 *  Se activa cuando Andrea conecte su cuenta (WOMPI_EVENTS_SECRET). Valida la firma,
 *  marca el pedido como pagado, registra las compras y envía el enlace mágico. */
export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Método no permitido' });
  const secret = process.env.WOMPI_EVENTS_SECRET;
  if (!secret || !SERVICE_KEY) return json(res, 503, { error: 'Pasarela no configurada todavía.' });
  try {
    const ev = readBody(req);
    const t = ev?.data?.transaction; if (!t) return json(res, 400, { error: 'Evento sin transacción' });
    const props = ev.signature?.properties || [];
    const concat = props.map(p => p.split('.').reduce((o, k) => o?.[k], ev.data)).join('') + ev.timestamp + secret;
    const check = crypto.createHash('sha256').update(concat).digest('hex');
    if (check !== ev.signature?.checksum) return json(res, 401, { error: 'Firma inválida' });
    if (t.status !== 'APPROVED') return json(res, 200, { ok: true, ignored: t.status });
    const db = admin();
    const { data: order } = await db.from('orders').select('*').eq('reference', t.reference).single();
    if (!order) return json(res, 200, { ok: true, ignored: 'sin pedido' });
    await db.from('orders').update({ status: 'paid', provider: 'wompi' }).eq('id', order.id);
    const rows = order.items.map(p => ({ email: order.email, product_id: p.id, status: 'paid', source: 'wompi', reference: t.reference, amount: p.price }));
    await db.from('purchases').upsert(rows, { onConflict: 'email,product_id' });
    await anon().auth.signInWithOtp({ email: order.email, options: { emailRedirectTo: SITE_URL + '/mis-audios/' } });
    return json(res, 200, { ok: true });
  } catch (e) { return json(res, 500, { error: e.message }); }
}
