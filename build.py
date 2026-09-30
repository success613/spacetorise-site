# -*- coding: utf-8 -*-
"""Space to Rise v2 — generador de páginas."""
import os, json, html, re

OUT = os.path.dirname(os.path.abspath(__file__))
WA = "https://wa.me/573107503359?text=Hola!%20Quiero%20reservar%20mi%20cita%20%F0%9F%98%8A"
IMG = "/assets/img/"
SPIRAL = open(os.path.join(OUT, 'assets/img/spiral-path.txt')).read().strip()
SUPA_URL = "https://epsokxvjqevmityasvrx.supabase.co"
SUPA_KEY = "sb_publishable_m4rurqAuHs8cHJfBq3bshQ_-4decACD"

NAV = [("RTT", "/rtt/"), ("Heal · Rise · Shine", "/heal-rise-shine/"), ("Kids", "/kids/"), ("Coaching", "/coaching/"), ("Gong", "/gong/"), ("Empresas", "/empresas/"), ("Shop", "/shop/"), ("Sobre mí", "/sobre-mi/")]
MENU = NAV + [("Preguntas frecuentes", "/preguntas-frecuentes/"), ("Agenda tu cita", "/agenda/"), ("Mi cuenta", "/mi-cuenta/")]
AG = "/agenda/"

SVG_WA = '<svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5.3-.5c.1-.2 0-.4 0-.5L9.1 6.9c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>'
SVG_CART = '<svg viewBox="0 0 24 24"><path d="M3 4h2l2.4 11.2a1 1 0 0 0 1 .8h8.8a1 1 0 0 0 1-.8L20 8H6.5"/><circle cx="9.5" cy="20" r="1.2"/><circle cx="17" cy="20" r="1.2"/></svg>'
SVG_USER = '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-6.5 8-6.5s8 2.5 8 6.5"/></svg>'
SVG_IG = '<svg viewBox="0 0 24 24"><path d="M12 7.3a4.7 4.7 0 1 0 0 9.4 4.7 4.7 0 0 0 0-9.4zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm5-8a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM21 8.6c-.1-1.5-.4-2.8-1.5-3.9S17 3.3 15.4 3.2c-1.6-.1-6.2-.1-7.8 0C6.1 3.3 4.8 3.6 3.7 4.7S2.3 7.1 2.2 8.6c-.1 1.6-.1 6.2 0 7.8.1 1.5.4 2.8 1.5 3.9s2.4 1.4 3.9 1.5c1.6.1 6.2.1 7.8 0 1.5-.1 2.8-.4 3.9-1.5s1.4-2.4 1.5-3.9c.1-1.6.1-6.2 0-7.8zm-2 9.5a3 3 0 0 1-1.7 1.7c-1.2.5-4 .4-5.3.4s-4.1.1-5.3-.4a3 3 0 0 1-1.7-1.7c-.5-1.2-.4-4-.4-5.3s-.1-4.1.4-5.3A3 3 0 0 1 6.7 5.9c1.2-.5 4-.4 5.3-.4s4.1-.1 5.3.4a3 3 0 0 1 1.7 1.7c.5 1.2.4 4 .4 5.3s.1 4.1-.4 5.3z"/></svg>'
SVG_YT = '<svg viewBox="0 0 24 24"><path d="M23 7.2a2.9 2.9 0 0 0-2-2C19.2 4.7 12 4.7 12 4.7s-7.2 0-9 .5a2.9 2.9 0 0 0-2 2C.5 9 .5 12 .5 12s0 3 .5 4.8a2.9 2.9 0 0 0 2 2c1.8.5 9 .5 9 .5s7.2 0 9-.5a2.9 2.9 0 0 0 2-2c.5-1.8.5-4.8.5-4.8s0-3-.5-4.8zM9.7 15V9l6 3-6 3z"/></svg>'
SVG_FB = '<svg viewBox="0 0 24 24"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.4c-.3 0-1.3-.1-2.4-.1-2.4 0-4.1 1.5-4.1 4.2v2.3H7.5V14h2.8v8h3.2z"/></svg>'
SVG_IN = '<svg viewBox="0 0 24 24"><path d="M6.9 21H3V8.5h3.9V21zM4.9 6.8a2.3 2.3 0 1 1 0-4.6 2.3 2.3 0 0 1 0 4.6zM21 21h-3.9v-6.1c0-1.5 0-3.3-2-3.3s-2.3 1.6-2.3 3.2V21H9V8.5h3.7v1.7h.1c.5-1 1.8-2 3.7-2 3.9 0 4.6 2.6 4.6 5.9V21z"/></svg>'
HEART = '<svg viewBox="0 0 24 24" width="100%" height="100%"><path d="M12 21s-7.5-4.6-9.5-9A5.3 5.3 0 0 1 12 6.5a5.3 5.3 0 0 1 9.5 5.5c-2 4.4-9.5 9-9.5 9z" fill="#EFBEB6"/></svg>'


def rings_svg(cls="rings", size=900, n=9, extra=""):
    cs = ''.join(f'<circle cx="450" cy="450" r="{40 + i * 46}"/>' for i in range(n))
    return f'<svg class="{cls}" viewBox="0 0 900 900" style="width:{size}px;height:{size}px;{extra}" aria-hidden="true">{cs}</svg>'


def spiral_svg(cls="", style=""):
    return f'<svg class="{cls}" viewBox="60 60 90 96" style="{style}" aria-hidden="true"><path d="{SPIRAL}"/></svg>'


def head(title, desc, path, dark=False, portal=False):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://spacetorise.com{path}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="https://spacetorise.com/assets/img/Home-Principal-New.jpg"><meta property="og:type" content="website"><meta property="og:locale" content="es_CO">
{'<meta name="robots" content="noindex">' if portal else ''}
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png"><link rel="apple-touch-icon" href="/assets/img/favicon-180.png">
<link rel="preload" href="/assets/fonts/gabriela-light.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/vendor/gsap.min.js" defer></script>
<script src="/assets/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="/assets/js/vendor/lenis.min.js" defer></script>
{'<script src="/assets/js/vendor/supabase.js" defer></script>' if portal else ''}
<script>window.STR_SUPABASE_URL="{SUPA_URL}";window.STR_SUPABASE_KEY="{SUPA_KEY}";</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HealthAndBeautyBusiness","name":"Space to Rise","url":"https://spacetorise.com","telephone":"+57 310 750 3359","image":"https://spacetorise.com/assets/img/Home-Principal-New.jpg","description":"{html.escape(desc)}","founder":{{"@type":"Person","name":"Andrea Zafra"}},"areaServed":"Colombia","sameAs":["https://www.instagram.com/spacetorise/","https://www.youtube.com/@spacetorise"]}}</script>
</head>
<body>
<div class="loader" aria-hidden="true">
  <div class="loader__stage">
    <svg class="loader__rings" viewBox="0 0 200 200"></svg>
    <div class="loader__drop"></div>
    <div class="loader__heart">{HEART}</div>
    <div class="loader__word">Space <em>to</em> Rise</div>
  </div>
</div>
<div class="wipe" aria-hidden="true"></div>
<header class="header{' dark' if dark else ''}">
  <div class="wrap">
    <a class="header__logo" href="/" aria-label="Space to Rise"><img src="{IMG}LOGO-Color_New.png" alt="Space to Rise"></a>
    <nav class="nav" aria-label="Principal">{''.join(f'<a href="{h}">{t}</a>' for t, h in NAV)}</nav>
    <div class="header__right">
      <a class="icon-btn" href="/mi-cuenta/" aria-label="Mi cuenta">{SVG_USER}</a>
      <button class="icon-btn cart-btn" aria-label="Carrito">{SVG_CART}<span class="count">0</span></button>
      <a class="pill" href="/agenda/"><span>Agenda tu cita</span></a>
      <button class="menu-btn" aria-label="Menú"><span></span><span></span></button>
    </div>
  </div>
</header>
<button class="menu-close" aria-label="Cerrar menú"></button>
<div class="menu" aria-hidden="true">
  <div>{''.join(f'<a class="big" href="{h}">{t}</a>' for t, h in MENU)}</div>
  <div class="meta"><span>Bogotá · Colombia · Online</span><a href="{WA}" target="_blank" rel="noopener">WhatsApp +57 310 750 3359</a></div>
</div>
<svg class="progress" viewBox="60 60 90 96" aria-hidden="true"><path class="track" d="{SPIRAL}"/><path class="fill" d="{SPIRAL}"/></svg>
<main>
"""


def foot(cta=True, cta_title="Tu transformación empieza con una conversación", cta_sub="Agenda una llamada inicial de 20 minutos y descubre cómo puedo acompañarte.", cta_btn="Agenda tu cita", cta_href="/agenda/"):
    ctahtml = f"""<section class="cta" data-dark>
  <video src="/assets/video/portrait.mp4" poster="/assets/video/portrait-poster.jpg" muted loop playsinline data-lazy></video>
  <div class="wrap">
    <span class="kicker fade" style="color:var(--linen)">Empieza hoy</span>
    <h2 class="display-l fade d1" style="margin-top:14px;max-width:18ch;margin-left:auto;margin-right:auto">{cta_title}</h2>
    <p class="fade d2" style="max-width:48ch;margin:0 auto 32px;color:rgba(249,245,237,.85)">{cta_sub}</p>
    <a class="pill light fade d3" href="{cta_href}"><span>{cta_btn}</span></a>
  </div>
</section>""" if cta else ''
    return f"""</main>
{ctahtml}
<footer class="footer" data-dark>
  {spiral_svg('spiral')}
  <div class="wrap">
    <div class="big">Space <em>to</em> Rise</div>
    <div class="cols">
      <div>
        <h5>Human evolution studio</h5>
        <p style="max-width:36ch;margin:0">Journey inward &amp; rise from your heart.</p>
        <p style="max-width:36ch;margin:14px 0 0">Nutre tu alma con nuestro newsletter y recibe un regalo de bienvenida.</p>
        <form class="newsletter" data-newsletter><input type="email" name="email" required placeholder="Tu correo electrónico" autocomplete="email" aria-label="Tu correo electrónico"><input type="text" name="website" tabindex="-1" autocomplete="off" style="display:none"><button type="submit">Suscríbete</button></form>
        <div class="social"><a href="https://www.instagram.com/spacetorise/" target="_blank" rel="noopener" aria-label="Instagram">{SVG_IG}</a><a href="https://www.youtube.com/@spacetorise" target="_blank" rel="noopener" aria-label="YouTube">{SVG_YT}</a><a href="https://www.facebook.com/profile.php?id=61574483459317" target="_blank" rel="noopener" aria-label="Facebook">{SVG_FB}</a><a href="https://www.linkedin.com/in/andrea-zafra-5b5bb09" target="_blank" rel="noopener" aria-label="LinkedIn">{SVG_IN}</a></div>
      </div>
      <div><h5>Explora</h5><ul><li><a href="/rtt/">RTT</a></li><li><a href="/heal-rise-shine/">Heal · Rise · Shine</a></li><li><a href="/kids/">Kids</a></li><li><a href="/coaching/">Coaching</a></li><li><a href="/gong/">Gong</a></li><li><a href="/empresas/">Empresas</a></li><li><a href="/shop/">Shop</a></li></ul></div>
      <div><h5>Space to Rise</h5><ul><li><a href="/sobre-mi/">Sobre mí</a></li><li><a href="/sobre-mi/#mision">Misión</a></li><li><a href="/preguntas-frecuentes/">Preguntas frecuentes</a></li><li><a href="/gif-for-you/">Gift for you</a></li><li><a href="/agenda/">Agenda tu cita</a></li><li><a href="/mi-cuenta/">Mi cuenta</a></li></ul></div>
      <div><h5>Contacto</h5><ul><li><a href="mailto:info@spacetorise.com">info@spacetorise.com</a></li><li><a href="https://www.instagram.com/spacetorise/" target="_blank" rel="noopener">@spacetorise</a></li><li><a href="{WA}" target="_blank" rel="noopener">WhatsApp +57 310 750 3359</a></li><li>Bogotá · Colombia · Online</li></ul></div>
    </div>
    <div class="bottom"><span>© 2026 Space to Rise · Andrea Zafra</span><span>Al despertar tu mundo, iluminas el mundo.</span></div>
  </div>
</footer>
<a class="wa" href="{WA}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{SVG_WA}<span class="tip">Escríbeme</span></a>
<div class="scrim"></div>
<aside class="drawer" aria-label="Carrito">
  <div class="drawer__head"><h3>Tu carrito</h3><button class="drawer__close pill" style="padding:8px 16px"><span>Cerrar</span></button></div>
  <div class="drawer__items"></div>
  <div class="drawer__foot"><div class="drawer__total"><span>Total</span><b></b></div><a class="pill solid" href="/checkout/"><span>Finalizar compra</span></a><p class="small muted" style="margin:12px 0 0;text-align:center">Recibirás tus audios en un espacio privado con enlace mágico.</p></div>
</aside>
<div class="modal" role="dialog" aria-modal="true"><div class="modal__box"><button class="modal__close" aria-label="Cerrar"></button><div class="modal__img"></div><div class="modal__body"></div></div></div>
<script src="/assets/js/site.js" defer></script>
<script src="/assets/js/shop.js" defer></script>
<script src="/assets/js/portal.js" defer></script>
</body>
</html>
"""


def hero(img, h1, sub=None, kicker=None, light=False, compact=True, video=None, pos="center", cta=True, cta2=None, btn="Agenda tu cita", href="/agenda/"):
    media = f'<video src="{video}" poster="{img}" autoplay muted loop playsinline></video>' if video else f'<img src="{img}" alt="" style="object-position:{pos}" fetchpriority="high">'
    kick = f'<span class="kicker fade" style="color:{"var(--taupe)" if light else "var(--linen)"}">{kicker}</span>' if kicker else ''
    b1 = f'<a class="pill{"" if light else " light"}" href="{href}"><span>{btn}</span></a>'
    b2 = f'<a class="pill{" light" if not light else ""}" href="{cta2[1]}" style="opacity:.85"><span>{cta2[0]}</span></a>' if cta2 else ''
    btns = f'<div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap">{b1}{b2}</div>' if cta else ''
    subh = f'<p class="lead fade d2">{sub}</p>' if sub else '<span></span>'
    return f"""<section class="hero{' light' if light else ''}{' compact' if compact else ''}"{'' if light else ' data-dark'}>
  <div class="hero__media">{media}</div>
  <div class="hero__body"><div class="wrap">
    {kick}
    <h1 class="display-l lines" style="margin-top:16px;max-width:16ch">{h1}</h1>
    <div class="hero__row">{subh}{btns}</div>
  </div></div>
  <div class="scroll-cue" aria-hidden="true"></div>
</section>"""


def feature(img, kicker, title, paras, link=None, flip=False, price=None, bg='', lst=None, cta=None, ratio=''):
    ps = ''.join(f'<p class="fade d{min(i + 1, 4)}">{p}</p>' for i, p in enumerate(paras))
    lst_html = f'<ul class="list fade d3" style="margin:22px 0">{"".join(f"<li>{x}</li>" for x in lst)}</ul>' if lst else ''
    price_html = f'<div class="price-tag fade d3">{price}<small>COP · sesión</small></div>' if price else ''
    link_html = f'<a class="pill fade d4" href="{link[1]}"><span>{link[0]}</span></a>' if link else ''
    cta_html = f'<a class="pill solid fade d4" href="{AG}"><span>{cta}</span></a>' if cta else ''
    return f"""<section class="pad {bg}"><div class="wrap feature{' flip' if flip else ''}">
  <div class="feature__media"><div class="media {ratio}"><img src="{IMG}{img}" alt="" loading="lazy"><div class="mask"></div></div></div>
  <div>{f'<span class="kicker fade">{kicker}</span>' if kicker else ''}<h2 class="display-m lines" style="margin:14px 0 22px">{title}</h2>{ps}{lst_html}{price_html}<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px">{cta_html}{link_html}</div></div>
</div></section>"""


T_ALL = [
 ("Me siento tan feliz. Liberaste a mi niña interior, volví a reír, a quererme, a valorarme y a entender que yo tengo el control de mi vida.", "Mónica"),
 ("Andre, gracias por enseñarme a fluir, a soltar todo lo que no controlo y a confiar en mí misma y en los tiempos del universo.", "Juliana"),
 ("Fue demasiado poderoso y me dio claridad total de muchas cosas. Gracias por darme herramientas para encontrar esa paz que tanto buscamos.", "Gabriela"),
 ("Gracias por ayudarme a entender que mi problema no era lo que comía, sino todo lo que me comía a mí. Tres meses después he logrado bajar 7 kilos.", "Alejandra"),
 ("Todavía no lo puedo creer: fui capaz de montarme al avión tranquila, ver una película y el vuelo se me pasó volando.", "Ma. Paula"),
 ("Desde que nos vimos no he vuelto a tener pesadillas ni ataques de ansiedad. Gracias por liberarme y enseñarme a perdonar.", "Santiago"),
 ("Nunca hubiera hecho la conexión entre mi problema de piel y lo que sentía en mi trabajo. Una vez lo expresé, mi piel sanó.", "Paciente RTT"),
 ("Recomiendo mucho la terapia para descubrir patrones del subconsciente que no sabemos que están ahí. Es un regalo para uno mismo.", "Sebastián"),
]


def deck(items):
    cards = ''.join(f'<figure class="deck__card" style="margin:0"><p>“{q}”</p><cite>{w}</cite></figure>' for q, w in items)
    return f'<section class="deck"><div class="deck__sticky"><div class="deck__title"><span class="kicker">Lo que dicen después de una sesión</span></div>{cards}</div></section>'


def steps3(items, cls=""):
    return f'<div class="tiles {cls}" style="gap:0 36px">' + ''.join(f'<div class="fade d{i}" style="border-top:1px solid rgba(58,58,57,.2);padding-top:22px"><span class="kicker" style="font-family:var(--display);font-size:1.3rem;letter-spacing:0;text-transform:none">0{i+1}</span><h3 class="display-s" style="margin:10px 0 8px;font-size:1.35rem">{t}</h3><p style="margin:0;font-size:.95rem;color:var(--charcoal)">{d}</p></div>' for i, (t, d) in enumerate(items)) + '</div>'


TESTI = [("Fue un proceso totalmente transformador.", "Natalia Lozano"),
         ("Me siento tan feliz. Liberaste a mi niña interior, volví a reír, a quererme y a entender que yo tengo el control de mi vida.", "Mónica · cliente RTT"),
         ("Gracias por ayudarme a entender que mi problema no era lo que comía, sino todo lo que me comía a mí. Tres meses después he logrado bajar 7 kilos.", "Alejandra · cliente RTT")]


def testi(items=TESTI, bg="bg-sand"):
    cards = ''.join(f'<figure class="tcard fade d{i}" style="margin:0"><p>“{q}”</p><cite>{w}</cite></figure>' for i, (q, w) in enumerate(items))
    return f'<section class="pad-s {bg}"><div class="wrap"><div class="sec-title"><span class="kicker">Lo que dicen quienes lo han vivido</span></div><div class="tcards">{cards}</div></div></section>'


def sec_title(kicker, more=None):
    m = f'<a class="more" href="{more[1]}">{more[0]} →</a>' if more else ''
    return f'<div class="sec-title"><span class="kicker">{kicker}</span>{m}</div>'


def lead_form(kind, fields, btn, intro=None, extra=None):
    f = ''
    for name, label, typ, opts in fields:
        if typ == 'select':
            f += f'<div class="field"><label for="{kind}-{name}">{label}</label><select id="{kind}-{name}" name="{name}">{"".join(f"<option>{o}</option>" for o in opts)}</select></div>'
        elif typ == 'textarea':
            f += f'<div class="field" style="grid-column:1/-1"><label for="{kind}-{name}">{label}</label><textarea id="{kind}-{name}" name="{name}" rows="4"></textarea></div>'
        else:
            f += f'<div class="field"><label for="{kind}-{name}">{label}</label><input id="{kind}-{name}" name="{name}" type="{typ}" {"required" if name in ("name","email") else ""} autocomplete="{ {"name":"name","email":"email","phone":"tel","company":"organization"}.get(name,"off") }"></div>'
    return f'''<div class="form-card fade d1"><form data-lead="{kind}">{f'<p class="small muted" style="margin:0 0 18px">{intro}</p>' if intro else ''}<div class="row">{f}</div><input type="text" name="website" tabindex="-1" autocomplete="off" style="display:none"><button class="pill solid" type="submit"><span>{btn}</span></button>{extra or ''}<div data-lead-out style="margin-top:16px"></div></form></div>'''


AUDIO_CATS = [("cuerpo-mente", "Sana tu cuerpo y mente", "bg-blush"), ("liberate", "Libérate de lo que no quieres", "bg-sand"), ("miedos", "Supera tus miedos", "bg-aqua"), ("profesional", "Desarrollo profesional", "bg-sky"), ("proyectos", "Proyectos de vida", "bg-rose"), ("kids", "Kids · Para niños", "bg-mist")]
COURSES = [("Sana la relación con tu peso para siempre", "Manten-tu-peso-ideal-scaled.jpg"), ("Queda embarazada", "Fertilizacion-Invitro-scaled.jpg"), ("Reset your life", "Energia-Sanadora-scaled.jpg")]


def courses_html():
    return '<div class="tiles">' + ''.join(f'<article class="course fade d{i}"><div class="media"><img src="{IMG}{img}" alt="" loading="lazy"><div class="mask"></div></div><div class="body"><span class="kicker" style="font-size:.62rem">Curso online</span><h3>{t}</h3><p class="small muted" style="margin:0">Muy pronto. Déjanos tu correo en el newsletter y te avisamos cuando abra.</p><div class="foot"><span>Próximamente</span><a href="/agenda/">Quiero saber más →</a></div></div></article>' for i, (t, img) in enumerate(COURSES)) + '</div>'


def cats_html():
    return '<div class="tiles" style="grid-template-columns:repeat(5,1fr)" data-cats>' + ''.join(f'<a class="tile {bg} fade d{i}" href="/shop/#{c}" style="min-height:170px;text-align:center;align-items:center;justify-content:center;border-radius:50%;aspect-ratio:1;padding:22px"><h3 style="font-size:clamp(1rem,1.3vw,1.25rem);margin:0 0 6px">{n}</h3><span class="tag" style="margin:0">Ver audios</span></a>' for i, (c, n, bg) in enumerate(AUDIO_CATS[:5])) + '</div>'


pages = {}
PRODUCTS = json.load(open(os.path.join(OUT, 'assets/data/products.json'), encoding='utf-8'))
fmt = lambda n: 'Gratis' if n == 0 else '$' + f'{n:,}'.replace(',', '.')

# ------------------------------------------------------------------ HOME
pages["/"] = dict(title="Space to Rise · Hipnoterapia RTT y neurociencia del cambio | Andrea Zafra",
 desc="Sana, transfórmate y evoluciona en quien estás destinada a ser. Hipnoterapia RTT, coaching, baños de gong y programas de bienestar para empresas. Andrea Zafra, Bogotá y online.",
 body=f"""
<section class="hero light" style="min-height:100svh">
  <div class="hero__media" style="background:var(--ivory)"><video src="/assets/video/drop.mp4" poster="/assets/video/drop-poster.jpg" autoplay muted loop playsinline style="opacity:.95"></video></div>
  <div class="hero__body"><div class="wrap">
    <span class="kicker fade" style="color:var(--taupe)">Hipnoterapia RTT · Neurociencia del cambio</span>
    <h1 class="display-xl lines" style="margin-top:18px;max-width:24ch;font-size:clamp(2.4rem,5.6vw,5.2rem)">Sana, transfórmate<br class="d">y evoluciona en quien<br class="d">estás destinada a ser.</h1>
    <div class="hero__row">
      <p class="lead fade d2">Acompaño a personas y empresas a encontrar la raíz de lo que las bloquea y a reprogramar la mente para un cambio real y permanente.</p>
      <div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap"><a class="pill solid" href="/agenda/"><span>Agenda tu cita</span></a><a class="pill" href="/empresas/"><span>Soy una empresa</span></a></div>
    </div>
  </div></div>
  <div class="scroll-cue" aria-hidden="true"></div>
</section>
<div class="creds fade"><span>Hipnoterapeuta clínica · RTT</span><span>Consultora certificada de Joe Dispenza (NCS)</span><span>MBA · IE Business School</span><span>Babson College</span><span>+10 años de experiencia</span></div>

<section class="pad"><div class="wrap grid g2" style="align-items:start">
  <div><span class="kicker fade">¿Te identificas?</span><h2 class="display-m lines" style="margin:14px 0 22px">Sabes lo que quieres cambiar,<br>pero algo más profundo<br>te sigue frenando.</h2><p class="fade d1">La fuerza de voluntad no basta cuando el 95% de nuestras decisiones nacen del subconsciente. Ahí es donde trabajamos: en la raíz, no en los síntomas.</p><a class="pill fade d2" href="/rtt/"><span>Descubre cómo funciona</span></a></div>
  <ul class="plist c2 fade d1" style="grid-template-columns:1fr"><li>Ansiedad, estrés o ataques de pánico</li><li>Miedos y fobias que te limitan</li><li>Baja autoestima o sensación de no ser suficiente</li><li>Insomnio, adicciones o hábitos que no logras dejar</li><li>Síntomas físicos que no mejoran</li><li>Metas que se te escapan una y otra vez</li></ul>
</div></section>

<section class="pad-s bg-stone"><div class="wrap">
  {sec_title("Dos caminos, una misma transformación")}
  <div class="tiles c2">
    <a class="tile bg-blush fade" href="/heal-rise-shine/"><span class="tag" style="position:absolute;top:26px;left:30px;margin:0">Para ti y tu familia</span><h3>Terapia individual</h3><p>Sesiones de RTT para sanar tu cuerpo, liberar tu mente y alcanzar tus objetivos. También para niños, con coaching y baños de gong.</p><span class="tag">Heal · Rise · Shine · Kids · Coaching · Gong →</span></a>
    <a class="tile bg-aqua fade d1" href="/empresas/"><span class="tag" style="position:absolute;top:26px;left:30px;margin:0">Para tu empresa</span><h3>Bienestar corporativo</h3><p>Talleres, retiros y el programa de neurociencia del cambio del Dr. Joe Dispenza, para cuidar a tu equipo y ayudarlo a crecer.</p><span class="tag">Talleres · Retiros · NeuroChangeSolutions →</span></a>
  </div>
</div></section>

<section class="manifesto" data-dark>
  <div class="manifesto__sticky">
    <div class="manifesto__bg"><video src="/assets/video/rtt.mp4" poster="/assets/video/rtt-poster.jpg" muted loop playsinline preload="metadata"></video></div>
    <div class="manifesto__phrases">
      <p class="manifesto__phrase">Sabes lo que quieres cambiar, <em>pero algo más profundo te sigue frenando.</em></p>
      <p class="manifesto__phrase">El 95% de tus decisiones <em>nacen del subconsciente.</em></p>
      <p class="manifesto__phrase">Por eso trabajamos en la raíz, <em>no en los síntomas.</em></p>
      <p class="manifesto__phrase">Muchas personas logran resultados <em>en 1 a 3 sesiones.</em></p>
      <p class="manifesto__phrase">Al despertar tu mundo, <em>iluminas el mundo.</em></p>
    </div>
    <div class="manifesto__idx">1 / 5</div>
  </div>
</section>

{feature("3.-Home-heal-New.jpg", "Rapid Transformational Therapy", "¿Qué es RTT?", [
 "Una terapia creada por Marisa Peer que combina hipnosis, PNL y neurociencia. Accede a tu subconsciente para encontrar la raíz de lo que te bloquea o te enferma, y reprogramarla.",
 "Muchas personas logran resultados en 1 a 3 sesiones."], link=("Conoce más", "/rtt/"), cta="Agenda tu cita")}
<section class="pad-s" style="padding-top:0"><div class="wrap">
  {steps3([("Conversación inicial", "Una llamada de 20 minutos para resolver tus dudas y entender lo que quieres sanar."), ("Tu sesión de RTT", "Entre 90 minutos y 2 horas de hipnosis para encontrar la raíz, entenderla y liberarla."), ("Tu audio personal", "Un audio hecho solo para ti, que escuchas 21 días para que tu mente cree nuevos hábitos.")])}
</div></section>

<section class="hscroll" data-dark>
  <div class="hscroll__pin">
    <div class="hscroll__track">
      <div class="panel intro"><span class="kicker">Cómo puedo acompañarte</span><h2 class="display-l" style="margin:16px 0 18px">Un camino para cada momento.</h2><p style="color:rgba(249,245,237,.8);max-width:36ch">Sana tu cuerpo, sana tu mente, alcanza tus objetivos. Desliza para descubrir cada camino.</p></div>
      <a class="panel" href="/heal-rise-shine/#heal"><span class="panel__n">01</span><img src="{IMG}HEAL.jpg" alt="" loading="lazy"><div class="panel__body"><h3>Heal</h3><p>Sana tu cuerpo. Enfermedades físicas y autoinmunes desde su raíz emocional.</p><span class="link"><i></i>Sana tu cuerpo</span></div></a>
      <a class="panel" href="/heal-rise-shine/#rise"><span class="panel__n">02</span><img src="{IMG}Rise.jpg" alt="" loading="lazy"><div class="panel__body"><h3>Rise</h3><p>Sana tu mente. Ansiedad, autoestima, adicciones, miedos, insomnio.</p><span class="link"><i></i>Sana tu mente</span></div></a>
      <a class="panel" href="/heal-rise-shine/#shine"><span class="panel__n">03</span><img src="{IMG}Shine.jpg" alt="" loading="lazy"><div class="panel__body"><h3>Shine</h3><p>Alcanza tus objetivos. Deportistas, líderes, profesionales y emprendedores.</p><span class="link"><i></i>Alcanza tus objetivos</span></div></a>
      <a class="panel" href="/kids/"><span class="panel__n">04</span><img src="{IMG}KIDS1Filtros.jpg" alt="" loading="lazy"><div class="panel__body"><h3>Kids</h3><p>Autoestima alta, menos ansiedad y mejor rendimiento para los más pequeños.</p><span class="link"><i></i>Conoce más</span></div></a>
      <a class="panel" href="/coaching/"><span class="panel__n">05</span><img src="{IMG}2.-Home-Coaching-New.jpg" alt="" loading="lazy"><div class="panel__body"><h3>Coaching</h3><p>Sesiones individuales para integrar tu transformación en el día a día.</p><span class="link"><i></i>Conoce más</span></div></a>
      <a class="panel" href="/gong/"><span class="panel__n">06</span><img src="{IMG}Gong_Home.jpg" alt="" loading="lazy"><div class="panel__body"><h3>Gong</h3><p>Baños de sonido para una relajación profunda del cuerpo y la mente.</p><span class="link"><i></i>Conoce más</span></div></a>
      <a class="panel" href="/empresas/"><span class="panel__n">07</span><img src="{IMG}babi-akpZ94lE0ZM-unsplash.jpg" alt="" loading="lazy"><div class="panel__body"><h3>Empresas</h3><p>Talleres, retiros y el programa NCS del Dr. Joe Dispenza para equipos y líderes.</p><span class="link"><i></i>Conoce más</span></div></a>
    </div>
  </div>
  <div class="hscroll__hint">Desliza · 07 caminos</div>
</section>

<section class="pad"><div class="wrap">
  <div class="feature">
    <div><span class="kicker fade">Empresas</span><h2 class="display-m lines" style="margin:14px 0 22px">Bienestar y transformación<br>para tu equipo.</h2><p class="lead fade d1">Las organizaciones crecen cuando crecen las personas que las forman.</p><p class="fade d2">Llevo a las empresas el mismo trabajo que hago con cada persona: herramientas para manejar el estrés, cuidar la salud emocional y cambiar los patrones que frenan a líderes y equipos.</p><div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px"><a class="pill solid" href="/empresas/#contacto"><span>Solicita una propuesta</span></a><a class="pill" href="/empresas/"><span>Ver programas</span></a></div></div>
    <div class="feature__media"><div class="media"><img src="{IMG}babi-akpZ94lE0ZM-unsplash.jpg" alt="" loading="lazy"><div class="mask"></div></div></div>
  </div>
  <div class="tiles" style="margin-top:clamp(36px,5vw,64px)">
    <a class="tile bg-blush fade" href="/empresas/"><span class="n">01</span><h3>Talleres de bienestar</h3><p>Manejo del estrés, salud emocional, autoestima y hábitos, con baños de gong grupales.</p></a>
    <a class="tile bg-sand fade d1" href="/empresas/"><span class="n">02</span><h3>Retiros corporativos</h3><p>Experiencias para que tu equipo desconecte, se reconecte y vuelva con más claridad.</p></a>
    <a class="tile bg-aqua fade d2" href="/empresas/#ncs"><span class="n">03</span><h3>Programa NCS del Dr. Joe Dispenza</h3><p>Change Your Mind… Create New Results: la neurociencia del cambio para líderes y equipos.</p></a>
  </div>
</div></section>

<section class="quote-band bg-taupe" data-dark><div class="wrap"><p class="fade">“No podemos ofrecer al mundo algo que no somos.”</p><cite class="fade d1">Andrea Zafra</cite></div></section>

{feature("AdreaZafra.jpg", "Hola, soy Andrea Zafra", "Hipnoterapeuta clínica especializada en RTT y consultora certificada de Joe Dispenza.", [
 "Después de años en grandes multinacionales, un MBA en el IE y mis estudios en Babson College, mis hijos me llevaron a transformar mi propia vida. Hoy uno la hipnoterapia, la neurociencia del cambio y más de 10 años de experiencia para acompañar a personas, familias y organizaciones."], link=("Conoce mi historia", "/sobre-mi/"), flip=True, bg="bg-stone")}

<section class="reel" data-dark>
  <div class="reel__sticky">
    <div class="reel__frame">
      <video src="/assets/video/rtt.mp4" poster="/assets/video/rtt-poster.jpg" playsinline preload="metadata" loop></video>
      <button class="reel__play" aria-label="Reproducir con sonido"><span>Ver</span></button>
    </div>
    <p class="reel__caption">Así es una terapia con Andrea</p>
  </div>
</section>

<section class="pad"><div class="wrap">
  <div class="narrow center fade" style="margin:0 auto clamp(40px,6vw,72px)"><span class="kicker">Conoce nuestra selección de audios y cursos</span><h2 class="display-m" style="margin-top:14px">Desbloquea tu potencial en la salud, el amor, la abundancia y mucho más, a tu ritmo y desde donde estés.</h2></div>
  {sec_title("Cursos", ("Ver todos", "/shop/#cursos"))}
  {courses_html()}
  <div style="height:clamp(40px,6vw,72px)"></div>
  {sec_title("Audios de autohipnosis", ("Ver todos", "/shop/#audios"))}
  {cats_html()}
</div></section>

{deck([TESTI[0]] + [(q, w) for q, w in T_ALL[:6]])}
""")

# ------------------------------------------------------------------ RTT
pages["/rtt/"] = dict(title="RTT · Terapia de Transformación Rápida | Space to Rise",
 desc="Hipnosis, PNL y neurociencia para llegar a la raíz de lo que te bloquea y lograr resultados rápidos, permanentes y transformadores. Muchas personas sanan en 1 a 3 sesiones.",
 body=hero(IMG + "RTT-Image-2.jpg", "Terapia de<br>Transformación Rápida", "Hipnosis, PNL y neurociencia para llegar a la raíz de lo que te bloquea y lograr resultados rápidos, permanentes y transformadores.", kicker="Rapid Transformational Therapy", pos="center 30%", cta2=("Preguntas frecuentes", "/preguntas-frecuentes/")) + f"""
<section class="pad-s bg-blush"><div class="wrap"><p class="caps fade" style="margin:0 auto;text-align:center;max-width:80ch">RTT es una terapia desarrollada por Marisa Peer que combina los principios más eficaces de la hipnosis, la PNL y la neurociencia. Muchas personas logran sanar en 1 a 3 sesiones, según la complejidad del tema.</p></div></section>

{feature("Heal1.jpg", "Cómo funciona", "La hipnosis te da acceso a tu subconsciente.", [
 "Ahí está toda tu programación: tus memorias y tus creencias. Entrar en él permite entender por qué reaccionas como reaccionas, encontrar la raíz del problema, sanarla y crear nuevas conexiones neuronales.",
 "<em>Entender es poder. Cuando entiendes el porqué de tus problemas, sanar es fácil.</em>"], flip=True)}

<section class="manifesto" data-dark style="height:320svh">
  <div class="manifesto__sticky">
    <div class="manifesto__bg"><video src="/assets/video/rtt.mp4" poster="/assets/video/rtt-poster.jpg" muted loop playsinline preload="metadata"></video></div>
    <div class="manifesto__phrases">
      <p class="manifesto__phrase">El 95% de tus decisiones <em>nacen del subconsciente.</em></p>
      <p class="manifesto__phrase">Por eso, aunque quieras cambiar con lógica y fuerza de voluntad, <em>ningún cambio será real y permanente hasta cambiar tu subconsciente.</em></p>
      <p class="manifesto__phrase">RTT te libera de creencias limitantes y “programas” obsoletos <em>que pueden estar detrás de tus bloqueos o de tu enfermedad.</em></p>
      <p class="manifesto__phrase">Y recablea tu mente con nuevas creencias <em>que transforman tu vida.</em></p>
    </div>
    <div class="manifesto__idx">1 / 4</div>
  </div>
</section>

<section class="pad"><div class="wrap">
  {sec_title("Tu proceso en 3 pasos")}
  {steps3([("Conversación inicial", "Una llamada de 20 minutos para aclarar cualquier duda sobre la terapia."), ("Tu sesión de RTT", "Entre 90 minutos y 2 horas. Con la hipnosis vamos a la raíz del problema para entender por qué y cuándo lo creaste, y liberarte de él."), ("Tu audio personal", "Un audio de 15 a 20 minutos hecho solo para ti, que escuchas cada día durante al menos 21 días para que el cambio sea permanente.")])}
</div></section>

<section class="pad-s bg-sand"><div class="wrap">
  {sec_title("¿Qué puedo sanar con RTT?")}
  <div class="tiles" style="gap:0 36px">
    <div class="fade"><h3 class="display-s" style="margin-bottom:8px">Salud física</h3><ul class="plist" style="grid-template-columns:1fr"><li>Enfermedades crónicas</li><li>Problemas de piel, pelo y digestivos</li><li>Dolores crónicos</li><li>Alergias y asma</li></ul></div>
    <div class="fade d1"><h3 class="display-s" style="margin-bottom:8px">Salud emocional</h3><ul class="plist" style="grid-template-columns:1fr"><li>Ansiedad y estrés</li><li>Autoestima y sensación de insuficiencia</li><li>Fobias, miedos y adicciones</li><li>Insomnio, peso y fertilidad</li></ul></div>
    <div class="fade d2"><h3 class="display-s" style="margin-bottom:8px">Desempeño</h3><ul class="plist" style="grid-template-columns:1fr"><li>Alcanzar sueños, metas y objetivos</li><li>Mejorar tu rendimiento deportivo</li><li>Hablar en público</li><li>Concentración y procrastinación</li></ul></div>
  </div>
  <div class="small muted fade" style="display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-top:28px"><span>Es una terapia apta para niños y adultos.</span><span>RTT es un acompañamiento complementario y no reemplaza el diagnóstico ni el tratamiento médico.</span></div>
</div></section>

<section class="pad-s"><div class="wrap">
  {sec_title("Preguntas frecuentes", ("Ver todas", "/preguntas-frecuentes/"))}
  <div class="acc fade">{''.join(f'<div class="acc__item"><button class="acc__q">{q}<i></i></button><div class="acc__a"><div><div class="inner"><p>{a}</p></div></div></div></div>' for q, a in [("¿Cómo se siente estar hipnotizado?", "La mayoría de las personas se siente muy relajada. Estás 100% en control de tu cuerpo y solo aceptas las sugerencias que tú quieras."), ("¿Por qué RTT sana en una sola sesión?", "La hipnosis permite identificar el origen de las creencias que te bloquean. Al observarlas desde tu mente adulta, es fácil dejarlas ir."), ("¿Cuándo veo los resultados?", "Pueden ser inmediatos, progresivos en 10 a 21 días, o retroactivos: a veces quienes te rodean notan el cambio primero."), ("¿Puedo hacer la sesión por Zoom?", "Sí. Las sesiones pueden ser presenciales o por Zoom.")])}</div>
</div></section>
{testi()}
""", cta_title="¿Lista para ir a la raíz?", cta_sub="Agenda tu llamada inicial de 20 minutos y resolvemos todas tus dudas.")

# ------------------------------------------------------------------ HEAL RISE SHINE
pages["/heal-rise-shine/"] = dict(title="Heal · Rise · Shine — RTT para personas | Space to Rise",
 desc="Tres caminos para sanar tu cuerpo, liberar tu mente y alcanzar todo lo que quieres con RTT.",
 body=hero(IMG + "Ansiedad-scaled.jpg", "Heal · Rise · Shine", "Tres caminos para sanar tu cuerpo, liberar tu mente y alcanzar todo lo que quieres.", kicker="RTT para personas", pos="center 20%") + f"""
<section class="pad-s"><div class="wrap tiles">
  <a class="tile dark fade" href="#heal" style="min-height:300px;background:url({IMG}HEAL.jpg) center/cover"><h3>Heal</h3><span class="tag">Sana tu cuerpo →</span></a>
  <a class="tile dark fade d1" href="#rise" style="min-height:300px;background:url({IMG}Rise.jpg) center/cover"><h3>Rise</h3><span class="tag">Sana tu mente →</span></a>
  <a class="tile dark fade d2" href="#shine" style="min-height:300px;background:url({IMG}Shine.jpg) center/cover"><h3>Shine</h3><span class="tag">Alcanza tus objetivos →</span></a>
</div></section>

<section id="heal" class="pad"><div class="wrap">
  <div class="sec-title"><h2 class="display-l" style="margin:0">Heal</h2><span class="more">Sana tu cuerpo</span></div>
  <div class="quote-band" style="padding:0 0 40px"><p class="fade" style="font-size:clamp(1.2rem,2vw,1.7rem)">“El dolor que no encuentra salida en las lágrimas pronto puede hacer llorar a otros órganos.”</p><cite class="fade d1">Sir Henry Maudsley</cite></div>
  <p class="caps fade" style="margin:0 auto 48px;text-align:center">Cualquier emoción reprimida puede ser la causa de enfermedades físicas. Mente y cuerpo están conectados: lo que no expresamos, el cuerpo lo expresa en forma de enfermedad.</p>
  <div class="feature">
    <div><p class="fade">RTT es muy efectiva para encontrar la causa raíz de estos bloqueos y emociones. A través de la hipnosis accedes a tu subconsciente, donde se guardan tus memorias y emociones, y logras reinterpretar lo que pasó para sanar.</p><p class="fade d1">Durante la sesión puedes recordar experiencias, eventos o patrones de pensamiento relacionados con tu problema de salud. Al entenderlos, puedes darles otra interpretación y cambiar las creencias que contribuyeron a tu enfermedad.</p><p class="lead fade d2">Tu mente puede crear una enfermedad, pero así como la crea, puede ayudarte a sanarla.</p><p class="small muted fade d3">RTT es un acompañamiento complementario y no reemplaza el diagnóstico ni el tratamiento médico.</p></div>
    <div class="feature__media"><div class="media"><img src="{IMG}Heal2.jpg" alt="" loading="lazy"><div class="mask"></div></div></div>
  </div>
  <div style="margin-top:clamp(40px,5vw,64px)">{sec_title("Temas con los que hemos trabajado")}<ul class="plist fade"><li>Cáncer (como acompañamiento)</li><li>Dolores crónicos</li><li>Enfermedades genéticas</li><li>Enfermedades autoinmunes</li><li>Problemas de audición</li><li>Problemas de visión</li><li>Asma</li><li>Problemas de piel y pelo</li><li>Alergias</li></ul></div>
</div></section>

<section id="rise" class="pad bg-stone"><div class="wrap">
  <div class="sec-title"><h2 class="display-l" style="margin:0">Rise</h2><span class="more">Sana tu mente</span></div>
  <div class="quote-band" style="padding:0 0 40px"><p class="fade" style="font-size:clamp(1.2rem,2vw,1.7rem);max-width:34ch">“Puede que no seamos responsables de cómo el mundo moldea nuestra mente, pero podemos aprender a ser responsables de la mente con la que creamos nuestro mundo.”</p></div>
  <p class="caps fade" style="margin:0 auto 48px;text-align:center">El 95% de las decisiones de tu vida nacen de las memorias guardadas en tu subconsciente. Lo que ves hoy está determinado por las experiencias de tu pasado.</p>
  <div class="feature flip">
    <div><p class="fade">Para un cambio permanente hay que encontrar la raíz del dolor. De nada sirve tratar solo los síntomas o confiar en la fuerza de voluntad: el subconsciente y la emoción siempre le ganan a la lógica.</p><p class="fade d1">RTT te permite encontrar esas memorias y reinterpretarlas desde tu mente adulta y no desde la de un niño, entendiendo y sanando para evolucionar.</p></div>
    <div class="feature__media"><div class="media"><img src="{IMG}4.Rise-en-vez-de-mano-scaled.jpg" alt="" loading="lazy"><div class="mask"></div></div></div>
  </div>
  <div style="margin-top:clamp(40px,5vw,64px)">{sec_title("Temas con los que hemos trabajado")}<ul class="plist fade"><li>Ansiedad y ataques de pánico</li><li>Baja autoestima</li><li>Estrés</li><li>Autosabotaje</li><li>Adicciones: cigarrillo, vapeador, alcohol, juego</li><li>Insomnio y trastornos de sueño</li><li>Depresión</li><li>Fobias: volar, agujas, claustrofobia</li><li>Fertilidad</li><li>Concentración y procrastinación</li><li>Miedo a hablar en público</li><li>Duelos y celos</li></ul></div>
</div></section>

<section id="shine" class="pad"><div class="wrap">
  <div class="sec-title"><h2 class="display-l" style="margin:0">Shine</h2><span class="more">Brilla · Alcanza tus objetivos</span></div>
  <div class="quote-band" style="padding:0 0 40px"><p class="fade" style="font-size:clamp(1.2rem,2vw,1.7rem)">“Tus palabras crean tu realidad. Si no te gusta tu realidad, cambia tus palabras.”</p></div>
  <p class="caps fade" style="margin:0 auto 48px;text-align:center">Conviértete en tu mejor versión y alcanza tus sueños. Libérate de lo que te impide ser y reprograma tu mente para lograr todo lo que quieres.</p>
  <div class="feature">
    <div><p class="fade">RTT te permite encontrar la causa raíz de lo que te detiene, y el audio de transformación personal, hecho especialmente para ti, reprograma tu mente para alcanzar tus objetivos.</p>
      <div class="tiles c2" style="margin-top:26px"><div class="tile bg-aqua fade d1" style="min-height:0"><span class="tag" style="margin:0 0 10px">Deporte</span><h3>Conviértete en el mejor deportista</h3><p>Supera bloqueos mentales, maneja la presión y lleva tu rendimiento al siguiente nivel.</p></div><div class="tile bg-sand fade d2" style="min-height:0"><span class="tag" style="margin:0 0 10px">Liderazgo</span><h3>Conviértete en el mejor líder</h3><p>Gana seguridad, claridad y confianza para liderar a tu equipo y a ti misma.</p></div></div></div>
    <div class="feature__media"><div class="media"><img src="{IMG}Shine-scaled.jpg" alt="" loading="lazy"><div class="mask"></div></div></div>
  </div>
</div></section>
{testi()}
""", cta_title="Empieza hoy tu transformación", cta_sub="Agenda una llamada inicial de 20 minutos y elegimos juntas el camino.")

# ------------------------------------------------------------------ KIDS
pages["/kids/"] = dict(title="Kids · RTT para niños | Space to Rise",
 desc="RTT ayuda a los niños a superar cualquier desafío emocional: autoestima alta, menos ansiedad y mejor rendimiento académico.",
 body=hero(IMG + "Nueva-Foto-Kids-scaled.jpg", "“Lo más valioso que puedes enseñarles a tus hijos es que son suficientes.”", "Marisa Peer", kicker="Kids · Niños", pos="center 35%", btn="Agenda una cita") + f"""
<section class="pad-s bg-blush"><div class="wrap"><p class="caps fade" style="margin:0 auto;text-align:center;max-width:80ch">Como papás tenemos una responsabilidad gigante: ayudar a nuestros hijos a tener una autoestima inquebrantable para que sean niños felices que se conviertan en adultos realizados y equilibrados.</p></div></section>
{feature("Kids2.jpg", None, "Su voz interior empieza en casa.", [
 "Las experiencias vividas en la infancia tienen un impacto enorme en la autoestima, las creencias, la mentalidad y la vida de una persona adulta.",
 "La manera en que les hablamos a nuestros hijos se convierte en su voz interior y moldea su imagen propia. Por eso es tan importante inculcar creencias positivas y construir una base sólida de autoestima, seguridad y confianza.",
 "RTT ayuda a los niños a superar cualquier desafío emocional para que no crezcan con creencias limitantes. Construimos una autoestima alta y les damos herramientas para manejar la ansiedad, el estrés y mejorar su rendimiento académico."], flip=True)}
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Temas en los que podemos ayudar")}<ul class="plist fade"><li>Autoestima alta y bullying</li><li>Ansiedad y estrés</li><li>Rendimiento académico</li><li>Pasar exámenes</li><li>Pesadillas y sueño</li><li>TDAH</li><li>Dislexia</li></ul></div></section>
<section class="pad"><div class="wrap tiles c2">
  <div class="fade"><span class="kicker">Para papás y mamás</span><h2 class="display-m" style="margin:14px 0 18px">Criar sin miedos empieza por ti.</h2><p>También acompaño a padres para que puedan criar nuevas generaciones libres de miedos y creencias limitantes, con mucho amor propio y alas fuertes para volar alto.</p><a class="pill" href="/heal-rise-shine/"><span>Conoce RTT para adultos</span></a></div>
  <div class="tile bg-blush fade d1"><span class="tag" style="position:absolute;top:26px;left:30px;margin:0">Sesiones Kids</span><h3>Una experiencia pensada para ellos</h3><p>Sesiones adaptadas a la edad de cada niño, con un audio personal para reforzar el cambio en casa.</p><p style="margin-top:14px"><span class="tag" style="margin:0">Valor</span><br><b style="font-family:var(--display);font-weight:300;font-size:1.8rem">$350.000</b></p><a class="pill solid" href="/agenda/" style="margin-top:18px;align-self:flex-start"><span>Agenda tu cita</span></a></div>
</div></section>
{testi()}
""", cta_title="Dale a tu hijo la mejor base para su vida", cta_sub="Agenda una llamada inicial y conversemos sobre lo que necesita.")

# ------------------------------------------------------------------ COACHING
pages["/coaching/"] = dict(title="Coaching individual — Combina lo mejor de ambos mundos | Space to Rise",
 desc="Con RTT sanas la raíz. Con el coaching integras el cambio en tu vida para no volver a los patrones del pasado. Sesiones de 1 hora, presenciales o por Zoom.",
 body=hero(IMG + "image.jpg", "Combina lo mejor<br>de ambos mundos", "Con RTT sanas la raíz. Con el coaching integras el cambio en tu vida para no volver a los patrones del pasado.", kicker="Coaching individual", pos="center 40%", btn="Agenda tu sesión") + f"""
<section class="pad-s bg-aqua"><div class="wrap"><p class="caps fade" style="margin:0 auto;text-align:center;max-width:80ch">Con RTT trabajamos tu mente subconsciente, entendiendo el porqué de tus comportamientos y la raíz de tus problemas. Con el coaching individual te ayudo a implementar los cambios necesarios para que nunca más vuelvas a autosabotear tu transformación.</p></div></section>
<section class="pad"><div class="wrap feature">
  <div><span class="kicker fade">Coaching individual</span>
    <div class="tiles c2 fade d1" style="margin:22px 0"><div class="pricecard bg-blush"><b>1h</b><span class="k">Por sesión</span><p>Un espacio enfocado solo en ti.</p></div><div class="pricecard bg-sand"><b>2</b><span class="k">Modalidades</span><p>Presencial o por Zoom.</p></div></div>
    <p class="lead fade d2" style="margin:0 0 8px">Valor por sesión: <b style="font-weight:500">$150.000</b></p>
    <p class="fade d2">Ideal después de tu sesión de RTT, o para acompañar cualquier proceso de cambio: nuevos hábitos, decisiones importantes, metas personales o profesionales.</p>
    <a class="pill solid fade d3" href="/agenda/"><span>Agenda tu sesión</span></a></div>
  <div class="feature__media"><div class="media"><img src="{IMG}Nueva-Foto-Coaching-scaled.jpg" alt="" loading="lazy"><div class="mask"></div></div></div>
</div></section>
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Cómo trabajamos")}{steps3([("Definimos tu objetivo", "Aclaramos qué quieres lograr y qué te ha detenido hasta ahora."), ("Diseñamos tu plan", "Pasos concretos y prácticos para integrar el cambio en tu día a día."), ("Te acompaño", "Sesiones de seguimiento para sostener tu transformación en el tiempo.")])}</div></section>
{testi()}
""", cta_title="Da el siguiente paso con acompañamiento", cta_sub="Agenda tu sesión de coaching, presencial o por Zoom.", cta_btn="Agenda tu sesión")

# ------------------------------------------------------------------ GONG
pages["/gong/"] = dict(title="Baños de gong — Sana y transforma tu vida con la vibración del sonido | Space to Rise",
 desc="Una técnica de relajación profunda que se alcanza a través de las vibraciones de este instrumento ancestral. Sesiones individuales, grupales y para empresas.",
 body=hero(IMG + "Gong_Home.jpg", "Sana y transforma tu vida con la vibración del sonido", "Una técnica de relajación profunda que se alcanza a través de las vibraciones de este instrumento ancestral.", kicker="Baños de gong", pos="center 50%", btn="Reserva tu sesión", cta2=("Para empresas", "/empresas/")) + f"""
{feature("EC5B0F01-906B-49CF-BFBC-83D8E23D25F6.jpg", "Qué es", "Más que un instrumento, un sistema vibracional.", [
 "El gong recibe las energías de la persona, las armoniza y las devuelve potenciadas con una intención. Su sonido y vibración promueven el bienestar físico, mental y emocional, equilibran los centros de energía del cuerpo y ayudan a liberar emociones reprimidas.",
 "Puede ser una terapia complementaria en procesos de salud, porque su vibración llega a cada célula del cuerpo.",
 "<span class='small muted'>RTT es un acompañamiento complementario y no reemplaza el diagnóstico ni el tratamiento médico.</span>"])}
<section class="pad-s bg-sand"><div class="wrap">{sec_title("Beneficios")}<div class="tiles c4">
  <div class="tile fade" style="background:var(--white);min-height:0"><span class="n">01</span><h3 style="margin-top:34px">Relajación profunda</h3><p>Calma el sistema nervioso y aquieta la mente.</p></div>
  <div class="tile fade d1" style="background:var(--white);min-height:0"><span class="n">02</span><h3 style="margin-top:34px">Libera emociones</h3><p>Ayuda a soltar tensiones y emociones reprimidas.</p></div>
  <div class="tile fade d2" style="background:var(--white);min-height:0"><span class="n">03</span><h3 style="margin-top:34px">Equilibra tu energía</h3><p>Armoniza los centros de energía del cuerpo.</p></div>
  <div class="tile fade d3" style="background:var(--white);min-height:0"><span class="n">04</span><h3 style="margin-top:34px">Claridad</h3><p>Te ayuda a ver con más claridad lo que quieres sanar.</p></div>
</div></div></section>
<section class="pad"><div class="wrap">{sec_title("Sesiones")}<div class="tiles c2">
  <div class="pricecard bg-blush fade"><span class="k">Individual</span><b>$150.000</b><p>Una experiencia sonora pensada solo para ti.</p><a class="pill" href="/agenda/" style="margin-top:18px"><span>Reservar</span></a></div>
  <div class="pricecard bg-aqua fade d1"><span class="k">Grupal</span><b>$100.000 <small style="font-size:.5em">por persona</small></b><p>Vive el baño de gong con tu familia, amigos o equipo de trabajo.</p><a class="pill" href="/agenda/" style="margin-top:18px"><span>Reservar</span></a></div>
</div><p class="lead fade d2" style="text-align:center;max-width:56ch;margin:clamp(36px,5vw,60px) auto 0;font-style:italic">Regálate esta experiencia única y déjame acompañarte en este viaje sonoro hacia tu bienestar.</p></div></section>
""", cta_title="Reserva tu baño de gong", cta_sub="Sesiones individuales, grupales y para empresas.", cta_btn="Reserva tu sesión")

# ------------------------------------------------------------------ EMPRESAS
pages["/empresas/"] = dict(title="Empresas — Bienestar y transformación para tu equipo | Space to Rise",
 desc="Talleres de bienestar, retiros corporativos y el programa NCS del Dr. Joe Dispenza (Change Your Mind… Create New Results) para líderes y equipos.",
 body=hero(IMG + "babi-akpZ94lE0ZM-unsplash.jpg", "Bienestar y<br>transformación<br>para tu equipo", "Las organizaciones crecen cuando crecen las personas que las forman.", kicker="Empresas", pos="center 30%", btn="Solicita una propuesta", href="#contacto", cta2=("Ver programa NCS", "#ncs")) + f"""
<div class="creds fade"><span>Consultora certificada de NeuroChangeSolutions</span><span>MBA · IE Business School</span><span>+10 años de experiencia</span></div>
<section class="pad"><div class="wrap">
  <p class="lead fade narrow" style="margin:0 0 clamp(36px,5vw,64px)">Llevo a las empresas el mismo trabajo que hago con cada persona: herramientas para manejar el estrés, cuidar la salud emocional y cambiar los patrones que frenan a líderes y equipos. Cada propuesta se diseña según lo que tu organización necesita.</p>
  {sec_title("Programas para empresas")}
  <div class="tiles">
    <div class="tile bg-blush fade"><span class="n">01</span><h3 style="margin-top:34px">Talleres de bienestar</h3><p>Sesiones para tu equipo sobre manejo del estrés, salud emocional, autoestima y hábitos. Incluyen baños de gong grupales.</p><span class="tag">Presencial o virtual</span></div>
    <div class="tile bg-sand fade d1"><span class="n">02</span><h3 style="margin-top:34px">Retiros corporativos</h3><p>Experiencias de uno o varios días para que tu equipo desconecte, se reconecte y vuelva con más claridad y energía.</p><span class="tag">Diseñados a la medida</span></div>
    <div class="tile bg-aqua fade d2"><span class="n">03</span><h3 style="margin-top:34px">Programa NCS del Dr. Joe Dispenza</h3><p>Change Your Mind… Create New Results: la neurociencia del cambio aplicada a líderes y equipos.</p><span class="tag">Consultora certificada</span></div>
  </div>
</div></section>
<section id="ncs" class="pad bg-sky"><div class="wrap">
  <div class="grid g2" style="align-items:start">
    <div><span class="kicker fade">NeuroChangeSolutions</span><h2 class="display-m lines" style="margin:14px 0 22px">Change Your Mind…<br>Create New Results</h2><p class="fade d1">Como consultora certificada de NeuroChangeSolutions, imparto el taller creado por el Dr. Joe Dispenza. Explica cómo funciona el cambio en el cerebro y en el cuerpo, y da a cada persona herramientas concretas para crearlo y sostenerlo en el tiempo.</p></div>
    <div class="fade d1" style="padding:clamp(24px,3vw,40px);background:rgba(249,245,237,.55);border-radius:3px"><span class="kicker">La premisa del programa</span><p class="display-s" style="margin:12px 0 0;font-size:clamp(1.3rem,2vw,1.7rem);line-height:1.3">El cambio sí es posible: existe un proceso para crearlo y sostenerlo, y se puede aprender.</p></div>
  </div>
  <div class="stats" style="margin-top:clamp(32px,4vw,56px)">
    <div class="stat fade"><b>8+</b><span>Horas de taller</span><p>Un programa que se adapta a tu equipo y a tu organización.</p></div>
    <div class="stat fade d1"><b>2</b><span>Modelos de cambio</span><p>Para entender las etapas que atraviesa cada persona para cambiar.</p></div>
    <div class="stat fade d2"><b>4</b><span>Herramientas</span><p>Para crear y sostener el cambio, entre ellas el ensayo mental.</p></div>
  </div>
</div></section>
<section class="pad-s"><div class="wrap">{sec_title("Ideal para empresas que buscan")}<ul class="plist fade"><li>Liderazgo consciente</li><li>Equipos preparados para el cambio</li><li>Menos estrés, más bienestar</li><li>Creatividad e innovación</li><li>Una cultura que retiene talento</li><li>Colaboración y productividad</li></ul></div></section>
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Cómo trabajamos")}{steps3([("Conversación", "Entendemos el momento de tu organización y lo que quieres lograr."), ("Propuesta", "Diseñamos el taller, retiro o programa adecuado para tu equipo."), ("Experiencia", "Llevamos la experiencia a tu equipo, presencial o virtual."), ("Seguimiento", "Acompañamos la integración del cambio en el día a día.")], cls="c4")}</div></section>
{testi([TESTI[0], ("Un espacio para que los equipos desconecten, se reconecten y vuelvan con más claridad.", "Retiro corporativo"), ("La neurociencia del cambio aplicada a líderes y equipos.", "Programa NCS")], bg="bg-sand")}
<section id="contacto" class="pad"><div class="wrap grid g2" style="align-items:start">
  <div><span class="kicker fade">Contacto</span><h2 class="display-m lines" style="margin:14px 0 18px">Diseñemos juntos la experiencia para tu equipo.</h2><p class="fade d1">Cuéntanos sobre tu organización y te enviaremos una propuesta a la medida.</p><p class="fade d2"><a href="mailto:info@spacetorise.com" style="text-decoration:underline">info@spacetorise.com</a></p></div>
  {lead_form("empresa", [("name", "Nombre", "text", None), ("company", "Empresa", "text", None), ("email", "Correo", "email", None), ("phone", "Teléfono", "tel", None), ("service", "Me interesa", "select", ["Talleres de bienestar", "Retiros corporativos", "Programa NCS del Dr. Joe Dispenza", "Baños de gong para equipos", "Aún no lo sé"]), ("message", "Cuéntanos sobre tu equipo", "textarea", None)], "Solicita una propuesta")}
</div></section>
""", cta=False)

# ------------------------------------------------------------------ SHOP
pages["/shop/"] = dict(title="Shop · Audios de autohipnosis y cursos | Space to Rise",
 desc="Audios de autohipnosis y cursos para crear cambios permanentes en tu vida, desde donde estés. Reconfigura tu cerebro en menos de 20 minutos al día.",
 body=hero(IMG + "Shop-Principal.jpg", "Reconfigura tu cerebro en menos de 20 minutos al día", "Audios de autohipnosis y cursos para crear cambios permanentes en tu vida, desde donde estés.", kicker="Shop · Audios y cursos", light=True, pos="center 30%", btn="Ver audios", href="#audios", cta2=("Ver cursos", "#cursos")) + f"""
<section class="pad-s"><div class="wrap grid g2" style="align-items:start">
  <div><span class="kicker fade">Cómo funcionan los audios</span><h2 class="display-m lines" style="margin:14px 0 20px">Ponte tus audífonos, recuéstate<br>y nosotros nos encargamos del resto.</h2><p class="fade d1">Es como una meditación guiada, pero en los primeros 3 minutos te guío a un estado de hipnosis. Así el audio llega a tu subconsciente, donde se guardan tus creencias y emociones, y reemplaza patrones negativos por creencias positivas y empoderadoras.</p></div>
  <div class="stats fade d1"><div class="stat bg-blush" style="border:0"><b>15–20</b><span>Minutos al día</span><p>Solo necesitas un espacio para relajarte.</p></div><div class="stat bg-sand" style="border:0"><b>21</b><span>Días mínimo</span><p>Lo que tarda tu mente en crear nuevos hábitos.</p></div><div class="stat bg-aqua" style="border:0"><b>100%</b><span>Seguro</span><p>Estás consciente y en control todo el tiempo.</p></div></div>
</div></section>
<section id="cursos" class="pad-s bg-stone"><div class="wrap">{sec_title("Cursos")}{courses_html()}</div></section>
<section id="audios" class="pad-s"><div class="wrap">{sec_title("Audios de autohipnosis")}<div class="chips" data-chips><button class="chip on" data-cat="all">Todos</button>{''.join(f'<button class="chip" data-cat="{c}">{n}</button>' for c, n, _ in AUDIO_CATS)}</div><div data-shop></div></div></section>
<section class="pad-s bg-blush"><div class="wrap" style="display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap"><div><span class="kicker fade">¿Quieres algo hecho solo para ti?</span><h2 class="display-m lines" style="margin:12px 0 10px">Tu audio personal llega con tu sesión de RTT.</h2><p class="fade d1" style="margin:0;max-width:60ch">En cada sesión de RTT creo un audio de transformación personal, diseñado para tu historia y tus objetivos.</p></div><a class="pill solid fade d2" href="/agenda/"><span>Agenda tu sesión</span></a></div></section>
{testi(bg="")}
""", cta=False)

# ------------------------------------------------------------------ PRODUCT PAGES
CATN = {c: n for c, n, _ in AUDIO_CATS}
for p in PRODUCTS:
    others = [x for x in PRODUCTS if x['id'] != p['id']][:3]
    rel = ''.join(f'<a class="disc fade d{i}" href="/shop/{x["slug"]}/"><div class="disc__art"><img src="{x["cover"]}" alt="{x["name"]}" loading="lazy"><span class="disc__hole"></span></div><h4>{x["name"]}</h4><div class="price">{fmt(x["price"])}</div></a>' for i, x in enumerate(others))
    pages[f"/shop/{p['slug']}/"] = dict(title=f"{p['name']} · Audio de autohipnosis | Space to Rise", desc=p['short'].strip()[:155],
     body=f"""<section class="portal pad-s"><div class="wrap feature">
  <div class="feature__media"><div class="media square"><img src="{p['cover']}" alt="{p['name']}"><div class="mask"></div></div></div>
  <div><span class="kicker fade">Shop / {CATN.get(p['category'], '')}</span><h1 class="display-m lines" style="margin:14px 0 18px">{p['name']}</h1><p class="lead fade d1">{p['description']}</p>
    <div class="price-tag fade d2">{fmt(p['price'])}<small>COP</small></div>
    <ul class="list fade d2" style="margin:0 0 26px"><li>Audio de autohipnosis de 15 a 20 minutos</li><li>Acceso inmediato en tu espacio privado, para escuchar donde quieras</li><li>Pensado para escucharlo cada día durante 21 días</li></ul>
    <div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap"><a class="pill solid" href="/checkout/?p={p['id']}"><span>Compra aquí</span></a><button class="pill" data-add="{p['id']}"><span>Añadir al carrito</span></button><a class="pill" href="/preguntas-frecuentes/" style="opacity:.8"><span>¿Tienes dudas?</span></a></div></div>
</div></section>
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Cómo usar tu audio")}{steps3([("Busca tu espacio", "Un lugar tranquilo donde puedas recostarte y desconectarte de 15 a 20 minutos."), ("Ponte tus audífonos", "Déjate guiar: en los primeros minutos entras en un estado de relajación profunda."), ("Repite 21 días", "La mente aprende por repetición. Escúchalo cada día para crear nuevos hábitos.")])}</div></section>
<section class="pad-s"><div class="wrap grid g2" style="align-items:start"><div><span class="kicker fade">Hipnosis 100% segura</span><h2 class="display-s lines" style="margin:12px 0 0">Estás consciente todo el tiempo.</h2></div><div><p class="fade">Puedes entrar y salir de la hipnosis muy fácilmente. Tu mente simplemente está más receptiva a las sugerencias que son buenas para ti.</p><p class="small muted fade d1">RTT es un acompañamiento complementario y no reemplaza el diagnóstico ni el tratamiento médico.</p></div></div></section>
<section class="pad-s bg-sand"><div class="wrap">{sec_title("Conoce otros audios", ("Ir al shop", "/shop/#audios"))}<div class="discs">{rel}</div></div></section>
""", cta=False)

# ------------------------------------------------------------------ CHECKOUT / PORTAL
pages["/checkout/"] = dict(title="Finalizar compra | Space to Rise", desc="Finaliza tu compra de audios de autohipnosis.", portal=True,
 body=f"""<section class="portal pad-s"><div class="wrap grid g2" data-checkout style="align-items:start">
  <div><span class="kicker fade">Tu pedido</span><h1 class="display-m lines" style="margin:14px 0 24px">Casi listo.</h1><div data-co-items></div><div class="drawer__total" style="margin-top:20px"><span>Total</span><b data-co-total></b></div></div>
  <div>
    <div data-co-form><p class="lead fade">Déjanos el correo donde quieres recibir tu acceso. Después de confirmar el pago, te llega un enlace mágico para entrar a tu espacio privado y escuchar tus audios.</p>
    <form class="fade d1"><div class="field"><label for="email">Tu correo</label><input id="email" name="email" type="email" required placeholder="nombre@correo.com" autocomplete="email"></div><button class="pill solid" type="submit"><span>Crear pedido</span></button><p class="small muted" style="margin-top:14px">Pagos por Nequi, transferencia o tarjeta, confirmados por WhatsApp con Andrea. Muy pronto: pago en línea.</p></form></div>
    <div data-co-result></div>
  </div>
</div></section>""", cta=False)

pages["/mi-cuenta/"] = dict(title="Mi cuenta | Space to Rise", desc="Entra a tu espacio privado con un enlace mágico.", portal=True,
 body=f"""<section class="portal pad-s"><div class="wrap grid g2" data-login style="align-items:center">
  <div><span class="kicker fade">Tu espacio privado</span><h1 class="display-l lines" style="margin:14px 0 20px">Entra con un<br>enlace mágico.</h1><p class="lead fade d1">Sin contraseñas. Escribe tu correo, ábrelo y toca el enlace: entras directo a tus audios.</p>
    <form class="fade d2" style="max-width:420px"><div class="field"><label for="email">Tu correo</label><input id="email" name="email" type="email" required placeholder="nombre@correo.com" autocomplete="email"></div><button class="pill solid" type="submit"><span>Enviarme el enlace</span></button></form><div data-login-out style="margin-top:20px;max-width:480px"></div></div>
  <div class="media square"><img src="{IMG}Recupera-tu-amor-propio-scaled.jpg" alt="" loading="lazy"><div class="mask"></div></div>
</div></section>""", cta=False)

pages["/mis-audios/"] = dict(title="Mis audios | Space to Rise", desc="Tus audios de autohipnosis.", portal=True,
 body=f"""<section class="portal pad-s"><div class="wrap" data-my-audios>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;margin-bottom:30px"><div><span class="kicker fade">Mis audios</span><h1 class="display-m lines" style="margin-top:14px">Tu espacio para escuchar.</h1><p class="small muted fade d1" style="margin:10px 0 0" data-who></p></div><div style="display:flex;gap:10px"><a class="pill" href="/shop/#audios"><span>Más audios</span></a><button class="pill" data-logout><span>Salir</span></button></div></div>
  <div data-my-out></div><div data-tracks></div>
  <p class="small muted" style="margin-top:34px;max-width:60ch">Recomendación: escucha tu audio con audífonos, en un lugar tranquilo donde puedas relajarte 15–20 minutos, todos los días durante 21 días. No lo escuches mientras conduces.</p>
</div></section>
<div class="player"><button class="toggle track" style="display:grid;grid-template-columns:auto;padding:0;border:0"><span class="play" aria-label="Pausar / reproducir"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></button><div><div class="title">—</div><div class="bar"><i></i></div></div><div class="time">0:00 / 0:00</div></div>""", cta=False)

pages["/admin/"] = dict(title="Panel | Space to Rise", desc="Panel de administración.", portal=True,
 body=f"""<section class="portal pad-s"><div class="wrap" data-admin>
  <span class="kicker fade">Panel de Andrea</span><h1 class="display-m lines" style="margin:14px 0 8px">Pedidos y accesos.</h1><p class="muted fade d1" style="max-width:60ch">Cuando confirmes un pago, marca el pedido como pagado: se activan los audios y el cliente recibe su enlace mágico por correo. También puedes dar acceso manual a cualquier correo.</p>
  <div data-admin-out style="margin:18px 0"></div>
  <div class="grid g2" style="align-items:start;margin-top:30px">
    <div><h3 class="display-s" style="margin-bottom:16px">Pedidos recientes</h3><div data-admin-orders><p class="muted">Cargando…</p></div></div>
    <div><h3 class="display-s" style="margin-bottom:16px">Dar acceso manual</h3><form><div class="field"><label for="email">Correo del cliente</label><input id="email" name="email" type="email" required placeholder="cliente@correo.com"></div><div class="field"><label>Audios</label><div data-admin-products class="small"></div></div><button class="pill solid" type="submit"><span>Activar y enviar enlace</span></button></form></div>
  </div>
</div></section>""", cta=False)

# ------------------------------------------------------------------ SOBRE MÍ
pages["/sobre-mi/"] = dict(title="Sobre mí — Andrea Zafra, hipnoterapeuta clínica RTT y consultora NCS | Space to Rise",
 desc="Hipnoterapeuta clínica especializada en RTT y consultora certificada de Joe Dispenza (NeuroChangeSolutions). Mi historia, mi formación y mi misión.",
 body=f"""<section class="portal pad"><div class="wrap feature">
  <div><span class="kicker fade">Sobre mí</span><h1 class="display-xl lines" style="margin:14px 0 18px">Andrea<br>Zafra</h1><p class="kicker fade d1" style="display:block;margin-bottom:20px;line-height:2">Hipnoterapeuta clínica especializada en RTT<br>Consultora certificada de Joe Dispenza (NeuroChangeSolutions)</p>
    <p class="lead fade d2">Te ayudo a encontrar la raíz de lo que te bloquea y a reprogramar tu mente para que tu cambio sea real y permanente. Uno la hipnoterapia, la neurociencia del cambio y más de 10 años de experiencia para acompañar a personas, familias y organizaciones.</p>
    <div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap"><a class="pill solid" href="/agenda/"><span>Agenda tu cita</span></a><a class="pill" href="#historia"><span>Conoce mi historia</span></a></div></div>
  <div class="feature__media"><div class="media"><img src="{IMG}AdreaZafra.jpg" alt="Andrea Zafra"><div class="mask"></div></div></div>
</div></section>
<section class="pad-s bg-aqua"><div class="wrap">{sec_title("Formación y certificaciones")}<div class="tiles" style="grid-template-columns:repeat(5,1fr);gap:0 28px">
  <div class="fade"><b class="display-m" style="display:block">+10</b><span class="kicker" style="margin:6px 0 10px;display:block">Años de experiencia</span><p class="small" style="margin:0">Acompañando procesos de sanación y transformación personal.</p></div>
  <div class="fade d1"><b class="display-m" style="display:block">RTT</b><span class="kicker" style="margin:6px 0 10px;display:block">Hipnoterapeuta clínica</span><p class="small" style="margin:0">Especializada en Rapid Transformational Therapy, el método creado por Marisa Peer.</p></div>
  <div class="fade d2"><b class="display-m" style="display:block">NCS</b><span class="kicker" style="margin:6px 0 10px;display:block">Consultora certificada</span><p class="small" style="margin:0">NeuroChangeSolutions, formada por el Dr. Joe Dispenza en la neurociencia del cambio.</p></div>
  <div class="fade d3"><b class="display-m" style="display:block">MBA</b><span class="kicker" style="margin:6px 0 10px;display:block">IE Business School</span><p class="small" style="margin:0">Instituto de Empresa, Madrid.</p></div>
  <div class="fade d4"><b class="display-m" style="display:block">BSBA</b><span class="kicker" style="margin:6px 0 10px;display:block">Babson College</span><p class="small" style="margin:0">Licenciada en Administración de Empresas, Estados Unidos.</p></div>
</div><p class="kicker fade" style="margin-top:36px;display:block;text-align:center">Estudios complementarios · Crianza consciente · Nutrición · Energía · Mindfulness · Yoga</p></div></section>
<section id="historia" class="pad"><div class="wrap">{sec_title("Mi historia")}<div class="grid g2" style="align-items:start">
  <div><h2 class="display-m lines" style="margin:0 0 22px">Dicen que los hijos son nuestros grandes maestros, y en mi caso es así.</h2><p class="fade">Jerónimo, Olivia y Alexa despertaron en mí una pregunta que cambió mi vida: ¿cómo me convierto en la mejor versión de mí misma para ser su ejemplo?</p><p class="fade d1">Durante años construí una carrera exitosa. Estudié Administración de Empresas en Babson College, hice mi MBA en el IE, trabajé en grandes multinacionales y fundé varios negocios. Pero con la llegada de Alexa mi mundo dio un giro que me reconectó con mi verdadera esencia.</p></div>
  <div><p class="fade">Dejé el mundo corporativo para aprender todo lo que pudiera sobre crianza consciente, nutrición, energía, mindfulness y yoga. En el camino entendí algo que lo cambió todo: para darles a mis hijos lo que quería para ellos, primero tenía que transformarme yo. Superar mis miedos, cuestionar mis creencias y sanar mi cuerpo.</p><p class="fade d1">Esa búsqueda me llevó a la Terapia de Transformación Rápida (RTT) de Marisa Peer y a la neurociencia del cambio del Dr. Joe Dispenza. Hoy uso estas herramientas para acompañar a otros en su propio camino de sanación.</p><div class="media wide fade d2" style="margin-top:22px"><img src="{IMG}Andrea-Zafra-Coach-scaled.jpeg" alt="" loading="lazy" style="object-position:center 20%"><div class="mask"></div></div></div>
</div></div></section>
<section class="quote-band bg-taupe" data-dark><div class="wrap"><p class="fade">“No podemos ofrecer al mundo algo que no somos.”</p><cite class="fade d1">Andrea Zafra</cite></div></section>
<section id="mision" class="pad"><div class="wrap">
  <div class="grid g2" style="align-items:start"><div><span class="kicker fade">Mi misión</span><h2 class="display-m lines" style="margin:14px 0 0">Despertar el potencial humano de millones de personas, de adentro hacia afuera.</h2></div><div><p class="lead fade">Acompaño a personas, familias y organizaciones a liberarse de las creencias limitantes y los programas desactualizados que las enferman, las bloquean y les impiden ser su mejor versión.</p><p class="fade d1">Para lograrlo uno dos caminos que se potencian: la hipnoterapia RTT, que llega a la raíz en el subconsciente, y la neurociencia del cambio del Dr. Joe Dispenza, que enseña cómo el cerebro y el cuerpo crean nuevos hábitos y los sostienen en el tiempo.</p></div></div>
  <div class="tiles" style="margin-top:clamp(36px,5vw,64px)">
    <div class="tile bg-blush fade" style="min-height:0"><span class="tag" style="margin:0 0 10px">Personas</span><p>Que cada persona sane su cuerpo y su mente, recupere su poder interior y alcance lo que sueña.</p></div>
    <div class="tile bg-sand fade d1" style="min-height:0"><span class="tag" style="margin:0 0 10px">Familias</span><p>Que los padres críen nuevas generaciones libres de miedos, con autoestima alta y alas fuertes para volar alto.</p></div>
    <div class="tile bg-aqua fade d2" style="min-height:0"><span class="tag" style="margin:0 0 10px">Empresas</span><p>Que líderes y equipos sean más conscientes, sanos y creativos, capaces de adaptarse al cambio y crecer juntos.</p></div>
  </div>
  <p class="caps fade" style="margin:clamp(40px,5vw,64px) auto 8px;text-align:center">Porque cuando una persona se transforma, transforma su familia, su equipo y su entorno.</p>
  <p class="display-s fade d1" style="text-align:center;margin:0;font-style:italic">¡Al despertar tu mundo, iluminas el mundo!</p>
</div></section>
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Cómo puedo acompañarte")}<div class="tiles">
  <a class="tile fade" href="/heal-rise-shine/" style="background:var(--white);min-height:0"><span class="tag" style="margin:0 0 10px">Personas</span><h3>Heal · Rise · Shine</h3><p>Sesiones de RTT para sanar tu cuerpo, liberar tu mente y alcanzar tus objetivos.</p><span class="tag">Conoce más →</span></a>
  <a class="tile fade d1" href="/kids/" style="background:var(--white);min-height:0"><span class="tag" style="margin:0 0 10px">Familias</span><h3>Kids</h3><p>Herramientas para que tus hijos crezcan con una autoestima alta, libres de miedos y creencias limitantes.</p><span class="tag">Conoce más →</span></a>
  <a class="tile fade d2" href="/empresas/" style="background:var(--white);min-height:0"><span class="tag" style="margin:0 0 10px">Empresas</span><h3>Bienestar corporativo</h3><p>Talleres, retiros y el programa NCS del Dr. Joe Dispenza para equipos y líderes.</p><span class="tag">Conoce más →</span></a>
</div></div></section>
""", cta_title="Me encantaría acompañarte", cta_sub="Agenda una llamada inicial y conversemos sobre lo que quieres transformar.")

# ------------------------------------------------------------------ GIFT
pages["/gif-for-you/"] = dict(title="Gift for you — Recursos gratuitos | Space to Rise",
 desc="Audios y PDFs gratuitos para inspirarte y acompañarte: descarga los tips para reducir la ansiedad y la depresión.",
 body=hero(IMG + "Ansiedad-y-Depresion.jpg", "Gift for you", "Recursos exclusivos, solo para ti.", kicker="Gratis", pos="center 30%", cta=False) + f"""
<section class="pad"><div class="wrap feature">
  <div><p class="lead fade">Descubre nuestra colección de audios y PDFs gratuitos, pensados para inspirarte, impulsarte y acompañarte en cada paso.</p><p class="fade d1">Porque en Space to Rise creemos que el conocimiento debe estar al alcance de todos. ¡Empieza hoy mismo!</p></div>
  <div class="feature__media"><div class="media wide"><img src="{IMG}Ansiedad-y-Depresion.jpg" alt="" loading="lazy"><div class="mask"></div></div><h3 class="display-s" style="margin-top:22px">Tips para reducir la ansiedad y la depresión</h3><p class="small muted" style="margin:8px 0 18px">Guía en PDF con herramientas efectivas que puedes aplicar en tu día a día.</p><a class="pill solid" href="/assets/doc/Depresion-y-Ansiedad.pdf" download><span>Descarga aquí</span></a></div>
</div></section>""")

# ------------------------------------------------------------------ FAQ
FAQ = [
 ("Sobre RTT", [
  ("¿Qué es RTT?", "Rapid Transformational Therapy es una terapia desarrollada por Marisa Peer que combina lo más eficaz de la hipnosis, la PNL y la neurociencia para lograr resultados rápidos, permanentes y transformadores. Generalmente se logra sanar en 1 o máximo 3 sesiones, según la complejidad del tema."),
  ("¿Por qué hipnosis?", "La hipnosis permite acceder al subconsciente, donde están tu programación, tus memorias y tus creencias. Así entendemos por qué reaccionas como reaccionas, encontramos la raíz del problema, la sanamos y creamos nuevas conexiones neuronales."),
  ("¿Por qué RTT es tan efectiva?", "Porque cambia tus creencias a nivel subconsciente. La mente consciente es la parte lógica, pero el subconsciente maneja cerca del 95% de nuestras decisiones: hasta que no lo cambias, ningún cambio es real y permanente."),
  ("¿Qué puedo sanar y transformar con RTT?", "Temas físicos como enfermedades crónicas y problemas de piel, pelo o digestivos; temas emocionales como ansiedad, estrés, autoestima, fobias, adicciones, insomnio, control de peso, fertilidad y relaciones; y temas de desempeño como metas y rendimiento deportivo. Es apta para niños y adultos, y complementa, no reemplaza, el tratamiento médico.")]),
 ("Las sesiones", [
  ("¿Cómo son las sesiones de RTT?", "Tienen 3 partes: una llamada de 20 minutos para aclarar dudas; la terapia, de 1:30 a 2 horas, donde con hipnosis vamos a la raíz del problema y lo liberamos; y un audio personalizado de 15 a 20 minutos que escuchas cada día durante al menos 21 días."),
  ("¿Cuánto tiempo dura la sesión?", "Entre 90 minutos y 2 horas. Te recomiendo reservar 2 horas en tu calendario para no estar apurada."),
  ("¿Qué pasa si necesito otra sesión?", "Algunos temas más profundos pueden requerir hasta tres sesiones. Muchos clientes continúan con sesiones para otras áreas de su vida o con coaching para integrar sus nuevas creencias y hábitos.")]),
 ("La hipnosis", [
  ("¿Cómo se siente estar hipnotizado?", "La mayoría de las personas se siente muy relajada. Estás 100% en control de tu cuerpo: puedes hablar, moverte o acomodarte cuando quieras, y solo aceptas las sugerencias que tú quieras."),
  ("¿Puedo quedarme atrapado en la hipnosis?", "No. Tienes control completo durante toda la sesión. Si haces tu sesión por Zoom y se corta la llamada, como mucho te quedarás dormido por la relajación y luego abrirás los ojos."),
  ("¿Cómo funciona?", "La hipnosis no es magia: se basa en principios científicos. Al relajarte, tu cerebro produce ondas alfa, parecidas a las del sueño, que permiten acceder al subconsciente. Es simple y posible para todo el mundo."),
  ("¿Qué pasa si veo escenas dolorosas?", "No las revives, las observas desde un lugar seguro y desde tu perspectiva adulta. Estaré a tu lado todo el tiempo para que puedas expresar tus emociones y sanar."),
  ("¿Qué pasa si no entro suficientemente profundo?", "La profundidad del trance no es crucial para los resultados. La efectividad no depende de qué tan profundo vayas.")]),
 ("Resultados", [
  ("¿Cómo se ven los resultados?", "De tres formas: inmediatos, cuando sales sintiéndote liviana y en paz; progresivos, en 10 a 21 días mientras dejas atrás viejos hábitos; y retroactivos, cuando son otros quienes notan el cambio primero."),
  ("¿Qué pasa si ya conozco el motivo de mi problema?", "RTT suele mostrar una perspectiva nueva sobre problemas conocidos y te permite cambiar su significado. Relájate y confía en que tu subconsciente te mostrará lo necesario.")]),
]
faq_html = ''.join(f'<div class="grid g2 fade" style="grid-template-columns:.6fr 1.4fr;align-items:start;padding:34px 0;border-top:1px solid rgba(58,58,57,.16)"><span class="kicker">{g}</span><div class="acc">' + ''.join(f'<div class="acc__item"><button class="acc__q">{q}<i></i></button><div class="acc__a"><div><div class="inner"><p>{a}</p></div></div></div></div>' for q, a in qs) + '</div></div>' for g, qs in FAQ)
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for g, qs in FAQ for q, a in qs]}, ensure_ascii=False)
pages["/preguntas-frecuentes/"] = dict(title="Preguntas frecuentes — Todo lo que quieres saber sobre RTT | Space to Rise",
 desc="¿Cómo se siente estar hipnotizado? ¿Cuánto dura una sesión de RTT? ¿Cuándo veo resultados? Respuestas a las dudas más comunes.",
 body=f"""<section class="portal pad-s"><div class="wrap">
  <div class="narrow center" style="margin:0 auto clamp(40px,6vw,72px)"><span class="kicker fade">Preguntas frecuentes</span><h1 class="display-l lines" style="margin:14px 0 18px">Todo lo que quieres saber sobre RTT</h1><p class="muted fade d1">Si no encuentras tu respuesta aquí, escríbeme a <a href="mailto:info@spacetorise.com" style="text-decoration:underline">info@spacetorise.com</a> o agenda tu llamada inicial.</p></div>
  {faq_html}
</div></section><script type="application/ld+json">{faq_ld}</script>""", cta_title="¿Te quedó alguna duda?", cta_sub="En la llamada inicial de 20 minutos resolvemos todas tus preguntas.")

# ------------------------------------------------------------------ AGENDA
pages["/agenda/"] = dict(title="Agenda tu cita — Solicita tu llamada inicial | Space to Rise",
 desc="Cuéntame qué te gustaría transformar y te contacto para agendar una llamada inicial de 20 minutos, sin compromiso.",
 body=f"""<section class="portal pad-s"><div class="wrap grid g2" style="align-items:start">
  <div><span class="kicker fade">Agenda tu cita</span><h1 class="display-l lines" style="margin:14px 0 18px">Tu transformación empieza con una conversación.</h1><p class="fade d1">Cuéntame qué te gustaría transformar y te contacto para agendar una llamada inicial de 20 minutos, sin compromiso, para resolver tus dudas y elegir juntas el mejor camino.</p>
    <div class="steps fade d2" style="margin-top:26px"><div class="step" style="grid-template-columns:48px 1fr;padding:20px 0"><div class="n">01</div><div><h4>Envía tu solicitud</h4><p>Completa el formulario o escríbeme por WhatsApp.</p></div></div><div class="step" style="grid-template-columns:48px 1fr;padding:20px 0"><div class="n">02</div><div><h4>Llamada inicial</h4><p>20 minutos para conocernos y aclarar tus preguntas.</p></div></div><div class="step" style="grid-template-columns:48px 1fr;padding:20px 0"><div class="n">03</div><div><h4>Tu sesión</h4><p>Presencial o por Zoom, en el horario que mejor te funcione.</p></div></div></div></div>
  {lead_form("agenda", [("name", "Nombre", "text", None), ("email", "Correo", "email", None), ("phone", "WhatsApp", "tel", None), ("city", "País y ciudad", "text", None), ("service", "Servicio", "select", ["Sesión de RTT", "RTT Kids", "Coaching individual", "Baño de gong", "Aún no lo sé"]), ("message", "¿Qué te gustaría transformar?", "textarea", None)], "Enviar solicitud", intro="Solicita tu llamada inicial", extra=f'<a class="pill" href="{WA}" target="_blank" rel="noopener" style="margin-left:10px"><span>O escríbeme por WhatsApp</span></a>')}
</div></section>
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Servicios y valores")}<div class="tiles c4">
  <div class="pricecard bg-blush fade"><span class="k">Personas</span><h4>Sesión de RTT</h4><p>Sesión de 90 min a 2 h con tu audio personal de 21 días.</p><b>$450.000</b></div>
  <div class="pricecard bg-rose fade d1"><span class="k">Niños</span><h4>RTT Kids</h4><p>Sesión adaptada a la edad de tu hijo, con su audio personal.</p><b>$350.000</b></div>
  <div class="pricecard bg-aqua fade d2"><span class="k">Integración</span><h4>Coaching individual</h4><p>Sesión de 1 hora, presencial o por Zoom.</p><b>$150.000</b></div>
  <div class="pricecard bg-sky fade d3"><span class="k">Sonido</span><h4>Baño de gong</h4><p>Individual o grupal, para ti, tu familia o tu equipo.</p><b>$150.000 <small style="font-size:.5em">· $100.000 p/p grupal</small></b></div>
</div><p class="fade" style="margin:28px 0 0">¿Buscas algo para tu empresa? <a href="/empresas/" style="text-decoration:underline">Conoce los programas para empresas →</a></p></div></section>
{testi(bg="")}
""", cta=False)

# ------------------------------------------------------------------ BUILD
for path, p in pages.items():
    d = os.path.join(OUT, path.strip('/')) if path != '/' else OUT
    os.makedirs(d, exist_ok=True)
    fkw = {k: p[k] for k in ('cta', 'cta_title', 'cta_sub', 'cta_btn', 'cta_href') if k in p}
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(head(p['title'], p['desc'], path, portal=p.get('portal', False)) + p['body'] + foot(**fkw))
    print('wrote', path)
pub = [p for p, v in pages.items() if not v.get('portal')]
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>https://spacetorise.com{p}</loc></url>' for p in pub) + '</urlset>')
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /mis-audios/\nSitemap: https://spacetorise.com/sitemap.xml\n')
