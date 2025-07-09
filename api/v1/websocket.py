"""
Router de WebSocket para conexiones en tiempo real
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from typing import Optional
import logging

from core.websocket_manager import websocket_manager
from core.events import event_emitter
from auth.security import get_current_user_websocket

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websocket"])

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    channel: str = Query(default="general", description="Canal de eventos a suscribirse"),
    user_id: Optional[str] = Query(default=None, description="ID del usuario (opcional)")
):
    """
    Endpoint principal de WebSocket para eventos en tiempo real
    
    Canales disponibles:
    - general: Eventos generales del sistema
    - sensors: Eventos de sensores
    - readings: Eventos de lecturas
    - locations: Eventos de ubicaciones  
    - anomalies: Eventos de anomalías
    - predictions: Eventos de predicciones
    """
    await websocket_manager.connect(websocket, channel, user_id)
    
    try:
        # Enviar estadísticas del canal al conectarse
        stats = websocket_manager.get_channel_stats(channel)
        await websocket_manager.send_personal_message(websocket, {
            "type": "channel_stats",
            "channel": channel,
            "stats": stats
        })
        
        # Mantener conexión activa y manejar mensajes
        while True:
            try:
                # Esperar por mensajes del cliente
                data = await websocket.receive_text()
                logger.info(f"Mensaje recibido en canal '{channel}': {data}")
                
                # Aquí podrías procesar comandos del cliente si es necesario
                # Por ejemplo: cambiar de canal, solicitar información específica, etc.
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error procesando mensaje WebSocket: {e}")
                await websocket_manager.send_personal_message(websocket, {
                    "type": "error", 
                    "message": "Error procesando mensaje"
                })
                
    except WebSocketDisconnect:
        logger.info(f"Cliente desconectado del canal '{channel}'")
    except Exception as e:
        logger.error(f"Error en conexión WebSocket: {e}")
    finally:
        websocket_manager.disconnect(websocket)

@router.websocket("/ws/secure")
async def secure_websocket_endpoint(
    websocket: WebSocket,
    channel: str = Query(default="general", description="Canal de eventos a suscribirse"),
    # user: dict = Depends(get_current_user_websocket)  # Descomenta si tienes autenticación WebSocket
):
    """
    Endpoint de WebSocket con autenticación
    """
    # user_id = user.get("user_id")  # Descomenta si tienes autenticación
    user_id = "authenticated_user"  # Placeholder
    
    await websocket_manager.connect(websocket, channel, user_id)
    
    try:
        # Enviar información de usuario autenticado
        await websocket_manager.send_personal_message(websocket, {
            "type": "authenticated",
            "user_id": user_id,
            "channel": channel
        })
        
        while True:
            try:
                data = await websocket.receive_text()
                logger.info(f"Mensaje autenticado recibido de {user_id} en '{channel}': {data}")
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error en WebSocket autenticado: {e}")
                
    except WebSocketDisconnect:
        logger.info(f"Usuario autenticado {user_id} desconectado del canal '{channel}'")
    except Exception as e:
        logger.error(f"Error en WebSocket autenticado: {e}")
    finally:
        websocket_manager.disconnect(websocket)

@router.get("/ws/stats")
async def get_websocket_stats():
    """
    Obtener estadísticas de las conexiones WebSocket
    """
    stats = {}
    for channel in websocket_manager.connections:
        stats[channel] = websocket_manager.get_channel_stats(channel)
    
    return {
        "total_channels": len(websocket_manager.connections),
        "channels": stats
    }

@router.get("/ws/stats/{channel}")
async def get_channel_stats(channel: str):
    """
    Obtener estadísticas de un canal específico
    """
    stats = websocket_manager.get_channel_stats(channel)
    return {
        "channel": channel,
        "stats": stats
    }

@router.post("/ws/test-event")
async def send_test_event(
    channel: str = "general",
    message: str = "Evento de prueba"
):
    """
    Enviar un evento de prueba (solo para desarrollo/testing)
    """
    await event_emitter.emit_system_event(
        message=message,
        level="info",
        data={"test": True},
        channel=channel
    )
    
    return {
        "message": f"Evento de prueba enviado al canal '{channel}'",
        "data": message
    }
