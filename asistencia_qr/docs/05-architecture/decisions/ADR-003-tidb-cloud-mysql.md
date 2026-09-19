# ADR-003: Persistencia en TiDB Cloud Serverless con Pool de Conexiones

> Estado: ?? Aprobado | Fecha: 2026-09-18
> Decisores: Equipo de Arquitectura y Desarrollo SENA ADSO

## Contexto
El proyecto requiere una base de datos relacional compatible con el dialecto MySQL que no genere costos de hosting fijos durante los per?odos intersemestrales y que soporte escalabilidad autom?tica sin administrar servidores.

## Decisi?n
Adoptar **TiDB Cloud Serverless** utilizando el conector oficial `mysql-connector-python` con cifrado TLS (`certifi`) y optimizado mediante un Pool de Conexiones (`MySQLConnectionPool`) para evitar saturaci?n de sockets durante picos de escaneo simult?neo.

## Consecuencias
- **Positivas:** Modelo 100% serverless, alta disponibilidad sin costo en el tier gratuito para el SENA, compatibilidad total con sintaxis est?ndar MySQL.
- **Negativas:** Exige TLS obligatorio y una gesti?n cuidadosa de reintentos ante desconexiones transitorias de la nube.
