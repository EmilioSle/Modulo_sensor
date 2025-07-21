"""
Servicio para manejo de predicciones de sequía
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from repositories.prediccion_repository import PrediccionRepository
from models.prediccion import PrediccionSequia
from schemas.prediccion import PrediccionCreate, PrediccionUpdate
from core.ml_utils import ml_manager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PrediccionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PrediccionRepository(db)

    def create(self, prediccion_data: PrediccionCreate) -> PrediccionSequia:
        """Crear nueva predicción"""
        return self.repository.create(self.db, **prediccion_data.dict())

    def get_by_id(self, prediccion_id: int) -> Optional[PrediccionSequia]:
        """Obtener predicción por ID"""
        return self.repository.get_by_id(self.db, prediccion_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[PrediccionSequia]:
        """Obtener todas las predicciones"""
        return self.repository.get_all(self.db, skip=skip, limit=limit)

    def update(self, prediccion_id: int, prediccion_data: PrediccionUpdate) -> Optional[PrediccionSequia]:
        """Actualizar predicción"""
        return self.repository.update(self.db, prediccion_id, **prediccion_data.dict(exclude_unset=True))

    def delete(self, prediccion_id: int) -> bool:
        """Eliminar predicción"""
        return self.repository.delete(self.db, prediccion_id)

    def get_by_ubicacion(self, ubicacion_id: int) -> List[PrediccionSequia]:
        """Obtener predicciones por ubicación"""
        return self.repository.get_multi_by_field(self.db, "ubicacion_id", ubicacion_id)

    def get_high_risk_predictions(self, threshold: float = 0.7) -> List[PrediccionSequia]:
        """Obtener predicciones de alto riesgo"""
        return self.db.query(PrediccionSequia).filter(
            PrediccionSequia.probabilidad >= threshold
        ).all()

    def get_latest_by_ubicacion(self, ubicacion_id: int) -> Optional[PrediccionSequia]:
        """Obtener la predicción más reciente para una ubicación"""
        return self.db.query(PrediccionSequia).filter(
            PrediccionSequia.ubicacion_id == ubicacion_id
        ).order_by(PrediccionSequia.fecha_prediccion.desc()).first()

    def generate_prediction(self, ubicacion_id: int, temperatura_promedio: float, 
                          humedad_promedio: float, comentario: str = "") -> PrediccionSequia:
        """Generar predicción automática usando ML o lógica heurística"""
        try:
            # Usar el gestor ML para calcular probabilidad
            probabilidad = ml_manager.predict_drought_probability(temperatura_promedio, humedad_promedio)
            
            # Analizar nivel de riesgo
            risk_level = ml_manager.analyze_risk_level(probabilidad)
            
            # Generar comentario automático si no se proporciona
            if not comentario:
                comentario = (f"Predicción automática: T={temperatura_promedio}°C, H={humedad_promedio}% "
                            f"| Riesgo: {risk_level} | Prob: {probabilidad:.1%}")
            
            # Agregar recomendaciones
            recommendations = ml_manager.get_recommendations(probabilidad)
            comentario += f" | {recommendations}"
            
            prediccion_data = PrediccionCreate(
                ubicacion_id=ubicacion_id,
                probabilidad=probabilidad,
                comentario=comentario
            )
            
            logger.info(f"Predicción generada para ubicación {ubicacion_id}: {probabilidad:.1%} de riesgo")
            return self.repository.create(self.db, **prediccion_data.dict())
            
        except Exception as e:
            logger.error(f"Error generando predicción: {e}")
            # Fallback con lógica simple
            return self._generate_fallback_prediction(ubicacion_id, temperatura_promedio, humedad_promedio, comentario)

    def _generate_fallback_prediction(self, ubicacion_id: int, temperatura: float, 
                                    humedad: float, comentario: str) -> PrediccionSequia:
        """Predicción de fallback en caso de error con ML"""
        # Lógica muy simple
        probabilidad = max(0.1, min(0.9, (temperatura - 20) / 30 + (100 - humedad) / 200))
        
        if not comentario:
            comentario = f"Predicción básica: T={temperatura}°C, H={humedad}% | Prob: {probabilidad:.1%}"
        
        prediccion_data = PrediccionCreate(
            ubicacion_id=ubicacion_id,
            probabilidad=probabilidad,
            comentario=comentario + " (método fallback)"
        )
        
        return self.repository.create(self.db, **prediccion_data.dict())

    def get_statistics(self) -> dict:
        """Obtener estadísticas de predicciones"""
        all_predictions = self.repository.get_all(self.db)
        
        if not all_predictions:
            return {
                "total": 0,
                "probabilidad_promedio": 0.0,
                "alto_riesgo": 0,
                "medio_riesgo": 0,
                "bajo_riesgo": 0
            }
        
        total = len(all_predictions)
        probabilidades = [p.probabilidad for p in all_predictions]
        promedio = sum(probabilidades) / total
        
        alto_riesgo = sum(1 for p in probabilidades if p >= 0.7)
        medio_riesgo = sum(1 for p in probabilidades if 0.3 <= p < 0.7)
        bajo_riesgo = sum(1 for p in probabilidades if p < 0.3)
        
        return {
            "total": total,
            "probabilidad_promedio": round(promedio, 3),
            "alto_riesgo": alto_riesgo,
            "medio_riesgo": medio_riesgo,
            "bajo_riesgo": bajo_riesgo
        }

    def analyze_trends(self, ubicacion_id: int, days: int = 30) -> dict:
        """Analizar tendencias de predicciones para una ubicación"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        recent_predictions = self.db.query(PrediccionSequia).filter(
            and_(
                PrediccionSequia.ubicacion_id == ubicacion_id,
                PrediccionSequia.fecha_prediccion >= cutoff_date
            )
        ).order_by(PrediccionSequia.fecha_prediccion.desc()).all()
        
        if not recent_predictions:
            return {"trend": "sin_datos", "predictions": 0, "avg_probability": 0.0}
        
        probabilities = [p.probabilidad for p in recent_predictions]
        avg_prob = sum(probabilities) / len(probabilities)
        
        # Analizar tendencia (comparar primera mitad vs segunda mitad)
        mid_point = len(probabilities) // 2
        if mid_point > 0:
            recent_avg = sum(probabilities[:mid_point]) / mid_point
            older_avg = sum(probabilities[mid_point:]) / (len(probabilities) - mid_point)
            
            if recent_avg > older_avg + 0.1:
                trend = "empeorando"
            elif recent_avg < older_avg - 0.1:
                trend = "mejorando"
            else:
                trend = "estable"
        else:
            trend = "insuficientes_datos"
        
        return {
            "trend": trend,
            "predictions": len(recent_predictions),
            "avg_probability": round(avg_prob, 3),
            "latest_probability": probabilities[0] if probabilities else 0.0
        }
from typing import List, Optional
from sqlalchemy.orm import Session
import pickle
import os

from models.prediccion import PrediccionSequia
from repositories.prediccion_repository import prediccion_repository
from repositories.ubicacion_repository import ubicacion_repository
from schemas.prediccion import PrediccionCreate, PrediccionUpdate

class PrediccionService:
    """Servicio para manejar lógica de negocio de predicciones"""
    
    def __init__(self):
        self.repository = prediccion_repository
        self.ubicacion_repository = ubicacion_repository
        self._load_ml_model()
    
    def create_prediccion(self, db: Session, prediccion_data: PrediccionCreate) -> PrediccionSequia:
        """Crear una nueva predicción"""
        # Validar que la ubicación existe
        if not self.ubicacion_repository.get_by_id(db, prediccion_data.ubicacion_id):
            raise ValueError(f"Ubicación con ID {prediccion_data.ubicacion_id} no existe")
        
        # Validar probabilidad
        self._validate_probability(prediccion_data.probabilidad)
        
        return self.repository.create(db, **prediccion_data.model_dump())
    
    def get_prediccion(self, db: Session, prediccion_id: int) -> Optional[PrediccionSequia]:
        """Obtener una predicción por ID"""
        return self.repository.get_by_id(db, prediccion_id)
    
    def get_all_predicciones(self, db: Session, skip: int = 0, limit: int = 100) -> List[PrediccionSequia]:
        """Obtener todas las predicciones con paginación"""
        return self.repository.get_all(db, skip=skip, limit=limit)
    
    def get_predicciones_by_ubicacion(self, db: Session, ubicacion_id: int) -> List[PrediccionSequia]:
        """Obtener predicciones de una ubicación específica"""
        return self.repository.get_by_ubicacion(db, ubicacion_id)
    
    def get_latest_prediction_by_location(self, db: Session, ubicacion_id: int) -> Optional[PrediccionSequia]:
        """Obtener la predicción más reciente de una ubicación"""
        return self.repository.get_latest_prediction_by_location(db, ubicacion_id)
    
    def get_high_risk_predictions(self, db: Session, threshold: float = 0.7) -> List[PrediccionSequia]:
        """Obtener predicciones de alto riesgo"""
        return self.repository.get_high_risk_predictions(db, threshold)
    
    def get_recent_predictions(self, db: Session, days: int = 30) -> List[PrediccionSequia]:
        """Obtener predicciones recientes"""
        return self.repository.get_recent_predictions(db, days)
    
    def update_prediccion(self, db: Session, prediccion_id: int, prediccion_data: PrediccionUpdate) -> Optional[PrediccionSequia]:
        """Actualizar una predicción"""
        # Filtrar campos None
        update_data = {k: v for k, v in prediccion_data.model_dump().items() if v is not None}
        if not update_data:
            return self.get_prediccion(db, prediccion_id)
        
        # Validar ubicación si se está actualizando
        if 'ubicacion_id' in update_data:
            if not self.ubicacion_repository.get_by_id(db, update_data['ubicacion_id']):
                raise ValueError(f"Ubicación con ID {update_data['ubicacion_id']} no existe")
        
        # Validar probabilidad si se está actualizando
        if 'probabilidad' in update_data:
            self._validate_probability(update_data['probabilidad'])
        
        return self.repository.update(db, prediccion_id, **update_data)
    
    def delete_prediccion(self, db: Session, prediccion_id: int) -> bool:
        """Eliminar una predicción"""
        return self.repository.delete(db, prediccion_id)
    
    def generate_prediction_with_ml(
        self, 
        db: Session, 
        ubicacion_id: int,
        temperatura_promedio: float,
        humedad_promedio: float,
        comentario: Optional[str] = None
    ) -> PrediccionSequia:
        """Generar una predicción usando el modelo de ML"""
        
        # Validar que la ubicación existe
        if not self.ubicacion_repository.get_by_id(db, ubicacion_id):
            raise ValueError(f"Ubicación con ID {ubicacion_id} no existe")
        
        try:
            # Usar el modelo de ML si está disponible
            if hasattr(self, 'ml_model') and self.ml_model is not None:
                # Preparar datos para el modelo
                features = [[temperatura_promedio, humedad_promedio]]
                probabilidad = float(self.ml_model.predict_proba(features)[0][1])  # Probabilidad de sequía
            else:
                # Fallback: usar lógica simple basada en reglas
                probabilidad = self._calculate_drought_probability_simple(
                    temperatura_promedio, 
                    humedad_promedio
                )
            
            # Crear la predicción
            prediccion_data = PrediccionCreate(
                ubicacion_id=ubicacion_id,
                probabilidad=probabilidad,
                comentario=comentario or f"Predicción automática basada en T:{temperatura_promedio}°C, H:{humedad_promedio}%"
            )
            
            return self.create_prediccion(db, prediccion_data)
            
        except Exception as e:
            raise ValueError(f"Error generando predicción: {str(e)}")
    
    def get_prediction_statistics(self, db: Session) -> dict:
        """Obtener estadísticas de predicciones"""
        all_predictions = self.repository.get_all(db)
        
        if not all_predictions:
            return {
                "total": 0,
                "probabilidad_promedio": 0.0,
                "alto_riesgo": 0,
                "bajo_riesgo": 0
            }
        
        probabilidades = [p.probabilidad for p in all_predictions]
        
        return {
            "total": len(all_predictions),
            "probabilidad_promedio": sum(probabilidades) / len(probabilidades),
            "alto_riesgo": len([p for p in probabilidades if p >= 0.7]),
            "medio_riesgo": len([p for p in probabilidades if 0.3 <= p < 0.7]),
            "bajo_riesgo": len([p for p in probabilidades if p < 0.3])
        }
    
    def _load_ml_model(self):
        """Cargar el modelo de ML para predicciones"""
        model_path = os.path.join(os.path.dirname(__file__), "..", "ml_models", "modelo_sequia.pkl")
        
        try:
            if os.path.exists(model_path):
                with open(model_path, 'rb') as file:
                    self.ml_model = pickle.load(file)
            else:
                self.ml_model = None
                print(f"Modelo ML no encontrado en {model_path}. Usando lógica simple.")
        except Exception as e:
            print(f"Error cargando modelo ML: {e}. Usando lógica simple.")
            self.ml_model = None
    
    def _calculate_drought_probability_simple(self, temperatura: float, humedad: float) -> float:
        """Calcular probabilidad de sequía usando lógica simple"""
        # Lógica básica: alta temperatura + baja humedad = mayor probabilidad de sequía
        
        # Normalizar temperatura (0-1, donde 1 es muy alta)
        temp_factor = min(1.0, max(0.0, (temperatura - 20) / 20))  # 20°C = 0, 40°C+ = 1
        
        # Normalizar humedad invertida (0-1, donde 1 es muy baja humedad)
        humidity_factor = min(1.0, max(0.0, (80 - humedad) / 80))  # 80% = 0, 0% = 1
        
        # Combinar factores con pesos
        probability = (temp_factor * 0.6) + (humidity_factor * 0.4)
        
        # Asegurar que esté en el rango válido
        return min(1.0, max(0.0, probability))
    
    def _validate_probability(self, probabilidad: float):
        """Validar que la probabilidad esté en el rango correcto"""
        if not (0.0 <= probabilidad <= 1.0):
            raise ValueError(f"Probabilidad {probabilidad} debe estar entre 0.0 y 1.0")

# Instancia global del servicio
prediccion_service = PrediccionService()
