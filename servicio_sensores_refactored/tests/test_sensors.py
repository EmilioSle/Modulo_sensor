"""
Pruebas para sensores
"""
from schemas.sensor import SensorCreate

def test_create_sensor(client, auth_headers):
    """Test crear un sensor"""
    sensor_data = {
        "tipo": "temperatura",
        "modelo": "T-1000"
    }
    
    response = client.post(
        "/api/v1/sensores/", 
        json=sensor_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["tipo"] == sensor_data["tipo"]
    assert data["modelo"] == sensor_data["modelo"]
    assert "id" in data

def test_get_sensors(client, auth_headers):
    """Test obtener lista de sensores"""
    # Crear un sensor primero
    sensor_data = {
        "tipo": "humedad", 
        "modelo": "H-2000"
    }
    client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    
    # Obtener lista
    response = client.get("/api/v1/sensores/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_sensor_by_id(client, auth_headers):
    """Test obtener sensor por ID"""
    # Crear sensor
    sensor_data = {"tipo": "presion", "modelo": "P-3000"}
    create_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = create_response.json()["id"]
    
    # Obtener por ID
    response = client.get(f"/api/v1/sensores/{sensor_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sensor_id
    assert data["tipo"] == sensor_data["tipo"]

def test_update_sensor(client, auth_headers):
    """Test actualizar sensor"""
    # Crear sensor
    sensor_data = {"tipo": "luz", "modelo": "L-4000"}
    create_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = create_response.json()["id"]
    
    # Actualizar
    update_data = {"modelo": "L-5000"}
    response = client.put(f"/api/v1/sensores/{sensor_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["modelo"] == "L-5000"
    assert data["tipo"] == "luz"  # No debería cambiar

def test_delete_sensor(client, auth_headers):
    """Test eliminar sensor"""
    # Crear sensor
    sensor_data = {"tipo": "sonido", "modelo": "S-6000"}
    create_response = client.post("/api/v1/sensores/", json=sensor_data, headers=auth_headers)
    sensor_id = create_response.json()["id"]
    
    # Eliminar
    response = client.delete(f"/api/v1/sensores/{sensor_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verificar que no existe
    get_response = client.get(f"/api/v1/sensores/{sensor_id}", headers=auth_headers)
    assert get_response.status_code == 404
