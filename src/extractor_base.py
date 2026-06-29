import os
import pdfplumber
from google import genai
from dotenv import load_dotenv

# 1. Configuración de rutas absolutas automáticas
RUTA_DEL_SCRIPT = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.dirname(RUTA_DEL_SCRIPT)
CARPETA_RAW = os.path.join(RAIZ_PROYECTO, "data", "raw")
CARPETA_PROCESSED = os.path.join(RAIZ_PROYECTO, "data", "processed")

# 2. CARGAR EL ARCHIVO .ENV SEGURO Y CONECTAR LA IA
load_dotenv(os.path.join(RAIZ_PROYECTO, ".env"))
client = genai.Client()


def analizar_contenido_juridico(texto_completo):
    """
    Envía las primeras páginas del fallo a Gemini con un prompt estructurado
    para extraer los hechos y la división de votos.
    """
    # Recortamos el texto para optimizar la velocidad (las primeras 15.000 letras)
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
            model='gemini-2.5-flash',  # El modelo gratuito, rápido y más moderno de Google
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"❌ Error al conectar con Gemini: {str(e)}"


def ejecutar_pipeline_completo():
    # Asegurar que existan las carpetas de salida
    os.makedirs(CARPETA_PROCESSED, exist_ok=True)

    archivos = [f for f in os.listdir(CARPETA_RAW) if f.endswith(".pdf")]

    if not archivos:
        print(f"❌ Error: No encontré ningún archivo .pdf en la carpeta: {CARPETA_RAW}")
        return

    # Tomamos el primer fallo (por ejemplo, fallo_1.pdf que contiene "Badaro")
    primer_fallo = archivos[0]
    ruta_completa = os.path.join(CARPETA_RAW, primer_fallo)
    print(f"📖 Leyendo el archivo físico: {primer_fallo}...")

    # Extraer el texto completo del PDF usando pdfplumber
    texto_fallo = ""
    with pdfplumber.open(ruta_completa) as pdf:
        for pagina in pdf.pages:
            texto_fallo += pagina.extract_text() or ""

    if not texto_fallo:
        print("⚠️ No se pudo extraer texto del PDF. Verificá que no sea una imagen escaneada.")
        return

    print("🧠 Enviando el texto a la Inteligencia Artificial para el análisis jurídico...")
    print("=" * 60)

    # Ejecutar la consulta a Gemini
    analisis_juridico = analizar_contenido_juridico(texto_fallo)

    # Mostrar el resultado final en la consola de PyCharm
    print(analisis_juridico)
    print("=" * 60)


if __name__ == "__main__":
    ejecutar_pipeline_completo()

