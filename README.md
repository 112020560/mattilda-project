# Mattilda prueba técnica

Una API REST desarrollada con FastAPI, containerizada con Docker y orquestada con Docker Compose.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Endpoints](#api-endpoints)
- [Variables de Entorno](#variables-de-entorno)
- [Desarrollo](#desarrollo)
- [Pruebas](#pruebas)
- [Despliegue](#despliegue)
- [Contribuir](#contribuir)

## ✨ Características

- API REST con FastAPI
- Documentación automática con Swagger/OpenAPI
- Containerización con Docker
- Orquestación con Docker Compose
- Base de datos con PostgreSQL
- Autenticación y autorización (si aplica)
- Validación de datos con Pydantic
- Logging estructurado
- Health checks

## 🛠 Tecnologías

- **FastAPI** - Framework web moderno para Python
- **Docker** - Containerización
- **Docker Compose** - Orquestación de contenedores
- **Python 3.11+** - Lenguaje de programación
- **PostgreSQL** - Base de datos 
- **Redis** - Cache

## 📋 Requisitos Previos

- Docker >= 20.10
- Docker Compose >= 2.0
- Python 3.11+ (para desarrollo local)
- Git

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/112020560/mattilda-project.git
cd mattilda-project
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus configuraciones:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@db:5432/dbname
DATABASE_URL_ASYNC=postgresql+asyncpg://user:password@db:5432/dbname

# App Configuration
APP_NAME=Mattilda API
DEBUG=true
VERSION=1.0.0

# Security
SECRET_KEY=your-very-secret-key-change-in-production

# Redis (opcional para cache)
REDIS_URL=redis://localhost:6379/0
```

### 3. Construir y levantar los servicios

```bash
# Construcción y inicio
docker-compose up --build -d

# Solo inicio (si ya están construidas las imágenes)
docker-compose up -d
```

### 4. Verificar que todo funcione

```bash
# Ver logs
docker-compose logs -f

# Verificar servicios corriendo
docker-compose ps
```

La API estará disponible en:
- **Aplicación**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 💻 Uso

### Acceder a la documentación

Visita `http://localhost:8000/docs` para ver la documentación interactiva de Swagger.

### Endpoints principales

```bash
# Health check
curl http://localhost:8000/health

# Ejemplo de endpoint (cambiar según tu API)
curl http://localhost:8000/api/v1/items
```

### Comandos útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Acceder al contenedor de la API
docker-compose exec api bash

# Reiniciar un servicio específico
docker-compose restart api

# Parar todos los servicios
docker-compose down

# Parar y eliminar volúmenes
docker-compose down -v
```

## 📁 Estructura del Proyecto

```
mattilda-project/
├── app/
│   ├── domain/          # Core business logic
│   │   ├── models/
│   │   └── services/
│   ├── infrastructure/  # External adapters
│   │   ├── database/
│   │   ├── repositories/
│   │   └── config/
│   ├── api/            # FastAPI adapters
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── dependencies/
│   └── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt        # Dependencias Python
├── .env.example           # Variables de entorno ejemplo
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

### Sistema General
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/` | Endpoint raíz |
| GET | `/docs` | Documentación Swagger UI |
| GET | `/redoc` | Documentación ReDoc |

### 🏫 Escuelas (Schools)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/schools/` | Crear nueva escuela |
| GET | `/api/v1/schools/` | Listar escuelas con paginación |
| GET | `/api/v1/schools/{school_id}` | Obtener escuela por ID |
| PUT | `/api/v1/schools/{school_id}` | Actualizar escuela |
| DELETE | `/api/v1/schools/{school_id}` | Eliminar escuela |
| PATCH | `/api/v1/schools/{school_id}/deactivate` | Desactivar escuela |
| GET | `/api/v1/schools/search/` | Buscar escuelas por nombre |
| GET | `/api/v1/schools/{school_id}/statistics` | Obtener estadísticas de la escuela |

### 👨‍🎓 Estudiantes (Students)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/students/` | Crear nuevo estudiante |
| GET | `/api/v1/students/` | Listar estudiantes con paginación |
| GET | `/api/v1/students/{student_id}` | Obtener estudiante por ID |
| PUT | `/api/v1/students/{student_id}` | Actualizar estudiante |
| DELETE | `/api/v1/students/{student_id}` | Eliminar estudiante |
| GET | `/api/v1/students/by-student-id/{student_id}` | Obtener estudiante por Student ID |
| GET | `/api/v1/students/school/{school_id}` | Obtener estudiantes por escuela |
| PATCH | `/api/v1/students/{student_id}/deactivate` | Desactivar estudiante |
| GET | `/api/v1/students/search/` | Buscar estudiantes por nombre |
| PATCH | `/api/v1/students/{student_id}/transfer` | Transferir estudiante a otra escuela |

### 🧾 Facturas (Invoices)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/invoices/` | Crear nueva factura |
| GET | `/api/v1/invoices/` | Listar facturas con paginación |
| GET | `/api/v1/invoices/{invoice_id}` | Obtener factura por ID |
| PUT | `/api/v1/invoices/{invoice_id}` | Actualizar factura |
| DELETE | `/api/v1/invoices/{invoice_id}` | Eliminar factura |
| GET | `/api/v1/invoices/by-number/{invoice_number}` | Obtener factura por número |
| GET | `/api/v1/invoices/student/{student_id}` | Obtener facturas por estudiante |
| GET | `/api/v1/invoices/school/{school_id}` | Obtener facturas por escuela |
| GET | `/api/v1/invoices/status/{status}` | Obtener facturas por estado |
| GET | `/api/v1/invoices/overdue/list` | Obtener facturas vencidas |
| PATCH | `/api/v1/invoices/{invoice_id}/mark-paid` | Marcar factura como pagada |
| PATCH | `/api/v1/invoices/{invoice_id}/cancel` | Cancelar factura |

### 💳 Pagos (Payments)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/payments/` | Crear nuevo pago |
| GET | `/api/v1/payments/` | Listar pagos con paginación |
| GET | `/api/v1/payments/{payment_id}` | Obtener pago por ID |
| PUT | `/api/v1/payments/{payment_id}` | Actualizar pago |
| DELETE | `/api/v1/payments/{payment_id}` | Eliminar pago |
| GET | `/api/v1/payments/invoice/{invoice_id}` | Obtener pagos por factura |
| GET | `/api/v1/payments/student/{student_id}` | Obtener pagos por estudiante |
| PATCH | `/api/v1/payments/{payment_id}/confirm` | Confirmar pago |
| PATCH | `/api/v1/payments/{payment_id}/reject` | Rechazar pago |

### 📊 Estados de Cuenta (Account Statements)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/account-statements/student/{student_id}` | Estado de cuenta del estudiante |
| GET | `/api/v1/account-statements/school/{school_id}` | Estado de cuenta del colegio |

### Parámetros de Consulta Comunes
- `skip` (integer): Número de registros a omitir (paginación)
- `limit` (integer): Límite de registros por página (máx. 1000)
- `active_only` (boolean): Filtrar solo registros activos
- `name` (string): Búsqueda por nombre
- `school_id` (integer): Filtrar por escuela específica

## ⚙️ Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a la base de datos | - |
| `DATABASE_URL_ASYNC` | URL de conexión a la base de datos | - |
| `SECRET_KEY` | Clave secreta para JWT | - |
| `ENVIRONMENT` | Entorno de ejecución | `development` |
| `DEBUG` | Modo debug | `False` |
| `APP_NAME` | Nombre de la aplicacion | `Mattilda API` |
| `CORS_ORIGINS` | Orígenes permitidos para CORS | `["*"]` | 
| `VERSION` | Version de la aplicación | `1.0.0` | 

## 🔧 Desarrollo

### Desarrollo local sin Docker

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Agregar nuevas dependencias

```bash
# Agregar al requirements.txt y reconstruir
docker-compose build api
docker-compose up -d
```

### Migraciones de base de datos

```bash
# Si usas Alembic
docker-compose exec api alembic revision --autogenerate -m "Descripción del cambio"
docker-compose exec api alembic upgrade head
```

## 🧪 Pruebas

```bash
# Ejecutar pruebas dentro del contenedor
docker-compose exec api pytest

# Ejecutar con cobertura
docker-compose exec api pytest --cov=app tests/

# Ejecutar pruebas específicas
docker-compose exec api pytest tests/test_main.py::test_read_main
```

## 🚀 Despliegue

### Producción con Docker

1. Configurar variables de entorno para producción
2. Usar `docker-compose.prod.yml` si tienes uno específico para producción
3. Configurar proxy reverso (Nginx, Traefik, etc.)
4. Configurar SSL/TLS

```bash
# Ejemplo para producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Consideraciones de seguridad

- Cambiar todas las claves por defecto
- Usar secretos de Docker para información sensible
- Configurar rate limiting
- Implementar logging y monitoreo
- Mantener dependencias actualizadas

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- Felipe Alpizar - *Desarrollo inicial* - [112020560](https://github.com/112020560)

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- La comunidad de Python
- Contribuidores del proyecto