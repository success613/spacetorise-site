import { createClient } from '@supabase/supabase-js';

export const SUPABASE_URL = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://epsokxvjqevmityasvrx.supabase.co';
export const ANON_KEY = process.env.SUPABASE_ANON_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || process.env.SUPABASE_PUBLISHABLE_KEY || 'sb_publishable_m4rurqAuHs8cHJfBq3bshQ_-4decACD';
export const SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SECRET_KEY || '';
export const SITE_URL = process.env.SITE_URL || process.env.VERCEL_PROJECT_PRODUCTION_URL && ('https://' + process.env.VERCEL_PROJECT_PRODUCTION_URL) || 'https://spacetorise.com';
export const ADMIN_EMAILS = (process.env.ADMIN_EMAILS || 'success@thrust-x.com').toLowerCase().split(',').map(s => s.trim()).filter(Boolean);

export const admin = () => createClient(SUPABASE_URL, SERVICE_KEY, { auth: { persistSession: false, autoRefreshToken: false } });
export const anon = () => createClient(SUPABASE_URL, ANON_KEY, { auth: { persistSession: false, autoRefreshToken: false } });

export function json(res, status, body) { res.setHeader('Content-Type', 'application/json; charset=utf-8'); res.status(status).send(JSON.stringify(body)); }
export function readBody(req) { if (!req.body) return {}; return typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body; }

/** Verifica el token del usuario (Authorization: Bearer <access_token>) y devuelve el usuario. */
export async function getUser(req) {
  const h = req.headers.authorization || '';
  const token = h.startsWith('Bearer ') ? h.slice(7) : null;
  if (!token) return null;
  const { data, error } = await anon().auth.getUser(token);
  if (error || !data?.user) return null;
  return data.user;
}
export const isAdmin = (user) => !!user?.email && ADMIN_EMAILS.includes(user.email.toLowerCase());

/* ---------- Mercado Pago ---------- */
export const MP_TOKEN = process.env.MP_ACCESS_TOKEN || '';
export async function mp(path, opts = {}) {
  const r = await fetch('https://api.mercadopago.com' + path, { ...opts, headers: { 'Authorization': 'Bearer ' + MP_TOKEN, 'Content-Type': 'application/json', ...(opts.headers || {}) } });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.message || ('Mercado Pago ' + r.status));
  return j;
}
/** Marca un pedido como pagado, registra las compras y envía el enlace mágico. Idempotente. */
export async function activateOrder(db, order, provider, paymentRef) {
  if (order.status === 'paid') return { ok: true, already: true };
  await db.from('orders').update({ status: 'paid', provider, payment_ref: paymentRef || null }).eq('id', order.id);
  const rows = (order.items || []).map(p => ({ email: order.email, product_id: p.id, status: 'paid', source: provider, reference: order.reference, amount: p.price }));
  if (rows.length) await db.from('purchases').upsert(rows, { onConflict: 'email,product_id' });
  await anon().auth.signInWithOtp({ email: order.email, options: { emailRedirectTo: SITE_URL + '/mis-audios/', shouldCreateUser: true } });
  return { ok: true };
}
