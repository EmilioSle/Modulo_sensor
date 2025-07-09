"""
Repositorio específico para Lecturas
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, UTC

from models.lectura import Lectura
from repositories.base import CRUDRepository

class LecturaRepository(CRUDRepository[Lectura]):
    """Repositorio para operaciones específicas de Lectura"""
    
    def __init__(self):
        super().__init__(Lectura)
    
    def get_by_sensor(self, db: Session, sensor_id: int) -> List[Lectura]:
        """Obtener lecturas por sensor"""
        return db.query(Lectura).filter(Lectura.sensor_id == sensor_id).all()
    
    def get_recent_readings(self, db: Session, sensor_id: int, hours: int = 24) -> List[Lectura]:
        """Obtener lecturas recientes de un sensor"""
        from datetime import timedelta
        cutoff_date = datetime.now(UTC) - timedelta(hours=hours)
        
        return db.query(Lectura).filter(
            Lectura.sensor_id == sensor_id,
            Lectura.created_at >= cutoff_date
        ).order_by(Lectura.created_at.desc()).all()
    
    def get_readings_by_temperature_range(
        self, 
        db: Session, 
        min_temp: float, 
        max_temp: float
    ) -> List[Lectura]:
        """Obtener lecturas por rango de temperatura"""
        return db.query(Lectura).filter(
            Lectura.temperatura.between(min_temp, max_temp)
        ).all()
    
    def get_readings_by_humidity_range(
        self, 
        db: Session, 
        min_hum: float, 
        max_hum: float
    ) -> List[Lectura]:
        """Obtener lecturas por rango de humedad"""
        return db.query(Lectura).filter(
            Lectura.humedad.between(min_hum, max_hum)
        ).all()
    
    def get_average_temperature(self, db: Session, sensor_id: int) -> Optional[float]:
        """Obtener temperatura promedio de un sensor"""
        from sqlalchemy import func
        result = db.query(func.avg(Lectura.temperatura)).filter(
            Lectura.sensor_id == sensor_id
        ).scalar()
        return float(result) if result else None
    
    def get_average_humidity(self, db: Session, sensor_id: int) -> Optional[float]:
        """Obtener humedad promedio de un sensor"""
        from sqlalchemy import func
        result = db.query(func.avg(Lectura.humedad)).filter(
            Lectura.sensor_id == sensor_id
        ).scalar()
        return float(result) if result else None

# Instancia global del repositorio
lectura_repository = LecturaRepository()
