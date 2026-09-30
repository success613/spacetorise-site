import { admin, getUser, isAdmin, json, SERVICE_KEY } from '../_lib.js';
/** GET /api/admin/orders → últimos pedidos y compras (solo administradoras). */
export default async function handler(req, res) {
  try {
    const user = await getUser(req);
    if (!isAdmin(user)) return json(res, 403, { error: 'Solo administradoras.' });
    if (!SERVICE_KEY) return json(res, 500, { error: 'Falta SUPABASE_SERVICE_ROLE_KEY.' });
    const db = admin();
    const [{ data: orders }, { data: purchases }] = await Promise.all([
      db.from('orders').select('*').order('created_at', { ascending: false }).limit(50),
      db.from('purchases').select('email,product_id,status,source,created_at').order('created_at', { ascending: false }).limit(100)
    ]);
    return json(res, 200, { orders: orders || [], purchases: purchases || [] });
  } catch (e) { return json(res, 500, { error: e.message }); }
}
