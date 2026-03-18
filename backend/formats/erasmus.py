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
        "contexto_europeo",
        "objetivos_proyecto",
        "descripcion_grupos_destinatarios",
        "metodologia_cooperacion",
        "plan_trabajo",
        "resultados_intelectuales",
        "actividades_multiplicacion",
        "plan_evaluacion",
        "plan_sostenibilidad",
        "plan_diseminacion",
        "capacidad_organizacional",
        "presupuesto_desglosado",
    ]

    campos_criticos = [
        "paises_socios",
        "acronimo",
        "contexto_europeo",
        "resultados_intelectuales",
        "plan_diseminacion",
    ]

    instrucciones_retorica = """
    INSTRUCCIONES ESPECÍFICAS PARA ERASMUS+ KA220:

    ESTRUCTURA OBLIGATORIA:
    1. INFORMACIÓN GENERAL
       - Título completo y acrónimo memorable (máximo 7 caracteres)
       - Consorcio: mínimo 3 organizaciones de 3 países del Programa Erasmus+
       - Duración: 24 o 36 meses
       - Presupuesto máximo: €400,000

    2. RESUMEN (máximo 5,000 caracteres)
       - Contexto y problema europeo abordado
       - Objetivos del proyecto
       - Metodología de cooperación transnacional
       - Resultados intelectuales (Intellectual Outputs)
       - Impacto esperado en los grupos destinatarios

    3. CONTEXTO Y RELEVANCIA
       - Alineación con las prioridades de Erasmus+ 2021-2027
       - Relevancia para el Espacio Europeo de Educación
       - Necesidades identificadas en los países socios
       - Valor añadido de la cooperación transnacional

    4. DESCRIPCIÓN DEL PROYECTO
       - Grupos destinatarios directos e indirectos
       - Metodología de trabajo colaborativo entre socios
       - Plan de trabajo por fases (Work Packages)
       - Resultados intelectuales concretos y transferibles

    5. PRESUPUESTO (costos unitarios Erasmus+)
       - Gestión de proyectos y ejecución: €500/mes por organización
       - Reuniones transnacionales: €575 por participante
       - Resultados intelectuales: según tipo y días de trabajo
       - Actividades de multiplicación: €100-€200 por participante

    TONO Y ESTILO ERASMUS+:
    - Énfasis en la dimensión europea y la cooperación transnacional
    - Lenguaje inclusivo y orientado a impacto social
    - Demostrar experiencia previa en proyectos europeos
    - Usar terminología oficial de la Guía de Programas Erasmus+
    """