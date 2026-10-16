(function(){
  'use strict';
  var C = window.CATALOGO || {}, RAIZ = document.documentElement.dataset.raiz || './';
  var WA = 'https://wa.me/34624840524?text=';
  var eur = function(n){ return n == null ? '' : n.toLocaleString('es-ES',{minimumFractionDigits:2,maximumFractionDigits:2}) + ' €'; };
  var $ = function(s,c){ return (c||document).querySelector(s); };
  var $$ = function(s,c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); };

  /* ---------- bolsa ---------- */
  var bolsa = {};
  try { bolsa = JSON.parse(localStorage.getItem('mm-bolsa') || '{}') || {}; } catch(e){ bolsa = {}; }
  Object.keys(bolsa).forEach(function(k){ if(!C[k]) delete bolsa[k]; });
  function guarda(){ try { localStorage.setItem('mm-bolsa', JSON.stringify(bolsa)); } catch(e){} }
  function unidades(){ return Object.keys(bolsa).reduce(function(s,k){ return s + bolsa[k]; }, 0); }

  var cajon = $('#cajon'), lista = $('#bolsa-items'), cuenta = $('#cuenta'), totalEl = $('#bolsa-total');
  function pinta(){
    var n = unidades();
    if (cuenta){ cuenta.textContent = n; cuenta.classList.toggle('si', n > 0); }
    $$('.bolsa-btn').forEach(function(b){ b.setAttribute('aria-label', 'Bolsa, ' + n + (n === 1 ? ' artículo' : ' artículos')); });
    if (!lista) return;
    var claves = Object.keys(bolsa), total = 0, sinPrecio = false;
    lista.innerHTML = claves.map(function(k){
      var p = C[k], q = bolsa[k];
      if (p.pvp == null) sinPrecio = true; else total += p.pvp * q;
      return '<li class="c-' + p.cat + '"><img src="' + RAIZ + p.img + '" alt="" width="64" height="64">' +
        '<div><b>' + p.nombre + '</b><small>' + (p.pvp == null ? 'Precio en tienda' : eur(p.pvp)) + '</small>' +
        '<div class="cant"><button type="button" data-menos="' + k + '" aria-label="Quitar uno de ' + p.nombre + '">−</button><span>' + q + '</span><button type="button" data-mas="' + k + '" aria-label="Añadir otro ' + p.nombre + '">+</button></div></div>' +
        '<span class="precio">' + (p.pvp == null ? '' : eur(p.pvp * q)) + '</span></li>';
    }).join('');
    var vacia = claves.length === 0;
    $('#bolsa-vacia').hidden = !vacia;
    $('#bolsa-pie').hidden = vacia;
    totalEl.textContent = eur(total) + (sinPrecio ? ' + precio en tienda' : '');
  }
  function anade(k, origen){
    if (!C[k]) return;
    bolsa[k] = (bolsa[k] || 0) + 1; guarda(); pinta(); vuela(origen);
    avisa('Añadido: ' + C[k].nombre);
  }
  function vuela(origen){
    var btn = $('.bolsa-btn'); if (!origen || !btn) return;
    var img = origen.closest('.prod, .ficha, .reservas');
    img = img && img.querySelector('img');
    var reducir = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    btn.classList.remove('late'); void btn.offsetWidth; btn.classList.add('late');
    if (!img || reducir) return;
    var a = img.getBoundingClientRect(), b = btn.getBoundingClientRect();
    var t = Math.min(a.width, a.height, 160);
    var f = img.cloneNode(); f.className = 'vuela'; f.removeAttribute('srcset'); f.alt = '';
    f.style.cssText = 'left:' + (a.left + a.width/2 - t/2) + 'px;top:' + (a.top + a.height/2 - t/2) + 'px;width:' + t + 'px;height:' + t + 'px';
    document.body.appendChild(f);
    requestAnimationFrame(function(){ requestAnimationFrame(function(){
      var dx = b.left + b.width/2 - (a.left + a.width/2), dy = b.top + b.height/2 - (a.top + a.height/2);
      f.style.transform = 'translate(' + dx + 'px,' + dy + 'px) scale(.12)'; f.style.opacity = '.2';
    }); });
    setTimeout(function(){ f.remove(); }, 800);
  }
  var avisoEl;
  function avisa(t){
    if (!avisoEl){ avisoEl = document.createElement('div'); avisoEl.className = 'aviso-flot'; avisoEl.setAttribute('role','status'); document.body.appendChild(avisoEl); }
    avisoEl.textContent = t; avisoEl.classList.add('si');
    clearTimeout(avisa.t); avisa.t = setTimeout(function(){ avisoEl.classList.remove('si'); }, 2200);
  }
  function abre(){ document.body.classList.add('bolsa-abierta'); cajon.removeAttribute('inert'); cajon.setAttribute('aria-hidden','false'); setTimeout(function(){ $('#cerrar-bolsa').focus(); }, 60); }
  function cierra(){ document.body.classList.remove('bolsa-abierta'); cajon.setAttribute('inert',''); cajon.setAttribute('aria-hidden','true'); }

  document.addEventListener('click', function(e){
    var t = e.target.closest('[data-add],[data-mas],[data-menos],.bolsa-btn,#cerrar-bolsa,.velo,[data-orden]');
    if (!t) return;
    if (t.dataset.add){ e.preventDefault(); anade(t.dataset.add, t); t.classList.add('hecho'); setTimeout(function(){ t.classList.remove('hecho'); }, 1400); }
    else if (t.dataset.mas){ bolsa[t.dataset.mas]++; guarda(); pinta(); }
    else if (t.dataset.menos){ var k = t.dataset.menos; bolsa[k]--; if (bolsa[k] <= 0) delete bolsa[k]; guarda(); pinta(); }
    else if (t.classList.contains('bolsa-btn')){ e.preventDefault(); abre(); }
    else if (t.id === 'cerrar-bolsa' || t.classList.contains('velo')){ cierra(); }
  });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && document.body.classList.contains('bolsa-abierta')) cierra(); });

  function lineas(){
    return Object.keys(bolsa).map(function(k){ var p = C[k]; return '· ' + bolsa[k] + ' × ' + p.nombre + (p.pvp == null ? '' : ' (' + eur(p.pvp) + ')'); }).join('\n');
  }
  var apartar = $('#apartar');
  if (apartar) apartar.addEventListener('click', function(){
    var modo = ($('input[name=entrega]:checked') || {}).value || 'Recojo en la tienda';
    window.open(WA + encodeURIComponent('Hola Marta, quiero apartar esto:\n' + lineas() + '\n\n' + modo + '. ¿Me confirmas que lo tienes?'), '_blank', 'noopener');
  });
  var hacerLista = $('#hacer-lista');
  if (hacerLista) hacerLista.addEventListener('click', function(){
    var url = new URL(RAIZ + 'lista/', location.href);
    url.searchParams.set('l', Object.keys(bolsa).join('.'));
    location.href = url.toString();
  });

  /* ---------- catálogo: filtros ---------- */
  var rej = $('#catalogo');
  if (rej){
    var items = $$('.prod', rej), q = $('#busca'), orden = $('#orden'), num = $('#cuantos');
    var estado = { cat: 'todo', edad: 'todo' };
    var p = new URLSearchParams(location.search);
    if (p.get('cat')) estado.cat = p.get('cat');
    if (p.get('edad')) estado.edad = p.get('edad');
    if (p.get('q') && q) q.value = p.get('q');
    function marca(){
      $$('[data-cat]').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.cat === estado.cat); });
      $$('[data-edad]').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.edad === estado.edad); });
    }
    function filtra(){
      var txt = (q && q.value || '').trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
      var vis = 0;
      items.forEach(function(li){
        var ok = (estado.cat === 'todo' || li.dataset.c === estado.cat) &&
                 (estado.edad === 'todo' || (' ' + li.dataset.e + ' ').indexOf(' ' + estado.edad + ' ') > -1) &&
                 (!txt || li.dataset.t.indexOf(txt) > -1);
        li.hidden = !ok; if (ok) vis++;
      });
      if (orden){
        var o = orden.value, arr = items.slice();
        if (o !== 'nuevo') arr.sort(function(a,b){ var x = +a.dataset.p || 1e6, y = +b.dataset.p || 1e6; return o === 'barato' ? x - y : y - x; });
        else arr.sort(function(a,b){ return a.dataset.i - b.dataset.i; });
        arr.forEach(function(li){ rej.appendChild(li); });
      }
      num.textContent = vis === 1 ? '1 cosa elegida' : vis + ' cosas elegidas';
      $('#nada').hidden = vis > 0;
      marca();
    }
    document.addEventListener('click', function(e){
      var b = e.target.closest('[data-cat],[data-edad]'); if (!b) return;
      if (b.dataset.cat) estado.cat = b.dataset.cat; else estado.edad = b.dataset.edad;
      filtra();
    });
    if (q) q.addEventListener('input', filtra);
    if (orden) orden.addEventListener('change', filtra);
    filtra();
  }

  /* ---------- lista de nacimiento ---------- */
  var ln = $('#lista-items');
  if (ln){
    var prm = new URLSearchParams(location.search), claves = (prm.get('l') || '').split('.').filter(function(k){ return C[k]; });
    var nom = $('#lista-nombre');
    function enlace(){
      var u = new URL(location.href); u.searchParams.set('l', claves.join('.'));
      if (nom && nom.value.trim()) u.searchParams.set('n', nom.value.trim()); else u.searchParams.delete('n');
      return u.toString();
    }
    if (nom && prm.get('n')) nom.value = prm.get('n');
    var quien = prm.get('n');
    if (quien) $('#lista-tit').textContent = 'La lista de ' + quien;
    if (!claves.length){ $('#lista-vacia').hidden = false; }
    ln.innerHTML = claves.map(function(k){
      var p = C[k];
      var msg = 'Hola Marta, quiero regalar «' + p.nombre + '» de la lista' + (quien ? ' de ' + quien : ' de nacimiento') + '. ¿Me lo apartas?';
      return '<li class="prod c-' + p.cat + '"><a class="foto" href="' + RAIZ + 'producto/' + k + '/" tabindex="-1" aria-hidden="true"><img src="' + RAIZ + p.img + '" alt="" width="480" height="600" loading="lazy"></a>' +
        '<p class="marca-p">' + p.marca + '</p><h3><a href="' + RAIZ + 'producto/' + k + '/">' + p.nombre + '</a></h3>' +
        '<div class="pie-p"><span class="precio">' + (p.pvp == null ? '' : eur(p.pvp)) + '</span>' +
        '<a class="btn btn-wa" style="position:relative;z-index:2;min-height:40px;padding:.4em .9em;font-size:.88rem" target="_blank" rel="noopener" href="' + WA + encodeURIComponent(msg) + '">Lo regalo yo</a></div></li>';
    }).join('');
    var comp = $('#compartir');
    if (comp) comp.addEventListener('click', function(){
      var u = enlace(), txt = 'Esta es nuestra lista de nacimiento en Minimundo (La Carlota). Si queréis regalarnos algo, desde aquí se lo pedís a Marta:';
      if (navigator.share) navigator.share({ title: 'Lista de nacimiento', text: txt, url: u }).catch(function(){});
      else window.open(WA + encodeURIComponent(txt + ' ' + u), '_blank', 'noopener');
    });
  }

  /* ---------- cuenta atrás de Reyes ---------- */
  var dias = $('#dias-reyes');
  if (dias){
    var hoy = new Date(), y = (hoy.getMonth() === 0 && hoy.getDate() <= 6) ? hoy.getFullYear() : hoy.getFullYear() + 1;
    var reyes = new Date(y, 0, 6), d = Math.ceil((reyes - new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate())) / 864e5);
    dias.textContent = d;
  }

  /* ---------- hoja de carrito ---------- */
  var f = $('#hoja-carrito');
  if (f){
    var mir = $('#miramos'), vac = $('#vacio'), ped = $('#pedir');
    var consejos = {
      cuando:{'Ya ha nacido':'Vente con tu bebé: probamos la postura en el capazo o en la silla.','Faltan 1 a 3 meses':'Buen momento: hay tiempo para probar y para pedirlo si no está en tienda.','Faltan más de 3 meses':'Sin agobios: primero lo vemos y luego decides.'},
      paseo:{'Aceras del pueblo':'Ruedas que suban bordillos y un plegado sencillo.','Caminos y campo':'Ruedas grandes y buena suspensión para el camino.','Ciudad, autobús y tiendas':'Poco peso y plegado con una mano.'},
      coche:{'Pequeño':'Medimos el maletero: trae la medida o ven con el coche.','Mediano o familiar':'Comprobamos que cabe plegado junto a la compra.','Monovolumen o SUV':'Miramos los anclajes ISOFIX para la silla.','Sin coche':'Sin coche, el carrito tiene que servir para todo el día.'},
      busca:{'Carrito completo con capazo':'Capazo y silla: cuánto tiempo usaréis cada parte.','Silla de coche':'La silla se elige por la altura de tu bebé y se prueba en tu coche.','Silla ligera de paseo':'Peso, plegado y si cabe en el maletero.','Aún no lo sé':'Empezamos por cómo vivís y de ahí sale el qué.'}
    };
    f.addEventListener('change', function(){
      var datos = new FormData(f), it = [], res = [];
      ['cuando','paseo','coche','busca'].forEach(function(k){ var v = datos.get(k); if (v){ it.push(consejos[k][v]); res.push(v); } });
      mir.innerHTML = it.map(function(t){ return '<li>' + t + '</li>'; }).join('');
      var hay = it.length > 0; mir.hidden = !hay; vac.hidden = hay; ped.hidden = !hay;
      ped.href = WA + encodeURIComponent('Hola Marta, quiero cita para probar carritos. Mi hoja: ' + res.join(' · ') + '.');
    });
  }

  cierra(); pinta();
})();
