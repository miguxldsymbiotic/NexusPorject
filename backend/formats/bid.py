from formats.base_format import BaseFormat

class FormatoBID(BaseFormat):
    id = "BID"
    nombre = "Ficha BID / IDB"
    descripcion = "Formato para proyectos financiados por el Banco Interamericano de Desarrollo"

    campos_obligatorios = [
        "titulo_proyecto",
        "pais_region",
        "sector_bid",
        "objetivo_desarrollo",
        "problema_oportunidad",
        "justificacion_intervencion",
        "descripcion_proyecto",
        "componentes",
        "beneficiarios",
        "costo_total",
        "financiamiento_bid",
        "contrapartida_local",
        "marco_resultados",
        "indicadores_impacto",
        "riesgos_mitigacion",
        "sostenibilidad",
        "salvaguardas_ambientales",
        "salvaguardas_sociales",
        "plan_adquisiciones",
    ]

    campos_criticos = [
        "salvaguardas_ambientales",
        "salvaguardas_sociales",
        "sostenibilidad",
        "contrapartida_local",
        "riesgos_mitigacion",
    ]

    instrucciones_retorica = """
    INSTRUCCIONES ESPECÍFICAS PARA FICHA BID/IDB:

    ESTRUCTURA OBLIGATORIA:
    1. RESUMEN EJECUTIVO
       - Máximo 500 palabras
       - Problema, solución, costo, beneficiarios, impacto esperado

    2. CONTEXTO Y JUSTIFICACIÓN
       - Análisis del contexto nacional/regional con datos macroeconómicos
       - Alineación con estrategia país del BID
       - Brecha de desarrollo que el proyecto atiende
       - Justificación de la intervención del BID (adicionalidad)

    3. DESCRIPCIÓN DEL PROYECTO
       - Objetivo de desarrollo (outcome de largo plazo)
       - Componentes del proyecto (máximo 4-5 componentes)
       - Actividades por componente
       - Productos esperados por componente

    4. MARCO DE RESULTADOS
       - Indicadores de impacto con línea base y meta
       - Indicadores de resultado por componente
       - Indicadores de producto con metas anuales
       - Fuentes de verificación para cada indicador

    5. ANÁLISIS DE RIESGOS
       - Riesgos fiduciarios, ambientales, sociales, políticos
       - Probabilidad e impacto (matriz semáforo)
       - Medidas de mitigación concretas

    6. SOSTENIBILIDAD
       - Arreglos institucionales post-proyecto
       - Estrategia de financiamiento recurrente
       - Transferencia de capacidades

    TONO Y ESTILO BID:
    - Inglés técnico o español neutro latinoamericano
    - Orientado a resultados de desarrollo (Development Effectiveness)
    - Énfasis en evidencia y evaluaciones de impacto
    - Alineación explícita con ODS y prioridades BID
    """