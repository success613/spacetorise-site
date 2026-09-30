import { admin, anon, json, readBody, SITE_URL, SERVICE_KEY } from './_lib.js';
/** POST /api/checkout { email, items:[{id}] } → crea pedido pendiente y devuelve resumen.
 *  El pago se confirma después (webhook de pasarela o panel de Andrea). */
export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Método no permitido' });
  try {
    const { email, items } = readBody(req);
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json(res, 400, { error: 'Correo inválido.' });
    if (!Array.isArray(items) || !items.length) return json(res, 400, { error: 'El carrito está vacío.' });
    const db = SERVICE_KEY ? admin() : anon();
    const ids = items.map(i => String(i.id));
    const { data: prods } = await db.from('products').select('id,name,price').in('id', ids);
    if (!prods?.length) return json(res, 400, { error: 'Productos no encontrados.' });
    const total = prods.reduce((a, p) => a + p.price, 0);
    const reference = 'STR-' + Date.now().toString(36).toUpperCase() + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();
    if (SERVICE_KEY) {
      await db.from('orders').insert({ email: email.toLowerCase(), items: prods, total, status: 'pending', reference });
    }
    const lines = prods.map(p => `• ${p.name} — $ ${p.price.toLocaleString('es-CO')}`).join('\n');
    const msg = `Hola Andrea 😊 Quiero comprar estos audios (pedido ${reference}):\n${lines}\n\nTotal: $ ${total.toLocaleString('es-CO')}\nMi correo para el acceso: ${email}\n\n¿Me indicas cómo realizar el pago?`;
    return json(res, 200, { ok: true, reference, total, items: prods, whatsapp: 'https://wa.me/573107503359?text=' + encodeURIComponent(msg), portal: SITE_URL + '/mi-cuenta/' });
  } catch (e) { return json(res, 500, { error: e.message }); }
}
