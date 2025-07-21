# 🐳 Guía de Docker para Servicio de Sensores

Esta guía te explica cómo dockerizar y ejecutar el proyecto usando Docker y Docker Compose.

## 📋 Archivos Docker Creados

- `Dockerfile` - Imagen de la aplicación
- `docker-compose.yml` - Configuración para desarrollo
- `docker-compose.prod.yml` - Configuración para producción
- `docker-entrypoint.sh` - Script de entrada que maneja migraciones
- `.dockerignore` - Archivos excluidos del contexto Docker
- `.env.docker` - Ejemplo de variables de entorno para Docker

## 🚀 Uso Rápido

### 1. Preparación Inicial

```bash
# Clonar el repositorio (si aún no lo tienes)
git clone <tu-repositorio>
cd Modulo_sensor

# Copiar el archivo de variables de entorno
cp .env.docker .env

# Editar las variables si es necesario
nano .env
```

### 2. Desarrollo con Docker Compose

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar todos los servicios
docker-compose down
```

### 3. Acceso a los Servicios

- **API Principal**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Adminer (DB Admin)**: http://localhost:8080
- **Base de datos**: localhost:5432
- **Redis**: localhost:6379

## 🛠️ Comandos Útiles

### Gestión de Contenedores

```bash
# Ver estado de los contenedores
docker-compose ps

# Acceder al shell del contenedor de la aplicación
docker-compose exec app bash

# Ejecutar comandos en la aplicación
docker-compose exec app python manage.py shell
docker-compose exec app python manage.py test

# Ver logs específicos
docker-compose logs app
docker-compose logs db
```

### Base de Datos

```bash
# Acceder a PostgreSQL directamente
docker-compose exec db psql -U sensor_user -d sensor_db

# Hacer backup de la base de datos
docker-compose exec db pg_dump -U sensor_user sensor_db > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U sensor_user -d sensor_db < backup.sql
```

### Desarrollo

```bash
# Reconstruir solo la aplicación
docker-compose build app

# Reiniciar solo la aplicación
docker-compose restart app

# Ver logs en tiempo real
docker-compose logs -f app
```

## 🏗️ Estructura de Docker

### Dockerfile
- Basado en Python 3.11-slim
- Instala dependencias del sistema (PostgreSQL, netcat)
- Crea usuario no-root para seguridad
- Expone puerto 8000
- Punto de entrada configurado para manejar migraciones automáticas

### Docker Compose - Desarrollo
Incluye:
- **app**: Tu aplicación FastAPI
- **db**: PostgreSQL 15
- **redis**: Redis para cache (opcional)
- **adminer**: Interfaz web para administrar la BD

### Docker Compose - Producción
Versión simplificada solo con:
- **app**: Aplicación en modo producción
- **db**: Base de datos (sin puerto expuesto)

## 🔧 Configuración

### Variables de Entorno (.env)

```bash
# Aplicación
DEBUG=true
SECRET_KEY=tu-clave-secreta-segura

# Base de datos
DATABASE_URL=postgresql://sensor_user:sensor_pass@db:5432/sensor_db

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Personalización

1. **Puerto de la aplicación**: Cambiar `8000:8000` in docker-compose.yml
2. **Credenciales de BD**: Modificar variables en docker-compose.yml
3. **Volúmenes**: Para datos persistentes, revisar sección `volumes:`

## 📦 Producción

### Usando docker-compose.prod.yml

```bash
# Construir para producción
docker-compose -f docker-compose.prod.yml build

# Ejecutar en producción
docker-compose -f docker-compose.prod.yml up -d

# Configurar SECRET_KEY
export SECRET_KEY="tu-clave-super-secreta-de-produccion"
docker-compose -f docker-compose.prod.yml up -d
```

### Con Docker puro (sin compose)

```bash
# Construir imagen
docker build -t sensor-app .

# Ejecutar con PostgreSQL externo
docker run -d \
  --name sensor-app \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e SECRET_KEY="tu-clave-secreta" \
  sensor-app
```

## 🧪 Testing

```bash
# Ejecutar tests en el contenedor
docker-compose exec app python manage.py test

# Ejecutar tests específicos
docker-compose exec app python -m pytest tests/test_sensors.py -v

# Con cobertura
docker-compose exec app python -m pytest --cov=. tests/
```

## 🔍 Troubleshooting

### Problemas Comunes

1. **Puerto ya en uso**:
   ```bash
   docker-compose down
   # O cambiar puerto en docker-compose.yml
   ```

2. **Problemas de permisos**:
   ```bash
   sudo chown -R $USER:$USER .
   ```

3. **Base de datos no conecta**:
   ```bash
   docker-compose logs db
   # Verificar que el contenedor de BD esté corriendo
   ```

4. **Limpiar todo y empezar de nuevo**:
   ```bash
   docker-compose down -v --remove-orphans
   docker system prune -a
   docker-compose up --build
   ```

### Logs y Debugging

```bash
# Logs detallados
docker-compose logs -f --tail=100 app

# Acceder al contenedor para debugging
docker-compose exec app bash
cd /app
python manage.py shell
```

## 🎯 Próximos Pasos

1. **CI/CD**: Integrar con GitHub Actions para build/deploy automático
2. **Nginx**: Agregar proxy reverso para producción
3. **SSL**: Configurar HTTPS con Let's Encrypt
4. **Monitoring**: Agregar Prometheus + Grafana
5. **Backups**: Automatizar backups de PostgreSQL

## 📚 Referencias

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Documentation](https://fastapi.tiangolo.com/deployment/docker/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
