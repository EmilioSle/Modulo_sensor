"""
API Router para lecturas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from auth.security import get_current_user
from services.lectura_service import lectura_service
from schemas.lectura import LecturaCreate, LecturaUpdate, LecturaResponse

router = APIRouter(prefix="/lecturas", tags=["Lecturas"])

@router.post("/", response_model=LecturaResponse, status_code=status.HTTP_201_CREATED)
def create_lectura(
    lectura_data: LecturaCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Crear una nueva lectura"""
    try:
        return lectura_service.create_lectura(db, lectura_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sensor/{sensor_id}", response_model=List[LecturaResponse])
def get_readings_by_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener lecturas de un sensor específico"""
    return lectura_service.get_readings_by_sensor(db, sensor_id)

@router.get("/sensor/{sensor_id}/recent", response_model=List[LecturaResponse])
def get_recent_readings(
    sensor_id: int,
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener lecturas recientes de un sensor"""
    return lectura_service.get_recent_readings(db, sensor_id, hours)

@router.get("/{lectura_id}", response_model=LecturaResponse)
def get_lectura(
    lectura_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener una lectura por ID"""
    lectura = lectura_service.get_lectura(db, lectura_id)
    if not lectura:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return lectura

@router.put("/{lectura_id}", response_model=LecturaResponse)
def update_lectura(
    lectura_id: int,
    lectura_data: LecturaUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Actualizar una lectura"""
    try:
        lectura = lectura_service.update_lectura(db, lectura_id, lectura_data)
        if not lectura:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        return lectura
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{lectura_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lectura(
    lectura_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Eliminar una lectura"""
    if not lectura_service.delete_lectura(db, lectura_id):
        raise HTTPException(status_code=404, detail="Lectura no encontrada")

@router.get("/sensor/{sensor_id}/stats")
def get_sensor_stats(
    sensor_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener estadísticas de un sensor"""
    return lectura_service.get_sensor_stats(db, sensor_id)
