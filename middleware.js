// Mientras el sitio no se lanza: spacetorise.com muestra la página "Muy pronto".
// La preview completa sigue en spacetorise-site.vercel.app. Para lanzar: borrar este archivo.
export const config = { matcher: ['/((?!_soon/|api/|assets/).*)'] };

export default function middleware(request) {
  const host = (request.headers.get('host') || '').toLowerCase();
  if (!/^(www\.)?spacetorise\.com$/.test(host)) return;
  const url = new URL(request.url);
  if (url.pathname.startsWith('/_soon/')) return;
  const target = new URL('/_soon/index.html', request.url);
  return new Response(null, { status: 200, headers: { 'x-middleware-rewrite': target.toString() } });
}
