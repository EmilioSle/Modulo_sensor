"""
Repositorio específico para Sensores
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from models.sensor import Sensor
from models.lectura import Lectura
from repositories.base import CRUDRepository

class SensorRepository(CRUDRepository[Sensor]):
    """Repositorio para operaciones específicas de Sensor"""
    
    def __init__(self):
        super().__init__(Sensor)
    
    def get_by_tipo(self, db: Session, tipo: str) -> List[Sensor]:
        """Obtener sensores por tipo"""
        return db.query(Sensor).filter(Sensor.tipo == tipo).all()
    
    def get_by_modelo(self, db: Session, modelo: str) -> List[Sensor]:
        """Obtener sensores por modelo"""
        return db.query(Sensor).filter(Sensor.modelo == modelo).all()
    
    def get_with_lecturas(self, db: Session, sensor_id: int) -> Optional[Sensor]:
        """Obtener sensor con sus lecturas"""
        return db.query(Sensor).filter(Sensor.id == sensor_id).first()
    
    def get_sensors_with_recent_readings(self, db: Session, days: int = 7) -> List[Sensor]:
        """Obtener sensores que han tenido lecturas recientes"""
        from datetime import datetime, timedelta, UTC
        cutoff_date = datetime.now(UTC) - timedelta(days=days)
        
        return db.query(Sensor).join(Lectura).filter(
            Lectura.created_at >= cutoff_date
        ).distinct().all()

# Instancia global del repositorio
sensor_repository = SensorRepository()
