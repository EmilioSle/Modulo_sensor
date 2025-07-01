"""
Pruebas para predicciones de sequía
"""

def test_create_prediccion(client, auth_headers):
    """Test crear una predicción"""
    # Crear sensor y ubicación primero
    sensor_data = {"tipo": "meteorológico", "modelo": "METEO-1000"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    ubicacion_data = {
        "sensor_id": sensor_id,
        "latitud": "4.598889",
        "longitud": "-74.075833",
        "descripcion": "Sabana de Bogotá"
    }
    ubicacion_response = client.post("/api/v1/ubicaciones/", json=ubicacion_data, headers=auth_headers)
    ubicacion_id = ubicacion_response.json()["id"]
    
    # Crear predicción
    prediccion_data = {
        "ubicacion_id": ubicacion_id,
        "probabilidad": 0.75,
        "comentario": "Predicción de prueba para área de Bogotá"
    }
    
    response = client.post("/api/v1/predicciones/", json=prediccion_data, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["ubicacion_id"] == ubicacion_id
    assert data["probabilidad"] == 0.75
    assert "Bogotá" in data["comentario"]

def test_generate_prediction_with_ml(client, auth_headers):
    """Test generar predicción con ML/lógica heurística"""
    # Crear sensor y ubicación
    sensor_data = {"tipo": "agroclimático", "modelo": "AGRO-2000"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    ubicacion_data = {
        "sensor_id": sensor_id,
        "latitud": "6.244203",
        "longitud": "-75.581212",
        "descripcion": "Valle de Aburrá"
    }
    ubicacion_response = client.post("/api/v1/ubicaciones/", json=ubicacion_data, headers=auth_headers)
    ubicacion_id = ubicacion_response.json()["id"]
    
    # Generar predicción automática
    response = client.post(
        f"/api/v1/predicciones/generate?ubicacion_id={ubicacion_id}&temperatura_promedio=32.5&humedad_promedio=25.0&comentario=Prueba automática",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["ubicacion_id"] == ubicacion_id
    assert 0.0 <= data["probabilidad"] <= 1.0
    assert "automática" in data["comentario"]

def test_get_high_risk_predictions(client, auth_headers):
    """Test obtener predicciones de alto riesgo"""
    # Crear datos de prueba
    sensor_data = {"tipo": "riesgo", "modelo": "RISK-1"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    ubicacion_data = {
        "sensor_id": sensor_id,
        "latitud": "10.000000",
        "longitud": "-73.000000",
        "descripcion": "Zona de alto riesgo"
    }
    ubicacion_response = client.post("/api/v1/ubicaciones/", json=ubicacion_data, headers=auth_headers)
    ubicacion_id = ubicacion_response.json()["id"]
    
    # Crear predicción de alto riesgo
    prediccion_data = {
        "ubicacion_id": ubicacion_id,
        "probabilidad": 0.85,
        "comentario": "Alto riesgo de sequía"
    }
    client.post("/api/v1/predicciones/", json=prediccion_data, headers=auth_headers)
    
    # Obtener predicciones de alto riesgo
    response = client.get("/api/v1/predicciones/high-risk?threshold=0.8", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) >= 1
    assert all(pred["probabilidad"] >= 0.8 for pred in data)

def test_get_latest_prediction_by_location(client, auth_headers):
    """Test obtener última predicción por ubicación"""
    # Crear datos de prueba
    sensor_data = {"tipo": "histórico", "modelo": "HIST-1"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    ubicacion_data = {
        "sensor_id": sensor_id,
        "latitud": "8.000000",
        "longitud": "-72.000000",
        "descripcion": "Campo histórico"
    }
    ubicacion_response = client.post("/api/v1/ubicaciones/", json=ubicacion_data, headers=auth_headers)
    ubicacion_id = ubicacion_response.json()["id"]
    
    # Crear varias predicciones
    for i in range(3):
        prediccion_data = {
            "ubicacion_id": ubicacion_id,
            "probabilidad": 0.3 + (i * 0.1),
            "comentario": f"Predicción histórica {i+1}"
        }
        client.post("/api/v1/predicciones/", json=prediccion_data, headers=auth_headers)
    
    # Obtener la más reciente
    response = client.get(f"/api/v1/predicciones/ubicacion/{ubicacion_id}/latest", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    assert data["ubicacion_id"] == ubicacion_id
    # La más reciente debería ser la última creada
    assert "3" in data["comentario"]

def test_prediction_statistics(client, auth_headers):
    """Test estadísticas de predicciones"""
    # Obtener estadísticas
    response = client.get("/api/v1/predicciones/statistics", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    assert "total" in data
    assert "probabilidad_promedio" in data
    assert "alto_riesgo" in data
    assert "bajo_riesgo" in data
    
    # Verificar que los números sean consistentes
    total = data["total"]
    alto = data["alto_riesgo"]
    medio = data.get("medio_riesgo", 0)
    bajo = data["bajo_riesgo"]
    
    assert alto + medio + bajo == total
