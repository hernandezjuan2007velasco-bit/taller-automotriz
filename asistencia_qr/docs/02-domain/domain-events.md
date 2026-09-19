# Cat?logo de Eventos de Dominio

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

Los eventos de dominio modelan hechos significativos que han ocurrido en el sistema:

| Evento | Origen / Disparador | Carga ?til (Payload) | Impacto en el Sistema |
|---|---|---|---|
| `SESION_CREADA` | Instructor inicia sesi?n para una ficha | `instructor_id`, `ficha_id`, `ip_instructor` | Se abre ventana de asistencia y se genera el primer token HMAC |
| `QR_ROTADO` | Temporizador de 30s en cliente/servidor | `sesion_id`, `periodo`, `codigo_hmac` | Se invalida el token anterior a los 60s de gracia |
| `ASISTENCIA_REGISTRADA` | Aprendiz env?a c?digo v?lido cumpliendo las 5 reglas | `sesion_id`, `aprendiz_id`, `ip_aprendiz`, `hora` | Se persiste registro como `presente`; se actualiza panel en vivo |
| `INTENTO_FRAUDE_DETECTADO` | Escaneo con QR expirado, red ajena o ficha err?nea | `aprendiz_id`, `ip_aprendiz`, `motivo_fallo` | Se deniega el registro y se asienta evento fallido en auditor?a |
| `SESION_CERRADA` | Instructor hace clic en "Cerrar ventana" | `sesion_id`, `hora_cierre` | Transacci?n at?mica: se asigna `ausente` a no registrados |
| `CORRECCION_ASISTENCIA` | Instructor modifica registro manual | `asistencia_id`, `nuevo_estado`, `motivo` | Estado pasa a `corregido`; se audita usuario e IP |
| `ALERTA_GENERADA` | Acumulaci?n de inasistencias por aprendiz | `aprendiz_id`, `ficha_id`, `tipo_riesgo` | Se lista en la pantalla de alertas del instructor |
| `ALERTA_ATENDIDA` | Instructor registra nota de seguimiento | `alerta_id`, `nota_seguimiento` | Se actualiza estado a `atendida` |
