#!/usr/bin/env python3
"""
Ejemplo práctico de uso de la nueva estructura refactorizada
"""

def ejemplo_uso_anterior():
    """Ejemplo de cómo se haría en la estructura anterior"""
    print("❌ ESTRUCTURA ANTERIOR - Ejemplo de uso:")
    print("   # Para crear un sensor, necesitabas:")
    print("   from app.repositorios.repositorio_sensores import crear_sensor")
    print("   from app.esquemas.esquema_sensor import SensorCrear")
    print("   from app.base_datos.conexion import SessionLocal")
    print("")
    print("   # Código repetitivo para cada operación:")
    print("   db = SessionLocal()")
    print("   try:")
    print("       sensor = crear_sensor(db, SensorCrear(...))")
    print("       db.commit()")
    print("   finally:")
    print("       db.close()")
    print("")

def ejemplo_uso_nuevo():
    """Ejemplo de cómo se hace en la nueva estructura"""
    print("✅ NUEVA ESTRUCTURA - Ejemplo de uso:")
    print("   # Para crear un sensor, ahora solo necesitas:")
    print("   from core.database import get_db_context")
    print("   from services.sensor_service import sensor_service")
    print("   from schemas.sensor import SensorCreate")
    print("")
    print("   # Código más limpio y simple:")
    print("   with get_db_context() as db:")
    print("       sensor = sensor_service.create_sensor(db, SensorCreate(...))")
    print("")

def ejemplo_api_anterior():
    """Ejemplo de endpoint en estructura anterior"""
    print("❌ ENDPOINT ANTERIOR:")
    print("""
    @router.post("/")
    def crear_sensor(sensor: SensorCrear, db: Session = Depends(get_db)):
        # Lógica duplicada en cada endpoint
        try:
            nuevo_sensor = Sensor(**sensor.dict())
            db.add(nuevo_sensor)
            db.commit()
            db.refresh(nuevo_sensor)
            return nuevo_sensor
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error creando sensor")
    """)

def ejemplo_api_nuevo():
    """Ejemplo de endpoint en nueva estructura"""
    print("✅ ENDPOINT NUEVO:")
    print("""
    @router.post("/", response_model=SensorResponse)
    def create_sensor(
        sensor_data: SensorCreate,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
    ):
        # Lógica centralizada en el servicio
        try:
            return sensor_service.create_sensor(db, sensor_data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    """)

def ejemplo_testing_anterior():
    """Ejemplo de testing anterior"""
    print("❌ TESTING ANTERIOR:")
    print("   # Configuración repetida en cada archivo de test")
    print("   # Múltiples funciones limpiar_bd()")
    print("   # Setup manual de la base de datos")

def ejemplo_testing_nuevo():
    """Ejemplo de testing nuevo"""
    print("✅ TESTING NUEVO:")
    print("   # Fixtures reutilizables en conftest.py")
    print("   def test_create_sensor(client, auth_headers):")
    print("       response = client.post('/api/v1/sensores/', ...)")
    print("       assert response.status_code == 201")

if __name__ == "__main__":
    print("🔄 EJEMPLOS PRÁCTICOS DE USO")
    print("=" * 50)
    
    ejemplo_uso_anterior()
    print()
    ejemplo_uso_nuevo()
    print()
    
    print("🛠️ COMPARACIÓN DE ENDPOINTS:")
    print("-" * 40)
    ejemplo_api_anterior()
    print()
    ejemplo_api_nuevo()
    print()
    
    print("🧪 COMPARACIÓN DE TESTING:")
    print("-" * 40)
    ejemplo_testing_anterior()
    print()
    ejemplo_testing_nuevo()
    print()
    
    print("🎯 CONCLUSIÓN:")
    print("La nueva estructura reduce significativamente el código boilerplate")
    print("y hace el desarrollo más eficiente y mantenible.")
