from formats.mga import FormatoMGA
from formats.minciencias import FormatoMinCiencias
from formats.bid import FormatoBID
from formats.erasmus import FormatoErasmus
from formats.horizonte import FormatoHorizonte
from formats.zopp import FormatoZOPP
from formats.marco_logico import FormatoMarcoLogico
from formats.universal import FormatoUniversal

# Diccionario central — la clave es el string que envía el usuario
FORMATOS_DISPONIBLES = {
    "UNIVERSAL": FormatoUniversal,
    "HIBRIDO": FormatoUniversal,
    "MAESTRO": FormatoUniversal,
    "MGA": FormatoMGA,
    "MINCIENCIAS": FormatoMinCiencias,
    "COLCIENCIAS": FormatoMinCiencias,  # Alias del nombre anterior
    "BID": FormatoBID,
    "IDB": FormatoBID,                  # Alias en inglés
    "ERASMUS": FormatoErasmus,
    "ERASMUS+": FormatoErasmus,         # Alias con el símbolo
    "HORIZONTE": FormatoHorizonte,
    "HORIZONTE_EUROPA": FormatoHorizonte,
    "ZOPP": FormatoZOPP,
    "PCM": FormatoZOPP,                 # Alias
    "MARCO_LOGICO": FormatoMarcoLogico,
    "MARCO LOGICO": FormatoMarcoLogico, # Alias con espacio
}

def get_formato(nombre: str):
    """
    Retorna la clase del formato solicitado.
    La búsqueda es insensible a mayúsculas/minúsculas.
    """
    clave = nombre.upper().strip()
    formato = FORMATOS_DISPONIBLES.get(clave)

    if not formato:
        formatos_validos = list(set(FORMATOS_DISPONIBLES.keys()))
        raise ValueError(
            f"Formato '{nombre}' no reconocido. "
            f"Formatos disponibles: {formatos_validos}"
        )
    return formato

def listar_formatos() -> list:
    """Retorna la lista de formatos únicos disponibles."""
    vistos = set()
    resultado = []
    for clase in FORMATOS_DISPONIBLES.values():
        if clase.id not in vistos:
            vistos.add(clase.id)
            resultado.append({
                "id": clase.id,
                "nombre": clase.nombre,
                "descripcion": clase.descripcion
            })
    return resultado