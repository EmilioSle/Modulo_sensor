"""
Pruebas para anomalías
"""

def test_create_anomalia(client, auth_headers):
    """Test crear una anomalía"""
    # Crear sensor y lectura primero
    sensor_data = {"tipo": "temperatura", "modelo": "TEMP-1000"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    lectura_data = {
        "sensor_id": sensor_id,
        "humedad": 20.0,
        "temperatura": 45.0  # Temperatura alta
    }
    lectura_response = client.post("/api/v1/lecturas/", json=lectura_data, headers=auth_headers)
    lectura_id = lectura_response.json()["id"]
    
    # Crear anomalía
    anomalia_data = {
        "lectura_id": lectura_id,
        "tipo": "temperatura_alta",
        "valor": 45.0
    }
    
    response = client.post("/api/v1/anomalias/", json=anomalia_data, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["lectura_id"] == lectura_id
    assert data["tipo"] == "temperatura_alta"
    assert data["valor"] == 45.0

def test_detect_anomalies_in_reading(client, auth_headers):
    """Test detección automática de anomalías"""
    # Crear sensor y lectura con valores anómalos
    sensor_data = {"tipo": "multisensor", "modelo": "MULTI-2000"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    lectura_data = {
        "sensor_id": sensor_id,
        "humedad": 5.0,    # Humedad muy baja
        "temperatura": 40.0  # Temperatura muy alta
    }
    lectura_response = client.post("/api/v1/lecturas/", json=lectura_data, headers=auth_headers)
    lectura_id = lectura_response.json()["id"]
    
    # Detectar anomalías automáticamente
    response = client.post(f"/api/v1/anomalias/detect/{lectura_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    # Debería detectar al menos 2 anomalías
    assert len(data) >= 2
    tipos = [anomalia["tipo"] for anomalia in data]
    assert "temperatura_alta" in tipos
    assert "humedad_baja" in tipos

def test_get_anomalias_by_tipo(client, auth_headers):
    """Test obtener anomalías por tipo"""
    # Crear datos de prueba
    sensor_data = {"tipo": "humedad", "modelo": "HUM-3000"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    lectura_data = {
        "sensor_id": sensor_id,
        "humedad": 95.0,
        "temperatura": 25.0
    }
    lectura_response = client.post("/api/v1/lecturas/", json=lectura_data, headers=auth_headers)
    lectura_id = lectura_response.json()["id"]
    
    anomalia_data = {
        "lectura_id": lectura_id,
        "tipo": "humedad_alta",
        "valor": 95.0
    }
    client.post("/api/v1/anomalias/", json=anomalia_data, headers=auth_headers)
    
    # Obtener anomalías por tipo
    response = client.get("/api/v1/anomalias/tipo/humedad_alta", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(anomalia["tipo"] == "humedad_alta" for anomalia in data)

def test_anomaly_statistics(client, auth_headers):
    """Test estadísticas de anomalías"""
    # Crear algunas anomalías de prueba
    sensor_data = {"tipo": "estadisticas", "modelo": "STATS-1"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    # Crear lecturas y anomalías
    for i in range(3):
        lectura_data = {
            "sensor_id": sensor_id,
            "humedad": 50.0 + i * 10,
            "temperatura": 20.0 + i * 5
        }
        lectura_response = client.post("/api/v1/lecturas/", json=lectura_data, headers=auth_headers)
        lectura_id = lectura_response.json()["id"]
        
        anomalia_data = {
            "lectura_id": lectura_id,
            "tipo": "temperatura_alta" if i % 2 == 0 else "humedad_alta",
            "valor": 30.0 + i * 10
        }
        client.post("/api/v1/anomalias/", json=anomalia_data, headers=auth_headers)
    
    # Obtener estadísticas
    response = client.get("/api/v1/anomalias/statistics", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    assert "total" in data
    assert "por_tipo" in data
    assert data["total"] >= 3
