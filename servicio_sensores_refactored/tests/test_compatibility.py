"""
Test simplificado para verificar compatibilidad Python 3.x
"""
import pytest
import sys

def test_python_version():
    """Verificar versión de Python"""
    print(f"Python version: {sys.version}")
    assert sys.version_info.major >= 3

def test_pydantic_compatibility():
    """Verificar compatibilidad de Pydantic"""
    try:
        from pydantic import BaseModel
        
        class TestSchema(BaseModel):
            name: str
            age: int
            
        # Probar ambos métodos
        data = TestSchema(name="Test", age=25)
        
        # Método dict() (v1 y v2)
        dict_data = data.dict() if hasattr(data, 'dict') else data.model_dump()
        assert dict_data == {"name": "Test", "age": 25}
        
        print("✅ Pydantic funciona correctamente")
        
    except Exception as e:
        pytest.fail(f"Error con Pydantic: {e}")

def test_sqlalchemy_compatibility():
    """Verificar compatibilidad de SQLAlchemy"""
    try:
        from sqlalchemy import Column, Integer, String, create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        
        Base = declarative_base()
        
        class TestModel(Base):
            __tablename__ = "test"
            id = Column(Integer, primary_key=True)
            name = Column(String)
        
        # Crear engine en memoria
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        # Crear registro
        obj = TestModel(name="test")
        session.add(obj)
        session.commit()
        
        # Verificar
        result = session.query(TestModel).first()
        assert result.name == "test"
        
        session.close()
        print("✅ SQLAlchemy funciona correctamente")
        
    except Exception as e:
        pytest.fail(f"Error con SQLAlchemy: {e}")

def test_settings_loading():
    """Verificar carga de settings"""
    try:
        from core.settings import get_settings
        settings = get_settings()
        
        assert hasattr(settings, 'DATABASE_URL')
        assert hasattr(settings, 'DEMO_USERNAME')
        
        print(f"✅ Settings cargados: DB={settings.DATABASE_URL}")
        
    except Exception as e:
        pytest.fail(f"Error cargando settings: {e}")
