"""
Servicio para manejar lógica de negocio de ubicaciones
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks

from models.ubicacion import Ubicacion
from repositories.ubicacion_repository import ubicacion_repository
from repositories.sensor_repository import sensor_repository
from schemas.ubicacion import UbicacionCreate, UbicacionUpdate
from core.events import event_emitter, EventType

class UbicacionService:
    """Servicio para manejar lógica de negocio de ubicaciones"""
    
    def __init__(self):
        self.repository = ubicacion_repository
        self.sensor_repository = sensor_repository
    
    def create_ubicacion(self, db: Session, ubicacion_data: UbicacionCreate, background_tasks: BackgroundTasks = None) -> Ubicacion:
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
        ubicacion_dict = ubicacion_data.model_dump() if hasattr(ubicacion_data, 'model_dump') else ubicacion_data.dict()
        ubicacion = self.repository.create(db, **ubicacion_dict)
        
        if not ubicacion:
            raise ValueError("Error al crear la ubicación en la base de datos")
        
        # Emitir evento de creación usando background task
        if background_tasks:
            background_tasks.add_task(
                event_emitter.emit_ubicacion_event,
                EventType.CREATED,
                {
                    "id": ubicacion.id,
                    "sensor_id": ubicacion.sensor_id,
                    "latitud": ubicacion.latitud,
                    "longitud": ubicacion.longitud,
                    "descripcion": ubicacion.descripcion,
                    "created_at": ubicacion.created_at.isoformat() if ubicacion.created_at else None,
                    "updated_at": ubicacion.updated_at.isoformat() if ubicacion.updated_at else None
                },
                ubicacion.id,
                {"action": "create_ubicacion"}
            )
        
        return ubicacion
    
    def get_ubicacion(self, db: Session, ubicacion_id: int) -> Optional[Ubicacion]:
        """Obtener una ubicación por ID"""
        return self.repository.get_by_id(db, ubicacion_id)
    
    def get_all_ubicaciones(self, db: Session, skip: int = 0, limit: int = 100) -> List[Ubicacion]:
        """Obtener todas las ubicaciones con paginación"""
        return self.repository.get_all(db, skip=skip, limit=limit)
    
    def get_ubicaciones_by_sensor(self, db: Session, sensor_id: int) -> List[Ubicacion]:
        """Obtener ubicaciones de un sensor específico"""
        return self.repository.get_by_sensor(db, sensor_id)
    
    def update_ubicacion(self, db: Session, ubicacion_id: int, ubicacion_data: UbicacionUpdate, background_tasks: BackgroundTasks = None) -> Optional[Ubicacion]:
        """Actualizar una ubicación"""
        # Verificar que la ubicación existe primero
        existing_ubicacion = self.get_ubicacion(db, ubicacion_id)
        if not existing_ubicacion:
            return None  # Se maneja en endpoint con 404
        
        # Filtrar campos None
        update_data = {k: v for k, v in ubicacion_data.model_dump().items() if v is not None}
        if not update_data:
            return existing_ubicacion  # Sin cambios, devolver ubicación actual
        
        # Validar coordenadas si se están actualizando
        if 'latitud' in update_data or 'longitud' in update_data:
            lat = update_data.get('latitud', existing_ubicacion.latitud)
            lng = update_data.get('longitud', existing_ubicacion.longitud)
            self._validate_coordinates(lat, lng)
        
        # Validar sensor si se está actualizando
        if 'sensor_id' in update_data:
            if not self.sensor_repository.exists(db, update_data['sensor_id']):
                raise ValueError(f"Sensor con ID {update_data['sensor_id']} no existe")
        
        ubicacion = self.repository.update(db, ubicacion_id, **update_data)
        if not ubicacion:
            raise ValueError(f"Error al actualizar la ubicación con ID {ubicacion_id}")
        
        # Emitir evento de actualización usando background task
        if ubicacion and background_tasks:
            background_tasks.add_task(
                event_emitter.emit_ubicacion_event,
                EventType.UPDATED,
                {
                    "id": ubicacion.id,
                    "sensor_id": ubicacion.sensor_id,
                    "latitud": ubicacion.latitud,
                    "longitud": ubicacion.longitud,
                    "descripcion": ubicacion.descripcion,
                    "created_at": ubicacion.created_at.isoformat() if ubicacion.created_at else None,
                    "updated_at": ubicacion.updated_at.isoformat() if ubicacion.updated_at else None,
                    "updated_fields": list(update_data.keys())
                },
                ubicacion.id,
                {"action": "update_ubicacion", "fields_updated": list(update_data.keys())}
            )
        
        return ubicacion
    
    def delete_ubicacion(self, db: Session, ubicacion_id: int, background_tasks: BackgroundTasks = None) -> bool:
        """Eliminar una ubicación"""
        # Obtener datos de la ubicación antes de eliminarla
        ubicacion = self.get_ubicacion(db, ubicacion_id)
        
        deleted = self.repository.delete(db, ubicacion_id)
        
        # Emitir evento de eliminación usando background task
        if deleted and ubicacion and background_tasks:
            background_tasks.add_task(
                event_emitter.emit_ubicacion_event,
                EventType.DELETED,
                {
                    "id": ubicacion.id,
                    "sensor_id": ubicacion.sensor_id,
                    "latitud": ubicacion.latitud,
                    "longitud": ubicacion.longitud,
                    "descripcion": ubicacion.descripcion,
                    "deleted_at": None  # Podríamos agregar un timestamp aquí
                },
                ubicacion.id,
                {"action": "delete_ubicacion"}
            )
        
        return deleted
    
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
