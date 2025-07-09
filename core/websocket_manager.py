"""
Manager de WebSocket para manejo de conexiones y eventos en tiempo real
"""
import json
import asyncio
from typing import List, Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    """
    Manager para manejar múltiples conexiones WebSocket y broadcasting de eventos
    """
    
    def __init__(self):
        # Conexiones activas organizadas por canales
        self.connections: Dict[str, Set[WebSocket]] = {}
        self.connection_info: Dict[WebSocket, Dict] = {}
        
    async def connect(self, websocket: WebSocket, channel: str = "general", user_id: Optional[str] = None):
        """
        Conectar un nuevo cliente WebSocket a un canal específico
        """
        await websocket.accept()
        
        if channel not in self.connections:
            self.connections[channel] = set()
            
        self.connections[channel].add(websocket)
        self.connection_info[websocket] = {
            "channel": channel,
            "user_id": user_id,
            "connected_at": datetime.now(),
        }
        
        logger.info(f"Cliente conectado al canal '{channel}'. Total conexiones: {len(self.connections[channel])}")
        
        # Enviar mensaje de bienvenida
        await self.send_personal_message(websocket, {
            "type": "connection",
            "status": "connected",
            "channel": channel,
            "timestamp": datetime.now().isoformat()
        })
    
    def disconnect(self, websocket: WebSocket):
        """
        Desconectar un cliente WebSocket
        """
        if websocket in self.connection_info:
            channel = self.connection_info[websocket]["channel"]
            self.connections[channel].discard(websocket)
            
            # Limpiar canal si no hay conexiones
            if not self.connections[channel]:
                del self.connections[channel]
                
            del self.connection_info[websocket]
            logger.info(f"Cliente desconectado del canal '{channel}'")
    
    async def send_personal_message(self, websocket: WebSocket, data: dict):
        """
        Enviar mensaje a un cliente específico
        """
        try:
            await websocket.send_text(json.dumps(data))
        except Exception as e:
            logger.error(f"Error enviando mensaje personal: {e}")
            self.disconnect(websocket)
    
    async def broadcast_to_channel(self, channel: str, data: dict):
        """
        Enviar mensaje a todos los clientes de un canal
        """
        if channel not in self.connections:
            return
            
        message = json.dumps(data)
        disconnected = []
        
        for websocket in self.connections[channel].copy():
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Error enviando broadcast: {e}")
                disconnected.append(websocket)
        
        # Limpiar conexiones fallidas
        for websocket in disconnected:
            self.disconnect(websocket)
    
    async def broadcast_to_all(self, data: dict):
        """
        Enviar mensaje a todos los canales
        """
        for channel in self.connections:
            await self.broadcast_to_channel(channel, data)
    
    def get_channel_stats(self, channel: str) -> dict:
        """
        Obtener estadísticas de un canal
        """
        if channel not in self.connections:
            return {"connections": 0, "users": []}
            
        users = []
        for websocket in self.connections[channel]:
            info = self.connection_info.get(websocket, {})
            users.append({
                "user_id": info.get("user_id"),
                "connected_at": info.get("connected_at").isoformat() if info.get("connected_at") else None
            })
        
        return {
            "connections": len(self.connections[channel]),
            "users": users
        }

# Instancia global del manager
websocket_manager = WebSocketManager()
