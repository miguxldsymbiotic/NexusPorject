import json
import os
from typing import List, Dict
from core.ai_client import ask_ai

MATCHER_PROMPT = """
Eres un analista de fondos de inversión y convocatorias. 
Tu tarea es evaluar la COMPATIBILIDAD entre un Proyecto (Formato Universal) y una Demanda específica (Convocatoria).

PROYECTO:
{proyecto_json}

DEMANDA:
{demanda_json}

Responde ÚNICAMENTE con un JSON con esta estructura:
{{
  "compatibilidad_score": 0-100,
  "justificacion": "Breve explicación de por qué este score",
  "brechas_detectadas": ["Lista de requisitos de la demanda que el proyecto no cumple bien"],
  "recomendaciones": ["Pasos para mejorar la compatibilidad"]
}}
"""

def cargar_demandas() -> List[Dict]:
    path = os.path.join(os.path.dirname(__file__), "..", "data", "demands.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_matches(proyecto: Dict) -> List[Dict]:
    """
    Compara el proyecto contra todas las demandas y devuelve los resultados.
    """
    demandas = cargar_demandas()
    resultados = []
    
    # Para el MVP, comparamos contra las 3 primeras demandas para no saturar la API
    for demanda in demandas[:3]:
        prompt = MATCHER_PROMPT.format(
            proyecto_json=json.dumps(proyecto, indent=2),
            demanda_json=json.dumps(demanda, indent=2)
        )
        
        print(f"[Matcher] Evaluando compatibilidad con: {demanda['nombre']}...")
        try:
            respuesta_raw = ask_ai(prompt)
            print(f"[Matcher] Respuesta AI recibida ({len(respuesta_raw)} chars)")
        except Exception as e:
            print(f"[Matcher] Error llamando a AI: {e}")
            continue
        
        # Extraer JSON
        import re
        match = re.search(r'\{.*\}', respuesta_raw, re.DOTALL)
        if match:
            try:
                evaluacion = json.loads(match.group())
                evaluacion["demanda_id"] = demanda["id"]
                evaluacion["demanda_nombre"] = demanda["nombre"]
                resultados.append(evaluacion)
                print(f"[Matcher] Match exitoso: {evaluacion['compatibilidad_score']}%")
            except Exception as e:
                print(f"[Matcher] Error parseando JSON: {e}")
                print(f"Raw: {respuesta_raw[:200]}...")
        else:
            print("[Matcher] No se encontró JSON en la respuesta")
                
    # Ordenar por score de mayor a menor
    resultados.sort(key=lambda x: x.get("compatibilidad_score", 0), reverse=True)
    return resultados
