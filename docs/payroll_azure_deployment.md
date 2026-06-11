# Despliegue Azure Payroll

Objetivo: publicar Payroll en Azure usando el mismo entorno general donde ya
vive otra app, sin tocar sus archivos, puertos ni configuraciones.

## Principios

- No reutilizar la carpeta de despliegue de la otra app.
- No compartir archivo `.env` con la otra app.
- No usar `Base.metadata.create_all` en producción.
- No hardcodear credenciales en código ni en frontend.
- Mantener todas las tablas del módulo con prefijo `payroll_`.

## Recomendación de arquitectura

La opción más segura es:

1. Crear una app separada para Payroll.
2. Mantenerla en el mismo App Service Plan si quieres compartir costo.
3. Usar una base `unisan_db` separada dentro de Azure MySQL.
4. Exponer Payroll bajo una ruta dedicada.

Configuración recomendada:

- Frontend Payroll: `/payroll/`
- API Payroll: `/payroll/api/`
- Puerto interno backend si compartes una VM o reverse proxy: `8010`

Si usas Azure App Service Linux, el puerto público lo gestiona Azure y el
proceso debe escuchar en `0.0.0.0:$PORT`. Si compartes una VM propia con otra
app, recomiendo reservar `8010` para Payroll y publicar la ruta `/payroll`
mediante Nginx o IIS reverse proxy.

## Archivos preparados

- Baseline MySQL desde cero:
  `backend/migrations/000_create_payroll_baseline_mysql.sql`
- Startup separado para Payroll:
  `backend/startup_payroll.sh`
- Variables de entorno ejemplo:
  `backend/.env.azure.payroll.example`
- Frontend configurable:
  `frontend/working_ui/config.js`
  `frontend/working_ui/config.example.js`

## Variables de entorno

Definir en Azure App Settings:

```text
PAYROLL_DATABASE_URL
PAYROLL_DB_SSL_CA
PAYROLL_JWT_SECRET
PAYROLL_ACCESS_TOKEN_MINUTES
PAYROLL_CORS_ORIGINS
PAYROLL_BOOTSTRAP_ADMIN_USERNAME
PAYROLL_BOOTSTRAP_ADMIN_PASSWORD
PAYROLL_BOOTSTRAP_ADMIN_NAME
PAYROLL_GUNICORN_WORKERS
PAYROLL_GUNICORN_TIMEOUT
```

Notas:

- `PAYROLL_DATABASE_URL` debe apuntar explícitamente a `/unisan_db`.
- No subir certificados, contraseñas ni secrets a GitHub.
- En producción deja vacíos `PAYROLL_BOOTSTRAP_ADMIN_USERNAME` y
  `PAYROLL_BOOTSTRAP_ADMIN_PASSWORD` si prefieres crear el admin manualmente.

## Frontend

El frontend ya no usa una URL hardcodeada a `127.0.0.1:8010`.

Reglas:

- En local, si no existe configuración, usa `http://127.0.0.1:8010/api`.
- En Azure, puedes publicar `frontend/working_ui/config.js` con:

```javascript
window.__PAYROLL_CONFIG__ = {
    apiBaseUrl: "/payroll/api"
};
```

## Flujo recomendado desde GitHub

### Backend

1. Subir el repositorio a GitHub.
2. Crear una Azure Web App separada para Payroll, por ejemplo:
   `unisan-payroll-api`.
3. Configurar Deployment Center apuntando al repositorio y rama de Payroll.
4. Configurar App Settings con las variables `PAYROLL_*`.
5. Configurar Startup Command:

```text
cd backend && chmod +x startup_payroll.sh && ./startup_payroll.sh
```

6. Instalar dependencias desde `backend/requirements.txt`.

### Frontend

Opciones recomendadas:

1. Publicarlo como sitio estático separado, por ejemplo en Azure Static Web Apps.
2. O publicarlo en la misma infraestructura web existente bajo `/payroll/`,
   copiando sólo `frontend/working_ui`.

No mezclar los archivos del frontend Payroll con la otra app si esa otra app ya
tiene su propio `index.html`, assets o pipeline.

## Creación inicial de base

Como Azure ya quedó vacío para Payroll:

1. Conectarse a `unisan_db` en DBeaver.
2. Ejecutar:

```text
backend/migrations/000_create_payroll_baseline_mysql.sql
```

3. Verificar que existan todas las tablas `payroll_`.
4. Luego crear el admin manualmente:

```bash
cd backend
python manage.py create-admin --username admin --full-name "Administrador"
```

Ese comando no ejecuta `create_all` en MySQL; sólo valida esquema y crea el
usuario.

## Validación posterior

Checklist mínimo:

1. `GET /api/health` responde `ok`.
2. Login con admin funciona.
3. `GET /api/cycles` responde.
4. `GET /api/workers` responde.
5. `GET /api/rates` responde.
6. El frontend carga bajo `/payroll/` y consume `/payroll/api`.

## Qué no hacer

- No publicar Payroll encima del directorio de despliegue de la otra app.
- No compartir secrets entre ambas apps.
- No usar `create_all` contra Azure.
- No volver a usar URLs hardcodeadas de localhost en frontend.
