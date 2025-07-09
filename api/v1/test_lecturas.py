"""
API Router para pruebas de lecturas (sin autenticación)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from core.database import get_db
from services.lectura_service import lectura_service
from schemas.lectura import LecturaCreate, LecturaUpdate, LecturaResponse

# Router temporal para pruebas sin autenticación
test_lecturas_router = APIRouter(prefix="/test-lecturas", tags=["Test Lecturas (No Auth)"])

@test_lecturas_router.post("/", response_model=LecturaResponse, status_code=status.HTTP_201_CREATED)
def create_test_lectura(
    lectura_data: LecturaCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Crear una lectura de prueba (sin autenticación)"""
    try:
        result = lectura_service.create_lectura(db, lectura_data, background_tasks)
        if not result:
            raise HTTPException(status_code=500, detail="Error al crear la lectura")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@test_lecturas_router.get("/", response_model=List[LecturaResponse])
def get_test_lecturas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lecturas de prueba (sin autenticación)"""
    try:
        result = lectura_service.get_all_lecturas(db, skip=skip, limit=limit)
        return result if result is not None else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@test_lecturas_router.get("/sensor/{sensor_id}", response_model=List[LecturaResponse])
def get_test_readings_by_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    """Obtener lecturas de prueba por sensor (sin autenticación)"""
    try:
        result = lectura_service.get_readings_by_sensor(db, sensor_id)
        return result if result is not None else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@test_lecturas_router.put("/{lectura_id}", response_model=LecturaResponse)
def update_test_lectura(
    lectura_id: int,
    lectura_data: LecturaUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Actualizar una lectura de prueba (sin autenticación)"""
    try:
        lectura = lectura_service.update_lectura(db, lectura_id, lectura_data, background_tasks)
        if not lectura:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        return lectura
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@test_lecturas_router.delete("/{lectura_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_lectura(
    lectura_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Eliminar una lectura de prueba (sin autenticación)"""
    try:
        if not lectura_service.delete_lectura(db, lectura_id, background_tasks):
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
