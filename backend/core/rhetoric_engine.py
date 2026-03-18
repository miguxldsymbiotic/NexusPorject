from core.ai_client import ask_ai
from formats.format_registry import get_formato

RHETORIC_PROMPT_TEMPLATE = """
Eres un experto en formulación de proyectos de investigación e innovación con 15 años 
de experiencia en convocatorias nacionales e internacionales.

Se te presenta la siguiente idea semilla de proyecto:
---
{idea}
---

Metodología deseada: {metodologia}
Formato de destino: {formato}

{instrucciones_formato}

Con base en todo lo anterior, expande esta idea semilla en una descripción técnica 
preliminar completa y rigurosa. Usa lenguaje técnico, preciso y académico en español 
colombiano formal. Cada sección debe ser sustancial y demostrar profundidad de análisis.
"""

def expand_seed_idea(idea: str, metodologia: str, formato: str) -> dict:
    # Carga las instrucciones específicas del formato solicitado
    clase_formato = get_formato(formato)
    instrucciones = clase_formato.get_prompt_instructions()

    prompt = RHETORIC_PROMPT_TEMPLATE.format(
        idea=idea,
        metodologia=metodologia,
        formato=formato,
        instrucciones_formato=instrucciones
    )

    print(f"[Nexus] Enviando idea a IA para expansión retórica...")
    print(f"[Nexus] Formato: {formato} | Metodología: {metodologia}")

    respuesta_raw = ask_ai(prompt)

    return {
        "estado": "expandido",
        "formato": formato,
        "formato_nombre": clase_formato.nombre,
        "metodologia": metodologia,
        "idea_original": idea,
        "campos_obligatorios": clase_formato.get_campos_obligatorios(),
        "campos_criticos": clase_formato.get_campos_criticos(),
        "expansion": respuesta_raw
    }