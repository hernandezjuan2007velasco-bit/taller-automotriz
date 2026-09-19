# Diccionario de Datos

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

---

### 1. Tabla: `usuarios`
Almacena las cuentas de acceso de todos los usuarios del sistema.

| Columna | Tipo de Dato | Nulo | Clave | Valor por Defecto | Descripci?n |
|---|---|---|---|---|---|
| `id` | INT | NO | PK | AUTO_INCREMENT | Identificador ?nico del usuario |
| `nombre` | VARCHAR(100) | NO | | | Nombres y apellidos completos |
| `documento` | VARCHAR(20) | NO | UK | | N?mero de documento de identidad (c?dula o TI) |
| `password_hash`| VARCHAR(255) | NO | | | Hash criptogr?fico de la contrase?a (scrypt) |
| `rol` | ENUM | NO | | | Rol de acceso: `'instructor'`, `'admin'`, `'aprendiz'` |
| `centro` | VARCHAR(100) | NO | | | Centro de formaci?n SENA (ej: 'Neiva') |
| `estado` | ENUM | S? | | `'activo'` | Estado de la cuenta: `'activo'`, `'desactivado'` |
| `created_at` | TIMESTAMP | S? | | CURRENT_TIMESTAMP | Fecha y hora de creaci?n del registro |

---

### 2. Tabla: `fichas`
Estructura acad?mica de los grupos de aprendices.

| Columna | Tipo de Dato | Nulo | Clave | Valor por Defecto | Descripci?n |
|---|---|---|---|---|---|
| `id` | INT | NO | PK | AUTO_INCREMENT | Identificador ?nico de la ficha |
| `numero` | VARCHAR(20) | NO | UK | | C?digo num?rico oficial de la ficha (ej: 2830145) |
| `programa` | VARCHAR(150) | NO | | | Nombre del programa de formaci?n profesional |
| `sede` | VARCHAR(100) | NO | | | Sede o subsede de formaci?n |
| `instructor_id`| INT | NO | FK | | ID del instructor l?der de la ficha (`usuarios.id`) |
| `estado` | ENUM | S? | | `'activa'` | `'activa'`, `'suspendida'`, `'finalizada'`, `'archivada'` |
| `fecha_apertura`| DATE | S? | | | Fecha en que inicia la etapa lectiva |
| `fecha_cierre` | DATE | S? | | | Fecha de finalizaci?n o cierre |

---

### 3. Tabla: `ficha_aprendiz`
Tabla asociativa de relaci?n muchos a muchos entre fichas y aprendices.

| Columna | Tipo de Dato | Nulo | Clave | Valor por Defecto | Descripci?n |
|---|---|---|---|---|---|
| `ficha_id` | INT | NO | PK, FK | | Referencia a `fichas.id` |
| `aprendiz_id` | INT | NO | PK, FK | | Referencia a `usuarios.id` |

---

### 4. Tabla: `sesiones`
Representa cada jornada de clase presencial donde se habilita el llamado a lista con QR.

| Columna | Tipo de Dato | Nulo | Clave | Valor por Defecto | Descripci?n |
|---|---|---|---|---|---|
| `id` | INT | NO | PK | AUTO_INCREMENT | Identificador ?nico de la sesi?n |
| `ficha_id` | INT | NO | FK | | Ficha a la que pertenece la clase |
| `instructor_id`| INT | NO | FK | | Instructor que abri? la sesi?n |
| `codigo_actual`| VARCHAR(100) | S? | | | C?digo HMAC vigente proyectado en el aula |
| `codigo_timestamp`| INT | S? | | | Epoch timestamp de generaci?n del c?digo actual |
| `ip_instructor`| VARCHAR(45) | NO | | | IP de origen del instructor para validaci?n de red |
| `fecha` | DATE | NO | | | Fecha de la sesi?n (AAAA-MM-DD) |
| `hora_inicio` | TIME | NO | | | Hora de apertura de la sesi?n |
| `hora_fin` | TIME | S? | | | Hora de cierre de la sesi?n |
| `estado` | ENUM | S? | | `'activa'` | Estado de la sesi?n: `'activa'`, `'cerrada'` |
| `created_at` | TIMESTAMP | S? | | CURRENT_TIMESTAMP | Momento de creaci?n en BD |

---

### 5. Tabla: `asistencias`
Registro del estado de presencia de cada aprendiz por sesi?n.

| Columna | Tipo de Dato | Nulo | Clave | Valor por Defecto | Descripci?n |
|---|---|---|---|---|---|
| `id` | INT | NO | PK | AUTO_INCREMENT | Identificador del registro de asistencia |
| `sesion_id` | INT | NO | FK, UK | | Sesi?n a la que corresponde el registro |
| `aprendiz_id` | INT | NO | FK, UK | | Aprendiz vinculado |
| `hora_registro`| TIME | S? | | | Hora exacta en la que el aprendiz confirm? asistencia |
| `ip_registro` | VARCHAR(45) | S? | | | Direcci?n IP desde la cual se confirm? |
| `estado` | ENUM | S? | | `'presente'` | `'presente'`, `'ausente'`, `'corregido'` |
| `motivo_correccion`| TEXT | S? | | | Justificaci?n escrita obligatoria si fue corregido |
| `created_at` | TIMESTAMP | S? | | CURRENT_TIMESTAMP | Fecha de creaci?n del registro |

*Restricci?n:* `UNIQUE KEY unique_sesion_aprendiz (sesion_id, aprendiz_id)`.

---

### 6. Tabla: `alertas`
Detecci?n preventiva de aprendices con inasistencias reiteradas.

| Columna | Tipo de Dato | Nulo | Clave | Valor por Defecto | Descripci?n |
|---|---|---|---|---|---|
| `id` | INT | NO | PK | AUTO_INCREMENT | Identificador ?nico de la alerta |
| `aprendiz_id` | INT | NO | FK | | Aprendiz en situaci?n de riesgo |
| `ficha_id` | INT | NO | FK | | Ficha del aprendiz |
| `tipo` | ENUM | NO | | | `'riesgo_alto'`, `'riesgo_moderado'` |
| `descripcion` | TEXT | NO | | | Raz?n del riesgo (ej: 'Inasistencia consecutiva cr?tica') |
| `porcentaje_riesgo`| INT | NO | | | Grado de riesgo calculado de 0 a 100 |
| `estado` | ENUM | S? | | `'activa'` | `'activa'`, `'atendida'` |
| `nota_seguimiento`| TEXT | S? | | | Anotaciones pedag?gicas registradas por el instructor |
| `created_at` | TIMESTAMP | S? | | CURRENT_TIMESTAMP | Momento de generaci?n |

---

### 7. Tabla: `auditoria`
Bit?cora de seguridad y cumplimiento normativo.

| Columna | Tipo de Dato | Nulo | Clave | Valor por Defecto | Descripci?n |
|---|---|---|---|---|---|
| `id` | INT | NO | PK | AUTO_INCREMENT | Identificador del evento auditado |
| `usuario_id` | INT | S? | FK | | Usuario que ejecut? la acci?n (o NULL si an?nimo) |
| `ip_origen` | VARCHAR(45) | NO | | | IP de origen del cliente |
| `accion` | VARCHAR(100) | NO | | | C?digo de acci?n (`SESION_CREADA`, `LOGIN`, etc.) |
| `resultado` | ENUM | NO | | | `'exitoso'`, `'fallido'` |
| `detalle` | TEXT | S? | | | Informaci?n complementaria del evento |
| `created_at` | TIMESTAMP | S? | | CURRENT_TIMESTAMP | Marca temporal inmutable del suceso |

---

### 8. Tabla: `configuracion`
Par?metros din?micos del sistema editables desde el panel de administraci?n.

| Columna | Tipo de Dato | Nulo | Clave | Valor por Defecto | Descripci?n |
|---|---|---|---|---|---|
| `clave` | VARCHAR(50) | NO | PK | | Identificador del par?metro (`qr_rotacion_segundos`, etc.) |
| `valor` | VARCHAR(255) | NO | | | Valor asignado |
| `descripcion` | TEXT | S? | | | Explicaci?n para los administradores |
