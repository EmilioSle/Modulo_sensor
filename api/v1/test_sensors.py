"""
API Router para pruebas de WebSocket (sin autenticación)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from core.database import get_db
from services.sensor_service import sensor_service
from schemas.sensor import SensorCreate, SensorUpdate, SensorResponse

# Router temporal para pruebas sin autenticación
test_router = APIRouter(prefix="/test-sensors", tags=["Test Sensors (No Auth)"])

@test_router.post("/", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
def create_test_sensor(
    sensor_data: SensorCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Crear un sensor de prueba (sin autenticación)"""
    try:
        result = sensor_service.create_sensor(db, sensor_data, background_tasks)
        if not result:
            raise HTTPException(status_code=500, detail="Error al crear el sensor")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@test_router.get("/", response_model=List[SensorResponse])
def get_test_sensors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener sensores de prueba (sin autenticación)"""
    try:
        result = sensor_service.get_all_sensors(db, skip=skip, limit=limit)
        return result if result is not None else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@test_router.put("/{sensor_id}", response_model=SensorResponse)
def update_test_sensor(
    sensor_id: int,
    sensor_data: SensorUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Actualizar un sensor de prueba (sin autenticación)"""
    try:
        sensor = sensor_service.update_sensor(db, sensor_id, sensor_data, background_tasks)
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return sensor
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@test_router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_sensor(
    sensor_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Eliminar un sensor de prueba (sin autenticación)"""
    try:
        if not sensor_service.delete_sensor(db, sensor_id, background_tasks):
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
