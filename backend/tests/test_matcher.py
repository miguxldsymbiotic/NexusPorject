import sys
import os
import json

# Añadimos el directorio actual al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_matcher_logic():
    print("PROBANDO LÓGICA DE MATCHING DE DEMANDAS...")
    
    # Proyecto de ejemplo (Telemedicina)
    proyecto_ejemplo = {
        "titulo_proyecto": "App de Telemedicina para el Amazonas",
        "sector_tematico": "Salud, Tecnología",
        "impacto_social": "Reducción de mortalidad infantil en zonas de difícil acceso.",
        "sostenibilidad": "Alianzas con gobiernos locales y modelo suscripción básico.",
        "metodologia": "Uso de tablets y conexión satelital para consultas remotas."
    }
    
    from core.matcher_engine import find_matches
    
    resultados = find_matches(proyecto_ejemplo)
    
    print(f"\nSe encontraron {len(resultados)} matches:")
    for res in resultados:
        print(f"\n--- {res['demanda_nombre']} ---")
        print(f"Score: {res['compatibilidad_score']}%")
        print(f"Justificación: {res['justificacion']}")
        print(f"Brechas: {', '.join(res['brechas_detectadas'])}")
        print(f"Recomendaciones: {', '.join(res['recomendaciones'])}")

if __name__ == "__main__":
    test_matcher_logic()
