"""
Configuración de la base de datos centralizada
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
import logging

from core.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Base declarativa para todos los modelos
Base = declarative_base()

# Engine de SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Muestra queries SQL si DEBUG=True
    pool_pre_ping=True,   # Verifica conexiones
    pool_recycle=3600     # Recicla conexiones cada hora
)

# Sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependencia para obtener sesión de base de datos
    Uso: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager para uso fuera de FastAPI
    Uso: 
    with get_db_context() as db:
        # usar db aquí
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Crea todas las tablas en la base de datos"""
    logger.info("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas exitosamente")

def drop_tables():
    """Elimina todas las tablas (útil para pruebas)"""
    logger.warning("Eliminando todas las tablas...")
    Base.metadata.drop_all(bind=engine)
    logger.info("Tablas eliminadas")

class DatabaseManager:
    """Manager para operaciones de base de datos"""
    
    @staticmethod
    def reset_database():
        """Resetea la base de datos (drop + create)"""
        drop_tables()
        create_tables()
    
    @staticmethod
    def check_connection() -> bool:
        """Verifica la conexión a la base de datos"""
        try:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Error conectando a la base de datos: {e}")
            return False
