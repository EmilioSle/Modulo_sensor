"""
Esquemas Pydantic para Sensor
"""
from typing import List, Optional
from schemas.base import BaseSchema, BaseResponse

class SensorBase(BaseSchema):
    """Campos base del sensor"""
    tipo: str
    modelo: str

class SensorCreate(SensorBase):
    """Esquema para crear sensor"""
    pass

class SensorUpdate(BaseSchema):
    """Esquema para actualizar sensor (campos opcionales)"""
    tipo: Optional[str] = None
    modelo: Optional[str] = None

class SensorResponse(SensorBase, BaseResponse):
    """Esquema de respuesta completo"""
    pass

class SensorDetail(SensorResponse):
    """Esquema detallado con relaciones"""
    # Se pueden agregar lecturas y ubicaciones cuando las necesitemos
    pass
