Requerimientos y arquitectura — resumen ejecutivo
Qué hace el sistema

El sistema recibe una idea de proyecto incompleta y la transforma en un documento formal listo para presentar a una convocatoria, generado en el formato específico que exige esa entidad.

-----------------------------------------------

Inputs que debe pedir el formulario
Estos son los campos que yo considero imprescindibles (más allá de los obvios):

1. Identificación básica: título del proyecto, descripción de la idea (texto libre), sector temático (educación, salud, tecnología, medio ambiente, etc.), duración estimada, presupuesto estimado, y país/región donde se ejecuta.
2. Convocatoria destino: selección del organismo (BID, Erasmus+, DNP-Colombia, Colciencias, Horizonte Europa, PNUD, etc.). Esto determina el formato de salida y el tono/lenguaje del documento.
3. Participantes: entidad solicitante, tipo de organización (pública, privada, academia, ONG), y si hay entidades socias.
4. Metodología de desarrollo: aquí el usuario elige cómo se va a gestionar el proyecto (Marco Lógico, Design Thinking, Scrum/Agile, PMBOK, PRINCE2, ZOPP, etc.).
5. Formato de presentación: el "molde" institucional en el que se vierte todo (MGA, Marco Lógico estándar, formulario Erasmus+ KA220, ficha BID, etc.).
6. Objetivos y beneficiarios: objetivo general en borrador, población objetivo estimada, y problema central que resuelve.

-----------------------------------------------

Formatos y metodologías que cubre el sistema
Formatos institucionales (outputs):

1. MGA — Metodología General Ajustada del DNP Colombia. Para inversión pública nacional y territorial.
2. Marco Lógico clásico — usado por CEPAL, BID, PNUD, cooperación internacional.
3. ZOPP / PCM — Project Cycle Management de la Comisión Europea; base de Erasmus+.
4. Erasmus+ KA220 — Asociaciones de cooperación en educación. Tiene su propio formulario con secciones muy específicas.
5. Ficha BID / IDB — formato de propuesta del Banco Interamericano de Desarrollo.
6. Horizonte Europa — formato de la UE para proyectos de I+D+i.
7. Colciencias / MinCiencias — convocatorias de ciencia y tecnología en Colombia.

Metodologías de gestión (influyen en la redacción y estructura):
Design Thinking, PMBOK, Scrum/Agile, PRINCE2, Lean Startup, ODS/PNUD.

-----------------------------------------------

Cómo funciona la IA en el proceso

El módulo de IA recibe los inputs del usuario y hace tres cosas: primero, infiere y completa las secciones que el usuario dejó en borrador (árbol de problemas, indicadores, justificación, antecedentes). Segundo, adapta el tono retórico al organismo destino (los documentos para el DNP suenan diferente a los de Erasmus+). Tercero, estructura la respuesta en JSON con los campos exactos del formato elegido, que luego el módulo PDF renderiza con las dimensiones y tipografía correctas.

-----------------------------------------------

Arquitectura del proyecto Node.js

/
├── src/
│   ├── server.js              # Express entry point
│   ├── routes/
│   │   ├── generate.js        # POST /api/generate
│   │   └── formats.js         # GET /api/formats
│   ├── modules/
│   │   ├── ai/
│   │   │   └── claude.js      # Anthropic SDK — prompt builder
│   │   ├── formats/
│   │   │   ├── mga.js         # Lógica + prompt MGA
│   │   │   ├── marco-logico.js
│   │   │   ├── erasmus-ka220.js
│   │   │   └── bid.js
│   │   └── pdf/
│   │       └── renderer.js    # Puppeteer → PDF
│   ├── templates/
│   │   ├── mga.html           # Plantilla HTML del formato MGA
│   │   ├── marco-logico.html
│   │   └── erasmus-ka220.html
│   └── config/
│       └── formats.json       # Catálogo de formatos y sus campos
├── frontend/                  # React o HTML+JS vanilla
├── .env
└── package.json

La clave de escalabilidad es que cada formato es un módulo independiente: un archivo JS con su lógica de prompt, una plantilla HTML con su estructura visual, y una entrada en formats.json. Para añadir el formato de Horizonte Europa, solo se agregan esos tres archivos sin tocar el core.

-----------------------------------------------

Propuesta de fases

Fase 1 (MVP — este prototipo): MGA + Marco Lógico + Erasmus+ KA220, con generación de PDF descargable, interfaz funcional en Node.js + HTML vanilla.
Fase 2: Añadir BID, Colciencias, Horizonte Europa. Añadir historial de proyectos con base de datos ligera (SQLite o MongoDB).
Fase 3: Autenticación, colaboración entre usuarios, plantillas personalizadas, y posiblemente exportación a Word (.docx) además de PDF.