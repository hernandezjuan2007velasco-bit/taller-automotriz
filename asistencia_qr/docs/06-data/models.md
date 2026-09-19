# Modelo Entidad-Relaci?n F?sico

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

El sistema opera sobre una base de datos relacional MySQL / TiDB Cloud compuesta por 8 tablas estructuradas en tercera forma normal (3NF):

```mermaid
erDiagram
    usuarios ||--o{ fichas : "lidera (instructor_id)"
    usuarios ||--o{ ficha_aprendiz : "matriculado"
    fichas ||--o{ ficha_aprendiz : "agrupa"
    fichas ||--o{ sesiones : "tiene"
    usuarios ||--o{ sesiones : "abre (instructor_id)"
    sesiones ||--o{ asistencias : "contiene"
    usuarios ||--o{ asistencias : "registra (aprendiz_id)"
    usuarios ||--o{ alertas : "alerta sobre (aprendiz_id)"
    fichas ||--o{ alertas : "asociada a"
    usuarios ||--o{ auditoria : "ejecuta (usuario_id)"
    configuracion

    usuarios {
        int id PK
        varchar nombre
        varchar documento UK
        varchar password_hash
        enum rol
        varchar centro
        enum estado
        timestamp created_at
    }

    fichas {
        int id PK
        varchar numero UK
        varchar programa
        varchar sede
        int instructor_id FK
        enum estado
        date fecha_apertura
        date fecha_cierre
    }

    ficha_aprendiz {
        int ficha_id PK_FK
        int aprendiz_id PK_FK
    }

    sesiones {
        int id PK
        int ficha_id FK
        int instructor_id FK
        varchar codigo_actual
        int codigo_timestamp
        varchar ip_instructor
        date fecha
        time hora_inicio
        time hora_fin
        enum estado
        timestamp created_at
    }

    asistencias {
        int id PK
        int sesion_id FK
        int aprendiz_id FK
        time hora_registro
        varchar ip_registro
        enum estado
        text motivo_correccion
        timestamp created_at
    }

    alertas {
        int id PK
        int aprendiz_id FK
        int ficha_id FK
        enum tipo
        text descripcion
        int porcentaje_riesgo
        enum estado
        text nota_seguimiento
        timestamp created_at
    }

    auditoria {
        int id PK
        int usuario_id FK
        varchar ip_origen
        varchar accion
        enum resultado
        text detalle
        timestamp created_at
    }

    configuracion {
        varchar clave PK
        varchar valor
        text descripcion
    }
```

## ?ndices y Restricciones Clave:
- `usuarios.documento`: Clave ?nica para evitar registros duplicados de aprendices o instructores.
- `fichas.numero`: Clave ?nica institucional.
- `asistencias.unique_sesion_aprendiz`: Restricci?n `UNIQUE KEY (sesion_id, aprendiz_id)` que garantiza a nivel de motor de base de datos la imposibilidad de dobles asistencias en la misma sesi?n.
