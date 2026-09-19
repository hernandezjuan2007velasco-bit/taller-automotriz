# Glosario T?cnico y de Negocio

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. T?rminos del Dominio SENA

- **Aprendiz:** Persona matriculada en un programa de formaci?n t?cnica, tecnol?gica o complementaria del SENA.
- **Instructor:** Profesional encargado de orientar y facilitar los procesos de aprendizaje en el ambiente de formaci?n.
- **Ficha de Caracterizaci?n (Ficha):** Identificador num?rico ?nico asignado a un grupo de aprendices matriculados en un programa de formaci?n y sede espec?fica (ej: Ficha 2830145).
- **Ambiente de Aprendizaje:** Espacio f?sico o taller del SENA donde se desarrollan las actividades presenciales de formaci?n.
- **Deserci?n:** Condici?n reglamentaria producida cuando el aprendiz acumula inasistencias continuas injustificadas (t?picamente 3 d?as continuos) o discontinuas, conllevando al inicio de tr?mite de cancelaci?n de matr?cula.
- **Etapa Lectiva:** Per?odo de formaci?n acad?mica te?rica y pr?ctica en el centro de formaci?n.

## 2. T?rminos T?cnicos y de Arquitectura

- **HMAC (Hash-based Message Authentication Code):** Mecanismo de autenticaci?n criptogr?fica de mensajes que combina una funci?n hash criptogr?fica (SHA-256) con una clave secreta compartida.
- **TOTP (Time-based One-Time Password):** Algoritmo que genera contrase?as de un solo uso basadas en la fecha y hora actual dividida en intervalos fijos de tiempo (en este sistema, per?odos de 30 segundos).
- **Subred IP (/24):** Segmento de red local donde los primeros 24 bits de la direcci?n IP corresponden a la red (ej: `192.168.1.0/24`), utilizado para asegurar que dos dispositivos pertenecen al mismo segmento f?sico o Wi-Fi.
- **TiDB Cloud:** Sistema de gesti?n de bases de datos relacionales distribuido, serverless y compatible con el protocolo MySQL.
- **RBAC (Role-Based Access Control):** Modelo de control de acceso que restringe los privilegios de un usuario en el sistema en funci?n de su rol asignado (`admin`, `instructor`, `aprendiz`).
- **Connection Pool:** Conjunto de conexiones preestablecidas a la base de datos que se reutilizan entre solicitudes HTTP para evitar el costo de establecimiento de sockets TLS.
