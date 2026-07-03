# CLAUDE.md — SENAMECF

Contexto para Claude Code. Este archivo documenta cómo está construido el proyecto y sus convenciones. **Mantenerlo actualizado a medida que el proyecto evolucione.**

## Qué es este proyecto

Sistema de Bienestar Social del SENAMECF (Servicio Nacional de Medicina y Ciencias Forenses, Venezuela) para automatizar la gestión de **Talento Humano** y **Servicios Médicos**. Proyecto de equipo (6 integrantes); el trabajo asignado a Geremy Viso es el **módulo de Empleados**.

Módulos del sistema: Seguridad (login/roles/usuarios), Empleados, Especializaciones Médicas, Especialistas, Citas Médicas.

## Stack

- **Python 3.13+ / Flask 3.1** — app factory + un solo blueprint
- **Flask-SQLAlchemy 3.1 / SQLAlchemy 2.0** — ORM
- **Flask-Migrate 4.1 (Alembic)** — migraciones en `migrations/`
- **PostgreSQL** (driver `psycopg2-binary`)
- **Jinja2** — plantillas renderizadas en servidor, sin JavaScript ni framework de frontend
- **python-dotenv** — configuración vía `.env` (no versionado): `SECRET_KEY`, `DATABASE_URL`

## Cómo ejecutar

```bash
source venv/bin/activate   # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
python run.py              # levanta Flask en modo debug, puerto 5000
```

Migraciones: `flask db migrate -m "mensaje"` y `flask db upgrade` (requiere `FLASK_APP=run.py`).

## Estructura

```
SENAMECF/
├── app/
│   ├── __init__.py      # create_app(): factory, registra db, migrate y blueprint "main"
│   ├── models.py        # TODOS los modelos en un solo archivo
│   ├── routes.py        # TODAS las rutas en un solo blueprint ("main")
│   ├── static/
│   │   └── css/senamecf.css   # sistema de diseño institucional (compartido)
│   └── templates/       # Jinja2: base.html + una vista por módulo + editar_<modulo>.html
├── migrations/          # Alembic
├── senamecf.backup      # dump de PostgreSQL (pg_restore) versionado para el equipo
├── config.py            # clase Config (lee .env)
└── run.py               # punto de entrada
```

## Modelo de datos

Nombres de tablas y columnas en español, PK con prefijo `id_`:

- **rol** (`id_rol`, `nombre_rol`, `descripcion`)
- **empleado** (`id_empleado`, `cedula`, `nombres`, `apellidos`, `telefono`, `correo`)
- **especializacion** (`id_especializacion`, `nombre_especializacion`)
- **usuario** (`id_usuario`, `usuario`, `clave`, `estado`, FK `id_empleado`, FK `id_rol`) — `estado` es texto: "Activo"/"Inactivo"
- **especialista** — su PK **es** la FK `id_empleado` (un especialista ES un empleado); `id_especializacion` FK, `hora_inicio`, `hora_fin`, `dias_disponibles` (texto libre)
- **cita** (`id_cita`, `fecha_cita`, `hora_cita`, FK `id_empleado` = paciente, FK `id_empleado_especialista` → especialista, `estado_cita`)

## Convenciones del código (seguirlas al agregar módulos)

- **Rutas por módulo**, todas en `app/routes.py`, separadas por comentarios `#----`:
  - `GET /<modulo>/` — lista (renderiza `<modulo>.html`, que incluye el formulario de alta arriba de la tabla)
  - `POST /<modulo>/nuevo` — crear, redirect a la lista
  - `GET /<modulo>/eliminar/<int:id>` — eliminar (sí, por GET; es el patrón existente)
  - `GET|POST /<modulo>/editar/<int:id>` — renderiza `editar_<modulo>.html` / guarda y redirect
- **Autenticación**: por sesión de Flask. Las rutas de listado empiezan con `if "usuario" not in session: return redirect(url_for("main.login"))`. Login compara `usuario.clave` en texto plano y exige `estado == "Activo"`.
- **Plantillas**: extienden `base.html` (`{% block contenido %}`). Español en toda la UI.
- Nombres de variables, funciones y comentarios en **español**.

## Peculiaridades conocidas (NO "corregir" sin acordarlo con el equipo — el sistema es funcional así)

- En `models.py` se usa `_tablename_` y `_repr_` (un guion bajo, no dunder `__tablename__`/`__repr__`). SQLAlchemy los ignora y deriva el nombre de tabla del nombre de la clase en minúscula, que coincide con lo esperado — por eso funciona.
- Las claves se guardan **en texto plano** en `usuario.clave`.
- Solo las rutas GET de listado verifican sesión; los POST/editar/eliminar en su mayoría no.
- Eliminaciones por GET sin confirmación.
- `requirements.txt` está codificado en **UTF-16** (generado con `pip freeze` en PowerShell). `pip install -r` lo maneja, pero `grep`/`cat` lo muestran raro.
- La migración inicial (`3f3023e52404`) fue autogenerada contra una BD que ya tenía tablas: su `upgrade()` hace `drop_table` de casi todo. La BD real ya existe; ojo al correr migraciones desde cero.
- `run.py` tiene `print()` de depuración ("INICIO", url_map, etc.).

## Diseño / UI (implementado)

Rediseño visual completo con la identidad del logo, **solo estilos — sin cambios de funcionalidad**. Todo el CSS vive en `app/static/css/senamecf.css` (sistema de diseño compartido); `base.html` y `login.html` lo enlazan con `url_for('static', ...)`.

Paleta (variables CSS en `:root`):
- Azul marino `#0D2C54` / `#12355B` — dominante (barra lateral, cabeceras)
- Azul institucional `#1B4F91` — interactivo (botón primario, foco, ícono activo)
- Amarillo bandera `#FFCC00` — acento puntual (indicador de módulo activo)
- Rojo bandera `#CF142B` — solo acciones destructivas (eliminar)
- Neutros fríos: `#F5F7FA` fondo, `#FFFFFF` tarjetas, `#E3E8EF` bordes, `#16273D` texto

Estructura de UI:
- `base.html` = shell con **barra lateral fija** (marca institucional recreada en SVG + cinta tricolor, navegación con secciones e indicador activo por `request.path`) y barra superior con título/usuario/logout. Expone bloques `{% block titulo %}`, `{% block crumb %}`, `{% block encabezado %}` y `{% block contenido %}`.
- Cada módulo: tarjeta de formulario (rejilla de campos) + tarjeta de tabla con buscador en vivo.
- Componentes: `.card`, `.form`/`.field`, `.btn`, `.tbl`, `.pill` (estados), `.iact` (acciones de fila), `.stat` (dashboard), `.emp`/`.ini` (avatar con iniciales).
- **JS solo de presentación** (en `base.html`): filtro en vivo de tablas (`input.js-search` → filtra su `.card`) y `confirm()` antes de eliminar (`a.js-del`). No tocan rutas ni datos.

Regla mantenida en el rediseño: se conservaron intactos todos los `action`, `method`, `name` de formularios, URLs de enlaces y variables Jinja. Solo cambió la presentación.

## Base de datos para el equipo

`senamecf.backup` (raíz del repo) es un dump personalizado de PostgreSQL (`senamecf_db`, PG 17.8) versionado para que el equipo lo tenga al hacer pull. Restaurar con:
`createdb senamecf_db && pg_restore -d senamecf_db senamecf.backup`

## Ejecución local en esta máquina (macOS)

El README asume Windows + PostgreSQL. Para correrlo localmente aquí se usó: `venv` con Python 3.13 (Homebrew), `.env` con `SECRET_KEY` y `DATABASE_URL=sqlite:///senamecf_local.db` (no hay Postgres instalado), tablas creadas con `db.create_all()` (la migración inicial hace `drop_table` y no sirve en BD vacía). El `.db` local está en `.gitignore`. Para usar la BD real, cambiar `DATABASE_URL` a la cadena `postgresql://...`.

**Datos reales cargados en la SQLite local:** el contenido de `senamecf.backup` se importó a `senamecf_local.db` (Homebrew no funcionaba para este usuario porque `/opt/homebrew` pertenece a `alfonso`; el dump es PG17 y `pgserver`/PG16 no podían leerlo, así que se convirtió el dump a SQL con el `pg_restore` de Postgres.app PG17 y se cargó en SQLite). Credenciales reales de login: `gabriel01` / `123456` o `ManuKill` / `123456` (ambos Activos, rol Administrador). Ya no existe el usuario de prueba `admin`.

## Trabajo en curso

- Rediseño visual institucional: **hecho** en todos los módulos y el login (pendiente solo de revisión visual de Geremy y de incrustar el archivo real del logo si se prefiere sobre la marca recreada en SVG).
