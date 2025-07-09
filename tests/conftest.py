"""
Configuración de pruebas
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os

from core.app import create_app
from core.database import Base
from core.settings import get_settings

# Importar todos los modelos para que se registren en Base
from models.sensor import Sensor
from models.lectura import Lectura
from models.ubicacion import Ubicacion
from models.anomalia import Anomalia
from models.prediccion import PrediccionSequia

# Configurar entorno de testing
os.environ["ENV"] = "testing"
settings = get_settings()

# Engine de testing (SQLite en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def app():
    """Fixture de la aplicación FastAPI"""
    from core.database import get_db
    
    # Crear tablas en SQLite en memoria
    Base.metadata.create_all(bind=test_engine)
    
    def override_get_db():
        """Override para la BD de testing"""
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    return app

@pytest.fixture(scope="session")
def client(app):
    """Cliente de testing"""
    return TestClient(app)

@pytest.fixture
def db():
    """Fixture de base de datos para testing"""
    # Las tablas ya están creadas en el fixture de sesión
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def auth_headers(client):
    """Fixture para headers de autenticación"""
    response = client.post("/auth/login", data={
        "username": settings.DEMO_USERNAME,
        "password": settings.DEMO_PASSWORD
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
