import { admin, json, readBody, SERVICE_KEY, MP_TOKEN, mp, activateOrder } from './_lib.js';
/** POST /api/webhook-mp — notificaciones de Mercado Pago (Checkout Pro).
 *  No confiamos en el cuerpo: consultamos el pago en la API con el Access Token y,
 *  si está aprobado, activamos el pedido (compras + enlace mágico). Siempre 200 para evitar reintentos. */
export default async function handler(req, res) {
  if (!MP_TOKEN || !SERVICE_KEY) return json(res, 200, { ok: false, reason: 'no configurado' });
  try {
    const q = req.query || {};
    const body = readBody(req) || {};
    const type = body.type || body.action || q.type || q.topic || '';
    const id = body?.data?.id || q['data.id'] || q.id;
    if (!/payment/.test(String(type)) || !id) return json(res, 200, { ok: true, ignored: type || 'sin tipo' });
    const p = await mp('/v1/payments/' + id);
    if (p.status !== 'approved') return json(res, 200, { ok: true, status: p.status });
    const ref = p.external_reference || q.ref;
    if (!ref) return json(res, 200, { ok: true, ignored: 'sin referencia' });
    const db = admin();
    const { data: order } = await db.from('orders').select('*').eq('reference', ref).single();
    if (!order) return json(res, 200, { ok: true, ignored: 'pedido no encontrado' });
    const r = await activateOrder(db, order, 'mercadopago', String(p.id));
    return json(res, 200, r);
  } catch (e) { console.error('webhook-mp', e); return json(res, 200, { ok: false, error: e.message }); }
}
