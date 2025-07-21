"""
Servicio para manejar lógica de negocio de ubicaciones
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models.ubicacion import Ubicacion
from repositories.ubicacion_repository import ubicacion_repository
from repositories.sensor_repository import sensor_repository
from schemas.ubicacion import UbicacionCreate, UbicacionUpdate

class UbicacionService:
    """Servicio para manejar lógica de negocio de ubicaciones"""
    
    def __init__(self):
        self.repository = ubicacion_repository
        self.sensor_repository = sensor_repository
    
    def create_ubicacion(self, db: Session, ubicacion_data: UbicacionCreate) -> Ubicacion:
        """Crear una nueva ubicación"""
        # Validar que el sensor existe
        if not self.sensor_repository.exists(db, ubicacion_data.sensor_id):
            raise ValueError(f"Sensor con ID {ubicacion_data.sensor_id} no existe")
        
        # Validar coordenadas
        self._validate_coordinates(ubicacion_data.latitud, ubicacion_data.longitud)
        
        # Verificar que no exista una ubicación exacta ya
        existing = self.repository.get_by_coordinates(db, ubicacion_data.latitud, ubicacion_data.longitud)
        if existing:
            raise ValueError(f"Ya existe una ubicación en las coordenadas {ubicacion_data.latitud}, {ubicacion_data.longitud}")
        
        # Crear la ubicación
        return self.repository.create(db, **ubicacion_data.dict())
        
    def get_ubicacion(self, db: Session, ubicacion_id: int) -> Optional[Ubicacion]:
        """Obtener una ubicación por ID"""
        return self.repository.get_by_id(db, ubicacion_id)
    
    def get_all_ubicaciones(self, db: Session, skip: int = 0, limit: int = 100) -> List[Ubicacion]:
        """Obtener todas las ubicaciones con paginación"""
        return self.repository.get_all(db, skip=skip, limit=limit)
    
    def get_ubicaciones_by_sensor(self, db: Session, sensor_id: int) -> List[Ubicacion]:
        """Obtener ubicaciones de un sensor específico"""
        return self.repository.get_by_sensor(db, sensor_id)
    
    def update_ubicacion(self, db: Session, ubicacion_id: int, ubicacion_data: UbicacionUpdate) -> Optional[Ubicacion]:
        """Actualizar ubicación"""
        # Validar coordenadas si se proporcionan
        if ubicacion_data.latitud is not None and ubicacion_data.longitud is not None:
            self._validate_coordinates(ubicacion_data.latitud, ubicacion_data.longitud)
        
        # Validar que el sensor existe si se proporciona
        if ubicacion_data.sensor_id is not None:
            if not self.sensor_repository.exists(db, ubicacion_data.sensor_id):
                raise ValueError(f"Sensor con ID {ubicacion_data.sensor_id} no existe")
        
        return self.repository.update(db, ubicacion_id, **ubicacion_data.dict(exclude_unset=True))
        
    def delete_ubicacion(self, db: Session, ubicacion_id: int) -> bool:
        """Eliminar una ubicación"""
        return self.repository.delete(db, ubicacion_id)
    
    def search_ubicaciones(self, db: Session, search_term: str) -> List[Ubicacion]:
        """Buscar ubicaciones por descripción"""
        return self.repository.search_by_description(db, search_term)
    
    def get_nearby_locations(
        self, 
        db: Session, 
        latitud: str, 
        longitud: str, 
        radio: float = 0.01
    ) -> List[Ubicacion]:
        """Obtener ubicaciones cercanas"""
        return self.repository.get_nearby_locations(db, latitud, longitud, radio)
    
    def _validate_coordinates(self, latitud: str, longitud: str):
        """Validar que las coordenadas sean válidas"""
        try:
            lat_float = float(latitud)
            lng_float = float(longitud)
            
            if not (-90 <= lat_float <= 90):
                raise ValueError("Latitud debe estar entre -90 y 90 grados")
            
            if not (-180 <= lng_float <= 180):
                raise ValueError("Longitud debe estar entre -180 y 180 grados")
                
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Coordenadas deben ser números válidos")
            raise

# Instancia global del servicio
ubicacion_service = UbicacionService()
