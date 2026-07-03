import os
import pdfplumber
import streamlit as st
from google import genai
from dotenv import load_dotenv

# 1. Configuración de la página web
st.set_page_config(page_title="LegalTech - Extractor de Fallos", page_icon="🏛️", layout="centered")

# Cargar variables de entorno ocultas (.env) para la API Key
RUTA_DE_RAIZ = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(RUTA_DE_RAIZ, ".env"))

# Inicializar el cliente de Gemini de forma segura
try:
    client = genai.Client()
except Exception:
    client = None


def analizar_con_ia(texto_completo):
    """Envía el fragmento del fallo a Gemini con el prompt jurídico."""
    if not client:
        return "❌ Error: No se pudo inicializar el cliente de IA. Verifica tu archivo .env"

    texto_recortado = texto_completo[:15000]
    prompt = f"""
    Actúa como un experto en derecho argentino y jurimetría. Analiza el siguiente fragmento de un fallo judicial y extrae estrictamente la siguiente información de forma clara y profesional:

    1. RESUMEN DE LOS HECHOS: (Explica brevemente qué originó el conflicto o reclamo en un párrafo de máximo 4 líneas).
    2. VOTO MAYORITARIO: (Indica qué resolvió la mayoría del tribunal y, si se menciona, qué jueces lo integraron o lideraron).
    3. VOTO MINORITARIO O DISIDENCIA: (Indica si hubo voto en disidencia, qué juez lo sostuvo y cuál era su postura. Si no hubo disidencia, escribe 'No registra disidencia').

    Texto del fallo:
    \"\"\"{texto_recortado}\"\"\"
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"❌ Error al conectar con Gemini: {str(e)}"


# 2. Interfaz Gráfica (UI)
st.title("🏛️ Analizador Inteligente de Jurisprudencia (PJN)")
st.write("Automatización jurídica y jurimetría aplicada para el derecho argentino.")
st.markdown("---")

# Pestañas centrales
pestaña_pdf, pestaña_buscar = st.tabs([
    "📂 Opción A: Subir Fallo en PDF",
    "🔍 Opción B: Buscar Fallo por Nombre"
])

# --- CONTENIDO DE LA OPCIÓN A ---
with pestaña_pdf:
    st.header("Cargar un documento nuevo")
    st.write("Arrastrá o seleccioná el PDF del fallo que descargaste del PJN para procesarlo al instante.")

    archivo_subido = st.file_uploader("Seleccionar archivo PDF", type=["pdf"])

    if st.button("🚀 Analizar PDF con IA"):
        if archivo_subido is not None:
            # Spinner animado mientras la IA procesa el documento
            with st.spinner("🧠 Leyendo PDF y analizando con Inteligencia Artificial..."):
                try:
                    # pdfplumber puede leer directamente el archivo subido en memoria por Streamlit
                    texto_fallo = ""
                    with pdfplumber.open(archivo_subido) as pdf:
                        for pagina in pdf.pages:
                            texto_fallo += pagina.extract_text() or ""

                    if texto_fallo.strip():
                        # Llamamos a Gemini
                        analisis_juridico = analizar_con_ia(texto_fallo)

                        # Mostramos el resultado en un cuadro elegante en la pantalla
                        st.success("✅ ¡Análisis Completado!")
                        st.markdown("### 🏛️ Resultado del Análisis")
                        st.info(analisis_juridico)
                    else:
                        st.error("⚠️ No se pudo extraer texto del PDF. Verifica que no sea una imagen escaneada.")
                except Exception as e:
                    st.error(f"❌ Ocurrió un error al procesar el archivo: {str(e)}")
        else:
            st.warning("Por favor, primero subí un archivo PDF válido.")

# --- CONTENIDO DE LA OPCIÓN B ---
with pestaña_buscar:
    st.header("Buscar en el archivo histórico")
    st.write("Ingresá las partes o el nombre clave del fallo para recuperar su análisis.")

    nombre_fallo = st.text_input("Nombre de la carátula o palabras clave:")

    if st.button("🔍 Buscar Fallo"):
        if nombre_fallo.strip() != "":
            st.info(f"Buscando '{nombre_fallo}' en la base de datos local... (Próxima fase)")
        else:
            st.warning("Por favor, escribí un nombre para iniciar la búsqueda.")

