"""
Esquemas Pydantic para Ubicación
"""
from typing import Optional, List
from schemas.base import BaseSchema, BaseResponse

class UbicacionBase(BaseSchema):
    """Campos base de la ubicación"""
    sensor_id: int
    latitud: str
    longitud: str
    descripcion: Optional[str] = None

class UbicacionCreate(UbicacionBase):
    """Esquema para crear ubicación"""
    pass

class UbicacionUpdate(BaseSchema):
    """Esquema para actualizar ubicación"""
    sensor_id: Optional[int] = None
    latitud: Optional[str] = None
    longitud: Optional[str] = None
    descripcion: Optional[str] = None

class UbicacionResponse(UbicacionBase, BaseResponse):
    """Esquema de respuesta completo"""
    pass

class UbicacionDetail(UbicacionResponse):
    """Esquema detallado con relaciones"""
    # Se pueden agregar predicciones cuando las necesitemos
    pass
