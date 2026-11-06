# -*- coding: utf-8 -*-
"""Guías educativas (blog) de Space to Rise. Cada guía es un dict; build.py las convierte en páginas."""
import json, html

GUIAS = []

# ------------------------------------------------------------------ GUÍA 1 · nov 2026
G1_FAQ = [
    ("¿Qué es la hipnosis clínica?",
     "Es el uso de la hipnosis con fines terapéuticos, guiado por un profesional formado. Durante la sesión entras en un estado de relajación y atención concentrada en el que eres más receptiva a sugerencias para cambiar un hábito, una emoción o una creencia. No pierdes el control ni la conciencia: puedes hablar, moverte o abrir los ojos cuando quieras."),
    ("¿Cuánto vale una sesión de hipnosis en Colombia?",
     "Depende del profesional, de la duración y de lo que incluya. En directorios de salud de Bogotá, a noviembre de 2026, las sesiones de hipnosis clínica se publican aproximadamente entre $110.000 y $420.000 COP. En Space to Rise, una sesión de hipnoterapia RTT cuesta $480.000 e incluye una llamada inicial, la sesión de unas 3 horas y un audio personalizado para escuchar durante 21 días."),
    ("¿Qué tan efectiva es la hipnosis clínica?",
     "La evidencia es más sólida para el manejo del dolor, el estrés y la ansiedad, incluida la ansiedad antes de procedimientos médicos. También se usa como apoyo para el insomnio, las fobias y el cambio de hábitos como dejar de fumar o controlar el peso, idealmente como parte de un plan más amplio. Funciona mejor en personas que se relajan con facilidad y que llegan con un objetivo claro."),
    ("¿Qué riesgos tiene la hipnosis?",
     "Guiada por un profesional formado, se considera segura. Las reacciones adversas son poco comunes y suelen ser leves: mareo, dolor de cabeza, náuseas, somnolencia o malestar emocional pasajero. No se recomienda en personas con enfermedades mentales graves sin supervisión de su médico tratante, y conviene ir con cuidado al trabajar recuerdos traumáticos. La hipnosis complementa, no reemplaza, el diagnóstico ni el tratamiento médico."),
    ("¿Cuál es la diferencia entre hipnosis clínica e hipnoterapia RTT?",
     "La hipnosis clínica es la herramienta general. RTT (Rapid Transformational Therapy) es un método específico creado por la terapeuta británica Marisa Peer que combina hipnosis con elementos de PNL, psicoterapia y terapia cognitivo-conductual para identificar la raíz de un bloqueo y transformarla, normalmente en una sesión principal más un audio personalizado."),
    ("¿La hipnosis funciona online?",
     "Sí. La sesión por videollamada sigue la misma estructura que la presencial: solo necesitas un lugar tranquilo, buena conexión y audífonos. Por eso es posible tomarla desde cualquier ciudad de Colombia, Latinoamérica o España."),
]

G1_BODY = f"""
<p class="lead-p">Si estás buscando <strong>hipnosis clínica en Bogotá</strong>, seguramente tienes las mismas preguntas que casi todo el mundo: qué es exactamente, si funciona, si tiene riesgos y cuánto cuesta. Esta guía las responde con claridad y con información verificable, para que decidas con calma.</p>

<nav class="toc" aria-label="Contenido de la guía"><span class="kicker">En esta guía</span><ol>
<li><a href="#que-es">Qué es la hipnosis clínica</a></li>
<li><a href="#para-que-sirve">Para qué sirve</a></li>
<li><a href="#efectividad">Qué tan efectiva es</a></li>
<li><a href="#riesgos">Qué riesgos tiene</a></li>
<li><a href="#rtt">Hipnosis clínica e hipnoterapia RTT</a></li>
<li><a href="#precio">Cuánto cuesta una sesión en Bogotá</a></li>
<li><a href="#elegir">Cómo elegir a tu hipnoterapeuta</a></li>
<li><a href="#sesion">Cómo es una sesión en Space to Rise</a></li>
</ol></nav>

<h2 id="que-es">¿Qué es la hipnosis clínica?</h2>
<p>La hipnosis clínica, también llamada hipnoterapia, es el uso de la hipnosis con un propósito terapéutico y guiado por un profesional formado. Con instrucciones verbales e imágenes mentales, la persona entra en un estado de <strong>relajación profunda y atención concentrada</strong>. En ese estado la mente es más receptiva a sugerencias que ayudan a cambiar una emoción, un hábito o una creencia.</p>
<p>No se parece a la hipnosis de espectáculo. <strong>No pierdes el control ni la conciencia</strong>: escuchas todo, puedes hablar, moverte o abrir los ojos cuando quieras, y por lo general recuerdas la sesión. La mayoría de las personas la describe como un estado de calma muy agradable, parecido al momento justo antes de dormirse.</p>

<h2 id="para-que-sirve">¿Para qué sirve la hipnosis clínica?</h2>
<p>Se usa como apoyo en temas emocionales, físicos y de hábitos. Entre los usos más frecuentes están:</p>
<ul>
<li><strong>Ansiedad y estrés</strong>, incluida la ansiedad antes de un procedimiento médico u odontológico.</li>
<li><strong>Miedos y fobias</strong>, como el miedo a volar o a hablar en público.</li>
<li><strong>Insomnio</strong> y problemas para conciliar el sueño.</li>
<li><strong>Manejo del dolor</strong>, por ejemplo en dolores de cabeza, colon irritable o fibromialgia.</li>
<li><strong>Cambio de hábitos</strong>: dejar de fumar o de vapear, controlar la ansiedad por la comida, dejar de procrastinar.</li>
<li><strong>Autoestima y creencias limitantes</strong> que frenan decisiones, relaciones o metas profesionales.</li>
</ul>

<h2 id="efectividad">¿Qué tan efectiva es?</h2>
<p>La respuesta honesta: depende del objetivo y de la persona. Según la Clínica Mayo, la evidencia es más sólida para ayudar a <strong>manejar el dolor, el estrés y la ansiedad</strong>. En cambios de hábito, como dejar de fumar o bajar de peso, funciona mejor como parte de un plan más amplio que como solución aislada.</p>
<p>Tres factores marcan la diferencia:</p>
<ul>
<li><strong>Tu disposición.</strong> Quien llega con un objetivo claro y ganas de cambiar suele obtener mejores resultados.</li>
<li><strong>La facilidad para relajarte.</strong> Cuanto más fácil te relajas durante la sesión, más probable es que la hipnosis te ayude.</li>
<li><strong>El seguimiento.</strong> Repetir las sugerencias en casa, por ejemplo con un audio, ayuda a que el cambio se mantenga.</li>
</ul>

<h2 id="riesgos">¿Qué riesgos tiene la hipnosis?</h2>
<p>Guiada por un profesional formado, la hipnosis se considera segura. Las reacciones adversas son poco comunes y, cuando aparecen, suelen ser leves y pasajeras: <strong>mareo, dolor de cabeza, náuseas, somnolencia o malestar emocional</strong>.</p>
<div class="callout"><p><strong>Cuándo tener cuidado.</strong> Si tienes un diagnóstico de enfermedad mental grave, consulta primero con tu médico tratante. Y si quieres trabajar recuerdos traumáticos, hazlo con un profesional con experiencia, porque pueden aparecer emociones intensas. La hipnosis <strong>complementa, no reemplaza</strong>, el diagnóstico ni el tratamiento médico o psicológico.</p></div>

<h2 id="rtt">Hipnosis clínica e hipnoterapia RTT: ¿en qué se diferencian?</h2>
<p>La hipnosis clínica es la herramienta general. La <strong>hipnoterapia RTT</strong> (Rapid Transformational Therapy) es un método específico creado por la terapeuta británica <strong>Marisa Peer</strong>. Combina hipnosis con elementos de programación neurolingüística (PNL), psicoterapia y terapia cognitivo-conductual.</p>
<p>Su enfoque es ir a la <strong>raíz</strong> de un bloqueo: durante la hipnosis se identifican las experiencias y creencias que lo originaron, se entienden desde la perspectiva adulta y se reemplazan por creencias nuevas. Normalmente se trabaja en <strong>una sesión principal</strong> (a veces hasta tres, según el tema) y se refuerza con un <strong>audio personalizado</strong> que escuchas durante 21 días. <a href="/rtt/">Conoce más sobre la hipnoterapia RTT</a>.</p>

<h2 id="precio">¿Cuánto cuesta una sesión de hipnosis en Bogotá?</h2>
<p>El precio cambia según el profesional, la duración de la sesión y lo que incluye. Como referencia, en directorios de salud de Bogotá las sesiones de hipnosis clínica se publican, a noviembre de 2026, aproximadamente <strong>entre $110.000 y $420.000 COP</strong>.</p>
<p>Al comparar precios, fíjate en qué incluye cada opción y no solo en la cifra:</p>
<ul>
<li><strong>Duración:</strong> ¿la sesión dura 50 minutos o varias horas?</li>
<li><strong>Número de sesiones:</strong> ¿cuántas se necesitan para tu objetivo?</li>
<li><strong>Seguimiento:</strong> ¿hay audio, material para casa o una conversación posterior?</li>
</ul>
<p>En Space to Rise, una <strong>sesión de hipnoterapia RTT cuesta $480.000</strong> e incluye una llamada inicial de 20 minutos, la sesión de aproximadamente 3 horas y tu audio personalizado de 21 días. La sesión de <a href="/kids/">RTT Kids</a> cuesta $380.000.</p>

<h2 id="elegir">Cómo elegir a tu hipnoterapeuta en Bogotá</h2>
<ul>
<li><strong>Formación verificable.</strong> Pregunta dónde se certificó y en qué método.</li>
<li><strong>Una conversación previa.</strong> Un buen profesional se toma el tiempo de entender tu caso antes de agendar.</li>
<li><strong>Expectativas realistas.</strong> Desconfía de quien promete curas garantizadas o resultados idénticos para todos.</li>
<li><strong>Trabajo complementario.</strong> Debe respetar tu tratamiento médico o psicológico, no pedirte que lo abandones.</li>
<li><strong>Que te sientas segura.</strong> La confianza es parte del proceso: si algo no te cuadra, sigue buscando.</li>
</ul>

<h2 id="sesion">Cómo es una sesión en Space to Rise</h2>
<p><a href="/sobre-mi/">Andrea Zafra</a> es hipnoterapeuta clínica certificada en RTT y atiende de forma presencial en Bogotá y online para Colombia, Latinoamérica y España. El proceso tiene tres pasos:</p>
<ol>
<li><strong>Llamada inicial (20 minutos).</strong> Hablamos de lo que quieres transformar y resolvemos tus dudas.</li>
<li><strong>Tu sesión de RTT (aprox. 3 horas).</strong> Con hipnosis vamos a la raíz del tema y trabajamos nuevas creencias.</li>
<li><strong>Tu audio de 21 días.</strong> Lo escuchas a diario para que tu mente integre el cambio.</li>
</ol>
<div class="inline-cta"><p>¿Quieres saber si la hipnoterapia es para ti?</p><a class="pill solid" href="/agenda/"><span>Agenda tu llamada inicial</span></a></div>

<h2 id="preguntas">Preguntas frecuentes</h2>
<div class="acc">{''.join(f'<div class="acc__item"><button class="acc__q">{q}<i></i></button><div class="acc__a"><div><div class="inner"><p>{a}</p></div></div></div></div>' for q, a in G1_FAQ)}</div>

<div class="sources"><span class="kicker">Fuentes</span><ul>
<li><a href="https://www.mayoclinic.org/es/tests-procedures/hypnosis/about/pac-20394405" target="_blank" rel="noopener">Clínica Mayo · Hipnosis: descripción general, usos y riesgos</a></li>
<li>Precios de referencia: tarifas publicadas por profesionales de hipnosis clínica en directorios de salud de Bogotá, consultadas el 5 de noviembre de 2026.</li>
</ul><p class="small muted">Esta guía es informativa y no sustituye la valoración de un profesional de la salud.</p></div>
"""

GUIAS.append(dict(
    slug="hipnosis-clinica-bogota",
    title="Hipnosis clínica en Bogotá: qué es, para qué sirve, riesgos y precios | Space to Rise",
    h1="Hipnosis clínica en Bogotá: qué es, para qué sirve y cuánto cuesta",
    desc="Guía 2026 de hipnosis clínica en Bogotá: qué es, para qué sirve, qué tan efectiva es, qué riesgos tiene, cuánto cuesta una sesión y en qué se diferencia de la hipnoterapia RTT.",
    card="Qué es, para qué sirve, qué tan efectiva es, qué riesgos tiene y cuánto cuesta una sesión de hipnosis clínica en Bogotá.",
    img="p/rtt-costa.jpg",
    date="2026-11-05", date_h="5 de noviembre de 2026", read="8 min de lectura",
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
      <a class="kicker fade" href="/guias/">Guías · Hipnosis clínica</a>
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
