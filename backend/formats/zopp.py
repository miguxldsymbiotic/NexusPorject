from formats.base_format import BaseFormat

class FormatoZOPP(BaseFormat):
    id = "ZOPP"
    nombre = "ZOPP / PCM"
    descripcion = "Planificación de Proyectos Orientada a Objetivos / Project Cycle Management"

    campos_obligatorios = [
        "analisis_participacion",
        "analisis_problemas",
        "analisis_objetivos",
        "analisis_alternativas",
        "matriz_marco_logico",
        "objetivo_general",
        "objetivo_especifico",
        "resultados",
        "actividades",
        "indicadores_objetivamente_verificables",
        "fuentes_verificacion",
        "supuestos",
        "insumos",
        "presupuesto",
        "condiciones_previas",
    ]

    campos_criticos = [
        "analisis_participacion",
        "supuestos",
        "fuentes_verificacion",
        "condiciones_previas",
    ]

    instrucciones_retorica = """
    INSTRUCCIONES ESPECÍFICAS PARA ZOPP/PCM:

    HERRAMIENTAS DE ANÁLISIS:

    1. ANÁLISIS DE PARTICIPACIÓN
       - Identificar todos los grupos de interés (stakeholders)
       - Clasificar: beneficiarios directos, indirectos, excluidos, opositores
       - Analizar intereses, expectativas y temores de cada grupo

    2. ÁRBOL DE PROBLEMAS
       - Problema central en el tronco
       - Causas en las raíces (mínimo 2 niveles de profundidad)
       - Efectos en las ramas (mínimo 2 niveles)
       - Cada nodo es una sola afirmación negativa

    3. ÁRBOL DE OBJETIVOS
       - Transformación positiva del árbol de problemas
       - Cada afirmación negativa se convierte en situación positiva alcanzada
       - Verificar coherencia lógica de medios-fines

    4. MATRIZ DE MARCO LÓGICO (4x4)
       Columnas: Descripción | IOV | FdV | Supuestos
       Filas:
       - Objetivo General (impacto/fin)
       - Objetivo Específico (propósito/outcome)
       - Resultados (outputs)
       - Actividades (inputs)

    5. INDICADORES OBJETIVAMENTE VERIFICABLES (IOV)
       - Cantidad: ¿cuánto?
       - Calidad: ¿de qué tipo?
       - Tiempo: ¿cuándo?
       - Grupo destinatario: ¿para quién?
       - Lugar: ¿dónde?

    TONO Y ESTILO ZOPP:
    - Participativo y orientado a consenso
    - Lenguaje de cooperación al desarrollo
    - Énfasis en sostenibilidad y apropiación local
    - Cada supuesto debe ser realista pero no trivial
    """