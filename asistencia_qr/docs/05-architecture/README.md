# Arquitectura del Sistema

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## Contenido

Contiene las vistas arquitect?nicas de alto nivel (diagramas C4), topolog?a de despliegue f?sico y en la nube, mecanismos transversales (seguridad, auditor?a, transaccionalidad) y los Registros de Decisiones de Arquitectura (ADR).

## Archivos

| Archivo | Descripci?n | Estado |
|---|---|---|
| [overview.md](./overview.md) | Vista general de arquitectura (Diagramas C4 Contexto, Contenedor y Componentes) | ?? Estable |
| [deployment.md](./deployment.md) | Topolog?a de despliegue en Render, TiDB Cloud Serverless y entorno local | ?? Estable |
| [cross-cutting.md](./cross-cutting.md) | Mecanismos transversales: seguridad HMAC, geocercado IP, RBAC, auditor?a y pool de conexiones | ?? Estable |
| [decisions/ADR-001-flask-modular.md](./decisions/ADR-001-flask-modular.md) | ADR: Selecci?n de Flask con Blueprints modulares | ?? Estable |
| [decisions/ADR-002-hmac-qr-totp.md](./decisions/ADR-002-hmac-qr-totp.md) | ADR: Algoritmo anti-fraude basado en HMAC-SHA256 con ventana de 30 segundos | ?? Estable |
| [decisions/ADR-003-tidb-cloud-mysql.md](./decisions/ADR-003-tidb-cloud-mysql.md) | ADR: Adopci?n de TiDB Cloud Serverless y Pool de Conexiones MySQL | ?? Estable |
