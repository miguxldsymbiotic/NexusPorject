import os
from dotenv import load_dotenv

load_dotenv()

# Credenciales
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Nueva API Cerebras (Migración)
CEREBRAS_API_KEY = "csk-yd4pppryxwj5ppk6edyfjdhnd85hccv9wvc8e2errmvyexrj"

# Modelo de IA (Cerebras - Qwen Ultra-Fast)
AI_MODEL = "qwen-3-235b-a22b-instruct-2507" 
AI_PROVIDER = "CEREBRAS"

# Validación al arrancar
if not CEREBRAS_API_KEY and AI_PROVIDER == "CEREBRAS":
    print("WARNING: No se encontró CEREBRAS_API_KEY")
