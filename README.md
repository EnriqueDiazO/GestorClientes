
# Gestión de Clientes — Plataforma Web (FastAPI)

Tres roles:
- **Cliente**: registra datos y sube archivos.
- **Administrador 1**: consulta reportes individuales.
- **Administrador 2**: ve dashboard y estadísticas agregadas.

## Rápido inicio (modo simple, SQLite)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.db_init   # crea DB y usuarios demo

```
## Opción 1 
```bash
# para visualizar la interfaz gráfica
uvicorn app.main_with_ui:app --reload
```
Abrir: <http://127.0.0.1:8000>

## Opción 2
```bash
# para visualizar los endpoints
uvicorn app.main:app --reload
```
Abrir: <http://127.0.0.1:8000/docs>

### Usuarios demo
- admin2@example.com / admin2 (rol: ADMIN_2)
- admin1@example.com / admin1 (rol: ADMIN_1)
- cliente@example.com / cliente (rol: CLIENTE)

## Producción con Postgres + Docker
```bash
docker compose up -d --build
```

## Estructura
- `app/models.py` — modelos SQLModel (User, Role, Client, Document).
- `app/auth.py` — JWT + dependencias de rol.
- `app/routers/*` — endpoints por dominio.
- `app/services/*` — lógica de negocio.
- `app/templates/*` — vistas simples (opcional).
- `app/db_init.py` — crea tablas y usuarios de ejemplo.
- `alembic/` — migraciones (opcional).
