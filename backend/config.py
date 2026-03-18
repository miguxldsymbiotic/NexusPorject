import os
from dotenv import load_dotenv

load_dotenv()

# Credenciales
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Modelo — llama-3.3-70b es el más capaz en el tier gratuito de Groq
AI_MODEL = "llama-3.3-70b-versatile"

# Validación al arrancar
if not GROQ_API_KEY:
    raise ValueError("No se encontró GROQ_API_KEY en el archivo .env")
