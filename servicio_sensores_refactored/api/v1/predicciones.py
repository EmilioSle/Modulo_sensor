"""
Router para predicciones de sequía
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database import get_db
from services.prediccion_service import PrediccionService
from schemas.prediccion import PrediccionCreate, PrediccionUpdate, PrediccionResponse
from auth.security import verify_token

router = APIRouter(prefix="/predicciones", tags=["predicciones"])


def get_prediccion_service(db: Session = Depends(get_db)) -> PrediccionService:
    return PrediccionService(db)


@router.get("/", response_model=List[PrediccionResponse])
def get_predicciones(
    skip: int = 0,
    limit: int = 100,
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Obtener todas las predicciones"""
    return service.get_all(skip=skip, limit=limit)


@router.get("/{prediccion_id}", response_model=PrediccionResponse)
def get_prediccion(
    prediccion_id: int,
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Obtener predicción por ID"""
    prediccion = service.get_by_id(prediccion_id)
    if not prediccion:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
    return prediccion


@router.post("/", response_model=PrediccionResponse, status_code=status.HTTP_201_CREATED)
def create_prediccion(
    prediccion_data: PrediccionCreate,
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Crear nueva predicción"""
    return service.create(prediccion_data)


@router.put("/{prediccion_id}", response_model=PrediccionResponse)
def update_prediccion(
    prediccion_id: int,
    prediccion_data: PrediccionUpdate,
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Actualizar predicción"""
    prediccion = service.update(prediccion_id, prediccion_data)
    if not prediccion:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
    return prediccion


@router.delete("/{prediccion_id}")
def delete_prediccion(
    prediccion_id: int,
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Eliminar predicción"""
    if not service.delete(prediccion_id):
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
    return {"message": "Predicción eliminada exitosamente"}


@router.get("/ubicacion/{ubicacion_id}", response_model=List[PrediccionResponse])
def get_predicciones_by_ubicacion(
    ubicacion_id: int,
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Obtener predicciones por ubicación"""
    return service.get_by_ubicacion(ubicacion_id)


@router.get("/ubicacion/{ubicacion_id}/latest", response_model=PrediccionResponse)
def get_latest_prediccion_by_ubicacion(
    ubicacion_id: int,
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Obtener la predicción más reciente para una ubicación"""
    prediccion = service.get_latest_by_ubicacion(ubicacion_id)
    if not prediccion:
        raise HTTPException(
            status_code=404, 
            detail="No se encontraron predicciones para esta ubicación"
        )
    return prediccion


@router.get("/high-risk", response_model=List[PrediccionResponse])
def get_high_risk_predictions(
    threshold: float = Query(0.7, ge=0.0, le=1.0, description="Umbral de probabilidad para alto riesgo"),
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Obtener predicciones de alto riesgo"""
    return service.get_high_risk_predictions(threshold)


@router.post("/generate", response_model=PrediccionResponse)
def generate_prediction(
    ubicacion_id: int = Query(..., description="ID de la ubicación"),
    temperatura_promedio: float = Query(..., description="Temperatura promedio en °C"),
    humedad_promedio: float = Query(..., ge=0.0, le=100.0, description="Humedad promedio en %"),
    comentario: str = Query("", description="Comentario adicional"),
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Generar predicción automática usando ML o lógica heurística"""
    return service.generate_prediction(ubicacion_id, temperatura_promedio, humedad_promedio, comentario)


@router.get("/statistics", response_model=dict)
def get_prediction_statistics(
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Obtener estadísticas de predicciones"""
    return service.get_statistics()


@router.get("/ubicacion/{ubicacion_id}/trends", response_model=dict)
def get_location_trends(
    ubicacion_id: int,
    days: int = Query(30, ge=1, le=365, description="Días hacia atrás para analizar"),
    service: PrediccionService = Depends(get_prediccion_service),
    token: dict = Depends(verify_token)
):
    """Analizar tendencias de predicciones para una ubicación"""
    return service.analyze_trends(ubicacion_id, days)
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database import get_db
from auth.security import get_current_user
from services.prediccion_service import prediccion_service
from schemas.prediccion import PrediccionCreate, PrediccionUpdate, PrediccionResponse

router = APIRouter(prefix="/predicciones", tags=["Predicciones"])

@router.post("/", response_model=PrediccionResponse, status_code=status.HTTP_201_CREATED)
def create_prediccion(
    prediccion_data: PrediccionCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Crear una nueva predicción"""
    try:
        return prediccion_service.create_prediccion(db, prediccion_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PrediccionResponse])
def get_predicciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener lista de predicciones"""
    return prediccion_service.get_all_predicciones(db, skip=skip, limit=limit)

@router.get("/ubicacion/{ubicacion_id}", response_model=List[PrediccionResponse])
def get_predicciones_by_ubicacion(
    ubicacion_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener predicciones de una ubicación específica"""
    return prediccion_service.get_predicciones_by_ubicacion(db, ubicacion_id)

@router.get("/ubicacion/{ubicacion_id}/latest", response_model=PrediccionResponse)
def get_latest_prediction(
    ubicacion_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener la predicción más reciente de una ubicación"""
    prediccion = prediccion_service.get_latest_prediction_by_location(db, ubicacion_id)
    if not prediccion:
        raise HTTPException(status_code=404, detail="No hay predicciones para esta ubicación")
    return prediccion

@router.get("/high-risk", response_model=List[PrediccionResponse])
def get_high_risk_predictions(
    threshold: float = Query(0.7, ge=0.0, le=1.0, description="Umbral de probabilidad"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener predicciones de alto riesgo"""
    return prediccion_service.get_high_risk_predictions(db, threshold)

@router.get("/recent", response_model=List[PrediccionResponse])
def get_recent_predictions(
    days: int = Query(30, ge=1, le=365, description="Días hacia atrás"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener predicciones recientes"""
    return prediccion_service.get_recent_predictions(db, days)

@router.post("/generate", response_model=PrediccionResponse)
def generate_prediction_with_ml(
    ubicacion_id: int = Query(..., description="ID de la ubicación"),
    temperatura_promedio: float = Query(..., ge=-50, le=70, description="Temperatura promedio"),
    humedad_promedio: float = Query(..., ge=0, le=100, description="Humedad promedio"),
    comentario: str = Query(None, description="Comentario opcional"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Generar una predicción usando ML o lógica heurística"""
    try:
        return prediccion_service.generate_prediction_with_ml(
            db, ubicacion_id, temperatura_promedio, humedad_promedio, comentario
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/statistics")
def get_prediction_statistics(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener estadísticas de predicciones"""
    return prediccion_service.get_prediction_statistics(db)

@router.get("/{prediccion_id}", response_model=PrediccionResponse)
def get_prediccion(
    prediccion_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener una predicción por ID"""
    prediccion = prediccion_service.get_prediccion(db, prediccion_id)
    if not prediccion:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
    return prediccion

@router.put("/{prediccion_id}", response_model=PrediccionResponse)
def update_prediccion(
    prediccion_id: int,
    prediccion_data: PrediccionUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Actualizar una predicción"""
    try:
        prediccion = prediccion_service.update_prediccion(db, prediccion_id, prediccion_data)
        if not prediccion:
            raise HTTPException(status_code=404, detail="Predicción no encontrada")
        return prediccion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{prediccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prediccion(
    prediccion_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Eliminar una predicción"""
    if not prediccion_service.delete_prediccion(db, prediccion_id):
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
