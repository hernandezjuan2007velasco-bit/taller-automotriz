# Estrategia de Migraciones y Gesti?n de Esquemas

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. Estructura de Scripts DDL y DML

El proyecto gestiona su ciclo de persistencia a trav?s de scripts SQL versionados en la carpeta `database/`:

1. **`database/schema.sql`:** Contiene todas las sentencias DDL idempotentes (`CREATE TABLE IF NOT EXISTS`) con claves for?neas, restricciones de unicidad e ?ndices para las 8 tablas.
2. **`database/seeds.sql`:** Inserta usuarios de prueba precargados (Admin, Instructores, Aprendices), fichas modelo y alertas representativas.
3. **`init_db.py`:** Script Python automatizado que establece conexi?n segura mediante TLS con TiDB Cloud y aplica secuencialmente `schema.sql` y `seeds.sql`.
4. **`migrate_fichas.py`:** Script de migraci?n incremental que a?ade campos de estado y ciclo de vida a la tabla `fichas` de forma segura.

## 2. Procedimiento de Inicializaci?n en un Nuevo Entorno

```bash
# 1. Configurar variables de entorno en el archivo .env
MYSQL_HOST=gateway01.us-east-1.prod.aws.tidbcloud.com
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_contrase?a
MYSQL_DB=asistencia_qr

# 2. Ejecutar inicializaci?n de tablas y datos semilla
python init_db.py

# 3. Validar estado de la conexi?n
python test_db.py
```
