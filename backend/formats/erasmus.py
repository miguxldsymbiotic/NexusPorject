from formats.base_format import BaseFormat

class FormatoErasmus(BaseFormat):
    id = "ERASMUS"
    nombre = "Erasmus+ KA220"
    descripcion = "Alianzas para la cooperación en educación y formación - Erasmus+ Acción Clave 2"

    campos_obligatorios = [
        "titulo_proyecto",
        "acronimo",
        "organizacion_solicitante",
        "paises_socios",
        "duracion_meses",
        "presupuesto_total",
        "resumen_ejecutivo",
        "prioridades_erasmus",
        "analisis_necesidades",
        "valor_anadido_europeo",
        "metodologia_pedagogica",
        "resultados_intelectuales",
        "plan_trabajo_wp",
        "actividades_aprendizaje",
        "gestion_calidad",
        "mecanismos_coordinacion",
        "impacto_esperado",
        "plan_diseminacion",
        "plan_sostenibilidad",
        "presupuesto_desglosado_socio",
        "avales_institucionales",
    ]

    campos_criticos = [
        "acronimo",
        "paises_socios",
        "valor_anadido_europeo",
        "resultados_intelectuales",
        "plan_diseminacion",
        "presupuesto_desglosado_socio",
        "avales_institucionales",
    ]

    instrucciones_retorica = """
    INSTRUCCIONES ESPECÍFICAS PARA ERASMUS+ KA220 (Alianzas para la Cooperación):

    REGLAS DE CONTENIDO OBLIGATORIO:
    1. PRESUPUESTO TOTAL: Debe declararse explícitamente en los datos básicos (ej. €250,000).
    2. PLAN DE DISEMINACIÓN: Debe ser una estrategia detallada, no solo una lista.
    3. DESGLOSE POR SOCIO: Es obligatorio presentar una tabla con la distribución del presupuesto entre los socios del consorcio.
    4. AVALES: Mencionar el compromiso formal de las instituciones participantes.

    ESTRUCTURA DE PUNTUACIÓN (Evaluar sobre 100):
    1. RELEVANCIA (30 pts): Alineación con prioridades horizontales (Inclusión, Digital, Verde).
    2. DISEÑO E IMPLEMENTACIÓN (20 pts): Metodología, Resultados Intelectuales (IOs).
    3. EQUIPO Y COOPERACIÓN (20 pts): Composición del consorcio.
    4. IMPACTO Y DISEMINACIÓN (30 pts): Estrategia de difusión y sostenibilidad.
    """

    @classmethod
    def get_secciones(cls):
        return [
            {
                "id": "resumen_ejecutivo",
                "nombre": "Datos Básicos y Resumen",
                "prompt": "Genera el resumen ejecutivo. Incluye: Título, Acrónimo (máx 20 chars), Organizaciones socias sugeridas y el PRESUPUESTO TOTAL SOLICITADO (ej. €400,000)."
            },
            {
                "id": "relevancia",
                "nombre": "Sección 1: Relevancia (30 puntos)",
                "prompt": "Genera la sección de Relevancia. Debe incluir prioritariamente: 1.1 Contexto, 1.2 Alineación con Prioridades Erasmus+ y 1.3 Valor Añadido Europeo."
            },
            {
                "id": "diseno_implementacion",
                "nombre": "Sección 2: Diseño e Implementación (20 puntos)",
                "prompt": "Genera la sección de Diseño. Incluye: 2.1 Metodología innovadora y 2.2 RESULTADOS INTELECTUALES (IOs) tangibles."
            },
            {
                "id": "equipo_cooperacion",
                "nombre": "Sección 3: Equipo y Cooperación (20 puntos)",
                "prompt": "Genera la sección de Equipo. Detalla la complementariedad de los socios y mecanismos de coordinación."
            },
            {
                "id": "impacto_sostenibilidad",
                "nombre": "Sección 4: Impacto y Sostenibilidad",
                "prompt": "Genera el impacto esperado y la estrategia de sostenibilidad a largo plazo post-financiamiento."
            },
            {
                "id": "diseminacion",
                "nombre": "Sección 5: PLAN DE DISEMINACIÓN DETALLADO",
                "prompt": "Genera un plan de diseminación exhaustivo. Incluye canales, audiencias objetivo y cronograma de actividades de difusión."
            },
            {
                "id": "presupuesto_desglosado",
                "nombre": "Sección 6: Presupuesto Desglosado por Socio",
                "prompt": "Genera una TABLA MARKDOWN con el desglose de presupuesto por socio (ej. Socio 1: €X, Socio 2: €Y). Asegura que la suma coincida con el total solicitado."
            },
            {
                "id": "avales",
                "nombre": "Sección 7: Avales Institucionales",
                "prompt": "Genera una sección que describa los compromisos institucionales de cada socio y el estado de sus avales para el proyecto."
            }
        ]