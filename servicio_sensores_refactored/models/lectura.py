"""
Modelo de Lectura
"""
from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base import BaseModel

class Lectura(BaseModel):
    __tablename__ = "lecturas"
    
    sensor_id = Column(Integer, ForeignKey("sensores.id"), nullable=False)
    humedad = Column(Float, nullable=False)
    temperatura = Column(Float, nullable=False)
    
    # Relaciones
    sensor = relationship("Sensor", back_populates="lecturas")
    anomalias = relationship("Anomalia", back_populates="lectura", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lectura(id={self.id}, sensor_id={self.sensor_id}, temp={self.temperatura}, hum={self.humedad})>"
