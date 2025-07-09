"""
Servicios (casos de uso) para Sensores
"""
import asyncio
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks

from models.sensor import Sensor
from repositories.sensor_repository import sensor_repository
from schemas.sensor import SensorCreate, SensorUpdate
from core.events import event_emitter, EventType

class SensorService:
    """Servicio para manejar lógica de negocio de sensores"""
    
    def __init__(self):
        self.repository = sensor_repository
    
    def create_sensor(self, db: Session, sensor_data: SensorCreate, background_tasks: BackgroundTasks = None) -> Sensor:
        """Crear un nuevo sensor"""
        # Aquí puedes agregar validaciones de negocio
        sensor_dict = sensor_data.model_dump() if hasattr(sensor_data, 'model_dump') else sensor_data.dict()
        sensor = self.repository.create(db, **sensor_dict)
        
        if not sensor:
            raise ValueError("Error al crear el sensor en la base de datos")
        
        # Emitir evento de creación usando background task
        if background_tasks:
            background_tasks.add_task(
                event_emitter.emit_sensor_event,
                EventType.CREATED,
                {
                    "id": sensor.id,
                    "tipo": sensor.tipo,
                    "modelo": sensor.modelo,
                    "created_at": sensor.created_at.isoformat() if sensor.created_at else None,
                    "updated_at": sensor.updated_at.isoformat() if sensor.updated_at else None
                },
                sensor.id,
                {"action": "create_sensor"}
            )
        
        return sensor
    
    def get_sensor(self, db: Session, sensor_id: int) -> Optional[Sensor]:
        """Obtener un sensor por ID"""
        return self.repository.get_by_id(db, sensor_id)
    
    def get_all_sensors(self, db: Session, skip: int = 0, limit: int = 100) -> List[Sensor]:
        """Obtener todos los sensores con paginación"""
        return self.repository.get_all(db, skip=skip, limit=limit)
    
    def update_sensor(self, db: Session, sensor_id: int, sensor_data: SensorUpdate, background_tasks: BackgroundTasks = None) -> Optional[Sensor]:
        """Actualizar un sensor"""
        # Verificar que el sensor existe primero
        existing_sensor = self.get_sensor(db, sensor_id)
        if not existing_sensor:
            return None  # Este caso se maneja en el endpoint con 404
        
        # Filtrar campos None
        update_data = {k: v for k, v in sensor_data.model_dump().items() if v is not None}
        if not update_data:
            return existing_sensor  # Sin cambios, devolver el sensor actual
        
        sensor = self.repository.update(db, sensor_id, **update_data)
        if not sensor:
            raise ValueError(f"Error al actualizar el sensor con ID {sensor_id}")
        
        # Emitir evento de actualización usando background task
        if sensor and background_tasks:
            background_tasks.add_task(
                event_emitter.emit_sensor_event,
                EventType.UPDATED,
                {
                    "id": sensor.id,
                    "tipo": sensor.tipo,
                    "modelo": sensor.modelo,
                    "created_at": sensor.created_at.isoformat() if sensor.created_at else None,
                    "updated_at": sensor.updated_at.isoformat() if sensor.updated_at else None,
                    "updated_fields": list(update_data.keys())
                },
                sensor.id,
                {"action": "update_sensor", "fields_updated": list(update_data.keys())}
            )
        
        return sensor
    
    def delete_sensor(self, db: Session, sensor_id: int, background_tasks: BackgroundTasks = None) -> bool:
        """Eliminar un sensor"""
        # Obtener datos del sensor antes de eliminarlo
        sensor = self.get_sensor(db, sensor_id)
        
        deleted = self.repository.delete(db, sensor_id)
        
        # Emitir evento de eliminación usando background task
        if deleted and sensor and background_tasks:
            background_tasks.add_task(
                event_emitter.emit_sensor_event,
                EventType.DELETED,
                {
                    "id": sensor.id,
                    "tipo": sensor.tipo,
                    "modelo": sensor.modelo,
                    "deleted_at": None  # Podríamos agregar un timestamp aquí
                },
                sensor.id,
                {"action": "delete_sensor"}
            )
        
        return deleted
    
    def get_sensors_by_type(self, db: Session, tipo: str) -> List[Sensor]:
        """Obtener sensores por tipo"""
        return self.repository.get_by_tipo(db, tipo)
    
    def sensor_exists(self, db: Session, sensor_id: int) -> bool:
        """Verificar si existe un sensor"""
        return self.repository.exists(db, sensor_id)

# Instancia global del servicio
sensor_service = SensorService()
