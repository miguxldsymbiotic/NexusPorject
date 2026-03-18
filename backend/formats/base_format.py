# Clase base que todos los formatos deben seguir
class BaseFormat:
    id: str = ""
    nombre: str = ""
    descripcion: str = ""
    campos_obligatorios: list = []
    instrucciones_retorica: str = ""
    campos_criticos: list = []  # Campos que disparan pregunta de clarificación

    @classmethod
    def get_prompt_instructions(cls) -> str:
        """Retorna las instrucciones específicas del formato para el prompt."""
        return cls.instrucciones_retorica

    @classmethod
    def get_secciones(cls) -> list:
        """
        Retorna la lista de secciones para generación secuencial.
        Por defecto, una sola sección llamada 'Expansión General'.
        """
        return getattr(cls, 'SECCIONES', [
            {"id": "expansion", "nombre": "Expansión General", "prompt": cls.instrucciones_retorica}
        ])

    @classmethod
    def get_campos_obligatorios(cls) -> list:
        return cls.campos_obligatorios

    @classmethod
    def get_campos_criticos(cls) -> list:
        return cls.campos_criticos