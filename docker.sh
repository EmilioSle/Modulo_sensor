#!/bin/bash

# Script de conveniencia para manejar Docker en el proyecto de sensores
# Uso: ./docker.sh [comando]

set -e

COMPOSE_FILE="docker-compose.yml"
PROD_COMPOSE_FILE="docker-compose.prod.yml"

show_help() {
    echo "🐳 Script de Docker para Servicio de Sensores"
    echo ""
    echo "Uso: ./docker.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  up              - Iniciar todos los servicios"
    echo "  down            - Parar todos los servicios"
    echo "  build           - Construir la imagen de la aplicación"
    echo "  logs            - Ver logs de todos los servicios"
    echo "  shell           - Acceder al shell del contenedor de la app"
    echo "  db-shell        - Acceder al shell de PostgreSQL"
    echo "  test            - Ejecutar tests en el contenedor"
    echo "  migrate         - Ejecutar migraciones"
    echo "  clean           - Limpiar contenedores y volúmenes"
    echo "  prod-up         - Iniciar en modo producción"
    echo "  prod-down       - Parar servicios de producción"
    echo "  backup-db       - Hacer backup de la base de datos"
    echo "  restore-db      - Restaurar backup de la base de datos"
    echo "  status          - Ver estado de los contenedores"
    echo ""
    echo "Ejemplos:"
    echo "  ./docker.sh up              # Iniciar en desarrollo"
    echo "  ./docker.sh logs app        # Ver logs solo de la app"
    echo "  ./docker.sh shell           # Entrar al contenedor"
    echo "  ./docker.sh prod-up         # Producción"
}

# Verificar que Docker esté instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker no está instalado"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose no está instalado"
        exit 1
    fi
}

# Verificar que exista el archivo .env
check_env_file() {
    if [ ! -f ".env" ]; then
        echo "⚠️  No existe archivo .env"
        echo "📋 Copiando .env.docker como .env..."
        cp .env.docker .env
        echo "✅ Archivo .env creado. Puedes editarlo si necesitas cambiar configuraciones."
    fi
}

case "${1:-help}" in
    "up")
        check_docker
        check_env_file
        echo "🚀 Iniciando servicios de desarrollo..."
        docker-compose up --build "${@:2}"
        ;;
        
    "down")
        echo "🛑 Parando servicios..."
        docker-compose down "${@:2}"
        ;;
        
    "build")
        echo "🏗️ Construyendo imagen..."
        docker-compose build "${@:2}"
        ;;
        
    "logs")
        docker-compose logs -f "${@:2}"
        ;;
        
    "shell")
        echo "🐚 Accediendo al shell de la aplicación..."
        docker-compose exec app bash
        ;;
        
    "db-shell")
        echo "🗄️ Accediendo a PostgreSQL..."
        docker-compose exec db psql -U sensor_user -d sensor_db
        ;;
        
    "test")
        echo "🧪 Ejecutando tests..."
        docker-compose exec app python manage.py test "${@:2}"
        ;;
        
    "migrate")
        echo "🔄 Ejecutando migraciones..."
        docker-compose exec app python manage.py migrate
        ;;
        
    "clean")
        echo "🧹 Limpiando contenedores, imágenes y volúmenes..."
        docker-compose down -v --remove-orphans
        docker system prune -a -f
        ;;
        
    "prod-up")
        check_docker
        echo "🏭 Iniciando servicios de producción..."
        docker-compose -f $PROD_COMPOSE_FILE up --build -d "${@:2}"
        ;;
        
    "prod-down")
        echo "🛑 Parando servicios de producción..."
        docker-compose -f $PROD_COMPOSE_FILE down "${@:2}"
        ;;
        
    "backup-db")
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        echo "💾 Creando backup: $BACKUP_FILE"
        docker-compose exec db pg_dump -U sensor_user sensor_db > "$BACKUP_FILE"
        echo "✅ Backup creado: $BACKUP_FILE"
        ;;
        
    "restore-db")
        if [ -z "$2" ]; then
            echo "❌ Especifica el archivo de backup: ./docker.sh restore-db backup.sql"
            exit 1
        fi
        echo "📥 Restaurando backup: $2"
        docker-compose exec -T db psql -U sensor_user -d sensor_db < "$2"
        echo "✅ Backup restaurado"
        ;;
        
    "status")
        echo "📊 Estado de los contenedores:"
        docker-compose ps
        ;;
        
    "help"|*)
        show_help
        ;;
esac
