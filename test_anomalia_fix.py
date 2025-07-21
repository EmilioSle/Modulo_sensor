#!/usr/bin/env python3
"""
Script de prueba para verificar la corrección del problema de anomalías
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_db, SessionLocal
from services.anomalia_service import anomalia_service
from services.lectura_service import lectura_service
from services.sensor_service import sensor_service
from schemas.anomalia import AnomaliaCreate
from schemas.lectura import LecturaCreate
from schemas.sensor import SensorCreate
import traceback

def main():
    """Función principal de prueba"""
    db = SessionLocal()
    
    try:
        print("🔍 Iniciando pruebas de anomalía...")
        
        # Primero crear un sensor de prueba
        print("\n1. Creando sensor de prueba...")
        sensor_data = SensorCreate(
            tipo="temperatura",
            modelo="DS18B20",
            descripcion="Sensor de prueba para anomalía"
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
        
        # Crear lectura de prueba
        print("\n2. Creando lectura de prueba...")
        lectura_data = LecturaCreate(
            sensor_id=sensor.id,
            temperatura=45.5,  # Temperatura alta para generar anomalía
            humedad=85.0
        )
        
        try:
            lectura = lectura_service.create_lectura(db, lectura_data)
            print(f"✅ Lectura creada con ID: {lectura.id}")
        except Exception as e:
            print(f"❌ Error creando lectura: {e}")
            # Buscar una lectura existente
            lecturas = lectura_service.get_all_lecturas(db, limit=1)
            if lecturas:
                lectura = lecturas[0]
                print(f"🔄 Usando lectura existente con ID: {lectura.id}")
            else:
                print("❌ No hay lecturas disponibles para prueba")
                return
        
        # Crear anomalía de prueba
        print("\n3. Creando anomalía de prueba...")
        anomalia_data = AnomaliaCreate(
            lectura_id=lectura.id,
            tipo="temperatura_alta",
            valor=45.5
        )
        
        anomalia = anomalia_service.create_anomalia(db, anomalia_data)
        print(f"✅ Anomalía creada exitosamente:")
        print(f"   - ID: {anomalia.id}")
        print(f"   - Lectura ID: {anomalia.lectura_id}")
        print(f"   - Tipo: {anomalia.tipo}")
        print(f"   - Valor: {anomalia.valor}")
        
        # Probar obtener anomalía
        print("\n4. Probando obtener anomalía...")
        anomalia_obtenida = anomalia_service.get_anomalia(db, anomalia.id)
        if anomalia_obtenida:
            print(f"✅ Anomalía obtenida correctamente: ID {anomalia_obtenida.id}")
        else:
            print("❌ No se pudo obtener la anomalía")
        
        # Probar detección automática
        print("\n5. Probando detección automática de anomalías...")
        anomalias_detectadas = anomalia_service.detect_anomalies_in_reading(db, lectura.id)
        print(f"✅ Detectadas {len(anomalias_detectadas)} anomalías automáticamente")
        for i, anom in enumerate(anomalias_detectadas):
            print(f"   {i+1}. Tipo: {anom.tipo}, Valor: {anom.valor}")
        
        print("\n🎉 Todas las pruebas de anomalías pasaron exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        print("Traceback completo:")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
