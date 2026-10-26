import { admin, json, SERVICE_KEY } from './_lib.js';
/** GET /api/keepalive → consulta mínima a Supabase para que el plan gratuito no pause el proyecto por inactividad (lo llama un cron de Vercel a diario). */
export default async function handler(req, res) {
  if (!SERVICE_KEY) return json(res, 200, { ok: false, reason: 'sin clave' });
  try {
    const { count, error } = await admin().from('products').select('id', { count: 'exact', head: true });
    if (error) throw error;
    res.setHeader('Cache-Control', 'no-store');
    return json(res, 200, { ok: true, products: count, at: new Date().toISOString() });
  } catch (e) { return json(res, 500, { ok: false, error: e.message }); }
}
