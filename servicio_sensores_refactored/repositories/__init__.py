"""
Repositorios principales - Exporta las instancias globales
"""
from repositories.sensor_repository import sensor_repository
from repositories.lectura_repository import lectura_repository
from repositories.ubicacion_repository import ubicacion_repository
from repositories.anomalia_repository import anomalia_repository
from repositories.prediccion_repository import prediccion_repository

__all__ = [
    "sensor_repository",
    "lectura_repository",
    "ubicacion_repository", 
    "anomalia_repository",
    "prediccion_repository"
]
