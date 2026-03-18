from formats.base_format import BaseFormat

class FormatoHorizonte(BaseFormat):
    id = "HORIZONTE"
    nombre = "Horizonte Europa"
    descripcion = "Programa marco de investigación e innovación de la Unión Europea 2021-2027"

    campos_obligatorios = [
        "titulo_proyecto",
        "acronimo",
        "call_identifier",
        "tipo_accion",
        "consorcio",
        "resumen",
        "excelencia_cientifica",
        "impacto",
        "implementacion",
        "etica",
        "seguridad",
        "plan_ciencia_abierta",
        "consideraciones_genero",
        "presupuesto",
    ]

    campos_criticos = [
        "excelencia_cientifica",
        "etica",
        "consideraciones_genero",
        "plan_ciencia_abierta",
        "call_identifier",
    ]

    instrucciones_retorica = """
    INSTRUCCIONES ESPECÍFICAS PARA HORIZONTE EUROPA:

    ESTRUCTURA OBLIGATORIA (Parte B técnica):

    SECCIÓN 1 — EXCELENCIA
    - Estado del arte y posicionamiento científico del proyecto
    - Objetivos y ambición científica o tecnológica
    - Metodología y plan de investigación detallado
    - Riesgos y planes de contingencia
    - Indicar TRL (Technology Readiness Level) inicial y final

    SECCIÓN 2 — IMPACTO
    - Resultados e impactos esperados a corto, medio y largo plazo
    - Medidas para maximizar el impacto (diseminación, explotación, comunicación)
    - Alineación con las misiones y partnerships de Horizonte Europa
    - Análisis de stakeholders y plan de involucramiento
    - Contribución al Green Deal, Digital Decade u otras prioridades EU

    SECCIÓN 3 — IMPLEMENTACIÓN
    - Estructura del trabajo (Work Packages, tareas, hitos, entregables)
    - Diagrama de Gantt
    - Gestión del consorcio y estructura de toma de decisiones
    - Gestión de recursos y presupuesto justificado
    - Gestión de propiedad intelectual (Consortium Agreement)

    CRITERIOS DE EVALUACIÓN (ponderación):
    - Excelencia: 50%
    - Impacto: 30%
    - Implementación: 20%

    TONO Y ESTILO HORIZONTE:
    - Inglés científico de alta calidad (o idioma de la convocatoria)
    - TRL explícito para proyectos tecnológicos
    - Énfasis en novedad e innovación disruptiva
    - Citar literatura científica reciente (últimos 3 años)
    """