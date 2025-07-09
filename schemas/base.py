"""
Esquemas Pydantic base compatibles con Python 3.x
"""
# Importar Pydantic de forma compatible
try:
    from pydantic import BaseModel, ConfigDict
    PYDANTIC_V2 = True
except ImportError:
    from pydantic import BaseModel
    PYDANTIC_V2 = False

from datetime import datetime
from typing import Optional

class BaseSchema(BaseModel):
    """Esquema base con configuración común"""
    
    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            from_attributes = True
            orm_mode = True

    def dict(self, **kwargs):
        """Método dict compatible que excluye campos de configuración"""
        if hasattr(super(), 'model_dump'):
            data = super().model_dump(**kwargs)
        else:
            data = super().dict(**kwargs)
        
        # Filtrar campos que no deben ir a la base de datos
        excluded_fields = ['model_config']
        return {k: v for k, v in data.items() if k not in excluded_fields}

class TimestampSchema(BaseSchema):
    """Esquema base con timestamps"""
    created_at: datetime
    updated_at: datetime

class BaseResponse(TimestampSchema):
    """Esquema base para respuestas"""
    id: int
