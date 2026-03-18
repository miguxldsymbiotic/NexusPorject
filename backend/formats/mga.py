from formats.base_format import BaseFormat

class FormatoMGA(BaseFormat):
    id = "MGA"
    nombre = "Metodología General Ajustada"
    descripcion = "Formato estándar del DNP colombiano para proyectos de inversión pública"

    campos_obligatorios = [
        "nombre_proyecto",
        "sector_subsector",
        "entidad_territorial",
        "localizacion",
        "duracion",
        "descripcion_situacion_actual",
        "problema_central",
        "causas_efectos",
        "objetivo_general",
        "objetivos_especificos",
        "alternativas_solucion",
        "cadena_valor",
        "indicadores_producto",
        "indicadores_resultado",
        "presupuesto_vigencias",
        "fuentes_financiacion",
        "poblacion_beneficiaria",
        "estudio_riesgo",
        "impacto_ambiental",
    ]

    campos_criticos = [
        "entidad_territorial",
        "fuentes_financiacion",
        "poblacion_beneficiaria",
        "estudio_riesgo",
        "impacto_ambiental",
    ]

    instrucciones_retorica = """
    INSTRUCCIONES CRÍTICAS PARA FORMATO MGA (DNP Colombia):

    PROHIBICIONES ABSOLUTAS:
    - NO USAR "N/A", "Por definir", "A medias" o similares.
    - SI NO HAY DATOS EXACTOS, LA IA DEBE GENERAR ESTIMACIONES REALISTAS basadas en el contexto del proyecto y el sector en Colombia.
    - CADA CAMPO CRÍTICO DEBE TENER CONTENIDO SUSTANCIAL.

    REGLAS DE ORO POR SECCIÓN:
    1. POBLACIÓN: Debe ser una tabla con números exactos (ej. 5.000 personas), discriminados por sexo, edad y estrato.
    2. FINANCIACIÓN: Declarar montos específicos asignados a Nación, SGR, Municipio o Recursos Propios.
    3. RIESGOS: Generar una matriz (tabla) con Probabilidad, Impacto y Mitigación para al menos 3 riesgos (Técnico, Económico, Social).
    4. AMBIENTAL: Declarar categoría de impacto y medidas concretas de manejo ambiental.
    5. PRESUPUESTO: Presentar tabla con montos por Vigencia (AÑO 1, AÑO 2, etc.).
    6. ALTERNATIVAS: Evaluar obligatoriamente 2 alternativas técnicas contrastadas.
    7. CADENA DE VALOR: Secuencia Insumos -> Actividades -> Productos -> Resultados -> Impacto.
    """

    @classmethod
    def get_secciones(cls):
        return [
            {
                "id": "identificacion",
                "nombre": "Sección 1: Identificación y Localización",
                "prompt": "Genera los datos de identificación. El nombre DEBE empezar con un verbo en infinitivo. Especifica Sector DNP, Entidad Territorial y Localización exacta."
            },
            {
                "id": "problema",
                "nombre": "Sección 2: Identificación del Problema (Árbol)",
                "prompt": "Genera el Árbol de Problemas. Problema Central (Situación negativa), Causas Directas, Indirectas y Efectos. NO dejar en blanco."
            },
            {
                "id": "objetivos",
                "nombre": "Sección 3: Objetivos del Proyecto (Árbol)",
                "prompt": "Genera el Árbol de Objetivos. Objetivo General y al menos 4 Objetivos Específicos alineados a las causas."
            },
            {
                "id": "alternativas",
                "nombre": "Sección 4: Alternativas de Solución",
                "prompt": "Evalúa obligatoriamente 2 (DOS) ALTERNATIVAS de solución técnica. Justifica la elección de la propuesta central basada en eficiencia y costo."
            },
            {
                "id": "cadena_valor",
                "nombre": "Sección 5: Cadena de Valor",
                "prompt": "Genera la Cadena de Valor siguiendo la estructura: Insumos -> Actividades -> Productos -> Resultados -> Impacto esperado."
            },
            {
                "id": "indicadores",
                "nombre": "Sección 6 y 7: Indicadores SMART",
                "prompt": "Genera una TABLA MARKDOWN con Indicadores de Producto y de Resultado. Incluye Nombre, Unidad, Línea Base, Meta y MEDIOS DE VERIFICACIÓN."
            },
            {
                "id": "presupuesto_fuentes",
                "nombre": "Sección 8: Presupuesto por Vigencia y Financiación",
                "prompt": "Genera una TABLA MARKDOWN con el presupuesto desglosado por VIGENCIAS (Año 1, Año 2) y otra tabla indicando las FUENTES (Nación, SGR, Propios) con montos sugeridos razonables."
            },
            {
                "id": "beneficiarios",
                "nombre": "Sección 9: Población Beneficiaria (Exacta)",
                "prompt": "Genera una TABLA MARKDOWN con la población beneficiaria. Exige cifras estimadas, distribución por sexo (H/M), rangos de edad y estratificación socioeconómica (1, 2, 3)."
            },
            {
                "id": "riesgos",
                "nombre": "Sección 10: Matriz de Riesgos",
                "prompt": "Genera una TABURA MARKDOWN con la Matriz de Riesgos. Incluye: Tipo de Riesgo, Probabilidad, Impacto y Medida de Mitigación."
            },
            {
                "id": "ambiental",
                "nombre": "Sección 11: Impacto Ambiental",
                "prompt": "Realiza el análisis ambiental. Clasifica en categoría (Baja, Media, Alta) y detalla las medidas de manejo ambiental requeridas por la normativa."
            }
        ]