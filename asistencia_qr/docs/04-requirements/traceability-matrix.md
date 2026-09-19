# Matriz de Trazabilidad de Requisitos

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

Esta matriz vincula los Requisitos Funcionales (RF), Historias de Usuario (HU), Controladores/Modelos implementados y las Pruebas de Verificaci?n:

| ID Requisito | Historia de Usuario | Controlador / M?dulo | Modelo de Datos | Archivo de Prueba / Verificaci?n |
|---|---|---|---|---|
| **RF-01** (Autenticaci?n) | HU-Auth | `controllers/auth_controller.py` | `models/usuario.py` | `test_db.py`, `models/usuario.py:autenticar` |
| **RF-02** (Redirecci?n RBAC) | HU-Auth | `controllers/auth_controller.py` | `models/usuario.py` | `app.py:index` |
| **RF-03** (Crear Sesi?n) | HU-01 | `controllers/instructor_controller.py` | `models/sesion.py` | `instructor/sesion.html` |
| **RF-04** (QR Din?mico HMAC) | HU-01 | `controllers/seguridad.py` | `models/sesion.py` | `test_templates.py`, API `/instructor/sesion/qr` |
| **RF-05** (Polling en Vivo) | HU-01 | `controllers/instructor_controller.py` | `models/asistencia.py` | API `/instructor/sesion/registros` |
| **RF-06** (Registro Aprendiz) | HU-02 | `controllers/aprendiz_controller.py` | `models/asistencia.py` | `aprendiz/escanear.html` |
| **RF-07** (Validaci?n 5 Pasos) | HU-02 | `controllers/seguridad.py` | `models/asistencia.py` | `controllers/aprendiz_controller.py:confirmar` |
| **RF-08** (Cierre At?mico) | HU-03 | `controllers/instructor_controller.py` | `models/sesion.py` | `models/sesion.py:cerrar` |
| **RF-09** (Historial Filtrado) | HU-Reportes | `controllers/instructor_controller.py` | `models/asistencia.py` | `instructor/historial.html` |
| **RF-10** (Correcci?n Manual) | HU-Correcci?n | `controllers/instructor_controller.py` | `models/asistencia.py` | `models/asistencia.py:corregir` |
| **RF-11** (Exportar Excel) | HU-Reportes | `controllers/instructor_controller.py` | `openpyxl` | Endpoint `/instructor/historial/exportar` |
| **RF-12** (Alertas Deserci?n) | HU-04 | `controllers/instructor_controller.py` | `models/alerta.py` | `instructor/alertas.html` |
| **RF-13** (Atender Alerta) | HU-04 | `controllers/instructor_controller.py` | `models/alerta.py` | `models/alerta.py:atender` |
| **RF-14** (Gesti?n Fichas) | HU-Admin | `controllers/admin_controller.py` | `models/ficha.py` | `admin/panel.html` |
| **RF-15** (Auditor?a Forense) | Transversal | `controllers/seguridad.py` | `models/auditoria.py` | `models/auditoria.py:registrar` |
