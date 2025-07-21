"""
Servicio para manejar lógica de negocio de anomalías
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from models.anomalia import Anomalia
from repositories.anomalia_repository import anomalia_repository
from repositories.lectura_repository import lectura_repository
from schemas.anomalia import AnomaliaCreate, AnomaliaUpdate

class AnomaliaService:
    """Servicio para manejar lógica de negocio de anomalías"""
    
    def __init__(self):
        self.repository = anomalia_repository
        self.lectura_repository = lectura_repository
    
    def create_anomalia(self, db: Session, anomalia_data: AnomaliaCreate) -> Anomalia:
        """Crear una nueva anomalía"""
        # Validar que la lectura existe
        if not self.lectura_repository.get_by_id(db, anomalia_data.lectura_id):
            raise ValueError(f"Lectura con ID {anomalia_data.lectura_id} no existe")
        
        # Validar el tipo de anomalía
        self._validate_anomaly_type(anomalia_data.tipo)
        
        # Validar el valor de la anomalía
        self._validate_anomaly_value(anomalia_data.tipo, anomalia_data.valor)
        
        # Crear la anomalía
        return self.repository.create(db, **anomalia_data.dict())
        
    def get_anomalia(self, db: Session, anomalia_id: int) -> Optional[Anomalia]:
        """Obtener una anomalía por ID"""
        return self.repository.get_by_id(db, anomalia_id)
    
    def get_all_anomalias(self, db: Session, skip: int = 0, limit: int = 100) -> List[Anomalia]:
        """Obtener todas las anomalías con paginación"""
        return self.repository.get_all(db, skip=skip, limit=limit)
    
    def get_anomalias_by_lectura(self, db: Session, lectura_id: int) -> List[Anomalia]:
        """Obtener anomalías de una lectura específica"""
        return self.repository.get_by_lectura(db, lectura_id)
    
    def get_anomalias_by_tipo(self, db: Session, tipo: str) -> List[Anomalia]:
        """Obtener anomalías por tipo"""
        return self.repository.get_by_tipo(db, tipo)
    
    def get_recent_anomalias(self, db: Session, hours: int = 24) -> List[Anomalia]:
        """Obtener anomalías recientes"""
        return self.repository.get_recent_anomalies(db, hours)
    
    def get_critical_anomalias(self, db: Session, threshold: float = 50.0) -> List[Anomalia]:
        """Obtener anomalías críticas"""
        return self.repository.get_critical_anomalies(db, threshold)
    
    def update_anomalia(self, db: Session, anomalia_id: int, anomalia_data: AnomaliaUpdate) -> Optional[Anomalia]:
        """Actualizar anomalía"""
        # Validar el tipo de anomalía si se proporciona
        if anomalia_data.tipo is not None:
            self._validate_anomaly_type(anomalia_data.tipo)
        
        # Validar el valor de la anomalía si se proporciona
        if anomalia_data.tipo is not None and anomalia_data.valor is not None:
            self._validate_anomaly_value(anomalia_data.tipo, anomalia_data.valor)
        
        # Validar que la lectura existe si se proporciona
        if anomalia_data.lectura_id is not None:
            if not self.lectura_repository.get_by_id(db, anomalia_data.lectura_id):
                raise ValueError(f"Lectura con ID {anomalia_data.lectura_id} no existe")
        
        return self.repository.update(db, anomalia_id, **anomalia_data.dict(exclude_unset=True))
        
    def delete_anomalia(self, db: Session, anomalia_id: int) -> bool:
        """Eliminar una anomalía"""
        return self.repository.delete(db, anomalia_id)
    
    def get_anomaly_statistics(self, db: Session) -> dict:
        """Obtener estadísticas de anomalías"""
        return {
            "total": self.repository.count(db),
            "por_tipo": self.repository.count_by_type(db),
            "recientes_24h": len(self.get_recent_anomalias(db, 24)),
            "criticas": len(self.get_critical_anomalias(db))
        }
    
    def detect_anomalies_in_reading(self, db: Session, lectura_id: int) -> List[Anomalia]:
        """Detectar anomalías automáticamente en una lectura"""
        lectura = self.lectura_repository.get_by_id(db, lectura_id)
        if not lectura:
            raise ValueError(f"Lectura con ID {lectura_id} no existe")
        
        anomalias_detectadas = []
        
        # Detectar temperatura alta
        if lectura.temperatura > 35:
            anomalia_data = AnomaliaCreate(
                lectura_id=lectura_id,
                tipo="temperatura_alta",
                valor=lectura.temperatura
            )
            anomalias_detectadas.append(self.create_anomalia(db, anomalia_data))
        
        # Detectar temperatura baja
        if lectura.temperatura < 5:
            anomalia_data = AnomaliaCreate(
                lectura_id=lectura_id,
                tipo="temperatura_baja",
                valor=lectura.temperatura
            )
            anomalias_detectadas.append(self.create_anomalia(db, anomalia_data))
        
        # Detectar humedad alta
        if lectura.humedad > 90:
            anomalia_data = AnomaliaCreate(
                lectura_id=lectura_id,
                tipo="humedad_alta",
                valor=lectura.humedad
            )
            anomalias_detectadas.append(self.create_anomalia(db, anomalia_data))
        
        # Detectar humedad baja
        if lectura.humedad < 10:
            anomalia_data = AnomaliaCreate(
                lectura_id=lectura_id,
                tipo="humedad_baja",
                valor=lectura.humedad
            )
            anomalias_detectadas.append(self.create_anomalia(db, anomalia_data))
        
        return anomalias_detectadas
    
    def _validate_anomaly_type(self, tipo: str):
        """Validar que el tipo de anomalía sea válido"""
        valid_types = [
            "temperatura_alta", "temperatura_baja",
            "humedad_alta", "humedad_baja",
            "sensor_desconectado", "lectura_invalida"
        ]
        
        if tipo not in valid_types:
            raise ValueError(f"Tipo de anomalía '{tipo}' no válido. Tipos válidos: {valid_types}")
    
    def _validate_anomaly_value(self, tipo: str, valor: float):
        """Validar que el valor de la anomalía sea coherente con su tipo"""
        if tipo in ["temperatura_alta", "temperatura_baja"]:
            if not (-50 <= valor <= 70):
                raise ValueError(f"Valor de temperatura {valor} fuera del rango válido (-50°C a 70°C)")
        
        elif tipo in ["humedad_alta", "humedad_baja"]:
            if not (0 <= valor <= 100):
                raise ValueError(f"Valor de humedad {valor} fuera del rango válido (0% a 100%)")

# Instancia global del servicio
anomalia_service = AnomaliaService()
