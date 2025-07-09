"""
Esquemas Pydantic para Anomalía
"""
from typing import Optional
from schemas.base import BaseSchema, BaseResponse

class AnomaliaBase(BaseSchema):
    """Campos base de la anomalía"""
    lectura_id: int
    tipo: str
    valor: float

class AnomaliaCreate(AnomaliaBase):
    """Esquema para crear anomalía"""
    pass

class AnomaliaUpdate(BaseSchema):
    """Esquema para actualizar anomalía"""
    lectura_id: Optional[int] = None
    tipo: Optional[str] = None
    valor: Optional[float] = None

class AnomaliaResponse(AnomaliaBase, BaseResponse):
    """Esquema de respuesta completo"""
    pass

class AnomaliaDetail(AnomaliaResponse):
    """Esquema detallado con relaciones"""
    # Se puede agregar información de la lectura relacionada
    pass
