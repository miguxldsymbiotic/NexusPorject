from groq import Groq
from config import GROQ_API_KEY, AI_MODEL

_client = Groq(api_key=GROQ_API_KEY)

def ask_ai(prompt: str) -> str:
    """
    Envía un prompt a Groq y retorna la respuesta como texto.
    Usa llama-3.3-70b, un modelo de lenguaje de alto rendimiento y gratuito.
    """
    response = _client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Eres un experto en formulación de proyectos de investigación e innovación para convocatorias latinoamericanas e internacionales."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=4096
    )
    return response.choices[0].message.content