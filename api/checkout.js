import { admin, anon, json, readBody, SITE_URL, SERVICE_KEY, MP_TOKEN, mp } from './_lib.js';
/** POST /api/checkout { email, items:[{id}] } → crea el pedido y, con Mercado Pago configurado,
 *  devuelve la URL de pago (Checkout Pro). Sin pasarela, devuelve el enlace de WhatsApp. */
export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Método no permitido' });
  try {
    const { email, items } = readBody(req);
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json(res, 400, { error: 'Correo inválido.' });
    if (!Array.isArray(items) || !items.length) return json(res, 400, { error: 'El carrito está vacío.' });
    const db = SERVICE_KEY ? admin() : anon();
    const ids = items.map(i => String(i.id));
    const { data: prods } = await db.from('products').select('id,name,price,cover').in('id', ids);
    if (!prods?.length) return json(res, 400, { error: 'Productos no encontrados.' });
    const total = prods.reduce((a, p) => a + p.price, 0);
    const reference = 'STR-' + Date.now().toString(36).toUpperCase() + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();
    const mail = email.toLowerCase();
    if (SERVICE_KEY) await db.from('orders').insert({ email: mail, items: prods.map(({ id, name, price }) => ({ id, name, price })), total, status: 'pending', reference });
    const base = { ok: true, reference, total, items: prods, portal: SITE_URL + '/mi-cuenta/' };
    if (MP_TOKEN) {
      const pref = await mp('/checkout/preferences', { method: 'POST', body: JSON.stringify({
        items: prods.map(p => ({ id: p.id, title: p.name, description: 'Audio de autohipnosis · Space to Rise', picture_url: p.cover ? SITE_URL + p.cover : undefined, category_id: 'services', quantity: 1, currency_id: 'COP', unit_price: p.price })),
        payer: { email: mail },
        external_reference: reference,
        back_urls: { success: SITE_URL + '/checkout/gracias/?ref=' + reference, pending: SITE_URL + '/checkout/gracias/?ref=' + reference + '&status=pending', failure: SITE_URL + '/checkout/?ref=' + reference + '&status=failure' },
        auto_return: 'approved',
        notification_url: SITE_URL + '/api/webhook-mp?ref=' + reference,
        statement_descriptor: 'SPACE TO RISE',
        metadata: { reference, email: mail },
        binary_mode: false,
      }) });
      return json(res, 200, { ...base, pay_url: pref.init_point, provider: 'mercadopago' });
    }
    const lines = prods.map(p => `• ${p.name} — $ ${p.price.toLocaleString('es-CO')}`).join('\n');
    const msg = `Hola Andrea 😊 Quiero comprar estos audios (pedido ${reference}):\n${lines}\n\nTotal: $ ${total.toLocaleString('es-CO')}\nMi correo para el acceso: ${email}\n\n¿Me indicas cómo realizar el pago?`;
    return json(res, 200, { ...base, whatsapp: 'https://wa.me/573107503359?text=' + encodeURIComponent(msg) });
  } catch (e) { return json(res, 500, { error: e.message }); }
}
