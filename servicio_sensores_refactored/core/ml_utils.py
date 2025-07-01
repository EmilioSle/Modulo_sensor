"""
Configuración y utilidades para modelos de Machine Learning
"""
import pickle
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class MLModelManager:
    """Gestor de modelos de Machine Learning"""
    
    def __init__(self):
        self.models = {}
        self.base_path = os.path.join(os.path.dirname(__file__), "..", "ml_models")
        
    def load_model(self, model_name: str) -> Optional[Any]:
        """Cargar modelo desde archivo"""
        try:
            model_path = os.path.join(self.base_path, f"{model_name}.pkl")
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                self.models[model_name] = model
                logger.info(f"Modelo {model_name} cargado exitosamente")
                return model
            else:
                logger.warning(f"Modelo {model_name} no encontrado en {model_path}")
                return None
        except Exception as e:
            logger.error(f"Error cargando modelo {model_name}: {e}")
            return None
    
    def get_model(self, model_name: str) -> Optional[Any]:
        """Obtener modelo (cargándolo si es necesario)"""
        if model_name not in self.models:
            return self.load_model(model_name)
        return self.models[model_name]

    def predict_drought_probability(self, temperatura_promedio: float, humedad_promedio: float) -> float:
        """
        Predecir probabilidad de sequía usando modelo ML o lógica heurística
        """
        # Intentar usar modelo ML primero
        model = self.get_model("modelo_sequia")
        
        if model:
            try:
                # Si existe el modelo, usarlo para predicción
                features = [[temperatura_promedio, humedad_promedio]]
                prediction = model.predict_proba(features)[0][1]  # Probabilidad de clase positiva
                return float(prediction)
            except Exception as e:
                logger.error(f"Error usando modelo ML: {e}")
        
        # Usar lógica heurística como fallback
        return self._heuristic_drought_prediction(temperatura_promedio, humedad_promedio)
    
    def _heuristic_drought_prediction(self, temperatura: float, humedad: float) -> float:
        """
        Lógica heurística para predecir sequía basada en temperatura y humedad
        """
        # Normalizar valores
        # Temperatura: 15-40°C -> 0-1
        temp_normalized = max(0, min(1, (temperatura - 15) / 25))
        
        # Humedad: 0-100% -> 1-0 (invertida porque menos humedad = más riesgo)
        humidity_normalized = max(0, min(1, 1 - (humedad / 100)))
        
        # Cálculo ponderado (temperatura 60%, humedad 40%)
        drought_probability = (temp_normalized * 0.6) + (humidity_normalized * 0.4)
        
        # Aplicar función sigmoid suave para valores más realistas
        import math
        sigmoid_prob = 1 / (1 + math.exp(-5 * (drought_probability - 0.5)))
        
        # Limitar entre 0.1 y 0.9 para evitar certezas absolutas
        final_prob = max(0.1, min(0.9, sigmoid_prob))
        
        return round(final_prob, 3)

    def analyze_risk_level(self, probabilidad: float) -> str:
        """Analizar nivel de riesgo basado en probabilidad"""
        if probabilidad >= 0.7:
            return "ALTO"
        elif probabilidad >= 0.4:
            return "MEDIO"
        else:
            return "BAJO"

    def get_recommendations(self, probabilidad: float, ubicacion_descripcion: str = "") -> str:
        """Generar recomendaciones basadas en el riesgo"""
        risk_level = self.analyze_risk_level(probabilidad)
        
        base_recommendations = {
            "ALTO": [
                "Implementar sistemas de riego de emergencia",
                "Reducir el consumo de agua no esencial",
                "Monitorear cultivos diariamente",
                "Considerar cultivos resistentes a la sequía"
            ],
            "MEDIO": [
                "Optimizar sistemas de riego existentes",
                "Monitorear niveles de humedad del suelo",
                "Preparar medidas de contingencia",
                "Evaluar reservas de agua"
            ],
            "BAJO": [
                "Continuar monitoreo regular",
                "Mantener sistemas de riego en buen estado",
                "Revisar planes de contingencia"
            ]
        }
        
        recommendations = base_recommendations.get(risk_level, [])
        return f"Riesgo {risk_level}: " + "; ".join(recommendations)

# Instancia global del gestor
ml_manager = MLModelManager()
