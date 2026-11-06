# -*- coding: utf-8 -*-
"""Guías educativas (blog) de Space to Rise. Cada guía es un dict; build.py las convierte en páginas."""
import json, html

GUIAS = []

# ------------------------------------------------------------------ GUÍA 1 · nov 2026
G1_FAQ = [
    ("¿Qué significa RTT?",
     "RTT son las siglas de Rapid Transformational Therapy, que en español se conoce como Terapia de Transformación Rápida. Es un método de hipnoterapia creado por la terapeuta británica Marisa Peer."),
    ("¿En qué se diferencia RTT de la hipnosis tradicional?",
     "La hipnosis tradicional suele trabajar con sugerencias para cambiar un síntoma o un hábito. RTT usa la hipnosis para ir a la raíz: busca las experiencias y creencias que originaron el problema, ayuda a entenderlas desde la perspectiva adulta y las reemplaza por creencias nuevas. Además combina técnicas de PNL, psicoterapia y terapia cognitivo-conductual, y se refuerza con un audio personalizado."),
    ("¿Cuántas sesiones de RTT se necesitan?",
     "Depende de la persona y del tema. Muchos terapeutas certificados trabajan con una sesión principal y, si hace falta, hasta tres. Cada sesión va acompañada de un audio para escuchar durante al menos 21 días."),
    ("¿Por qué hay que escuchar el audio durante 21 días?",
     "El audio repite las nuevas creencias trabajadas en la sesión para que la mente las integre con la práctica diaria. Escucharlo a diario durante al menos 21 días es parte del método y ayuda a que el cambio se mantenga."),
    ("¿RTT tiene respaldo científico?",
     "La hipnosis clínica en general tiene evidencia sólida para el manejo del dolor, el estrés y la ansiedad. Sobre RTT como método específico, la investigación todavía está en desarrollo: los resultados que se reportan provienen sobre todo de la práctica de los terapeutas y de la experiencia de los pacientes. Por eso se usa como complemento, no como reemplazo de un tratamiento médico o psicológico."),
    ("¿La hipnoterapia RTT tiene riesgos?",
     "Guiada por un terapeuta certificado se considera segura. Como en cualquier hipnosis, pueden aparecer mareo, dolor de cabeza, somnolencia o emociones intensas pasajeras. Si tienes un diagnóstico de enfermedad mental grave, consulta primero con tu médico tratante."),
    ("¿Se puede hacer RTT online?",
     "Sí. La sesión por videollamada sigue la misma estructura que la presencial: solo necesitas un lugar tranquilo, buena conexión y audífonos."),
]

G1_BODY = f"""
<p class="lead-p">Si has escuchado hablar de la <strong>hipnoterapia RTT</strong> y quieres entender qué es antes de decidir nada, esta guía es para ti. Te explicamos de dónde viene, cómo funciona una sesión, para qué se usa, qué dice la evidencia y qué preguntas hacerte antes de empezar.</p>

<nav class="toc" aria-label="Contenido de la guía"><span class="kicker">En esta guía</span><ol>
<li><a href="#que-es">Qué es la hipnoterapia RTT</a></li>
<li><a href="#origen">Quién la creó</a></li>
<li><a href="#diferencia">En qué se diferencia de la hipnosis tradicional</a></li>
<li><a href="#sesion">Cómo es una sesión</a></li>
<li><a href="#para-que">Para qué se usa</a></li>
<li><a href="#evidencia">Qué dice la evidencia</a></li>
<li><a href="#riesgos">Riesgos y cuándo tener cuidado</a></li>
<li><a href="#mitos">Mitos frecuentes</a></li>
</ol></nav>

<h2 id="que-es">¿Qué es la hipnoterapia RTT?</h2>
<p><strong>RTT</strong> son las siglas de <em>Rapid Transformational Therapy</em>, o <strong>Terapia de Transformación Rápida</strong>. Es un método de hipnoterapia que combina la hipnosis con elementos de <strong>programación neurolingüística (PNL), psicoterapia, terapia cognitivo-conductual (TCC) y neurociencia</strong>.</p>
<p>Su idea central es sencilla: muchos bloqueos actuales, como la ansiedad, un miedo o un hábito que no logras dejar, tienen su origen en experiencias y creencias que se formaron hace tiempo y que siguen operando sin que te des cuenta. RTT usa la hipnosis para <strong>encontrar esa raíz</strong>, entenderla y reemplazar la creencia que ya no te sirve por una nueva.</p>

<h2 id="origen">¿Quién creó RTT?</h2>
<p>RTT fue creada por <strong>Marisa Peer</strong>, terapeuta y formadora de hipnoterapeutas británica. Hoy existe una red internacional de terapeutas formados y certificados en el método, que trabajan de forma presencial y online.</p>

<h2 id="diferencia">¿En qué se diferencia de la hipnosis tradicional?</h2>
<p>La hipnosis clínica tradicional trabaja sobre todo con <strong>sugerencias</strong>: en estado de relajación, el terapeuta propone ideas que ayudan a cambiar un síntoma o un hábito. RTT añade tres elementos:</p>
<ul>
<li><strong>Ir a la causa, no solo al síntoma.</strong> Con la hipnosis se exploran los recuerdos y experiencias relacionados con el tema que quieres trabajar.</li>
<li><strong>Entender desde la perspectiva adulta.</strong> No se trata de revivir lo difícil, sino de observarlo desde un lugar seguro y darle un significado nuevo.</li>
<li><strong>Un audio personalizado.</strong> Después de la sesión recibes una grabación con tus nuevas creencias para escucharla a diario durante al menos 21 días.</li>
</ul>

<h2 id="sesion">¿Cómo es una sesión de RTT?</h2>
<p>La duración varía según el terapeuta: suele estar entre una hora y media y tres horas. La estructura general es esta:</p>
<ol>
<li><strong>Conversación inicial.</strong> Hablas de lo que quieres transformar y el terapeuta entiende tu historia y tu objetivo.</li>
<li><strong>Hipnosis.</strong> Entras en un estado de relajación profunda y atención concentrada. Sigues consciente y en control: puedes hablar, moverte o abrir los ojos cuando quieras.</li>
<li><strong>Exploración.</strong> Se buscan las escenas y experiencias relacionadas con tu tema para entender cómo se formó la creencia que hoy te limita.</li>
<li><strong>Transformación.</strong> Con técnicas de reencuadre se reemplaza esa creencia por una nueva y más útil.</li>
<li><strong>Tu audio.</strong> Recibes una grabación personalizada para escuchar durante al menos 21 días y que tu mente integre el cambio.</li>
</ol>
<p>Muchos terapeutas trabajan con <strong>una sesión principal</strong> y, según la complejidad del tema, hasta tres.</p>

<h2 id="para-que">¿Para qué se usa la hipnoterapia RTT?</h2>
<p>Se usa como acompañamiento en temas emocionales, de hábitos y de desempeño, por ejemplo:</p>
<ul>
<li>Ansiedad, estrés y preocupación constante.</li>
<li>Miedos y fobias, como el miedo a volar o a hablar en público.</li>
<li>Insomnio y dificultad para descansar.</li>
<li>Autoestima, inseguridad y creencias limitantes.</li>
<li>Hábitos como fumar, vapear, comer por ansiedad o procrastinar.</li>
<li>Metas personales, profesionales y deportivas.</li>
</ul>
<p>También existe una adaptación para niños, <a href="/kids/">RTT Kids</a>.</p>

<h2 id="evidencia">¿Qué dice la evidencia?</h2>
<p>Conviene separar dos cosas. La <strong>hipnosis clínica</strong> en general tiene evidencia sólida: según la Clínica Mayo, puede ayudar a manejar el <strong>dolor, el estrés y la ansiedad</strong>, y es útil como parte de un plan más amplio para cambiar hábitos.</p>
<p>Sobre <strong>RTT como método específico</strong>, la investigación todavía está en desarrollo: los resultados rápidos que se reportan provienen sobre todo de la práctica de los terapeutas y de la experiencia de los pacientes. Por eso la presentamos como lo que es: un <strong>acompañamiento complementario</strong> que a muchas personas les funciona, no una cura garantizada.</p>

<h2 id="riesgos">Riesgos y cuándo tener cuidado</h2>
<p>Guiada por un terapeuta certificado, la hipnoterapia se considera segura. Las reacciones adversas son poco comunes y suelen ser leves y pasajeras: <strong>mareo, dolor de cabeza, somnolencia o emociones intensas</strong> durante o después de la sesión.</p>
<div class="callout"><p><strong>Cuándo consultar primero.</strong> Si tienes un diagnóstico de enfermedad mental grave, habla antes con tu médico tratante. Y si vas a trabajar experiencias traumáticas, hazlo con un terapeuta con experiencia. RTT <strong>complementa, no reemplaza</strong>, el diagnóstico ni el tratamiento médico o psicológico.</p></div>

<h2 id="mitos">Mitos frecuentes sobre la hipnoterapia</h2>
<ul>
<li><strong>«Voy a perder el control.»</strong> No. Escuchas todo, puedes hablar y moverte, y no harás nada que no quieras.</li>
<li><strong>«Me puedo quedar atrapado en la hipnosis.»</strong> No. Si la sesión se interrumpe, como mucho te quedarías dormido por la relajación y luego abrirías los ojos.</li>
<li><strong>«Si no entro muy profundo, no funciona.»</strong> La profundidad del trance no es lo que define el resultado.</li>
<li><strong>«Es como la hipnosis de espectáculo.»</strong> Nada que ver: en terapia tú eres quien quiere el cambio y el proceso está a tu servicio.</li>
</ul>

<h2 id="empezar">¿Quieres probar la hipnoterapia RTT?</h2>
<p>En Space to Rise, <a href="/sobre-mi/">Andrea Zafra</a>, hipnoterapeuta clínica certificada en RTT, acompaña procesos de forma presencial en Bogotá y online para Colombia, Latinoamérica y España. Conoce <a href="/rtt/">cómo son las sesiones de RTT</a> o, si prefieres, empieza con una conversación.</p>
<div class="inline-cta"><p>¿Quieres saber si RTT es para ti?</p><a class="pill solid" href="/agenda/"><span>Agenda tu llamada inicial</span></a></div>

<h2 id="preguntas">Preguntas frecuentes</h2>
<div class="acc">{''.join(f'<div class="acc__item"><button class="acc__q">{q}<i></i></button><div class="acc__a"><div><div class="inner"><p>{a}</p></div></div></div></div>' for q, a in G1_FAQ)}</div>

<div class="sources"><span class="kicker">Fuentes</span><ul>
<li><a href="https://www.mayoclinic.org/es/tests-procedures/hypnosis/about/pac-20394405" target="_blank" rel="noopener">Clínica Mayo · Hipnosis: descripción general, usos y riesgos</a></li>
<li><a href="https://hypnotherapy-directory.org.uk/approach/rapid-transformational-therapy.html" target="_blank" rel="noopener">Hypnotherapy Directory · Rapid Transformational Therapy</a></li>
</ul><p class="small muted">Esta guía es informativa y no sustituye la valoración de un profesional de la salud.</p></div>
"""

GUIAS.append(dict(
    slug="que-es-la-hipnoterapia-rtt",
    title="¿Qué es la hipnoterapia RTT? Cómo funciona y para qué sirve | Space to Rise",
    h1="¿Qué es la hipnoterapia RTT? Cómo funciona, para qué sirve y qué esperar",
    desc="Guía de la hipnoterapia RTT (Rapid Transformational Therapy): qué es, quién la creó, cómo es una sesión, para qué se usa, qué dice la evidencia, riesgos y mitos frecuentes.",
    card="Qué es la Terapia de Transformación Rápida, cómo es una sesión, para qué se usa, qué dice la evidencia y qué esperar.",
    img="p/rtt-costa.jpg",
    date="2026-11-05", date_h="5 de noviembre de 2026", read="7 min de lectura",
    body=G1_BODY, faq=G1_FAQ,
))


def guia_page(g, IMG):
    url = f"https://spacetorise.com/guias/{g['slug']}/"
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g['h1'], "description": g['desc'],
           "image": f"https://spacetorise.com{IMG}{g['img']}", "datePublished": g['date'], "dateModified": g['date'],
           "inLanguage": "es-CO", "mainEntityOfPage": url,
           "author": {"@id": "https://spacetorise.com/#org"}, "publisher": {"@id": "https://spacetorise.com/#org"},
           "about": [{"@type": "Thing", "name": "Hipnosis clínica"}, {"@type": "Thing", "name": "Hipnoterapia RTT"}]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g['faq']]}
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (art, faq))
    body = f"""<section class="portal pad-s"><div class="wrap">
  <article class="article">
    <header class="article__head">
      <a class="kicker fade" href="/guias/">Guías · Hipnoterapia</a>
      <h1 class="display-m lines" style="margin:14px 0 18px">{g['h1']}</h1>
      <p class="small muted fade d1">{g['date_h']} · {g['read']} · Space to Rise</p>
    </header>
    <figure class="article__img fade d2"><img src="{IMG}{g['img']}" alt="{html.escape(g['h1'])}" loading="eager"></figure>
    <div class="article__body">{g['body']}</div>
  </article>
</div></section>"""
    return dict(title=g['title'], desc=g['desc'], body=body, ld=ld, og=None,
                cta_title="Tu transformación empieza con una conversación",
                cta_sub="Agenda una llamada inicial de 20 minutos, sin costo, y resolvemos juntas si la hipnoterapia RTT es para ti.")


def guias_index(IMG):
    cards = ''.join(f"""<a class="gcard fade" href="/guias/{g['slug']}/"><div class="gcard__img"><img src="{IMG}{g['img']}" alt="{html.escape(g['h1'])}" loading="lazy"></div><div class="gcard__body"><span class="kicker">{g['date_h']} · {g['read']}</span><h2>{g['h1']}</h2><p>{g['card']}</p><span class="gcard__more">Leer la guía →</span></div></a>""" for g in GUIAS)
    body = f"""<section class="portal pad-s"><div class="wrap">
  <div class="narrow center" style="margin:0 auto clamp(28px,4vw,48px)"><span class="kicker fade">Guías</span><h1 class="display-m lines" style="margin:14px 0 18px">Guías sobre hipnosis, hipnoterapia y bienestar</h1><p class="muted fade d1">Respuestas claras a las preguntas más comunes sobre hipnosis clínica, hipnoterapia RTT y autohipnosis, escritas por el equipo de Space to Rise.</p></div>
  <div class="gcards">{cards}</div>
</div></section>"""
    return dict(title="Guías de hipnosis clínica e hipnoterapia RTT | Space to Rise",
                desc="Guías claras sobre hipnosis clínica, hipnoterapia RTT y autohipnosis: qué es, para qué sirve, riesgos, precios y cómo elegir a tu hipnoterapeuta en Bogotá y online.",
                body=body)
