#!/usr/bin/env python3
"""
Script simple para probar solo eventos WebSocket
"""
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
    """Función principal de prueba WebSocket"""
    print("🚀 PRUEBA DE EVENTOS WEBSOCKET")
    print("=" * 40)
    print("📝 Esta prueba solo testa los eventos WebSocket")
    print("🔗 Abre el cliente WebSocket en tu navegador:")
    print("📱 file:///home/elpajarowtf/Documentos/PROYECTOS/Modulo_sensor/websocket_client.html")
    print("\n⏰ Esperando 5 segundos para que conectes...")
    
    for i in range(5, 0, -1):
        print(f"   {i}...", end=" ", flush=True)
        time.sleep(1)
    print("\n")

    try:
        # Obtener estadísticas iniciales
        print("1. 📊 Estadísticas iniciales:")
        get_websocket_stats()
        time.sleep(1)

        # Eventos de prueba básicos
        print("\n2. 📢 Enviando eventos de prueba básicos:")
        test_events = [
            ("general", "¡Sistema WebSocket iniciado!"),
            ("general", "Probando conectividad..."),
            ("system", "Evento de sistema de prueba"),
        ]
        
        for channel, message in test_events:
            send_test_event(channel, message)
            time.sleep(1)

        # Eventos simulando operaciones CRUD
        print("\n3. 🔧 Simulando eventos de entidades:")
        entity_events = [
            ("sensors", "Simulación: Sensor DHT22 creado"),
            ("sensors", "Simulación: Sensor actualizado"),
            ("readings", "Simulación: Nueva lectura - T:25°C, H:60%"),
            ("readings", "Simulación: Nueva lectura - T:26°C, H:58%"),
            ("anomalies", "Simulación: Posible anomalía detectada"),
            ("predictions", "Simulación: Predicción completada"),
        ]
        
        for channel, message in entity_events:
            send_test_event(channel, message)
            time.sleep(1.5)

        # Eventos masivos para probar rendimiento
        print("\n4. 🚀 Prueba de eventos masivos:")
        for i in range(10):
            channel = ["general", "sensors", "readings"][i % 3]
            message = f"Evento masivo #{i+1}/10"
            send_test_event(channel, message)
            time.sleep(0.3)

        # Estadísticas finales
        print("\n5. 📊 Estadísticas finales:")
        get_websocket_stats()

        print("\n✅ ¡Prueba de WebSocket completada!")
        print("📝 Revisa los eventos recibidos en tu cliente WebSocket")
        print("🔍 Deberías haber visto:")
        print("   - Eventos de conexión")
        print("   - Eventos de sistema")
        print("   - Eventos simulados de entidades")
        print("   - Estadísticas de canales")

    except KeyboardInterrupt:
        print("\n⏹️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")

if __name__ == "__main__":
    main()
