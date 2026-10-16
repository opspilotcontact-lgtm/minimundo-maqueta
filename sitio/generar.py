"""Genera la tienda de Minimundo (v2) desde sitio/catalogo.json.

    python sitio/generar.py

Escribe en la raíz: index.html, tienda/, producto/<slug>/, carritos/, lista/,
css/tienda.css, js/tienda.js, js/catalogo.js e img/p/*.webp (desde fuente/productos).
La v1 vive en /v1/ y la propuesta en /propuesta/ (no se tocan aquí).
"""
import json, html, shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITIO = RAIZ / 'sitio'
FUENTE = RAIZ / 'fuente' / 'productos'
WA = 'https://wa.me/34624840524?text='
TEL = '624 84 05 24'

CATS = {
    'comer': 'La hora de comer', 'paseo': 'Triciclos y paseo', 'juego': 'Juego y puzles',
    'libros': 'Libros', 'manualidades': 'Manualidades', 'embarazo': 'Embarazo y regalo',
}
EDADES = [
    ('espera', 'Esperando', 'para la futura mamá'),
    ('0-1', '0–12 m', 'el primer año'),
    ('1-3', '1–3 años', 'aprende a hacerlo solo'),
    ('3-6', '3–6 años', 'juega, pinta, pregunta'),
    ('6+', '6+ años', 'ya lee solo'),
]
NOTAS = {  # palabras de Marta en su Instagram (oct-2026), recortadas, nunca inventadas
    'babate': ('Prácticas, bonitas y pensadas para acompañar a los peques mientras aprenden a comer solitos.', 'https://www.instagram.com/p/Degrsivo511/', '15 oct'),
    'olmitos': ('Estos modelos se suelen agotar para las fechas navideñas. Si tenéis pensado regalar uno, os recomiendo reservarlo con antelación.', 'https://www.instagram.com/p/DeeggVrCN7z/', '14 oct'),
    'educa': ('Piezas grandes, gruesas y súper resistentes, perfectas para sus manitas. Ver su cara de orgullo cuando encajan la última pieza… ¡no tiene precio!', 'https://www.instagram.com/p/DeM8V8OoxqV/', '6 oct'),
    'maletin': ('Perfectos para que los peques creen, jueguen y se entretengan allá donde estén.', 'https://www.instagram.com/p/DeHCYe2I2pp/', 'oct'),
    'rollo': ('Un plan creativo perfecto para una tarde tranquila, para regalar o para llevar de viaje.', 'https://www.instagram.com/p/DeBz9QyoYZ6/', 'oct'),
    'ladron': ('Una historia tierna y divertida sobre el otoño, los cambios y aprender a dejar ir.', 'https://www.instagram.com/p/DeOfLjOI1_Z/', '8 oct'),
    'diario': ('El regalo más especial para una futura mamá, o el capricho perfecto para acompañarte en este viaje.', 'https://www.instagram.com/p/Deb7MDiIddw/', '13 oct'),
    'halloween': ('Halloween también se lee: historias de brujas, monstruos y aventuras para todos los niveles, desde los primeros lectores.', 'https://www.instagram.com/p/DeM7IRXIjcr/', 'oct'),
}

def e(s):
    return html.escape(str(s), quote=True)

def eur(n):
    return '' if n is None else f'{n:,.2f} €'.replace(',', 'X').replace('.', ',').replace('X', '.')

ICONOS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="simbolo" viewBox="0 0 100 100"><clipPath id="si"><path d="M48 4a46 46 0 0 0 0 92z"/></clipPath><clipPath id="sd"><path d="M52 4a46 46 0 0 1 0 92z"/></clipPath><g clip-path="url(#si)"><path d="M48 4a46 46 0 0 0 0 92z" fill="#E3A3A6"/><path d="M30 100V79a7.5 7.5 0 0 1 15 0v21z" fill="#FBF6EE"/></g><g clip-path="url(#sd)"><path d="M52 4a46 46 0 0 1 0 92z" fill="#659DC0"/><path d="M55 100V79a7.5 7.5 0 0 1 15 0v21z" fill="#FBF6EE"/></g></symbol>
<symbol id="i-bolsa" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 8h14l-1 12H6z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/></symbol>
<symbol id="i-busca" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></symbol>
<symbol id="i-mas" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></symbol>
<symbol id="i-cierra" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></symbol>
<symbol id="i-ok" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></symbol>
<symbol id="i-wa" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.2A9.8 9.8 0 0 0 3.6 17l-1.3 4.8 4.9-1.3A9.8 9.8 0 1 0 12 2.2Zm0 17.9a8.1 8.1 0 0 1-4.1-1.1l-.3-.2-2.9.8.8-2.8-.2-.3A8.1 8.1 0 1 1 12 20.1Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></symbol>
<symbol id="i-mano" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10Z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-6.5-5.8-6.5-11a6.5 6.5 0 0 1 13 0c0 5.2-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/></symbol>
<symbol id="i-envio" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/></symbol>
<symbol id="i-regalo" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 10h16v10H4zM3 7h18v3H3zM12 7v13"/><path d="M12 7c-1.5-3-5-3-5-1s3 1 5 1c2 0 5 1 5-1s-3.5-2-5 1"/></symbol>
<symbol id="i-calma" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></symbol>
</svg>'''

AVISO = ('Propuesta de <a href="{r}propuesta/">OpsPilot</a> para Minimundo · catálogo de demostración con productos que Marta ya vende '
         '(precios de referencia) · servicios por confirmar · <a href="{r}v1/">ver v1</a>')


def cabeza(titulo, desc, r, extra='', actual=''):
    nav = [('tienda/', 'Tienda', 'tienda'), ('tienda/?edad=espera', 'Bebé en camino', ''), ('carritos/', 'Carritos con cita', 'carritos'),
           ('lista/', 'Lista de nacimiento', 'lista'), ('#club' if actual == 'inicio' else 'index.html#club', 'Club de lectura', '')]
    def enlaces(cls=''):
        out = []
        for href, txt, k in nav:
            h = href if href.startswith('#') else r + href
            cur = ' aria-current="page"' if k and k == actual else ''
            out.append(f'<a href="{h}"{cur}>{txt}</a>')
        return ''.join(out)
    return f'''<!doctype html>
<html lang="es" data-raiz="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#234A78">
<link rel="icon" href="{r}img/simbolo.svg" type="image/svg+xml">
<link rel="preload" href="{r}fonts/lexend-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS.replace("url(../fonts/", "url(" + r + "fonts/")}</style>
{extra}
</head>
<body>
{ICONOS}
<a class="sr" href="#contenido">Saltar al contenido</a>
<p class="aviso">{AVISO.format(r=r)}</p>
<a class="temporada" href="{r}producto/{RESERVA}/"><b>Reservas de Reyes abiertas.</b> Los triciclos Olmitos solo se consiguen reservados: <span>reservar el mío</span></a>
<header class="cab">
  <div class="wrap">
    <a class="marca" href="{r}" aria-label="Minimundo, inicio"><svg aria-hidden="true"><use href="#simbolo"/></svg><b>minimundo</b></a>
    <nav class="menu" aria-label="Principal">{enlaces()}</nav>
    <div class="herr">
      <a class="icono" href="{r}tienda/#busca" aria-label="Buscar en la tienda"><svg aria-hidden="true"><use href="#i-busca"/></svg></a>
      <a class="icono bolsa-btn" href="{r}tienda/" aria-label="Bolsa"><svg aria-hidden="true"><use href="#i-bolsa"/></svg><span class="cuenta" id="cuenta">0</span></a>
    </div>
  </div>
  <nav class="menu-movil" aria-label="Principal en móvil">{enlaces()}</nav>
</header>
<main id="contenido">
'''


def pie(r, catalogo_js=True):
    cats = ''.join(f'<li><a href="{r}tienda/?cat={k}">{v}</a></li>' for k, v in CATS.items())
    return f'''</main>
<footer class="pie">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="marca" href="{r}"><svg aria-hidden="true"><use href="#simbolo"/></svg><b>minimundo</b></a>
        <p style="margin-top:.8rem;max-width:30ch">Juguetes, libros y todo para tu bebé, elegido de uno en uno en La Carlota.</p>
      </div>
      <div><h2>Tienda</h2><ul>{cats}</ul></div>
      <div><h2>Te ayudamos</h2><ul><li><a href="{r}carritos/">Carritos con cita</a></li><li><a href="{r}lista/">Lista de nacimiento</a></li><li><a href="{r}#club">Club de lectura</a></li><li><a href="{WA}{e('Hola Marta, tengo una pregunta')}">Escríbenos por WhatsApp</a></li></ul></div>
      <div><h2>Visítanos</h2><ul><li>Av. de la Paz, 59</li><li>14100 La Carlota (Córdoba)</li><li><a href="tel:+34624840524">{TEL}</a></li><li><a href="https://www.instagram.com/minimundo_kid/">@minimundo_kid</a></li></ul></div>
    </div>
    <div class="legal"><span>© Minimundo · La Carlota</span><span>Propuesta de OpsPilot · no indexada · catálogo de demostración</span></div>
  </div>
</footer>
<div class="velo" aria-hidden="true"></div>
<aside class="cajon" id="cajon" aria-label="Tu bolsa" aria-hidden="true" inert>
  <header><h2>Tu bolsa</h2><button class="icono" id="cerrar-bolsa" type="button" aria-label="Cerrar la bolsa"><svg aria-hidden="true"><use href="#i-cierra"/></svg></button></header>
  <p class="vacia" id="bolsa-vacia">Aún no has elegido nada. Mira lo <a href="{r}tienda/">recién llegado</a>.</p>
  <ul class="items" id="bolsa-items"></ul>
  <footer id="bolsa-pie" hidden>
    <div class="total"><span>Total orientativo</span><b id="bolsa-total"></b></div>
    <div class="entrega" role="radiogroup" aria-label="Cómo lo quieres">
      <label><input type="radio" name="entrega" value="Lo recojo en la tienda" checked><span>Lo recojo</span></label>
      <label><input type="radio" name="entrega" value="Quiero que me lo enviéis"><span>Envío</span></label>
    </div>
    <button class="btn btn-wa" id="apartar" type="button"><svg aria-hidden="true"><use href="#i-wa"/></svg>Apartar por WhatsApp</button>
    <button class="btn btn-linea" id="hacer-lista" type="button"><svg aria-hidden="true"><use href="#i-regalo"/></svg>Convertir en lista de nacimiento</button>
    <p class="como">Marta te confirma por WhatsApp que lo tiene y te lo guarda. Pagas al recogerlo o te cuenta el envío.</p>
  </footer>
</aside>
{'<script src="' + r + 'js/catalogo.js" defer></script>' if catalogo_js else ''}
<script src="{r}js/tienda.js" defer></script>
</body>
</html>
'''


def tarjeta(p, r, i=0, lazy=True):
    sello = ''
    if p.get('sello'):
        sello = f'<span class="sello{" reserva" if p["sello"].startswith("Solo") else ""}">{e(p["sello"])}</span>'
    nota = NOTAS.get(p.get('nota', ''), ('',))[0]
    texto = ' '.join([p['nombre'], p['marca'], CATS[p['cat']], p.get('desc', '')]).lower()
    import unicodedata
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    precio = f'<span class="precio">{eur(p["pvp"])}</span>' if p.get('pvp') is not None else '<span class="precio sin">Precio en tienda</span>'
    return f'''<li class="prod c-{p['cat']} sube" data-c="{p['cat']}" data-e="{' '.join(p['etapas'])}" data-p="{p.get('pvp') or ''}" data-i="{i}" data-t="{e(texto)}">
  <a class="foto" href="{r}producto/{p['slug']}/" tabindex="-1" aria-hidden="true">{sello}<img src="{r}img/p/{p['slug']}.webp" alt="" width="480" height="600"{' loading="lazy"' if lazy else ''}></a>
  <p class="marca-p">{e(p['marca'])}</p>
  <h3><a href="{r}producto/{p['slug']}/">{e(p['nombre'])}</a></h3>
  {f'<p class="nota-mini">{e(nota)}</p>' if nota and p.get('nota_en_tarjeta') else ''}
  <div class="pie-p">{precio}<button class="anadir" type="button" data-add="{p['slug']}" aria-label="Añadir {e(p['nombre'])} a la bolsa"><svg aria-hidden="true"><use href="#i-mas"/></svg></button></div>
</li>'''


def mundo(lunas, r):
    l = ''.join(f'<div class="luna" style="--a:{int(i*360/len(lunas))}deg"><a href="{r}producto/{p["slug"]}/" tabindex="-1"><img src="{r}img/p/{p["slug"]}.webp" alt="" width="200" height="250" fetchpriority="low" decoding="async"></a></div>' for i, p in enumerate(lunas))
    estrellas = ''.join(f'<path d="M{x} {y-6}l1.6 4.4 4.4 1.6-4.4 1.6L{x} {y+6}l-1.6-4.4-4.4-1.6 4.4-1.6z" fill="#FBF6EE" opacity="{o}"/>' for x, y, o in [(70, 90, .8), (520, 70, .6), (548, 330, .5), (60, 410, .6), (470, 540, .7), (130, 560, .4), (300, 30, .5)])
    return f'''<div class="mundo" aria-hidden="true">
  <svg viewBox="0 0 600 600">
    <circle cx="300" cy="300" r="240" fill="none" stroke="#FBF6EE" stroke-opacity=".22" stroke-dasharray="2 9" stroke-linecap="round" stroke-width="2"/>
    {estrellas}
    <g transform="rotate(38 300 300)"><g class="paseante">
      <g transform="translate(300 152) scale(1.35)" fill="#1F2340">
        <circle cx="-9" cy="-31" r="4.6"/>
        <path d="M-14 -25h9.5l2 13.5h-3.4L-7 0h-3.6l-.6-11.5h-3.6z"/>
        <path d="M-5 -21l10 3" stroke="#1F2340" stroke-width="2.4" stroke-linecap="round"/>
        <path d="M5 -18l4 7" stroke="#1F2340" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M7 -12h19a9.5 9.5 0 0 1-19 0z" fill="#E3A3A6"/>
        <path d="M14 -12a9 9 0 0 1 12 -9v9z" fill="#F6DCDA"/>
        <circle cx="11" cy="-1.6" r="2.6"/><circle cx="23" cy="-1.6" r="2.6"/>
      </g>
    </g></g>
    <path d="M296 150a150 150 0 0 0 0 300z" fill="#E3A3A6"/>
    <path d="M304 150a150 150 0 0 1 0 300z" fill="#659DC0"/>
    <clipPath id="mi"><path d="M296 150a150 150 0 0 0 0 300z"/></clipPath>
    <clipPath id="md"><path d="M304 150a150 150 0 0 1 0 300z"/></clipPath>
    <path d="M200 236c22-8 46-4 60 6M340 250c26-12 54-10 72 2M210 330c18 6 34 6 50 0M352 340c20-6 40-4 56 4" stroke="#1F2340" stroke-opacity=".12" stroke-width="3" stroke-linecap="round" fill="none"/>
    <g>
      <rect x="258" y="104" width="84" height="54" rx="3" fill="#FBF6EE"/>
      <path d="M254 104h92v10c-4.6 6-9.2 6-13.8 0-4.6 6-9.2 6-13.8 0-4.6 6-9.2 6-13.8 0-4.6 6-9.2 6-13.8 0-4.6 6-9.2 6-13.8 0-4.6 6-9.2 6-13.8 0-4.6 6-9.2 6-9 0z" fill="#9E4F57"/>
      <path d="M266 158v-20a8 8 0 0 1 16 0v20zM318 158v-20a8 8 0 0 1 16 0v20z" fill="#659DC0"/>
      <path d="M292 158v-22a8 8 0 0 1 16 0v22z" fill="#234A78"/>
      <path d="M248 98h104v6H248z" fill="#1F2340"/>
      <path d="M232 160c10-14 20-30 18-44-10 6-20 22-18 44z M232 160c-2-16 4-34 12-40" fill="#7FA36B"/>
    </g>
  </svg>
  <div class="orbita">{l}</div>
</div>'''


def acera():
    return '''<svg class="acera" viewBox="0 0 520 220" role="img" aria-label="Una madre empuja un carrito por la acera">
  <path d="M0 196h520" stroke="currentColor" stroke-width="3"/>
  <path d="M0 206h520" stroke="currentColor" stroke-opacity=".25" stroke-width="2" stroke-dasharray="40 14"/>
  <g class="empuja">
    <g fill="#1F2340"><circle cx="182" cy="58" r="13"/><path d="M168 76h26l6 52h-9l-4 66h-9l-3-60-3 60h-9l-3-66h-9z"/></g>
    <path d="M194 92l40 10M234 102l18 30" stroke="#1F2340" stroke-width="6" stroke-linecap="round" fill="none"/>
    <path d="M244 128h96a48 48 0 0 1-96 0z" fill="#E3A3A6"/>
    <path d="M278 128a46 46 0 0 1 62-44v44z" fill="#F6DCDA"/>
    <path d="M262 168l-8 20M320 168l10 20" stroke="#1F2340" stroke-width="5" stroke-linecap="round"/>
    <g class="rueda"><circle cx="254" cy="186" r="11" fill="none" stroke="#1F2340" stroke-width="5"/><path d="M254 175v22M243 186h22" stroke="#1F2340" stroke-width="2"/></g>
    <g class="rueda"><circle cx="330" cy="186" r="11" fill="none" stroke="#1F2340" stroke-width="5"/><path d="M330 175v22M319 186h22" stroke="#1F2340" stroke-width="2"/></g>
  </g>
  <path d="M420 196v-26h40v26" fill="none" stroke="currentColor" stroke-width="3"/>
  <path d="M410 170h60" stroke="currentColor" stroke-width="3"/>
</svg>'''


def hoja():
    def grupo(n, nombre, titulo, ops):
        o = ''.join(f'<label><input type="radio" name="{nombre}" value="{e(v)}"><span>{e(t)}</span></label>' for v, t in ops)
        return f'<fieldset><legend><span class="n">{n}</span>{titulo}</legend><div class="ops">{o}</div></fieldset>'
    return f'''<form class="hoja" id="hoja-carrito" aria-labelledby="t-hoja">
  <h2 id="t-hoja">Tu hoja de carrito</h2>
  <p class="intro">Cuatro preguntas, un minuto. Llegas a la cita con lo importante ya pensado.</p>
  {grupo(1, 'cuando', '¿Para cuándo?', [('Ya ha nacido', 'Ya ha nacido'), ('Faltan 1 a 3 meses', 'Faltan 1 a 3 meses'), ('Faltan más de 3 meses', 'Más de 3 meses')])}
  {grupo(2, 'paseo', '¿Por dónde vais a pasear más?', [('Aceras del pueblo', 'Aceras del pueblo'), ('Caminos y campo', 'Caminos y campo'), ('Ciudad, autobús y tiendas', 'Ciudad y autobús')])}
  {grupo(3, 'coche', '¿Qué coche tenéis?', [('Pequeño', 'Pequeño'), ('Mediano o familiar', 'Mediano o familiar'), ('Monovolumen o SUV', 'Monovolumen o SUV'), ('Sin coche', 'Sin coche')])}
  {grupo(4, 'busca', '¿Qué buscas?', [('Carrito completo con capazo', 'Carrito con capazo'), ('Silla de coche', 'Silla de coche'), ('Silla ligera de paseo', 'Silla ligera'), ('Aún no lo sé', 'Aún no lo sé')])}
  <div class="resultado" aria-live="polite">
    <h3>Lo que miraremos juntas</h3>
    <p class="vacio" id="vacio">Marca tus respuestas y aquí aparece tu hoja.</p>
    <ul id="miramos" hidden></ul>
    <a class="btn btn-wa" id="pedir" href="{WA}{e('Hola Marta, quiero cita para probar carritos.')}" target="_blank" rel="noopener" hidden><svg aria-hidden="true"><use href="#i-wa"/></svg>Pedir cita por WhatsApp</a>
  </div>
  <noscript><p>Escríbenos al <a href="https://wa.me/34624840524">WhatsApp {TEL}</a> y lo vemos juntas.</p></noscript>
</form>'''


def etiqueta(clave):
    if clave not in NOTAS:
        return ''
    t, url, f = NOTAS[clave]
    return f'<blockquote class="etiqueta"><q>{e(t)}</q><cite>Marta, en <a href="{url}">su Instagram</a> · {f}</cite></blockquote>'


def inicio(P, por):
    r = ''
    nuevos = [p for p in P if p.get('portada')][:8] or P[:8]
    lunas = [p for p in P if p.get('luna')][:6]
    res = por[RESERVA]
    tarjetas = '\n'.join(tarjeta(p, r, i) for i, p in enumerate(nuevos))
    edades = ''.join(f'<li><a href="tienda/?edad={k}"><b>{t}</b><span>{s}</span></a></li>' for k, t, s in EDADES)
    ticket = ''.join(f'<li><span>{e(p["nombre"])}</span>{"<span class=de>Regalado</span>" if i % 2 == 0 else "<s>" + eur(p["pvp"]) + "</s>" if p.get("pvp") else ""}</li>' for i, p in enumerate([q for q in P if 'espera' in q['etapas'] or '0-1' in q['etapas']][:4]))
    lomos = ''.join(f'<i style="--h:{h}%;--c:{c}"></i>' for h, c in [(70, '#E3A3A6'), (88, '#659DC0'), (62, '#FBF6EE'), (96, '#9E4F57'), (78, '#F6DCDA'), (55, '#DDEBF4'), (84, '#E3A3A6'), (68, '#659DC0'), (92, '#FBF6EE'), (74, '#9E4F57')])
    schema = {
        '@context': 'https://schema.org', '@type': 'Store', 'name': 'Minimundo',
        'description': 'Juguetería educativa, librería infantil y artículos de bebé en La Carlota (Córdoba).',
        'telephone': '+34624840524', 'image': 'img/fachada.webp',
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Av. de la Paz, 59', 'postalCode': '14100', 'addressLocality': 'La Carlota', 'addressRegion': 'Córdoba', 'addressCountry': 'ES'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': 37.6688974, 'longitude': -4.9333163},
        'sameAs': ['https://www.instagram.com/minimundo_kid/'],
    }
    extra = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script>'
    return cabeza('Minimundo · Juguetes, libros y bebé en La Carlota', 'Juguetes educativos, libros infantiles y todo para tu bebé, elegido de uno en uno en La Carlota (Córdoba). Apártalo por WhatsApp y recógelo en la Av. de la Paz, 59.', r, extra, 'inicio') + f'''
<section class="portada" aria-labelledby="t-portada">
  <div class="wrap">
    <div>
      <h1 id="t-portada">Elegido de uno en uno.</h1>
      <p class="bajada">Juguetes, libros y lo que necesita tu bebé, escogido por Marta en La Carlota. Lo apartas por WhatsApp y lo recoges en la Avenida de la Paz.</p>
      <div class="acciones">
        <a class="btn btn-cal" href="tienda/">Ver la tienda</a>
        <a class="btn btn-linea" href="carritos/">Probar carritos con cita</a>
      </div>
      <ul class="garantias">
        <li><svg aria-hidden="true"><use href="#i-mano"/></svg>Lo elige una madre</li>
        <li><svg aria-hidden="true"><use href="#i-wa"/></svg>Apartado por WhatsApp</li>
        <li><svg aria-hidden="true"><use href="#i-envio"/></svg>Envíos: pregúntanos</li>
        <li><svg aria-hidden="true"><use href="#i-calma"/></svg>Te atendemos sin prisa</li>
      </ul>
    </div>
    {mundo(lunas, r)}
  </div>
</section>

<section class="bloque" aria-labelledby="t-nuevo">
  <div class="wrap">
    <div class="cabeza"><h2 id="t-nuevo">Recién llegado a la tienda</h2><a class="ver-todo" href="tienda/">Ver todo lo elegido</a></div>
    <ul class="rejilla">
{tarjetas}
    </ul>
  </div>
</section>

<section class="bloque reservas" id="reservas" aria-labelledby="t-reservas">
  <div class="wrap">
    <a class="escaparate c-paseo" href="producto/{res['slug']}/" aria-label="{e(res['nombre'])}"><img src="img/p/{res['slug']}.webp" alt="" width="480" height="600" loading="lazy"></a>
    <div class="txt">
      <h2 id="t-reservas">El triciclo de Reyes se reserva ahora.</h2>
      <p>Los triciclos evolutivos de Olmitos crecen con tu peque: empiezan con barra para empujar y acaban siendo suyos del todo. Y cada año, en diciembre, se acaban.</p>
      <div class="cuenta-atras"><b id="dias-reyes">82</b><span>días para el 6 de enero</span></div>
      {etiqueta('olmitos')}
      <div class="acciones" style="display:flex;flex-wrap:wrap;gap:.6rem">
        <button class="btn btn-anil" type="button" data-add="{res['slug']}">Añadir a mi bolsa</button>
        <a class="btn btn-wa" target="_blank" rel="noopener" href="{WA}{e('Hola Marta, quiero reservar un triciclo Olmitos para Reyes.')}"><svg aria-hidden="true"><use href="#i-wa"/></svg>Reservar por WhatsApp</a>
      </div>
    </div>
  </div>
</section>

<section class="bloque" aria-labelledby="t-edad">
  <div class="wrap">
    <div class="cabeza"><h2 id="t-edad">¿Cuántos años tiene tu peque?</h2><p>Empieza por su edad y te enseñamos solo lo que le va a servir ahora.</p></div>
    <ul class="edades">{edades}</ul>
  </div>
</section>

<section class="bloque carritos" aria-labelledby="t-carritos">
  <div class="wrap">
    <div class="txt">
      <h2 id="t-carritos">Un carrito no se elige en una foto. Se empuja.</h2>
      <p>Por eso los carritos no están en la tienda online: se prueban aquí, con cita y sin prisa. Lo pliegas, lo subes al bordillo, medimos tu maletero y decides en casa, tranquila.</p>
      <ol class="pasos">
        <li><span><b>Haz tu hoja de carrito</b>Cuatro preguntas, un minuto.</span></li>
        <li><span><b>Te damos cita por WhatsApp</b>A la hora que te venga bien.</span></li>
        <li><span><b>Lo pruebas en la acera</b>Con tu coche, tu bebé o tu barriga.</span></li>
      </ol>
      <a class="btn btn-anil" href="carritos/">Hacer mi hoja de carrito</a>
    </div>
    {acera()}
  </div>
</section>

<section class="bloque marta" aria-labelledby="t-marta">
  <div class="wrap">
    <figure style="margin:0">
      <div class="arco"><img src="img/estanteria-montessori-sm.webp" srcset="img/estanteria-montessori-sm.webp 520w, img/estanteria-montessori.webp 900w" sizes="(max-width:900px) 90vw, 36vw" width="520" height="520" alt="Estantería de cubos con juguetes de madera sobre la pared azul de Minimundo" loading="lazy"></div>
      <figcaption>Foto de su ficha de Google, provisional hasta la sesión de fotos.</figcaption>
    </figure>
    <div>
      <h2 id="t-marta" class="sr">Quién elige</h2>
      <blockquote>«Los libros no siempre se leen sentados y en silencio. A veces se escuchan, se tocan, se descubren… y hasta se bailan. Porque el amor por los libros empieza mucho antes de aprender a leer.»</blockquote>
      <p class="firma">Marta, mamá de Daniela y Andrea<span>Elige todo lo que hay en Minimundo · en <a href="https://www.instagram.com/p/DeOhdLzoLdH/">su Instagram</a>, 8 oct</span></p>
    </div>
  </div>
</section>

<section class="bloque lista-n" aria-labelledby="t-lista">
  <div class="wrap">
    <div>
      <h2 id="t-lista">Que te regalen lo que de verdad vas a usar.</h2>
      <p>Llena tu bolsa con lo que te gusta y conviértela en tu lista de nacimiento. La compartes por WhatsApp, cada uno elige qué regalar y Marta lo aparta para que nada se repita.</p>
      <div style="margin-top:1.6rem"><a class="btn btn-anil" href="tienda/?edad=espera">Empezar mi lista</a></div>
    </div>
    <div class="ticket" aria-label="Ejemplo de lista de nacimiento">
      <h3>Lista de nacimiento · ejemplo</h3>
      <ul>{ticket}</ul>
    </div>
  </div>
</section>

<section class="bloque club" id="club" aria-labelledby="t-club">
  <div class="wrap">
    <div>
      <div class="lomos" aria-hidden="true">{lomos}</div>
      <h2 id="t-club">Un ratito para nosotras.</h2>
    </div>
    <div>
      <p>El club de lectura de Minimundo, para mujeres y madres: un libro al mes y una tarde al mes en la librería, para hablar de la historia, de lo que nos ha removido y de todo lo que surja.</p>
      <ul class="reglas"><li>No hace falta ser una gran lectora.</li><li>No hace falta tener tiempo de sobra.</li><li>Solo ganas de leer, compartir y dedicarte un rato.</li></ul>
      <a class="btn btn-rosa" target="_blank" rel="noopener" href="{WA}CLUB">Escribir «CLUB» por WhatsApp</a>
    </div>
  </div>
</section>

<section class="bloque visita" id="visita" aria-labelledby="t-visita">
  <div class="wrap">
    <figure style="margin:0"><img src="img/fachada.webp" width="900" height="600" alt="Fachada rosa de Minimundo en la Avenida de la Paz" loading="lazy"><figcaption>Street View, provisional.</figcaption></figure>
    <div>
      <h2 id="t-visita">Ven a verlo con tus manos.</h2>
      <dl>
        <dt>Dónde</dt><dd>Av. de la Paz, 59 · La Carlota, junto a Tropicalia</dd>
        <dt>Horario</dt><dd>10:00–13:30 y desde las 17:30</dd>
        <dt>Teléfono</dt><dd><a href="tel:+34624840524">{TEL}</a></dd>
      </dl>
      <div style="display:flex;flex-wrap:wrap;gap:.6rem">
        <a class="btn btn-anil" href="https://www.google.com/maps/search/?api=1&amp;query=Minimundo%20Av.%20de%20la%20Paz%2059%20La%20Carlota">Cómo llegar</a>
        <a class="btn btn-linea" href="tel:+34624840524">Llamar</a>
      </div>
    </div>
  </div>
</section>
''' + pie(r)


def tienda(P):
    r = '../'
    chips_c = '<button type="button" data-cat="todo" aria-pressed="true">Todo</button>' + ''.join(f'<button type="button" data-cat="{k}" aria-pressed="false">{v}</button>' for k, v in CATS.items() if any(p['cat'] == k for p in P))
    chips_e = '<button type="button" data-edad="todo" aria-pressed="true">Cualquier edad</button>' + ''.join(f'<button type="button" data-edad="{k}" aria-pressed="false">{t}</button>' for k, t, s in EDADES)
    tarjetas = '\n'.join(tarjeta(dict(p, nota_en_tarjeta=True), r, i, lazy=i > 3) for i, p in enumerate(P))
    return cabeza('La tienda · Minimundo, La Carlota', 'Juguetes educativos, libros infantiles, vajilla, triciclos y regalos para futuras mamás, elegidos por Marta en La Carlota.', r, actual='tienda') + f'''
<div class="wrap tit-pag">
  <h1>La tienda</h1>
  <p>Todo lo que hay aquí lo ha elegido Marta, de uno en uno. Añádelo a tu bolsa y apártalo por WhatsApp: te lo guarda en la tienda.</p>
</div>
<div class="filtros">
  <div class="wrap">
    <div class="chips" role="group" aria-label="Sección">{chips_c}</div>
    <div class="chips" role="group" aria-label="Edad">{chips_e}</div>
    <div class="busca-fila">
      <label class="sr" for="busca">Buscar</label><input id="busca" type="search" placeholder="Busca: puzle, babero, otoño…">
      <label class="sr" for="orden">Ordenar</label><select id="orden"><option value="nuevo">Lo último</option><option value="barato">Precio: menor</option><option value="caro">Precio: mayor</option></select>
    </div>
  </div>
</div>
<div class="wrap" style="padding-bottom:4rem">
  <h2 class="sr">Productos</h2>
  <p class="cuantos" id="cuantos" aria-live="polite"></p>
  <ul class="rejilla" id="catalogo">
{tarjetas}
  </ul>
  <p id="nada" hidden>No hay nada con ese filtro. Escríbele a Marta: <a href="{WA}{e('Hola Marta, estoy buscando ')}">«Estoy buscando…»</a></p>
</div>
''' + pie(r)


def producto(p, P):
    r = '../../'
    rel = [q for q in P if q['cat'] == p['cat'] and q['slug'] != p['slug']][:4]
    if len(rel) < 4:
        rel += [q for q in P if q not in rel and q['slug'] != p['slug']][:4 - len(rel)]
    datos = f'<dt>Marca</dt><dd>{e(p["marca"])}</dd>' + (f'<dt>Edad</dt><dd>{e(p["edad"])}</dd>' if p.get('edad') else '')
    if p.get('datos'):
        datos += '<dt>Detalles</dt><dd><ul style="margin:0;padding-left:1.1rem">' + ''.join(f'<li>{e(d)}</li>' for d in p['datos']) + '</ul></dd>'
    precio = eur(p['pvp']) if p.get('pvp') is not None else 'Precio en tienda'
    pregunta = f'Hola Marta, ¿tienes «{p["nombre"]}»?'
    offer = {'@type': 'Offer', 'priceCurrency': 'EUR', 'price': p['pvp'], 'availability': 'https://schema.org/InStoreOnly'} if p.get('pvp') is not None else None
    schema = {'@context': 'https://schema.org', '@type': 'Product', 'name': p['nombre'], 'brand': {'@type': 'Brand', 'name': p['marca']}, 'image': f'img/p/{p["slug"]}.webp', 'description': p.get('desc', '')}
    if offer:
        schema['offers'] = offer
    extra = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script>'
    reserva = p['slug'] == RESERVA
    return cabeza(f'{p["nombre"]} · Minimundo', f'{p["nombre"]} de {p["marca"]} en Minimundo, La Carlota. {p.get("desc", "")}'[:155], r, extra) + f'''
<div class="wrap">
  <nav class="miga" aria-label="Estás en"><a href="{r}">Inicio</a> / <a href="{r}tienda/">Tienda</a> / <a href="{r}tienda/?cat={p['cat']}">{CATS[p['cat']]}</a></nav>
  <div class="ficha c-{p['cat']}">
    <div class="foto"><img src="{r}img/p/{p['slug']}.webp" alt="{e(p['nombre'])}" width="480" height="600"></div>
    <div>
      <p class="marca-p">{e(p['marca'])}</p>
      <h1>{e(p['nombre'])}</h1>
      <span class="precio">{precio}</span>
      {'<span class="orient">PVP de referencia · Marta te confirma el suyo</span>' if p.get('pvp') is not None and not p.get('precio_suyo') else ''}
      <p class="desc">{e(p.get('desc', ''))}</p>
      <div class="comprar">
        <button class="btn btn-anil" type="button" data-add="{p['slug']}"><svg aria-hidden="true"><use href="#i-bolsa"/></svg>{'Reservar para Reyes' if reserva else 'Añadir a la bolsa'}</button>
        <a class="btn btn-linea" target="_blank" rel="noopener" href="{WA}{e(pregunta)}"><svg aria-hidden="true"><use href="#i-wa"/></svg>Preguntar a Marta</a>
      </div>
      {etiqueta(p.get('nota', ''))}
      <ul class="servicio">
        <li><svg aria-hidden="true"><use href="#i-pin"/></svg><span><b>Apártalo y recógelo</b> en Av. de la Paz, 59 (La Carlota).</span></li>
        <li><svg aria-hidden="true"><use href="#i-envio"/></svg><span><b>¿Te lo enviamos?</b> Escríbenos y te contamos cómo.</span></li>
        <li><svg aria-hidden="true"><use href="#i-regalo"/></svg><span><b>¿Es para un bebé que viene?</b> Añádelo a una <a href="{r}lista/">lista de nacimiento</a>.</span></li>
      </ul>
      <dl class="datos">{datos}</dl>
      <p class="origen">Foto y precio de referencia: <a href="{e(p.get('fuente_url', '#'))}">{e(p.get('fuente', 'fabricante'))}</a>. Catálogo de demostración hasta cargar el de Minimundo.</p>
    </div>
  </div>
  <section class="bloque" style="padding-top:0" aria-labelledby="t-rel">
    <div class="cabeza"><h2 id="t-rel" style="font-size:clamp(1.5rem,3vw,2rem)">También lo ha elegido Marta</h2></div>
    <ul class="rejilla">{''.join(tarjeta(q, r) for q in rel)}</ul>
  </section>
</div>
''' + pie(r)


def carritos():
    r = '../'
    return cabeza('Carritos con cita · Minimundo, La Carlota', 'Prueba tu carrito antes de comprarlo: cita en Minimundo (La Carlota), sin prisa, con tu coche y tu bebé. Haz tu hoja de carrito y pide cita por WhatsApp.', r, actual='carritos') + f'''
<section class="bloque carritos" style="padding-top:2.4rem" aria-labelledby="t-c">
  <div class="wrap">
    <div class="txt">
      <h1 id="t-c" style="font-size:clamp(2.3rem,5.6vw,4rem);letter-spacing:-.04em">Prueba tu carrito antes de comprarlo.</h1>
      <p>Es lo primero que compras para tu bebé y lo que más dudas da. Aquí no se elige en una foto: se pliega, se empuja por la acera y se mete en tu maletero. Con cita, para que nadie te meta prisa.</p>
      <ol class="pasos">
        <li><span><b>Rellena tu hoja</b>Cuatro preguntas sobre cómo vais a vivir.</span></li>
        <li><span><b>Pide cita por WhatsApp</b>Marta te propone hora.</span></li>
        <li><span><b>Pruébalo con calma</b>Ven con tu coche, tu bebé o tu barriga.</span></li>
        <li><span><b>Decide en casa</b>Sin compromiso. Si lo quieres, te lo pedimos.</span></li>
      </ol>
      {acera()}
    </div>
    {hoja()}
  </div>
</section>
''' + pie(r)


def lista():
    r = '../'
    return cabeza('Lista de nacimiento · Minimundo, La Carlota', 'Haz tu lista de nacimiento en Minimundo (La Carlota): elige, compártela por WhatsApp y Marta aparta cada regalo para que nada se repita.', r, actual='lista') + f'''
<div class="wrap tit-pag">
  <h1 id="lista-tit">Lista de nacimiento</h1>
  <p>Elige en la tienda lo que de verdad vas a usar, conviértelo en lista desde tu bolsa y compártela. Cada familiar pulsa «Lo regalo yo» y Marta lo aparta, así nada se repite.</p>
  <div class="busca-fila" style="margin-top:1.4rem;max-width:34rem">
    <label class="sr" for="lista-nombre">Nombre de la lista</label><input id="lista-nombre" placeholder="Nombre del bebé o de la familia">
    <button class="btn btn-wa" id="compartir" type="button"><svg aria-hidden="true"><use href="#i-wa"/></svg>Compartir</button>
  </div>
</div>
<div class="wrap" style="padding-bottom:4rem">
  <p id="lista-vacia" hidden>Tu lista aún está vacía. Empieza en la <a href="{r}tienda/?edad=espera">tienda</a>: añade lo que te guste a la bolsa y pulsa «Convertir en lista de nacimiento».</p>
  <h2 class="sr">Regalos de la lista</h2>
  <ul class="rejilla" id="lista-items"></ul>
</div>
''' + pie(r)


def imagenes(P):
    from PIL import Image
    out = RAIZ / 'img' / 'p'
    out.mkdir(parents=True, exist_ok=True)
    for p in P:
        src = FUENTE / p['imagen']
        dst = out / f'{p["slug"]}.webp'
        if dst.exists() and dst.stat().st_mtime > src.stat().st_mtime:
            continue
        im = Image.open(src)
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA')
            fondo = Image.new('RGB', im.size, (255, 255, 255))
            fondo.paste(im, mask=im.split()[-1])
            im = fondo
        im = im.convert('RGB')
        im.thumbnail((560, 700), Image.LANCZOS)
        lienzo = Image.new('RGB', (480, 600), (255, 255, 255))
        im.thumbnail((480, 600), Image.LANCZOS)
        lienzo.paste(im, ((480 - im.width) // 2, (600 - im.height) // 2))
        lienzo.save(dst, 'WEBP', quality=80, method=6)


def escribe(ruta, txt):
    f = RAIZ / ruta
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(txt, encoding='utf-8', newline='\n')


def main():
    global RESERVA
    P = json.loads((SITIO / 'catalogo.json').read_text(encoding='utf-8'))
    por = {p['slug']: p for p in P}
    RESERVA = next(p['slug'] for p in P if p.get('reserva'))
    imagenes(P)
    (RAIZ / 'css').mkdir(exist_ok=True); (RAIZ / 'js').mkdir(exist_ok=True)
    shutil.copy(SITIO / 'tienda.css', RAIZ / 'css' / 'tienda.css')
    shutil.copy(SITIO / 'tienda.js', RAIZ / 'js' / 'tienda.js')
    cat = {p['slug']: {'nombre': p['nombre'], 'marca': p['marca'], 'cat': p['cat'], 'pvp': p.get('pvp'), 'img': f'img/p/{p["slug"]}.webp'} for p in P}
    escribe('js/catalogo.js', 'window.CATALOGO=' + json.dumps(cat, ensure_ascii=False, separators=(',', ':')) + ';\n')
    escribe('index.html', inicio(P, por))
    escribe('tienda/index.html', tienda(P))
    escribe('carritos/index.html', carritos())
    escribe('lista/index.html', lista())
    for p in P:
        escribe(f'producto/{p["slug"]}/index.html', producto(p, P))
    print(f'{len(P)} productos · {len(P) + 4} páginas')


RESERVA = ''
CSS = (SITIO / 'tienda.css').read_text(encoding='utf-8')
if __name__ == '__main__':
    main()
