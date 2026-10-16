# Minimundo · maqueta y propuesta (OpsPilot)

Propuesta de marca y tienda para Minimundo (Av. de la Paz, 59 · La Carlota). No indexada.

- `/` v2 «Elegido de uno en uno»: tienda con productos que Marta ya vende (precios de referencia), bolsa que se aparta por WhatsApp, carritos con cita, lista de nacimiento y club de lectura.
- `/propuesta/` documento comercial: lo medido, posicionamiento, arquitectura de marca, identidad, Google y plan.
- `/v1/` primera vuelta «una marca, dos puertas».

## Regenerar la tienda

```
python sitio/generar.py
```

Lee `sitio/catalogo.json`, `sitio/tienda.css` y `sitio/tienda.js` y escribe `index.html`, `tienda/`, `producto/<slug>/`, `carritos/`, `lista/`, `js/` e `img/p/` (fotos desde `fuente/productos/`, que no se publica).
Las notas de Marta (`NOTAS` en el generador) son frases suyas de Instagram; no se inventan.
