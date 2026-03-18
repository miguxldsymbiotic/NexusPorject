import os
import requests
import json
from config import OPENROUTER_API_KEY, CEREBRAS_API_KEY, AI_MODEL, AI_PROVIDER

def ask_ai(prompt: str, system_prompt: str = "Eres un experto en formulación de proyectos de I+D+i.") -> str:
    """
    Envía una consulta a la IA (Cerebras o OpenRouter) según la configuración.
    """
    if AI_PROVIDER == "CEREBRAS":
        if not CEREBRAS_API_KEY:
            return "ERROR: No hay API Key configurada para Cerebras."
        url = "https://api.cerebras.ai/v1/chat/completions"
        api_key = CEREBRAS_API_KEY
    else:
        if not OPENROUTER_API_KEY:
            return "ERROR: No hay API Key configurada para OpenRouter."
        url = "https://openrouter.ai/api/v1/chat/completions"
        api_key = OPENROUTER_API_KEY

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Headers adicionales para OpenRouter si es el caso
    if AI_PROVIDER == "OPENROUTER":
        headers["HTTP-Referer"] = "http://localhost:8000"
        headers["X-Title"] = "Project Nexus"

    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 16384
    }

    try:
        print(f"[Nexus] Consultando a {AI_PROVIDER} ({AI_MODEL})...")
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        
        if response.status_code == 402:
            return f"Error: {AI_PROVIDER} solicita pago (402). El saldo de la cuenta se ha agotado."
        
        response.raise_for_status()
        data = response.json()
        
        if 'choices' in data and len(data['choices']) > 0:
            return data['choices'][0]['message']['content']
        else:
            return f"Error: Respuesta inesperada de {AI_PROVIDER}: {json.dumps(data)}"
            
    except Exception as e:
        print(f"Error en {AI_PROVIDER}: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Detalle error: {e.response.text}")
        return f"Error al conectar con la IA ({AI_PROVIDER}): {str(e)}"

def ask_ai_multimodal(prompt: str, audio_base64: str = None, audio_mime: str = "audio/mpeg") -> str:
    """
    Versión multimodal. 
    NOTA: Cerebras no soporta multimodal nativo por ahora. 
    Usaremos OpenRouter si se requiere procesamiento de audio, de lo contrario devolvemos error.
    """
    if AI_PROVIDER == "CEREBRAS":
        # Por ahora Cerebras solo soporta texto. 
        # Si el usuario quiere audio, deberíamos usar un STT separado o volver a OpenRouter.
        # En este POC, simplemente avisamos.
        return "Nexus: Cerebras es texto-puro actualmente. Por favor escribe tu idea o recarga OpenRouter."

    # Lógica anterior de OpenRouter para multimodal
    if not OPENROUTER_API_KEY: return "Error: No APK Key para audio."
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = { "Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json" }
    content = [{"type": "text", "text": prompt}]
    if audio_base64:
        content.append({
            "type": "input_audio",
            "input_audio": { "data": audio_base64, "format": "mp3" }
        })
    payload = { "model": "google/gemini-2.0-flash-001", "messages": [{"role": "user", "content": content}] }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=90)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e: return f"Error en multimodal: {str(e)}"