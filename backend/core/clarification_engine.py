from core.ai_client import ask_ai
from formats.format_registry import get_formato

# Prompt que le pide a la IA analizar qué falta en la idea
ANALYSIS_PROMPT = """
Eres un revisor experto en formulación de proyectos para convocatorias {formato}.
Tu objetivo es realizar un "Gap Analysis" (Detección de Brechas) técnico y riguroso.

Se te presenta una idea de proyecto:
---
{idea}
---

Los siguientes campos son CRÍTICOS para el formato {formato}:
{campos_criticos}

Tu tarea es evaluar la presencia y madurez de cada campo crítico en la descripción proporcionada.
Para cada campo, asigna un "nivel_madurez":
- "Verde": El campo está claramente definido, con detalles técnicos y coherencia.
- "Amarillo": El campo se menciona o se insinúa, pero le falta profundidad, datos o justificación.
- "Rojo": El campo está totalmente ausente o lo que se dice es irrelevante/insuficiente.

Responde ÚNICAMENTE con un objeto JSON con esta estructura exacta, sin texto adicional:
{{
  "analisis_detallado": [
    {{
      "campo": "nombre_del_campo",
      "nivel_madurez": "Verde/Amarillo/Rojo",
      "observacion": "Breve explicación de por qué tiene ese nivel y qué falta específicamente."
    }}
  ],
  "analisis_general": "Una sola oración explicando el estado global de la propuesta.",
  "puntuacion_maestra": 0-100
}}
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
    Analiza la madurez de los campos críticos del formato solicitado.
    """
    clase_formato = get_formato(formato)
    campos_criticos = clase_formato.get_campos_criticos()

    prompt = ANALYSIS_PROMPT.format(
        idea=idea,
        formato=formato,
        campos_criticos="\n".join(f"- {c}" for c in campos_criticos)
    )

    print(f"[Nexus] Realizando Gap Analysis (Brechas) para formato {formato}...")
    respuesta_raw = ask_ai(prompt)

    import json, re
    match = re.search(r'\{.*\}', respuesta_raw, re.DOTALL)
    if not match:
        print(f"[DEBUG] Respuesta raw sin JSON: {respuesta_raw}")
        return {
            "analisis_detallado": [],
            "analisis_general": "Error en el análisis de IA.",
            "puntuacion_maestra": 0
        }

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {
            "analisis_detallado": [],
            "analisis_general": "Análisis corrupto de IA.",
            "puntuacion_maestra": 0
        }

def generar_pregunta_clarificacion(analisis_detallado: list, formato: str) -> str:
    """
    Genera una pregunta amigable basada en los campos con nivel Rojo o Amarillo.
    """
    campos_debiles = [
        f"{item['campo']} ({item['observacion']})" 
        for item in analisis_detallado 
        if item['nivel_madurez'] in ['Rojo', 'Amarillo']
    ]
    
    prompt = QUESTION_PROMPT.format(
        formato=formato,
        campos_faltantes="\n".join(campos_debiles)
    )
    return ask_ai(prompt)

def evaluar_idea(idea: str, formato: str) -> dict:
    """
    Evalúa la idea y determina si requiere clarificación o puede expandirse.
    """
    analisis = analizar_campos_faltantes(idea, formato)
    detallado = analisis.get("analisis_detallado", [])
    
    # Decidimos si expandir: Si no hay "Rojos" y la puntuación es > 60
    rojos = [c for c in detallado if c['nivel_madurez'] == 'Rojo']
    puntuacion = analisis.get("puntuacion_maestra", 0)
    
    lista_para_expandir = len(rojos) == 0 and puntuacion >= 60

    if lista_para_expandir:
        return {
            "lista_para_expandir": True,
            "pregunta": None,
            "analisis_completo": analisis
        }

    # Necesita más información
    pregunta = generar_pregunta_clarificacion(detallado, formato)

    return {
        "lista_para_expandir": False,
        "pregunta": pregunta,
        "analisis_completo": analisis
    }