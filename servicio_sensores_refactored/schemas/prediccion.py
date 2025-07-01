"""
Esquemas Pydantic para Predicción de Sequía
"""
from typing import Optional
from schemas.base import BaseSchema, BaseResponse

class PrediccionBase(BaseSchema):
    """Campos base de la predicción"""
    ubicacion_id: int
    probabilidad: float
    comentario: Optional[str] = None

class PrediccionCreate(PrediccionBase):
    """Esquema para crear predicción"""
    pass

class PrediccionUpdate(BaseSchema):
    """Esquema para actualizar predicción"""
    ubicacion_id: Optional[int] = None
    probabilidad: Optional[float] = None
    comentario: Optional[str] = None

class PrediccionResponse(PrediccionBase, BaseResponse):
    """Esquema de respuesta completo"""
    pass

class PrediccionDetail(PrediccionResponse):
    """Esquema detallado con relaciones"""
    # Se puede agregar información de la ubicación relacionada
    pass
