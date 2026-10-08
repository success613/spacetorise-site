import { admin, json, SERVICE_KEY, MP_TOKEN, mp, activateOrder } from './_lib.js';
/** GET /api/checkout-status?ref=STR-… → estado del pedido. Si Mercado Pago ya aprobó el pago
 *  y el webhook aún no llegó, lo verifica en la API y activa el pedido. */
export default async function handler(req, res) {
  try {
    const ref = String(req.query?.ref || '');
    if (!/^STR-[A-Z0-9-]+$/.test(ref) || !SERVICE_KEY) return json(res, 400, { error: 'Referencia inválida.' });
    const db = admin();
    const { data: order } = await db.from('orders').select('*').eq('reference', ref).single();
    if (!order) return json(res, 404, { error: 'Pedido no encontrado.' });
    const mask = order.email.replace(/^(.{2}).*(@.*)$/, '$1•••$2');
    if (order.status !== 'paid' && MP_TOKEN) {
      const s = await mp('/v1/payments/search?sort=date_created&criteria=desc&external_reference=' + encodeURIComponent(ref));
      const ok = (s.results || []).find(p => p.status === 'approved');
      if (ok) { await activateOrder(db, order, 'mercadopago', String(ok.id)); order.status = 'paid'; }
    }
    return json(res, 200, { status: order.status, email: mask, items: (order.items || []).map(i => i.name), total: order.total });
  } catch (e) { return json(res, 500, { error: e.message }); }
}
