import json
import os
from core.ai_client import ask_ai
from formats.format_registry import get_formato

def cargar_investigadores() -> list:
    """Carga la base de datos de investigadores desde el archivo JSON."""
    ruta = os.path.join(os.path.dirname(__file__), '..', 'data', 'researchers.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['investigadores']

TALENT_MATCH_PROMPT = """
Eres un experto en gestión de talento investigador y formulación de proyectos.

Se necesita conformar el equipo ideal para el siguiente proyecto:
---
IDEA DEL PROYECTO: {idea}
FORMATO DE CONVOCATORIA: {formato} ({formato_nombre})
METODOLOGÍA: {metodologia}
---

Los campos críticos que debe cubrir el equipo son:
{campos_criticos}

Los siguientes investigadores están disponibles en la base de datos:
{perfiles}

Tu tarea es seleccionar el equipo óptimo (entre 3 y 5 personas) considerando:
1. Complementariedad de expertises para cubrir todos los campos críticos
2. Experiencia previa con el formato de convocatoria específico
3. Balance entre investigadores senior (PhD) y de apoyo (Magíster)
4. Diversidad institucional cuando sea posible

Responde ÚNICAMENTE con un objeto JSON con esta estructura exacta, sin texto adicional:
{{
  "equipo_sugerido": [
    {{
      "id": "INV001",
      "rol": "Investigador Principal",
      "justificacion": "Razón específica de 1-2 oraciones",
      "dedicacion_porcentaje": 50
    }}
  ],
  "justificacion_equipo": "Párrafo explicando por qué este equipo es ideal para el proyecto",
  "advertencias": ["Advertencia si hay alguna debilidad del equipo"]
}}
"""

def sugerir_equipo(idea: str, formato: str, metodologia: str) -> dict:
    """
    Analiza el proyecto y sugiere el equipo investigador ideal
    de la base de datos disponible.
    """
    investigadores = cargar_investigadores()
    clase_formato = get_formato(formato)

    # Preparamos el resumen de perfiles para el prompt
    perfiles_texto = ""
    for inv in investigadores:
        perfiles_texto += f"""
ID: {inv['id']} | {inv['nombre']} ({inv['titulo']})
  Institución: {inv['institucion']}
  Expertises: {', '.join(inv['areas_expertise'])}
  Experiencia en formatos: {', '.join(inv['experiencia_convocatorias'])}
  Proyectos anteriores: {inv['proyectos_anteriores']} | Publicaciones: {inv['publicaciones_indexadas']}
  Disponibilidad: {inv['disponibilidad']}
"""

    prompt = TALENT_MATCH_PROMPT.format(
        idea=idea,
        formato=formato,
        formato_nombre=clase_formato.nombre,
        metodologia=metodologia,
        campos_criticos="\n".join(f"- {c}" for c in clase_formato.get_campos_criticos()),
        perfiles=perfiles_texto
    )

    print(f"[Nexus] Analizando perfiles para match de talento...")
    respuesta_raw = ask_ai(prompt)

    # Parseamos el JSON de respuesta
    import re
    match = re.search(r'\{.*\}', respuesta_raw, re.DOTALL)
    if not match:
        return {"error": "No se pudo generar sugerencia de equipo", "raw": respuesta_raw}

    try:
        resultado = json.loads(match.group())

        # Enriquecemos la respuesta con los datos completos de cada investigador
        investigadores_dict = {inv['id']: inv for inv in investigadores}
        for miembro in resultado.get('equipo_sugerido', []):
            inv_id = miembro.get('id')
            if inv_id in investigadores_dict:
                miembro['perfil_completo'] = investigadores_dict[inv_id]

        return resultado
    except json.JSONDecodeError:
        return {"error": "Error al parsear respuesta", "raw": respuesta_raw}