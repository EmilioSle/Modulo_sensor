"""
API Router para ubicaciones
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database import get_db
from auth.security import get_current_user
from services.ubicacion_service import ubicacion_service
from schemas.ubicacion import UbicacionCreate, UbicacionUpdate, UbicacionResponse

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones"])

@router.post("/", response_model=UbicacionResponse, status_code=status.HTTP_201_CREATED)
def create_ubicacion(
    ubicacion_data: UbicacionCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Crear una nueva ubicación"""
    try:
        return ubicacion_service.create_ubicacion(db, ubicacion_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UbicacionResponse])
def get_ubicaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener lista de ubicaciones"""
    return ubicacion_service.get_all_ubicaciones(db, skip=skip, limit=limit)

@router.get("/sensor/{sensor_id}", response_model=List[UbicacionResponse])
def get_ubicaciones_by_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener ubicaciones de un sensor específico"""
    return ubicacion_service.get_ubicaciones_by_sensor(db, sensor_id)

@router.get("/search", response_model=List[UbicacionResponse])
def search_ubicaciones(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Buscar ubicaciones por descripción"""
    return ubicacion_service.search_ubicaciones(db, q)

@router.get("/nearby", response_model=List[UbicacionResponse])
def get_nearby_ubicaciones(
    latitud: str = Query(..., description="Latitud base"),
    longitud: str = Query(..., description="Longitud base"),
    radio: float = Query(0.01, ge=0.001, le=1.0, description="Radio de búsqueda"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener ubicaciones cercanas a unas coordenadas"""
    return ubicacion_service.get_nearby_locations(db, latitud, longitud, radio)

@router.get("/{ubicacion_id}", response_model=UbicacionResponse)
def get_ubicacion(
    ubicacion_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener una ubicación por ID"""
    ubicacion = ubicacion_service.get_ubicacion(db, ubicacion_id)
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return ubicacion

@router.put("/{ubicacion_id}", response_model=UbicacionResponse)
def update_ubicacion(
    ubicacion_id: int,
    ubicacion_data: UbicacionUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Actualizar una ubicación"""
    try:
        ubicacion = ubicacion_service.update_ubicacion(db, ubicacion_id, ubicacion_data)
        if not ubicacion:
            raise HTTPException(status_code=404, detail="Ubicación no encontrada")
        return ubicacion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{ubicacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ubicacion(
    ubicacion_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Eliminar una ubicación"""
    if not ubicacion_service.delete_ubicacion(db, ubicacion_id):
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
