import streamlit as st

# Configuración de la página web (Título en la pestaña del navegador)
st.set_page_config(page_title="LegalTech - Extractor de Fallos", page_icon="🏛️", layout="centered")

# Título principal en el centro de la pantalla
st.title("🏛️ Analizador Inteligente de Jurisprudencia (PJN)")
st.write("Automatización jurídica y jurimetría aplicada para el derecho argentino.")
st.markdown("---")

# Creamos las dos opciones en pestañas centrales y grandes
pestaña_pdf, pestaña_buscar = st.tabs([
    "📂 Opción A: Subir Fallo en PDF",
    "🔍 Opción B: Buscar Fallo por Nombre"
])

# --- CONTENIDO DE LA OPCIÓN A ---
with pestaña_pdf:
    st.header("Cargar un documento nuevo")
    st.write(
        "Arrastrá o seleccioná el PDF del fallo que descargaste del PJN para que la IA extraiga los hechos y la división de votos.")

    # Caja para arrastrar el archivo
    archivo_subido = st.file_uploader("Seleccionar archivo PDF", type=["pdf"])

    # Botón de acción
    if st.button("🚀 Analizar PDF con IA"):
        if archivo_subido is not None:
            st.info(f"Procesando el archivo: {archivo_subido.name}...")
            # Acá conectaremos la lógica de pdfplumber y Gemini próximamente
        else:
            st.warning("Por favor, primero subí un archivo PDF válido.")

# --- CONTENIDO DE LA OPCIÓN B ---
with pestaña_buscar:
    st.header("Buscar en el archivo histórico")
    st.write(
        "Ingresá las partes o el nombre clave del fallo (ej: 'Badaro') para recuperar su análisis si ya fue procesado.")

    # Formulario de texto
    nombre_fallo = st.text_input("Nombre de la carátula o palabras clave:")

    # Botón de acción
    if st.button("🔍 Buscar Fallo"):
        if nombre_fallo.strip() != "":
            st.info(f"Buscando '{nombre_fallo}' en la base de datos local...")
            # Acá conectaremos la lectura del Excel/CSV en data/processed próximamente
        else:
            st.warning("Por favor, escribí un nombre para iniciar la búsqueda.")
