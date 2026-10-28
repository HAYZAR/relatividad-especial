#!/usr/bin/env python3
"""Genera index.html (la presentación) a partir de fuente/deck.json y fuente/diapositivas/*.html.

Uso:  python3 build.py
Cada diapositiva es un <section> de 1920×1080 px con estilos en línea. El script:
  - sustituye <x-icon> por iconos SVG,
  - convierte <x-embed> (animaciones) en iframes con srcdoc,
  - mueve las notas del orador (<aside>) a un atributo data-notes,
  - apunta las imágenes a la carpeta assets/ y el enlace de simuladores a simuladores.html.
"""
import html
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent
FUENTE = RAIZ / "fuente"

IMAGENES = {
    "87ff717e2505da8558f6f8779bc860f7": "assets/fondo.jpg",
    "327ee5fe9bb8bf55f929553e5255b89c": "assets/muones.jpg",
}
ENLACE_SIMULADORES = "https://claude.ai/artifact/6rQGogQwzWJug3VLQy397n"

ICONOS = {
    "Check": '<polyline points="20 6 9 17 4 12"/>',
    "Lightning": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "Globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/>'
             '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "Search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "Activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "PaperPlane": '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>',
    "Clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "Chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>'
             '<line x1="6" y1="20" x2="6" y2="14"/>',
}


def icono(m):
    nombre, estilo = m.group(1), m.group(2)
    trazos = ICONOS[nombre]
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'style="{estilo}">{trazos}</svg>')


def embed(m):
    estilo, interior = m.group(1), m.group(2)
    doc = ('<!doctype html><html><head><meta charset="utf-8"></head>'
           f'{interior}</html>')
    return ('<iframe class="embed" title="Animación" sandbox="allow-scripts" '
            f'style="{estilo};border:0;background:#0B1230" '
            f'data-doc="{html.escape(doc, quote=True)}"></iframe>')


def procesar(texto):
    texto = texto.strip()
    notas = ""
    m = re.search(r"<aside>(.*?)</aside>", texto, re.S)
    if m:
        notas = m.group(1).strip()
        texto = texto.replace(m.group(0), "")
        notas = notas.replace(
            " Nota: el enlace solo abre para quien tenga acceso a la página; compártela antes de la charla.", "")
    texto = re.sub(r'<x-icon name="(\w+)" style="([^"]*)"></x-icon>', icono, texto)
    texto = re.sub(r"<x-embed style=\"([^\"]*)\">(.*?)</x-embed>", embed, texto, flags=re.S)
    for id_recurso, ruta in IMAGENES.items():
        texto = texto.replace(f"/_blob/{id_recurso}", ruta)
    texto = texto.replace(
        "Abrir los simuladores: claude.ai/artifact/6rQGogQwzWJug3VLQy397n", "Abrir los simuladores →")
    texto = texto.replace(
        "Para practicar: simuladores interactivos de esta charla en claude.ai/artifact/6rQGogQwzWJug3VLQy397n",
        'Para practicar: <a href="simuladores.html"><span style="color:#FFC24D">simuladores interactivos de esta charla</span></a>')
    texto = texto.replace(f'href="{ENLACE_SIMULADORES}"', 'href="simuladores.html"')
    texto = re.sub(r'<a href="(https://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', texto)
    texto = texto.replace("<section ", f'<section class="slide" data-notes="{html.escape(notas, quote=True)}" ', 1)
    return texto


PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="Charla de divulgación científica: trenes, muones, GPS y PET, con animaciones y simuladores.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400..700&family=DM+Sans:wght@400;500;700&display=swap">
<style>
html,body{{margin:0;height:100%;background:#000;overflow:hidden;font-family:'DM Sans',Arial,sans-serif}}
#viewport{{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;cursor:pointer}}
#stage{{position:relative;width:1920px;height:1080px;flex:none;transform-origin:center center;background:#070B16}}
.slide,.slide *{{box-sizing:border-box}}
.slide{{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden;visibility:hidden;opacity:0;transition:opacity .35s,visibility 0s .35s}}
.slide.on{{visibility:visible;opacity:1;transition:opacity .35s}}
.slide p,.slide h1,.slide h2,.slide h3{{margin:0}}
.slide ul,.slide ol{{margin:0;padding-left:1.1em}}
.slide li+li{{margin-top:.3em}}
.slide hr{{margin:0;border:0;height:0}}
.slide table{{border-collapse:collapse}}
.slide th,.slide td{{padding:.3em .6em;border-bottom:1px solid #26335F;text-align:left}}
.slide th{{color:#FFC24D;border-bottom:2px solid #4A5A8C}}
.slide a{{color:inherit;text-decoration:underline;text-underline-offset:6px}}
.slide svg{{flex:none}}
#bar{{position:fixed;left:0;top:0;height:4px;background:#FFC24D;width:0;transition:width .3s;z-index:5}}
#count{{position:fixed;right:16px;bottom:12px;color:#A9B6D6;font-size:15px;z-index:5;opacity:.8;pointer-events:none}}
#notes{{position:fixed;left:0;right:0;bottom:0;max-height:38%;overflow:auto;background:rgba(7,11,22,.94);color:#EAF0FF;padding:18px 28px 28px;font-size:19px;line-height:1.5;z-index:6;border-top:2px solid #FFC24D;display:none;cursor:default}}
#notes.on{{display:block}}
#hint{{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);background:rgba(15,23,48,.92);color:#EAF0FF;border:1px solid #26335F;border-radius:999px;padding:10px 22px;font-size:16px;z-index:7;transition:opacity .6s;pointer-events:none}}
</style>
</head>
<body>
<div id="viewport"><div id="stage">
{diapositivas}
</div></div>
<div id="bar"></div>
<div id="count"></div>
<div id="notes" role="region" aria-label="Notas del orador"></div>
<div id="hint">← → para avanzar · F pantalla completa · N notas del orador</div>
<script>
(function(){{
var slides=[].slice.call(document.querySelectorAll('.slide')),N=slides.length,cur=-1;
var stage=document.getElementById('stage'),notes=document.getElementById('notes');
function fit(){{var s=Math.min(innerWidth/1920,innerHeight/1080);stage.style.transform='scale('+s+')'}}
function frames(sl,on){{[].forEach.call(sl.querySelectorAll('iframe[data-doc]'),function(f){{
if(on){{f.srcdoc=f.getAttribute('data-doc')}}else{{f.removeAttribute('srcdoc')}}}})}}
function show(n){{n=Math.max(0,Math.min(N-1,n));if(n===cur)return;
if(cur>=0){{slides[cur].classList.remove('on');frames(slides[cur],false)}}
cur=n;slides[n].classList.add('on');frames(slides[n],true);
document.getElementById('bar').style.width=((n+1)/N*100)+'%';
document.getElementById('count').textContent=(n+1)+' / '+N;
notes.textContent=slides[n].getAttribute('data-notes')||'Esta diapositiva no tiene notas.';
try{{history.replaceState(null,'','#'+(n+1))}}catch(e){{}}}}
function next(){{show(cur+1)}}function prev(){{show(cur-1)}}
document.addEventListener('keydown',function(e){{
if(e.ctrlKey||e.metaKey||e.altKey)return;var k=e.key;
if(k==='ArrowRight'||k==='PageDown'||k===' '||k==='Enter'||k==='ArrowDown'){{e.preventDefault();next()}}
else if(k==='ArrowLeft'||k==='PageUp'||k==='Backspace'||k==='ArrowUp'){{e.preventDefault();prev()}}
else if(k==='Home')show(0);else if(k==='End')show(N-1);
else if(k==='f'||k==='F'){{if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen()}}
else if(k==='n'||k==='N')notes.classList.toggle('on');
else if(k==='Escape')notes.classList.remove('on')}});
document.getElementById('viewport').addEventListener('click',function(e){{
if(e.target.closest('a'))return;if(e.clientX<innerWidth/3)prev();else next()}});
var tx=null;
document.addEventListener('touchstart',function(e){{tx=e.touches[0].clientX}},{{passive:true}});
document.addEventListener('touchend',function(e){{if(tx===null)return;var d=e.changedTouches[0].clientX-tx;tx=null;
if(Math.abs(d)>50){{if(d<0)next();else prev()}}}},{{passive:true}});
window.addEventListener('resize',fit);
window.addEventListener('hashchange',function(){{var n=parseInt(location.hash.slice(1),10);if(n)show(n-1)}});
fit();show((parseInt(location.hash.slice(1),10)||1)-1);
setTimeout(function(){{document.getElementById('hint').style.opacity=0}},5000);
}})();
</script>
</body>
</html>
"""


def main():
    indice = json.loads((FUENTE / "deck.json").read_text(encoding="utf-8"))
    partes = []
    for id_diapositiva in indice["order"]:
        archivo = FUENTE / "diapositivas" / f"{id_diapositiva}.html"
        partes.append(procesar(archivo.read_text(encoding="utf-8")))
    salida = PLANTILLA.format(titulo=html.escape(indice["title"]), diapositivas="\n".join(partes))
    (RAIZ / "index.html").write_text(salida, encoding="utf-8")
    print(f"index.html generado con {len(partes)} diapositivas ({len(salida) // 1024} KB)")


if __name__ == "__main__":
    main()
