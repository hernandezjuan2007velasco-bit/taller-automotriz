# Product Backlog Priorizado (MoSCoW)

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. Must Have (Cr?ticos e Imprescindibles ? MVP Implementado)

- **PB-01:** Autenticaci?n por documento y contrase?a con segregaci?n estricta por roles (`admin`, `instructor`, `aprendiz`).
- **PB-02:** Generaci?n y proyecci?n de c?digo QR din?mico firmado con HMAC-SHA256 con refresco autom?tico cada 30 segundos.
- **PB-03:** Registro m?vil de asistencia con validaci?n de c?digo HMAC, vigencia temporal, membres?a a la ficha y anti-duplicado.
- **PB-04:** Lista de asistentes en tiempo real en la pantalla del instructor con polling autom?tico cada 5 segundos.
- **PB-05:** Cierre de sesi?n de asistencia con inserci?n at?mica masiva de inasistencias (`ausente`) para los aprendices faltantes.
- **PB-06:** Bit?cora inmutable de auditor?a registrando acciones, IPs y resultados exitosos/fallidos.
- **PB-07:** Panel de alertas tempranas de deserci?n con c?lculo de inasistencias cr?ticas (3+ faltas seguidas).

## 2. Should Have (Importantes pero no bloqueantes del Core)

- **PB-08:** Exportaci?n de historial de asistencia consolidado a archivo Microsoft Excel (.xlsx) con filtros por ficha y fecha.
- **PB-09:** Correcci?n manual de asistencia con justificaci?n obligatoria por parte del instructor.
- **PB-10:** Modo oscuro/claro con persistencia en localStorage para ambientes de baja luminosidad.
- **PB-11:** Pool de conexiones MySQL con soporte TLS para cl?steres serverless de alta disponibilidad.

## 3. Could Have (Deseables para siguientes versiones)

- **PB-12:** Esc?ner integrado con c?mara web mediante API WebRTC dentro de la propia interfaz web.
- **PB-13:** Exportaci?n del reporte de asistencia y del historial del aprendiz en formato PDF institucional.
- **PB-14:** Notificaciones push en navegador para advertir al aprendiz de faltas acumuladas.

## 4. Won't Have (Descartados para esta entrega)

- **PB-15:** Integraci?n directa con las APIs propietarias de SOFIA Plus.
- **PB-16:** Reconocimiento biom?trico facial.
