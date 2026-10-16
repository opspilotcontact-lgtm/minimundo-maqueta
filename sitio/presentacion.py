"""Imagen de presentación para los dueños (y vista previa del enlace en WhatsApp).

    python sitio/presentacion.py   → _presentacion.html (se captura a img/presentacion.png/.jpg)
"""
import json
import generar as g

P = json.loads((g.SITIO / 'catalogo.json').read_text(encoding='utf-8'))
lunas = [p for p in P if p.get('luna')][:6]

COLORES = [('#E3A3A6', 'Rosa fachada'), ('#659DC0', 'Azul pared'), ('#234A78', 'Añil'), ('#1F2340', 'Tinta'), ('#FBF6EE', 'Cal')]
muestras = ''.join(f'<li><i style="background:{c}"></i><b>{n}</b><span>{c}</span></li>' for c, n in COLORES)

html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Minimundo · presentación</title>
<style>
@font-face{{font-family:'Lexend';font-weight:300 800;src:url(fonts/lexend-var-latin.woff2) format('woff2')}}
*{{box-sizing:border-box;margin:0}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{background:#234A78;color:#FBF6EE;font:300 16px/1.4 'Lexend',sans-serif;position:relative}}
.lienzo{{position:absolute;inset:0;display:grid;grid-template-columns:600px 1fr;padding:56px 0 52px 64px}}
.marca{{display:flex;align-items:center;gap:14px}}
.marca svg{{width:58px;height:58px}}
.marca b{{font-weight:600;font-size:44px;letter-spacing:-.035em}}
.pre{{margin-top:44px;font-size:21px;color:#F6DCDA;font-weight:400}}
h1{{font-weight:650;font-size:78px;line-height:.98;letter-spacing:-.045em;margin-top:10px}}
.sub{{margin-top:18px;font-size:20px;color:#D5DEEA;max-width:36ch}}
ul{{list-style:none;padding:0;display:flex;gap:18px;margin-top:34px}}
li{{display:grid;grid-template-columns:30px auto;column-gap:9px;align-items:center}}
li i{{grid-row:span 2;width:30px;height:30px;border-radius:50%;box-shadow:0 0 0 2px rgb(251 246 238/.6)}}
li b{{font-size:13px;font-weight:500;line-height:1.1}}
li span{{font-size:11px;color:#B9C6D8;letter-spacing:.02em}}
.url{{position:absolute;left:64px;bottom:34px;font-size:15px;color:#D5DEEA}}
.url b{{color:#FBF6EE;font-weight:500}}
.arte{{position:relative;width:540px;height:540px;align-self:center;margin:-20px 0 0 -6px}}
.mundo{{position:absolute;inset:0;width:100%;height:100%}}
.mundo>svg{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
.orbita{{position:absolute;inset:0}}
.luna{{position:absolute;left:50%;top:50%;width:17%;aspect-ratio:1;margin:-8.5% 0 0 -8.5%;transform:rotate(var(--a)) translateX(235%) rotate(calc(-1*var(--a)))}}
.luna a{{display:block;width:100%;height:100%;border-radius:50%;background:#FFFDF9;box-shadow:0 10px 24px rgb(10 20 40/.3);overflow:hidden}}
.luna img{{width:100%;height:100%;object-fit:contain;padding:14%;mix-blend-mode:multiply}}
.sello{{position:absolute;right:36px;top:30px;font-size:13px;color:#B9C6D8}}
</style></head><body>
{g.ICONOS}
<div class="lienzo">
  <div>
    <div class="marca"><svg aria-hidden="true"><use href="#simbolo"/></svg><b>minimundo</b></div>
    <p class="pre">Así podría ser vuestra web</p>
    <h1>Elegido de uno en uno.</h1>
    <p class="sub">Marca, tienda online y apartado por WhatsApp para Minimundo, La Carlota.</p>
    <ul>{muestras}</ul>
  </div>
  <div class="arte">{g.mundo(lunas, '').replace(' fetchpriority="low" decoding="async"','')}</div>
</div>
<p class="url">Miradla en el móvil · <b>opspilotcontact-lgtm.github.io/minimundo-maqueta</b></p>
<p class="sello">Propuesta de OpsPilot</p>
</body></html>'''
(g.RAIZ / '_presentacion.html').write_text(html, encoding='utf-8')
print('ok')
