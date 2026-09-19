# Aspectos Transversales de Arquitectura

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. Algoritmo Criptogr?fico Anti-Fraude (HMAC-SHA256 TOTP)
Para evitar que un aprendiz comparta una captura de pantalla del c?digo QR con personas ausentes:
1. El servidor divide el tiempo Unix en per?odos de 30 segundos: $\text{periodo} = \lfloor \text{time}() / 30 \rfloor$.
2. Concatena el identificador de sesi?n y el per?odo: $\text{mensaje} = \text{sesion\_id} - \text{periodo}$.
3. Firma con clave secreta: $\text{firma} = \text{HMAC-SHA256}(\text{mensaje}, \text{secreto})[:8]$.
4. El formato emitido es: `{sesion_id}-{periodo}-{firma}` (ej: `3-59124012-A8C2B10F`).
5. Al verificar, se admite como m?ximo una desviaci?n de $\pm 1$ per?odo (ventana efectiva de hasta 60 segundos), invalidando tokens m?s antiguos.

## 2. Validaci?n de Proximidad F?sica por Subred IP
Si la directiva `VALIDAR_RED` est? activa:
- El servidor extrae la IP real del aprendiz mediante `obtener_ip_real()` (inspeccionando cabeceras `X-Forwarded-For` o `remote_addr`).
- Compara la IP del aprendiz contra la IP del instructor capturada al abrir la sesi?n usando la m?scara configurada (`/24`), asegurando que ambos se encuentren dentro del mismo segmento local de red.

## 3. Conexiones Optimizadas y Transaccionalidad At?mica
- **Pool de Conexiones:** Se implementa `MySQLConnectionPool` en `models/db.py` con tama?o de 5 conexiones persistentes, evitando el overhead de handshakes TLS en cada escaneo concurrente.
- **Transaccionalidad At?mica:** En `models/sesion.py:cerrar`, la inserci?n de inasistencias para todos los aprendices no registrados y la actualizaci?n del estado de sesi?n se ejecutan dentro de una ?nica transacci?n SQL (`BEGIN ... COMMIT`) con `ROLLBACK` autom?tico ante cualquier fallo.

## 4. Trazabilidad y Auditor?a Forense
Toda operaci?n sensible (`SESION_CREADA`, `ASISTENCIA_REGISTRADA`, `INTENTO_REGISTRO_FALLIDO`, `CORRECCION_ASISTENCIA`, `CONFIG_ACTUALIZADA`) escribe de forma s?ncrona en la tabla `auditoria` guardando la marca de tiempo, usuario, IP, tipo de acci?n y resultado.
