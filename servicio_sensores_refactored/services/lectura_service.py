"""
Servicio para manejar lógica de negocio de lecturas
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models.lectura import Lectura
from repositories.lectura_repository import lectura_repository
from repositories.sensor_repository import sensor_repository
from schemas.lectura import LecturaCreate, LecturaUpdate

class LecturaService:
    """Servicio para manejar lógica de negocio de lecturas"""
    
    def __init__(self):
        self.repository = lectura_repository
        self.sensor_repository = sensor_repository
    
    def create_lectura(self, db: Session, lectura_data: LecturaCreate) -> Lectura:
        """Crear una nueva lectura"""
        # Validar que el sensor existe
        if not self.sensor_repository.exists(db, lectura_data.sensor_id):
            raise ValueError(f"Sensor con ID {lectura_data.sensor_id} no existe")
        
        # Aquí puedes agregar más validaciones de negocio
        self._validate_reading_values(lectura_data)
        
        return self.repository.create(db, **lectura_data.model_dump())
    
    def get_lectura(self, db: Session, lectura_id: int) -> Optional[Lectura]:
        """Obtener una lectura por ID"""
        return self.repository.get_by_id(db, lectura_id)
    
    def get_readings_by_sensor(self, db: Session, sensor_id: int) -> List[Lectura]:
        """Obtener lecturas de un sensor específico"""
        return self.repository.get_by_sensor(db, sensor_id)
    
    def get_recent_readings(self, db: Session, sensor_id: int, hours: int = 24) -> List[Lectura]:
        """Obtener lecturas recientes de un sensor"""
        return self.repository.get_recent_readings(db, sensor_id, hours)
    
    def update_lectura(self, db: Session, lectura_id: int, lectura_data: LecturaUpdate) -> Optional[Lectura]:
        """Actualizar una lectura"""
        # Filtrar campos None
        update_data = {k: v for k, v in lectura_data.model_dump().items() if v is not None}
        if not update_data:
            return self.get_lectura(db, lectura_id)
        
        # Validar valores si se están actualizando
        if 'temperatura' in update_data or 'humedad' in update_data:
            temp_lectura = LecturaCreate(
                sensor_id=1,  # Temporal, solo para validación
                temperatura=update_data.get('temperatura', 0),
                humedad=update_data.get('humedad', 0)
            )
            self._validate_reading_values(temp_lectura)
        
        return self.repository.update(db, lectura_id, **update_data)
    
    def delete_lectura(self, db: Session, lectura_id: int) -> bool:
        """Eliminar una lectura"""
        return self.repository.delete(db, lectura_id)
    
    def get_sensor_stats(self, db: Session, sensor_id: int) -> dict:
        """Obtener estadísticas de un sensor"""
        avg_temp = self.repository.get_average_temperature(db, sensor_id)
        avg_hum = self.repository.get_average_humidity(db, sensor_id)
        
        return {
            "temperatura_promedio": avg_temp,
            "humedad_promedio": avg_hum,
            "total_lecturas": len(self.get_readings_by_sensor(db, sensor_id))
        }
    
    def _validate_reading_values(self, lectura: LecturaCreate):
        """Validar que los valores de la lectura son razonables"""
        if lectura.temperatura < -50 or lectura.temperatura > 60:
            raise ValueError("Temperatura fuera del rango válido (-50°C a 60°C)")
        
        if lectura.humedad < 0 or lectura.humedad > 100:
            raise ValueError("Humedad fuera del rango válido (0% a 100%)")

# Instancia global del servicio
lectura_service = LecturaService()
