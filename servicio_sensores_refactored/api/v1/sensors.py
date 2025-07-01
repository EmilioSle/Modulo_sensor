"""
API Router para sensores
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from auth.security import get_current_user
from services.sensor_service import sensor_service
from schemas.sensor import SensorCreate, SensorUpdate, SensorResponse

router = APIRouter(prefix="/sensores", tags=["Sensores"])

@router.post("/", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
def create_sensor(
    sensor_data: SensorCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Crear un nuevo sensor"""
    try:
        return sensor_service.create_sensor(db, sensor_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[SensorResponse])
def get_sensors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener lista de sensores"""
    return sensor_service.get_all_sensors(db, skip=skip, limit=limit)

@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener un sensor por ID"""
    sensor = sensor_service.get_sensor(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return sensor

@router.put("/{sensor_id}", response_model=SensorResponse)
def update_sensor(
    sensor_id: int,
    sensor_data: SensorUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Actualizar un sensor"""
    sensor = sensor_service.update_sensor(db, sensor_id, sensor_data)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return sensor

@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Eliminar un sensor"""
    if not sensor_service.delete_sensor(db, sensor_id):
        raise HTTPException(status_code=404, detail="Sensor no encontrado")

@router.get("/tipo/{tipo}", response_model=List[SensorResponse])
def get_sensors_by_type(
    tipo: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener sensores por tipo"""
    return sensor_service.get_sensors_by_type(db, tipo)
