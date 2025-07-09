"""
Pruebas para ubicaciones
"""

def test_create_ubicacion(client, auth_headers):
    """Test crear una ubicación"""
    # Primero crear un sensor
    sensor_data = {"tipo": "gps", "modelo": "GPS-1000"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    # Crear ubicación
    ubicacion_data = {
        "sensor_id": sensor_id,
        "latitud": "10.123456",
        "longitud": "-70.987654",
        "descripcion": "Campo de prueba"
    }
    
    response = client.post("/api/v1/ubicaciones/", json=ubicacion_data, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["sensor_id"] == sensor_id
    assert data["latitud"] == "10.123456"
    assert data["descripcion"] == "Campo de prueba"

def test_get_ubicaciones_by_sensor(client, auth_headers):
    """Test obtener ubicaciones por sensor"""
    # Crear sensor y ubicación
    sensor_data = {"tipo": "ambiental", "modelo": "AMB-2000"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    ubicacion_data = {
        "sensor_id": sensor_id,
        "latitud": "5.000000",
        "longitud": "-75.000000",
        "descripcion": "Invernadero 1"
    }
    client.post("/api/v1/ubicaciones/", json=ubicacion_data, headers=auth_headers)
    
    # Obtener ubicaciones del sensor
    response = client.get(f"/api/v1/ubicaciones/sensor/{sensor_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["descripcion"] == "Invernadero 1"

def test_search_ubicaciones(client, auth_headers):
    """Test buscar ubicaciones por descripción"""
    # Crear sensor y ubicación
    sensor_data = {"tipo": "clima", "modelo": "CLIMA-3000"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    ubicacion_data = {
        "sensor_id": sensor_id,
        "latitud": "0.000000",
        "longitud": "-80.000000",
        "descripcion": "Cultivo de maíz experimental"
    }
    client.post("/api/v1/ubicaciones/", json=ubicacion_data, headers=auth_headers)
    
    # Buscar por término
    response = client.get("/api/v1/ubicaciones/search?q=maíz", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "maíz" in data[0]["descripcion"]

def test_invalid_coordinates(client, auth_headers):
    """Test coordenadas inválidas"""
    # Crear sensor
    sensor_data = {"tipo": "test", "modelo": "TEST-1"}
    sensor_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = sensor_response.json()["id"]
    
    # Intentar crear ubicación con coordenadas inválidas
    ubicacion_data = {
        "sensor_id": sensor_id,
        "latitud": "999.999999",  # Latitud inválida
        "longitud": "-70.000000",
        "descripcion": "Ubicación inválida"
    }
    
    response = client.post("/api/v1/ubicaciones/", json=ubicacion_data, headers=auth_headers)
    assert response.status_code == 400
    assert "rango válido" in response.json()["detail"]
