import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Frame, PageTemplate
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas

# ── Paleta de colores profesional ─────────────────────────────────
C_PRIMARIO      = HexColor('#0f2d52')   # Azul marino oscuro
C_SECUNDARIO    = HexColor('#1a56a0')   # Azul medio
C_ACENTO        = HexColor('#e8772e')   # Naranja institucional
C_TEXTO         = HexColor('#1f2937')   # Casi negro
C_TEXTO_SUAVE   = HexColor('#4b5563')   # Gris oscuro
C_LINEA         = HexColor('#e5e7eb')   # Gris muy claro
C_FONDO_TABLA   = HexColor('#f8fafc')   # Blanco azulado
C_FONDO_HEADER  = HexColor('#eef2f7')   # Azul muy claro
C_VERDE         = HexColor('#059669')   # Verde esmeralda
C_VERDE_FONDO   = HexColor('#ecfdf5')
C_NARANJA_FONDO = HexColor('#fff7ed')
C_NARANJA_BORDE = HexColor('#fed7aa')
C_ROJO          = HexColor('#dc2626')   # Rojo para brechas
C_CRITICO       = HexColor('#b45309')

PAGE_W, PAGE_H = A4
MARGIN_L = 2.2 * cm
MARGIN_R = 2.2 * cm
MARGIN_T = 2.5 * cm
MARGIN_B = 2.2 * cm
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

MESES_ES = {
    'January': 'enero', 'February': 'febrero', 'March': 'marzo',
    'April': 'abril', 'May': 'mayo', 'June': 'junio',
    'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
    'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
}

def fecha_es():
    ahora = datetime.now()
    mes = MESES_ES[ahora.strftime('%B')]
    return ahora.strftime(f'%d de {mes} de %Y')


# ── Flowables personalizados ──────────────────────────────────────
class SeccionHeader(Flowable):
    """Encabezado de sección con barra de color lateral izquierda."""
    def __init__(self, numero, titulo, ancho=CONTENT_W):
        Flowable.__init__(self)
        self.numero  = numero
        self.titulo  = titulo
        self.ancho   = ancho
        self.altura  = 1.1 * cm

    def draw(self):
        c = self.canv
        c.setFillColor(C_FONDO_HEADER)
        c.roundRect(0, 0, self.ancho, self.altura, 4, fill=1, stroke=0)
        c.setFillColor(C_ACENTO)
        c.rect(0, 0, 4, self.altura, fill=1, stroke=0)
        c.setFillColor(C_ACENTO)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(10, self.altura / 2 - 3, self.numero)
        c.setFillColor(C_PRIMARIO)
        c.setFont('Helvetica-Bold', 12)
        c.drawString(32, self.altura / 2 - 4, self.titulo.upper())

    def wrap(self, *args):
        return (self.ancho, self.altura + 6)

class BarraProgreso(Flowable):
    """Barra de progreso visual para el matching score."""
    def __init__(self, porcentaje, ancho=CONTENT_W, alto=18, color=C_VERDE):
        Flowable.__init__(self)
        self.porcentaje = min(100, max(0, porcentaje))
        self.ancho = ancho
        self.alto = alto
        self.color = color

    def draw(self):
        c = self.canv
        c.setFillColor(C_LINEA)
        c.roundRect(0, 0, self.ancho, self.alto, self.alto/2, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0, 0, (self.ancho * self.porcentaje) / 100.0, self.alto, self.alto/2, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(self.ancho/2, self.alto/2 - 3, f"{self.porcentaje}% COMPATIBILIDAD CON REQUISITOS")

    def wrap(self, *args):
        return (self.ancho, self.alto + 5)

# ── Estilos de página ─────────────────────────────────────────────
LOGO_PATH = os.path.join(os.path.dirname(__file__), '..', 'static', 'logo_nexus.png')

def on_primera_pagina(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(HexColor('#f1f5f9'))
    canvas.circle(PAGE_W, PAGE_H, 4.5*cm, fill=1, stroke=0)
    if os.path.exists(LOGO_PATH):
        from reportlab.lib.utils import ImageReader
        try:
            img = ImageReader(LOGO_PATH)
            canvas.drawImage(img, MARGIN_L, PAGE_H - 2.5*cm, width=1.5*cm, height=1.5*cm, mask='auto')
        except: pass
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(C_PRIMARIO)
    canvas.drawString(MARGIN_L + 1.8*cm, PAGE_H - 2*cm, "PROJECT NEXUS / SYMBIOTIC")
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(C_TEXTO_SUAVE)
    canvas.drawString(MARGIN_L + 1.8*cm, PAGE_H - 2.4*cm, "Motor de Inteligencia para Propuestas Académicas")
    agregar_pie_pagina(canvas, doc, doc.formato_nombre, doc.fecha_str)
    canvas.restoreState()

def on_paginas_siguientes(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(C_LINEA)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, PAGE_H - 1.5*cm, PAGE_W - MARGIN_R, PAGE_H - 1.5*cm)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.setFillColor(C_TEXTO_SUAVE)
    canvas.drawString(MARGIN_L, PAGE_H - 1.35*cm, "NEXUS · Propuesta Técnica")
    agregar_pie_pagina(canvas, doc, doc.formato_nombre, doc.fecha_str)
    canvas.restoreState()

def agregar_pie_pagina(canvas, doc, formato_nombre, fecha):
    canvas.setStrokeColor(C_LINEA)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, MARGIN_B - 2*mm, PAGE_W - MARGIN_R, MARGIN_B - 2*mm)
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(C_TEXTO_SUAVE)
    canvas.drawString(MARGIN_L, MARGIN_B - 6*mm, f'Symbiotic Nexus · {formato_nombre}')
    canvas.drawCentredString(PAGE_W / 2, MARGIN_B - 6*mm, fecha)
    canvas.drawRightString(PAGE_W - MARGIN_R, MARGIN_B - 6*mm, f'Pág. {doc.page}')

# ── Estilos tipográficos ──────────────────────────────────────────
def estilos():
    return {
        'subseccion': ParagraphStyle('subseccion', fontName='Helvetica-Bold', fontSize=11, textColor=C_PRIMARIO, spaceBefore=14, spaceAfter=4, leading=15),
        'cuerpo': ParagraphStyle('cuerpo', fontName='Helvetica', fontSize=10, textColor=C_TEXTO, alignment=TA_JUSTIFY, spaceAfter=5, leading=15),
        'cuerpo_tabla': ParagraphStyle('cuerpo_tabla', fontName='Helvetica', fontSize=9, textColor=C_TEXTO, leading=13),
        'header_tabla': ParagraphStyle('header_tabla', fontName='Helvetica-Bold', fontSize=9, textColor=white, leading=13),
        'etiqueta': ParagraphStyle('etiqueta', fontName='Helvetica-Bold', fontSize=9, textColor=C_PRIMARIO, leading=13),
        'campo_critico': ParagraphStyle('campo_critico', fontName='Helvetica-Bold', fontSize=9, textColor=C_CRITICO, leading=13),
    }

# ── Tablas y Cajas ────────────────────────────────────────────────
def hacer_ficha_tecnica(datos, est):
    def fila(label, valor):
        return [Paragraph(f"<b>{label}:</b>", est['cuerpo_tabla']), Paragraph(str(valor or 'N/A'), est['cuerpo_tabla'])]
    filas = [
        fila('Investigador Principal', datos.get('investigador')),
        fila('ID / CVLAC', datos.get('id_investigador')),
        fila('Unidad / Facultad', datos.get('facultad')),
        fila('Grupo de Investigación', datos.get('grupo')),
        fila('Sector Temático', datos.get('sector_tematico')),
    ]
    t = Table(filas, colWidths=[6*cm, 10.6*cm])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, C_LINEA),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [C_FONDO_TABLA, white]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5), ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t

def hacer_tabla_equipo(equipo, est):
    encabezados = [Paragraph(h, est['header_tabla']) for h in ['Investigador', 'Rol', 'Institución', '%', 'Justificación']]
    filas = [encabezados]
    for i, m in enumerate(equipo):
        p = m.get('perfil_completo', {})
        filas.append([
            Paragraph(p.get('nombre', ''), est['cuerpo_tabla']),
            Paragraph(m.get('rol', ''), est['cuerpo_tabla']),
            Paragraph(p.get('institucion', ''), est['cuerpo_tabla']),
            Paragraph(f"{m.get('dedicacion_porcentaje', 0)}%", est['cuerpo_tabla']),
            Paragraph(m.get('justificacion', ''), est['cuerpo_tabla']),
        ])
    t = Table(filas, colWidths=[3.2*cm, 2.4*cm, 2.8*cm, 1.2*cm, 7.0*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_FONDO_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_PRIMARIO),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_FONDO_TABLA, white]),
        ('GRID', (0, 0), (-1, -1), 0.25, C_LINEA),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t

def hacer_tabla_campos(campos_ob, campos_crit, est):
    filas = [[Paragraph(h, est['header_tabla']) for h in ['Campo requerido', 'Clasificación']]]
    for c in campos_ob:
        es_critico = c in campos_crit
        filas.append([Paragraph(c.replace('_', ' ').title(), est['cuerpo_tabla']), 
                      Paragraph('(!) Critico' if es_critico else 'Estandar', est['campo_critico'] if es_critico else est['cuerpo_tabla'])])
    t = Table(filas, colWidths=[13*cm, 3.6*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARIO),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_FONDO_TABLA, white]),
        ('GRID', (0, 0), (-1, -1), 0.25, C_LINEA),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, C_ACENTO),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def hacer_caja(texto, est, bg=C_VERDE_FONDO, borde=HexColor('#6ee7b7')):
    t = Table([[Paragraph(texto, est['cuerpo'])]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('LINEBELOW', (0, 0), (-1, -1), 2, borde),
        ('LINEBEFORE', (0, 0), (0, -1), 3, borde),
        ('TOPPADDING', (0, 0), (-1, -1), 9), ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    return t

def hacer_tabla_desde_markdown(filas_md, est):
    """Convierte filas de texto tipo | col1 | col2 | en una tabla ReportLab."""
    datos_tabla = []
    for fila in filas_md:
        # Limpiar bordes y dividir
        celdas = [c.strip() for c in fila.strip('|').split('|')]
        if all(re.match(r'^[- :|]+$', c) for c in celdas): continue # Ignorar separadores |---|
        
        # Sanitizar cada celda
        celdas_safe = []
        for c in celdas:
            c_safe = c.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            c_safe = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', c_safe)
            celdas_safe.append(Paragraph(c_safe, est['cuerpo_tabla']))
        
        datos_tabla.append(celdas_safe)
    
    if not datos_tabla: return None
    
    # Calcular anchos proporcionales
    num_cols = len(datos_tabla[0])
    ancho_col = CONTENT_W / num_cols
    
    t = Table(datos_tabla, colWidths=[ancho_col]*num_cols)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_FONDO_HEADER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_LINEA),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t

def parsear_expansion(texto, est):
    elementos = []
    lineas = texto.split('\n')
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if not linea:
            i += 1
            continue
            
        # Detección de tablas Markdown
        if linea.startswith('|'):
            filas_tabla = []
            while i < len(lineas) and lineas[i].strip().startswith('|'):
                filas_tabla.append(lineas[i].strip())
                i += 1
            tabla = hacer_tabla_desde_markdown(filas_tabla, est)
            if tabla:
                elementos.append(Spacer(1, 0.2*cm))
                elementos.append(tabla)
                elementos.append(Spacer(1, 0.2*cm))
            continue

        # Escapado robusto: primero escapamos todo lo que rompe ReportLab
        linea_safe = linea.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Luego restauramos solo las negritas si la IA las puso (convertimos ** a <b>)
        # O si ya venían como tags (que ahora están escapados)
        linea_safe = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', linea_safe)
        
        if linea.startswith('###'):
            clean_title = linea.replace('###', '').strip().rstrip(':')
            clean_title = clean_title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            elementos.append(Paragraph(clean_title, est['subseccion']))
        elif re.match(r'^[-•*]\s+', linea):
            clean_item = re.sub(r'^[-•*]\s+', '', linea_safe)
            elementos.append(Paragraph(f"&nbsp;&nbsp;&nbsp;— {clean_item}", est['cuerpo']))
        else:
            elementos.append(Paragraph(linea_safe, est['cuerpo']))
        i += 1
    return elementos

# ── Generación de PDF ─────────────────────────────────────────────
def generar_pdf(datos_proyecto: dict, ruta_salida: str) -> str:
    est = estilos()
    fecha = fecha_es()
    formato_nombre = datos_proyecto.get('formato_nombre', datos_proyecto.get('formato', 'Documento'))
    
    doc = SimpleDocTemplate(ruta_salida, pagesize=A4, rightMargin=MARGIN_R, leftMargin=MARGIN_L, topMargin=MARGIN_T, bottomMargin=MARGIN_B + 8*mm)
    elementos = []
    
    expansion_txt = datos_proyecto.get('expansion', '')
    print(f"[PDF Engine] Longitud de expansión recibida: {len(expansion_txt)} caracteres.")
    if len(expansion_txt) < 50:
        print(f"[PDF Engine] ADVERTENCIA: La expansión es muy corta o está vacía: '{expansion_txt}'")

    # 0. Ficha Técnica
    elementos.append(SeccionHeader('00', 'Ficha Técnica de la Propuesta'))
    elementos.append(Spacer(1, 0.4*cm))
    elementos.append(hacer_ficha_tecnica(datos_proyecto, est))
    elementos.append(Spacer(1, 0.8*cm))

    # 1. Estructura Lógica (Árboles)
    if datos_proyecto.get('arbol_problemas') or datos_proyecto.get('arbol_objetivos'):
        elementos.append(SeccionHeader('01', 'Estructura Lógica del Proyecto'))
        elementos.append(Spacer(1, 0.4*cm))
        if datos_proyecto.get('arbol_problemas'):
            elementos.append(Paragraph("<b>Árbol de Problemas:</b>", est['etiqueta']))
            elementos.append(Paragraph(datos_proyecto['arbol_problemas'], est['cuerpo']))
            elementos.append(Spacer(1, 0.3*cm))
        if datos_proyecto.get('arbol_objetivos'):
            elementos.append(Paragraph("<b>Árbol de Objetivos:</b>", est['etiqueta']))
            elementos.append(Paragraph(datos_proyecto['arbol_objetivos'], est['cuerpo']))
            elementos.append(Spacer(1, 0.3*cm))
        elementos.append(Spacer(1, 0.5*cm))

    # 3. Expansión
    elementos.append(SeccionHeader('02', 'Propuesta Técnica Detallada (IA)'))
    elementos.append(Spacer(1, 0.4*cm))
    elementos.extend(parsear_expansion(datos_proyecto.get('expansion', ''), est))
    elementos.append(Spacer(1, 1*cm))

    # 4. Equipo (Más discreto)
    equipo_data = datos_proyecto.get('equipo', {})
    if equipo_data.get('equipo_sugerido'):
        elementos.append(Paragraph("ANEXO: APOYO ESTRATÉGICO Y TALENTO SUGERIDO", est['etiqueta']))
        elementos.append(Spacer(1, 0.2*cm))
        elementos.append(hacer_tabla_equipo(equipo_data['equipo_sugerido'], est))
        elementos.append(Spacer(1, 0.6*cm))

    # 3. Campos del Formato
    elementos.append(SeccionHeader('03', f'Requisitos del Formato {formato_nombre}'))
    elementos.append(Spacer(1, 0.4*cm))
    elementos.append(hacer_tabla_campos(datos_proyecto.get('campos_obligatorios', []), datos_proyecto.get('campos_criticos', []), est))
    elementos.append(Spacer(1, 1*cm))

    # 4. Matching y Validación
    match_data = datos_proyecto.get('match_evaluacion', {})
    if match_data:
        elementos.append(PageBreak())
        elementos.append(SeccionHeader('04', 'Validación de Requisitos y Compatibilidad'))
        elementos.append(Spacer(1, 0.5*cm))
        score = match_data.get('compatibilidad_score', 0)
        color = C_VERDE if score >= 85 else (C_CRITICO if score < 60 else C_ACENTO)
        
        elementos.append(Paragraph(f"<b>Evaluación contra:</b> {match_data.get('demanda_nombre', 'Estándar de Convocatoria')}", est['subseccion']))
        elementos.append(BarraProgreso(score, color=color))
        elementos.append(Spacer(1, 0.5*cm))
        
        elementos.append(hacer_caja(f"<b>Dictamen IA:</b> {match_data.get('justificacion', '')}", est, bg=C_FONDO_HEADER, borde=color))
        elementos.append(Spacer(1, 0.6*cm))
        
        if match_data.get('brechas_detectadas'):
            elementos.append(Paragraph("<b>BRECHAS DE CUMPLIMIENTO IDENTIFICADAS</b>", est['etiqueta']))
            for b in match_data['brechas_detectadas']:
                elementos.append(Paragraph(f"<font color='#dc2626'>[X]</font> {b}", est['cuerpo']))
            elementos.append(Spacer(1, 0.6*cm))

        if match_data.get('recomendaciones'):
            elementos.append(Paragraph("<b>RECOMENDACIONES PARA EL CIERRE DE BRECHAS</b>", est['etiqueta']))
            for r in match_data['recomendaciones']:
                elementos.append(Paragraph(f"<font color='#059669'>[+]</font> {r}", est['cuerpo']))

    # 5. Próximos Pasos
    elementos.append(Spacer(1, 1*cm))
    elementos.append(SeccionHeader('05', 'Próximos Pasos para la Radicación'))
    pasos = ["Validar brechas identificadas.", "Completar presupuesto financiero.", "Obtener avales institucionales."]
    for p in pasos: elementos.append(Paragraph(f"• {p}", est['cuerpo']))

    doc.formato_nombre, doc.fecha_str = formato_nombre, fecha
    doc.build(elementos, onFirstPage=on_primera_pagina, onLaterPages=on_paginas_siguientes)
    return ruta_salida