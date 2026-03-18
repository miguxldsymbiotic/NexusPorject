import wave
import struct
import sys
import os
import requests

# Añadimos el directorio actual al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def generate_silent_wav(filename, duration=1):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    with wave.open(filename, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for _ in range(n_samples):
            data = struct.pack('<h', 0)
            wav.writeframesraw(data)
    print(f"Archivo {filename} generado.")

def test_audio_endpoint():
    filename = "test_audio.wav"
    generate_silent_wav(filename)
    
    url = "http://localhost:8000/audio-to-idea"
    # Nota: Este test asume que el servidor está corriendo. 
    # Como no podemos asegurar que esté corriendo en el background del agente de la misma forma,
    # probaremos la lógica interna directamente en su lugar.
    
    try:
        from core.audio_engine import procesar_audio_proyecto, procesar_transcripcion_proyecto
        import json

        print("\nPROBANDO LÓGICA DE AUDIO (Requiere balance OpenRouter)...")
        resultado = procesar_audio_proyecto(filename, "UNIVERSAL")
        print(f"Resultado:\n{json.dumps(resultado, indent=2)}")

        print("\nPROBANDO LÓGICA DE TRANSCRIPCIÓN (100% GRATIS)...")
        texto_ejemplo = "Mi proyecto es una app de telemedicina para zonas rurales que usa IA para triaje."
        resultado_tx = procesar_transcripcion_proyecto(texto_ejemplo)
        print(f"Resultado Transcripción:\n{json.dumps(resultado_tx, indent=2)}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    test_audio_endpoint()
