"""
Sistema de eventos para notificaciones en tiempo real
"""
import asyncio
from typing import Any, Dict, Optional, Union
from datetime import datetime
from enum import Enum
import logging

from core.websocket_manager import websocket_manager

logger = logging.getLogger(__name__)

class EventType(str, Enum):
    """Tipos de eventos del sistema"""
    CREATED = "created"
    UPDATED = "updated" 
    DELETED = "deleted"
    ANOMALY_DETECTED = "anomaly_detected"
    PREDICTION_COMPLETED = "prediction_completed"

class EntityType(str, Enum):
    """Tipos de entidades del sistema"""
    SENSOR = "sensor"
    LECTURA = "lectura"
    UBICACION = "ubicacion"
    ANOMALIA = "anomalia"
    PREDICCION = "prediccion"

class EventEmitter:
    """
    Emisor de eventos para notificaciones en tiempo real
    """
    
    @staticmethod
    async def emit_entity_event(
        entity_type: EntityType,
        event_type: EventType,
        entity_data: Dict[str, Any],
        entity_id: Optional[Union[int, str]] = None,
        channel: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Emitir un evento de entidad
        
        Args:
            entity_type: Tipo de entidad (sensor, lectura, etc.)
            event_type: Tipo de evento (created, updated, deleted)
            entity_data: Datos de la entidad
            entity_id: ID de la entidad
            channel: Canal de WebSocket
            metadata: Información adicional
        """
        try:
            event_data = {
                "type": "entity_event",
                "entity_type": entity_type.value,
                "event_type": event_type.value,
                "entity_id": entity_id,
                "data": entity_data,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            await websocket_manager.broadcast_to_channel(channel, event_data)
            logger.info(f"Evento emitido: {entity_type.value} {event_type.value} (ID: {entity_id})")
            
        except Exception as e:
            logger.error(f"Error emitiendo evento: {e}")
    
    @staticmethod 
    async def emit_sensor_event(
        event_type: EventType,
        sensor_data: Dict[str, Any],
        sensor_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Emitir evento específico de sensor"""
        await EventEmitter.emit_entity_event(
            EntityType.SENSOR,
            event_type,
            sensor_data,
            sensor_id,
            "sensors",
            metadata
        )
    
    @staticmethod
    async def emit_lectura_event(
        event_type: EventType,
        lectura_data: Dict[str, Any],
        lectura_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Emitir evento específico de lectura"""
        await EventEmitter.emit_entity_event(
            EntityType.LECTURA,
            event_type,
            lectura_data,
            lectura_id,
            "readings",
            metadata
        )
    
    @staticmethod
    async def emit_ubicacion_event(
        event_type: EventType,
        ubicacion_data: Dict[str, Any],
        ubicacion_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Emitir evento específico de ubicación"""
        await EventEmitter.emit_entity_event(
            EntityType.UBICACION,
            event_type,
            ubicacion_data,
            ubicacion_id,
            "locations",
            metadata
        )
    
    @staticmethod
    async def emit_anomalia_event(
        event_type: EventType,
        anomalia_data: Dict[str, Any],
        anomalia_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Emitir evento específico de anomalía"""
        await EventEmitter.emit_entity_event(
            EntityType.ANOMALIA,
            event_type,
            anomalia_data,
            anomalia_id,
            "anomalies",
            metadata
        )
    
    @staticmethod
    async def emit_prediccion_event(
        event_type: EventType,
        prediccion_data: Dict[str, Any],
        prediccion_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Emitir evento específico de predicción"""
        await EventEmitter.emit_entity_event(
            EntityType.PREDICCION,
            event_type,
            prediccion_data,
            prediccion_id,
            "predictions",
            metadata
        )
    
    @staticmethod
    async def emit_system_event(
        message: str,
        level: str = "info",
        data: Optional[Dict[str, Any]] = None,
        channel: str = "general"
    ):
        """
        Emitir evento del sistema
        
        Args:
            message: Mensaje del evento
            level: Nivel de severidad (info, warning, error)
            data: Datos adicionales
            channel: Canal de WebSocket
        """
        try:
            event_data = {
                "type": "system_event",
                "level": level,
                "message": message,
                "data": data or {},
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket_manager.broadcast_to_channel(channel, event_data)
            logger.info(f"Evento de sistema emitido: {level} - {message}")
            
        except Exception as e:
            logger.error(f"Error emitiendo evento de sistema: {e}")

# Instancia global del emisor
event_emitter = EventEmitter()

# Emitters específicos para cada entidad
class SensorEmitter:
    @staticmethod
    def emit_create(background_tasks, sensor_data, sensor_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_sensor_event, EventType.CREATED, sensor_data, sensor_id, metadata)
    
    @staticmethod
    def emit_update(background_tasks, sensor_data, sensor_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_sensor_event, EventType.UPDATED, sensor_data, sensor_id, metadata)
    
    @staticmethod
    def emit_delete(background_tasks, sensor_data, sensor_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_sensor_event, EventType.DELETED, sensor_data, sensor_id, metadata)

class LecturaEmitter:
    @staticmethod
    def emit_create(background_tasks, lectura_data, lectura_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_lectura_event, EventType.CREATED, lectura_data, lectura_id, metadata)
    
    @staticmethod
    def emit_update(background_tasks, lectura_data, lectura_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_lectura_event, EventType.UPDATED, lectura_data, lectura_id, metadata)
    
    @staticmethod
    def emit_delete(background_tasks, lectura_data, lectura_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_lectura_event, EventType.DELETED, lectura_data, lectura_id, metadata)

class UbicacionEmitter:
    @staticmethod
    def emit_create(background_tasks, ubicacion_data, ubicacion_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_ubicacion_event, EventType.CREATED, ubicacion_data, ubicacion_id, metadata)
    
    @staticmethod
    def emit_update(background_tasks, ubicacion_data, ubicacion_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_ubicacion_event, EventType.UPDATED, ubicacion_data, ubicacion_id, metadata)
    
    @staticmethod
    def emit_delete(background_tasks, ubicacion_data, ubicacion_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_ubicacion_event, EventType.DELETED, ubicacion_data, ubicacion_id, metadata)

class AnomaliaEmitter:
    @staticmethod
    def emit_create(background_tasks, anomalia_data, anomalia_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_anomalia_event, EventType.CREATED, anomalia_data, anomalia_id, metadata)
    
    @staticmethod
    def emit_update(background_tasks, anomalia_data, anomalia_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_anomalia_event, EventType.UPDATED, anomalia_data, anomalia_id, metadata)
    
    @staticmethod
    def emit_delete(background_tasks, anomalia_data, anomalia_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_anomalia_event, EventType.DELETED, anomalia_data, anomalia_id, metadata)

class PrediccionEmitter:
    @staticmethod
    def emit_create(background_tasks, prediccion_data, prediccion_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_prediccion_event, EventType.CREATED, prediccion_data, prediccion_id, metadata)
    
    @staticmethod
    def emit_update(background_tasks, prediccion_data, prediccion_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_prediccion_event, EventType.UPDATED, prediccion_data, prediccion_id, metadata)
    
    @staticmethod
    def emit_delete(background_tasks, prediccion_data, prediccion_id, metadata=None):
        background_tasks.add_task(event_emitter.emit_prediccion_event, EventType.DELETED, prediccion_data, prediccion_id, metadata)

# Instancias de emitters específicos
sensor_emitter = SensorEmitter()
lectura_emitter = LecturaEmitter()
ubicacion_emitter = UbicacionEmitter()
anomalia_emitter = AnomaliaEmitter()
prediccion_emitter = PrediccionEmitter()
