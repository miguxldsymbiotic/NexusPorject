# Project Nexus - Motor de Homologación y Formulación de Propuestas I+D+i

Bienvenido a **Project Nexus**, una plataforma avanzada asistida por Inteligencia Artificial diseñada para transformar ideas "semilla" y transcripciones de audio en propuestas de investigación técnicas, estructuradas y listas para convocatorias de alto nivel como **Erasmus+ KA220** o **MGA (DNP Colombia)**.

---

## 🚀 Visión General del Proyecto

Project Nexus fue concebido para eliminar el "síndrome de la página en blanco" en los investigadores. Utilizando motores LLM de última generación (actualmente impulsado por **Cerebras AI - modelo Qwen 2.5 72B**), el sistema procesa entradas desestructuradas y las convierte en documentos formales y altamente técnicos.

### Características Principales:
1. **Expansión Retórica de Alta Fidelidad**: Toma una idea de 1 párrafo y la expande a un documento estructurado de más de 12 páginas (para formatos como MGA), cubriendo 11 secciones críticas (Problemas, Objetivos, Presupuesto, Riesgos, Impacto, etc.).
2. **Editor IA Estricto**: Permite al usuario revisar la propuesta inicial y dar instrucciones en lenguaje natural ("Cambia el presupuesto", "Enfócate más en innovación social"). La IA reestructurará el documento **completo** garantizando que no se pierda ninguna sección, manteniendo una coherencia del 100%.
3. **Motor de Emparejamiento (Matching Engine)**: Analiza el contexto de la propuesta y lo cruza semánticamente con un catálogo de demandas tecnológicas/convocatorias reales, identificando el porcentaje de compatibilidad.
4. **Sugerencia de Talento**: Basado en las necesidades del proyecto, sugiere los perfiles de los investigadores requeridos (roles y dedicación).
5. **Transcriptor Gratuito (Audio a Idea)**: Permite ingresar la idea del proyecto a través de notas de voz transcritas, que luego el sistema estructura automáticamente en los campos requeridos.
6. **Motor PDF Técnico Avanzado**: Exporta la métrica final y toda la expansión en un documento PDF profesional (utilizando `ReportLab`), con formato nativo para tablas, cuadros estéticos, viñetas y títulos jerarquizados.

---

## 🛠️ Arquitectura Técnica y Stack

- **Backend**: FastAPI (Python 3) - Alta velocidad y soporte asíncrono.
- **Frontend**: Vanilla HTML / JS / CSS - Diseño original v0.6.0 (Azul profundo y Naranja, sin frameworks externos para máxima ligereza). Tipografía *DM Sans*.
- **IA Core**: Cerebras API (`qwen-3-235b-a22b-instruct-2507` o `qwen2.5-72b-instruct`) - Utilizado por su enorme velocidad en inferencia, configurado con un límite de **16,384 tokens de salida** para garantizar propuestas masivas sin cortes.
- **Generación PDF**: ReportLab (Python) - Renderización dinámica de elementos estructurados, tablas y Markdown.

---

## 📝 Registro Histórico de Evolución e Implementaciones (Changelog v0.6.1)

Durante el último ciclo intensivo de desarrollo se resolvieron y mejoraron áreas críticas de la aplicación para asegurar su paso a producción:

### 1. Motor de Inteligencia Artificial (Cerebras & Persistencia)
- **Migración a Cerebras API**: Todo el ecosistema (Expansión, Matching, Sugerencia de talento y Edición) fue migrado exitosamente desde OpenRouter hacia Cerebras, garantizando mayor velocidad de respuesta.
- **Eliminación del Truncamiento**: Se evidenció que las propuestas masivas (12+ páginas) se cortaban. Se aumentó el `max_tokens` a **16384**.
- **Red de Seguridad (Fallbacks)**: Implementación de validación de longitud en `rhetoric_engine.py`:
  - Si una corrección de IA "resumía" y omitía la última sección técnica del documento o se reducía su tamaño drásticamente (< 85% de la longitud inicial), el sistema descarta esa versión y recupera de inmediato la versión cruda paso-a-paso, **garantizando que el contenido nunca se mutile**.

### 2. Editor IA y Previsualizador Markdown
- **Editor Estricto**: Modificación del Prompt para obligar a Qwen a devolver **siempre** el documento completo y estructurado en lugar de un resumen de cambios, preservando el encabezado `###` para parseo en HTML y PDF.
- **Sanitización del Visor**: Corrección de expresiones regulares en Javascript que causaban el colapso ("daño") de la ventana de previsualización al detectar tablas complejas. El nuevo sistema respeta la integridad del documento y asegura el formateado Markdown (negritas, etiquetas automáticas, saltos de página).
- **Visor Extendido**: Aumento de capacidad de `min-height` y `max-height` (hasta 1200px) para acomodar lecturas técnicas largas de forma ergonómica en la web.

### 3. Motor de PDF (ReportLab)
- **Blindaje de Caracteres**: Los caracteres especiales técnicos (como `&`, `<`, `>`) causaban que el motor de ReportLab colapsara con páginas en blanco o errores silenciosos. Se aplicó una capa de sanitización estricta (`replace`) justo antes de inyectar en la librería.
- **Generación de Tablas Complejas**: Soporte restaurado para procesar tablas estilo Markdown (`| c1 | c2 |`) e imprimirlas con estilos tabulares corporativos en el PDF.
- **Descargas Síncronas y Directas**: Corrección del pipeline de frontend-backend que obligaba al usuario a editar el documento para poder descargarlo. Ahora el botón "Generar PDF" captura la expansión original intacta si no hubo ediciones.

### 4. Interfaz de Usuario e Identidad
- **Rollback de Estética v0.6.0**: Reversión a petición del usuario de un diseño blanco minimalista hacia el corporativo "Azul e Institucional" que inspiraba más confianza.
- **Avisos y Logs de Error en Vivo**: El frontend se sincronizó para mostrar alertas de Javascript nativas si el servidor de Python falla al emitir el PDF u ocurre un límite de cuota, en lugar de un error de carga infinita.

---

## ⚙️ Pasos para Ejecutar Localmente

### Requisitos:
1. Python 3.9+
2. Claves de API (`.env` o en `config.py` - Principalmente `CEREBRAS_API_KEY`).

### Instalación:
```bash
# 1. Clonar el repositorio
git clone https://github.com/miguxldsymbiotic/NexusPorject.git

# 2. Ir al backend
cd NexusPorject/backend

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Levantar el servidor Uvicorn en modo hot-reload
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Una vez ejecutado, abre `http://localhost:8000` en tu navegador. El sistema redirigirá al cliente frontend original y conectará automáticamente con los módulos de Cerebras.

---
**Documentado con automatización algorítmica y revisado manual por el Agente de Sistemas (AntiGravity / Nexus). 2026.**
