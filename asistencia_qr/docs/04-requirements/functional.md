# Requisitos Funcionales (RF)

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

| ID | Nombre | Descripci?n | Actor | Regla Asociada |
|---|---|---|---|---|
| **RF-01** | Autenticaci?n de Usuarios | El sistema debe permitir iniciar sesi?n validando n?mero de documento y contrase?a hasheada. | Todos | RN-Identidad |
| **RF-02** | Redirecci?n por Rol | Tras un inicio de sesi?n exitoso, el sistema debe redirigir a la vista correspondiente seg?n el rol (`admin`, `instructor`, `aprendiz`). | Todos | RBAC |
| **RF-03** | Creaci?n de Sesi?n de Asistencia | El instructor debe poder seleccionar una ficha asignada y crear una sesi?n activa, registrando su IP de red. | Instructor | RN-01 |
| **RF-04** | Generaci?n de QR Criptogr?fico | El sistema debe generar y proyectar un c?digo QR firmado con HMAC-SHA256 que se renueva cada 30 segundos. | Sistema / Instructor | RN-02 |
| **RF-05** | Polling de Registros en Vivo | El sistema debe consultar y actualizar en pantalla cada 5 segundos la lista de aprendices que confirman su asistencia. | Instructor | - |
| **RF-06** | Registro de Asistencia del Aprendiz | El aprendiz debe poder registrar su asistencia mediante URL con par?metro o digitando el c?digo de sesi?n. | Aprendiz | RN-02, RN-03, RN-04, RN-05 |
| **RF-07** | Validaci?n Anti-Fraude en 5 Pasos | El sistema debe validar secuencialmente: firma HMAC vigente, sesi?n activa, proximidad de red (/24), matr?cula en ficha y no duplicidad. | Sistema | RN-02 a RN-05 |
| **RF-08** | Cierre At?mico de Sesi?n | Al cerrar la sesi?n, el sistema debe marcar como `ausente` autom?ticamente a todos los aprendices que no registraron ingreso. | Instructor / Sistema | RN-06 |
| **RF-09** | Historial Filtrado de Asistencia | El instructor debe poder filtrar asistencias por ficha, rango de fechas, aprendiz y estado. | Instructor | - |
| **RF-10** | Correcci?n Manual de Registro | El instructor debe poder cambiar el estado de asistencia (`ausente` -> `corregido`) indicando obligatoriamente una justificaci?n. | Instructor | RN-08 |
| **RF-11** | Exportaci?n a Formato Excel | El instructor debe poder descargar el historial filtrado de asistencias en formato Microsoft Excel (.xlsx). | Instructor | - |
| **RF-12** | Monitoreo de Alertas de Deserci?n | El sistema debe presentar aprendices con riesgo moderado (>10% faltas) y riesgo alto (3+ faltas seguidas). | Instructor | RN-07 |
| **RF-13** | Atenci?n de Alertas con Nota | El instructor debe poder registrar notas de seguimiento pedag?gico y cerrar una alerta activa. | Instructor | - |
| **RF-14** | Gesti?n de Fichas (Admin) | El administrador debe poder crear fichas y actualizar su estado (activa, suspendida, finalizada, archivada). | Administrador | - |
| **RF-15** | Bit?cora de Auditor?a | El sistema debe registrar cada evento de acceso, registro de asistencia o intento fallido en una tabla inmutable. | Sistema | - |
