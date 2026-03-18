from formats.base_format import BaseFormat

class FormatoMarcoLogico(BaseFormat):
    id = "MARCO_LOGICO"
    nombre = "Marco Lógico clásico"
    descripcion = "Enfoque del Marco Lógico clásico para proyectos de desarrollo"

    campos_obligatorios = [
        "resumen_narrativo",
        "fin",
        "proposito",
        "componentes",
        "actividades",
        "indicadores",
        "medios_verificacion",
        "supuestos",
        "presupuesto",
        "cronograma",
    ]

    campos_criticos = [
        "supuestos",
        "medios_verificacion",
        "fin",
    ]

    instrucciones_retorica = """
    INSTRUCCIONES ESPECÍFICAS PARA MARCO LÓGICO CLÁSICO:

    MATRIZ DE MARCO LÓGICO:

    1. FIN (Goal/Impacto)
       - Objetivo de desarrollo de largo plazo al que contribuye el proyecto
       - El proyecto contribuye pero no es el único responsable
       - Indicadores de impacto medibles a 5-10 años

    2. PROPÓSITO (Purpose/Outcome)
       - Cambio de comportamiento o condición en la población objetivo
       - El proyecto es directamente responsable de este cambio
       - Debe haber un solo propósito por proyecto
       - Indicadores de resultado medibles al final del proyecto

    3. COMPONENTES/PRODUCTOS (Outputs)
       - Bienes y servicios producidos directamente por el proyecto
       - El equipo del proyecto controla directamente su producción
       - Redactados como sustantivos (ej: "Sistema de monitoreo implementado")

    4. ACTIVIDADES (Inputs)
       - Acciones necesarias para producir cada componente
       - Agrupadas por componente
       - Base para el presupuesto y el cronograma

    5. LÓGICA VERTICAL (si-entonces)
       - Si se ejecutan las Actividades → se producen los Componentes
       - Si se producen los Componentes → se logra el Propósito
       - Si se logra el Propósito → se contribuye al Fin
       - En cada nivel: si se cumplen los Supuestos

    6. LÓGICA HORIZONTAL
       - Cada nivel tiene: Descripción | Indicadores | Medios de Verificación | Supuestos

    TONO Y ESTILO MARCO LÓGICO:
    - Preciso y sin ambigüedades
    - Verbos en pasado para componentes (ya producidos)
    - Supuestos externos al control del proyecto
    - Indicadores SMART en todos los niveles
    """