"""
Modelo de Ubicación
"""
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base import BaseModel

class Ubicacion(BaseModel):
    __tablename__ = "ubicaciones"
    
    sensor_id = Column(Integer, ForeignKey("sensores.id"), nullable=False)
    latitud = Column(String, nullable=False)
    longitud = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    
    # Relaciones
    sensor = relationship("Sensor", back_populates="ubicaciones")
    predicciones = relationship("PrediccionSequia", back_populates="ubicacion", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Ubicacion(id={self.id}, lat={self.latitud}, lng={self.longitud})>"
