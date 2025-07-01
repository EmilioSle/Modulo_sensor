#!/usr/bin/env python3
"""
Punto de entrada principal del proyecto, similar al manage.py de Django
"""
import sys
import os
from pathlib import Path

# Agregar el directorio del proyecto al Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Función principal para manejar comandos"""
    if len(sys.argv) < 2:
        print("Comandos disponibles:")
        print("  runserver    - Ejecutar el servidor de desarrollo")
        print("  test         - Ejecutar las pruebas")
        print("  migrate      - Crear/actualizar tablas de base de datos")
        print("  shell        - Abrir shell interactivo")
        return
    
    command = sys.argv[1]
    
    if command == "runserver":
        from core.server import run_server
        run_server()
    elif command == "test":
        from core.testing import run_tests
        run_tests()
    elif command == "migrate":
        from core.database import create_tables
        create_tables()
    elif command == "shell":
        from core.shell import interactive_shell
        interactive_shell()
    else:
        print(f"Comando desconocido: {command}")

if __name__ == "__main__":
    main()
