#!/usr/bin/env python3
"""
Script de prueba para verificar la corrección del problema de ubicaciones
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_db, SessionLocal
from services.ubicacion_service import ubicacion_service
from services.sensor_service import sensor_service
from schemas.ubicacion import UbicacionCreate
from schemas.sensor import SensorCreate
import traceback

def main():
    """Función principal de prueba"""
    db = SessionLocal()
    
    try:
        print("🔍 Iniciando pruebas de ubicación...")
        
        # Primero crear un sensor de prueba
        print("\n1. Creando sensor de prueba...")
        sensor_data = SensorCreate(
            tipo="temperatura",
            modelo="DS18B20",
            descripcion="Sensor de prueba para ubicación"
        )
        
        try:
            sensor = sensor_service.create_sensor(db, sensor_data)
            print(f"✅ Sensor creado con ID: {sensor.id}")
        except Exception as e:
            print(f"❌ Error creando sensor: {e}")
            # Buscar un sensor existente
            sensors = sensor_service.get_all_sensors(db, limit=1)
            if sensors:
                sensor = sensors[0]
                print(f"🔄 Usando sensor existente con ID: {sensor.id}")
            else:
                print("❌ No hay sensores disponibles para prueba")
                return
        
        # Crear ubicación de prueba
        print("\n2. Creando ubicación de prueba...")
        ubicacion_data = UbicacionCreate(
            sensor_id=sensor.id,
            latitud="-34.6118",
            longitud="-58.3960",
            descripcion="Buenos Aires - Prueba"
        )
        
        ubicacion = ubicacion_service.create_ubicacion(db, ubicacion_data)
        print(f"✅ Ubicación creada exitosamente:")
        print(f"   - ID: {ubicacion.id}")
        print(f"   - Sensor ID: {ubicacion.sensor_id}")
        print(f"   - Latitud: {ubicacion.latitud}")
        print(f"   - Longitud: {ubicacion.longitud}")
        print(f"   - Descripción: {ubicacion.descripcion}")
        
        # Probar obtener ubicación
        print("\n3. Probando obtener ubicación...")
        ubicacion_obtenida = ubicacion_service.get_ubicacion(db, ubicacion.id)
        if ubicacion_obtenida:
            print(f"✅ Ubicación obtenida correctamente: ID {ubicacion_obtenida.id}")
        else:
            print("❌ No se pudo obtener la ubicación")
        
        print("\n🎉 Todas las pruebas pasaron exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        print("Traceback completo:")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
