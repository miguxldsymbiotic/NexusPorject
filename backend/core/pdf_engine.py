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
C_VERDE         = HexColor('#065f46')
C_VERDE_FONDO   = HexColor('#ecfdf5')
C_NARANJA_FONDO = HexColor('#fff7ed')
C_NARANJA_BORDE = HexColor('#fed7aa')
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


# ── Flowable personalizado: barra lateral de sección ──────────────
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
        # Fondo completo
        c.setFillColor(C_FONDO_HEADER)
        c.roundRect(0, 0, self.ancho, self.altura, 4, fill=1, stroke=0)
        # Barra lateral izquierda
        c.setFillColor(C_ACENTO)
        c.rect(0, 0, 4, self.altura, fill=1, stroke=0)
        # Número de sección
        c.setFillColor(C_ACENTO)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(10, self.altura / 2 - 3, self.numero)
        # Título
        c.setFillColor(C_PRIMARIO)
        c.setFont('Helvetica-Bold', 12)
        c.drawString(32, self.altura / 2 - 4, self.titulo.upper())

    def wrap(self, *args):
        return (self.ancho, self.altura + 6)


class LineaDivisoria(Flowable):
    """Línea horizontal decorativa."""
    def __init__(self, ancho=CONTENT_W, color=C_LINEA, grosor=0.5):
        Flowable.__init__(self)
        self.ancho  = ancho
        self.color  = color
        self.grosor = grosor

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.grosor)
        self.canv.line(0, 0, self.ancho, 0)

    def wrap(self, *args):
        return (self.ancho, self.grosor + 2)


# ── Numeración de páginas ─────────────────────────────────────────
def agregar_pie_pagina(canvas, doc, formato_nombre, fecha):
    canvas.saveState()
    # Línea superior del pie
    canvas.setStrokeColor(C_LINEA)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, MARGIN_B - 2*mm, PAGE_W - MARGIN_R, MARGIN_B - 2*mm)
    # Texto izquierdo
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(C_TEXTO_SUAVE)
    canvas.drawString(MARGIN_L, MARGIN_B - 6*mm, f'Project Nexus · {formato_nombre}')
    # Fecha centro
    canvas.drawCentredString(PAGE_W / 2, MARGIN_B - 6*mm, fecha)
    # Número de página derecha
    canvas.drawRightString(PAGE_W - MARGIN_R, MARGIN_B - 6*mm, f'Página {doc.page}')
    canvas.restoreState()


# ── Estilos tipográficos ──────────────────────────────────────────
def estilos():
    return {
        'titulo_portada': ParagraphStyle(
            'titulo_portada',
            fontName='Helvetica-Bold', fontSize=22,
            textColor=white, alignment=TA_LEFT,
            spaceAfter=6, leading=28,
        ),
        'subtitulo_portada': ParagraphStyle(
            'subtitulo_portada',
            fontName='Helvetica', fontSize=11,
            textColor=HexColor('#93c5fd'), alignment=TA_LEFT,
            spaceAfter=4, leading=16,
        ),
        'etiqueta_portada': ParagraphStyle(
            'etiqueta_portada',
            fontName='Helvetica-Bold', fontSize=8,
            textColor=HexColor('#93c5fd'), alignment=TA_LEFT,
            spaceBefore=10, spaceAfter=2,
        ),
        'valor_portada': ParagraphStyle(
            'valor_portada',
            fontName='Helvetica', fontSize=10,
            textColor=white, alignment=TA_LEFT,
            spaceAfter=6, leading=14,
        ),
        'subseccion': ParagraphStyle(
            'subseccion',
            fontName='Helvetica-Bold', fontSize=11,
            textColor=C_PRIMARIO, spaceBefore=14,
            spaceAfter=4, leading=15,
        ),
        'cuerpo': ParagraphStyle(
            'cuerpo',
            fontName='Helvetica', fontSize=10,
            textColor=C_TEXTO, alignment=TA_JUSTIFY,
            spaceAfter=5, leading=15,
        ),
        'cuerpo_tabla': ParagraphStyle(
            'cuerpo_tabla',
            fontName='Helvetica', fontSize=9,
            textColor=C_TEXTO, leading=13,
        ),
        'header_tabla': ParagraphStyle(
            'header_tabla',
            fontName='Helvetica-Bold', fontSize=9,
            textColor=white, leading=13,
        ),
        'etiqueta': ParagraphStyle(
            'etiqueta',
            fontName='Helvetica-Bold', fontSize=9,
            textColor=C_PRIMARIO, leading=13,
        ),
        'nota': ParagraphStyle(
            'nota',
            fontName='Helvetica-Oblique', fontSize=8,
            textColor=C_TEXTO_SUAVE, leading=11,
        ),
        'campo_critico': ParagraphStyle(
            'campo_critico',
            fontName='Helvetica-Bold', fontSize=9,
            textColor=C_CRITICO, leading=13,
        ),
        'idea_texto': ParagraphStyle(
            'idea_texto',
            fontName='Helvetica-Oblique', fontSize=10,
            textColor=C_VERDE, alignment=TA_JUSTIFY,
            leading=15,
        ),
    }


# ── Portada de página completa ────────────────────────────────────
def dibujar_portada(canvas, datos):
    """Dibuja la portada directamente sobre el canvas (página completa)."""
    canvas.saveState()

    # Fondo azul marino completo
    canvas.setFillColor(C_PRIMARIO)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Franja de acento en la parte superior
    canvas.setFillColor(C_ACENTO)
    canvas.rect(0, PAGE_H - 8*mm, PAGE_W, 8*mm, fill=1, stroke=0)

    # Franja inferior
    canvas.setFillColor(C_SECUNDARIO)
    canvas.rect(0, 0, PAGE_W, 3*cm, fill=1, stroke=0)

    # Línea decorativa vertical izquierda
    canvas.setFillColor(C_ACENTO)
    canvas.rect(MARGIN_L - 5, 3*cm, 3, PAGE_H - 3*cm - 8*mm, fill=1, stroke=0)

    # Logo / Marca
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(C_ACENTO)
    canvas.drawString(MARGIN_L + 6, PAGE_H - 7*mm + 1, 'PROJECT NEXUS')

    # Título principal
    canvas.setFont('Helvetica-Bold', 28)
    canvas.setFillColor(white)
    canvas.drawString(MARGIN_L + 6, PAGE_H * 0.72, datos.get('formato_nombre', 'Documento Técnico'))

    # Subtítulo
    canvas.setFont('Helvetica', 14)
    canvas.setFillColor(HexColor('#93c5fd'))
    canvas.drawString(MARGIN_L + 6, PAGE_H * 0.72 - 22, 'Propuesta técnica preliminar · Project Nexus')

    # Línea separadora
    canvas.setStrokeColor(C_ACENTO)
    canvas.setLineWidth(1)
    canvas.line(MARGIN_L + 6, PAGE_H * 0.68, PAGE_W - MARGIN_R, PAGE_H * 0.68)

    # Metadatos en la portada
    y = PAGE_H * 0.62
    meta = [
        ('METODOLOGÍA', datos.get('metodologia', '')),
        ('ESTADO', 'Borrador técnico preliminar'),
        ('GENERADO POR', 'Project Nexus v0.5.0'),
        ('FECHA', fecha_es()),
    ]
    for etiqueta, valor in meta:
        canvas.setFont('Helvetica-Bold', 7.5)
        canvas.setFillColor(HexColor('#93c5fd'))
        canvas.drawString(MARGIN_L + 6, y, etiqueta)
        canvas.setFont('Helvetica', 10)
        canvas.setFillColor(white)
        canvas.drawString(MARGIN_L + 6, y - 13, valor)
        y -= 32

    # Caja de idea semilla
    idea = datos.get('idea_original', '')
    idea_y = 3*cm + 10*mm
    canvas.setFillColor(HexColor('#1e3f6e'))
    canvas.roundRect(MARGIN_L, idea_y - 5*mm,
                     PAGE_W - MARGIN_L - MARGIN_R, 4.5*cm, 6, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(C_ACENTO)
    canvas.drawString(MARGIN_L + 8, idea_y + 3.2*cm, 'IDEA SEMILLA')
    # Texto de la idea (truncado si es muy largo)
    canvas.setFont('Helvetica-Oblique', 9.5)
    canvas.setFillColor(HexColor('#dbeafe'))
    # Dividimos la idea en líneas manualmente
    palabras = idea.split()
    lineas, linea_actual = [], ''
    for palabra in palabras:
        prueba = linea_actual + ' ' + palabra if linea_actual else palabra
        if len(prueba) * 5.5 < (PAGE_W - MARGIN_L - MARGIN_R - 20):
            linea_actual = prueba
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)
    for i, linea in enumerate(lineas[:4]):
        canvas.drawString(MARGIN_L + 8, idea_y + 2.4*cm - i * 14, linea)

    # Pie de portada
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(HexColor('#93c5fd'))
    canvas.drawCentredString(PAGE_W / 2, 1.2*cm,
        'Documento generado automáticamente · No constituye propuesta oficial radicada')

    canvas.restoreState()


# ── Tablas ────────────────────────────────────────────────────────
def hacer_tabla_equipo(equipo, est):
    encabezados = [
        Paragraph('Investigador', est['header_tabla']),
        Paragraph('Rol', est['header_tabla']),
        Paragraph('Institución', est['header_tabla']),
        Paragraph('%', est['header_tabla']),
        Paragraph('Justificación', est['header_tabla']),
    ]
    filas = [encabezados]
    for i, m in enumerate(equipo):
        p = m.get('perfil_completo', {})
        bg = C_FONDO_TABLA if i % 2 == 0 else white
        filas.append([
            Paragraph(p.get('nombre', ''), est['cuerpo_tabla']),
            Paragraph(m.get('rol', ''), est['cuerpo_tabla']),
            Paragraph(p.get('institucion', ''), est['cuerpo_tabla']),
            Paragraph(f"{m.get('dedicacion_porcentaje', 0)}%", est['cuerpo_tabla']),
            Paragraph(m.get('justificacion', ''), est['cuerpo_tabla']),
        ])
    t = Table(filas, colWidths=[3.8*cm, 2.6*cm, 3.2*cm, 1.2*cm, 5.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  C_PRIMARIO),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [C_FONDO_TABLA, white]),
        ('GRID',          (0, 0), (-1, -1), 0.25, C_LINEA),
        ('LINEBELOW',     (0, 0), (-1, 0),  1.5, C_ACENTO),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING',   (0, 0), (-1, -1), 7),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 7),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
    ]))
    return t


def hacer_tabla_campos(campos_obligatorios, campos_criticos, est):
    encabezados = [
        Paragraph('Campo requerido', est['header_tabla']),
        Paragraph('Clasificacion', est['header_tabla']),
    ]
    filas = [encabezados]
    for campo in campos_obligatorios:
        es_critico = campo in campos_criticos
        nombre = campo.replace('_', ' ').title()
        tipo_p = Paragraph(
            '(!) Critico' if es_critico else 'Estandar',
            est['campo_critico'] if es_critico else est['cuerpo_tabla']
        )
        filas.append([Paragraph(nombre, est['cuerpo_tabla']), tipo_p])
    t = Table(filas, colWidths=[13*cm, 3.6*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  C_PRIMARIO),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [C_FONDO_TABLA, white]),
        ('GRID',          (0, 0), (-1, -1), 0.25, C_LINEA),
        ('LINEBELOW',     (0, 0), (-1, 0),  1.5, C_ACENTO),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
    ]))
    return t


def hacer_caja(texto, est, bg=C_VERDE_FONDO, borde=HexColor('#6ee7b7'), estilo_texto='cuerpo'):
    t = Table([[Paragraph(texto, est[estilo_texto])]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), bg),
        ('LINEBELOW',     (0, 0), (-1, -1), 2, borde),
        ('LINEBEFORE',    (0, 0), (0, -1),  3, borde),
        ('TOPPADDING',    (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
    ]))
    return t


# ── Parser de texto de la IA ──────────────────────────────────────
def parsear_expansion(texto, est):
    elementos = []
    for linea in texto.split('\n'):
        linea = linea.strip()
        if not linea:
            elementos.append(Spacer(1, 3))
            continue
        # Encabezados con ** al inicio y al final
        if re.match(r'^\*\*[^*]+\*\*$', linea):
            titulo = linea.replace('**', '').strip().rstrip(':')
            elementos.append(Spacer(1, 4))
            elementos.append(Paragraph(titulo, est['subseccion']))
            continue
        # Encabezados mixtos: **TITULO:** texto
        match = re.match(r'^\*\*(.+?)\*\*[:\s]*(.*)', linea)
        if match:
            titulo = match.group(1).strip().rstrip(':')
            resto  = match.group(2).strip()
            elementos.append(Spacer(1, 4))
            elementos.append(Paragraph(titulo, est['subseccion']))
            if resto:
                elementos.append(Paragraph(resto, est['cuerpo']))
            continue
        # Markdown headers
        if linea.startswith('###'):
            elementos.append(Paragraph(linea.lstrip('#').strip(), est['subseccion']))
            continue
        if linea.startswith('##') or linea.startswith('#'):
            elementos.append(Paragraph(linea.lstrip('#').strip(), est['subseccion']))
            continue
        # Listas con guión o bullet
        if re.match(r'^[-•*]\s+', linea):
            texto_item = re.sub(r'^[-•*]\s+', '', linea)
            # Limpiar negritas residuales
            texto_item = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', texto_item)
            elementos.append(Paragraph(f'&nbsp;&nbsp;&nbsp;— {texto_item}', est['cuerpo']))
            continue
        # Sublistas con +
        if re.match(r'^\+\s+', linea):
            texto_item = re.sub(r'^\+\s+', '', linea)
            texto_item = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', texto_item)
            elementos.append(Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;· {texto_item}', est['cuerpo']))
            continue
        # Listas numeradas
        if re.match(r'^\d+[\.\)]\s+', linea):
            texto_item = re.sub(r'^\d+[\.\)]\s+', '', linea)
            texto_item = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', texto_item)
            elementos.append(Paragraph(texto_item, est['cuerpo']))
            continue
        # Texto normal — convertir **negrita** a tags HTML
        linea_html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', linea)
        elementos.append(Paragraph(linea_html, est['cuerpo']))
    return elementos


# ── Función principal ─────────────────────────────────────────────
def generar_pdf(datos_proyecto: dict, ruta_salida: str) -> str:
    est = estilos()
    fecha = fecha_es()
    formato_nombre = datos_proyecto.get('formato_nombre',
                     datos_proyecto.get('formato', 'Documento'))

    def on_primera_pagina(canvas, doc):
        # La primera página ES la portada completa
        dibujar_portada(canvas, datos_proyecto)

    def on_paginas_siguientes(canvas, doc):
        agregar_pie_pagina(canvas, doc, formato_nombre, fecha)

    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=A4,
        rightMargin=MARGIN_R,
        leftMargin=MARGIN_L,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B + 8*mm,
        title=f'Project Nexus · {formato_nombre}',
        author='Project Nexus v0.5.0',
    )

    elementos = []

    # La primera página es manejada por on_primera_pagina (portada completa)
    # Forzamos un salto de página para que el contenido empiece en la página 2
    elementos.append(PageBreak())

    # ── SECCIÓN 1: PROPUESTA EXPANDIDA ───────────────────────────
    elementos.append(SeccionHeader('01', 'Propuesta técnica expandida'))
    elementos.append(Spacer(1, 0.4*cm))
    expansion = datos_proyecto.get('expansion', '')
    elementos.extend(parsear_expansion(expansion, est))
    elementos.append(Spacer(1, 0.6*cm))

    # ── SECCIÓN 2: EQUIPO INVESTIGADOR ───────────────────────────
    equipo_data = datos_proyecto.get('equipo', {})
    equipo_lista = equipo_data.get('equipo_sugerido', [])

    if equipo_lista:
        elementos.append(PageBreak())
        elementos.append(SeccionHeader('02', 'Equipo investigador sugerido'))
        elementos.append(Spacer(1, 0.4*cm))

        justificacion = equipo_data.get('justificacion_equipo', '')
        if justificacion:
            elementos.append(hacer_caja(justificacion, est,
                bg=C_FONDO_HEADER, borde=C_SECUNDARIO, estilo_texto='cuerpo'))
            elementos.append(Spacer(1, 0.4*cm))

        elementos.append(hacer_tabla_equipo(equipo_lista, est))

        for adv in equipo_data.get('advertencias', []):
            elementos.append(Spacer(1, 0.3*cm))
            elementos.append(hacer_caja(f'Advertencia: {adv}', est,
                bg=C_NARANJA_FONDO, borde=C_NARANJA_BORDE, estilo_texto='cuerpo'))

    # ── SECCIÓN 3: CAMPOS DEL FORMATO ────────────────────────────
    elementos.append(Spacer(1, 0.6*cm))
    elementos.append(SeccionHeader('03', 'Campos requeridos por el formato'))
    elementos.append(Spacer(1, 0.35*cm))
    elementos.append(Paragraph(
        f'El formato <b>{formato_nombre}</b> exige los campos listados a continuación. '
        f'Los marcados como <b>(!) Critico</b> deben estar explícitamente '
        f'documentados en la versión final.',
        est['cuerpo']
    ))
    elementos.append(Spacer(1, 0.3*cm))
    elementos.append(hacer_tabla_campos(
        datos_proyecto.get('campos_obligatorios', []),
        datos_proyecto.get('campos_criticos', []),
        est
    ))

    # ── SECCIÓN 4: PRÓXIMOS PASOS ─────────────────────────────────
    elementos.append(Spacer(1, 0.6*cm))
    elementos.append(SeccionHeader('04', 'Proximos pasos recomendados'))
    elementos.append(Spacer(1, 0.35*cm))

    pasos = [
        '1.  Revisar y validar la expansión retórica con el equipo investigador.',
        '2.  Completar los campos críticos marcados con (!) en la sección anterior.',
        '3.  Solicitar aval institucional de las entidades participantes.',
        '4.  Construir el árbol de problemas y objetivos de forma participativa.',
        '5.  Elaborar el presupuesto detallado por vigencias y fuentes de financiación.',
        '6.  Someter el borrador a revisión interna antes de la radicación oficial.',
    ]
    for paso in pasos:
        elementos.append(Paragraph(paso, est['cuerpo']))
        elementos.append(Spacer(1, 2))

    # ── BUILD ─────────────────────────────────────────────────────
    doc.build(
        elementos,
        onFirstPage=on_primera_pagina,
        onLaterPages=on_paginas_siguientes
    )
    print(f'[Nexus] PDF profesional generado: {ruta_salida}')
    return ruta_salida