# Sistema WebSocket para Reportes en Tiempo Real

## Descripción
Sistema de WebSocket implementado para el módulo de sensores que permite recibir notificaciones en tiempo real de todas las operaciones CRUD (crear, actualizar, eliminar) realizadas sobre las entidades del sistema.

## Arquitectura

### Componentes Principales

1. **WebSocketManager** (`core/websocket_manager.py`)
   - Gestiona múltiples conexiones WebSocket
   - Organiza conexiones por canales temáticos
   - Maneja reconexiones y desconexiones automáticamente

2. **EventEmitter** (`core/events.py`)
   - Sistema de emisión de eventos
   - Tipos de eventos predefinidos (created, updated, deleted, etc.)
   - Soporte para metadatos adicionales

3. **Router WebSocket** (`api/v1/websocket.py`)
   - Endpoints de conexión WebSocket
   - Endpoints de estadísticas
   - Endpoints de prueba

4. **Servicios Modificados**
   - Integración con el sistema de eventos
   - Emisión automática de eventos en operaciones CRUD

## Canales Disponibles

| Canal | Descripción | Eventos |
|-------|-------------|---------|
| `general` | Eventos generales del sistema | Todos los eventos |
| `sensors` | Eventos de sensores | created, updated, deleted |
| `readings` | Eventos de lecturas | created, updated |
| `locations` | Eventos de ubicaciones | created, updated, deleted |
| `anomalies` | Eventos de anomalías | created, anomaly_detected |
| `predictions` | Eventos de predicciones | created, prediction_completed |

## Tipos de Eventos

### Eventos de Entidad
```json
{
  "type": "entity_event",
  "entity_type": "sensor",
  "event_type": "created",
  "entity_id": 123,
  "data": {
    "id": 123,
    "tipo": "temperatura",
    "modelo": "DHT22",
    "created_at": "2025-07-20T00:05:37.123Z"
  },
  "timestamp": "2025-07-20T00:05:37.123Z",
  "metadata": {
    "action": "create_sensor"
  }
}
```

### Eventos del Sistema
```json
{
  "type": "system_event",
  "level": "info",
  "message": "Sistema iniciado correctamente",
  "data": {},
  "timestamp": "2025-07-20T00:05:37.123Z"
}
```

## Endpoints WebSocket

### Conexión Principal
```
ws://localhost:8000/api/v1/ws?channel=CANAL&user_id=USUARIO
```

**Parámetros:**
- `channel` (opcional): Canal a suscribirse (default: "general")
- `user_id` (opcional): ID del usuario para tracking

### Conexión Segura (Autenticada)
```
ws://localhost:8000/api/v1/ws/secure?channel=CANAL
```

## Endpoints HTTP

### Estadísticas Generales
```http
GET /api/v1/ws/stats
```

**Respuesta:**
```json
{
  "total_channels": 3,
  "channels": {
    "general": {
      "connections": 2,
      "users": [...]
    },
    "sensors": {
      "connections": 1,
      "users": [...]
    }
  }
}
```

### Estadísticas por Canal
```http
GET /api/v1/ws/stats/{channel}
```

### Enviar Evento de Prueba
```http
POST /api/v1/ws/test-event?channel=general&message=test
```

## Uso del Cliente

### 1. Cliente HTML
Abre el archivo `websocket_client.html` en tu navegador:
```
file:///ruta/al/proyecto/websocket_client.html
```

### 2. Cliente JavaScript
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws?channel=sensors');

ws.onopen = function(event) {
    console.log('Conectado al WebSocket');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Evento recibido:', data);
};

ws.onclose = function(event) {
    console.log('Conexión cerrada');
};

ws.onerror = function(error) {
    console.log('Error:', error);
};
```

### 3. Cliente Python
```python
import asyncio
import websockets
import json

async def client():
    uri = "ws://localhost:8000/api/v1/ws?channel=sensors"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Evento recibido: {data}")

asyncio.run(client())
```

## Integración en Servicios

### Ejemplo de Emisión de Eventos
```python
from core.events import event_emitter, EventType

# En un servicio
async def create_sensor(self, db: Session, sensor_data: SensorCreate):
    sensor = self.repository.create(db, **sensor_data.dict())
    
    # Emitir evento
    if sensor:
        asyncio.create_task(event_emitter.emit_sensor_event(
            EventType.CREATED,
            {
                "id": sensor.id,
                "tipo": sensor.tipo,
                "modelo": sensor.modelo
            },
            sensor.id,
            {"action": "create_sensor"}
        ))
    
    return sensor
```

## Ejemplo de Uso Completo

Ver archivos:
- `websocket_client.html` - Cliente web completo
- `test_websocket_only.py` - Pruebas automatizadas

---

**Autor:** Sistema de Sensores WebSocket  
**Fecha:** 20 de Julio, 2025  
**Versión:** 1.0.0
