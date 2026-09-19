# Requisitos No Funcionales (RNF)

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. Seguridad (RNF-SEC)
- **RNF-SEC-01 (Cifrado en Tr?nsito):** Todas las comunicaciones entre la aplicaci?n y el cl?ster de base de datos TiDB Cloud deben operar obligatoriamente sobre TLS 1.2+ con verificaci?n de certificados CA (`certifi`).
- **RNF-SEC-02 (Almacenamiento de Contrase?as):** Las contrase?as deben ser sometidas a funciones de derivaci?n criptogr?fica con salting usando el algoritmo `scrypt` provisto por `werkzeug.security`.
- **RNF-SEC-03 (Seguridad en Sesiones):** Las cookies de sesi?n deben tener configurados los atributos `HttpOnly = True` y `SameSite = 'Lax'` para prevenir ataques XSS y CSRF.
- **RNF-SEC-04 (Protecci?n contra Inyecci?n SQL):** El 100% de las consultas a la base de datos deben ser preparadas con par?metros tipados (`%s`).

## 2. Rendimiento y Escalabilidad (RNF-PERF)
- **RNF-PERF-01 (Tiempo de Respuesta en Escaneo):** El endpoint `/aprendiz/confirmar` debe procesar y responder la solicitud de confirmaci?n en menos de 500 milisegundos bajo condiciones normales de red.
- **RNF-PERF-02 (Pool de Conexiones):** El backend debe reutilizar conexiones mediante `MySQLConnectionPool` para absorber r?fagas simult?neas de escaneo de 35 aprendices en un aula sin sobrecargar sockets TLS.

## 3. Disponibilidad y Concurrencia (RNF-DISP)
- **RNF-DISP-01:** La arquitectura debe operar de forma serverless en la capa de datos (TiDB Cloud) y mediante servidor WSGI escalable (Gunicorn en Linux o multihilo local).

## 4. Usabilidad y Dise?o (RNF-USA)
- **RNF-USA-01 (Dise?o Responsivo):** La vista del aprendiz debe adaptarse perfectamente a pantallas de dispositivos m?viles (resoluciones desde 320px de ancho).
- **RNF-USA-02 (Identidad Institucional):** La interfaz gr?fica debe reflejar la paleta de colores y tipograf?as oficiales del SENA (verde `#39A900`, fondos neutros y tipograf?a Inter/Manrope).
