# -*- coding: utf-8 -*-
"""Space to Rise v2 — generador de páginas."""
import os, json, html, re

OUT = os.path.dirname(os.path.abspath(__file__))
WA = "https://wa.me/573107503359?text=Hola!%20Quiero%20reservar%20mi%20cita%20%F0%9F%98%8A"
IMG = "/assets/img/"
import hashlib, time
VER = hashlib.md5(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/css/site.css'),'rb').read() + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/js/site.js'),'rb').read() + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/data/products.json'),'rb').read() + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/js/shop.js'),'rb').read()).hexdigest()[:8]
SPIRAL = open(os.path.join(OUT, 'assets/img/spiral-path.txt')).read().strip()
OG_BASE = os.environ.get("SITE_BASE", "https://spacetorise-site.vercel.app")  # cambiar a https://spacetorise.com al conectar el dominio
SUPA_URL = "https://epsokxvjqevmityasvrx.supabase.co"
SUPA_KEY = "sb_publishable_m4rurqAuHs8cHJfBq3bshQ_-4decACD"

NAV = [("RTT", "/rtt/"), ("Heal · Rise · Shine", "/heal-rise-shine/"), ("Kids", "/kids/"), ("Coaching", "/coaching/"), ("Gong", "/gong/"), ("Empresas", "/empresas/"), ("Shop", "/shop/"), ("Sobre mí", "/sobre-mi/")]
MENU = NAV + [("Preguntas frecuentes", "/preguntas-frecuentes/"), ("Agenda tu cita", "/agenda/"), ("Mi cuenta", "/mi-cuenta/")]
AG = "/agenda/"
ENTITY = "Space to Rise es un human evolution studio con sede en Bogotá, Colombia, fundado por la hipnoterapeuta clínica Andrea Zafra. Ofrece hipnoterapia RTT (Rapid Transformational Therapy, el método de Marisa Peer), coaching individual, baños de gong, audios de autohipnosis y programas de bienestar para empresas basados en la neurociencia del cambio del Dr. Joe Dispenza, de forma presencial en Bogotá y online."

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


def head(title, desc, path, dark=False, portal=False, og=None, ld=None):
    parts = [p for p in path.strip('/').split('/') if p]
    names = {"rtt": "RTT", "heal-rise-shine": "Heal · Rise · Shine", "kids": "Kids", "coaching": "Coaching", "gong": "Gong", "empresas": "Empresas", "shop": "Shop", "sobre-mi": "Sobre mí", "preguntas-frecuentes": "Preguntas frecuentes", "agenda": "Agenda tu cita", "gif-for-you": "Gift for you"}
    items = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://spacetorise.com/"}]
    acc = ''
    for i, p in enumerate(parts):
        acc += '/' + p
        items.append({"@type": "ListItem", "position": i + 2, "name": names.get(p, title.split(' | ')[0].split(' · ')[0]), "item": f"https://spacetorise.com{acc}/"})
    crumbs = (',' + json.dumps({"@type": "BreadcrumbList", "itemListElement": items}, ensure_ascii=False)) if parts and not portal else ''
    return f"""<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://spacetorise.com{path}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{OG_BASE}{og or "/assets/img/og-home.jpg"}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Space to Rise · Hipnoterapia RTT en Bogotá y online"><meta property="og:site_name" content="Space to Rise"><meta property="og:url" content="{OG_BASE}{path}"><meta name="twitter:card" content="summary_large_image"><meta property="og:type" content="website"><meta property="og:locale" content="es_CO">
{'<meta name="robots" content="noindex">' if portal else ''}
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png"><link rel="apple-touch-icon" href="/assets/img/favicon-180.png">
<link rel="preload" href="/assets/fonts/gabriela-light.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
<script src="/assets/js/vendor/gsap.min.js" defer></script>
<script src="/assets/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="/assets/js/vendor/lenis.min.js" defer></script>
{'<script src="/assets/js/vendor/supabase.js" defer></script>' if portal else ''}
<script>window.STR_SUPABASE_URL="{SUPA_URL}";window.STR_SUPABASE_KEY="{SUPA_KEY}";</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":["Organization","HealthAndBeautyBusiness"],"@id":"https://spacetorise.com/#org","name":"Space to Rise","alternateName":["Space to Rise · Human Evolution Studio","Space to Rise Bogotá"],"url":"https://spacetorise.com","logo":"https://spacetorise.com/assets/img/Logo2x.png","image":"https://spacetorise.com/assets/img/p/home-hero-3.jpg","description":{json.dumps(ENTITY, ensure_ascii=False)},"slogan":"Journey inward & rise from your heart","telephone":"+57 310 750 3359","email":"info@spacetorise.com","address":{{"@type":"PostalAddress","addressLocality":"Bogotá","addressRegion":"Cundinamarca","addressCountry":"CO"}},"areaServed":[{{"@type":"City","name":"Bogotá"}},{{"@type":"Country","name":"Colombia"}},"Online"],"priceRange":"$$","founder":{{"@id":"https://spacetorise.com/#andrea"}},"knowsAbout":["Hipnoterapia","Rapid Transformational Therapy","Hipnosis clínica","Neurociencia del cambio","Coaching","Baño de gong","Bienestar laboral"],"sameAs":["https://www.instagram.com/spacetorise/","https://www.youtube.com/@spacetorise","https://www.facebook.com/profile.php?id=61574483459317","https://www.linkedin.com/in/andrea-zafra-5b5bb09"],"makesOffer":[{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"Sesión de hipnoterapia RTT","url":"https://spacetorise.com/rtt/"}},"price":"480000","priceCurrency":"COP"}},{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"RTT Kids · hipnoterapia para niños","url":"https://spacetorise.com/kids/"}},"price":"350000","priceCurrency":"COP"}},{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"Coaching individual","url":"https://spacetorise.com/coaching/"}},"price":"180000","priceCurrency":"COP"}},{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"Baño de gong individual","url":"https://spacetorise.com/gong/"}},"price":"180000","priceCurrency":"COP"}},{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"Programas de bienestar laboral para empresas","url":"https://spacetorise.com/empresas/"}}}}]}},{{"@type":"Person","@id":"https://spacetorise.com/#andrea","name":"Andrea Zafra","url":"https://spacetorise.com/sobre-mi/","image":"https://spacetorise.com/assets/img/p/andrea.jpg","jobTitle":"Hipnoterapeuta clínica RTT y consultora certificada NeuroChangeSolutions","worksFor":{{"@id":"https://spacetorise.com/#org"}},"alumniOf":[{{"@type":"CollegeOrUniversity","name":"IE Business School"}},{{"@type":"CollegeOrUniversity","name":"Babson College"}}],"hasCredential":[{{"@type":"EducationalOccupationalCredential","name":"Rapid Transformational Therapy (RTT) · Marisa Peer"}},{{"@type":"EducationalOccupationalCredential","name":"Consultora certificada NeuroChangeSolutions · Dr. Joe Dispenza"}}],"sameAs":["https://www.linkedin.com/in/andrea-zafra-5b5bb09","https://www.instagram.com/spacetorise/"]}},{{"@type":"WebSite","@id":"https://spacetorise.com/#web","url":"https://spacetorise.com","name":"Space to Rise","inLanguage":"es-CO","publisher":{{"@id":"https://spacetorise.com/#org"}}}},{{"@type":"WebPage","url":"https://spacetorise.com{path}","name":{json.dumps(title, ensure_ascii=False)},"description":{json.dumps(desc, ensure_ascii=False)},"inLanguage":"es-CO","isPartOf":{{"@id":"https://spacetorise.com/#web"}},"about":{{"@id":"https://spacetorise.com/#org"}}}}{crumbs}]}}</script>
{ld or ""}
</head>
<body>
<div class="loader" aria-hidden="true">
  <div class="loader__stage">
    <div class="loader__word"><img src="/assets/img/Logo_Blanco_Full.png" alt="Space to Rise" style="filter:invert(1) brightness(.42)"></div>
    <div class="loader__line"></div>
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
    <div class="big"><img src="/assets/img/Logo_Blanco_Full.png" alt="Space to Rise" loading="lazy"></div>
    <div class="cols">
      <div>
        <h5>Human evolution studio</h5>
        <p style="max-width:40ch;margin:0">Journey inward &amp; rise from your heart. Human evolution studio en Bogotá, Colombia: hipnoterapia RTT, coaching, baños de gong, audios de autohipnosis y bienestar para empresas, presencial y online.</p>
        <div class="social"><a href="https://www.instagram.com/spacetorise/" target="_blank" rel="noopener" aria-label="Instagram">{SVG_IG}</a><a href="https://www.youtube.com/@spacetorise" target="_blank" rel="noopener" aria-label="YouTube">{SVG_YT}</a><a href="https://www.facebook.com/profile.php?id=61574483459317" target="_blank" rel="noopener" aria-label="Facebook">{SVG_FB}</a><a href="https://www.linkedin.com/in/andrea-zafra-5b5bb09" target="_blank" rel="noopener" aria-label="LinkedIn">{SVG_IN}</a></div>
      </div>
      <div><h5>Explora</h5><ul><li><a href="/rtt/">RTT</a></li><li><a href="/heal-rise-shine/">Heal · Rise · Shine</a></li><li><a href="/kids/">Kids</a></li><li><a href="/coaching/">Coaching</a></li><li><a href="/gong/">Gong</a></li><li><a href="/empresas/">Empresas</a></li><li><a href="/shop/">Shop</a></li></ul></div>
      <div><h5>Space to Rise</h5><ul><li><a href="/sobre-mi/">Sobre mí</a></li><li><a href="/sobre-mi/#mision">Misión</a></li><li><a href="/preguntas-frecuentes/">Preguntas frecuentes</a></li><li><a href="/gif-for-you/">Gift for you</a></li><li><a href="/agenda/">Agenda tu cita</a></li><li><a href="/mi-cuenta/">Mi cuenta</a></li></ul></div>
      <div><h5>Contacto</h5><ul><li><a href="mailto:info@spacetorise.com">info@spacetorise.com</a></li><li><a href="https://www.instagram.com/spacetorise/" target="_blank" rel="noopener">@spacetorise</a></li><li><a href="{WA}" target="_blank" rel="noopener">WhatsApp +57 310 750 3359</a></li><li>Bogotá · Colombia · Online</li></ul></div>
    </div>
    <div class="bottom"><span>© 2026 Space to Rise · Andrea Zafra</span><span>Al despertar tu mundo, iluminas el mundo.</span><span><a class="credit" href="https://clicalto.com" target="_blank" rel="noopener">Site by Clicalto</a></span></div>
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
<script src="/assets/js/site.js?v={VER}" defer></script>
<script src="/assets/js/shop.js?v={VER}" defer></script>
<script src="/assets/js/portal.js?v={VER}" defer></script>
</body>
</html>
"""


def hero(img, h1, sub=None, kicker=None, light=False, compact=True, video=None, pos="center", cta=True, cta2=None, btn="Agenda tu cita", href="/agenda/", alt=None):
    alt = alt or re.sub("<[^>]+>", " ", h1).replace("  ", " ").strip()
    media = f'<video src="{video}" poster="{img}" autoplay muted loop playsinline></video>' if video else f'<img src="{img}" alt="{alt}" style="object-position:{pos}" fetchpriority="high">'
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
</section>"""


def feature(img, kicker, title, paras, link=None, flip=False, price=None, bg='', lst=None, cta=None, ratio='', video=None, alt=None, fit=False, h2="display-m"):
    ps = ''.join(f'<p class="fade d{min(i + 1, 4)}">{p}</p>' for i, p in enumerate(paras))
    lst_html = f'<ul class="list fade d3" style="margin:22px 0">{"".join(f"<li>{x}</li>" for x in lst)}</ul>' if lst else ''
    price_html = f'<div class="price-tag fade d3">{price}<small>COP · sesión</small></div>' if price else ''
    link_html = f'<a class="pill fade d4" href="{link[1]}"><span>{link[0]}</span></a>' if link else ''
    cta_html = f'<a class="pill solid fade d4" href="{AG}"><span>{cta}</span></a>' if cta else ''
    return f"""<section class="pad {bg}{' fit' if fit else ''}"><div class="wrap feature{' flip' if flip else ''}">
  <div class="feature__media">{f'<div class="media video"><video src="{video}" poster="{IMG}{img}" muted loop playsinline preload="metadata" data-start="11.5"></video><button class="unmute" type="button" aria-label="Ver con sonido">Ver</button></div>' if video else f'<div class="media {ratio}"><img src="{IMG}{img}" alt="{alt or re.sub("<[^>]+>", " ", title)}" loading="lazy"></div>'}</div>
  <div>{f'<span class="kicker fade">{kicker}</span>' if kicker else ''}<h2 class="{h2} lines" style="margin:14px 0 22px">{title}</h2>{ps}{lst_html}{price_html}<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px">{cta_html}{link_html}</div></div>
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


AVATAR = '<div class="avatar"><img src="/assets/img/favicon-512.png" alt="" loading="lazy" width="64" height="64"></div>'
TST = {
 'rtt': ("Fue un proceso totalmente transformador.", "Natalia Lozano", "RTT"),
 'peso': ("Por primera vez entendí por qué comía como comía. Dejé de pelear con la comida y empecé a cuidarme desde otro lugar.", "Sandra Londoño", "Peso"),
 'dormir': ("Llevaba años durmiendo mal. Después de la sesión y de escuchar mi audio, empecé a descansar de verdad.", "María López", "Dormir mejor"),
 'confianza': ("Descubrí de dónde venía esa voz que me decía que no era suficiente. Hoy me siento segura de quién soy.", "Lina Parra", "Confianza"),
 'motivacion': ("Volví a sentir ganas de hacer las cosas. Retomé proyectos que tenía guardados hace años.", "Santiago Luna", "Motivación"),
 'publico': ("Me paralizaba presentar en el trabajo. Hoy disfruto hablar frente a mi equipo, y nunca pensé que diría eso.", "Valentina Ramírez", "Hablar en público"),
 'dolor': ("Entendí la emoción que había detrás de mi dolor de espalda. Me siento más liviana, en el cuerpo y en el alma.", "Camila Díaz", "Dolores corporales"),
 'pareja': ("Me di cuenta de que siempre elegía desde el miedo. Sané esa creencia y hoy estoy en una relación sana y feliz.", "Cristina Casas", "Pareja"),
 'patprimo': ("Después del taller, el equipo empezó a hablar del estrés con otra apertura. Nos llevamos herramientas sencillas que seguimos usando en el día a día.", "Patprimo", "Taller de bienestar"),
 'barcu': ("El taller nos conectó como equipo. Nos dio más claridad, más energía y una forma distinta de ver la vida.", "Barcú", "Taller de bienestar"),
 'cyglo': ("Nunca habíamos vivido algo así en la oficina. El baño de gong le bajó las revoluciones a todo el equipo; salimos tranquilos, presentes y con otra energía para el resto de la semana.", "Cyglo", "Baño de gong"),
 'malva': ("Fue un espacio para desconectarnos del ritmo del trabajo y volver a nosotros mismos. Varias personas nos dijeron que fue la primera vez en meses que sintieron su mente en silencio.", "Malva", "Retiro corporativo"),
 'johanna': ("Fue un momento de pausa y conexión profunda para nuestro equipo y nuestras clientas: salimos más livianas, más presentes y con una mirada distinta hacia nosotras mismas y los demás.", "Johanna Ortiz", "Experiencia para equipos y clientas"),
 'pesadillas': ("Desde que nos vimos no he vuelto a tener pesadillas ni ataques de ansiedad. Gracias por liberarme y enseñarme a perdonar.", "Santiago", "Ansiedad y sueño"),
 'avion': ("Todavía no lo puedo creer: fui capaz de montarme al avión tranquila, ver una película y el vuelo se me pasó volando.", "Ma. Paula", "Miedo a volar"),
 'piel': ("Nunca hubiera hecho la conexión entre mi problema de piel y lo que sentía en mi trabajo. Una vez lo expresé, mi piel sanó.", "Cliente RTT", "Piel"),
 'nina': ("Me siento tan feliz. Liberaste a mi niña interior, volví a reír, a quererme y a entender que yo tengo el control de mi vida.", "Mónica", "Autoestima"),
}


def tcards(keys, bg="bg-sand", title="Lo que dicen quienes lo han vivido", cols=3):
    cards = ''.join(f'<figure class="tcard" style="margin:0"><div><p class="cat">{TST[k][2]}</p><p>“{TST[k][0]}”</p></div><cite>{TST[k][1]}</cite></figure>' for k in keys)
    dur = max(28, 11 * len(keys))
    return f'<section class="pad-s {bg}"><div class="wrap"><div class="sec-title"><span class="kicker">{title}</span></div></div><div class="tcar" data-tcar><div class="tcar__track" style="animation-duration:{dur}s">{cards}{cards}</div></div></section>'


def deck(items):
    cards = ''.join(f'<figure class="deck__card" style="margin:0"><p>“{q}”</p><cite>{w}</cite></figure>' for q, w in items)
    return f'<section class="deck"><div class="deck__sticky"><div class="deck__title"><span class="kicker">Lo que dicen después de una sesión</span></div>{cards}</div></section>'


def steps3(items, cls=""):
    return f'<div class="tiles steps3 {cls} stagger">' + ''.join(f'<div style="border-top:1px solid rgba(58,58,57,.2);padding-top:22px"><span class="kicker" style="font-family:var(--display);font-size:1.3rem;letter-spacing:0;text-transform:none">0{i+1}</span><h3 class="display-s" style="margin:10px 0 8px;font-size:1.35rem">{t}</h3><p style="margin:0;font-size:.95rem;color:var(--charcoal)">{d}</p></div>' for i, (t, d) in enumerate(items)) + '</div>'


TESTI = [("Fue un proceso totalmente transformador.", "Natalia Lozano"),
         ("Me siento tan feliz. Liberaste a mi niña interior, volví a reír, a quererme y a entender que yo tengo el control de mi vida.", "Mónica · cliente RTT"),
         ("Gracias por ayudarme a entender que mi problema no era lo que comía, sino todo lo que me comía a mí. Tres meses después he logrado bajar 7 kilos.", "Alejandra · cliente RTT")]


def testi(items=TESTI, bg="bg-sand"):
    cards = ''.join(f'<figure class="tcard" style="margin:0"><p>“{q}”</p><cite>{w}</cite></figure>' for i, (q, w) in enumerate(items))
    return f'<section class="pad-s {bg}"><div class="wrap"><div class="sec-title"><span class="kicker">Lo que dicen quienes lo han vivido</span></div><div class="tcards stagger">{cards}</div></div></section>'


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
    return f'''<div class="form-card fade d1"><form data-lead="{kind}">{f'<p class="small muted" style="margin:0 0 18px">{intro}</p>' if intro else ''}<div class="row">{f}</div><input type="text" name="website" tabindex="-1" autocomplete="off" style="display:none"><div class="form-actions"><button class="pill solid" type="submit"><span>{btn}</span></button>{extra or ''}</div><div data-lead-out style="margin-top:16px"></div></form></div>'''


AUDIO_CATS = [("cuerpo-mente", "Sana tu cuerpo y mente", "bg-blush"), ("liberate", "Libérate de lo que no quieres", "bg-sand"), ("miedos", "Supera tus miedos", "bg-aqua"), ("profesional", "Desarrollo profesional", "bg-sky"), ("proyectos", "Proyectos de vida", "bg-rose"), ("kids", "Kids · Para niños", "bg-mist")]
COURSES = [("Sana la relación con tu peso para siempre", "p/curso-peso.jpg", "Descubre la raíz de por qué comes como comes, aprende a nutrirte con lo que te hace bien y recodifica tu mente para mantener tu peso para siempre."), ("Queda embarazada", "p/curso-embarazo.jpg", "Desbloquea tu mente y tu cuerpo, nútrete con conciencia y prepárate desde adentro para ser el nido perfecto para tu bebé."), ("Reset your life", "p/curso-reset.jpg", "Libérate de las creencias y patrones que te frenan, y recodifica tu mente para manifestar y vivir la vida que de verdad quieres.")]
COURSE_PRICE = "$250.000"


def courses_html():
    return '<div class="tiles stagger">' + ''.join(f'<article class="course"><div class="media"><img src="{IMG}{img}" alt="{t}" loading="lazy"></div><div class="body"><span class="kicker" style="font-size:.62rem">Curso online</span><h3>{t}</h3><p class="small" style="margin:0;color:var(--charcoal)">{d}</p><div class="foot"><span>Próximamente</span><a href="{WA}" target="_blank" rel="noopener">Quiero saber más →</a></div></div></article>' for i, (t, img, d) in enumerate(COURSES)) + '</div>'


CAT_IMG = {"cuerpo-mente": "audios/consigue-tu-peso-ideal-y-mantenlo-para-siempre.jpg", "liberate": "audios/dile-adios-al-insomnio.jpg", "miedos": "audios/vence-el-miedo-de-hablar-en-publico.jpg", "profesional": "audios/deja-de-procrastinar-y-cumple-tus-objetivos.jpg", "proyectos": "audios/atrae-tu-pareja-ideal.jpg"}


def cats_html():
    return '<div class="circles stagger" data-cats>' + ''.join(f'<a class="circle pastel {bg}" href="/shop/#{c}"><div class="body"><h3>{n}</h3><span class="tag">Ver audios</span></div></a>' for c, n, bg in AUDIO_CATS[:5]) + '</div>'


def icard(img, title, sub, href, tag, wide=False, i=0):
    return f'<a class="icard{" wide" if wide else ""}" href="{href}"><img src="{IMG}{img}" alt="{title}" loading="lazy"><div class="body"><h3>{title}</h3>{f"<p>{sub}</p>" if sub else ""}<span class="tag">{tag} →</span></div></a>'


HRS_CARDS = '<div class="icards stagger">' + icard('p/heal-card-3.jpg', 'Heal', None, '/heal-rise-shine/#heal', 'Sana tu cuerpo') + icard('p/rise-card-2.jpg', 'Rise', None, '/heal-rise-shine/#rise', 'Sana tu mente', i=1) + icard('p/shine-card-2.jpg', 'Shine', None, '/heal-rise-shine/#shine', 'Alcanza tus objetivos', i=2) + '</div>'
HRS_CARDS = HRS_CARDS.replace('class="icard"', 'class="icard big"')
def mcard(img, title, sub, href):
    return f'<a class="mcard" href="{href}"><div class="media"><img src="{IMG}{img}" alt="{title}" loading="lazy"></div><h3>{title}</h3><p>{sub}</p><span class="tag">Conoce más →</span></a>'


MORE_CARDS = '<div class="mcards stagger">' + mcard('p/kids-parachute.jpg', 'Kids', 'Autoestima alta, menos ansiedad y mejor rendimiento para los más pequeños.', '/kids/') + mcard('p/coaching-taza.jpg', 'Coaching', 'Sesiones individuales para integrar tu transformación en el día a día.', '/coaching/') + mcard('p/gong-hero.jpg', 'Gong', 'Baños de sonido para una relajación profunda del cuerpo y la mente.', '/gong/') + '</div>'

pages = {}
PRODUCTS = json.load(open(os.path.join(OUT, 'assets/data/products.json'), encoding='utf-8'))
fmt = lambda n: 'Gratis' if n == 0 else '$' + f'{n:,}'.replace(',', '.')

# ------------------------------------------------------------------ HOME
pages["/"] = dict(title="Hipnoterapia en Bogotá · Hipnosis clínica RTT | Space to Rise",
 desc="Hipnoterapia RTT en Bogotá y online con Andrea Zafra: sana la ansiedad, los miedos, el insomnio y las enfermedades desde la raíz. Agenda tu llamada inicial.", og="/assets/img/og-home.jpg",
 body=f"""<section class="hero light right" style="min-height:100svh">
  <div class="hero__media"><img src="{IMG}p/home-hero-3.jpg" alt="Mujer sonriendo frente al mar, con el pelo al viento" style="object-position:left center" fetchpriority="high"></div>
  <div class="hero__body"><div class="wrap">
    <span class="kicker fade">Hipnoterapia RTT (Rapid Transformational Therapy) · Neurociencia del cambio</span>
    <h1 class="display-xl lines" style="margin-top:18px;max-width:14ch;font-size:clamp(2.2rem,4.3vw,4.1rem);line-height:1.08">Sana, transfórmate y evoluciona en quien estás destinada a ser</h1>
    <p class="lead fade d2" style="max-width:46ch;margin:22px 0 28px">Acompaño a personas y empresas a encontrar la raíz de lo que las bloquea y a reprogramar la mente para un cambio real y permanente.</p>
    <div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap"><a class="pill solid" href="{WA}" target="_blank" rel="noopener"><span>Agenda tu cita</span></a><a class="pill" href="/empresas/"><span>Soy una empresa</span></a></div>
  </div></div>
</section>

<div class="creds stagger"><span>Hipnoterapeuta clínica · RTT (Rapid Transformational Therapy)</span><span>Consultora certificada de Joe Dispenza (NCS)</span><span>MBA · IE Business School</span><span>Babson College</span><span>+10 años de experiencia</span></div>
<section class="pad"><div class="wrap grid g2" style="align-items:start">
  <div><span class="kicker fade">¿Te identificas?</span><h2 class="display-m lines" style="margin:14px 0 22px;font-size:clamp(1.8rem,3.4vw,2.9rem)">Sabes lo que quieres cambiar, pero algo más profundo te sigue frenando</h2><p class="fade d1">La fuerza de voluntad no basta cuando el 95% de nuestras decisiones nacen del subconsciente. Ahí es donde trabajamos: en la raíz, no en los síntomas.</p><a class="pill fade d2" href="/rtt/"><span>Descubre cómo funciona</span></a></div>
  <div class="temas"><span class="kicker fade" style="display:block;margin-bottom:10px">Temas con los que he trabajado</span><ul class="plist c2 stagger" style="grid-template-columns:1fr"><li>Ansiedad, estrés o ataques de pánico</li><li>Miedos y fobias que te limitan</li><li>Baja autoestima o sensación de no ser suficiente</li><li>Insomnio, adicciones o hábitos que no logras dejar</li><li>Síntomas físicos que no mejoran</li><li>Metas que se te escapan una y otra vez</li></ul></div>
</div></section>

<section class="pad-s bg-stone"><div class="wrap">
  {sec_title("Dos caminos, una misma transformación")}
  <div class="tiles c2 stagger">
    <a class="tile bg-blush" href="/heal-rise-shine/"><span class="tag top">Para ti y tu familia</span><h3>Terapia individual</h3><p>Hipnoterapia RTT (Rapid Transformational Therapy) para adultos y niños: sana tu cuerpo, libera tu mente y alcanza tus objetivos. Complementa tu proceso con coaching personalizado, presencial o virtual, y sesiones de sound healing.</p><span class="tag">RTT (Rapid Transformational Therapy) · Kids · Coaching · Sound healing →</span></a>
    <a class="tile bg-aqua" href="/empresas/"><span class="tag top">Para tu empresa</span><h3>Bienestar corporativo</h3><p>Programas a la medida para líderes y equipos. Como consultora certificada del Dr. Joe Dispenza, llevo a tu organización Change Your Mind… Create New Results, el programa de neurociencia del cambio de NeuroChangeSolutions (NCS). También diseño charlas y talleres corporativos, retiros para equipos y sesiones grupales de sound healing. Presencial o virtual.</p><span class="tag">Talleres · Retiros · Sound healing · NCS →</span></a>
  </div>
</div></section>

{feature("../video/rtt-poster-2.jpg", "Hipnoterapia", "¿Qué es RTT (Rapid Transformational Therapy)?", [
 "Una terapia creada por Marisa Peer que combina hipnosis, PNL y neurociencia. Accede a tu subconsciente para encontrar la raíz de lo que te bloquea o te enferma, y reprogramarla. Muchas personas logran resultados en 1 a 3 sesiones."], link=("Conoce más", "/rtt/"), cta="Agenda tu cita", video="/assets/video/rtt.mp4")}
<section class="pad-s" style="padding-top:0"><div class="wrap">
  {steps3([("Conversación inicial", "Una llamada de 20 minutos para resolver tus dudas y entender lo que quieres sanar."), ("Tu sesión de RTT (Rapid Transformational Therapy)", "3 horas de hipnosis para encontrar la raíz, entenderla y liberarla."), ("Tu audio personal", "Un audio hecho solo para ti, que escuchas 21 días para que tu mente cree nuevos hábitos.")])}
  <div style="height:clamp(28px,4vw,48px)"></div>
  {HRS_CARDS}
</div></section>

<section class="pad bg-stone"><div class="wrap">
  <div class="feature">
    <div><span class="kicker fade">Empresas</span><h2 class="display-m lines" style="margin:14px 0 22px">Bienestar y transformación<br>para tu equipo</h2><p class="lead fade d1">Las organizaciones crecen cuando crecen las personas que las forman.</p><p class="fade d2">Llevo a las empresas el mismo trabajo que hago con cada persona: herramientas para manejar el estrés, cuidar la salud emocional y cambiar los patrones que frenan a líderes y equipos.</p><div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px"><a class="pill solid" href="/empresas/#contacto"><span>Solicita una propuesta</span></a><a class="pill" href="/empresas/"><span>Ver programas</span></a></div></div>
    <div class="feature__media"><div class="media"><img src="{IMG}p/empresas-3.jpg" alt="Equipo de trabajo conversando en una oficina" loading="lazy"></div></div>
  </div>
  <div class="tiles stagger" style="margin-top:clamp(28px,4vw,48px)">
    <a class="tile bg-blush" href="/empresas/"><span class="n">01</span><h3 style="margin-top:34px">Talleres de bienestar</h3><p>Manejo del estrés, salud emocional, autoestima y hábitos, y sound healing.</p></a>
    <a class="tile bg-sand" href="/empresas/"><span class="n">02</span><h3 style="margin-top:34px">Retiros corporativos</h3><p>Experiencias para que tu equipo desconecte, se reconecte y vuelva con más claridad.</p></a>
    <a class="tile bg-aqua" href="/empresas/#ncs"><span class="n">03</span><h3 style="margin-top:34px">Programa NCS del Dr. Joe Dispenza</h3><p>Change Your Mind… Create New Results: la neurociencia del cambio para líderes y equipos.</p></a>
  </div>
</div></section>

<section class="quote-band bg-taupe" data-dark><div class="wrap"><p class="fade">“No podemos ofrecer al mundo algo que no somos.”</p><cite class="fade d1">Andrea Zafra</cite></div></section>

{feature("p/andrea.jpg", "Hola, soy Andrea Zafra", "Hipnoterapeuta clínica especializada en RTT (Rapid Transformational Therapy) y consultora certificada de Joe Dispenza", [
 "Después de años en grandes multinacionales, un MBA en el IE y mis estudios en Babson College, mis hijos me llevaron a transformar mi propia vida. Hoy uno la hipnoterapia, la neurociencia del cambio y más de 10 años de experiencia para acompañar a personas, familias y organizaciones."], link=("Conoce mi historia", "/sobre-mi/"), alt="Andrea Zafra, hipnoterapeuta RTT", h2="display-s")}

<section class="entity bg-stone" id="que-es"><div class="wrap">
  <span class="kicker fade" style="display:block;margin-bottom:22px">Qué es Space to Rise</span>
  <img class="logo fade" src="{IMG}LOGO-Color_New.png" alt="Space to Rise" loading="lazy">
  <p class="sub fade d1">Human evolution <i>studio</i></p>
  <h2 class="text fade d2">Un espacio para sanar, transformarte y elevarte a tu nuevo potencial. Fundado en Bogotá por <em>Andrea Zafra</em>, Space to Rise une la hipnoterapia RTT (Rapid Transformational Therapy) de Marisa Peer, la neurociencia del cambio del Dr. Joe Dispenza y el poder sanador del sonido.</h2>
  <div class="cols5 stagger">
    <div><h4>Hipnoterapia RTT<small>(Rapid Transformational Therapy)</small></h4><p>Para adultos y niños. Llega a la raíz de lo que te bloquea.</p></div>
    <div><h4>Empresas</h4><p>Bienestar y neurociencia del cambio para equipos.</p></div>
    <div><h4>Coaching individual</h4><p>Para integrar tu cambio en el día a día.</p></div>
    <div><h4>Cursos y audios</h4><p>Cursos online y autohipnosis para transformarte a tu ritmo.</p></div>
    <div><h4>Sound healing</h4><p>Baños de gong para una relajación profunda.</p></div>
  </div>
  <p class="foot fade">Presencial en Bogotá · Online desde cualquier lugar del mundo</p>
</div></section>

<section class="pad-s"><div class="wrap">{sec_title("Más formas de acompañarte")}{MORE_CARDS}</div></section>

<section class="pad bg-stone"><div class="wrap">
  <div class="narrow center fade" style="margin:0 auto clamp(32px,4vw,56px)"><h2 class="display-s" style="text-transform:uppercase;letter-spacing:.06em;margin:0 0 12px">Conoce nuestra selección de audios y cursos</h2><p style="margin:0;color:var(--charcoal)">Desbloquea tu potencial en la salud, el amor, la abundancia y mucho más, a tu ritmo y desde donde estés.</p></div>
  {sec_title("Cursos", ("Ver todos", "/shop/#cursos"))}
  {courses_html()}
  <div style="height:clamp(28px,4vw,48px)"></div>
  {sec_title("Audios de autohipnosis", ("Ver todos", "/shop/#audios"))}
  {cats_html()}
</div></section>

{tcards(['rtt', 'confianza', 'dormir', 'publico', 'peso', 'pareja'])}
""")

# ------------------------------------------------------------------ RTT
pages["/rtt/"] = dict(title="¿Qué es RTT? Hipnoterapia de Transformación Rápida | Space to Rise",
 desc="Qué es la hipnoterapia RTT de Marisa Peer, cómo funciona, sus beneficios y qué puedes sanar. Hipnosis, PNL y neurociencia para resultados en 1 a 3 sesiones.", og="/assets/img/p/rtt-hero-3.jpg",
 body=hero(IMG + "p/rtt-hero-3.jpg", "Terapia de<br class=\"d\">Transformación Rápida", "Hipnosis, PNL y neurociencia para llegar a la raíz de lo que te bloquea y lograr resultados rápidos, permanentes y transformadores.", kicker="Hipnoterapia RTT · Rapid Transformational Therapy", pos="center 30%", compact=True, cta2=("Preguntas frecuentes", "/preguntas-frecuentes/")) + f"""
<section class="pad-s bg-blush"><div class="wrap"><p class="caps fade" style="margin:0 auto;text-align:center;max-width:80ch">RTT (Rapid Transformational Therapy) es una terapia desarrollada por Marisa Peer que combina los principios más eficaces de la hipnosis, la PNL y la neurociencia. Muchas personas logran sanar en 1 a 3 sesiones, según la complejidad del tema.</p></div></section>

{feature("../video/rtt-poster-2.jpg", "Cómo funciona", "La hipnosis te da acceso a tu subconsciente.", [
 "Ahí está toda tu programación: tus memorias y tus creencias. Entrar en él permite entender por qué reaccionas como reaccionas, encontrar la raíz del problema, sanarla y crear nuevas conexiones neuronales.",
 "<em>Entender es poder. Cuando entiendes el porqué de tus problemas, sanar es fácil.</em>"], flip=True, video="/assets/video/rtt.mp4")}

{feature("p/rtt-costa.jpg", "Por qué es tan efectiva", "El 95% de tus decisiones nacen del subconsciente.", [
 "Por eso, aunque quieras cambiar con lógica y fuerza de voluntad, ningún cambio será real y permanente hasta cambiar tu subconsciente.",
 "RTT (Rapid Transformational Therapy) te libera de creencias limitantes y “programas” obsoletos que pueden estar detrás de tus bloqueos o de tu enfermedad, y recablea tu mente con nuevas creencias que transforman tu vida."], bg="bg-stone", cta="Agenda tu cita", alt="Mujer frente al mar, en calma")}

<section class="pad-s"><div class="wrap">
  {sec_title("Tu proceso en 3 pasos")}
  {steps3([("Conversación inicial", "Una llamada de 20 minutos para aclarar cualquier duda sobre la terapia."), ("Tu sesión de RTT (Rapid Transformational Therapy)", "Aproximadamente 3 horas. Con la hipnosis vamos a la raíz del problema para entender por qué y cuándo lo creaste, y liberarte de él."), ("Tu audio personal", "Un audio de 15 a 20 minutos hecho solo para ti, que escuchas cada día durante al menos 21 días para que el cambio sea permanente.")])}
</div></section>

<section class="pad-s bg-sand"><div class="wrap">
  {sec_title("¿Qué puedo sanar con RTT (Rapid Transformational Therapy)?")}
  <div class="tiles stagger" style="gap:0 36px">
    <div class="fade"><h3 class="display-s" style="margin-bottom:8px">Salud física</h3><ul class="plist stagger" style="grid-template-columns:1fr"><li>Enfermedades crónicas</li><li>Problemas de piel, pelo y digestivos</li><li>Dolores crónicos</li><li>Alergias y asma</li></ul></div>
    <div class="fade d1"><h3 class="display-s" style="margin-bottom:8px">Salud emocional</h3><ul class="plist stagger" style="grid-template-columns:1fr"><li>Ansiedad y estrés</li><li>Autoestima y sensación de insuficiencia</li><li>Fobias, miedos y adicciones</li><li>Insomnio, peso y fertilidad</li></ul></div>
    <div class="fade d2"><h3 class="display-s" style="margin-bottom:8px">Desempeño</h3><ul class="plist stagger" style="grid-template-columns:1fr"><li>Alcanzar sueños, metas y objetivos</li><li>Mejorar tu rendimiento deportivo</li><li>Hablar en público</li><li>Concentración y procrastinación</li></ul></div>
  </div>
  <div class="small muted fade" style="display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-top:28px"><span>Es una terapia apta para niños y adultos.</span><span>RTT (Rapid Transformational Therapy) es un acompañamiento complementario y no reemplaza el diagnóstico ni el tratamiento médico.</span></div>
</div></section>

<section class="pad-s"><div class="wrap">
  {sec_title("Preguntas frecuentes", ("Ver todas", "/preguntas-frecuentes/"))}
  <div class="acc stagger">{''.join(f'<div class="acc__item"><button class="acc__q">{q}<i></i></button><div class="acc__a"><div><div class="inner"><p>{a}</p></div></div></div></div>' for q, a in [("¿Cómo se siente estar hipnotizado?", "La mayoría de las personas se siente muy relajada. Estás 100% en control de tu cuerpo y solo aceptas las sugerencias que tú quieras."), ("¿Por qué RTT (Rapid Transformational Therapy) sana en una sola sesión?", "La hipnosis permite identificar el origen de las creencias que te bloquean. Al observarlas desde tu mente adulta, es fácil dejarlas ir."), ("¿Cuándo veo los resultados?", "Pueden ser inmediatos, progresivos en 10 a 21 días, o retroactivos: a veces quienes te rodean notan el cambio primero."), ("¿Puedo hacer la sesión por Zoom?", "Sí. Las sesiones pueden ser presenciales o por Zoom.")])}</div>
</div></section>
{tcards(['rtt', 'confianza', 'motivacion'])}
""", cta_title="¿Lista para ir a la raíz?", cta_sub="Agenda tu llamada inicial de 20 minutos y resolvemos todas tus dudas.")

# ------------------------------------------------------------------ HEAL RISE SHINE
pages["/heal-rise-shine/"] = dict(title="Hipnosis para ansiedad, miedos y fobias · Heal Rise Shine | Space to Rise",
 desc="Hipnoterapia RTT para sanar el cuerpo, liberar la mente (ansiedad, miedo a volar, fobias, insomnio, traumas) y alcanzar tus objetivos. Bogotá y online.", og="/assets/img/p/heal-card-3.jpg",
 body=f"""<section class="portal pad-s"><div class="wrap">
  <div class="narrow center" style="margin:0 auto clamp(28px,4vw,44px)"><span class="kicker fade">RTT (Rapid Transformational Therapy) para personas</span><h1 class="display-l lines" style="margin:14px 0 14px;text-transform:uppercase;letter-spacing:.06em;font-size:clamp(2.2rem,5vw,4.4rem)">Heal · Rise · Shine</h1><p class="fade d1" style="margin:0;color:var(--charcoal)">Tres caminos para sanar tu cuerpo, liberar tu mente y alcanzar todo lo que quieres.</p></div>
  {HRS_CARDS.replace('/heal-rise-shine/#', '#')}
</div></section>

<section id="heal" class="pad-s"><div class="wrap hrs">
  <div class="hrs__media"><div class="media"><img src="{IMG}p/heal.jpg" alt="Heal · sana tu cuerpo" loading="lazy"></div></div>
  <div>
    <div class="hrs__head"><h2 class="display-l">Heal</h2><span>Sana tu cuerpo</span></div>
    <blockquote class="fade">“El dolor que no encuentra salida en las lágrimas pronto puede hacer llorar a otros órganos.”<cite>Sir Henry Maudsley</cite></blockquote>
    <p class="strong fade">Cualquier emoción reprimida puede estar detrás de una enfermedad física. Mente y cuerpo están conectados: lo que no expresamos, el cuerpo lo expresa.</p>
    <p class="fade d1">RTT (Rapid Transformational Therapy) es muy efectiva para encontrar la causa raíz de estos bloqueos y emociones. A través de la hipnosis accedes a tu subconsciente, donde se guardan tus memorias y emociones, y logras reinterpretar lo que pasó para sanar.</p>
    <p class="fade d2">Durante la sesión puedes recordar experiencias, eventos o patrones de pensamiento relacionados con tu problema de salud. Al entenderlos, puedes darles otra interpretación y cambiar las creencias que contribuyeron a tu enfermedad.</p>
    <p class="it fade d2">Tu mente puede crear una enfermedad, pero así como la crea, puede ayudarte a sanarla.</p>
    <span class="k">Temas con los que he trabajado</span>
    <ul class="tags stagger"><li>Cáncer (como acompañamiento)</li><li>Dolores crónicos</li><li>Enfermedades genéticas</li><li>Enfermedades autoinmunes</li><li>Problemas de audición</li><li>Problemas de visión</li><li>Asma</li><li>Problemas de piel y pelo</li><li>Alergias</li></ul>
    <p class="small muted fade" style="margin:18px 0 0">RTT (Rapid Transformational Therapy) es un acompañamiento complementario y no reemplaza el diagnóstico ni el tratamiento médico.</p>
  </div>
</div></section>

<section id="rise" class="pad-s bg-stone"><div class="wrap hrs flip">
  <div class="hrs__media"><div class="media"><img src="{IMG}p/rtt-hero-3.jpg" alt="Rise · sana tu mente" loading="lazy" style="object-position:60% center"></div></div>
  <div>
    <div class="hrs__head"><h2 class="display-l">Rise</h2><span>Sana tu mente</span></div>
    <blockquote class="fade">“Puede que no seamos responsables de cómo el mundo moldea nuestra mente, pero podemos aprender a ser responsables de la mente con la que creamos nuestro mundo.”</blockquote>
    <p class="strong fade">El 95% de las decisiones de tu vida nacen de las memorias guardadas en tu subconsciente. Lo que vives hoy está determinado por las experiencias de tu pasado.</p>
    <p class="fade d1">Para un cambio permanente hay que encontrar la raíz del dolor. De nada sirve tratar solo los síntomas o confiar en la fuerza de voluntad: el subconsciente y la emoción siempre le ganan a la lógica.</p>
    <p class="fade d2">RTT (Rapid Transformational Therapy) te permite encontrar esas memorias y reinterpretarlas desde tu mente adulta, y no desde la de un niño, para entender, sanar y evolucionar.</p>
    <span class="k">Temas con los que he trabajado</span>
    <ul class="tags stagger"><li>Ansiedad y ataques de pánico</li><li>Baja autoestima</li><li>Estrés</li><li>Autosabotaje</li><li>Adicciones: cigarrillo, vapeador, alcohol, juego</li><li>Insomnio y trastornos de sueño</li><li>Depresión</li><li>Fobias: volar, agujas, claustrofobia</li><li>Fertilidad</li><li>Concentración y procrastinación</li><li>Miedo a hablar en público</li><li>Duelos y celos</li><li>Traumas del pasado</li></ul>
  </div>
</div></section>

<section id="shine" class="pad-s"><div class="wrap hrs">
  <div class="hrs__media"><div class="media"><img src="{IMG}p/shine-bn.jpg" alt="Shine · alcanza tus objetivos" loading="lazy"></div></div>
  <div>
    <div class="hrs__head"><h2 class="display-l">Shine</h2><span>Brilla · Alcanza tus objetivos</span></div>
    <blockquote class="fade">“Tus palabras crean tu realidad. Si no te gusta tu realidad, cambia tus palabras.”</blockquote>
    <p class="strong fade">Conviértete en tu mejor versión y alcanza tus sueños. Libérate de lo que te impide avanzar y reprograma tu mente para lograr todo lo que quieres.</p>
    <p class="fade d1">RTT (Rapid Transformational Therapy) te permite encontrar la causa raíz de lo que te detiene, y el audio de transformación personal, hecho especialmente para ti, reprograma tu mente para alcanzar tus objetivos.</p>
    <div class="tiles c2 stagger" style="margin-top:22px"><div class="tile bg-aqua" style="min-height:0;padding:22px"><span class="tag" style="margin:0 0 8px">Deporte</span><h3 style="font-size:1.25rem">Conviértete en el mejor deportista</h3><p style="font-size:.88rem">Supera bloqueos mentales, maneja la presión y lleva tu rendimiento al siguiente nivel.</p></div><div class="tile bg-blush" style="min-height:0;padding:22px"><span class="tag" style="margin:0 0 8px">Liderazgo</span><h3 style="font-size:1.25rem">Conviértete en el mejor líder</h3><p style="font-size:.88rem">Gana seguridad, claridad y confianza para liderar a tu equipo y a ti misma.</p></div></div>
  </div>
</div></section>
{tcards(['rtt', 'peso', 'dolor', 'pareja', 'motivacion', 'dormir'])}
""", cta_title="Empieza hoy tu transformación", cta_sub="Agenda una llamada inicial de 20 minutos y elegimos juntas el camino.")

# ------------------------------------------------------------------ KIDS
pages["/kids/"] = dict(title="Hipnoterapia para niños · RTT Kids | Space to Rise",
 desc="Hipnosis para niños con RTT Kids: autoestima inquebrantable, menos ansiedad y estrés, mejor sueño y rendimiento académico. Bogotá y online.", og="/assets/img/p/kids-hero.jpg",
 body=hero(IMG + "p/kids-hero.jpg", "“Lo más valioso que puedes enseñarles a tus hijos es que son suficientes”", "Marisa Peer", kicker="Kids · Niños", pos="center 35%", btn="Agenda una cita") + f"""
<section class="pad-s"><div class="wrap hrs" style="grid-template-columns:.75fr 1.25fr">
  <div class="hrs__media"><div class="media"><img src="{IMG}p/kids-familia.jpg" alt="Familia corriendo en un campo al atardecer" loading="lazy"></div></div>
  <div>
    <h2 class="display-s lines" style="margin:0 0 14px;padding-bottom:12px;border-bottom:1px solid rgba(58,58,57,.2)">Una autoestima inquebrantable para toda la vida</h2>
    <p class="strong fade">Como papás tenemos una responsabilidad gigante: ayudar a nuestros hijos a ser niños felices que se conviertan en adultos realizados y equilibrados.</p>
    <p class="fade d1">Las experiencias de la infancia marcan la autoestima, las creencias y la vida adulta. La manera en que les hablamos se convierte en su voz interior; por eso es tan importante construir una base sólida de seguridad y confianza.</p>
    <p class="fade d2">RTT (Rapid Transformational Therapy) ayuda a los niños a superar cualquier desafío emocional para que no crezcan con creencias limitantes, y les da herramientas para manejar la ansiedad, el estrés y mejorar su rendimiento académico.</p>
    <span class="k">Temas en los que podemos ayudar</span>
    <ul class="tags stagger"><li>Autoestima alta y bullying</li><li>Ansiedad y estrés</li><li>Rendimiento académico</li><li>Pasar exámenes</li><li>Pesadillas y sueño</li><li>TDAH</li><li>Dislexia</li></ul>
    <div class="tiles c2 stagger" style="margin-top:22px">
      <div class="tile bg-blush" style="min-height:0;padding:22px"><span class="tag" style="margin:0 0 8px">Sesiones Kids</span><h3 style="font-size:1.25rem">Una experiencia pensada para ellos</h3><p style="font-size:.88rem">Sesiones adaptadas a la edad de cada niño, con un audio personal para reforzar el cambio en casa.</p><p style="margin-top:10px;font-size:.88rem">Valor: <b style="font-family:var(--display);font-weight:300;font-size:1.4rem">$380.000</b></p><a class="pill solid" href="/agenda/" style="margin-top:12px;align-self:flex-start;padding:9px 18px"><span>Agenda</span></a></div>
      <div class="tile bg-sand" style="min-height:0;padding:22px"><span class="tag" style="margin:0 0 8px">Para papás y mamás</span><h3 style="font-size:1.25rem">Criar sin miedos empieza por ti</h3><p style="font-size:.88rem">Acompaño a padres para criar nuevas generaciones libres de miedos, con amor propio y alas fuertes para volar alto.</p><a class="tag" href="/heal-rise-shine/" style="margin-top:12px">Conoce RTT (Rapid Transformational Therapy) para adultos →</a></div>
    </div>
  </div>
</div></section>
{tcards(['pesadillas', 'confianza', 'nina'])}
""", cta_title="Dale a tu hijo la mejor base para su vida", cta_sub="Agenda una llamada inicial y conversemos sobre lo que necesita.")

# ------------------------------------------------------------------ COACHING
pages["/coaching/"] = dict(title="Coaching de vida en Bogotá y online | Space to Rise",
 desc="Coaching de vida individual con Andrea Zafra: integra los cambios de tu sesión de RTT y alcanza tus metas. Sesiones de 1 hora en Bogotá o por Zoom. $180.000.", og="/assets/img/p/coaching-hero-4.jpg",
 body=f"""<section class="hero light split"><div class="wrap feature" style="grid-template-columns:.9fr 1.1fr">
  <div><span class="kicker fade" style="color:var(--taupe)">Coaching individual</span>
    <h1 class="display-l lines" style="margin:16px 0 18px;max-width:12ch">Combina lo mejor de ambos mundos</h1>
    <p class="fade d2" style="max-width:46ch;color:var(--charcoal)">Con RTT (Rapid Transformational Therapy) sanas la raíz. Con el coaching integras el cambio en tu vida para no volver a los patrones del pasado.</p>
    <div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px"><a class="pill solid" href="/agenda/"><span>Agenda tu sesión</span></a></div>
  </div>
  <div class="feature__media"><div class="media wide"><img src="{IMG}p/coaching-hero-4.jpg" alt="Sesión de coaching individual" fetchpriority="high"></div></div>
</div></section>
<section class="pad-xs"><div class="wrap"><p class="caps fade" style="margin:0 auto;text-align:center;max-width:78ch">Con RTT (Rapid Transformational Therapy) trabajamos tu mente subconsciente, entendiendo el porqué de tus comportamientos y la raíz de tus problemas. Con el coaching individual te ayudo a implementar los cambios necesarios para que nunca más vuelvas a autosabotear tu transformación.</p></div></section>
<section class="pad-s"><div class="wrap feature">
  <div><div class="sec-title" style="margin-bottom:22px"><h2 class="display-s" style="margin:0;text-transform:uppercase;letter-spacing:.06em;font-size:1.3rem">Coaching individual</h2></div>
    <div class="tiles c2 fade d1 stagger" style="margin:0 0 18px"><div class="pricecard bg-blush"><b>1 h</b><span class="k">Por sesión</span><p>Un espacio enfocado solo en ti.</p></div><div class="pricecard bg-sand"><b>2</b><span class="k">Modalidades</span><p>Presencial o por Zoom.</p></div></div>
    <p class="lead fade d2" style="margin:0 0 8px">Valor por sesión: <b style="font-weight:500">$180.000</b></p>
    <p class="fade d2">Ideal después de tu sesión de RTT (Rapid Transformational Therapy), o para acompañar cualquier proceso de cambio: nuevos hábitos, decisiones importantes, metas personales o profesionales.</p>
    <a class="pill solid fade d3" href="/agenda/"><span>Agenda tu sesión</span></a></div>
  <div class="feature__media"><div class="media"><img src="{IMG}p/coaching-taza.jpg" alt="Coaching individual" loading="lazy"></div></div>
</div></section>
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Cómo trabajamos")}{steps3([("Definimos tu objetivo", "Aclaramos qué quieres lograr y qué te ha detenido hasta ahora."), ("Diseñamos tu plan", "Pasos concretos y prácticos para integrar el cambio en tu día a día."), ("Te acompaño", "Sesiones de seguimiento para sostener tu transformación en el tiempo.")])}</div></section>
{tcards(['rtt', 'motivacion', 'confianza'])}
""", cta_title="Da el siguiente paso con acompañamiento", cta_sub="Agenda tu sesión de coaching, presencial o por Zoom.", cta_btn="Agenda tu sesión")

# ------------------------------------------------------------------ GONG
pages["/gong/"] = dict(title="Baño de gong en Bogotá · Baño de sonido | Space to Rise",
 desc="Baño de gong en Bogotá: relajación profunda, liberación emocional y equilibrio energético. Sesiones individuales, grupales y para empresas.", og="/assets/img/p/gong-hero.jpg",
 body=hero(IMG + "p/gong-hero.jpg", "Sana y transforma tu vida con la vibración del sonido", "Una técnica de relajación profunda que se alcanza a través de las vibraciones de este instrumento ancestral.", kicker="Baños de gong", pos="center 50%", btn="Reserva tu sesión", cta2=("Para empresas", "/empresas/")) + f"""
<section class="pad-s"><div class="wrap hrs" style="grid-template-columns:.8fr 1.2fr">
  <div class="hrs__media"><div class="media"><img src="{IMG}p/gong-2.jpg" alt="Andrea tocando el gong en una sesión de sound healing" loading="lazy"></div></div>
  <div>
    <span class="kicker fade">Qué es</span>
    <h2 class="display-s lines" style="margin:10px 0 14px;padding-bottom:12px;border-bottom:1px solid rgba(58,58,57,.2)">Más que un instrumento, un sistema vibracional</h2>
    <p class="strong fade">El gong recibe las energías de la persona, las armoniza y las devuelve potenciadas con una intención.</p>
    <p class="fade d1">Su sonido y vibración promueven el bienestar físico, mental y emocional, equilibran los centros de energía del cuerpo y ayudan a liberar emociones reprimidas. Su vibración llega a cada célula, por eso puede acompañar también procesos de salud.</p>
    <span class="k">Beneficios</span>
    <ul class="tags stagger"><li>Relajación profunda</li><li>Libera emociones</li><li>Equilibra tu energía</li><li>Claridad mental</li><li>Calma el sistema nervioso</li></ul>
    <div class="tiles c2 stagger" style="margin-top:22px">
      <div class="pricecard bg-blush"><span class="k">Sesión individual</span><b>$180.000</b><p>Una experiencia sonora pensada solo para ti.</p><a class="tag" href="/agenda/" style="display:inline-block;margin-top:12px;font-size:.64rem;letter-spacing:.22em;text-transform:uppercase">Reservar →</a></div>
      <div class="pricecard bg-aqua"><span class="k">Sesión grupal</span><b>$120.000 <small style="font-size:.5em">p/p</small></b><p>Para tu familia, tus amigos o tu equipo de trabajo.</p><a class="tag" href="/agenda/" style="display:inline-block;margin-top:12px;font-size:.64rem;letter-spacing:.22em;text-transform:uppercase">Reservar →</a></div>
    </div>
    <p class="it fade d2" style="margin:20px 0 10px">Regálate esta experiencia única y déjame acompañarte en este viaje sonoro hacia tu bienestar.</p>
    <p class="small muted fade" style="margin:0">El sound healing es un acompañamiento complementario y no reemplaza el diagnóstico ni el tratamiento médico.</p>
  </div>
</div></section>
""", cta_title="Reserva tu baño de gong", cta_sub="Sesiones individuales, grupales y para empresas.", cta_btn="Reserva tu sesión")

# ------------------------------------------------------------------ EMPRESAS
pages["/empresas/"] = dict(title="Bienestar laboral para empresas · Talleres y retiros | Space to Rise",
 desc="Programa de bienestar laboral: talleres de manejo del estrés y burnout, retiros corporativos, coaching empresarial y el programa NCS del Dr. Joe Dispenza.", og="/assets/img/p/empresas-3.jpg",
 body=f"""<section class="hero light compact" style="min-height:0;padding-top:118px"><div class="wrap feature flip" style="align-items:center">
  <div><span class="kicker fade" style="color:var(--taupe)">Empresas · Bienestar laboral</span>
    <h1 class="display-l lines" style="margin:16px 0 18px;max-width:14ch">Bienestar y<br class="d">transformación<br class="d">para tu equipo</h1>
    <p class="lead fade d2" style="max-width:44ch">Las organizaciones crecen cuando crecen las personas que las forman.</p>
    <p class="fade d2" style="max-width:52ch">Llevo a las empresas el mismo trabajo que hago con cada persona: herramientas para manejar el estrés, cuidar la salud emocional y cambiar los patrones que frenan a líderes y equipos. Cada propuesta se diseña según lo que tu organización necesita.</p>
    <div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px"><a class="pill solid" href="#contacto"><span>Solicita una propuesta</span></a><a class="pill" href="#ncs"><span>Ver programa NCS</span></a></div>
  </div>
  <div class="feature__media"><div class="media"><img src="{IMG}p/empresas-3.jpg" alt="Equipo de trabajo conversando en una oficina" fetchpriority="high"></div></div>
</div></section>
<div class="band" style="margin-top:44px"><div class="creds stagger" style="padding-top:30px"><span>Consultora certificada de NeuroChangeSolutions</span><span>MBA · IE Business School</span><span>+10 años de experiencia</span></div></div>
<section class="pad-s"><div class="wrap">
  {sec_title("Programas para empresas")}
  <div class="tiles stagger">
    <div class="tile bg-blush"><span class="n">01</span><h3 style="margin-top:34px">Talleres de bienestar y manejo del estrés</h3><p>Sesiones para tu equipo sobre manejo del estrés laboral y prevención del burnout, salud emocional, autoestima y hábitos. Incluyen baños de gong grupales.</p><span class="tag">Presencial o virtual</span></div>
    <div class="tile bg-sand"><span class="n">02</span><h3 style="margin-top:34px">Retiros corporativos y coaching para equipos</h3><p>Experiencias de uno o varios días, charlas y coaching empresarial para que tu equipo desconecte, se reconecte y vuelva con más claridad y energía.</p><span class="tag">Diseñados a la medida</span></div>
    <div class="tile bg-aqua"><span class="n">03</span><h3 style="margin-top:34px">Programa NCS del Dr. Joe Dispenza</h3><p>Change Your Mind… Create New Results: la neurociencia del cambio aplicada a líderes y equipos.</p><span class="tag">Consultora certificada</span></div>
  </div>
</div></section>
<section id="ncs" class="pad-s bg-sky"><div class="wrap">
  <div class="grid g2" style="align-items:start">
    <div><span class="kicker fade">NeuroChangeSolutions</span><h2 class="display-m lines" style="margin:14px 0 22px">Change Your Mind…<br>Create New Results</h2><p class="fade d1">Como consultora certificada de NeuroChangeSolutions, imparto el taller creado por el Dr. Joe Dispenza. Explica cómo funciona el cambio en el cerebro y en el cuerpo, y da a cada persona herramientas concretas para crearlo y sostenerlo en el tiempo.</p></div>
    <div class="fade d1" style="padding:clamp(24px,3vw,40px);background:rgba(249,245,237,.55);border-radius:3px"><span class="kicker">La premisa del programa</span><p class="display-s" style="margin:12px 0 0;font-size:clamp(1.3rem,2vw,1.7rem);line-height:1.3">El cambio sí es posible: existe un proceso para crearlo y sostenerlo, y se puede aprender.</p></div>
  </div>
  <div class="stats stagger" style="margin-top:clamp(24px,3vw,40px)">
    <div class="stat"><b>8+</b><span>Horas de taller</span><p>Un programa que se adapta a tu equipo y a tu organización.</p></div>
    <div class="stat"><b>2</b><span>Modelos de cambio</span><p>Para entender las etapas que atraviesa cada persona para cambiar.</p></div>
    <div class="stat"><b>4</b><span>Herramientas</span><p>Para crear y sostener el cambio, entre ellas el ensayo mental.</p></div>
  </div>
</div></section>
<section class="pad-s"><div class="wrap">{sec_title("Ideal para empresas que buscan")}<ul class="plist stagger"><li>Liderazgo consciente</li><li>Equipos preparados para el cambio</li><li>Menos estrés, más bienestar</li><li>Creatividad e innovación</li><li>Una cultura que retiene talento</li><li>Colaboración y productividad</li></ul></div></section>
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Cómo trabajamos")}{steps3([("Conversación", "Entendemos el momento de tu organización y lo que quieres lograr."), ("Propuesta", "Diseñamos el taller, retiro o programa adecuado para tu equipo."), ("Experiencia", "Llevamos la experiencia a tu equipo, presencial o virtual."), ("Seguimiento", "Acompañamos la integración del cambio en el día a día.")], cls="c4")}</div></section>
{tcards(['patprimo', 'barcu', 'cyglo', 'malva', 'johanna'], bg="bg-sand", title="Lo que dicen las empresas", cols=3)}
<section id="contacto" class="pad-s"><div class="wrap grid g2" style="align-items:start">
  <div><span class="kicker fade">Contacto</span><h2 class="display-m lines" style="margin:14px 0 18px">Diseñemos juntos la experiencia para tu equipo.</h2><p class="fade d1">Cuéntanos sobre tu organización y te enviaremos una propuesta a la medida.</p><p class="fade d2"><a href="mailto:info@spacetorise.com" style="text-decoration:underline">info@spacetorise.com</a></p></div>
  {lead_form("empresa", [("name", "Nombre", "text", None), ("company", "Empresa", "text", None), ("email", "Correo", "email", None), ("phone", "Teléfono", "tel", None), ("service", "Me interesa", "select", ["Talleres de bienestar", "Retiros corporativos", "Programa NCS del Dr. Joe Dispenza", "Baños de gong para equipos", "Aún no lo sé"]), ("message", "Cuéntanos sobre tu equipo", "textarea", None)], "Solicita una propuesta")}
</div></section>
""", cta=False)

# ------------------------------------------------------------------ SHOP
pages["/shop/"] = dict(title="Audios de autohipnosis guiada · Tienda y cursos | Space to Rise",
 desc="Audios de autohipnosis guiada para bajar de peso, dormir bien, superar la ansiedad y el miedo a volar. Reprograma tu mente en 15–20 minutos al día.", og="/assets/img/p/shop-hero.jpg",
 body=hero(IMG + "p/shop-hero.jpg", "Reconfigura tu cerebro en menos de 20 minutos al día", "Audios de autohipnosis y cursos para crear cambios permanentes en tu vida, desde donde estés.", kicker="Shop · Audios de autohipnosis y cursos", pos="center 25%", btn="Ver audios", href="#audios", cta2=("Ver cursos", "#cursos")) + f"""
<section class="pad-s"><div class="wrap feature" style="align-items:center">
  <div><span class="kicker fade">Cómo funcionan los audios</span><h2 class="display-m lines" style="margin:14px 0 20px">Ponte tus audífonos, recuéstate<br>y nosotros nos encargamos del resto.</h2><p class="fade d1">Es como una meditación guiada, pero en los primeros 3 minutos te guío a un estado de hipnosis. Así el audio llega a tu subconsciente, donde se guardan tus creencias y emociones, y reemplaza patrones negativos por creencias positivas y empoderadoras.</p>
    <div class="stats fade d1 stagger" style="margin-top:26px"><div class="stat bg-blush" style="border:0"><b>15–20</b><span>Minutos al día</span><p>Solo necesitas un espacio para relajarte.</p></div><div class="stat bg-sand" style="border:0"><b>21</b><span>Días mínimo</span><p>Lo que tarda tu mente en crear nuevos hábitos.</p></div><div class="stat bg-aqua" style="border:0"><b>100%</b><span>Seguro</span><p>Estás consciente y en control todo el tiempo.</p></div></div>
  </div>
  <div class="feature__media"><div class="media video wide"><video src="/assets/video/autohipnosis.mp4" poster="{IMG}../video/autohipnosis-poster.jpg" muted loop playsinline preload="metadata" data-start="6"></video><button class="unmute" type="button" aria-label="Ver con sonido">Ver</button></div></div>
</div></section>
<section id="cursos" class="pad-s bg-stone"><div class="wrap">{sec_title("Cursos")}{courses_html()}</div></section>
<section id="audios" class="pad-s"><div class="wrap">{sec_title("Audios de autohipnosis")}<div class="chips stagger" data-chips><button class="chip on" data-cat="all">Todos</button>{''.join(f'<button class="chip" data-cat="{c}">{n}</button>' for c, n, _ in AUDIO_CATS)}</div><div data-shop></div></div></section>
<section class="pad-s bg-blush"><div class="wrap" style="display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap"><div><span class="kicker fade">¿Quieres algo hecho solo para ti?</span><h2 class="display-m lines" style="margin:12px 0 10px">Tu audio personal llega con tu sesión de RTT (Rapid Transformational Therapy)</h2><p class="fade d1" style="margin:0;max-width:60ch">En cada sesión de RTT (Rapid Transformational Therapy) creo un audio de transformación personal, diseñado para tu historia y tus objetivos.</p></div><a class="pill solid fade d2" href="/agenda/"><span>Agenda tu sesión</span></a></div></section>
{tcards(['dormir', 'peso', 'avion'], bg="")}
""", cta=False)

# ------------------------------------------------------------------ PRODUCT PAGES
CATN = {c: n for c, n, _ in AUDIO_CATS}
for p in PRODUCTS:
    others = [x for x in PRODUCTS if x['id'] != p['id']][:3]
    rel = ''.join(f'<a class="disc" href="/shop/{x["slug"]}/"><div class="disc__art"><img src="{x["cover"]}" alt="{x["name"]}" loading="lazy"><span class="disc__hole"></span></div><h4>{x["name"]}</h4><div class="price">{fmt(x["price"])}</div></a>' for i, x in enumerate(others))
    seo_t = {'a10735': 'Hipnosis para bajar de peso · Audio', 'a10736': 'Hipnosis para dormir bien · Audio', 'a7143': 'Hipnosis para la ansiedad · Audio', 'a11260': 'Hipnosis para el miedo a volar · Audio', 'a11258': 'Hipnosis para dejar de vapear · Audio', 'a10737': 'Hipnosis para hablar en público · Audio', 'a10733': 'Hipnosis para la autoestima · Audio', 'a7151': 'Autohipnosis para atraer abundancia · Audio', 'a7154': 'Autohipnosis para el amor propio · Audio', 'a10742': 'Hipnosis para dejar de procrastinar · Audio', 'a11254': 'Hipnosis para pasar exámenes · Audio', 'a11256': 'Autohipnosis para atraer a tu pareja ideal · Audio', 'a10743': 'Hipnoparto · Audio de autohipnosis', 'a10741': 'Hipnosis para la fertilidad y FIV · Audio', 'a11257': 'Autohipnosis de energía sanadora · Audio'}
    ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": p['name'], "image": "https://spacetorise.com" + p['cover'], "description": p['short'].strip(), "brand": {"@type": "Brand", "name": "Space to Rise"}, "offers": {"@type": "Offer", "priceCurrency": "COP", "price": p['price'], "availability": "https://schema.org/InStock", "url": f"https://spacetorise.com/shop/{p['slug']}/"}}, ensure_ascii=False)
    pages[f"/shop/{p['slug']}/"] = dict(title=f"{seo_t.get(p['id'], p['name'] + ' · Audio de autohipnosis')} | Space to Rise", desc=(p['short'].strip().replace('\n', ' ')[:150] + '…'), og=p['cover'], ld=f'<script type="application/ld+json">{ld}</script>',
     body=f"""<section class="portal pad-s"><div class="wrap feature">
  <div class="feature__media"><div class="media square"><img src="{p['cover']}" alt="{p['name']}"></div></div>
  <div><span class="kicker fade">Shop / {CATN.get(p['category'], '')}</span><h1 class="display-m lines" style="margin:14px 0 18px">{p['name']}</h1><p class="lead fade d1">{p['description']}</p>
    <div class="price-tag fade d2">{fmt(p['price'])}<small>COP</small></div>
    <ul class="list fade d2" style="margin:0 0 26px"><li>Audio de autohipnosis de 15 a 20 minutos</li><li>Acceso inmediato en tu espacio privado, para escuchar donde quieras</li><li>Pensado para escucharlo cada día durante 21 días</li></ul>
    <div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap"><a class="pill solid" href="/checkout/?p={p['id']}"><span>Compra aquí</span></a><button class="pill" data-add="{p['id']}"><span>Añadir al carrito</span></button><a class="pill" href="/preguntas-frecuentes/" style="opacity:.8"><span>¿Tienes dudas?</span></a></div></div>
</div></section>
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Cómo usar tu audio")}{steps3([("Busca tu espacio", "Un lugar tranquilo donde puedas recostarte y desconectarte de 15 a 20 minutos."), ("Ponte tus audífonos", "Déjate guiar: en los primeros minutos entras en un estado de relajación profunda."), ("Repite 21 días", "La mente aprende por repetición. Escúchalo cada día para crear nuevos hábitos.")])}</div></section>
<section class="pad-s"><div class="wrap grid g2" style="align-items:start"><div><span class="kicker fade">Hipnosis 100% segura</span><h2 class="display-s lines" style="margin:12px 0 0">Estás consciente todo el tiempo.</h2></div><div><p class="fade">Puedes entrar y salir de la hipnosis muy fácilmente. Tu mente simplemente está más receptiva a las sugerencias que son buenas para ti.</p><p class="small muted fade d1">RTT (Rapid Transformational Therapy) es un acompañamiento complementario y no reemplaza el diagnóstico ni el tratamiento médico.</p></div></div></section>
<section class="pad-s bg-sand"><div class="wrap">{sec_title("Conoce otros audios", ("Ir al shop", "/shop/#audios"))}<div class="discs stagger">{rel}</div></div></section>
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
  <div class="media square"><img src="{IMG}Recupera-tu-amor-propio-scaled.jpg" alt="" loading="lazy"></div>
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
    <div><h3 class="display-s" style="margin-bottom:16px">Solicitudes (citas, empresas, newsletter)</h3><div data-admin-leads><p class="muted">Cargando…</p></div></div>
    <div><h3 class="display-s" style="margin-bottom:16px">Dar acceso manual</h3><form><div class="field"><label for="email">Correo del cliente</label><input id="email" name="email" type="email" required placeholder="cliente@correo.com"></div><div class="field"><label>Audios</label><div data-admin-products class="small"></div></div><button class="pill solid" type="submit"><span>Activar y enviar enlace</span></button></form></div>
  </div>
</div></section>""", cta=False)

# ------------------------------------------------------------------ SOBRE MÍ
pages["/sobre-mi/"] = dict(title="Andrea Zafra · Hipnoterapeuta clínica RTT en Bogotá | Space to Rise", og="/assets/img/p/andrea.jpg",
 desc="Hipnoterapeuta clínica especializada en RTT y consultora certificada de Joe Dispenza (NeuroChangeSolutions). Mi historia, mi formación y mi misión.",
 body=f"""<section class="portal pad-s"><div class="wrap feature">
  <div><span class="kicker fade">Sobre mí</span><h1 class="display-xl lines" style="margin:14px 0 18px">Andrea<br>Zafra</h1><p class="kicker fade d1" style="display:block;margin-bottom:20px;line-height:2">Hipnoterapeuta clínica especializada en RTT (Rapid Transformational Therapy)<br>Consultora certificada de Joe Dispenza (NeuroChangeSolutions)</p>
    <p class="fade d2" style="color:var(--charcoal)">Te ayudo a encontrar la raíz de lo que te bloquea y a reprogramar tu mente para que tu cambio sea real y permanente. Uno la hipnoterapia, la neurociencia del cambio y más de 10 años de experiencia para acompañar a personas, familias y organizaciones.</p>
    <div class="fade d3" style="display:flex;gap:12px;flex-wrap:wrap"><a class="pill solid" href="/agenda/"><span>Agenda tu cita</span></a><a class="pill" href="#historia"><span>Conoce mi historia</span></a></div></div>
  <div class="feature__media"><div class="media"><img src="{IMG}p/andrea.jpg" alt="Andrea Zafra, hipnoterapeuta clínica RTT"></div></div>
</div></section>
<section class="pad-s bg-aqua"><div class="wrap">{sec_title("Formación y certificaciones")}<div class="tiles stagger" style="grid-template-columns:repeat(5,1fr);gap:0 28px">
  <div class="fade"><b class="display-m" style="display:block">+10</b><span class="kicker" style="margin:6px 0 10px;display:block">Años de experiencia</span><p class="small" style="margin:0">Acompañando procesos de sanación y transformación personal.</p></div>
  <div class="fade d1"><b class="display-m" style="display:block">RTT</b><span class="kicker" style="margin:6px 0 10px;display:block">Hipnoterapeuta clínica</span><p class="small" style="margin:0">Especializada en Rapid Transformational Therapy, el método creado por Marisa Peer.</p></div>
  <div class="fade d2"><b class="display-m" style="display:block">NCS</b><span class="kicker" style="margin:6px 0 10px;display:block">Consultora certificada</span><p class="small" style="margin:0">NeuroChangeSolutions, formada por el Dr. Joe Dispenza en la neurociencia del cambio.</p></div>
  <div class="fade d3"><b class="display-m" style="display:block">MBA</b><span class="kicker" style="margin:6px 0 10px;display:block">IE Business School</span><p class="small" style="margin:0">Instituto de Empresa, Madrid.</p></div>
  <div class="fade d4"><b class="display-m" style="display:block">BSBA</b><span class="kicker" style="margin:6px 0 10px;display:block">Babson College</span><p class="small" style="margin:0">Licenciada en Administración de Empresas, Estados Unidos.</p></div>
</div><p class="kicker fade" style="margin-top:36px;display:block;text-align:center">Estudios complementarios · Crianza consciente · Nutrición · Energía · Mindfulness · Yoga</p></div></section>
<section id="historia" class="pad-s"><div class="wrap">{sec_title("Mi historia")}<div class="grid g2" style="align-items:start">
  <div><h2 class="display-m lines" style="margin:0 0 22px">Dicen que los hijos son nuestros grandes maestros, y en mi caso es así.</h2><p class="fade">Jerónimo, Olivia y Alexa despertaron en mí una pregunta que cambió mi vida: ¿cómo me convierto en la mejor versión de mí misma para ser su ejemplo?</p><p class="fade d1">Durante años construí una carrera exitosa. Estudié Administración de Empresas en Babson College, hice mi MBA en el IE, trabajé en grandes multinacionales y fundé varios negocios. Pero con la llegada de Alexa mi mundo dio un giro que me reconectó con mi verdadera esencia.</p></div>
  <div><p class="fade">Dejé el mundo corporativo para aprender todo lo que pudiera sobre crianza consciente, nutrición, energía, mindfulness y yoga. En el camino entendí algo que lo cambió todo: para darles a mis hijos lo que quería para ellos, primero tenía que transformarme yo. Superar mis miedos, cuestionar mis creencias y sanar mi cuerpo.</p><p class="fade d1">Esa búsqueda me llevó a la Terapia de Transformación Rápida (RTT, Rapid Transformational Therapy) de Marisa Peer y a la neurociencia del cambio del Dr. Joe Dispenza. Hoy uso estas herramientas para acompañar a otros en su propio camino de sanación.</p><div class="media wide fade d2" style="margin-top:22px"><img src="{IMG}p/sobre-mi-nina.jpg" alt="" loading="lazy"></div></div>
</div></div></section>
<section class="quote-band bg-taupe" data-dark><div class="wrap"><p class="fade">“No podemos ofrecer al mundo algo que no somos.”</p><cite class="fade d1">Andrea Zafra</cite></div></section>
<section id="mision" class="pad-s"><div class="wrap">
  <div class="grid g2" style="align-items:start"><div><span class="kicker fade">Mi misión</span><h2 class="display-m lines" style="margin:14px 0 0">Despertar el potencial humano de millones de personas, de adentro hacia afuera.</h2></div><div><p class="lead fade">Acompaño a personas, familias y organizaciones a liberarse de las creencias limitantes y los programas desactualizados que las enferman, las bloquean y les impiden ser su mejor versión.</p><p class="fade d1">Para lograrlo uno dos caminos que se potencian: la hipnoterapia RTT (Rapid Transformational Therapy), que llega a la raíz en el subconsciente, y la neurociencia del cambio del Dr. Joe Dispenza, que enseña cómo el cerebro y el cuerpo crean nuevos hábitos y los sostienen en el tiempo.</p></div></div>
  <div class="tiles stagger" style="margin-top:clamp(36px,5vw,64px)">
    <div class="tile bg-blush" style="min-height:0"><span class="tag" style="margin:0 0 10px">Personas</span><p>Que cada persona sane su cuerpo y su mente, recupere su poder interior y alcance lo que sueña.</p></div>
    <div class="tile bg-sand" style="min-height:0"><span class="tag" style="margin:0 0 10px">Familias</span><p>Que los padres críen nuevas generaciones libres de miedos, con autoestima alta y alas fuertes para volar alto.</p></div>
    <div class="tile bg-aqua" style="min-height:0"><span class="tag" style="margin:0 0 10px">Empresas</span><p>Que líderes y equipos sean más conscientes, sanos y creativos, capaces de adaptarse al cambio y crecer juntos.</p></div>
  </div>
  <p class="caps fade" style="margin:clamp(40px,5vw,64px) auto 8px;text-align:center">Porque cuando una persona se transforma, transforma su familia, su equipo y su entorno.</p>
  <p class="display-s fade d1" style="text-align:center;margin:0;font-style:italic">¡Al despertar tu mundo, iluminas el mundo!</p>
</div></section>
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Cómo puedo acompañarte")}<div class="tiles stagger">
  <a class="tile" href="/heal-rise-shine/" style="background:var(--white);min-height:0"><span class="tag" style="margin:0 0 10px">Personas</span><h3>Heal · Rise · Shine</h3><p>Sesiones de RTT (Rapid Transformational Therapy) para sanar tu cuerpo, liberar tu mente y alcanzar tus objetivos.</p><span class="tag">Conoce más →</span></a>
  <a class="tile" href="/kids/" style="background:var(--white);min-height:0"><span class="tag" style="margin:0 0 10px">Familias</span><h3>Kids</h3><p>Herramientas para que tus hijos crezcan con una autoestima alta, libres de miedos y creencias limitantes.</p><span class="tag">Conoce más →</span></a>
  <a class="tile" href="/empresas/" style="background:var(--white);min-height:0"><span class="tag" style="margin:0 0 10px">Empresas</span><h3>Bienestar corporativo</h3><p>Talleres, retiros y el programa NCS del Dr. Joe Dispenza para equipos y líderes.</p><span class="tag">Conoce más →</span></a>
</div></div></section>
""", cta_title="Me encantaría acompañarte", cta_sub="Agenda una llamada inicial y conversemos sobre lo que quieres transformar.")

# ------------------------------------------------------------------ GIFT
pages["/gif-for-you/"] = dict(title="Gift for you — Recursos gratuitos | Space to Rise",
 desc="Audios y PDFs gratuitos para inspirarte y acompañarte: descarga los tips para reducir la ansiedad y la depresión.",
 body=hero(IMG + "Ansiedad-y-Depresion.jpg", "Gift for you", "Recursos exclusivos, solo para ti.", kicker="Gratis", pos="center 30%", cta=False) + f"""
<section class="pad"><div class="wrap feature">
  <div><p class="lead fade">Descubre nuestra colección de audios y PDFs gratuitos, pensados para inspirarte, impulsarte y acompañarte en cada paso.</p><p class="fade d1">Porque en Space to Rise creemos que el conocimiento debe estar al alcance de todos. ¡Empieza hoy mismo!</p></div>
  <div class="feature__media"><div class="media wide"><img src="{IMG}Ansiedad-y-Depresion.jpg" alt="" loading="lazy"></div><h3 class="display-s" style="margin-top:22px">Tips para reducir la ansiedad y la depresión</h3><p class="small muted" style="margin:8px 0 18px">Guía en PDF con herramientas efectivas que puedes aplicar en tu día a día.</p><a class="pill solid" href="/assets/doc/Depresion-y-Ansiedad.pdf" download><span>Descarga aquí</span></a></div>
</div></section>""")

# ------------------------------------------------------------------ FAQ
FAQ = [
 ("Sobre Space to Rise", [
  ("¿Qué es Space to Rise?", ENTITY),
  ("¿Quién es Andrea Zafra?", "Andrea Zafra es hipnoterapeuta clínica especializada en Rapid Transformational Therapy (RTT), consultora certificada de NeuroChangeSolutions (el programa del Dr. Joe Dispenza), MBA del IE Business School y administradora de empresas de Babson College. Fundó Space to Rise en Bogotá y acompaña a personas, familias y organizaciones de forma presencial y online."),
  ("¿Dónde atiende Space to Rise?", "En Bogotá, Colombia, de forma presencial, y online por Zoom para cualquier ciudad o país. Los audios de autohipnosis se compran en la tienda y se escuchan desde un espacio privado en cualquier dispositivo.")]),
 ("Sobre RTT", [
  ("¿Qué es RTT (Rapid Transformational Therapy)?", "Rapid Transformational Therapy es una terapia desarrollada por Marisa Peer que combina lo más eficaz de la hipnosis, la PNL y la neurociencia para lograr resultados rápidos, permanentes y transformadores. Generalmente se logra sanar en 1 o máximo 3 sesiones, según la complejidad del tema."),
  ("¿Por qué hipnosis?", "La hipnosis permite acceder al subconsciente, donde están tu programación, tus memorias y tus creencias. Así entendemos por qué reaccionas como reaccionas, encontramos la raíz del problema, la sanamos y creamos nuevas conexiones neuronales."),
  ("¿Por qué RTT (Rapid Transformational Therapy) es tan efectiva?", "Porque cambia tus creencias a nivel subconsciente. La mente consciente es la parte lógica, pero el subconsciente maneja cerca del 95% de nuestras decisiones: hasta que no lo cambias, ningún cambio es real y permanente."),
  ("¿Qué puedo sanar y transformar con RTT (Rapid Transformational Therapy)?", "Temas físicos como enfermedades crónicas y problemas de piel, pelo o digestivos; temas emocionales como ansiedad, estrés, autoestima, fobias, adicciones, insomnio, control de peso, fertilidad y relaciones; y temas de desempeño como metas y rendimiento deportivo. Es apta para niños y adultos, y complementa, no reemplaza, el tratamiento médico.")]),
 ("Las sesiones", [
  ("¿Cómo son las sesiones de RTT (Rapid Transformational Therapy)?", "Tienen 3 partes: una llamada de 20 minutos para aclarar dudas; la terapia, de aproximadamente 3 horas, donde con hipnosis vamos a la raíz del problema y lo liberamos; y un audio personalizado de 15 a 20 minutos que escuchas cada día durante al menos 21 días."),
  ("¿Cuánto tiempo dura la sesión?", "Aproximadamente 3 horas. Te recomiendo reservar ese tiempo completo en tu calendario para no estar apurada."),
  ("¿Qué pasa si necesito otra sesión?", "Algunos temas más profundos pueden requerir hasta tres sesiones. Muchos clientes continúan con sesiones para otras áreas de su vida o con coaching para integrar sus nuevas creencias y hábitos.")]),
 ("La hipnosis", [
  ("¿La hipnosis es real y para qué sirve?", "Sí. La hipnosis es un estado natural de relajación profunda y atención enfocada, respaldado por la neurociencia, en el que tu mente subconsciente es más receptiva. En hipnoterapia sirve para encontrar y cambiar la raíz de la ansiedad, los miedos, el insomnio, los hábitos y muchos síntomas físicos."),
  ("¿La hipnosis tiene peligros?", "No, cuando la guía una hipnoterapeuta clínica. No pierdes el control ni haces nada que no quieras: puedes hablar, moverte o abrir los ojos en cualquier momento. RTT (Rapid Transformational Therapy) es un acompañamiento complementario y no reemplaza el diagnóstico ni el tratamiento médico."),
  ("¿Cómo se siente estar hipnotizado?", "La mayoría de las personas se siente muy relajada. Estás 100% en control de tu cuerpo: puedes hablar, moverte o acomodarte cuando quieras, y solo aceptas las sugerencias que tú quieras."),
  ("¿Puedo quedarme atrapado en la hipnosis?", "No. Tienes control completo durante toda la sesión. Si haces tu sesión por Zoom y se corta la llamada, como mucho te quedarás dormido por la relajación y luego abrirás los ojos."),
  ("¿Cómo funciona?", "La hipnosis no es magia: se basa en principios científicos. Al relajarte, tu cerebro produce ondas alfa, parecidas a las del sueño, que permiten acceder al subconsciente. Es simple y posible para todo el mundo."),
  ("¿Qué pasa si veo escenas dolorosas?", "No las revives, las observas desde un lugar seguro y desde tu perspectiva adulta. Estaré a tu lado todo el tiempo para que puedas expresar tus emociones y sanar."),
  ("¿Qué pasa si no entro suficientemente profundo?", "La profundidad del trance no es crucial para los resultados. La efectividad no depende de qué tan profundo vayas.")]),
 ("Resultados", [
  ("¿Cómo se ven los resultados?", "De tres formas: inmediatos, cuando sales sintiéndote liviana y en paz; progresivos, en 10 a 21 días mientras dejas atrás viejos hábitos; y retroactivos, cuando son otros quienes notan el cambio primero."),
  ("¿Qué pasa si ya conozco el motivo de mi problema?", "RTT (Rapid Transformational Therapy) suele mostrar una perspectiva nueva sobre problemas conocidos y te permite cambiar su significado. Relájate y confía en que tu subconsciente te mostrará lo necesario.")]),
]
faq_html = ''.join(f'<div class="grid g2 fade" style="grid-template-columns:.6fr 1.4fr;align-items:start;padding:24px 0;border-top:1px solid rgba(58,58,57,.16)"><span class="kicker">{g}</span><div class="acc stagger">' + ''.join(f'<div class="acc__item"><button class="acc__q">{q}<i></i></button><div class="acc__a"><div><div class="inner"><p>{a}</p></div></div></div></div>' for q, a in qs) + '</div></div>' for g, qs in FAQ)
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for g, qs in FAQ for q, a in qs]}, ensure_ascii=False)
pages["/preguntas-frecuentes/"] = dict(title="¿La hipnosis es real? Preguntas frecuentes sobre RTT | Space to Rise",
 desc="¿La hipnosis es real? ¿Tiene peligros? ¿Para qué sirve la hipnoterapia y funciona? ¿Cómo se siente? Respuestas claras de una hipnoterapeuta clínica RTT.",
 body=f"""<section class="portal pad-s"><div class="wrap">
  <div class="narrow center" style="margin:0 auto clamp(28px,4vw,48px)"><span class="kicker fade">Preguntas frecuentes</span><h1 class="display-l lines" style="margin:14px 0 18px">Todo lo que quieres saber sobre la hipnosis y RTT (Rapid Transformational Therapy)</h1><p class="muted fade d1">Si no encuentras tu respuesta aquí, escríbeme a <a href="mailto:info@spacetorise.com" style="text-decoration:underline">info@spacetorise.com</a> o agenda tu llamada inicial.</p></div>
  {faq_html}
</div></section><script type="application/ld+json">{faq_ld}</script>""", cta_title="¿Te quedó alguna duda?", cta_sub="En la llamada inicial de 20 minutos resolvemos todas tus preguntas.")

# ------------------------------------------------------------------ AGENDA
pages["/agenda/"] = dict(title="Agenda tu cita de hipnoterapia RTT en Bogotá u online | Space to Rise",
 desc="Cuéntame qué te gustaría transformar y te contacto para agendar una llamada inicial de 20 minutos, sin compromiso.",
 body=f"""<section class="portal pad-s"><div class="wrap grid g2" style="align-items:start">
  <div><span class="kicker fade">Agenda tu cita</span><h1 class="display-l lines" style="margin:14px 0 18px">Tu transformación empieza con una conversación.</h1><p class="fade d1">Cuéntame qué te gustaría transformar y te contacto para agendar una llamada inicial de 20 minutos, sin compromiso, para resolver tus dudas y elegir juntas el mejor camino.</p>
    <div class="steps fade d2" style="margin-top:26px"><div class="step" style="grid-template-columns:48px 1fr;padding:20px 0"><div class="n">01</div><div><h4>Envía tu solicitud</h4><p>Completa el formulario o escríbeme por WhatsApp.</p></div></div><div class="step" style="grid-template-columns:48px 1fr;padding:20px 0"><div class="n">02</div><div><h4>Llamada inicial</h4><p>20 minutos para conocernos y aclarar tus preguntas.</p></div></div><div class="step" style="grid-template-columns:48px 1fr;padding:20px 0"><div class="n">03</div><div><h4>Tu sesión</h4><p>Presencial o por Zoom, en el horario que mejor te funcione.</p></div></div></div></div>
  {lead_form("agenda", [("name", "Nombre", "text", None), ("email", "Correo", "email", None), ("phone", "WhatsApp", "tel", None), ("city", "País y ciudad", "text", None), ("service", "Servicio", "select", ["Sesión de RTT (Rapid Transformational Therapy)", "RTT Kids", "Coaching individual", "Baño de gong", "Empresas", "Aún no lo sé"]), ("message", "¿Qué te gustaría transformar?", "textarea", None)], "Enviar solicitud", intro="Solicita tu llamada inicial", extra=f'<a class="pill" href="{WA}" target="_blank" rel="noopener"><span>O escríbeme por WhatsApp</span></a>')}
</div></section>
<section class="pad-s bg-stone"><div class="wrap">{sec_title("Servicios y valores")}<div class="tiles c4 stagger">
  <div class="pricecard bg-blush"><span class="k">Personas</span><h4>Sesión de RTT (Rapid Transformational Therapy)</h4><p>Sesión de 3 horas con tu audio personal de 21 días.</p><b>$480.000</b></div>
  <div class="pricecard bg-rose"><span class="k">Niños</span><h4>RTT (Rapid Transformational Therapy) Kids</h4><p>Sesión adaptada a la edad de tu hijo, con su audio personal.</p><b>$380.000</b></div>
  <div class="pricecard bg-aqua"><span class="k">Integración</span><h4>Coaching individual</h4><p>Sesión de 1 hora, presencial o por Zoom.</p><b>$180.000</b></div>
  <div class="pricecard bg-sky"><span class="k">Sonido</span><h4>Baño de gong</h4><p>Individual o grupal, para ti, tu familia o tu equipo.</p><b>$180.000 <small style="font-size:.5em">· $120.000 p/p grupal</small></b></div>
</div><p class="fade" style="margin:28px 0 0">¿Buscas algo para tu empresa? <a href="/empresas/" style="text-decoration:underline">Conoce los programas para empresas →</a></p></div></section>
{tcards(['rtt', 'dormir', 'confianza'], bg="")}
""", cta=False)

SVC = {'/rtt/': ('Sesión de hipnoterapia RTT', '480000', 'Hipnoterapia RTT (Rapid Transformational Therapy): hipnosis clínica, PNL y neurociencia para encontrar la raíz de lo que te bloquea y reprogramarla. Sesión de aproximadamente 3 horas más audio personal de 21 días.'), '/kids/': ('RTT Kids · hipnoterapia para niños', '380000', 'Hipnoterapia para niños adaptada a su edad, con audio personal para reforzar el cambio en casa.'), '/coaching/': ('Coaching individual', '180000', 'Sesiones de coaching de vida de 1 hora, presenciales en Bogotá o por Zoom.'), '/gong/': ('Baño de gong', '180000', 'Baño de sonido con gong para relajación profunda, liberación emocional y equilibrio energético. Individual $180.000, grupal $120.000 por persona.'), '/empresas/': ('Programas de bienestar laboral para empresas', None, 'Talleres de manejo del estrés y burnout, retiros corporativos, coaching para equipos y el programa NCS del Dr. Joe Dispenza. Presencial en Bogotá o virtual.'), '/heal-rise-shine/': ('Hipnoterapia RTT · Heal, Rise, Shine', '480000', 'RTT para sanar el cuerpo (Heal), liberar la mente de ansiedad, miedos y fobias (Rise) y alcanzar objetivos (Shine).')}
for _p, (_n, _price, _d) in SVC.items():
    if _p in pages:
        _o = {"@context": "https://schema.org", "@type": "Service", "name": _n, "serviceType": _n, "description": _d, "url": "https://spacetorise.com" + _p, "provider": {"@id": "https://spacetorise.com/#org"}, "areaServed": ["Bogotá", "Colombia", "Online"], "availableChannel": [{"@type": "ServiceChannel", "name": "Presencial en Bogotá"}, {"@type": "ServiceChannel", "name": "Online por Zoom"}]}
        if _price: _o["offers"] = {"@type": "Offer", "price": _price, "priceCurrency": "COP", "availability": "https://schema.org/InStock", "url": "https://spacetorise.com/agenda/"}
        pages[_p]['ld'] = (pages[_p].get('ld') or '') + '<script type="application/ld+json">' + json.dumps(_o, ensure_ascii=False) + '</script>'

# ------------------------------------------------------------------ BUILD
for path, p in pages.items():
    d = os.path.join(OUT, path.strip('/')) if path != '/' else OUT
    os.makedirs(d, exist_ok=True)
    fkw = {k: p[k] for k in ('cta', 'cta_title', 'cta_sub', 'cta_btn', 'cta_href') if k in p}
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(head(p['title'], p['desc'], path, portal=p.get('portal', False), og=p.get('og'), ld=p.get('ld')) + p['body'] + foot(**fkw))
    print('wrote', path)
pub = [p for p, v in pages.items() if not v.get('portal')]
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>https://spacetorise.com{p}</loc></url>' for p in pub) + '</urlset>')
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /mis-audios/\nDisallow: /checkout/\n\nUser-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ChatGPT-User\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: https://spacetorise.com/sitemap.xml\n')
open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf-8').write(f"""# Space to Rise

> {ENTITY}

Fundadora: Andrea Zafra — hipnoterapeuta clínica RTT (método de Marisa Peer), consultora certificada NeuroChangeSolutions (Dr. Joe Dispenza), MBA IE Business School, BSBA Babson College. Sede: Bogotá, Colombia. Atención presencial y online (Zoom). Contacto: info@spacetorise.com · WhatsApp +57 310 750 3359.

## Servicios y precios (COP)
- Sesión de hipnoterapia RTT (aprox. 3 h + audio personal de 21 días): $480.000 — https://spacetorise.com/rtt/
- Heal · Rise · Shine (RTT para sanar el cuerpo, la mente y alcanzar objetivos): https://spacetorise.com/heal-rise-shine/
- RTT Kids (hipnoterapia para niños): $380.000 — https://spacetorise.com/kids/
- Coaching individual (1 h, presencial o Zoom): $180.000 — https://spacetorise.com/coaching/
- Baño de gong: individual $180.000 · grupal $120.000 por persona — https://spacetorise.com/gong/
- Empresas: talleres de bienestar y manejo del estrés, retiros corporativos, programa NCS de Joe Dispenza — https://spacetorise.com/empresas/
- Audios de autohipnosis ($55.500 c/u): https://spacetorise.com/shop/

## Páginas
- Sobre Andrea Zafra: https://spacetorise.com/sobre-mi/
- Preguntas frecuentes sobre hipnosis y RTT: https://spacetorise.com/preguntas-frecuentes/
- Agenda una llamada inicial de 20 minutos: https://spacetorise.com/agenda/
""")
