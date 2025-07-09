"""
Esquemas Pydantic para Lectura
"""
from typing import Optional
from schemas.base import BaseSchema, BaseResponse

class LecturaBase(BaseSchema):
    """Campos base de la lectura"""
    sensor_id: int
    humedad: float
    temperatura: float

class LecturaCreate(LecturaBase):
    """Esquema para crear lectura"""
    pass

class LecturaUpdate(BaseSchema):
    """Esquema para actualizar lectura"""
    humedad: Optional[float] = None
    temperatura: Optional[float] = None

class LecturaResponse(LecturaBase, BaseResponse):
    """Esquema de respuesta completo"""
    pass
