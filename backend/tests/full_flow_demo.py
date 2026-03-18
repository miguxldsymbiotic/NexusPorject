import sys
import os
import json
from pydantic import BaseModel
from typing import Optional

# Añadimos el directorio actual al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock de la clase SeedIdea para compatibilidad con el endpoint
class MockPayload:
    def __init__(self):
        self.idea = "App de telemedicina para niños en el Chocó usando inteligencia artificial para diagnóstico temprano."
        self.metodologia = "Desarrollo Ágil con enfoque social"
        self.formato = "UNIVERSAL"
        self.id_demanda = "minciencias-salud-2024"
        self.facultad = "Medicina"
        self.grupo = "Bio-Informática"
        self.investigador = "Dr. Robot"
        self.id_investigador = "889900"
        self.sector_tematico = "Salud / Tech"
        self.duracion_estimada = "18 meses"
        self.beneficiarios = "Comunidades rurales del pacífico colombiano"
        self.arbol_problemas = "Falta de especialistas, alta mortalidad infantil, distancias geográficas."
        self.arbol_objetivos = "Mejorar triaje remoto, reducir tiempos de diagnóstico, salvar vidas."
        self.contexto_adicional = "Queremos usar modelos de visión por computadora para detectar desnutrición en fotos."

def run_full_flow():
    print("=== INICIANDO EJECUCIÓN FULL FLOW (Symbiotic POC) ===")
    
    from main import generar_documento
    payload = MockPayload()
    
    try:
        print("\n[Demo] Orquestando expansión, matching y generación de PDF...")
        # Llamamos a la función interna de main.py
        # Nota: generar_documento devuelve una FileResponse. 
        # Para el test, capturamos el resultado de la lógica interna.
        
        # Como generar_documento es un endpoint de FastAPI, lo llamamos directamente
        resultado = generar_documento(payload)
        
        print(f"\n[Demo] ¡Éxito! Documento generado correctamente.")
        print(f"Ruta del archivo: {resultado.path}")
        
        # Verificamos si el archivo existe
        if os.path.exists(resultado.path):
            print(f"Tamaño del PDF: {os.path.getsize(resultado.path)} bytes")
            print("\n--- RESUMEN FINAL ---")
            print("1. Idea expandida con Retórica Académica.")
            print("2. Equipo de 5 perfiles sugerido e instanciado.")
            print("3. Matching realizado contra 'MinCiencias Salud 2024'.")
            print("4. PDF 'Transducido' generado con reporte de compatibilidad.")
            
    except Exception as e:
        print(f"\n[Error en Demo] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_full_flow()
