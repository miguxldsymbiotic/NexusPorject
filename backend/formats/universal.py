from formats.base_format import BaseFormat

class FormatoUniversal(BaseFormat):
    id = "UNIVERSAL"
    nombre = "Formato Universal (Híbrido)"
    descripcion = "Carga maestra adaptable a cualquier convocatoria (Académica + Empresarial)"

    campos_obligatorios = [
        "titulo_proyecto",
        "objetivo_general",
        "problema_central",
        "metodologia",
        "sector_tematico",
        "duracion_estimada",
        "beneficiarios",
        "arbol_problemas",
        "arbol_objetivos",
        "ods_relacionados",
        "impacto_social",
        "presupuesto_total",
        "marco_teorico",
        "analisis_riesgos",
        "presupuesto_detallado",
        "sostenibilidad",
    ]

    campos_criticos = [
        "problema_central",
        "arbol_problemas",
        "ods_relacionados",
        "impacto_social",
        "presupuesto_total",
        "marco_teorico",
        "analisis_riesgos",
    ]

    instrucciones_retorica = """
    INSTRUCCIONES PARA EL FORMATO UNIVERSAL (MAESTRO 2.0):
    Este es el núcleo de carga para cualquier convocatoria. Debe ser exhaustivo y profesional.
    
    ESTRUCTURA OBLIGATORIA EN EL RESULTADO:
    1. RESUMEN EJECUTIVO (Punto de entrada comercial/académico)
    2. ÁRBOL DE PROBLEMAS: Desglosar Causa Raíz -> Problema Central -> Efectos.
    3. ÁRBOL DE OBJETIVOS: Medios -> Objetivo General -> Fines/Impactos.
    4. MARCO TEÓRICO Y TÉCNICO: Sustentación científica o técnica de la solución.
    5. ALINEACIÓN ODS: Explicar técnicamente la contribución a los Objetivos de Desarrollo Sostenible.
    6. METODOLOGÍA DETALLADA: Fases, hitos y entregables.
    7. ANÁLISIS DE BENEFICIARIOS: Segmentación y cuantificación estimada.
    8. IMPACTO Y SOSTENIBILIDAD: Social, técnica y financiera a largo plazo.
    9. ANÁLISIS DE RIESGOS: Mitigación de riesgos técnicos, financieros y operativos.
    10. PRESUPUESTO ESTIMADO: Desglose por grandes rubros.

    TONO:
    - Riguroso, innovador y persuasivo.
    - Utilizar terminología técnica adecuada al sector indicado.
    """
