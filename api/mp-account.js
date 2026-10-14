import { json, mp, MP_TOKEN } from './_lib.js';
/** GET /api/mp-account → estado de la cuenta de Mercado Pago que cobra (sin datos sensibles). Diagnóstico temporal. */
export default async function handler(req, res) {
  if (!MP_TOKEN) return json(res, 200, { configured: false });
  try {
    const u = await mp('/users/me');
    return json(res, 200, { configured: true, site_id: u.site_id, status: u.status, tags: u.tags, user_type: u.user_type, seller_experience: u.seller_experience, buyer_reputation: u.buyer_reputation && u.buyer_reputation.tags });
  } catch (e) { return json(res, 200, { configured: true, error: e.message }); }
}
