import streamlit as st

# Configuración básica de la página
st.set_page_config(
    page_title="UL Tablero 2026",
    page_icon="📊",
    layout="wide"
)

# --- Definición de los Placeholders para las 7 Actividades ---

def actividad_1():
    st.header("Actividad 1: [Título de la Actividad 1]")
    st.info("Espacio reservado para el desarrollo de la Actividad 1.")
    # Ejemplo de widget placeholder
    st.slider("Widget de prueba 1", 0, 100, 50)

def actividad_2():
    st.header("Actividad 2: [Título de la Actividad 2]")
    st.info("Espacio reservado para el desarrollo de la Actividad 2.")
    st.text_input("Widget de prueba 2", placeholder="Escribe algo aquí...")

def actividad_3():
    st.header("Actividad 3: [Título de la Actividad 3]")
    st.info("Espacio reservado para el desarrollo de la Actividad 3.")
    st.checkbox("Widget de prueba 3")

def actividad_4():
    st.header("Actividad 4: [Título de la Actividad 4]")
    st.info("Espacio reservado para el desarrollo de la Actividad 4.")
    st.selectbox("Widget de prueba 4", ["Opción A", "Opción B", "Opción C"])

def actividad_5():
    st.header("Actividad 5: [Título de la Actividad 5]")
    st.info("Espacio reservado para el desarrollo de la Actividad 5.")
    st.date_input("Widget de prueba 5")

def actividad_6():
    st.header("Actividad 6: [Título de la Actividad 6]")
    st.info("Espacio reservado para el desarrollo de la Actividad 6.")
    st.number_input("Widget de prueba 6", min_value=0, max_value=50, value=10)

def actividad_7():
    st.header("Actividad 7: [Título de la Actividad 7]")
    st.info("Espacio reservado para el desarrollo de la Actividad 7.")
    st.color_picker("Widget de prueba 7", "#00f900")


# --- Panel de Control Izquierdo (Sidebar) ---

st.sidebar.title("UL Tablero 2026")
st.sidebar.markdown("Selecciona una actividad:")

# Diccionario que vincula el nombre en el menú con su función
actividades = {
    "1. Actividad 1": actividad_1,
    "2. Actividad 2": actividad_2,
    "3. Actividad 3": actividad_3,
    "4. Actividad 4": actividad_4,
    "5. Actividad 5": actividad_5,
    "6. Actividad 6": actividad_6,
    "7. Actividad 7": actividad_7,
}

# Widget de navegación en el panel izquierdo
seleccion = st.sidebar.radio("Navegación", list(actividades.keys()), label_visibility="collapsed")

st.sidebar.divider()
st.sidebar.caption("Ejemplo sobre cómo utilizar Widgets en los tableros.")

# --- Renderizado de la Actividad Seleccionada ---
actividades[seleccion]()
