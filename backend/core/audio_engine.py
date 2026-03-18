import base64
import os
from core.ai_client import ask_ai_multimodal
from formats.format_registry import get_formato

AUDIO_EXTRACTION_PROMPT = """
Eres un asistente experto en transcripción y estructuración de proyectos de innovación.
Se te proporciona un audio donde un usuario explica su idea de proyecto de forma desestructurada.

Tu tarea es:
1. Escuchar y transcribir fielmente el contenido.
2. Extraer y organizar la información para completar los campos del formato {formato}:
   Campos a identificar: {campos}

INSTRUCCIONES:
- Si el usuario menciona el problema, ponlo en 'problema_central'.
- Si menciona objetivos, ponlos en 'objetivo_general' o similar.
- Si no menciona información para un campo, deja el valor como cadena vacía "".
- Sé profesional en la redacción de los datos extraídos, manteniendo la intención del usuario.

Responde ÚNICAMENTE con un objeto JSON con esta estructura exacta:
{{
  "transcripcion": "Texto completo de lo que dijo el usuario",
  "datos_extraidos": {{
    "campo_n": "valor_extraido"
  }},
  "meta": {{
    "formato": "{formato}",
    "calidad_audio": "Alta/Media/Baja"
  }}
}}
"""

def procesar_audio_proyecto(ruta_audio: str, formato: str = "UNIVERSAL") -> dict:
    """
    Lee un archivo de audio, lo envía a la IA y retorna la información estructurada.
    """
    if not os.path.exists(ruta_audio):
        raise FileNotFoundError(f"No se encontró el archivo de audio: {ruta_audio}")

    # 1. Leer y codificar a Base64
    with open(ruta_audio, "rb") as audio_file:
        audio_data = audio_file.read()
        audio_b64 = base64.b64encode(audio_data).decode('utf-8')

    # 2. Preparar campos del formato
    clase_formato = get_formato(formato)
    campos = ", ".join(clase_formato.get_campos_obligatorios())

    # 3. Preparar prompt
    prompt = AUDIO_EXTRACTION_PROMPT.format(
        formato=formato,
        campos=campos
    )

    # 4. Determinar MIME Type (simple)
    ext = os.path.splitext(ruta_audio)[1].lower()
    mime = "audio/mpeg"
    if ext == ".wav": mime = "audio/wav"
    elif ext == ".ogg": mime = "audio/ogg"

    # 5. Consultar IA
    print(f"[Nexus] Procesando audio de {len(audio_data)} bytes...")
    respuesta_raw = ask_ai_multimodal(prompt, audio_b64, mime)

    # 6. Parsear JSON
    import json, re
    match = re.search(r'\{.*\}', respuesta_raw, re.DOTALL)
    if not match:
        return {
            "error": "No se pudo extraer información del audio",
            "raw": respuesta_raw
        }

    try:
        data = json.loads(match.group())
        return data
    except Exception as e:
        print(f"[Nexus] Error parsing JSON audio output: {e}")
        return {
            "error": "Respuesta AI no válida",
            "raw": respuesta_raw
        }

# --- NUEVA LÓGICA: Procesar Texto/Transcripción (100% Gratis) ---

TRANSCRIPTION_MAPPING_PROMPT = """
Eres un experto en estructuración de proyectos. 
Se te proporciona el texto de una transcripción de un usuario describiendo su idea.

Tu tarea es extraer la información para completar los campos del formato {formato}:
Campos del formato a extraer: {campos}

Responde ÚNICAMENTE con un JSON con esta estructura:
{{
  "datos_extraidos": {{ "nombre_campo": "valor extraído" }},
  "mensaje": "Resumen breve de lo que logré extraer"
}}
"""

def procesar_transcripcion_proyecto(texto: str, formato: str = "UNIVERSAL") -> dict:
    """
    Versión gratuita que procesa solo texto (transcripción hecha por el frontend 
    o pegada por el usuario) y la estructura en campos de proyecto.
    """
    from formats.format_registry import get_formato
    from core.ai_client import ask_ai
    import json, re

    clase_formato = get_formato(formato)
    instancia = clase_formato()
    # Usamos campos obligatorios como guía
    campos = ", ".join(instancia.get_campos_obligatorios())
    
    prompt = TRANSCRIPTION_MAPPING_PROMPT.format(
        formato=formato, 
        campos=campos
    )
    
    print(f"[Nexus] Estructurando transcripción de {len(texto)} caracteres...")
    respuesta_raw = ask_ai(f"{prompt}\n\nTranscripción:\n{texto}")
    
    match = re.search(r'\{.*\}', respuesta_raw, re.DOTALL)
    if not match: 
        return {"error": "No se pudo estructurar la transcripción", "raw": respuesta_raw}
        
    try:
        return json.loads(match.group())
    except Exception as e:
        print(f"[Nexus] Error JSON en transcripción: {e}")
        return {"error": "AI devolvió JSON inválido", "raw": respuesta_raw}
