# Entidades del Dominio y Reglas de Negocio

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. Entidades Principales

### 1.1 Usuario
Representa a cualquier actor autenticado en el sistema.
- **Atributos:** Identificador, Nombre completo, Documento de identidad (?nico), Rol (`admin`, `instructor`, `aprendiz`), Centro de formaci?n, Estado (`activo`, `desactivado`).

### 1.2 Ficha de Caracterizaci?n
Agrupa a los aprendices bajo un programa acad?mico y un instructor l?der.
- **Atributos:** N?mero de ficha (?nico), Programa formativo, Sede, Instructor responsable, Estado (`activa`, `suspendida`, `finalizada`, `archivada`), Fecha de apertura, Fecha de cierre.

### 1.3 Sesi?n de Asistencia
Instancia temporal de una clase presencial donde se habilita el registro de asistencia.
- **Atributos:** Ficha asociada, Instructor responsable, IP de origen del instructor, Fecha, Hora de inicio, Hora de fin, C?digo QR actual, Timestamp del c?digo, Estado (`activa`, `cerrada`).

### 1.4 Asistencia
Registro individual que certifica la presencia o ausencia de un aprendiz en una sesi?n.
- **Atributos:** Sesi?n, Aprendiz, Hora de registro, IP del dispositivo, Estado (`presente`, `ausente`, `corregido`), Motivo de correcci?n.

### 1.5 Alerta de Deserci?n
Notificaci?n proactiva sobre aprendices en riesgo acad?mico o deserci?n inminente.
- **Atributos:** Aprendiz, Ficha, Tipo (`riesgo_alto`, `riesgo_moderado`), Descripci?n, Porcentaje de riesgo (0-100), Estado (`activa`, `atendida`), Nota de seguimiento.

---

## 2. Invariantes y Reglas de Negocio (RN)

- **RN-01 (Unicidad de Sesi?n Activa por Instructor):** Un instructor solo puede tener una sesi?n en estado `activa` a la vez. Debe cerrar la sesi?n vigente antes de abrir una nueva.
- **RN-02 (Ventana de Rotaci?n QR):** El c?digo QR caduca cada 30 segundos. Su validez se calcula mediante la f?rmula:
  $$\text{periodo} = \lfloor \text{timestamp} / 30 \rfloor$$
  Se admite una tolerancia m?xima de $\pm 1$ per?odo (ventana efectiva de hasta 60 segundos) para compensar desfases de red leves.
- **RN-03 (Anti-Duplicidad Estricta):** Un aprendiz solo puede registrar asistencia una ?nica vez por sesi?n. Todo intento subsiguiente es rechazado y registrado como duplicado.
- **RN-04 (Membres?a Obligatoria):** Un aprendiz solo puede registrar asistencia en sesiones pertenecientes a una ficha en la que est? formalmente matriculado.
- **RN-05 (Validaci?n de Proximidad por Red):** Si la validaci?n de red est? habilitada (`VALIDAR_RED = True`), la IP de origen del aprendiz debe coincidir en su segmento de subred (/24) con la IP del instructor que abri? la sesi?n.
- **RN-06 (Cierre y Asignaci?n Autom?tica de Ausencias):** Al pasar una sesi?n de estado `activa` a `cerrada`, el sistema inserta autom?ticamente registros de estado `ausente` para todos los aprendices matriculados que no registraron ingreso.
- **RN-07 (Criterio de Alerta de Deserci?n):**
  - **Riesgo Moderado:** Inasistencia superior al 10% del total de sesiones de la ficha.
  - **Riesgo Alto:** Acumulaci?n de 3 o m?s inasistencias consecutivas sin justificar.
- **RN-08 (Auditor?a de Correcciones Manuales):** Toda alteraci?n manual del estado de asistencia (`ausente` $\rightarrow$ `corregido`) exige registrar obligatoriamente una justificaci?n textual y queda sellada en la bit?cora de auditor?a.
