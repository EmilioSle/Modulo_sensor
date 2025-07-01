"""
Repositorio específico para Predicciones de Sequía
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, UTC, timedelta

from models.prediccion import PrediccionSequia
from repositories.base import CRUDRepository

class PrediccionRepository(CRUDRepository[PrediccionSequia]):
    """Repositorio para operaciones específicas de Predicción"""
    
    def __init__(self):
        super().__init__(PrediccionSequia)
    
    def get_by_ubicacion(self, db: Session, ubicacion_id: int) -> List[PrediccionSequia]:
        """Obtener predicciones por ubicación"""
        return db.query(PrediccionSequia).filter(
            PrediccionSequia.ubicacion_id == ubicacion_id
        ).order_by(PrediccionSequia.created_at.desc()).all()
    
    def get_recent_predictions(self, db: Session, days: int = 30) -> List[PrediccionSequia]:
        """Obtener predicciones recientes"""
        cutoff_date = datetime.now(UTC) - timedelta(days=days)
        
        return db.query(PrediccionSequia).filter(
            PrediccionSequia.created_at >= cutoff_date
        ).order_by(PrediccionSequia.created_at.desc()).all()
    
    def get_high_risk_predictions(self, db: Session, threshold: float = 0.7) -> List[PrediccionSequia]:
        """Obtener predicciones de alto riesgo"""
        return db.query(PrediccionSequia).filter(
            PrediccionSequia.probabilidad >= threshold
        ).order_by(PrediccionSequia.probabilidad.desc()).all()
    
    def get_predictions_by_probability_range(
        self, 
        db: Session, 
        min_prob: float, 
        max_prob: float
    ) -> List[PrediccionSequia]:
        """Obtener predicciones por rango de probabilidad"""
        return db.query(PrediccionSequia).filter(
            PrediccionSequia.probabilidad.between(min_prob, max_prob)
        ).all()
    
    def get_latest_prediction_by_location(
        self, 
        db: Session, 
        ubicacion_id: int
    ) -> Optional[PrediccionSequia]:
        """Obtener la predicción más reciente de una ubicación"""
        return db.query(PrediccionSequia).filter(
            PrediccionSequia.ubicacion_id == ubicacion_id
        ).order_by(PrediccionSequia.created_at.desc()).first()
    
    def get_average_probability_by_location(self, db: Session, ubicacion_id: int) -> Optional[float]:
        """Obtener probabilidad promedio de una ubicación"""
        from sqlalchemy import func
        
        result = db.query(func.avg(PrediccionSequia.probabilidad)).filter(
            PrediccionSequia.ubicacion_id == ubicacion_id
        ).scalar()
        
        return float(result) if result else None

# Instancia global del repositorio
prediccion_repository = PrediccionRepository()
