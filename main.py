import os
import pdfplumber
import streamlit as st
import pandas as pd
from google import genai
from dotenv import load_dotenv

st.set_page_config(page_title="LegalTech - Extractor de Fallos", page_icon="🏛️", layout="centered")

# --- FUNCIÓN PARA INYECTAR CSS DESDE UN ARCHIVO APARTE ---
def cargar_css(ruta_css):
    if os.path.exists(ruta_css):
        with open(ruta_css, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Cargar estilos de forma automática
RUTA_DE_RAIZ = os.path.dirname(os.path.abspath(__file__))
cargar_css(os.path.join(RUTA_DE_RAIZ, "static", "styles.css"))


# 1. Configuración de la página web (Diseño centralizado)
st.set_page_config(page_title="LegalTech - Extractor de Fallos", page_icon="🏛️", layout="centered")

# Cargar variables de entorno ocultas (.env)
RUTA_DE_RAIZ = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(RUTA_DE_RAIZ, ".env"))

# Rutas para el historial local
CARPETA_PROCESSED = os.path.join(RUTA_DE_RAIZ, "data", "processed")
ARCHIVO_BD = os.path.join(CARPETA_PROCESSED, "base_conocimiento_fallos.csv")

# Inicializar el cliente de Gemini de forma segura
try:
    client = genai.Client()
except Exception:
    client = None


def guardar_en_base_local(nombre_archivo, analisis_texto):
    """Guarda el análisis del fallo en un archivo CSV local como base de datos."""
    os.makedirs(CARPETA_PROCESSED, exist_ok=True)

    nuevo_registro = {
        "Archivo": nombre_archivo,
        "Analisis": analisis_texto
    }

    if os.path.exists(ARCHIVO_BD):
        df = pd.read_csv(ARCHIVO_BD)
        # Evitar duplicados si se procesa el mismo archivo
        df = df[df["Archivo"] != nombre_archivo]
        df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
    else:
        df = pd.DataFrame([nuevo_registro])

    df.to_csv(ARCHIVO_BD, index=False, encoding="utf-8-sig")


def analizar_con_ia(texto_completo):
    """Envía el fragmento del fallo a Gemini con el prompt jurídico abstracto universal."""
    if not client:
        return "❌ Error: No se pudo inicializar el cliente de IA. Verifica tu archivo .env"

    texto_recortado = texto_completo[:15000]
    prompt = f"""
    Actúa como un prestigioso experto en derecho argentino, técnica legislativa y jurimetría. 
    Analiza el siguiente fragmento de una sentencia judicial y extrae estrictamente la siguiente información estructurada de forma clara, técnica y objetiva, adaptándote al fuero del caso:

    1. RESUMEN DE LOS HECHOS Y OBJETO: (Explica brevemente qué situación originó el conflicto y qué pretensión concreta se reclama en un párrafo de máximo 4 líneas).
    2. FUNDAMENTOS JURÍDICOS DEL VOTO MAYORITARIO: (Indica los argumentos legales del voto que hace mayoría. Menciona las normas, códigos, leyes, decretos o artículos constitucionales clave en los que se basaron para decidir).
    3. DISIDENCIAS / VOTOS MINORITARIOS: (Si existieron votos en disidencia, explica brevemente quién los sostuvo y cuál era su postura legal. Si el fallo fue por unanimidad, escribe 'Decidido por unanimidad / No registra disidencia').
    4. PARTE DISPOSITIVA (RESOLUCIÓN): (Resume de forma directa qué ordena, prohíbe, declara o resuelve el tribunal en su decisión final respecto a las partes).
    5. PRECEDENTE / DOCTRINA LEGAL: (Identifica el principio jurídico abstracto o la regla general que este fallo establece como precedente para futuros casos similares en una sola frase contundente).

    Texto del fallo:
    \"\"\"{texto_recortado}\"\"\"
    """
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text
    except Exception as e:
        return f"❌ Error al conectar con Gemini: {str(e)}"


# 2. Interfaz Gráfica de Usuario (UI central)
st.title("🏛️ Analizador Inteligente de Jurisprudencia (PJN)")
st.write("Automatización jurídica y jurimetría aplicada para el derecho argentino.")
st.markdown("---")

pestaña_pdf, pestaña_buscar = st.tabs([
    "📂 Opción A: Subir Fallo en PDF",
    "🔍 Opción B: Buscar / Consultar Fallo"
])

# --- CONTENIDO DE LA OPCIÓN A (SUBIR PDF) ---
with pestaña_pdf:
    st.header("Cargar un documento nuevo")
    st.write("Arrastrá o seleccioná el PDF del fallo para procesarlo con IA y guardarlo en el historial.")

    archivo_subido = st.file_uploader("Seleccionar archivo PDF", type=["pdf"])

    if st.button("🚀 Analizar PDF con IA"):
        if archivo_subido is not None:
            with st.spinner("🧠 Analizando con Inteligencia Artificial..."):
                try:
                    texto_fallo = ""
                    with pdfplumber.open(archivo_subido) as pdf:
                        for pagina in pdf.pages:
                            texto_fallo += pagina.extract_text() or ""

                    if texto_fallo.strip():
                        analisis_juridico = analizar_con_ia(texto_fallo)
                        guardar_en_base_local(archivo_subido.name, analisis_juridico)

                        st.success("✅ ¡Análisis Completado y Guardado en la Base de Datos!")
                        st.markdown("### 🏛️ Resultado del Análisis")
                        st.info(analisis_juridico)
                    else:
                        st.error("⚠️ No se pudo extraer texto del PDF.")
                except Exception as e:
                    st.error(f"❌ Ocurrió un error: {str(e)}")
        else:
            st.warning("Por favor, primero subí un archivo PDF válido.")

# --- CONTENIDO DE LA OPCIÓN B (BUSCAR / CONSULTAR CON RESPALDO DE IA) ---
with pestaña_buscar:
    st.header("Buscar o Consultar un Fallo")
    st.write(
        "Ingresá el nombre del fallo (ej: 'Aquino' o 'Badaro'). Si no está en tu base local, la IA lo investigará al instante.")

    nombre_fallo = st.text_input("Nombre del fallo o carátula a consultar:")

    if st.button("🔍 Buscar / Consultar Fallo"):
        if nombre_fallo.strip() != "":
            encontrado_local = False

            # 1. Intentar buscar primero en el archivo CSV local
            if os.path.exists(ARCHIVO_BD):
                df_bd = pd.read_csv(ARCHIVO_BD)
                coincidencias = df_bd[
                    df_bd["Archivo"].str.contains(nombre_fallo, case=False, na=False) |
                    df_bd["Analisis"].str.contains(nombre_fallo, case=False, na=False)
                    ]

                if not coincidencias.empty:
                    encontrado_local = True
                    st.success(f"🎉 ¡Recuperado de la base de conocimiento local!")
                    for index, fila in coincidencias.iterrows():
                        with st.expander(f"📄 Historial: {fila['Archivo']}"):
                            st.markdown("### 🏛️ Análisis Histórico Recuperado")
                            st.info(fila["Analisis"])

            # 2. Si no existe en el CSV local, Gemini actúa como oráculo histórico
            if not encontrado_local:
                with st.spinner(
                        f"🧠 El fallo '{nombre_fallo}' no está en el historial. Consultando jurisprudencia histórica con IA..."):

                    prompt_consulta = f"""
                    Actúa como un prestigioso experto en derecho argentino e historia judicial.
                    Identifica y analiza el célebre fallo judicial de la jurisprudencia argentina conocido como: "{nombre_fallo}".
                    Extrae estrictamente la siguiente información estructurada de forma clara, técnica y objetiva (si es un fallo muy específico o no posees registro exacto, redacta una aproximación basada en la doctrina que lleva ese nombre):

                    1. RESUMEN DE LOS HECHOS Y OBJETO: (Explica brevemente qué situación originó el conflicto y qué pretensión concreta se reclamaba en un párrafo de máximo 4 líneas).
                    2. FUNDAMENTOS JURÍDICOS DEL VOTO MAYORITARIO: (Indica los argumentos legales del voto que hizo mayoría. Menciona las normas, códigos, leyes o artículos constitucionales clave en los que se basaron).
                    3. DISIDENCIAS / VOTOS MINORITARIOS: (Explica brevemente quién los sostuvo y cuál era su postura legal. Si fue unánime, acláralo).
                    4. PARTE DISPOSITIVA (RESOLUCIÓN): (Qué ordenó o resolvió finalmente el tribunal).
                    5. PRECEDENTE / DOCTRINA LEGAL: (Identifica el principio jurídico abstracto o la regla general que este fallo estableció como precedente en una sola frase contundente).
                    """

                    try:
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_consulta)
                        analisis_resultado = response.text

                        # Guardamos automáticamente en la base local para consultas futuras
                        guardar_en_base_local(f"Consulta_IA_{nombre_fallo.replace(' ', '_')}.pdf", analisis_resultado)

                        st.success(f"✅ ¡Análisis generado con éxito mediante Inteligencia Jurisprudencial!")
                        st.markdown(f"### 🏛️ Resultado para: {nombre_fallo}")
                        st.info(analisis_resultado)

                    except Exception as e:
                        st.error(f"❌ Ocurrió un error al consultar con la IA: {str(e)}")
        else:
            st.warning("Por favor, escribí un nombre para iniciar la búsqueda.")

st.caption("🔒 **Aviso de Privacidad:** Este sistema procesa los documentos de forma segura a través de la API de Google Gemini en modo de desarrollo. Las sentencias reales con datos sensibles deben ser anonimizadas previamente conforme a la Ley N° 25.326 de Protección de Datos Personales.")
