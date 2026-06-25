import os
import re
import pdfplumber
import pandas as pd

# Configuración de rutas absolutas automáticas
RUTA_DEL_SCRIPT = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.dirname(RUTA_DEL_SCRIPT)
CARPETA_RAW = os.path.join(RAIZ_PROYECTO, "data", "raw")
CARPETA_PROCESSED = os.path.join(RAIZ_PROYECTO, "data", "processed")


def extraer_metadatos_fallo(texto):
    """
    Usa Expresiones Regulares (Regex) adaptadas a la estructura del PJN
    para extraer Actor, Demandado y Fecha.
    """
    metadatos = {
        "Actor": "No encontrado",
        "Demandado": "No encontrado",
        "Fecha": "No encontrada"
    }

    if not texto:
        return metadatos

    # 1. Buscar el formato clásico argentino: "Actor c/ Demandado s/ materia"
    # El patrón busca texto antes del "c/" y texto entre el "c/" y el "s/"
    patron_caratula = re.search(r"([A-Za-z\s\,\.]+)\s+c\/\s+([A-Za-z\s\,\.\&\-]+)\s+s\/", texto)

    if patron_caratula:
        metadatos["Actor"] = patron_caratula.group(1).strip()
        metadatos["Demandado"] = patron_caratula.group(2).strip()

    # 2. Buscar la fecha del fallo (Ej: "Buenos Aires, 26 de noviembre de 2007")
    # Busca un lugar seguido de una fecha con mes en texto
    patron_fecha = re.search(
        r"(?:Buenos Aires|CABA|Ciudad Autónoma de Buenos Aires)?\,\s*(\d{1,2}\s+de\s+[a-z]+\s+de\s+\d{4})", texto,
        re.IGNORECASE)

    if patron_fecha:
        metadatos["Fecha"] = patron_fecha.group(1).strip()

    return metadatos


def procesar_pipeline():
    # Asegurar que las carpetas existan
    os.makedirs(CARPETA_PROCESSED, exist_ok=True)

    archivos = [f for f in os.listdir(CARPETA_RAW) if f.endswith(".pdf")]

    if not archivos:
        print(f"❌ No encontré archivos PDF en: {CARPETA_RAW}")
        return

    resultados_totales = []

    for archivo in archivos:
        ruta_completa = os.path.join(CARPETA_RAW, archivo)
        print(f"🔍 Analizando: {archivo}...")

        with pdfplumber.open(ruta_completa) as pdf:
            # Extraemos la primera página donde está la carátula y fecha
            primera_pagina = pdf.pages[0]
            texto = primera_pagina.extract_text()

            # Aplicamos nuestra lógica de Regex
            datos_extraidos = extraer_metadatos_fallo(texto)
            datos_extraidos["Archivo_Origen"] = archivo

            resultados_totales.append(datos_extraidos)

    # 3. Convertir a un DataFrame de Pandas para verlo como tabla
    df_resultados = pd.DataFrame(resultados_totales)

    print("\n📊 ¡PROCESO COMPLETADO! Datos Estructurados:")
    print("-" * 60)
    print(df_resultados.to_string(index=False))
    print("-" * 60)

    # Guardar el resultado en la carpeta processed
    ruta_guardado = os.path.join(CARPETA_PROCESSED, "reporte_jurisprudencia.csv")
    df_resultados.to_csv(ruta_guardado, index=False, encoding="utf-8-sig")
    print(f"💾 Reporte guardado con éxito en: {ruta_guardado}")


if __name__ == "__main__":
    procesar_pipeline()
