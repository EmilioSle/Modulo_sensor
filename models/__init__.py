"""
Exporta todos los modelos para facilitar los imports
"""
from models.sensor import Sensor
from models.lectura import Lectura
from models.ubicacion import Ubicacion
from models.anomalia import Anomalia
from models.prediccion import PrediccionSequia

__all__ = [
    "Sensor",
    "Lectura", 
    "Ubicacion",
    "Anomalia",
    "PrediccionSequia"
]
