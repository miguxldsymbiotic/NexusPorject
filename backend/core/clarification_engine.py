from core.ai_client import ask_ai
from formats.format_registry import get_formato

# Prompt que le pide a la IA analizar qué falta en la idea
ANALYSIS_PROMPT = """
Eres un revisor experto en formulación de proyectos para convocatorias {formato}.

Se te presenta una idea de proyecto:
---
{idea}
---

Los siguientes campos son CRÍTICOS para el formato {formato} y deben estar 
presentes o al menos insinuados en la descripción del proyecto:
{campos_criticos}

Tu tarea es analizar la idea y determinar cuáles de esos campos críticos 
NO están cubiertos ni siquiera de forma implícita.

Responde ÚNICAMENTE con un objeto JSON con esta estructura exacta, sin texto adicional:
{{
  "campos_faltantes": ["campo1", "campo2"],
  "campos_cubiertos": ["campo3", "campo4"],
  "analisis_breve": "Una sola oración explicando el estado general de la idea"
}}

Si todos los campos están cubiertos, "campos_faltantes" debe ser una lista vacía [].
"""

# Prompt para generar la pregunta de clarificación
QUESTION_PROMPT = """
Eres un consultor amable y profesional en formulación de proyectos.

El usuario quiere formular un proyecto en formato {formato} pero le falta 
información sobre los siguientes campos críticos:
{campos_faltantes}

Genera UNA SOLA pregunta de clarificación que sea:
- Conversacional y amigable, no intimidante
- Explique brevemente por qué ese campo es importante para el formato {formato}
- Pida la información faltante de forma concreta
- Si hay varios campos faltantes, agrúpalos en una sola pregunta coherente

Responde solo con la pregunta, sin introducción ni cierre.
"""

def analizar_campos_faltantes(idea: str, formato: str) -> dict:
    """
    Analiza si la idea cubre los campos críticos del formato solicitado.
    Retorna qué campos faltan y cuáles están cubiertos.
    """
    clase_formato = get_formato(formato)
    campos_criticos = clase_formato.get_campos_criticos()

    prompt = ANALYSIS_PROMPT.format(
        idea=idea,
        formato=formato,
        campos_criticos="\n".join(f"- {c}" for c in campos_criticos)
    )

    print(f"[Nexus] Analizando campos críticos para formato {formato}...")
    respuesta_raw = ask_ai(prompt)

    # Limpiamos la respuesta y la parseamos como JSON
    import json, re
    # Extraemos el JSON aunque la IA añada texto extra
    match = re.search(r'\{.*\}', respuesta_raw, re.DOTALL)
    if not match:
        # Si la IA no devolvió JSON válido, asumimos que no faltan campos
        return {
            "campos_faltantes": [],
            "campos_cubiertos": campos_criticos,
            "analisis_breve": "No se pudo analizar — se procede con la expansión"
        }

    try:
        resultado = json.loads(match.group())
        return resultado
    except json.JSONDecodeError:
        return {
            "campos_faltantes": [],
            "campos_cubiertos": campos_criticos,
            "analisis_breve": "Análisis inconcluso — se procede con la expansión"
        }

def generar_pregunta_clarificacion(campos_faltantes: list, formato: str) -> str:
    """
    Genera una pregunta de clarificación amigable para los campos que faltan.
    """
    prompt = QUESTION_PROMPT.format(
        formato=formato,
        campos_faltantes="\n".join(f"- {c}" for c in campos_faltantes)
    )
    return ask_ai(prompt)

def evaluar_idea(idea: str, formato: str) -> dict:
    """
    Función principal del ciclo de clarificación.
    Retorna si la idea está lista para expandirse o si necesita más información.
    
    Retorna un dict con:
    - lista_para_expandir: bool
    - pregunta: str (si no está lista)
    - campos_faltantes: list
    - campos_cubiertos: list
    - analisis: str
    """
    analisis = analizar_campos_faltantes(idea, formato)
    campos_faltantes = analisis.get("campos_faltantes", [])

    if not campos_faltantes:
        return {
            "lista_para_expandir": True,
            "pregunta": None,
            "campos_faltantes": [],
            "campos_cubiertos": analisis.get("campos_cubiertos", []),
            "analisis": analisis.get("analisis_breve", "")
        }

    # Hay campos faltantes — generamos la pregunta
    pregunta = generar_pregunta_clarificacion(campos_faltantes, formato)

    return {
        "lista_para_expandir": False,
        "pregunta": pregunta,
        "campos_faltantes": campos_faltantes,
        "campos_cubiertos": analisis.get("campos_cubiertos", []),
        "analisis": analisis.get("analisis_breve", "")
    }