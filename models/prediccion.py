"""
Modelo de Predicción de Sequía
"""
from sqlalchemy import Column, Float, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from models.base import BaseModel

class PrediccionSequia(BaseModel):
    __tablename__ = "predicciones_sequia"
    
    ubicacion_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=False)
    probabilidad = Column(Float, nullable=False)
    comentario = Column(String, nullable=True)
    fecha_prediccion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    ubicacion = relationship("Ubicacion", back_populates="predicciones")
    
    def __repr__(self):
        return f"<PrediccionSequia(id={self.id}, prob={self.probabilidad})>"
