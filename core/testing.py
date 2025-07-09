"""
Herramientas para testing
"""
import pytest
from core.database import engine, Base
import os

def run_tests():
    """Ejecutar las pruebas del proyecto"""
    # Configurar entorno de testing
    os.environ["ENV"] = "testing"
    
    # Ejecutar pytest
    exit_code = pytest.main([
        "tests/",
        "-v",
        "--tb=short",
        "--disable-warnings"
    ])
    
    return exit_code
