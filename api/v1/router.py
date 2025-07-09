"""
Router principal de la API v1
"""
from fastapi import APIRouter

from api.v1.sensors import router as sensors_router
from api.v1.readings import router as readings_router
from api.v1.ubicaciones import router as ubicaciones_router
from api.v1.anomalias import router as anomalias_router
from api.v1.predicciones import router as predicciones_router
from api.v1.websocket import router as websocket_router

api_router = APIRouter()

# Incluir todos los routers
api_router.include_router(sensors_router)
api_router.include_router(readings_router)
api_router.include_router(ubicaciones_router)
api_router.include_router(anomalias_router)
api_router.include_router(predicciones_router)
api_router.include_router(websocket_router)
