"""
Modelos base y abstractos
"""
from abc import ABC, abstractmethod
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime, UTC
from typing import Dict, Any

from core.database import Base

class TimestampMixin:
    """Mixin para agregar campos de fecha de creación y actualización"""
    
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    
    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

class BaseModel(Base, TimestampMixin):
    """Modelo base abstracto"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def update_from_dict(self, data: Dict[str, Any]):
        """Actualiza el modelo desde un diccionario"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

class BaseRepository(ABC):
    """Repositorio base abstracto"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    @abstractmethod
    def create(self, db, **kwargs):
        """Crear una nueva instancia"""
        pass
    
    @abstractmethod
    def get_by_id(self, db, id: int):
        """Obtener por ID"""
        pass
    
    @abstractmethod
    def get_all(self, db, skip: int = 0, limit: int = 100):
        """Obtener todos los registros"""
        pass
    
    @abstractmethod
    def update(self, db, id: int, **kwargs):
        """Actualizar un registro"""
        pass
    
    @abstractmethod
    def delete(self, db, id: int):
        """Eliminar un registro"""
        pass
