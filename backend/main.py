import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from typing import Optional
from core.rhetoric_engine import expand_seed_idea
from core.clarification_engine import evaluar_idea
from core.talent_engine import sugerir_equipo
from core.pdf_engine import generar_pdf
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
    contexto_adicional: Optional[str] = None

class EvaluacionRequest(BaseModel):
    idea: str
    formato: str

class TalentRequest(BaseModel):
    idea: str
    formato: str
    metodologia: str

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/app", response_class=HTMLResponse)
def frontend():
    """Sirve la interfaz web principal."""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/")
def root():
    return {"mensaje": "Project Nexus activo", "version": "0.4.0"}

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
    return expand_seed_idea(
        idea=idea_completa,
        metodologia=payload.metodologia,
        formato=payload.formato
    )

@app.post("/equipo")
def equipo(payload: TalentRequest):
    return sugerir_equipo(
        idea=payload.idea,
        formato=payload.formato,
        metodologia=payload.metodologia
    )

@app.post("/generar-documento")
def generar_documento(payload: SeedIdea):
    """
    Endpoint principal — orquesta todo el flujo completo:
    1. Expande la idea retóricamente
    2. Sugiere el equipo investigador
    3. Genera el PDF profesional
    4. Retorna el archivo para descarga
    """
    print(f"[Nexus] Iniciando generación de documento completo...")

    # Paso 1: Expansión retórica
    idea_completa = payload.idea
    if payload.contexto_adicional:
        idea_completa = f"{payload.idea}\n\nINFORMACIÓN ADICIONAL:\n{payload.contexto_adicional}"

    datos_expansion = expand_seed_idea(
        idea=idea_completa,
        metodologia=payload.metodologia,
        formato=payload.formato
    )

    # Paso 2: Sugerencia de equipo
    datos_equipo = sugerir_equipo(
        idea=idea_completa,
        formato=payload.formato,
        metodologia=payload.metodologia
    )

    # Paso 3: Compilar todos los datos
    datos_completos = {
        **datos_expansion,
        "equipo": datos_equipo,
    }

    # Paso 4: Generar PDF
    nombre_archivo = f"nexus_{payload.formato.lower()}_{os.urandom(4).hex()}.pdf"
    ruta_pdf = os.path.join(PDF_OUTPUT_DIR, nombre_archivo)
    generar_pdf(datos_completos, ruta_pdf)

    # Paso 5: Retornar el PDF como descarga
    return FileResponse(
        path=ruta_pdf,
        media_type='application/pdf',
        filename=nombre_archivo
    )