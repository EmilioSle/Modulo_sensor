#!/usr/bin/env python3
"""
Script para generar eventos de ejemplo y probar el sistema de WebSocket
"""
import asyncio
import httpx
import random
import json
from datetime import datetime, timedelta
import time

# URL base de la API
BASE_URL = "http://localhost:8000"

class EventTester:
    """Generador de eventos de prueba para el sistema WebSocket"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
        
    async def close(self):
        """Cerrar cliente HTTP"""
        await self.client.aclose()
    
    async def create_test_sensor(self) -> dict:
        """Crear un sensor de prueba"""
        sensor_data = {
            "tipo": random.choice(["temperatura", "humedad", "presion", "luz", "movimiento"]),
            "modelo": f"Sensor-{random.randint(1000, 9999)}"
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/sensors",
                json=sensor_data
            )
            if response.status_code == 201:
                sensor = response.json()
                print(f"✅ Sensor creado: ID {sensor['id']}, Tipo: {sensor['tipo']}, Modelo: {sensor['modelo']}")
                return sensor
            else:
                print(f"❌ Error creando sensor: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error de conexión creando sensor: {e}")
            return None
    
    async def create_test_reading(self, sensor_id: int) -> dict:
        """Crear una lectura de prueba para un sensor"""
        reading_data = {
            "sensor_id": sensor_id,
            "temperatura": round(random.uniform(15.0, 35.0), 2),
            "humedad": round(random.uniform(30.0, 90.0), 2),
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/readings",
                json=reading_data
            )
            if response.status_code == 201:
                reading = response.json()
                print(f"📊 Lectura creada: ID {reading['id']}, Sensor: {sensor_id}, Temp: {reading['temperatura']}°C, Humedad: {reading['humedad']}%")
                return reading
            else:
                print(f"❌ Error creando lectura: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error de conexión creando lectura: {e}")
            return None
    
    async def update_test_sensor(self, sensor_id: int) -> dict:
        """Actualizar un sensor existente"""
        update_data = {
            "modelo": f"Sensor-Updated-{random.randint(1000, 9999)}"
        }
        
        try:
            response = await self.client.put(
                f"{self.base_url}/api/v1/sensors/{sensor_id}",
                json=update_data
            )
            if response.status_code == 200:
                sensor = response.json()
                print(f"🔄 Sensor actualizado: ID {sensor['id']}, Nuevo modelo: {sensor['modelo']}")
                return sensor
            else:
                print(f"❌ Error actualizando sensor: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error de conexión actualizando sensor: {e}")
            return None
    
    async def delete_test_sensor(self, sensor_id: int) -> bool:
        """Eliminar un sensor"""
        try:
            response = await self.client.delete(f"{self.base_url}/api/v1/sensors/{sensor_id}")
            if response.status_code == 204:
                print(f"🗑️  Sensor eliminado: ID {sensor_id}")
                return True
            else:
                print(f"❌ Error eliminando sensor: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error de conexión eliminando sensor: {e}")
            return False
    
    async def send_test_websocket_event(self, channel: str = "general", message: str = "Evento de prueba") -> bool:
        """Enviar evento de prueba a través del endpoint HTTP"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/ws/test-event",
                params={"channel": channel, "message": message}
            )
            if response.status_code == 200:
                print(f"📡 Evento enviado al canal '{channel}': {message}")
                return True
            else:
                print(f"❌ Error enviando evento: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error de conexión enviando evento: {e}")
            return False
    
    async def get_websocket_stats(self) -> dict:
        """Obtener estadísticas de WebSocket"""
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/ws/stats")
            if response.status_code == 200:
                stats = response.json()
                print(f"📊 Estadísticas WebSocket: {json.dumps(stats, indent=2, ensure_ascii=False)}")
                return stats
            else:
                print(f"❌ Error obteniendo estadísticas: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Error de conexión obteniendo estadísticas: {e}")
            return {}
    
    async def run_continuous_test(self, duration_minutes: int = 5, interval_seconds: int = 10):
        """Ejecutar pruebas continuas por un período determinado"""
        print(f"🚀 Iniciando pruebas continuas por {duration_minutes} minutos...")
        print(f"⏰ Generando eventos cada {interval_seconds} segundos")
        print("=" * 50)
        
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        sensor_ids = []
        
        try:
            while datetime.now() < end_time:
                print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Generando eventos...")
                
                # Decidir qué tipo de evento generar
                action = random.choice(["create_sensor", "create_reading", "update_sensor", "test_event"])
                
                if action == "create_sensor":
                    sensor = await self.create_test_sensor()
                    if sensor:
                        sensor_ids.append(sensor['id'])
                
                elif action == "create_reading" and sensor_ids:
                    sensor_id = random.choice(sensor_ids)
                    await self.create_test_reading(sensor_id)
                
                elif action == "update_sensor" and sensor_ids:
                    sensor_id = random.choice(sensor_ids)
                    await self.update_test_sensor(sensor_id)
                
                elif action == "test_event":
                    channel = random.choice(["general", "sensors", "readings", "anomalies"])
                    message = f"Evento de prueba automático - {datetime.now().strftime('%H:%M:%S')}"
                    await self.send_test_websocket_event(channel, message)
                
                # Esperar antes del siguiente evento
                await asyncio.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n⛔ Prueba interrumpida por el usuario")
        
        finally:
            # Limpiar sensores creados durante la prueba
            print("\n🧹 Limpiando sensores de prueba...")
            for sensor_id in sensor_ids:
                await self.delete_test_sensor(sensor_id)
            
            print("\n📊 Estadísticas finales:")
            await self.get_websocket_stats()
    
    async def run_single_test(self):
        """Ejecutar una prueba única de todos los tipos de eventos"""
        print("🎯 Ejecutando prueba única de eventos...")
        print("=" * 50)
        
        # 1. Crear un sensor
        sensor = await self.create_test_sensor()
        if not sensor:
            return
        
        sensor_id = sensor['id']
        
        # 2. Crear algunas lecturas
        print("\n📊 Creando lecturas...")
        for i in range(3):
            await self.create_test_reading(sensor_id)
            await asyncio.sleep(1)
        
        # 3. Actualizar el sensor
        print("\n🔄 Actualizando sensor...")
        await self.update_test_sensor(sensor_id)
        
        # 4. Enviar eventos de prueba a diferentes canales
        print("\n📡 Enviando eventos de prueba...")
        channels = ["general", "sensors", "readings", "anomalies", "predictions"]
        for channel in channels:
            await self.send_test_websocket_event(channel, f"Prueba en canal {channel}")
            await asyncio.sleep(1)
        
        # 5. Obtener estadísticas
        print("\n📊 Obteniendo estadísticas...")
        await self.get_websocket_stats()
        
        # 6. Eliminar el sensor
        print("\n🗑️  Eliminando sensor de prueba...")
        await self.delete_test_sensor(sensor_id)
        
        print("\n✅ Prueba única completada!")

async def main():
    """Función principal"""
    tester = EventTester()
    
    try:
        print("🔧 WebSocket Event Tester")
        print("=" * 50)
        print("Opciones disponibles:")
        print("1. Ejecutar prueba única")
        print("2. Ejecutar pruebas continuas (5 minutos)")
        print("3. Ejecutar pruebas continuas personalizadas")
        print("4. Solo enviar evento de prueba")
        print("5. Ver estadísticas de WebSocket")
        
        choice = input("\nSelecciona una opción (1-5): ").strip()
        
        if choice == "1":
            await tester.run_single_test()
        
        elif choice == "2":
            await tester.run_continuous_test(duration_minutes=5, interval_seconds=10)
        
        elif choice == "3":
            duration = int(input("Duración en minutos: "))
            interval = int(input("Intervalo entre eventos en segundos: "))
            await tester.run_continuous_test(duration_minutes=duration, interval_seconds=interval)
        
        elif choice == "4":
            channel = input("Canal (general/sensors/readings/anomalies/predictions): ") or "general"
            message = input("Mensaje: ") or "Evento de prueba manual"
            await tester.send_test_websocket_event(channel, message)
        
        elif choice == "5":
            await tester.get_websocket_stats()
        
        else:
            print("❌ Opción no válida")
    
    except KeyboardInterrupt:
        print("\n⛔ Programa interrumpido")
    
    finally:
        await tester.close()

if __name__ == "__main__":
    asyncio.run(main())
