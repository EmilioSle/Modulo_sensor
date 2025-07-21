#!/bin/bash
set -e

# Función para esperar por la base de datos
wait_for_db() {
    echo "Esperando por la base de datos..."
    
    # Si estamos usando PostgreSQL, esperar por la conexión
    if [[ $DATABASE_URL == *"postgresql"* ]]; then
        host=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
        port=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        
        until nc -z $host $port; do
            echo "Base de datos no disponible - esperando..."
            sleep 1
        done
        
        echo "Base de datos disponible!"
    fi
}

# Si el comando es runserver, hacer las migraciones primero
if [ "$1" = "runserver" ]; then
    wait_for_db
    
    echo "Ejecutando migraciones..."
    python manage.py migrate
    
    echo "Iniciando servidor..."
    exec python manage.py runserver
fi

# Si es otro comando, ejecutarlo directamente
exec python manage.py "$@"
