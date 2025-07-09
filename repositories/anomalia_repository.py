"""
Repositorio específico para Anomalías
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, UTC, timedelta

from models.anomalia import Anomalia
from repositories.base import CRUDRepository

class AnomaliaRepository(CRUDRepository[Anomalia]):
    """Repositorio para operaciones específicas de Anomalía"""
    
    def __init__(self):
        super().__init__(Anomalia)
    
    def get_by_lectura(self, db: Session, lectura_id: int) -> List[Anomalia]:
        """Obtener anomalías por lectura"""
        return db.query(Anomalia).filter(Anomalia.lectura_id == lectura_id).all()
    
    def get_by_tipo(self, db: Session, tipo: str) -> List[Anomalia]:
        """Obtener anomalías por tipo"""
        return db.query(Anomalia).filter(Anomalia.tipo == tipo).all()
    
    def get_recent_anomalies(self, db: Session, hours: int = 24) -> List[Anomalia]:
        """Obtener anomalías recientes"""
        cutoff_date = datetime.now(UTC) - timedelta(hours=hours)
        
        return db.query(Anomalia).filter(
            Anomalia.created_at >= cutoff_date
        ).order_by(Anomalia.created_at.desc()).all()
    
    def get_anomalies_by_value_range(
        self, 
        db: Session, 
        min_valor: float, 
        max_valor: float
    ) -> List[Anomalia]:
        """Obtener anomalías por rango de valor"""
        return db.query(Anomalia).filter(
            Anomalia.valor.between(min_valor, max_valor)
        ).all()
    
    def get_critical_anomalies(self, db: Session, threshold: float = 50.0) -> List[Anomalia]:
        """Obtener anomalías críticas (valor alto)"""
        return db.query(Anomalia).filter(
            Anomalia.valor >= threshold
        ).order_by(Anomalia.valor.desc()).all()
    
    def count_by_type(self, db: Session) -> dict:
        """Contar anomalías por tipo"""
        from sqlalchemy import func
        
        result = db.query(
            Anomalia.tipo,
            func.count(Anomalia.id).label('count')
        ).group_by(Anomalia.tipo).all()
        
        return {tipo: count for tipo, count in result}

# Instancia global del repositorio
anomalia_repository = AnomaliaRepository()
