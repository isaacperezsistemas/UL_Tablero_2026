"""
UL Tablero 2026 · Principios de la Gestalt aplicados a la visualización de datos.

Cada sección explica un principio, lo demuestra con un gráfico interactivo
en estilo de bloques (pixel art) y recomienda el widget de ipywidgets que
lo ejemplifica en un notebook de Jupyter.

Ejecutar:  streamlit run app.py
"""

import base64
import json
import math
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="UL Tablero 2026 · Gestalt", page_icon="🧱", layout="wide")

# ---------------------------------------------------------------------------
# Paleta del mundo de bloques
# ---------------------------------------------------------------------------
C = {
    "pasto": "#5D9C3B", "tierra": "#8B5A3C", "piedra": "#8A8A8A", "tablon": "#B08850",
    "cielo": "#87B8FF", "noche": "#141A2E", "cueva": "#262626",
    "diamante": "#3FE0D0", "oro": "#F5D03B", "hierro": "#D8AF93", "redstone": "#C0261F",
    "esmeralda": "#2BD46B", "lapislazuli": "#3557C4", "carbon": "#3A3A3A",
}
COLOR_MINERAL = {"Hierro": C["hierro"], "Oro": C["oro"], "Diamante": C["diamante"]}
PIXEL = "'Press Start 2P', monospace"
TEXTO = "'VT323', monospace"


# ---------------------------------------------------------------------------
# Texturas pixeladas generadas como SVG (sin imágenes externas)
# ---------------------------------------------------------------------------
def _data_uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def textura(colores, semilla, n=16, px=4):
    rnd = random.Random(semilla)
    rects = "".join(
        f'<rect x="{x*px}" y="{y*px}" width="{px}" height="{px}" fill="{rnd.choice(colores)}"/>'
        for y in range(n) for x in range(n)
    )
    return _data_uri(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{n*px}" height="{n*px}" '
        f'shape-rendering="crispEdges">{rects}</svg>'
    )


def textura_tablones(px=4, n=16):
    rnd = random.Random(5)
    base = ["#B08850", "#A57E48", "#BB9258", "#9C7642"]
    rects = []
    for y in range(n):
        linea = y % 4 == 3
        for x in range(n):
            color = "#6E5030" if linea or (x == (5 if (y // 4) % 2 else 12)) else rnd.choice(base)
            rects.append(f'<rect x="{x*px}" y="{y*px}" width="{px}" height="{px}" fill="{color}"/>')
    return _data_uri(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{n*px}" height="{n*px}" '
        f'shape-rendering="crispEdges">{"".join(rects)}</svg>'
    )


TX_PIEDRA = textura(["#7A7A7A", "#6E6E6E", "#858585", "#747474", "#686868"], 1)
TX_TIERRA = textura(["#8B5A3C", "#7A4E33", "#966446", "#6F4630"], 2)
TX_PASTO = textura(["#5D9C3B", "#4F8A31", "#6AAE44", "#57933A"], 3)
TX_TABLON = textura_tablones()


# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------
st.markdown(
    f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
.stApp {{
  background-color:#3a3a3a;
  background-image:linear-gradient(rgba(18,18,18,.62),rgba(18,18,18,.62)),url({TX_PIEDRA});
  background-size:auto,64px 64px; image-rendering:pixelated;
}}
[data-testid="stHeader"] {{ background:transparent; }}
[data-testid="stSidebar"] > div:first-child {{
  background-image:linear-gradient(rgba(0,0,0,.08),rgba(0,0,0,.08)),url({TX_TABLON});
  background-size:auto,64px 64px; border-right:4px solid #000;
}}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] h1 {{ color:#2b1d0e !important; }}
[data-testid="stSidebar"] h1 {{ font-family:{PIXEL}; font-size:15px; line-height:1.6;
  text-shadow:2px 2px 0 rgba(255,255,255,.25); }}
.stApp p, .stApp li, .stApp label, .stApp input, .stApp .stMarkdown {{ font-family:{TEXTO}; font-size:21px; }}
.stApp code, .stApp pre {{ font-family:ui-monospace,Menlo,Consolas,monospace; font-size:14px; }}
[data-testid="stExpander"] details {{ background:#1e1e1e; border:3px solid #000 !important; border-radius:0; }}
[data-testid="stExpander"] summary p {{ font-family:{PIXEL}; font-size:11px; color:{C['oro']}; }}

.banner {{ border:4px solid #000; margin-bottom:10px; }}
.banner .pasto {{ height:20px; background:url({TX_PASTO}); background-size:64px 64px; border-bottom:3px solid #3f6e27; }}
.banner .tierra {{ background:linear-gradient(rgba(0,0,0,.25),rgba(0,0,0,.25)),url({TX_TIERRA});
  background-size:auto,64px 64px; padding:16px 20px 18px; }}
.banner .num {{ font-family:{PIXEL}; font-size:10px; color:{C['oro']}; letter-spacing:1px; }}
.banner .titulo {{ font-family:{PIXEL}; font-size:26px; color:#fff; margin:10px 0 8px;
  text-shadow:3px 3px 0 #3f3f3f; line-height:1.3; }}
.banner .sub {{ font-family:{TEXTO}; font-size:24px; color:#f1e6d8; }}
.chip {{ display:inline-block; margin-top:10px; font-family:{PIXEL}; font-size:9px; color:#1b1b1b;
  background:{C['diamante']}; padding:6px 8px; border:3px solid; border-color:#bff8f2 #1c8f85 #1c8f85 #bff8f2; }}

.hotbar {{ display:flex; gap:4px; margin:0 0 18px; flex-wrap:wrap; }}
.slot {{ width:46px; height:46px; background:#8B8B8B; border:3px solid; border-color:#373737 #fff #fff #373737;
  display:flex; align-items:center; justify-content:center; font-family:{PIXEL}; font-size:12px; color:#3f3f3f; }}
.slot.on {{ outline:4px solid #fff; outline-offset:-1px; background:#a8a8a8; color:#000; }}

.panel {{ background:#C6C6C6; border:4px solid; border-color:#fff #555 #555 #fff; box-shadow:0 0 0 3px #000;
  padding:12px 16px 10px; margin:3px 3px 18px; }}
.panel .t {{ font-family:{PIXEL}; font-size:11px; color:#3f3f3f; margin-bottom:6px; }}
.panel p, .panel li {{ color:#262626 !important; font-family:{TEXTO}; font-size:22px; line-height:1.12; margin:0 0 6px; }}
.panel b {{ color:#000; }}
.panel.mision {{ background:#2f2f2f; border-color:#6b6b6b #111 #111 #6b6b6b; }}
.panel.mision .t {{ color:{C['oro']}; }}
.panel.mision p {{ color:#eaeaea !important; }}

.lienzo {{ border:4px solid #000; box-shadow:4px 4px 0 rgba(0,0,0,.45); line-height:0; margin-bottom:10px; }}
.lienzo svg {{ display:block; width:100%; height:auto; }}
.nota {{ font-family:{TEXTO}; font-size:22px; color:#fff; background:#1e1e1e; border-left:6px solid {C['esmeralda']};
  padding:8px 12px; margin:6px 0 14px; }}
.nota.alerta {{ border-left-color:{C['redstone']}; }}

.grid7 {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:14px; }}
.grid7 .panel {{ margin:3px; }}
.tabla td, .tabla th {{ font-family:{TEXTO}; font-size:21px; color:#262626; padding:3px 8px; text-align:left; }}
.tabla th {{ font-family:{PIXEL}; font-size:9px; }}
.pie {{ font-family:{TEXTO}; font-size:18px; color:#bdbdbd; margin-top:26px; }}
.pie a {{ color:{C['diamante']}; }}

/* Controles: caja oscura propia, texto blanco y acento verde aunque no exista config.toml */
[data-testid="stSlider"], [data-testid="stRadio"], [data-testid="stCheckbox"],
[data-testid="stSelectbox"], [data-testid="stColorPicker"] {{
  background:#1e1e1e; border:3px solid #000; box-shadow:inset 3px 3px 0 #3a3a3a; padding:8px 12px 6px; }}
[data-testid="stMain"] [data-testid="stWidgetLabel"] p,
[data-testid="stMain"] [data-testid="stRadio"] label p,
[data-testid="stMain"] [data-testid="stCheckbox"] label p,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] > p {{ color:#fff !important; text-shadow:2px 2px 0 #000; }}
[data-testid="stSlider"] [data-baseweb="slider"], [data-testid="stSlider"] [role="group"],
[data-testid="stRadio"] [role="radiogroup"],
[data-testid="stCheckbox"] label {{ filter:hue-rotate(110deg); }}
</style>""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Utilidades de dibujo
# ---------------------------------------------------------------------------
def bloque(x, y, s, color, opacidad=1.0):
    """Un bloque con biselado: luz arriba/izquierda, sombra abajo/derecha."""
    b = max(2, s // 7)
    op = f' opacity="{opacidad:.2f}"' if opacidad < 1 else ""
    return (
        f'<g{op}><rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{color}"/>'
        f'<rect x="{x}" y="{y}" width="{s}" height="{b}" fill="#fff" opacity=".30"/>'
        f'<rect x="{x}" y="{y}" width="{b}" height="{s}" fill="#fff" opacity=".18"/>'
        f'<rect x="{x}" y="{y+s-b}" width="{s}" height="{b}" fill="#000" opacity=".32"/>'
        f'<rect x="{x+s-b}" y="{y}" width="{b}" height="{s}" fill="#000" opacity=".22"/></g>'
    )


def texto(x, y, contenido, color="#fff", tam=18, ancla="start", fuente=TEXTO):
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{tam}" font-family="{fuente}" '
        f'text-anchor="{ancla}">{contenido}</text>'
    )


def svg(ancho, alto, cuerpo, fondo):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" '
        f'shape-rendering="crispEdges"><rect width="{ancho}" height="{alto}" fill="{fondo}"/>{cuerpo}</svg>'
    )


def lienzo(contenido_svg):
    st.markdown(f'<div class="lienzo">{contenido_svg}</div>', unsafe_allow_html=True)


def panel(titulo, html, clase=""):
    st.markdown(f'<div class="panel {clase}"><div class="t">{titulo}</div>{html}</div>', unsafe_allow_html=True)


def nota(html, alerta=False):
    st.markdown(f'<div class="nota{" alerta" if alerta else ""}">{html}</div>', unsafe_allow_html=True)


def encabezado(n, titulo, subtitulo, widget):
    slots = "".join(f'<div class="slot{" on" if i == n else ""}">{i}</div>' for i in range(1, 8))
    st.markdown(
        f'<div class="banner"><div class="pasto"></div><div class="tierra">'
        f'<div class="num">BLOQUE {n} DE 7</div>'
        f'<div class="titulo">{titulo}</div><div class="sub">{subtitulo}</div>'
        f'<span class="chip">ipywidgets.{widget}</span></div></div>'
        f'<div class="hotbar">{slots}</div>',
        unsafe_allow_html=True,
    )


def teoria(que_es, en_datos, mision):
    panel("¿QUÉ ES?", f"<p>{que_es}</p>")
    panel("¿Y EN LAS GRÁFICAS?", f"<p>{en_datos}</p>")
    panel("⛏ TU MISIÓN", f"<p>{mision}</p>", "mision")


def widget_recomendado(widget, porque, codigo, equivalente):
    with st.expander(f"🧩 Para programadores: ipywidgets.{widget}"):
        st.markdown(f"**¿Por qué este widget?** {porque}")
        st.markdown("**En un notebook de Jupyter:**")
        st.code(codigo, language="python")
        st.markdown(f"**Equivalente usado en este tablero (Streamlit):** `{equivalente}`")


# ---------------------------------------------------------------------------
# Inicio
# ---------------------------------------------------------------------------
PRINCIPIOS = [
    ("Cierre", "IntSlider", "Tu cerebro rellena los huecos."),
    ("Proximidad", "ToggleButtons", "Lo que está cerca parece un equipo."),
    ("Continuidad", "Dropdown", "Tus ojos siguen los caminos suaves."),
    ("Semejanza", "ColorPicker", "Lo que se parece, parece familia."),
    ("Figura y fondo", "FloatSlider", "Ves lo importante y lo demás queda atrás."),
    ("Dirección común", "Play", "Lo que avanza junto es un grupo."),
    ("Simetría", "ToggleButton", "Igual de los dos lados se ve ordenado."),
]


def inicio():
    st.markdown(
        f'<div class="banner"><div class="pasto"></div><div class="tierra">'
        f'<div class="num">UL TABLERO 2026</div>'
        f'<div class="titulo">El Mundo Gestalt</div>'
        f'<div class="sub">7 trucos que usa tu cerebro para entender dibujos y gráficas.</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )
    panel(
        "¿DE QUÉ SE TRATA?",
        "<p>Tu cerebro es un <b>constructor experto</b>: cuando ve muchos bloques sueltos, los junta y arma "
        "una figura completa. A esto los científicos le llaman <b>Gestalt</b>, una palabra alemana que "
        "significa <i>forma</i>.</p>"
        "<p>Hace más de 100 años, unos científicos descubrieron <b>7 trucos</b> que usa tu cerebro para ver. "
        "Hoy los usamos para hacer gráficas fáciles de entender. Entra a cada bloque, lee, mueve los "
        "controles y cumple la misión. ⛏</p>",
    )
    tarjetas = "".join(
        f'<div class="panel"><div class="t">BLOQUE {i} · {n.upper()}</div>'
        f'<p>{d}</p><span class="chip">{w}</span></div>'
        for i, (n, w, d) in enumerate(PRINCIPIOS, start=1)
    )
    st.markdown(f'<div class="grid7">{tarjetas}</div>', unsafe_allow_html=True)
    nota("Elige un bloque en el menú de la izquierda para empezar. ⛏")


# ---------------------------------------------------------------------------
# 1 · Cierre
# ---------------------------------------------------------------------------
def anillo_svg(removidos, avance, guia):
    n, s, m = 21, 18, 12
    c, r = (n - 1) / 2, 8.6
    celdas = [(x, y) for y in range(n) for x in range(n) if r - 1.1 <= math.hypot(x - c, y - c) <= r + 0.5]
    celdas.sort(key=lambda p: math.atan2(p[0] - c, -(p[1] - c)) % (2 * math.pi))
    llenas = round(len(celdas) * avance / 100)
    orden = celdas[:]
    random.Random(7).shuffle(orden)
    quitadas = set(orden[: round(len(celdas) * removidos / 100)])

    cuerpo = []
    for i, (x, y) in enumerate(celdas):
        px, py = m + x * s, m + y * s
        if (x, y) in quitadas:
            if guia:
                cuerpo.append(
                    f'<rect x="{px+2}" y="{py+2}" width="{s-4}" height="{s-4}" fill="none" '
                    f'stroke="#ffffff" stroke-opacity=".35" stroke-dasharray="3 3"/>'
                )
            continue
        cuerpo.append(bloque(px, py, s, C["diamante"] if i < llenas else C["piedra"]))
    centro = m + n * s / 2
    cuerpo.append(texto(centro, centro + 4, f"{avance}%", "#fff", 26, "middle", PIXEL))
    cuerpo.append(texto(centro, centro + 34, "EXCAVADO", "#bdbdbd", 22, "middle"))
    lado = n * s + 2 * m
    return svg(lado, lado, "".join(cuerpo), C["cueva"])


def seccion_cierre():
    encabezado(1, "Cierre", "Tu cerebro rellena los huecos.", "IntSlider")
    izq, der = st.columns([1, 1.25], gap="large")
    with izq:
        teoria(
            "Si a un dibujo le faltan pedazos, tu cerebro <b>rellena los huecos</b> solito y ves la figura "
            "completa. ¡Ni te das cuenta!",
            "Por eso una gráfica puede tener <b>espacios o cortes</b> y aun así la entiendes. No hace falta "
            "dibujar todos los bordes.",
            "Usa el pico para quitarle bloques al círculo. ¿Hasta cuándo sigues viendo un círculo?",
        )
    with der:
        quitados = st.slider("⛏ ¿Cuántos bloques quitas con el pico? (%)", 0, 90, 30, step=5)
        a, b = st.columns(2)
        avance = a.slider("💎 ¿Cuánto llevamos excavado? (%)", 0, 100, 72)
        b.write("")
        guia = b.checkbox("Ver los huecos", value=False)
        lienzo(anillo_svg(quitados, avance, guia))
        if quitados <= 45:
            nota("¡Le faltan bloques, pero tú sigues viendo un <b>círculo completo</b>! Tu cerebro rellenó los huecos.")
        elif quitados <= 70:
            nota("Ya cuesta más trabajo… tu cerebro necesita <b>suficientes pistas</b> para adivinar la figura.")
        else:
            nota("¡Se rompió! Con tantos huecos tu cerebro <b>ya no puede</b> adivinar la figura.", alerta=True)
    widget_recomendado(
        "IntSlider",
        "Un deslizador entero permite quitar información poco a poco y encontrar el punto donde el "
        "cerebro deja de completar la figura.",
        """from ipywidgets import interact, IntSlider

@interact(removidos=IntSlider(value=30, min=0, max=90, step=5,
                              description='Removidos %'))
def anillo(removidos):
    dibujar_anillo(removidos)   # tu función con matplotlib""",
        'st.slider("Bloques removidos (%)", 0, 90, 30, step=5)',
    )


# ---------------------------------------------------------------------------
# 2 · Proximidad
# ---------------------------------------------------------------------------
DATOS_PROX = {
    "Pradera": {"Hierro": 7, "Oro": 3, "Diamante": 1},
    "Desierto": {"Hierro": 4, "Oro": 8, "Diamante": 1},
    "Taiga": {"Hierro": 8, "Oro": 2, "Diamante": 2},
    "Montaña": {"Hierro": 9, "Oro": 5, "Diamante": 4},
}


def barras_agrupadas_svg(por_bioma, separacion):
    s, m, base = 18, 24, 9
    biomas, minerales = list(DATOS_PROX), ["Hierro", "Oro", "Diamante"]
    externos, internos = (biomas, minerales) if por_bioma else (minerales, biomas)
    alto = m + base * s + s + 58
    cuerpo, x, grupos = [], m, []
    for g in externos:
        x0 = x
        for i in internos:
            bioma, mineral = (g, i) if por_bioma else (i, g)
            valor = DATOS_PROX[bioma][mineral]
            for k in range(valor):
                cuerpo.append(bloque(x, m + (base - 1 - k) * s, s, COLOR_MINERAL[mineral]))
            if not por_bioma:
                cuerpo.append(texto(x + s / 2, m + base * s + s + 16, bioma[:3], "#1d2b4a", 16, "middle"))
            x += s + 2
        grupos.append((g, x0, x - 2))
        x += separacion * s
    ancho = x - separacion * s + m
    for gx in range(0, ancho, s):
        cuerpo.append(bloque(gx, m + base * s, s, C["pasto"]))
    for g, a, b in grupos:
        cuerpo.append(texto((a + b) / 2, alto - 10, g, "#10203f", 20, "middle"))
    return svg(max(ancho, 260), alto, "".join(cuerpo), C["cielo"])


def leyenda_minerales():
    return " ".join(
        f'<span style="display:inline-block;width:14px;height:14px;background:{c};border:2px solid #000;'
        f'vertical-align:middle"></span> {n}'
        for n, c in COLOR_MINERAL.items()
    )


def seccion_proximidad():
    encabezado(2, "Proximidad", "Lo que está cerca parece un equipo.", "ToggleButtons")
    izq, der = st.columns([1, 1.25], gap="large")
    with izq:
        teoria(
            "Cuando las cosas están <b>juntitas</b>, tu cerebro piensa que son un equipo, aunque sean iguales. "
            "Como los amigos que se sientan juntos en el recreo.",
            "En una gráfica de barras, las barras que están juntas se comparan entre sí. El <b>espacio</b> "
            "entre grupos le dice a tus ojos cuáles son los equipos.",
            "Cambia los equipos con los botones. Luego pon el espacio en 0. ¿Todavía ves los equipos?",
        )
    with der:
        modo = st.radio("¿Cómo armamos los equipos?", ["Por lugar", "Por mineral"], horizontal=True)
        sep = st.slider("↔ Espacio entre equipos (bloques)", 0, 4, 2)
        lienzo(barras_agrupadas_svg(modo == "Por lugar", sep))
        st.markdown(f'<div class="nota">{leyenda_minerales()}</div>', unsafe_allow_html=True)
        if sep == 0:
            nota("¡Sin espacio ya no hay equipos! Parece <b>una sola fila</b> de barras.", alerta=True)
        elif modo == "Por lugar":
            nota("Cada lugar es un equipo: ves <b>qué minerales hay</b> en cada uno.")
        else:
            nota("Cada mineral es un equipo: ves <b>en qué lugar hay más</b> de cada uno.")
    widget_recomendado(
        "ToggleButtons",
        "Un conjunto de botones exclusivos deja cambiar el criterio de agrupación con un clic y ver "
        "cómo la proximidad reorganiza la lectura.",
        """from ipywidgets import interact, ToggleButtons, IntSlider

@interact(agrupar=ToggleButtons(options=['Bioma', 'Mineral'],
                                description='Agrupar por'),
          separacion=IntSlider(value=2, min=0, max=4))
def barras(agrupar, separacion):
    dibujar_barras(agrupar, separacion)""",
        'st.radio("Agrupar por", ["Bioma", "Mineral"], horizontal=True)',
    )


# ---------------------------------------------------------------------------
# 3 · Continuidad
# ---------------------------------------------------------------------------
TUNELES = {"Túnel A": 12, "Túnel B": 7, "Túnel C": 18, "Túnel D": 4,
           "Túnel E": 15, "Túnel F": 9, "Túnel G": 20, "Túnel H": 11}


def tuneles_svg(orden, rieles):
    s, izq, m = 16, 92, 16
    items = list(TUNELES.items())
    if orden == "De mayor a menor":
        items.sort(key=lambda t: -t[1])
    elif orden == "De menor a mayor":
        items.sort(key=lambda t: t[1])
    cuerpo, puntos = [], []
    for fila, (nombre, valor) in enumerate(items):
        y = m + fila * (s + 8)
        cuerpo.append(texto(izq - 10, y + s - 2, nombre, "#e6e6e6", 19, "end"))
        for k in range(valor):
            cuerpo.append(bloque(izq + k * s, y, s, C["lapislazuli"]))
        puntos.append((izq + valor * s + 6, y + s / 2))
    if rieles:
        ruta = " ".join(f"{x},{y}" for x, y in puntos)
        cuerpo.append(f'<polyline points="{ruta}" fill="none" stroke="#6b4a2b" stroke-width="8" '
                      f'stroke-dasharray="3 4" shape-rendering="auto"/>')
        cuerpo.append(f'<polyline points="{ruta}" fill="none" stroke="#cfcfcf" stroke-width="2.5" '
                      f'shape-rendering="auto"/>')
        cuerpo += [bloque(x - 5, y - 5, 10, C["oro"]) for x, y in puntos]
    ancho, alto = izq + 20 * s + 40, m * 2 + len(items) * (s + 8)
    return svg(ancho, alto, "".join(cuerpo), C["cueva"])


def seccion_continuidad():
    encabezado(3, "Continuidad", "Tus ojos siguen el camino más suave.", "Dropdown")
    izq, der = st.columns([1, 1.25], gap="large")
    with izq:
        teoria(
            "Tus ojos son como un carrito de mina: les gusta seguir un <b>riel suave</b>, sin saltos ni "
            "vueltas raras.",
            "Si <b>ordenas</b> las barras de mayor a menor, tus ojos bajan como por una resbaladilla y ves "
            "rápido cuál es la más grande.",
            "Cambia el orden de los túneles. ¿Con cuál orden el riel se ve más suave y fácil de seguir?",
        )
    with der:
        a, b = st.columns([1.3, 1])
        orden = a.selectbox("¿En qué orden van los túneles?", ["Por letra", "De mayor a menor", "De menor a mayor"])
        b.write("")
        rieles = b.checkbox("Rieles", value=True)
        lienzo(tuneles_svg(orden, rieles))
        if orden == "Por letra":
            nota("¡El riel va de un lado a otro! Tus ojos <b>brincan</b> y cuesta ver cuál túnel es el más largo.", alerta=True)
        else:
            nota("¡El riel va suavecito! Ves de un vistazo <b>cuál túnel es el más largo</b>.")
    widget_recomendado(
        "Dropdown",
        "Un menú desplegable permite probar distintos órdenes del mismo gráfico y comparar cuál "
        "genera una lectura continua.",
        """from ipywidgets import interact, Dropdown

@interact(orden=Dropdown(options=['Alfabético', 'Descendente', 'Ascendente'],
                         value='Alfabético', description='Orden'))
def tuneles(orden):
    datos = ordenar(TUNELES, orden)
    dibujar_barras_h(datos)""",
        'st.selectbox("Orden de los túneles", ["Alfabético", "Descendente", "Ascendente"])',
    )


# ---------------------------------------------------------------------------
# 4 · Semejanza
# ---------------------------------------------------------------------------
def _muestras_vetas():
    rnd = random.Random(11)
    rangos = {"Diamante": (4, 18, 1, 4), "Oro": (14, 34, 2, 7), "Hierro": (24, 62, 4, 10)}
    return [(mineral, rnd.uniform(c0, c1), rnd.uniform(t0, t1))
            for mineral, (c0, c1, t0, t1) in rangos.items() for _ in range(14)]


VETAS = _muestras_vetas()


def dispersion_svg(modo, resaltado, color_resaltado):
    s, izq, arr, w, h = 12, 56, 16, 480, 288
    cuerpo = [f'<rect x="{izq}" y="{arr}" width="{w}" height="{h}" fill="#1c1c1c"/>']
    for v in range(0, 65, 16):
        x = izq + v / 64 * w
        cuerpo.append(f'<rect x="{x:.0f}" y="{arr}" width="1" height="{h}" fill="#333"/>')
        cuerpo.append(texto(x, arr + h + 20, v, "#cfcfcf", 18, "middle"))
    for v in range(0, 11, 2):
        y = arr + h - v / 10 * h
        cuerpo.append(f'<rect x="{izq}" y="{y:.0f}" width="{w}" height="1" fill="#333"/>')
        cuerpo.append(texto(izq - 8, y + 5, v, "#cfcfcf", 18, "end"))
    cuerpo.append(texto(izq + w / 2, arr + h + 42, "¿Qué tan profundo está? →", "#e6e6e6", 20, "middle"))
    cuerpo.append(f'<text transform="translate(18 {arr + h / 2}) rotate(-90)" fill="#e6e6e6" font-size="20" '
                  f'font-family="{TEXTO}" text-anchor="middle">Tamaño del mineral</text>')
    puntos = sorted(VETAS, key=lambda v: v[0] == resaltado)  # el resaltado al frente
    for mineral, capa, tam in puntos:
        x = izq + round(capa / 64 * w / s) * s - s / 2
        y = arr + h - round(tam / 10 * h / s) * s - s / 2
        if modo == "Todos grises":
            color = "#9E9E9E"
        elif modo == "Un color por mineral":
            color = COLOR_MINERAL[mineral]
        else:
            color = color_resaltado if mineral == resaltado else "#4d4d4d"
        cuerpo.append(bloque(x, y, s, color))
    return svg(izq + w + 16, arr + h + 52, "".join(cuerpo), C["cueva"])


def seccion_semejanza():
    encabezado(4, "Semejanza", "Lo que se parece, parece familia.", "ColorPicker")
    izq, der = st.columns([1, 1.25], gap="large")
    with izq:
        teoria(
            "Las cosas que tienen el <b>mismo color</b> o la misma forma parecen de la misma familia, "
            "aunque estén separadas.",
            "En las gráficas cada grupo tiene <b>su propio color</b>. Y si quieres que algo resalte, píntalo "
            "de un color diferente a todo lo demás.",
            "Primero mira los bloques grises. Luego dale un color a cada mineral. Al final elige un mineral "
            "y ¡píntalo de tu color favorito!",
        )
    with der:
        modo = st.radio("¿Cómo pintamos los bloques?", ["Todos grises", "Un color por mineral", "Resaltar uno"],
                        horizontal=True)
        a, b = st.columns(2)
        resaltado = a.selectbox("¿Qué mineral resaltamos?", list(COLOR_MINERAL), index=2,
                                disabled=modo != "Resaltar uno")
        color = b.color_picker("🎨 Tu color", C["redstone"], disabled=modo != "Resaltar uno")
        lienzo(dispersion_svg(modo, resaltado if modo == "Resaltar uno" else None, color))
        mensajes = {
            "Todos grises": ("Todo gris parece <b>un solo montón</b> de bloques.", True),
            "Un color por mineral": ("¡Aparecen <b>3 familias</b>! Y mira: el diamante está muy profundo.", False),
            "Resaltar uno": (f"Lo demás queda apagado y el <b>{resaltado.lower()}</b> brilla. ¡Lo encuentras al instante!", False),
        }
        nota(*mensajes[modo])
    widget_recomendado(
        "ColorPicker",
        "Elegir el color en vivo demuestra que la semejanza cromática crea grupos y que un único color "
        "distinto basta para resaltar una categoría.",
        """from ipywidgets import interact, ColorPicker, Dropdown

@interact(mineral=Dropdown(options=['Hierro', 'Oro', 'Diamante'], value='Diamante'),
          color=ColorPicker(value='#C0261F', description='Resaltar'))
def vetas(mineral, color):
    dibujar_dispersion(resaltar=mineral, color=color)""",
        'st.color_picker("Color de resaltado", "#C0261F")',
    )


# ---------------------------------------------------------------------------
# 5 · Figura y fondo
# ---------------------------------------------------------------------------
MINAS = ["Mina Norte", "Mina Sur", "Mina Roca", "Mina Lava", "Mina Hielo", "Mina Musgo", "Mina Eco"]


def _series_minas():
    rnd, series = random.Random(21), {}
    for nombre in MINAS:
        v, valores = rnd.uniform(18, 42), []
        for _ in range(12):
            v = min(58, max(4, v + rnd.uniform(-7, 7)))
            valores.append(v)
        series[nombre] = valores
    return series


SERIES = _series_minas()


def lineas_svg(foco, opacidad, noche):
    izq, arr, w, h = 48, 18, 500, 280
    fondo = C["noche"] if noche else C["cielo"]
    tinta = "#cfd6e6" if noche else "#1d2b4a"
    contexto = "#9aa3b5" if noche else "#4a5368"
    color_foco = C["oro"] if noche else C["redstone"]
    paso = w / 11

    def ruta(valores):
        pts = []
        for i, v in enumerate(valores):
            x, y = izq + i * paso, arr + h - v / 60 * h
            if pts:
                pts.append(f"{x:.0f},{pts[-1].split(',')[1]}")
            pts.append(f"{x:.0f},{y:.0f}")
        return " ".join(pts)

    cuerpo = []
    for v in range(0, 61, 20):
        y = arr + h - v / 60 * h
        cuerpo.append(f'<rect x="{izq}" y="{y:.0f}" width="{w}" height="1" fill="{tinta}" opacity=".18"/>')
        cuerpo.append(texto(izq - 8, y + 5, v, tinta, 17, "end"))
    for i in range(0, 12, 2):
        cuerpo.append(texto(izq + i * paso, arr + h + 22, f"S{i+1}", tinta, 17, "middle"))
    for nombre, valores in SERIES.items():
        if nombre != foco:
            cuerpo.append(f'<polyline points="{ruta(valores)}" fill="none" stroke="{contexto}" '
                          f'stroke-width="3" opacity="{opacidad:.2f}"/>')
    valores = SERIES[foco]
    cuerpo.append(f'<polyline points="{ruta(valores)}" fill="none" stroke="#000" stroke-width="9"/>')
    cuerpo.append(f'<polyline points="{ruta(valores)}" fill="none" stroke="{color_foco}" stroke-width="5"/>')
    xf, yf = izq + 11 * paso, arr + h - valores[-1] / 60 * h
    cuerpo.append(bloque(xf - 7, yf - 7, 14, color_foco))
    cuerpo.append(texto(xf + 12, yf + 6, foco, color_foco, 20))
    return svg(izq + w + 140, arr + h + 34, "".join(cuerpo), fondo)


def seccion_figura_fondo():
    encabezado(5, "Figura y fondo", "Lo importante adelante, lo demás atrás.", "FloatSlider")
    izq, der = st.columns([1, 1.25], gap="large")
    with izq:
        teoria(
            "Tu cerebro separa lo <b>importante</b> (la figura) de lo que está atrás (el fondo). Como cuando "
            "buscas a tu amigo en una foto llena de gente.",
            "Para que algo resalte en una gráfica, píntalo con un <b>color fuerte</b> y deja lo demás en "
            "<b>gris clarito</b>.",
            "Sube la barra hasta el máximo. ¿Todavía encuentras tu mina? Luego bájala y prueba el modo cueva.",
        )
    with der:
        a, b = st.columns([1.3, 1])
        foco = a.selectbox("¿Qué mina quieres ver?", MINAS, index=3)
        b.write("")
        noche = b.toggle("Modo cueva", value=False)
        opacidad = st.slider("👀 ¿Qué tanto se ven las otras minas?", 0.05, 1.0, 0.25, step=0.05)
        lienzo(lineas_svg(foco, opacidad, noche))
        if opacidad >= 0.8:
            nota("¡Las otras minas tapan la tuya! La figura <b>se perdió en el fondo</b>.", alerta=True)
        else:
            nota(f"¡Ahí está <b>{foco}</b>! Resalta y las demás minas se quedan atrás.")
    widget_recomendado(
        "FloatSlider",
        "Un deslizador decimal controla de forma continua la opacidad del contexto y muestra en qué "
        "punto la figura se separa del fondo.",
        """from ipywidgets import interact, FloatSlider, Dropdown

@interact(mina=Dropdown(options=MINAS, value='Mina Lava'),
          opacidad=FloatSlider(value=0.25, min=0.05, max=1.0, step=0.05,
                               description='Fondo'))
def produccion(mina, opacidad):
    dibujar_lineas(foco=mina, alpha_contexto=opacidad)""",
        'st.slider("Opacidad del fondo", 0.05, 1.0, 0.25, step=0.05)',
    )


# ---------------------------------------------------------------------------
# 6 · Dirección común
# ---------------------------------------------------------------------------
ANIMACION = """
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<div style="border:4px solid #000;background:#1b1b1b;line-height:0">
  <canvas id="c" width="640" height="300" style="width:100%;image-rendering:pixelated"></canvas>
</div>
<button id="b" style="margin-top:8px;font-family:'Press Start 2P',monospace;font-size:10px;padding:9px 12px;
  background:#8B8B8B;color:#1b1b1b;border:3px solid;border-color:#fff #373737 #373737 #fff;cursor:pointer">⏸ PAUSA</button>
<script>
const P = __PARAMS__;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const W = cv.width, H = cv.height, S = 16;
let semilla = 42;
const rnd = () => { semilla = (semilla * 16807) % 2147483647; return semilla / 2147483647; };
const indices = [...Array(P.total).keys()].sort(() => rnd() - 0.5);
const manada = new Set(indices.slice(0, P.manada));
const dir = -0.35;
const bloques = [...Array(P.total)].map((_, i) => ({x: rnd() * W, y: rnd() * H, a: rnd() * Math.PI * 2, g: manada.has(i)}));
function dibujar(b) {
  const x = Math.round(b.x / 4) * 4, y = Math.round(b.y / 4) * 4;
  ctx.fillStyle = (P.colorear && b.g) ? '#2BD46B' : '#9E9E9E'; ctx.fillRect(x, y, S, S);
  ctx.fillStyle = 'rgba(255,255,255,.30)'; ctx.fillRect(x, y, S, 3); ctx.fillRect(x, y, 3, S);
  ctx.fillStyle = 'rgba(0,0,0,.35)'; ctx.fillRect(x, y + S - 3, S, 3); ctx.fillRect(x + S - 3, y, 3, S);
}
let pausa = false, t = 0;
document.getElementById('b').onclick = e => { pausa = !pausa; e.target.textContent = pausa ? '▶ JUGAR' : '⏸ PAUSA'; };
function paso() {
  if (!pausa && (t++ % 2 === 0)) {
    ctx.fillStyle = '#1b1b1b'; ctx.fillRect(0, 0, W, H);
    for (const b of bloques) {
      if (!b.g) b.a += (rnd() - 0.5) * 0.9;
      const ang = b.g ? dir : b.a;
      b.x = (b.x + P.vel * Math.cos(ang) + W + S) % (W + S) - S / 2;
      b.y = (b.y + P.vel * Math.sin(ang) + H + S) % (H + S) - S / 2;
      dibujar(b);
    }
  }
  requestAnimationFrame(paso);
}
paso();
</script>
"""

ALDEAS = {"Aldea Roble": (32, 18), "Aldea Arena": (12, 27), "Aldea Pino": (26, 35), "Aldea Nieve": (6, 14),
          "Aldea Río": (20, 10), "Aldea Cueva": (36, 23), "Aldea Colina": (16, 31), "Aldea Bahía": (9, 4)}


def pendiente_svg(colorear):
    x1, x2, arr, h = 200, 420, 34, 260
    cuerpo = [texto(x1, 20, "2025", "#e6e6e6", 22, "middle"), texto(x2, 20, "2026", "#e6e6e6", 22, "middle"),
              f'<rect x="{x1 - 1}" y="{arr}" width="3" height="{h}" fill="#444"/>',
              f'<rect x="{x2 - 1}" y="{arr}" width="3" height="{h}" fill="#444"/>']
    y = lambda v: arr + h - v / 40 * h
    for nombre, (a, b) in ALDEAS.items():
        color = (C["esmeralda"] if b > a else C["redstone"]) if colorear else "#9E9E9E"
        cuerpo.append(f'<line x1="{x1}" y1="{y(a):.0f}" x2="{x2}" y2="{y(b):.0f}" stroke="{color}" '
                      f'stroke-width="4" shape-rendering="auto"/>')
        cuerpo += [bloque(x1 - 6, y(a) - 6, 12, color), bloque(x2 - 6, y(b) - 6, 12, color)]
        cuerpo.append(texto(x1 - 14, y(a) + 6, f"{nombre} {a}", "#e6e6e6", 18, "end"))
        cuerpo.append(texto(x2 + 14, y(b) + 6, f"{b}", "#e6e6e6", 18))
    return svg(480, arr + h + 16, "".join(cuerpo), C["cueva"])


def seccion_direccion_comun():
    encabezado(6, "Dirección común", "Lo que avanza junto es un grupo.", "Play")
    izq, der = st.columns([1, 1.25], gap="large")
    with izq:
        teoria(
            "Cuando varias cosas se mueven <b>hacia el mismo lado</b>, tu cerebro piensa que van juntas. "
            "Como una parvada de pájaros volando.",
            "En una gráfica de líneas, las que <b>suben</b> parecen un grupo y las que <b>bajan</b> parecen "
            "otro. ¡Sin leer ningún número!",
            "Mira la animación: todos los bloques son iguales. ¿Encuentras al grupo que viaja junto? Si no, "
            "píntalo de verde.",
        )
    with der:
        a, b = st.columns(2)
        manada = a.slider("¿Cuántos bloques viajan juntos?", 3, 20, 10)
        vel = b.slider("Velocidad", 1, 5, 2)
        colorear = st.checkbox("Pintar de verde al grupo", value=False)
        params = json.dumps({"total": 40, "manada": manada, "vel": vel, "colorear": colorear})
        components.html(ANIMACION.replace("__PARAMS__", params), height=300)
        nota("Todos los bloques son <b>iguales</b>. Descubres al grupo solo porque <b>se mueven hacia el mismo lado</b>.")
        st.markdown("**¿Cuántas esmeraldas juntó cada aldea? · 2025 → 2026**")
        color_dir = st.checkbox("Pintar: verde si subió, rojo si bajó", value=False)
        lienzo(pendiente_svg(color_dir))
        nota("Aunque todo esté gris, ves dos grupos: las líneas que <b>suben</b> y las que <b>bajan</b>.")
    widget_recomendado(
        "Play",
        "Play anima un valor paso a paso. Enlazado a un deslizador con jslink, mueve los elementos en el "
        "tiempo y hace visible la dirección común.",
        """from ipywidgets import Play, IntSlider, jslink, HBox, interactive_output
from IPython.display import display

play = Play(value=0, min=0, max=100, step=1, interval=80, description='▶')
tick = IntSlider(min=0, max=100, description='Tick')
jslink((play, 'value'), (tick, 'value'))

salida = interactive_output(dibujar_cuadro, {'t': tick})   # dibuja el cuadro t
display(HBox([play, tick]), salida)""",
        "components.html(animación JS) + st.slider para velocidad y tamaño de la manada",
    )


# ---------------------------------------------------------------------------
# 7 · Simetría
# ---------------------------------------------------------------------------
RECURSOS = {"Madera": (12, 2), "Piedra": (6, 11), "Carbón": (4, 9),
            "Hierro": (3, 8), "Oro": (1, 4), "Diamante": (0, 3)}
COLOR_MUNDOS = ("#5D9C3B", "#7E6BB0")


def mariposa_svg(espejo):
    s, arr, fila = 14, 40, 26
    cuerpo = []
    if espejo:
        centro, etiqueta = 280, 110
        xi, xd = centro - etiqueta / 2, centro + etiqueta / 2
        cuerpo += [texto(xi - 4, 24, "◀ SUPERFICIE", COLOR_MUNDOS[0], 20, "end"),
                   texto(xd + 4, 24, "CAVERNAS ▶", "#b9a9e8", 20)]
        for i, (nombre, (a, b)) in enumerate(RECURSOS.items()):
            y = arr + i * fila
            cuerpo.append(texto(centro, y + s - 1, nombre, "#e6e6e6", 19, "middle"))
            cuerpo += [bloque(xi - 4 - (k + 1) * s, y, s, COLOR_MUNDOS[0]) for k in range(a)]
            cuerpo += [bloque(xd + 4 + k * s, y, s, COLOR_MUNDOS[1]) for k in range(b)]
        ancho = 560
    else:
        izq = 96
        cuerpo += [texto(izq, 24, "■ SUPERFICIE", COLOR_MUNDOS[0], 20),
                   texto(izq + 140, 24, "■ CAVERNAS", "#b9a9e8", 20)]
        for i, (nombre, (a, b)) in enumerate(RECURSOS.items()):
            y = arr + i * fila
            cuerpo.append(texto(izq - 8, y + s - 1, nombre, "#e6e6e6", 19, "end"))
            cuerpo += [bloque(izq + k * 9, y, 9, COLOR_MUNDOS[0]) for k in range(a)]
            cuerpo += [bloque(izq + k * 9, y + 10, 9, COLOR_MUNDOS[1]) for k in range(b)]
        ancho = 560
    return svg(ancho, arr + len(RECURSOS) * fila + 16, "".join(cuerpo), C["cueva"])


def seccion_simetria():
    encabezado(7, "Simetría", "Igual de los dos lados se ve ordenado.", "ToggleButton")
    izq, der = st.columns([1, 1.25], gap="large")
    with izq:
        teoria(
            "Cuando algo es <b>igual de los dos lados</b>, como una mariposa, tu cerebro lo ve como una sola "
            "figura bien ordenada.",
            "Si pones dos grupos <b>uno frente al otro</b> con una línea en medio, es facilísimo "
            "compararlos. ¡Como un espejo!",
            "Prende y apaga el espejo. ¿Qué mundo tiene más madera? ¿Y cuál tiene más minerales?",
        )
    with der:
        espejo = st.toggle("Modo espejo", value=True)
        lienzo(mariposa_svg(espejo))
        if espejo:
            nota("Con el espejo, cada mundo forma <b>su propia figura</b> y comparas todo de un vistazo.")
        else:
            nota("Sin espejo tienes que leer <b>fila por fila</b>. ¡Cuesta más trabajo!", alerta=True)
    widget_recomendado(
        "ToggleButton",
        "Un interruptor de dos estados alterna entre la vista simétrica y la asimétrica para comparar el "
        "efecto del eje central sobre los mismos datos.",
        """from ipywidgets import interact, ToggleButton

@interact(espejo=ToggleButton(value=True, description='Vista en espejo',
                              icon='exchange'))
def recursos(espejo):
    dibujar_mariposa(espejo)""",
        'st.toggle("Vista en espejo", value=True)',
    )


# ---------------------------------------------------------------------------
# Navegación (barra lateral)
# ---------------------------------------------------------------------------
secciones = {
    "🏠 Inicio": inicio,
    "1. Cierre": seccion_cierre,
    "2. Proximidad": seccion_proximidad,
    "3. Continuidad": seccion_continuidad,
    "4. Semejanza": seccion_semejanza,
    "5. Figura y fondo": seccion_figura_fondo,
    "6. Dirección común": seccion_direccion_comun,
    "7. Simetría": seccion_simetria,
}

st.sidebar.title("UL Tablero 2026")
st.sidebar.markdown("**Principios de la Gestalt** · elige un bloque:")
seleccion = st.sidebar.radio("Navegación", list(secciones), label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("Ejemplo sobre cómo utilizar widgets en los tableros.")

secciones[seleccion]()

st.markdown(
    '<div class="pie">Referencias: '
    '<a href="https://www.plainconcepts.com/es/visualizacion-datos-guia-ejemplos/" target="_blank">'
    "Plain Concepts · Visualización de datos</a> · "
    '<a href="https://pypi.org/project/ipywidgets/" target="_blank">ipywidgets en PyPI</a></div>',
    unsafe_allow_html=True,
)
