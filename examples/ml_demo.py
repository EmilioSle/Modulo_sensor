"""
Ejemplo de uso del módulo ML para predicción de sequías
"""
import sys
import os
# Agregar el directorio padre al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.ml_utils import ml_manager

def demonstrate_ml_predictions():
    """Demostrar el funcionamiento del módulo ML"""
    print("=== Demostración del Módulo ML de Predicción de Sequías ===\n")
    
    # Casos de prueba
    test_cases = [
        {"temp": 35.0, "humidity": 20.0, "description": "Condiciones muy secas"},
        {"temp": 28.0, "humidity": 45.0, "description": "Condiciones moderadas"},
        {"temp": 22.0, "humidity": 70.0, "description": "Condiciones húmedas"},
        {"temp": 40.0, "humidity": 15.0, "description": "Condiciones extremas"},
        {"temp": 18.0, "humidity": 85.0, "description": "Condiciones muy húmedas"}
    ]
    
    print("Predicciones usando lógica heurística:\n")
    print("| Temp | Humedad | Probabilidad | Riesgo | Descripción")
    print("|------|---------|--------------|--------|-------------")
    
    for case in test_cases:
        prob = ml_manager.predict_drought_probability(case["temp"], case["humidity"])
        risk = ml_manager.analyze_risk_level(prob)
        print(f"| {case['temp']:4.1f}°C | {case['humidity']:6.1f}% | {prob:10.3f} | {risk:6s} | {case['description']}")
    
    print("\n" + "="*70)
    print("Recomendaciones por nivel de riesgo:\n")
    
    # Generar recomendaciones para cada nivel
    for prob, level in [(0.85, "ALTO"), (0.55, "MEDIO"), (0.25, "BAJO")]:
        recommendations = ml_manager.get_recommendations(prob, "Zona de prueba")
        print(f"🔴 Riesgo {level} ({prob:.0%}):")
        print(f"   {recommendations}")
        print()
    
    print("="*70)
    print("Información del modelo ML:\n")
    
    # Verificar disponibilidad del modelo
    model = ml_manager.get_model("modelo_sequia")
    if model:
        print("✅ Modelo ML 'modelo_sequia.pkl' encontrado y cargado")
        print(f"   Tipo: {type(model)}")
    else:
        print("⚠️  Modelo ML no encontrado, usando lógica heurística")
        print("   Para usar ML real:")
        print("   1. Entrenar un modelo scikit-learn")
        print("   2. Guardar como 'ml_models/modelo_sequia.pkl'")
        print("   3. El modelo debe tener método predict_proba()")
    
    print("\n" + "="*70)
    print("Ejemplo de integración con API:\n")
    
    print("""
# Endpoint para generar predicción automática:
POST /api/v1/predicciones/generate?ubicacion_id=1&temperatura_promedio=32.5&humedad_promedio=25.0

# Respuesta esperada:
{
    "id": 123,
    "ubicacion_id": 1,
    "probabilidad": 0.742,
    "comentario": "Predicción automática: T=32.5°C, H=25.0% | Riesgo: ALTO | Prob: 74.2% | Riesgo ALTO: Implementar sistemas de riego de emergencia; Reducir el consumo de agua no esencial; ...",
    "fecha_prediccion": "2024-01-15T10:30:00"
}
    """)

if __name__ == "__main__":
    demonstrate_ml_predictions()
