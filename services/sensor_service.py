"""
Servicios (casos de uso) para Sensores
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models.sensor import Sensor
from repositories.sensor_repository import sensor_repository
from schemas.sensor import SensorCreate, SensorUpdate

class SensorService:
    """Servicio para manejar lógica de negocio de sensores"""
    
    def __init__(self):
        self.repository = sensor_repository
    
    def create_sensor(self, db: Session, sensor_data: SensorCreate) -> Sensor:
        """Crear un nuevo sensor"""
        # Aquí puedes agregar validaciones de negocio
        return self.repository.create(db, **sensor_data.dict())
    
    def get_sensor(self, db: Session, sensor_id: int) -> Optional[Sensor]:
        """Obtener un sensor por ID"""
        return self.repository.get_by_id(db, sensor_id)
    
    def get_all_sensors(self, db: Session, skip: int = 0, limit: int = 100) -> List[Sensor]:
        """Obtener todos los sensores con paginación"""
        return self.repository.get_all(db, skip=skip, limit=limit)
    
    def update_sensor(self, db: Session, sensor_id: int, sensor_data: SensorUpdate) -> Optional[Sensor]:
        """Actualizar un sensor"""
        # Filtrar campos None
        update_data = {k: v for k, v in sensor_data.model_dump().items() if v is not None}
        if not update_data:
            return self.get_sensor(db, sensor_id)
        
        return self.repository.update(db, sensor_id, **update_data)
    
    def delete_sensor(self, db: Session, sensor_id: int) -> bool:
        """Eliminar un sensor"""
        return self.repository.delete(db, sensor_id)
    
    def get_sensors_by_type(self, db: Session, tipo: str) -> List[Sensor]:
        """Obtener sensores por tipo"""
        return self.repository.get_by_tipo(db, tipo)
    
    def sensor_exists(self, db: Session, sensor_id: int) -> bool:
        """Verificar si existe un sensor"""
        return self.repository.exists(db, sensor_id)

# Instancia global del servicio
sensor_service = SensorService()
