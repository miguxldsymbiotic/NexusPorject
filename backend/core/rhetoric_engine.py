from core.ai_client import ask_ai
from formats.format_registry import get_formato
import time

SECTIONAL_PROMPT_TEMPLATE = """
Eres un experto de élite en formulación de proyectos de I+D+i. 
Estás trabajando en una propuesta de alto impacto para: {formato_nombre}.

CONCEPTO INICIAL Y METADATA:
{idea_y_metadata}

SECCIÓN ACTUAL A DESARROLLAR: {seccion_nombre}
OBJETIVO DE ESTA SECCIÓN:
{seccion_prompt}

CONTEXTO DE SECCIONES ANTERIORES:
{contexto_previo}

REQUERIMIENTOS:
- Mantén el hilo conductor.
- Usa terminología experta de {formato_nombre}.
- No repitas información ya escrita en secciones anteriores, busca expandir y profundizar.
- El resultado debe ser riguroso, técnico y persuasivo.

Genera el contenido de esta sección ahora:
"""

REVIEW_PROMPT_TEMPLATE = """
Eres un evaluador de élite de propuestas de I+D+i para {formato_nombre}.
Has recibido la propuesta generada a continuación. Tu objetivo es convertirla en una VERSIÓN PREMIUM DE GRADO PROFESIONAL.

ESTRICTAMENTE REQUERIDO:
1. PROHIBICIÓN DE PLACEHOLDERS: Elimina cualquier "N/A", "Por definir", "TBD", "[Inserte aquí]" o campos vacíos.
2. GENERACIÓN REALISTA: Si falta un dato técnico, presupuestario o de población, INVÉNTALO de forma coherente y profesional basándote en el contexto del proyecto (ej. si es salud en Chocó, usa cifras reales de población de esa región).
3. ESTRUCTURA DE TABLAS: Asegúrate de que presupuestos, riesgos e indicadores estén en tablas Markdown claras (| Col 1 | Col 2 |).
4. TONO: Debe ser 100% formal, académico y persuasivo.

Propuesta a procesar:
---
{propuesta_completa}
---

Devuelve la VERSIÓN FINAL REVISADA Y OPTIMIZADA. No incluyas comentarios externos, solo el contenido de la propuesta.
"""

def expand_seed_idea(idea: str, metodologia: str, formato: str, metadata: dict = None) -> dict:
    clase_formato = get_formato(formato)
    secciones = clase_formato.get_secciones()
    
    meta_str = ""
    if metadata:
        meta_str = "\nMETADATA ACADÉMICA:"
        for k, v in metadata.items():
            if v: meta_str += f"\n- {k.replace('_', ' ').title()}: {v}"

    idea_full = f"IDEA SEMILLA: {idea}\nMETODOLOGÍA: {metodologia}{meta_str}"
    
    if formato == "MGA":
        idea_full += "\n\nNOTA CRÍTICA PARA MGA: El usuario ha optado por NO llenar campos de población o duración manualmente para agilizar. TU TAREA ES ESTIMAR ESTOS DATOS con precisión profesional basándote en la idea y el sector Colombiano indicado. NO uses N/A."
    
    propuesta_partes = []
    contexto_acumulado = "Inicio del proyecto."

    print(f"[Nexus] Iniciando Generación de Alta Fidelidad en {len(secciones)} secciones para {formato}...")

    for i, sec in enumerate(secciones):
        print(f"[Nexus] Generando sección {i+1}/{len(secciones)}: {sec['nombre']}...")
        
        prompt_sec = SECTIONAL_PROMPT_TEMPLATE.format(
            formato_nombre=clase_formato.nombre,
            idea_y_metadata=idea_full,
            seccion_nombre=sec['nombre'],
            seccion_prompt=sec['prompt'],
            contexto_previo=contexto_acumulado
        )
        
        contenido_sec = ask_ai(prompt_sec)
        propuesta_partes.append(f"### {sec['nombre']}\n\n{contenido_sec}")
        
        # Limitar contexto acumulado para no saturar la ventana de contexto de la IA
        contexto_acumulado += f"\n\nResumen de {sec['nombre']}: {contenido_sec[:1200]}..."
        
        # Pacing estricto para evitar bloqueos por Rate Limit de la capa gratuita (Cerebras)
        time.sleep(4)

    propuesta_final_cruda = "\n\n".join(propuesta_partes)

    print(f"[Nexus] Realizando paso de Verificación y Pulido con IA (Regla de No Placeholders)...")
    prompt_review = REVIEW_PROMPT_TEMPLATE.format(
        formato_nombre=clase_formato.nombre,
        propuesta_completa=propuesta_final_cruda
    )
    
    propuesta_refinada = ask_ai(prompt_review)

    # Red de seguridad: si la revisión falla, devuelve vacío o se trunca drásticamente
    # Comprobación estricta: ¿La última sección sobrevivió a la revisión?
    last_section_name = secciones[-1]['nombre']
    last_sec_present = last_section_name.lower() in propuesta_refinada.lower()

    if not propuesta_refinada or propuesta_refinada.strip() == "" or propuesta_refinada.startswith("Error") or not last_sec_present or len(propuesta_refinada) < (len(propuesta_final_cruda) * 0.85):
        print(f"[Nexus] ADVERTENCIA: La revisión de IA se truncó o falló. Última sección presente: {last_sec_present}. Longitud: {len(propuesta_refinada)} vs {len(propuesta_final_cruda)}. Usando versión cruda completa.")
        propuesta_refinada = propuesta_final_cruda
    else:
        print(f"[Nexus] Revisión completada con éxito ({len(propuesta_refinada)} caracteres).")

    # El diccionario de retorno ahora incluye la metadata para que el motor de PDF la use en la Ficha Técnica
    resultado = {
        "estado": "expandido_alta_fidelidad",
        "formato": formato,
        "formato_nombre": clase_formato.nombre,
        "metodologia": metodologia,
        "idea_original": idea,
        "campos_obligatorios": clase_formato.get_campos_obligatorios(),
        "campos_criticos": clase_formato.get_campos_criticos(),
        "expansion": propuesta_refinada
    }
    
    if metadata:
        resultado.update(metadata)
        
    return resultado