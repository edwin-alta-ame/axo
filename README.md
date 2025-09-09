
# Documentación de la API-REST

Este proyecto es una API-REST desarrollada con Python y Flask-RESTful, diseñada para la gestión de usuarios, incluyendo registro, inicio de sesión y validación de tokens. La API se conecta a una base de datos PostgreSQL y utiliza JWT (JSON Web Tokens) para la autenticación.

## Requisitos del Sistema

*   Docker
*   Docker Compose

## Configuración y Despliegue

La forma más sencilla de ejecutar el proyecto es usando Docker Compose, ya que gestiona todas las dependencias y servicios.

### 1\. Variables de Entorno

Antes de ejecutar la aplicación, debes configurar tus credenciales de base de datos en el archivo `.env`.

```
HOST=tu_host_de_postgresql
USER=tu_usuario_de_bd
PASS=tu_contraseña_de_bd
DB=tu_nombre_de_bd
PORT=tu_puerto_de_bd
```

**Nota:** Asegúrate de que tu base de datos esté accesible.

### 2\. Base de Datos (PostgreSQL)

Para inicializar la base de datos con las tablas requeridas, ejecuta el script SQL en tu cliente de PostgreSQL que viene en la carpeta raiz.

### 3\. Estructura del Proyecto

El proyecto está organizado en módulos para mantener la lógica separada y reutilizable:

```
.
├── app.py              # Archivo principal de la aplicación Flask
├── api_files/          # Endpoints de la API
│   ├── signup.py       # Lógica para el registro de usuarios
│   ├── login.py        # Lógica para el inicio de sesión
│   └── getuser.py      # Lógica para obtener un usuario por nombre o correo
├── junglebranchs/      # Módulos de funciones reutilizables
│   ├── dbpg.py         # Módulo para la interacción con PostgreSQL
│   └── token.py        # Módulo para la gestión y validación de tokens JWT
├── configs.py          # Archivo de configuración global
├── compose.yaml        # Archivo de configuración para Docker Compose
├── Dockerfile          # Instrucciones para construir la imagen de Docker
├── requirements.txt    # Dependencias de Python
└── .env                # Variables de entorno
```

### 4\. Ejecución del Proyecto

Para iniciar la aplicación, ejecuta el siguiente comando en la terminal desde el directorio raíz del proyecto:

```
docker-compose up --build
```

Esto construirá la imagen de Docker, instalará las dependencias y levantará el servidor web en el puerto `8000`. La API estará accesible en `http://localhost:8000`.

## Endpoints de la API

### 1\. Registro de Usuario (`/api/signup`)

*   **Método:** `POST`
*   **Descripción:** Crea una nueva cuenta de usuario en la base de datos. La contraseña se hashea con SHA-256 antes de ser almacenada.
*   **Cuerpo de la Solicitud (JSON):**
    
    ```
    {
        "nombre": "string",
        "email": "string",
        "contrasena": "string",
        "rol_id": "string"
    }
    ```
    
*   **Ejemplo de Petición (cURL):**
    
    ```
    curl -X POST http://localhost:8000/api/signup -H "Content-Type: application/json" -d '{"nombre": "Jane Doe", "email": "jane@example.com", "contrasena": "securepass123", "rol_id": "1"}'
    ```
    
*   **Respuestas:**
    *   `200 OK`: `{"TOKEN": "..."}` (Devuelve un JWT si el registro es exitoso).
    *   `200 OK`: `{"_error": "USUARIO_EMAIL_EXISTE"}` (Si el email ya está en uso).
    *   `500 Internal Server Error`: Errores de la base de datos.

### 2\. Inicio de Sesión (`/api/login`)

*   **Método:** `POST`
*   **Descripción:** Autentica a un usuario. Si las credenciales son correctas, devuelve un JWT.
*   **Cuerpo de la Solicitud (JSON):**
    
    ```
    {
        "email": "string",
        "contrasena": "string"
    }
    ```
    
*   **Ejemplo de Petición (cURL):**
    
    ```
    curl -X POST http://localhost:8000/api/login -H "Content-Type: application/json" -d '{"email": "jane@example.com", "contrasena": "securepass123"}'
    ```
    
*   **Respuestas:**
    *   `200 OK`: `{"TOKEN": "..."}` (Devuelve un JWT si las credenciales son válidas).
    *   `200 OK`: `{"_error": "DATOS_INCORRECTOS"}` (Si el email o la contraseña no coinciden).

### 3\. Obtener Usuario (`/api/getuser`)

*   **Método:** `GET`
*   **Descripción:** Un endpoint protegido que busca un usuario por su nombre o correo electrónico.
*   **Parámetros de la URL (Query):**
    *   `value`: El nombre o email del usuario a buscar.
*   **Encabezados de la Petición:**
    *   `ApiKeyAuth`: El token JWT del usuario autenticado.
*   **Ejemplo de Petición (cURL):**
    
    ```
    # Reemplaza 'tu_token_jwt' y 'nombre_o_email'
    curl -X GET "http://localhost:8000/api/getuser?value=juan@example.com" -H "ApiKeyAuth: tu_token_jwt"
    ```
    
*   **Respuestas:**
    *   `200 OK`: `{ "id": 1, "email": "..." }` (Si se encuentra el usuario).
    *   `200 OK`: `{"ERROR": "NOT_FOUND"}` (Si no se encuentra el usuario).
    *   `200 OK`: `{"ERROR": "INVALID_TOKEN"}` (Si el token es inválido o no está presente).
