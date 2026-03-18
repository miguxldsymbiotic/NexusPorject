from formats.base_format import BaseFormat

class FormatoMGA(BaseFormat):
    id = "MGA"
    nombre = "Metodología General Ajustada"
    descripcion = "Formato estándar del DNP colombiano para proyectos de inversión pública"

    campos_obligatorios = [
        "nombre_proyecto",
        "entidad_territorial",
        "sector",
        "problema_central",
        "descripcion_situacion_actual",
        "objetivo_general",
        "objetivos_especificos",
        "alternativas_solucion",
        "indicadores_producto",
        "indicadores_resultado",
        "cadena_valor",
        "presupuesto_por_vigencias",
        "fuentes_financiacion",
        "poblacion_beneficiaria",
        "localizacion_geografica",
        "estudio_riesgo",
        "impacto_ambiental",
    ]

    campos_criticos = [
        "impacto_ambiental",
        "estudio_riesgo",
        "fuentes_financiacion",
        "entidad_territorial",
        "poblacion_beneficiaria",
    ]

    instrucciones_retorica = """
    INSTRUCCIONES ESPECÍFICAS PARA FORMATO MGA (Metodología General Ajustada - DNP Colombia):

    ESTRUCTURA OBLIGATORIA:
    1. IDENTIFICACIÓN DEL PROYECTO
       - Nombre del proyecto (máximo 150 caracteres, debe iniciar con verbo en infinitivo)
       - Sector y subsector (según clasificación DNP)
       - Entidad territorial responsable

    2. PROBLEMA CENTRAL (Árbol de Problemas)
       - Redactar el problema central como una situación negativa existente
       - Identificar mínimo 3 causas directas y 2 causas indirectas por cada causa directa
       - Identificar mínimo 3 efectos directos y el efecto final
       - El problema NO debe redactarse como ausencia de solución

    3. OBJETIVO GENERAL (Árbol de Objetivos)
       - Es la situación contraria positiva del problema central
       - Debe ser medible con indicadores SMART
       - Incluir línea base y meta

    4. ALTERNATIVAS DE SOLUCIÓN
       - Mínimo 2 alternativas técnicamente viables
       - Análisis costo-beneficio simplificado
       - Justificación de la alternativa seleccionada

    5. CADENA DE VALOR
       - Insumos → Actividades → Productos → Resultados → Impacto
       - Cada producto debe tener indicador con unidad de medida, línea base y meta

    6. PRESUPUESTO POR VIGENCIAS
       - Desagregado por año fiscal
       - Clasificado por fuente de financiación (SGR, PGN, recursos propios, cooperación)

    7. INDICADORES
       - Indicadores de producto: miden las salidas directas de las actividades
       - Indicadores de resultado: miden cambios en la población objetivo

    TONO Y ESTILO MGA:
    - Lenguaje técnico-administrativo formal colombiano
    - Cifras con fuentes estadísticas oficiales (DANE, DNP, MinEducación)
    - Evitar adjetivos valorativos sin respaldo cuantitativo
    - Cada afirmación debe ser verificable
    """