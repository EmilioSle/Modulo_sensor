"""
Shell interactivo para el proyecto
"""
from core.database import get_db_context
from models import *
from repositories import *
from services.sensor_service import sensor_service
from services.lectura_service import lectura_service

def interactive_shell():
    """Abre un shell interactivo con contexto del proyecto"""
    print("=== Shell Interactivo del Proyecto Sensores ===")
    print("Objetos disponibles:")
    print("  - db: contexto de base de datos")
    print("  - sensor_service: servicio de sensores")
    print("  - lectura_service: servicio de lecturas")
    print("  - Modelos: Sensor, Lectura, etc.")
    print("Ejemplo: sensor_service.get_all_sensors(db)")
    
    import IPython
    with get_db_context() as db:
        IPython.embed(
            header="Shell del proyecto cargado exitosamente",
            colors="neutral"
        )
