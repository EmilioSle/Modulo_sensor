# Sistema de WebSocket - Reportes en Tiempo Real

Este documento describe la implementación del sistema de WebSocket para reportes en tiempo real de eventos en el módulo de sensores.

## 📋 Índice

1. [Características](#características)
2. [Arquitectura](#arquitectura)
3. [Endpoints WebSocket](#endpoints-websocket)
4. [Tipos de Eventos](#tipos-de-eventos)
5. [Canales Disponibles](#canales-disponibles)
6. [Uso del Sistema](#uso-del-sistema)
7. [Ejemplos de Código](#ejemplos-de-código)
8. [Pruebas](#pruebas)

## ✨ Características

- **Conexiones múltiples**: Soporte para múltiples clientes simultáneos
- **Canales organizados**: Eventos organizados por tipo de entidad
- **Eventos automáticos**: Emisión automática al crear/actualizar/eliminar entidades
- **Cliente de prueba**: Interfaz web para testing y monitoreo
- **Autenticación**: Soporte para WebSocket autenticado (opcional)
- **Estadísticas**: Monitoreo de conexiones y estadísticas en tiempo real

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente Web   │    │   Cliente App   │    │  Otro Cliente   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴───────────────┐
                    │     WebSocket Manager       │
                    │  - Gestión de conexiones    │
                    │  - Organización por canales │
                    │  - Broadcasting de eventos  │
                    └─────────────┬───────────────┘
                                 │
                    ┌─────────────┴───────────────┐
                    │      Event Emitter          │
                    │  - Emisión de eventos       │
                    │  - Formateo de mensajes     │
                    │  - Metadatos de eventos     │
                    └─────────────┬───────────────┘
                                 │
                    ┌─────────────┴───────────────┐
                    │       Servicios             │
                    │  - SensorService            │
                    │  - LecturaService           │
                    │  - AnomaliaService          │
                    │  - PrediccionService        │
                    └─────────────────────────────┘
```

## 🔌 Endpoints WebSocket

### Conexión básica
```
ws://localhost:8000/api/v1/ws?channel=general&user_id=optional
```

### Conexión autenticada
```
ws://localhost:8000/api/v1/ws/secure?channel=general&token=jwt_token
```

### Parámetros de consulta:
- `channel`: Canal al que suscribirse (por defecto: "general")
- `user_id`: ID del usuario (opcional)
- `token`: Token JWT para autenticación (solo en endpoint seguro)

## 📡 Tipos de Eventos

### 1. Eventos de Entidad (`entity_event`)

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
    "created_at": "2025-07-20T10:30:00Z"
  },
  "timestamp": "2025-07-20T10:30:00Z",
  "metadata": {
    "action": "create_sensor"
  }
}
```

**Tipos de eventos de entidad:**
- `created`: Entidad creada
- `updated`: Entidad actualizada
- `deleted`: Entidad eliminada
- `anomaly_detected`: Anomalía detectada
- `prediction_completed`: Predicción completada

### 2. Eventos del Sistema (`system_event`)

```json
{
  "type": "system_event",
  "level": "info",
  "message": "Sistema iniciado correctamente",
  "data": {
    "module": "websocket",
    "version": "1.0.0"
  },
  "timestamp": "2025-07-20T10:30:00Z"
}
```

**Niveles de sistema:**
- `info`: Información general
- `warning`: Advertencias
- `error`: Errores

### 3. Eventos de Conexión (`connection`)

```json
{
  "type": "connection",
  "status": "connected",
  "channel": "sensors",
  "timestamp": "2025-07-20T10:30:00Z"
}
```

## 📊 Canales Disponibles

| Canal | Descripción | Eventos |
|-------|-------------|---------|
| `general` | Eventos generales del sistema | Todos los tipos |
| `sensors` | Eventos relacionados con sensores | CRUD de sensores |
| `readings` | Eventos de lecturas de sensores | Nuevas lecturas, actualizaciones |
| `locations` | Eventos de ubicaciones | CRUD de ubicaciones |
| `anomalies` | Eventos de anomalías detectadas | Detección, resolución de anomalías |
| `predictions` | Eventos de predicciones ML | Predicciones completadas, actualizaciones |

## 🚀 Uso del Sistema

### 1. Iniciar el servidor

```bash
cd /home/elpajarowtf/Documentos/PROYECTOS/Modulo_sensor
python core/server.py
```

### 2. Conectar cliente WebSocket

#### Usando JavaScript (navegador)
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws?channel=sensors');

ws.onopen = function(event) {
    console.log('Conectado al WebSocket');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Evento recibido:', data);
    
    // Manejar diferentes tipos de eventos
    if (data.type === 'entity_event') {
        handleEntityEvent(data);
    } else if (data.type === 'system_event') {
        handleSystemEvent(data);
    }
};

function handleEntityEvent(event) {
    console.log(`${event.entity_type} ${event.event_type}:`, event.data);
}

function handleSystemEvent(event) {
    console.log(`Sistema [${event.level}]: ${event.message}`);
}
```

#### Usando Python
```python
import asyncio
import websockets
import json

async def listen_to_events():
    uri = "ws://localhost:8000/api/v1/ws?channel=sensors"
    
    async with websockets.connect(uri) as websocket:
        print("Conectado al WebSocket")
        
        async for message in websocket:
            data = json.loads(message)
            print(f"Evento recibido: {data}")
            
            if data['type'] == 'entity_event':
                print(f"Entidad {data['entity_type']} {data['event_type']}: ID {data['entity_id']}")

# Ejecutar
asyncio.run(listen_to_events())
```

### 3. Usar el cliente web de prueba

1. Abrir `websocket_client.html` en un navegador
2. Configurar la URL del servidor: `ws://localhost:8000/api/v1/ws`
3. Seleccionar el canal deseado
4. Hacer clic en "Conectar"
5. Observar los eventos en tiempo real

## 📋 Ejemplos de Código

### Crear un sensor (genera evento)

```bash
curl -X POST "http://localhost:8000/api/v1/sensors" \
     -H "Content-Type: application/json" \
     -d '{
       "tipo": "temperatura",
       "modelo": "DHT22"
     }'
```

**Evento generado:**
```json
{
  "type": "entity_event",
  "entity_type": "sensor",
  "event_type": "created",
  "entity_id": 1,
  "data": {
    "id": 1,
    "tipo": "temperatura",
    "modelo": "DHT22",
    "created_at": "2025-07-20T10:30:00Z"
  },
  "timestamp": "2025-07-20T10:30:00Z",
  "metadata": {
    "action": "create_sensor"
  }
}
```

### Crear una lectura (genera evento)

```bash
curl -X POST "http://localhost:8000/api/v1/readings" \
     -H "Content-Type: application/json" \
     -d '{
       "sensor_id": 1,
       "temperatura": 23.5,
       "humedad": 65.2,
       "timestamp": "2025-07-20T10:30:00Z"
     }'
```

## 🧪 Pruebas

### 1. Usar el script de prueba automatizada

```bash
# Ejecutar el tester interactivo
python websocket_tester.py

# Opciones disponibles:
# 1. Prueba única
# 2. Pruebas continuas (5 minutos)
# 3. Pruebas continuas personalizadas
# 4. Enviar evento de prueba
# 5. Ver estadísticas
```

### 2. Endpoints de prueba HTTP

#### Enviar evento de prueba
```bash
curl -X POST "http://localhost:8000/api/v1/ws/test-event?channel=general&message=Prueba"
```

#### Ver estadísticas de WebSocket
```bash
curl "http://localhost:8000/api/v1/ws/stats"
```

#### Ver estadísticas de un canal específico
```bash
curl "http://localhost:8000/api/v1/ws/stats/sensors"
```

### 3. Pruebas manuales

1. **Abrir múltiples clientes**: Abre varias pestañas con `websocket_client.html`
2. **Suscribirse a diferentes canales**: Cada cliente puede escuchar un canal diferente
3. **Generar eventos**: Usa la API REST para crear/actualizar/eliminar entidades
4. **Observar la propagación**: Los eventos deben aparecer en todos los clientes conectados al canal correspondiente

## 📊 Monitoreo y Estadísticas

### Estadísticas disponibles:

```json
{
  "total_channels": 3,
  "channels": {
    "general": {
      "connections": 2,
      "users": [
        {
          "user_id": "user1",
          "connected_at": "2025-07-20T10:00:00Z"
        }
      ]
    },
    "sensors": {
      "connections": 1,
      "users": [...]
    }
  }
}
```

## 🔐 Seguridad

### Autenticación WebSocket

Para usar WebSocket autenticado:

1. Obtén un token JWT del endpoint `/auth/login`
2. Conéctate al endpoint seguro: `ws://localhost:8000/api/v1/ws/secure?token=YOUR_JWT`
3. El sistema validará el token automáticamente

### Consideraciones de producción

- Implementar límites de conexiones por IP
- Validar permisos por canal
- Configurar CORS apropiadamente
- Usar HTTPS/WSS en producción
- Implementar reconexión automática en clientes
- Monitorear uso de memoria y conexiones

## 🔧 Configuración

### Variables de entorno

```bash
# En tu archivo .env
WEBSOCKET_MAX_CONNECTIONS=100
WEBSOCKET_PING_INTERVAL=30
WEBSOCKET_PING_TIMEOUT=10
```

### Configuración CORS

```python
# En core/app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurar apropiadamente en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🚨 Solución de Problemas

### Problemas comunes:

1. **Error de conexión**: Verificar que el servidor esté ejecutándose en el puerto correcto
2. **No se reciben eventos**: Verificar que el canal sea correcto
3. **Conexión se cierra**: Verificar logs del servidor para errores
4. **Eventos duplicados**: Verificar que no hay múltiples conexiones del mismo cliente

### Logs útiles:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("websocket")
```

¡El sistema de WebSocket está listo para usar! 🎉
