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

    @classmethod
    def get_secciones(cls):
        return [
            {
                "id": "excellence",
                "nombre": "Excelencia: Objetivos, Metodología y Ambición",
                "prompt": "Genera una sección de 'Excelencia' para una propuesta de Horizonte Europa. Debe incluir: 1. Objetivos del proyecto (SMART), 2. Metodología detallada (incluyendo conceptos interdisciplinarios y recursos de género si aplica), 3. Ambición y estado del arte (cómo el proyecto va más allá de lo existente). Usa lenguaje técnico y académico de alto nivel."
            },
            {
                "id": "impact",
                "nombre": "Impacto: Vías hacia el impacto y Medidas para maximizarlo",
                "prompt": "Genera una sección de 'Impacto' para Horizonte Europa. Debe detallar: 1. Contribución a los 'Expected Impacts' del programa de trabajo, 2. Medidas de difusión, explotación y comunicación (C&D), 3. Estrategia de gestión de propiedad intelectual. Sé específico y utiliza métricas de impacto realistas."
            },
            {
                "id": "implementation",
                "nombre": "Implementación: Plan de Trabajo, Recursos y Gestión",
                "prompt": "Genera una sección de 'Implementación' para Horizonte Europa. Debe describir: 1. Plan de trabajo (Work Packages detallados), 2. Estructura de gestión y toma de decisiones, 3. Consorcio y capacidades de los socios, 4. Evaluación de riesgos detallada y planes de mitigación."
            }
        ]