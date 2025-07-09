#!/usr/bin/env python3
"""
Script simple para probar eventos WebSocket sin dependencias externas
"""
import asyncio
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import quote_plus
import time

# Configuración del servidor
SERVER_URL = "http://127.0.0.1:8000"
API_BASE = f"{SERVER_URL}/api/v1"

def send_request(url, method="GET", data=None):
    """Enviar una petición HTTP simple"""
    try:
        if data:
            data = json.dumps(data).encode('utf-8')
            req = Request(url, data=data, method=method)
            req.add_header('Content-Type', 'application/json')
        else:
            req = Request(url, method=method)
        
        with urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except (URLError, HTTPError) as e:
        print(f"❌ Error en petición: {e}")
        return None

def create_sensor(tipo, modelo):
    """Crear un sensor"""
    data = {"tipo": tipo, "modelo": modelo}
    result = send_request(f"{API_BASE}/sensores", "POST", data)
    if result:
        print(f"✅ Sensor creado: ID={result['id']}, Tipo={result['tipo']}, Modelo={result['modelo']}")
    return result

def update_sensor(sensor_id, tipo=None, modelo=None):
    """Actualizar un sensor"""
    data = {}
    if tipo:
        data["tipo"] = tipo
    if modelo:
        data["modelo"] = modelo
    
    if data:
        result = send_request(f"{API_BASE}/sensores/{sensor_id}", "PUT", data)
        if result:
            print(f"📝 Sensor actualizado: ID={result['id']}")
        return result
    return None

def delete_sensor(sensor_id):
    """Eliminar un sensor"""
    result = send_request(f"{API_BASE}/sensores/{sensor_id}", "DELETE")
    if result is not None:
        print(f"🗑️ Sensor eliminado: ID={sensor_id}")
        return True
    return False

def send_test_event(channel="general", message="Evento de prueba"):
    """Enviar evento de prueba"""
    url = f"{API_BASE}/ws/test-event?channel={quote_plus(channel)}&message={quote_plus(message)}"
    result = send_request(url, "POST")
    if result:
        print(f"📢 {result['message']}")
    return result

def get_websocket_stats():
    """Obtener estadísticas WebSocket"""
    result = send_request(f"{API_BASE}/ws/stats")
    if result:
        print(f"📈 Estadísticas WebSocket:")
        print(f"   - Canales totales: {result['total_channels']}")
        for channel, stats in result['channels'].items():
            print(f"   - {channel}: {stats['connections']} conexiones")
    return result

def main():
    """Función principal de prueba"""
    print("🚀 PRUEBA SIMPLE DE EVENTOS WEBSOCKET")
    print("=" * 50)
    print("🔗 Asegúrate de tener el cliente WebSocket abierto en tu navegador")
    print("📱 URL del cliente: file:///home/elpajarowtf/Documentos/PROYECTOS/Modulo_sensor/websocket_client.html")
    print("\nPresiona Enter para continuar...")
    input()

    try:
        # Obtener estadísticas iniciales
        print("\n1. 📊 Estadísticas iniciales:")
        get_websocket_stats()
        time.sleep(1)

        # Enviar evento de prueba
        print("\n2. 📢 Enviando evento de prueba:")
        send_test_event("general", "¡Sistema WebSocket funcionando!")
        time.sleep(2)

        # Crear sensores
        print("\n3. 🔧 Creando sensores:")
        sensor1 = create_sensor("temperatura", "DHT22")
        time.sleep(1)
        
        sensor2 = create_sensor("humedad", "SHT30")
        time.sleep(1)

        # Actualizar sensor
        if sensor1:
            print("\n4. 📝 Actualizando sensor:")
            update_sensor(sensor1["id"], modelo="DHT22-Pro")
            time.sleep(1)

        # Enviar eventos a diferentes canales
        print("\n5. 📡 Enviando eventos a canales específicos:")
        channels = ["sensors", "readings", "anomalies"]
        for i, channel in enumerate(channels):
            send_test_event(channel, f"Evento #{i+1} para {channel}")
            time.sleep(1)

        # Estadísticas finales
        print("\n6. 📊 Estadísticas finales:")
        get_websocket_stats()

        # Limpiar (eliminar sensores creados)
        print("\n7. 🧹 Limpiando datos de prueba:")
        if sensor1:
            delete_sensor(sensor1["id"])
        if sensor2:
            delete_sensor(sensor2["id"])

        print("\n✅ ¡Prueba completada! Revisa los eventos en el cliente WebSocket.")

    except KeyboardInterrupt:
        print("\n⏹️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")

if __name__ == "__main__":
    main()
