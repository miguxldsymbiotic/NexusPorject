from formats.base_format import BaseFormat

class FormatoMinCiencias(BaseFormat):
    id = "MINCIENCIAS"
    nombre = "Colciencias / MinCiencias"
    descripcion = "Formato para convocatorias de ciencia, tecnología e innovación de MinCiencias Colombia"

    campos_obligatorios = [
        "titulo_proyecto",
        "clasificacion_proyecto",  # Investigación básica, aplicada, desarrollo experimental
        "grupo_investigacion",
        "investigador_principal",
        "coinvestigadores",
        "institucion_avalante",
        "resumen_ejecutivo",
        "planteamiento_problema",
        "pregunta_investigacion",
        "estado_arte",
        "marco_teorico",
        "objetivos",
        "metodologia_detallada",
        "cronograma",
        "presupuesto_detallado",
        "resultados_esperados",
        "impacto_potencial",
        "apropiacion_social",
        "consideraciones_eticas",
        "bibliografia",
    ]

    campos_criticos = [
        "grupo_investigacion",
        "institucion_avalante",
        "consideraciones_eticas",
        "apropiacion_social",
        "estado_arte",
    ]

    instrucciones_retorica = """
    INSTRUCCIONES ESPECÍFICAS PARA FORMATO MINCIENCIAS (Colombia):

    ESTRUCTURA OBLIGATORIA:
    1. IDENTIFICACIÓN
       - Título: máximo 20 palabras, descriptivo y específico
       - Clasificación: Investigación Básica / Aplicada / Desarrollo Experimental / Innovación
       - Área del conocimiento (según clasificación OCDE)
       - Programa nacional de CTel correspondiente

    2. PLANTEAMIENTO DEL PROBLEMA
       - Descripción clara de la brecha de conocimiento o problema tecnológico
       - Contexto nacional e internacional del problema
       - Pregunta de investigación central (una sola pregunta clara y enfocada)
       - Hipótesis de investigación (si aplica)

    3. ESTADO DEL ARTE
       - Revisión sistemática de literatura de los últimos 5 años
       - Identificación del vacío de conocimiento que justifica el proyecto
       - Mínimo 20 referencias en formato APA 7ma edición

    4. METODOLOGÍA
       - Enfoque metodológico (cuantitativo, cualitativo, mixto)
       - Diseño de investigación específico
       - Población y muestra con justificación estadística
       - Instrumentos de recolección de datos
       - Plan de análisis de datos

    5. RESULTADOS ESPERADOS
       - Nuevos conocimientos generados
       - Productos tecnológicos o innovaciones
       - Formación de recurso humano (tesis, pasantías)
       - Apropiación social del conocimiento
       - Publicaciones indexadas proyectadas (Scopus, WoS)

    6. PRESUPUESTO
       - Personal (honorarios investigadores, auxiliares)
       - Equipos y materiales
       - Salidas de campo o viajes
       - Difusión y publicación
       - Gastos administrativos (máximo 10% del total)

    TONO Y ESTILO MINCIENCIAS:
    - Lenguaje científico riguroso
    - Citar estadísticas de ScienTI, Scopus, Web of Science
    - Justificar cada rubro presupuestal
    - Demostrar capacidad instalada del grupo de investigación
    """