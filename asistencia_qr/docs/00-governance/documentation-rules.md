# Reglas de Documentaci?n

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

Este documento establece los est?ndares de redacci?n, formato y organizaci?n para la base de conocimiento t?cnico del proyecto **Asistencia QR**.

## 1. Convenciones de Nomenclatura

- **Archivos:** Se utiliza estrictamente `kebab-case.md` en min?sculas (ej: `traceability-matrix.md`, `entities-and-rules.md`).
- **Carpetas:** Prefijo num?rico de dos d?gitos `NN-nombre` respetando el ?ndice del marco de trabajo SENA ADSO (`00-governance`, `01-context`, ..., `06-data`).
- **Registros de Decisiones de Arquitectura (ADR):** Formato `ADR-NNN-titulo-corto.md` almacenados en `05-architecture/decisions/`.

## 2. Estructura Obligatoria de Archivos Markdown

Todo documento debe comenzar con el bloque de metadatos institucional:

```markdown
# T?tulo Descriptivo

> Estado: ?? Estable | ?ltima actualizaci?n: YYYY-MM-DD
> Autor: <Nombre o Equipo> | Equipo: An?lisis y Desarrollo de Software (SENA)
```

## 3. Estados de Madurez Documental

| Estado | Significado y Criterio |
|---|---|
| ?? Pendiente | Estructura inicial creada, pendiente de desarrollo o validaci?n |
| ?? En progreso | Documento con desarrollo activo o en proceso de revisi?n por pares |
| ?? Estable | Documento revisado, aprobado y alineado con el c?digo fuente en producci?n |
| ? Deprecado | Documento hist?rico o sustituido por una versi?n posterior |

## 4. Est?ndar de Diagramas

- Se privilegia el uso de **Mermaid.js** dentro de bloques de c?digo Markdown (`mermaid`) para mantener diagramas versionables y editables en texto plano.
- Tipos de diagramas est?ndar:
  - Diagramas de Flujo y Estados: para algoritmos como rotaci?n HMAC y validaci?n de subred.
  - Diagramas Entidad-Relaci?n (`erDiagram`): para la capa de persistencia en `06-data/models.md`.
  - Diagramas C4 o Componentes: para vistas arquitect?nicas en `05-architecture/overview.md`.
