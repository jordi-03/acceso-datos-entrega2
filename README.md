Acceso a Datos – Entrega 2.1
Práctica 1 – API REST Sakila

Este repositorio contiene el desarrollo de la Práctica 1 de la asignatura Acceso a Datos, que consiste en la implementación de una API RESTful para interactuar con la base de datos Sakila, centrándose en la gestión de Clientes (Customers) y Alquileres (Rentals).

📌 Descripción del proyecto

La API permite a las aplicaciones cliente realizar operaciones CRUD sobre los clientes y gestionar los alquileres asociados, siguiendo los principios REST y utilizando los métodos HTTP estándar.

El proyecto utiliza FastAPI como framework backend y MySQL (Sakila) como base de datos. Todo el entorno está dockerizado para facilitar su instalación y ejecución.

🧠 Tecnologías utilizadas

Python 3.12

FastAPI

Uvicorn

SQLAlchemy

MySQL 8.0 (Sakila)

Docker

Docker Compose

📦 Dependencias

Las dependencias del proyecto se encuentran en el archivo requirements.txt:

fastapi

uvicorn[standard]

sqlalchemy

pymysql

python-dotenv

📁 Estructura del proyecto
.
├── app/
│   ├── main.py
│   ├── db.py
│   ├── schemas.py
│   └── routers/
│       ├── customers.py
│       └── rentals.py
├── db/
│   └── sakila/
│       ├── sakila-schema.sql
│       └── sakila-data.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

⚙️ Instalación y puesta en marcha
Requisitos previos

Docker instalado

Docker Compose instalado

Puertos disponibles:

8000 → API

3307 → MySQL

8080 → Adminer

Pasos de instalación

Clonar el repositorio:

git clone <url-del-repositorio>
cd acceso-datos-entrega2


Arrancar el proyecto con Docker:

docker compose up -d --build


Comprobar que los contenedores están en ejecución:

docker compose ps

🌐 Acceso a la API
Documentación Swagger (OpenAPI)

La documentación interactiva de la API está disponible en:

http://localhost:8000/docs

Health Check

Endpoint para comprobar el estado del servicio:

GET /health


Respuesta esperada:

{
  "status": "ok"
}

📘 Endpoints disponibles
Customers

POST /api/v1/customers → Crear un cliente

GET /api/v1/customers → Listar clientes

GET /api/v1/customers/{customerId} → Obtener cliente por ID

PUT /api/v1/customers/{customerId} → Actualizar cliente

DELETE /api/v1/customers/{customerId} → Eliminar cliente

Rentals

POST /api/v1/rentals → Crear un alquiler

GET /api/v1/rentals/{rentalId} → Obtener alquiler por ID

PUT /api/v1/rentals/{rentalId}/return → Marcar la devolución

GET /api/v1/customers/{customerId}/rentals → Alquileres por cliente

GET /api/v1/rentals → Listar alquileres

📌 Códigos HTTP utilizados

200 – Operación correcta

201 – Recurso creado

204 – Recurso eliminado

404 – Recurso no encontrado

409 – Conflicto (cliente con alquileres asociados)

422 – Error de validación