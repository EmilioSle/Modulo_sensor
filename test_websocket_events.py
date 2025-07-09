#!/usr/bin/env python3
"""
Script de prueba para WebSocket de todas las entidades
"""
import asyncio
import websockets
import json
import requests
from datetime import datetime

async def test_websocket_events():
    """Probar eventos de WebSocket para todas las entidades"""
    
    # URLs para pruebas
    base_url = "http://localhost:8000/api/v1"
    websocket_url = "ws://localhost:8000/api/v1/ws"
    
    print("🚀 Iniciando prueba de WebSocket Events...")
    
    try:
        # Conectarse al WebSocket en el canal general
        async with websockets.connect(f"{websocket_url}?channel=general") as websocket:
            print("✅ Conectado al WebSocket en canal 'general'")
            
            # Función para escuchar eventos
            async def listen_events():
                try:
                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        
                        if data.get('type') == 'entity_event':
                            entity_type = data.get('entity_type', 'unknown')
                            event_type = data.get('event_type', 'unknown')
                            entity_id = data.get('entity_id', 'N/A')
                            print(f"📨 [{timestamp}] {entity_type.upper()} {event_type.upper()} (ID: {entity_id})")
                            print(f"    Datos: {json.dumps(data.get('data', {}), indent=2)}")
                        elif data.get('type') == 'system_event':
                            level = data.get('level', 'info')
                            message = data.get('message', '')
                            print(f"🔧 [{timestamp}] SYSTEM [{level.upper()}]: {message}")
                        else:
                            print(f"❓ [{timestamp}] Evento desconocido: {data}")
                        print("-" * 50)
                        
                except websockets.exceptions.ConnectionClosed:
                    print("❌ Conexión WebSocket cerrada")
                except Exception as e:
                    print(f"❌ Error escuchando eventos: {e}")
            
            # Iniciar la escucha de eventos en background
            listen_task = asyncio.create_task(listen_events())
            
            # Esperar un poco para que se establezca la conexión
            await asyncio.sleep(1)
            
            print("🧪 Iniciando pruebas de CRUD...")
            
            # 1. Probar sensores
            print("\n1️⃣ Probando SENSORES:")
            sensor_data = {
                "tipo": "humedad",
                "modelo": "SHT30-WebSocket-Test",
                "descripcion": "Sensor de prueba para WebSocket events",
                "activo": True
            }
            response = requests.post(f"{base_url}/test-sensors/", json=sensor_data)
            if response.status_code == 201:
                sensor_created = response.json()
                sensor_id = sensor_created['id']
                print(f"✅ Sensor creado: ID {sensor_id}")
                await asyncio.sleep(1)  # Esperar evento
                
                # Actualizar sensor
                update_data = {"descripcion": "Sensor actualizado via WebSocket"}
                response = requests.put(f"{base_url}/test-sensors/{sensor_id}", json=update_data)
                if response.status_code == 200:
                    print(f"✅ Sensor {sensor_id} actualizado")
                    await asyncio.sleep(1)
            else:
                print(f"❌ Error creando sensor: {response.status_code} - {response.text}")
            
            # 2. Probar ubicaciones
            print("\n2️⃣ Probando UBICACIONES:")
            if 'sensor_id' in locals():
                ubicacion_data = {
                    "sensor_id": sensor_id,
                    "latitud": "-12.0465000",
                    "longitud": "-77.0429000",
                    "descripcion": "Lima, Perú - Prueba WebSocket"
                }
                response = requests.post(f"{base_url}/test-ubicaciones/", json=ubicacion_data)
                if response.status_code == 201:
                    ubicacion_created = response.json()
                    ubicacion_id = ubicacion_created['id']
                    print(f"✅ Ubicación creada: ID {ubicacion_id}")
                    await asyncio.sleep(1)
                    
                    # Actualizar ubicación
                    ubicacion_update = {
                        "descripcion": "Lima, Perú - Actualizada WebSocket"
                    }
                    response = requests.put(f"{base_url}/test-ubicaciones/{ubicacion_id}", json=ubicacion_update)
                    if response.status_code == 200:
                        print(f"✅ Ubicación actualizada: ID {ubicacion_id}")
                        await asyncio.sleep(1)
                else:
                    print(f"❌ Error creando ubicación: {response.status_code} - {response.text}")
                    
            # 3. Probar lecturas
            print("\n3️⃣ Probando LECTURAS:")
            if 'sensor_id' in locals():
                lectura_data = {
                    "sensor_id": sensor_id,
                    "temperatura": 25.5,
                    "humedad": 60.0
                }
                response = requests.post(f"{base_url}/test-lecturas/", json=lectura_data)
                if response.status_code == 201:
                    lectura_created = response.json()
                    lectura_id = lectura_created['id']
                    print(f"✅ Lectura creada: ID {lectura_id}")
                    await asyncio.sleep(1)
                    
                    # Actualizar lectura
                    lectura_update = {
                        "temperatura": 28.0,
                        "humedad": 65.0
                    }
                    response = requests.put(f"{base_url}/test-lecturas/{lectura_id}", json=lectura_update)
                    if response.status_code == 200:
                        print(f"✅ Lectura actualizada: ID {lectura_id}")
                        await asyncio.sleep(1)
                else:
                    print(f"❌ Error creando lectura: {response.status_code} - {response.text}")
            
            # Esperar un poco más para ver todos los eventos
            print("\n⏳ Esperando eventos finales...")
            await asyncio.sleep(3)
            
            # Cancelar la tarea de escucha
            listen_task.cancel()
            
    except Exception as e:
        print(f"❌ Error general: {e}")
    
    print("\n🏁 Prueba completada!")

if __name__ == "__main__":
    asyncio.run(test_websocket_events())
