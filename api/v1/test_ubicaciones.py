"""
API Router para pruebas de ubicaciones (sin autenticación)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from core.database import get_db
from services.ubicacion_service import ubicacion_service
from schemas.ubicacion import UbicacionCreate, UbicacionUpdate, UbicacionResponse

# Router temporal para pruebas sin autenticación
test_ubicaciones_router = APIRouter(prefix="/test-ubicaciones", tags=["Test Ubicaciones (No Auth)"])

@test_ubicaciones_router.post("/", response_model=UbicacionResponse, status_code=status.HTTP_201_CREATED)
def create_test_ubicacion(
    ubicacion_data: UbicacionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Crear una ubicación de prueba (sin autenticación)"""
    try:
        result = ubicacion_service.create_ubicacion(db, ubicacion_data, background_tasks)
        if not result:
            raise HTTPException(status_code=500, detail="Error al crear la ubicación")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@test_ubicaciones_router.get("/", response_model=List[UbicacionResponse])
def get_test_ubicaciones(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener ubicaciones de prueba (sin autenticación)"""
    try:
        result = ubicacion_service.get_all_ubicaciones(db, skip=skip, limit=limit)
        return result if result is not None else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@test_ubicaciones_router.put("/{ubicacion_id}", response_model=UbicacionResponse)
def update_test_ubicacion(
    ubicacion_id: int,
    ubicacion_data: UbicacionUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Actualizar una ubicación de prueba (sin autenticación)"""
    try:
        ubicacion = ubicacion_service.update_ubicacion(db, ubicacion_id, ubicacion_data, background_tasks)
        if not ubicacion:
            raise HTTPException(status_code=404, detail="Ubicación no encontrada")
        return ubicacion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@test_ubicaciones_router.delete("/{ubicacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_ubicacion(
    ubicacion_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Eliminar una ubicación de prueba (sin autenticación)"""
    try:
        if not ubicacion_service.delete_ubicacion(db, ubicacion_id, background_tasks):
            raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
