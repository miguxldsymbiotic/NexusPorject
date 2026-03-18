import sys
import os
from dotenv import load_dotenv

# Añadir el directorio actual al path para importar core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from core.rhetoric_engine import expand_seed_idea

def test_horizon_generation():
    idea = "Sistema IA para monitoreo de biodiversidad en el Amazonas usando sensores acústicos y drones"
    metodologia = "Marco Lógico"
    formato = "HORIZONTE"
    metadata = {
        "facultad": "Ingeniería / Ciencias Ambientales",
        "grupo": "BioAI Research Group",
        "investigador": "Dr. Sarah Miller"
    }

    print("--- INICIANDO TEST DE GENERACIÓN SECCIONAL (HORIZONTE) ---")
    resultado = expand_seed_idea(idea, metodologia, formato, metadata)
    
    print("\n--- RESULTADO FINAL ---\n")
    print(f"Estado: {resultado['estado']}")
    print(f"Formato: {resultado['formato_nombre']}")
    print("\nContenido Generado:\n")
    print(resultado['expansion'])
    
    # Guardar en un archivo para revisión
    with open("proposal_horizon_v2.md", "w", encoding="utf-8") as f:
        f.write(resultado['expansion'])
    print(f"\n[Test] Propuesta guardada en proposal_horizon_v2.md")

if __name__ == "__main__":
    test_horizon_generation()
