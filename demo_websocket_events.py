#!/usr/bin/env python3
"""
Script de ejemplo para probar el sistema de eventos WebSocket
Simula operaciones CRUD que generan eventos en tiempo real
"""
import asyncio
import requests
import json
import time
from typing import Dict, Any

# Configuración del servidor
SERVER_URL = "http://localhost:8000"
API_BASE = f"{SERVER_URL}/api/v1"

class WebSocketEventDemo:
    """Clase para demostrar eventos WebSocket mediante operaciones CRUD"""
    
    def __init__(self):
        self.session = requests.Session()
        
    def create_sensor(self, tipo: str, modelo: str) -> Dict[Any, Any]:
        """Crear un sensor y generar evento de creación"""
        data = {
            "tipo": tipo,
            "modelo": modelo
        }
        
        try:
            response = self.session.post(f"{API_BASE}/sensors", json=data)
            response.raise_for_status()
            sensor = response.json()
            print(f"✅ Sensor creado: ID={sensor['id']}, Tipo={sensor['tipo']}, Modelo={sensor['modelo']}")
            return sensor
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creando sensor: {e}")
            return {}
    
    def update_sensor(self, sensor_id: int, tipo: str = None, modelo: str = None) -> Dict[Any, Any]:
        """Actualizar un sensor y generar evento de actualización"""
        data = {}
        if tipo:
            data["tipo"] = tipo
        if modelo:
            data["modelo"] = modelo
            
        if not data:
            return {}
        
        try:
            response = self.session.put(f"{API_BASE}/sensors/{sensor_id}", json=data)
            response.raise_for_status()
            sensor = response.json()
            print(f"📝 Sensor actualizado: ID={sensor['id']}, Datos actualizados: {list(data.keys())}")
            return sensor
        except requests.exceptions.RequestException as e:
            print(f"❌ Error actualizando sensor: {e}")
            return {}
    
    def delete_sensor(self, sensor_id: int) -> bool:
        """Eliminar un sensor y generar evento de eliminación"""
        try:
            response = self.session.delete(f"{API_BASE}/sensors/{sensor_id}")
            response.raise_for_status()
            print(f"🗑️ Sensor eliminado: ID={sensor_id}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Error eliminando sensor: {e}")
            return False
    
    def create_reading(self, sensor_id: int, temperatura: float, humedad: float) -> Dict[Any, Any]:
        """Crear una lectura y generar evento de creación"""
        data = {
            "sensor_id": sensor_id,
            "temperatura": temperatura,
            "humedad": humedad
        }
        
        try:
            response = self.session.post(f"{API_BASE}/readings", json=data)
            response.raise_for_status()
            lectura = response.json()
            print(f"📊 Lectura creada: ID={lectura['id']}, Sensor={sensor_id}, T={temperatura}°C, H={humedad}%")
            return lectura
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creando lectura: {e}")
            return {}
    
    def send_test_event(self, channel: str = "general", message: str = "Evento de prueba") -> bool:
        """Enviar evento de prueba directo"""
        try:
            response = self.session.post(
                f"{API_BASE}/ws/test-event",
                params={"channel": channel, "message": message}
            )
            response.raise_for_status()
            result = response.json()
            print(f"📢 {result['message']}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Error enviando evento de prueba: {e}")
            return False
    
    def get_websocket_stats(self) -> Dict[Any, Any]:
        """Obtener estadísticas de conexiones WebSocket"""
        try:
            response = self.session.get(f"{API_BASE}/ws/stats")
            response.raise_for_status()
            stats = response.json()
            print(f"📈 Estadísticas WebSocket: {json.dumps(stats, indent=2)}")
            return stats
        except requests.exceptions.RequestException as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}

async def demo_scenario_1():
    """Escenario 1: Operaciones básicas con sensores"""
    print("\n🎬 ESCENARIO 1: Operaciones básicas con sensores")
    print("=" * 60)
    
    demo = WebSocketEventDemo()
    
    # Crear varios sensores
    print("\n1. Creando sensores...")
    sensor1 = demo.create_sensor("temperatura", "DHT22")
    await asyncio.sleep(1)
    
    sensor2 = demo.create_sensor("humedad", "SHT30")
    await asyncio.sleep(1)
    
    sensor3 = demo.create_sensor("presión", "BMP280")
    await asyncio.sleep(2)
    
    # Actualizar sensores
    print("\n2. Actualizando sensores...")
    if sensor1:
        demo.update_sensor(sensor1["id"], modelo="DHT22-Pro")
        await asyncio.sleep(1)
    
    if sensor2:
        demo.update_sensor(sensor2["id"], tipo="temperatura-humedad", modelo="SHT35")
        await asyncio.sleep(2)
    
    # Eliminar un sensor
    print("\n3. Eliminando sensor...")
    if sensor3:
        demo.delete_sensor(sensor3["id"])
        await asyncio.sleep(1)
    
    return [s for s in [sensor1, sensor2] if s]

async def demo_scenario_2(sensors):
    """Escenario 2: Generación de lecturas"""
    print("\n🎬 ESCENARIO 2: Generación de lecturas")
    print("=" * 60)
    
    demo = WebSocketEventDemo()
    
    if not sensors:
        print("⚠️ No hay sensores disponibles para generar lecturas")
        return
    
    print("\n1. Generando lecturas simuladas...")
    for i in range(5):
        for sensor in sensors:
            # Simular valores de temperatura y humedad
            temperatura = 20 + i * 2 + (i % 2) * 0.5
            humedad = 45 + i * 3 + (i % 3) * 2
            
            demo.create_reading(sensor["id"], temperatura, humedad)
            await asyncio.sleep(0.5)
        
        print(f"   Lote {i+1}/5 completado")
        await asyncio.sleep(1)

async def demo_scenario_3():
    """Escenario 3: Eventos del sistema"""
    print("\n🎬 ESCENARIO 3: Eventos del sistema")
    print("=" * 60)
    
    demo = WebSocketEventDemo()
    
    # Enviar eventos a diferentes canales
    channels = ["general", "sensors", "readings", "anomalies"]
    
    print("\n1. Enviando eventos a diferentes canales...")
    for i, channel in enumerate(channels):
        message = f"Evento de prueba #{i+1} para canal {channel}"
        demo.send_test_event(channel, message)
        await asyncio.sleep(1)
    
    # Obtener estadísticas
    print("\n2. Obteniendo estadísticas de WebSocket...")
    demo.get_websocket_stats()

async def main():
    """Función principal del demo"""
    print("🚀 DEMO DE EVENTOS WEBSOCKET - SISTEMA DE SENSORES")
    print("=" * 60)
    print("Asegúrate de que:")
    print("1. El servidor esté ejecutándose en http://localhost:8000")
    print("2. Tengas el cliente WebSocket abierto en websocket_client.html")
    print("3. Estés conectado a los canales relevantes")
    print("\nPresiona Enter para continuar...")
    input()
    
    try:
        # Ejecutar escenarios secuencialmente
        sensors = await demo_scenario_1()
        await asyncio.sleep(2)
        
        await demo_scenario_2(sensors)
        await asyncio.sleep(2)
        
        await demo_scenario_3()
        
        print("\n🎉 Demo completado! Revisa los eventos en el cliente WebSocket.")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante el demo: {e}")

if __name__ == "__main__":
    print("Iniciando demo en 3 segundos...")
    time.sleep(3)
    asyncio.run(main())
