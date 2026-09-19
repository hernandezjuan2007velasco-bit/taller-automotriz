# Capa de Datos y Persistencia

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## Contenido

Documenta el modelo relacional f?sico, diagrama Entidad-Relaci?n (ER), diccionario de datos completo de las 8 tablas y la estrategia de versionado y migraci?n de esquemas.

> **Diferencia con `02-domain`:** Esta secci?n describe la implementaci?n concreta de persistencia en la base de datos (tablas, columnas, claves for?neas, ?ndices y restricciones). La sem?ntica de negocio y las reglas invariantes se describen en [`02-domain/`](../02-domain/).

## Archivos

| Archivo | Descripci?n | Estado |
|---|---|---|
| [models.md](./models.md) | Diagrama Entidad-Relaci?n (ER en Mermaid) y arquitectura relacional f?sica | ?? Estable |
| [data-dictionary.md](./data-dictionary.md) | Diccionario de datos exhaustivo de las 8 tablas del sistema | ?? Estable |
| [migration-strategy.md](./migration-strategy.md) | Estrategia de inicializaci?n de esquemas, migraciones y datos semilla (seeds) | ?? Estable |
