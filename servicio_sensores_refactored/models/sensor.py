"""
Modelo de Sensor
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base import BaseModel

class Sensor(BaseModel):
    __tablename__ = "sensores"
    
    tipo = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    
    # Relaciones
    lecturas = relationship("Lectura", back_populates="sensor", cascade="all, delete-orphan")
    ubicaciones = relationship("Ubicacion", back_populates="sensor", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Sensor(id={self.id}, tipo='{self.tipo}', modelo='{self.modelo}')>"
