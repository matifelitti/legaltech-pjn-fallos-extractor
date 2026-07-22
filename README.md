# 🏛️ Analizador Inteligente de Jurisprudencia (PJN) - Inteligencia Artificial & Jurimetría

Un pipeline de **LegalTech** y procesamiento de lenguaje natural (NLP) de extremo a extremo diseñado específicamente para el derecho argentino. La aplicación ofrece una interfaz web unificada y centralizada que permite a estudios jurídicos, áreas de *Compliance* y departamentos legales corporativos automatizar la disección y el análisis de sentencias judiciales de cualquier fuero (Civil, Comercial, Laboral, Penal o Familia).

---

## 🎯 Perfil del Proyecto
Este sistema resuelve el cuello de botella que genera la revisión manual de jurisprudencia compleja. Combina ingeniería de prompts abstractos avanzados, almacenamiento indexado local y un diseño de interfaz de alta gama, demostrando el valor de la intersección entre el **Derecho, la Programación y la Analítica de Datos**.

---

## 🛠️ Logros Técnicos Clave

* **Extracción Semántica con IA (Prompt Universal)**: Implementación de Google Gemini (`gemini-2.5-flash`) mediante un molde conceptual abstracto que identifica las estructuras transversales de cualquier sentencia del país (Hechos, Fundamentos de la Mayoría, Disidencias, Parte Dispositiva y Precedente), evitando sesgos de fueros específicos.
* **Doble Flujo de Consulta Integrado**: 
  * *Opción A (Procesamiento de PDF)*: Lectura en memoria de archivos físicos mediante `pdfplumber`, permitiendo al usuario arrastrar dictámenes del PJN directamente a la web.
  * *Opción B (Oráculo Jurisprudencial)*: Consulta directa a la base de conocimiento global de la IA por carátula o nombre clave (ej: *Ekmekdjian c/ Sofovich*, *Mendoza*, *Badaro*).
* **Base de Conocimiento Local (Jurimetría)**: Almacenamiento automatizado e indexación de resultados en un archivo histórico mediante **Pandas**, permitiendo recuperar análisis previos de forma instantánea sin consumir cuotas de API de Inteligencia Artificial.
* **Diseño Legal Premium & Responsive**: Interfaz de usuario centralizada con estilos CSS independientes (`static/styles.css`). Cuenta con soporte adaptivo (*responsive*) para dispositivos móviles y una paleta de colores corporativa de alta gama (Azul Marino e incrustaciones en Dorado Champagne) que optimiza el contraste y la legibilidad tanto en Modo Claro como en Modo Oscuro.
* **Cumplimiento Normativo (Privacy by Design)**: Inclusión de políticas y alertas de confidencialidad en la UI alineadas con la Ley N° 25.326 de Protección de Datos Personales de la República Argentina.

---

## 💻 Stack Tecnológico
* **Interfaz de Usuario**: Streamlit (Python)
* **Oráculo de IA / NLP**: Google GenAI SDK (Gemini 2.5)
* **Ingeniería de Datos & Almacenamiento**: Pandas
* **Extracción de Documentos**: Pdfplumber
* **Seguridad / Configuración**: Python-Dotenv (Gestión de secretos mediante archivo `.env`)

---

## 📂 Estructura del Repositorio
```text
legaltech-pjn-fallos-extractor/
│
├── .streamlit/              
│   └── config.toml          # Configuraciones nativas del servidor Streamlit
│
├── data/                    
│   ├── raw/                 # PDFs de fallos locales y archivo de instrucciones
│   └── processed/           # Base de conocimiento indexada en formato CSV
│
├── src/                     
│   └── extractor_base.py    # Laboratorio de pruebas backend e historial de desarrollo
│
├── static/                  
│   └── styles.css           # Estilos CSS independientes de alta gama corporativa
│
├── main.py                  # Orquestador principal de la interfaz web y lógica unificada
├── .env                     # Claves privadas de API (Excluido de Git por seguridad)
├── .gitignore               # Filtros de exclusión para entornos virtuales y datos sensibles
└── requirements.txt         # Lista automatizada de dependencias del entorno virtual
```

---

## 🚀 Instalación y Uso Local

Siga estos pasos para clonar el proyecto, configurar su entorno virtual local y ejecutar la aplicación.

### 1. Clonar el repositorio
```bash
git clone https://github.com
cd legaltech-pjn-fallos-extractor
```

### 2. Configurar el entorno virtual e instalar dependencias
**En Windows (PyCharm / PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar su Clave de API Oculta
Cree un archivo llamado exactamente **`.env`** en la raíz del proyecto y añada su API Key gratuita de Google AI Studio (sin comillas y sin espacios):
```text
GEMINI_API_KEY=AIzaSyBlahBlahBlah_TuCodigoReal
```

### 4. Lanzar la aplicación web
Ejecute el servidor local de Streamlit desde su terminal:
```bash
streamlit run main.py
```
*La aplicación se abrirá automáticamente en su navegador web listo para procesar jurisprudencia en el centro de la pantalla.*
