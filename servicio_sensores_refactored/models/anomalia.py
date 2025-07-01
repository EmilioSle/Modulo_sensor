"""
Modelo de Anomalía
"""
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base import BaseModel

class Anomalia(BaseModel):
    __tablename__ = "anomalias"
    
    lectura_id = Column(Integer, ForeignKey("lecturas.id"), nullable=False)
    tipo = Column(String, nullable=False)  # "temperatura_alta", "humedad_baja", etc.
    valor = Column(Float, nullable=False)
    
    # Relaciones
    lectura = relationship("Lectura", back_populates="anomalias")
    
    def __repr__(self):
        return f"<Anomalia(id={self.id}, tipo='{self.tipo}', valor={self.valor})>"
