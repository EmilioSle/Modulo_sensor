"""
API Router para anomalías
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database import get_db
from auth.security import get_current_user
from services.anomalia_service import anomalia_service
from schemas.anomalia import AnomaliaCreate, AnomaliaUpdate, AnomaliaResponse

router = APIRouter(prefix="/anomalias", tags=["Anomalías"])

@router.post("/", response_model=AnomaliaResponse, status_code=status.HTTP_201_CREATED)
def create_anomalia(
    anomalia_data: AnomaliaCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Crear una nueva anomalía"""
    try:
        return anomalia_service.create_anomalia(db, anomalia_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[AnomaliaResponse])
def get_anomalias(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener lista de anomalías"""
    return anomalia_service.get_all_anomalias(db, skip=skip, limit=limit)

@router.get("/lectura/{lectura_id}", response_model=List[AnomaliaResponse])
def get_anomalias_by_lectura(
    lectura_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener anomalías de una lectura específica"""
    return anomalia_service.get_anomalias_by_lectura(db, lectura_id)

@router.get("/tipo/{tipo}", response_model=List[AnomaliaResponse])
def get_anomalias_by_tipo(
    tipo: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener anomalías por tipo"""
    return anomalia_service.get_anomalias_by_tipo(db, tipo)

@router.get("/recent", response_model=List[AnomaliaResponse])
def get_recent_anomalias(
    hours: int = Query(24, ge=1, le=168, description="Horas hacia atrás"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener anomalías recientes"""
    return anomalia_service.get_recent_anomalias(db, hours)

@router.get("/critical", response_model=List[AnomaliaResponse])
def get_critical_anomalias(
    threshold: float = Query(50.0, ge=0.0, description="Umbral de criticidad"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener anomalías críticas"""
    return anomalia_service.get_critical_anomalias(db, threshold)

@router.post("/detect/{lectura_id}", response_model=List[AnomaliaResponse])
def detect_anomalies_in_reading(
    lectura_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Detectar anomalías automáticamente en una lectura"""
    try:
        return anomalia_service.detect_anomalies_in_reading(db, lectura_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/statistics")
def get_anomaly_statistics(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener estadísticas de anomalías"""
    return anomalia_service.get_anomaly_statistics(db)

@router.get("/{anomalia_id}", response_model=AnomaliaResponse)
def get_anomalia(
    anomalia_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtener una anomalía por ID"""
    anomalia = anomalia_service.get_anomalia(db, anomalia_id)
    if not anomalia:
        raise HTTPException(status_code=404, detail="Anomalía no encontrada")
    return anomalia

@router.put("/{anomalia_id}", response_model=AnomaliaResponse)
def update_anomalia(
    anomalia_id: int,
    anomalia_data: AnomaliaUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Actualizar una anomalía"""
    try:
        anomalia = anomalia_service.update_anomalia(db, anomalia_id, anomalia_data)
        if not anomalia:
            raise HTTPException(status_code=404, detail="Anomalía no encontrada")
        return anomalia
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{anomalia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_anomalia(
    anomalia_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Eliminar una anomalía"""
    if not anomalia_service.delete_anomalia(db, anomalia_id):
        raise HTTPException(status_code=404, detail="Anomalía no encontrada")
