import { admin, getUser, json, SERVICE_KEY } from './_lib.js';
/** GET /api/audio-url?product=ID → URL firmada (1 h) solo si el usuario compró el audio. */
export default async function handler(req, res) {
  try {
    const user = await getUser(req);
    if (!user) return json(res, 401, { error: 'Inicia sesión con tu enlace mágico.' });
    if (!SERVICE_KEY) return json(res, 500, { error: 'Falta configurar SUPABASE_SERVICE_ROLE_KEY.' });
    const product = (req.query.product || '').toString();
    const db = admin();
    const { data: p } = await db.from('products').select('id,name,audio_path').eq('id', product).single();
    if (!p) return json(res, 404, { error: 'Audio no encontrado.' });
    const { data: pur } = await db.from('purchases').select('id').eq('email', user.email).eq('product_id', product).eq('status', 'paid').maybeSingle();
    if (!pur) return json(res, 403, { error: 'Este audio no está en tus compras.' });
    let path = p.audio_path;
    let { data: signed, error } = await db.storage.from('audios').createSignedUrl(path, 3600);
    if (error) {
      // tolerancia: buscar por nombre parecido si el archivo se subió con otro nombre
      const { data: list } = await db.storage.from('audios').list('', { limit: 200 });
      const norm = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
      const want = norm(path).slice(0, 12);
      const hit = (list || []).find(f => norm(f.name).startsWith(want));
      if (hit) { path = hit.name; ({ data: signed, error } = await db.storage.from('audios').createSignedUrl(path, 3600)); }
    }
    if (error || !signed) return json(res, 500, { error: 'No se pudo generar el enlace del audio.' });
    return json(res, 200, { url: signed.signedUrl, name: p.name });
  } catch (e) { return json(res, 500, { error: e.message }); }
}
