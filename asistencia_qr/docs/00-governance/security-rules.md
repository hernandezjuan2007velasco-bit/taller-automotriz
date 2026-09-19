# Reglas de Seguridad Documental y de C?digo

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. Prohibici?n de Secretos en el Repositorio

- **Archivos `.env` y `.env.local`:** Nunca deben subirse a sistemas de control de versiones. Est?n expresamente ignorados en `.gitignore`.
- **Certificados y Claves Criptogr?ficas:** Certificados CA (`*.pem`), claves privadas SSL y secretos HMAC deben inyectarse mediante variables de entorno en el servidor de despliegue.
- **Scripts de Prueba:** Ning?n script de test o migraci?n (`test_*.py`, `check_db.py`, `init_db.py`) debe contener credenciales quemadas en texto plano; todos deben consumir la clase centralizada `Config`.

## 2. Manejo de Credenciales y Base de Datos

- La conexi?n a TiDB Cloud Serverless exige obligatoriamente cifrado en tr?nsito TLS (`ssl_verify_cert=True`, `ssl_ca=certifi.where()`).
- Las contrase?as de usuarios en base de datos deben ser almacenadas exclusivamente con algoritmos de derivaci?n de claves seguros como `scrypt` o `pbkdf2:sha256` mediante `werkzeug.security`.

## 3. Medidas de Seguridad Web Implementadas

- `SESSION_COOKIE_HTTPONLY = True`: Previene el robo de cookies de sesi?n v?a ataques Cross-Site Scripting (XSS).
- `SESSION_COOKIE_SAMESITE = 'Lax'`: Mitiga ataques de Cross-Site Request Forgery (CSRF).
- Consultas SQL 100% parametrizadas con placeholders `%s`: Erradicaci?n de inyecciones SQL (SQLi).
