"""
Repositorio específico para Ubicaciones
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from models.ubicacion import Ubicacion
from repositories.base import CRUDRepository

class UbicacionRepository(CRUDRepository[Ubicacion]):
    """Repositorio para operaciones específicas de Ubicación"""
    
    def __init__(self):
        super().__init__(Ubicacion)
    
    def get_by_sensor(self, db: Session, sensor_id: int) -> List[Ubicacion]:
        """Obtener ubicaciones por sensor"""
        return db.query(Ubicacion).filter(Ubicacion.sensor_id == sensor_id).all()
    
    def get_by_coordinates(self, db: Session, latitud: str, longitud: str) -> Optional[Ubicacion]:
        """Obtener ubicación por coordenadas exactas"""
        return db.query(Ubicacion).filter(
            Ubicacion.latitud == latitud,
            Ubicacion.longitud == longitud
        ).first()
    
    def get_nearby_locations(
        self, 
        db: Session, 
        latitud_base: str, 
        longitud_base: str, 
        radio: float = 0.01
    ) -> List[Ubicacion]:
        """Obtener ubicaciones cercanas (aproximación simple)"""
        # Esta es una aproximación básica, en producción usarías funciones geoespaciales
        lat_float = float(latitud_base)
        lng_float = float(longitud_base)
        
        return db.query(Ubicacion).filter(
            Ubicacion.latitud.between(str(lat_float - radio), str(lat_float + radio)),
            Ubicacion.longitud.between(str(lng_float - radio), str(lng_float + radio))
        ).all()
    
    def search_by_description(self, db: Session, search_term: str) -> List[Ubicacion]:
        """Buscar ubicaciones por descripción"""
        return db.query(Ubicacion).filter(
            Ubicacion.descripcion.ilike(f"%{search_term}%")
        ).all()

# Instancia global del repositorio
ubicacion_repository = UbicacionRepository()
