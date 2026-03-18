import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.clarification_engine import evaluar_idea
from core.rhetoric_engine import expand_seed_idea

def demo_validacion():
    idea = "Sistema de telemedicina para zonas rurales con IA para pre-diagnóstico."
    formato = "UNIVERSAL"
    metodologia = "Investigación-Acción"
    
    print(f"--- VALIDACIÓN FASE 2 ---")
    print(f"Idea: {idea}")
    
    # 1. Evaluar (Gap Analysis)
    print("\n1. EJECUTANDO GAP ANALYSIS...")
    res_eval = evaluar_idea(idea, formato)
    analisis = res_eval['analisis_completo']
    print(f"Puntuación Maestra: {analisis.get('puntuacion_maestra')}/100")
    print("Brechas detectadas:")
    for item in analisis.get('analisis_detallado', []):
        if item['nivel_madurez'] != 'Verde':
            print(f"  - [{item['nivel_madurez']}] {item['campo']}: {item['observacion']}")

    # 2. Expandir (Rhetoric Engine)
    print("\n2. EJECUTANDO EXPANSIÓN RETÓRICA (Simulación de flujo aprobado)...")
    res_exp = expand_seed_idea(idea, metodologia, formato)
    print("\n--- RESULTADO DE EXPANSIÓN (Fragmento) ---")
    print(res_exp['expansion'][:1000] + "...")

if __name__ == "__main__":
    demo_validacion()
