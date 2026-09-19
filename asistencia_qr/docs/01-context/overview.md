# Justificaci?n, Problem?tica y Objetivos

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. Contexto Institucional

El **Servicio Nacional de Aprendizaje (SENA)**, Regional Huila, imparte formaci?n profesional integral a trav?s de programas t?cnicos y tecn?logos estructurados por fichas de caracterizaci?n. El seguimiento puntual y veraz de la asistencia presencial de los aprendices es un elemento regulatorio cr?tico: determina el cumplimiento de la etapa lectiva, el derecho a apoyos de sostenimiento y la detecci?n oportuna de causales de deserci?n o cancelaci?n de matr?cula seg?n el Reglamento del Aprendiz SENA.

## 2. Declaraci?n del Problema

Los m?todos tradicionales de control de asistencia presencial presentan serias deficiencias operativas y de seguridad:

1. **Llamado a lista verbal / Planillas de papel:** Consume entre 10 y 15 minutos por sesi?n de formaci?n, es susceptible a suplantaci?n y la informaci?n f?sica se dispersa, dificultando consolidaciones estad?sticas.
2. **C?digos QR Est?ticos o Formularios Web Abiertos:** Los aprendices suelen tomar fotograf?as a los c?digos est?ticos o reenviar enlaces por mensajer?a instant?nea (WhatsApp, Telegram) a compa?eros ausentes, quienes registran su presencia desde fuera del centro de formaci?n.
3. **Deserci?n Silenciosa:** Los instructores carecen de tableros de advertencia temprana automatizados que consoliden inasistencias consecutivas, impidiendo activar oportunamente los comit?s de seguimiento y planes de rescate pedag?gico.

## 3. Objetivos del Proyecto

### 3.1 Objetivo General
Desarrollar e implementar un sistema web seguro y automatizado para el registro de asistencia presencial en ambientes de formaci?n del SENA mediante c?digos QR din?micos con firma criptogr?fica HMAC y detecci?n temprana de deserci?n.

### 3.2 Objetivos Espec?ficos
1. Dise?ar un mecanismo anti-fraude basado en rotaci?n temporal de c?digos QR (TOTP/HMAC) cada 30 segundos, impidiendo el uso de capturas de pantalla compartidas.
2. Implementar geocercado l?gico mediante validaci?n de subred IP local para exigir presencia f?sica en el ambiente de aprendizaje.
3. Automatizar el cierre de sesiones con asignaci?n masiva de estados de inasistencia para los aprendices que no registraron ingreso.
4. Proveer paneles de control anal?ticos diferenciados por rol (Administrador, Instructor y Aprendiz) con m?tricas de rendimiento y alertas de deserci?n.
5. Garantizar la trazabilidad y la no repudio de todas las operaciones a trav?s de un registro de auditor?a forense inmutable.
