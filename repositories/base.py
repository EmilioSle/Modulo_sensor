"""
Repositorio genérico que implementa CRUD básico
"""
from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from models.base import BaseModel

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=BaseModel)

class CRUDRepository(Generic[ModelType]):
    """Repositorio CRUD genérico"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def create(self, db: Session, **kwargs) -> ModelType:
        """Crear una nueva instancia"""
        try:
            db_obj = self.model(**kwargs)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Creado {self.model.__name__} con ID {db_obj.id}")
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creando {self.model.__name__}: {e}")
            raise
    
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """Obtener por ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Obtener todos con paginación"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, db: Session, id: int, **kwargs) -> Optional[ModelType]:
        """Actualizar un registro"""
        try:
            db_obj = self.get_by_id(db, id)
            if not db_obj:
                return None
            
            for key, value in kwargs.items():
                setattr(db_obj, key, value)
            
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Actualizado {self.model.__name__} con ID {db_obj.id}")
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error actualizando {self.model.__name__}: {e}")
            raise
    
    def delete(self, db: Session, id: int) -> bool:
        """Eliminar un registro"""
        try:
            db_obj = self.get_by_id(db, id)
            if not db_obj:
                return False
            
            db.delete(db_obj)
            db.commit()
            logger.info(f"Eliminado {self.model.__name__} con ID {id}")
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error eliminando {self.model.__name__}: {e}")
            raise
    
    def filter_by(self, db: Session, **filters) -> List[ModelType]:
        """Filtrar por campos específicos"""
        query = db.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.all()
    
    def get_multi_by_field(self, db: Session, field: str, value: Any) -> List[ModelType]:
        """Obtener múltiples registros por un campo específico"""
        if hasattr(self.model, field):
            return db.query(self.model).filter(getattr(self.model, field) == value).all()
        return []
    
    def count(self, db: Session) -> int:
        """Contar total de registros"""
        return db.query(self.model).count()
    
    def exists(self, db: Session, id: int) -> bool:
        """Verificar si existe un registro"""
        return db.query(self.model).filter(self.model.id == id).first() is not None
