import os
import pdfplumber

# 1. ESTO CORRIGE EL ERROR: Encuentra la raíz del proyecto de forma automática
# Toma la ubicación de este script (src/) y sube un nivel a la raíz del proyecto
RUTA_DEL_SCRIPT = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.dirname(RUTA_DEL_SCRIPT)

# Define la ruta absoluta hacia data/raw
CARPETA_RAW = os.path.join(RAIZ_PROYECTO, "data", "raw")


def probar_lectura_pdf():
    # Creamos la carpeta automáticamente si por alguna razón no existía
    if not os.path.exists(CARPETA_RAW):
        os.makedirs(CARPETA_RAW)
        print(f"📁 Se creó la carpeta automáticamente en: {CARPETA_RAW}")
        print("👉 Por favor, guarda un fallo en PDF ahí dentro y vuelve a ejecutar el script.")
        return

    # Buscar todos los archivos PDF en la carpeta
    archivos = [f for f in os.listdir(CARPETA_RAW) if f.endswith(".pdf")]

    if not archivos:
        print(f"❌ Error: No encontré ningún archivo .pdf en la carpeta: {CARPETA_RAW}")
        print("👉 Por favor, guardá un fallo en PDF en esa carpeta antes de correr el script.")
        return

    # Tomamos el primer fallo de la lista para la prueba
    primer_fallo = archivos[0]  # <-- Corregido también el índice que faltaba en el script anterior
    ruta_completa = os.path.join(CARPETA_RAW, primer_fallo)
    print(f"📖 Intentando leer el archivo: {primer_fallo}...\n")

    # 2. Abrir el PDF y extraer el texto de la primera página
    with pdfplumber.open(ruta_completa) as pdf:
        primera_pagina = pdf.pages[0]
        texto_extraido = primera_pagina.extract_text()

        if texto_extraido:
            print("✅ ¡Texto extraído con éxito! Aquí tenés las primeras 500 letras:\n")
            print("-" * 50)
            print(texto_extraido[:500])  # Muestra solo el inicio del fallo
            print("-" * 50)
        else:
            print("⚠️ Advertencia: No se pudo extraer texto. ¿El PDF es una imagen escaneada?")


if __name__ == "__main__":
    probar_lectura_pdf()
