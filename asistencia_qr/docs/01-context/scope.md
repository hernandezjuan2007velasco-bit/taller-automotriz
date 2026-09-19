# Alcance del Sistema, L?mites y Restricciones

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. Alcance Funcional (Inclusiones)

El sistema **Asistencia QR** contempla en su fase actual:

- **M?dulo de Autenticaci?n y Autorizaci?n (RBAC):** Login seguro con documento y contrase?a con roles: Administrador, Instructor y Aprendiz.
- **M?dulo de Generaci?n y Proyecci?n QR:** Generaci?n de c?digos QR firmados con HMAC-SHA256, actualizados en pantalla v?a AJAX cada 30 segundos y visualizaci?n en tiempo real de registros entrantes.
- **M?dulo de Registro M?vil del Aprendiz:** Captura de c?digo v?a escaneo de URL o digitaci?n manual con validaci?n secuencial en 5 pasos (HMAC, sesi?n activa, red, inscripci?n y no duplicidad).
- **M?dulo de Gesti?n de Fichas y Aprendices:** Creaci?n y actualizaci?n de estados de fichas (activa, suspendida, finalizada, archivada) y vinculaci?n de aprendices.
- **M?dulo de Reportes e Historial:** Filtros combinados por fecha, ficha, aprendiz y estado, con exportaci?n a formato Microsoft Excel (.xlsx) y correcci?n justificada de registros.
- **M?dulo de Alertas de Deserci?n:** Detecci?n algor?tmica de riesgo moderado (inasistencias acumuladas) y riesgo alto (3+ faltas seguidas) con formulario de notas de seguimiento.
- **M?dulo de Auditor?a del Sistema:** Bit?cora detallada de eventos, IPs, usuario y resultados (exitoso/fallido).

## 2. Exclusiones (Fuera de Alcance del MVP)

- Reconocimiento facial biom?trico mediante c?mara web (evaluado para fases futuras).
- Integraci?n directa por API con el sistema SOFIA Plus / Zajuna (requiere autorizaciones directas de la Direcci?n General).
- Notificaciones autom?ticas por mensajer?a SMS o WhatsApp (previsto para Fase 2).

## 3. Supuestos y Restricciones T?cnicas

- **Conectividad:** El aula de formaci?n debe disponer de conexi?n de red local (Wi-Fi o LAN cableada) donde operen tanto el equipo del instructor como los dispositivos m?viles de los aprendices.
- **Navegadores:** Compatibilidad total con navegadores modernos (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari Mobile).
- **Persistencia:** Cl?ster MySQL / TiDB Cloud con soporte obligatorio para cifrado TLS 1.2+.
