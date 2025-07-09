"""
Configuraciones centralizadas del proyecto, compatible con Python 3.x
"""
import os
from pathlib import Path
from typing import List, Optional

# Verificar si tenemos Pydantic v2 o v1
try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
    PYDANTIC_V2 = True
except ImportError:
    try:
        from pydantic import BaseSettings, Field
        PYDANTIC_V2 = False
    except ImportError:
        # Fallback sin Pydantic
        class BaseSettings:
            pass
        def Field(default=None, env=None):
            return default
        PYDANTIC_V2 = False

from dotenv import load_dotenv

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Cargar variables de entorno
load_dotenv(BASE_DIR / ".env")

class Settings(BaseSettings):
    """Configuraciones del proyecto"""
    
    # Configuración de la aplicación
    APP_NAME: str = "Servicio de Sensores Mundo Verde"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    TEST_DATABASE_URL: Optional[str] = os.getenv("TEST_DATABASE_URL")
    
    # Seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOWED_METHODS: List[str] = ["*"] 
    ALLOWED_HEADERS: List[str] = ["*"]
    
    # Usuario demo (en producción esto debe venir de BD)
    DEMO_USERNAME: str = os.getenv("DEMO_USERNAME", "admin")
    DEMO_PASSWORD: str = os.getenv("DEMO_PASSWORD", "admin123")
    
    def __init__(self):
        # Para compatibilidad con versiones de Pydantic
        super().__init__()

# Configuraciones específicas para diferentes entornos
class DevelopmentSettings(Settings):
    DEBUG: bool = True

class TestingSettings(Settings):
    DATABASE_URL: str = "sqlite:///./test.db"
    DEBUG: bool = True
    
class ProductionSettings(Settings):
    DEBUG: bool = False
    ALLOWED_ORIGINS: List[str] = ["https://tu-dominio.com"]

def get_settings() -> Settings:
    """Obtiene las configuraciones según el entorno"""
    env = os.getenv("ENV", "development").lower()
    
    if env == "testing":
        return TestingSettings()
    elif env == "production":
        return ProductionSettings()
    else:
        return DevelopmentSettings()
