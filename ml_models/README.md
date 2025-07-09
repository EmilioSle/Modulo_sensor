# Este directorio contiene los modelos de Machine Learning
# 
# Archivos esperados:
# - modelo_sequia.pkl: Modelo entrenado para predicción de sequías
#
# Para entrenar un modelo nuevo:
# 1. Recopilar datos históricos de sensores
# 2. Preparar dataset con features (temperatura, humedad, etc.)
# 3. Entrenar modelo (RandomForest, SVM, etc.)
# 4. Guardar modelo serializado con pickle
#
# Ejemplo de uso desde el servicio:
# prediccion_service.generate_prediction_with_ml(db, ubicacion_id, temp, hum)
