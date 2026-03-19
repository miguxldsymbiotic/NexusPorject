import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from typing import Optional
from core.rhetoric_engine import expand_seed_idea
from core.clarification_engine import evaluar_idea
from core.talent_engine import sugerir_equipo
from core.pdf_engine import generar_pdf
from core.audio_engine import procesar_audio_proyecto
from formats.format_registry import listar_formatos

# Creamos la aplicación web
app = FastAPI(
    title="Project Nexus",
    description="Motor de homologación de propuestas de investigación",
    version="0.4.0"
)

# Carpeta donde se guardan los PDFs generados
PDF_OUTPUT_DIR = "outputs"
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)

# Definimos la estructura del dato que recibe la API
class SeedIdea(BaseModel):
    idea: str
    metodologia: str
    formato: str
    # Campos Académicos
    facultad: Optional[str] = None
    grupo: Optional[str] = None
    investigador: Optional[str] = None
    id_investigador: Optional[str] = None
    # Campos Técnicos (V2.0)
    sector_tematico: Optional[str] = None
    arbol_problemas: Optional[str] = None
    arbol_objetivos: Optional[str] = None
    contexto_adicional: Optional[str] = None
    id_demanda: Optional[str] = None

class EvaluacionRequest(BaseModel):
    idea: str
    formato: str

class TalentRequest(BaseModel):
    idea: str
    formato: str
    metodologia: str
    facultad: Optional[str] = None
    grupo: Optional[str] = None
    investigador: Optional[str] = None

class RefineRequest(BaseModel):
    texto: str
    objetivo: Optional[str] = "profesionalizar"

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/app", response_class=HTMLResponse)
def frontend():
    """Sirve la interfaz web principal."""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/")
def root():
    """Redirige o sirve la app directamente desde la raíz."""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/formatos")
def obtener_formatos():
    return {"formatos": listar_formatos()}

@app.post("/evaluar")
def evaluar(payload: EvaluacionRequest):
    return evaluar_idea(idea=payload.idea, formato=payload.formato)

@app.post("/expandir")
def expandir_idea(payload: SeedIdea):
    idea_completa = payload.idea
    if payload.contexto_adicional:
        idea_completa = f"{payload.idea}\n\nINFORMACIÓN ADICIONAL:\n{payload.contexto_adicional}"
    metadata = {
        "facultad": payload.facultad,
        "grupo": payload.grupo,
        "investigador": payload.investigador,
        "id_investigador": payload.id_investigador,
        "sector_tematico": payload.sector_tematico,
        "arbol_problemas": payload.arbol_problemas,
        "arbol_objetivos": payload.arbol_objetivos
    }
    return expand_seed_idea(
        idea=idea_completa,
        metodologia=payload.metodologia,
        formato=payload.formato,
        metadata=metadata
    )

@app.post("/equipo")
def equipo(payload: TalentRequest):
    return sugerir_equipo(
        idea=payload.idea,
        formato=payload.formato,
        metodologia=payload.metodologia
    )

class EdicionRequest(BaseModel):
    texto_actual: str
    instrucciones: str
    formato: str

class PDFRequest(BaseModel):
    datos: dict
    html_content: Optional[str] = None # Opcional si queremos pasar el texto editado directamente

# ... (otros endpoints)

@app.post("/generar-documento")
def generar_documento(payload: SeedIdea):
    """
    Retorna JSON con el contenido para PREVISUALIZACIÓN.
    """
    print(f"[Nexus] Iniciando flujo de previsualización para: {payload.idea[:40]}...")
    try:
        # Paso 1: Expansión retórica
        idea_completa = payload.idea
        if payload.contexto_adicional:
            idea_completa = f"{payload.idea}\n\nINFORMACIÓN ADICIONAL:\n{payload.contexto_adicional}"

        metadata = {
            "facultad": payload.facultad,
            "grupo": payload.grupo,
            "investigador": payload.investigador,
            "id_investigador": payload.id_investigador,
            "sector_tematico": payload.sector_tematico,
            "arbol_problemas": payload.arbol_problemas,
            "arbol_objetivos": payload.arbol_objetivos
        }

        datos_expansion = expand_seed_idea(
            idea=idea_completa,
            metodologia=payload.metodologia,
            formato=payload.formato,
            metadata=metadata
        )

        # Paso 2: Sugerencia de equipo
        concept_talento = f"CONCEPTO: {payload.idea}\nSECTOR: {payload.sector_tematico}"
        datos_equipo = sugerir_equipo(
            idea=concept_talento,
            formato=payload.formato,
            metodologia=payload.metodologia
        )

        # Paso 3: Matching de validación
        from core.matcher_engine import find_matches
        id_demanda_final = payload.id_demanda
        if not id_demanda_final and payload.formato == "MGA":
            id_demanda_final = "sgr-mga-colombia"
                
        matches = find_matches(datos_expansion)
        match_eval = None
        if id_demanda_final:
            match_eval = next((m for m in matches if m["demanda_id"] == id_demanda_final), None)
        elif matches:
            match_eval = matches[0]

        return {
            "success": True,
            "datos_expansion": datos_expansion,
            "equipo": datos_equipo,
            "match_evaluacion": match_eval,
            "texto_previsualizacion": datos_expansion.get("expansion", ""),
            "metadata": metadata
        }
    except Exception as e:
        print(f"[Nexus] ERROR EN GENERACIÓN: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

@app.post("/editar-propuesta")
def editar_propuesta(payload: EdicionRequest):
    """
    Aplica ediciones estrictas al texto de la propuesta usando IA.
    """
    from core.ai_client import ask_ai
    print(f"[Nexus] Editando propuesta con instrucciones: {payload.instrucciones[:50]}...")
    
    prompt = f"""
    PROHIBICIÓN ABSOLUTA: No devuelvas solo los cambios. No devuelvas resúmenes. 
    DEBES DEVOLVER EL DOCUMENTO COMPLETO, desde el primer ### hasta el último párrafo, incorporando las ediciones solicitadas.
    
    TEXTO ACTUAL:
    ---
    {payload.texto_actual}
    ---
    
    RESPONDE ÚNICAMENTE CON EL TEXTO COMPLETO RE-ESTRUCTURADO Y EDITADO:
    """
    
    nuevo_texto = ask_ai(prompt)
    return {"texto_editado": nuevo_texto}

@app.post("/generar-pdf-final")
def generar_pdf_final(datos: dict):
    """
    Toma los datos finales (posiblemente editados) y genera el archivo PDF.
    """
    # Asegurar que el texto editado pase a la expansión del PDF
    if "texto_editado" in datos:
        datos["expansion"] = datos["texto_editado"]
    
    nombre_archivo = f"nexus_final_{os.urandom(4).hex()}.pdf"
    ruta_pdf = os.path.join(PDF_OUTPUT_DIR, nombre_archivo)
        
    try:
        generar_pdf(datos, ruta_pdf)
        return {
            "pdf_url": f"/descargar-file/{nombre_archivo}",
            "filename": nombre_archivo
        }
    except Exception as e:
        print(f"[Nexus] ERROR GENERANDO PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Fallo en motor PDF: {str(e)}"}

@app.get("/descargar-file/{filename}")
def descargar_file(filename: str):
    ruta = os.path.join(PDF_OUTPUT_DIR, filename)
    if os.path.exists(ruta):
        return FileResponse(ruta, media_type='application/pdf', filename=filename)
    return {"error": "Archivo no encontrado"}

@app.post("/audio-to-idea")
async def audio_to_idea(file: UploadFile = File(...)):
    """
    Endpoint para Audio-to-Form (Requiere balance en OpenRouter para multimodal).
    """
    # Guardar temporalmente el archivo
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        from core.audio_engine import procesar_audio_proyecto
        resultado = procesar_audio_proyecto(temp_path)
        return resultado
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/transcribir-audio")
async def transcribir_audio(file: UploadFile = File(...)):
    """
    Transcribión de audio gratuita usando Google Speech API vía SpeechRecognition (sin API key).
    """
    import speech_recognition as sr
    import tempfile, os
    
    try:
        # Leer el audio en memoria
        audio_bytes = await file.read()
        print(f"[Nexus] Audio recibido: {len(audio_bytes)} bytes")
        
        if len(audio_bytes) == 0:
            return {"transcripcion": "", "error": "El archivo de audio está vacío"}
        
        # Detectar formato por content_type o nombre de archivo
        fname = file.filename or 'audio.webm'
        ext = os.path.splitext(fname)[1].lower() or '.webm'
        content_type = file.content_type or 'audio/webm'
        if 'wav' in content_type or ext == '.wav': audio_fmt = 'wav'
        elif 'ogg' in content_type or ext == '.ogg': audio_fmt = 'ogg'
        else: audio_fmt = 'webm'
        
        with tempfile.NamedTemporaryFile(suffix=f'.{audio_fmt}', delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_src = tmp.name
        
        tmp_wav = tmp_src.rsplit('.', 1)[0] + '.wav'
        
        try:
            if audio_fmt == 'wav':
                tmp_wav = tmp_src  # ya es wav, no convertir
            else:
                # Configurar pydub con ffmpeg de imageio
                import imageio_ffmpeg
                from pydub import AudioSegment
                ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
                AudioSegment.converter = ffmpeg_path
                print(f"[Nexus] Convirtiendo {audio_fmt} -> wav usando {ffmpeg_path}")
                audio_seg = AudioSegment.from_file(tmp_src, format=audio_fmt)
                audio_seg.export(tmp_wav, format='wav')
            
            # Transcribir con Google Speech-to-Text gratuito
            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_wav) as source:
                audio_data = recognizer.record(source)
            
            texto = recognizer.recognize_google(audio_data, language="es-ES")
            print(f"[Nexus] Transcripción exitosa: {texto[:80]}")
            return {"transcripcion": texto}
            
        except sr.UnknownValueError:
            return {"transcripcion": "", "error": "No se pudo entender el audio. Intenta hablar más claro."}
        except sr.RequestError as e:
            return {"transcripcion": "", "error": f"Error en Google Speech API: {e}"}
        finally:
            for f in [tmp_src, tmp_wav]:
                if os.path.exists(f) and f != tmp_src: os.remove(f)
            if os.path.exists(tmp_src): os.remove(tmp_src)

                
    except ImportError:
        return {"transcripcion": "", "error": "Librerías de audio no instaladas. Ejecuta: pip install SpeechRecognition pydub"}
    except Exception as e:
        import traceback; traceback.print_exc()
        return {"transcripcion": "", "error": f"Error interno: {str(e)}"}

@app.post("/transcription-to-idea")
async def transcription_to_idea(data: dict):
    """
    Endpoint Gratuito: Toma una transcripción de texto y la estructura.
    """
    texto = data.get("transcripcion", "")
    formato = data.get("formato", "UNIVERSAL")
    
    if not texto:
        return {"error": "No se proporcionó transcripción"}
        
    from core.audio_engine import procesar_transcripcion_proyecto
    resultado = procesar_transcripcion_proyecto(texto, formato)
    return resultado

@app.post("/match-demands")
async def match_demands(proyecto: dict):
    """
    Compara un proyecto contra el catálogo de demandas y devuelve el ranking de compatibilidad.
    """
    from core.matcher_engine import find_matches
    resultados = find_matches(proyecto)
    return {"matches": resultados}

@app.get("/demands")
async def get_all_demands():
    """
    Lista las demandas disponibles en el catálogo.
    """
    from core.matcher_engine import cargar_demandas
    return {"demandas": cargar_demandas()}

@app.post("/refinar-texto")
async def refinar_texto(payload: RefineRequest):
    """
    Refina un texto (idea, título, etc.) usando IA profesional.
    """
    from core.ai_client import ask_ai
    prompt = f"Actúa como un experto en redacción de proyectos de investigación. Refina el siguiente texto con el objetivo de '{payload.objetivo}':\n\n{payload.texto}\n\nDevuelve solo el texto refinado, con un tono académico y técnico, sin comentarios adicionales."
    try:
        resultado = ask_ai(prompt)
        return {"texto_refinado": resultado.strip()}
    except Exception as e:
        return {"error": str(e)}