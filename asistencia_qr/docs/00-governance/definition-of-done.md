# Definition of Done (DoD)

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

Una funcionalidad se considera **Terminada (Done)** y lista para despliegue cuando satisface rigurosamente los siguientes ?tems:

1. **C?digo Funcional:** El c?digo ejecuta correctamente en entorno local y de pruebas sin lanzar excepciones no controladas.
2. **Consultas Parametrizadas:** Toda interacci?n con TiDB/MySQL utiliza consultas preparadas libres de vulnerabilidades SQLi.
3. **Auditor?a Activa:** La acci?n registra su respectivo evento (exitoso o fallido) en la tabla `auditoria`.
4. **Pruebas de Plantilla:** La vista asociada renderiza sin fallos mediante el suite de validaci?n `test_templates.py`.
5. **Revisi?n de Seguridad:** El c?digo est? libre de credenciales, tokens o IPs privadas quemadas en c?digo fuente.
6. **Documentaci?n Actualizada:** Se documentan los requisitos asociados, eventos de dominio y diccionarios de datos en la carpeta `docs/`.
