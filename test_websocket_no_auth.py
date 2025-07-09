"""
Script para probar el endpoint de sensores sin autenticación
"""
import asyncio
import json
import websockets
import requests
import time
from threading import Thread

# Configuraciones
BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/api/v1/ws?channel=sensors"

class WebSocketListener:
    def __init__(self):
        self.events = []
    
    async def listen(self):
        """Escucha eventos del WebSocket"""
        try:
            async with websockets.connect(WS_URL) as websocket:
                print("📡 Conectado al WebSocket")
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        print(f"🔔 Evento recibido: {data}")
                        self.events.append(data)
                    except json.JSONDecodeError:
                        print(f"📝 Mensaje: {message}")
        except Exception as e:
            print(f"❌ Error en WebSocket: {e}")

def test_crud_operations():
    """Prueba las operaciones CRUD"""
    print("🚀 Iniciando pruebas CRUD sin autenticación...")
    
    # 1. Crear un sensor
    print("\n📝 Creando sensor...")
    sensor_data = {
        "nombre": "Sensor de Prueba",
        "tipo": "temperatura",
        "modelo": "DHT22",  # Campo requerido
        "descripcion": "Sensor para pruebas WebSocket",
        "activo": True,
        "ubicacion_id": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/test-sensors/", json=sensor_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            sensor = response.json()
            print(f"✅ Sensor creado: {sensor}")
            sensor_id = sensor['id']
            
            # Esperar un momento para que se procese el evento
            time.sleep(1)
            
            # 2. Actualizar el sensor
            print("\n🔄 Actualizando sensor...")
            update_data = {
                "modelo": "DHT22-Updated"  # Cambiar el modelo para asegurar que se actualice
            }
            response = requests.put(f"{BASE_URL}/api/v1/test-sensors/{sensor_id}", json=update_data)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                updated_sensor = response.json()
                print(f"✅ Sensor actualizado: {updated_sensor}")
            else:
                print(f"❌ Error actualizando: {response.text}")
            
            # 3. Eliminar el sensor
            print("\n🗑️ Eliminando sensor...")
            response = requests.delete(f"{BASE_URL}/api/v1/test-sensors/{sensor_id}")
            print(f"Status: {response.status_code}")
            if response.status_code == 204:
                print("✅ Sensor eliminado correctamente")
            
        else:
            print(f"❌ Error creando sensor: {response.text}")
    except Exception as e:
        print(f"❌ Error en petición: {e}")

async def main():
    """Función principal"""
    # Crear listener
    listener = WebSocketListener()
    
    # Iniciar WebSocket en un task separado
    websocket_task = asyncio.create_task(listener.listen())
    
    # Esperar un poco para que se conecte
    await asyncio.sleep(2)
    
    # Ejecutar operaciones CRUD en un hilo separado
    crud_thread = Thread(target=test_crud_operations)
    crud_thread.daemon = True
    crud_thread.start()
    
    # Esperar a que terminen las operaciones
    crud_thread.join()
    
    # Esperar un poco más para recibir todos los eventos
    await asyncio.sleep(3)
    
    # Cancelar el websocket task
    websocket_task.cancel()
    
    print(f"\n📊 Total de eventos recibidos: {len(listener.events)}")
    for i, event in enumerate(listener.events):
        print(f"Evento {i+1}: {event}")

if __name__ == "__main__":
    print("🧪 Prueba de WebSocket con endpoints sin autenticación")
    print("📋 Asegúrate de que el servidor esté ejecutándose en localhost:8000")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Prueba interrumpida")
    except Exception as e:
        print(f"❌ Error: {e}")
