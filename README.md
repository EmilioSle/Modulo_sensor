# 🌱 Servicio de Sensores Refactorizado - Mundo Verde

Proyecto refactorizado con una estructura más limpia y organizada, siguiendo mejores prácticas de desarrollo.

## 🏗️ Nueva Estructura del Proyecto

```
servicio_sensores_refactored/
├── manage.py                    # Punto de entrada principal (como Django)
├── requirements.txt             # Dependencias
├── .env.example                 # Ejemplo de variables de entorno
├── .gitignore
│
├── core/                        # Configuraciones centrales
│   ├── __init__.py
│   ├── settings.py              # Configuración centralizada
│   ├── database.py              # Configuración de BD
│   ├── app.py                   # Aplicación FastAPI
│   ├── server.py                # Servidor de desarrollo
│   ├── testing.py               # Herramientas de testing
│   └── shell.py                 # Shell interactivo
│
├── models/                      # Modelos de datos (SQLAlchemy)
│   ├── __init__.py
│   ├── base.py                  # Modelos base y mixins
│   ├── sensor.py
│   ├── lectura.py
│   ├── ubicacion.py
│   ├── anomalia.py
│   └── prediccion.py
│
├── schemas/                     # Esquemas Pydantic
│   ├── __init__.py
│   ├── base.py                  # Esquemas base
│   ├── sensor.py
│   ├── lectura.py
│   ├── auth.py
│   └── ...
│
├── repositories/                # Capa de acceso a datos
│   ├── __init__.py
│   ├── base.py                  # Repositorio CRUD genérico
│   ├── sensor_repository.py
│   ├── lectura_repository.py
│   └── ...
│
├── services/                    # Lógica de negocio
│   ├── __init__.py
│   ├── sensor_service.py
│   ├── lectura_service.py
│   └── ...
│
├── api/                         # Endpoints de la API
│   └── v1/
│       ├── __init__.py
│       ├── router.py            # Router principal
│       ├── sensors.py
│       ├── readings.py
│       └── ...
│
├── auth/                        # Sistema de autenticación
│   ├── __init__.py
│   ├── security.py              # JWT y autenticación
│   └── router.py                # Endpoints de auth
│
└── tests/                       # Pruebas
    ├── __init__.py
    ├── conftest.py
    ├── test_sensors.py
    └── ...
```

## 🚀 Uso del Sistema

### 1. Instalación
```bash
# Clonar y entrar al directorio
cd servicio_sensores_refactored

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

### 2. Comandos Principales (estilo Django)
```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Crear/actualizar tablas de base de datos
python manage.py migrate

# Ejecutar pruebas
python manage.py test

# Abrir shell interactivo
python manage.py shell
```

### 3. Uso con Docker 🐳
```bash
# Ejecutar con Docker Compose (recomendado)
docker-compose up --build

# Acceso a servicios:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs  
# - Adminer: http://localhost:8080

# Ver documentación completa de Docker
cat DOCKER.md
```

### URL: 
```http://127.0.0.1:8000/docs#/```


## 📈 Mejoras Implementadas

### ✅ Eliminación de Duplicación
- **Un solo repositorio CRUD genérico** en lugar de repetir código
- **Servicios reutilizables** con lógica de negocio centralizada
- **Configuración unificada** en lugar de múltiples archivos de config

### ✅ Estructura Clara y Organizada
- **Separación de responsabilidades** clara (MVC-style)
- **Modelos base** con mixins reutilizables (timestamps, etc.)
- **Esquemas Pydantic** organizados y consistentes

### ✅ Mejor Manejo de Errores
- **Validaciones centralizadas** en servicios
- **Logging estructurado**
- **Manejo consistente de excepciones**

### ✅ Configuración Centralizada
- **Un solo archivo de settings** con diferentes entornos
- **Variables de entorno** manejadas correctamente
- **Configuración flexible** por environment

### ✅ Testing Mejorado
- **Fixtures reutilizables**
- **Base de datos de testing** separada
- **Comandos simplificados**

## 🔧 Ventajas de la Nueva Estructura

1. **Mantenibilidad**: Código más organizado y fácil de mantener
2. **Escalabilidad**: Fácil agregar nuevos módulos siguiendo el patrón
3. **Testabilidad**: Estructura clara para pruebas
4. **Reutilización**: Componentes reutilizables (repositorio base, servicios)
5. **Consistencia**: Patrones consistentes en todo el proyecto

## 🛠️ Migración desde la Estructura Anterior

Los datos y funcionalidad se mantienen igual, solo cambió la organización:

- **Controladores** → **api/v1/**
- **Repositorios específicos** → **Repositorio CRUD genérico + métodos específicos**
- **Casos de uso** → **Services con lógica de negocio**
- **Esquemas dispersos** → **schemas/ organizados**
- **Configuración dispersa** → **core/settings.py**

## 📚 Próximos Pasos

1. Migrar ubicaciones, anomalías y predicciones a la nueva estructura
2. Implementar migraciones de base de datos (Alembic)
3. Agregar más validaciones de negocio
4. Implementar cache (Redis)
5. Documentación automática mejorada
