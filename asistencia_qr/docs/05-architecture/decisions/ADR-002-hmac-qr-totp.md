# ADR-002: Algoritmo Anti-Fraude con HMAC-SHA256 y Rotaci?n de 30 Segundos

> Estado: ?? Aprobado | Fecha: 2026-09-18
> Decisores: Equipo de Arquitectura y Desarrollo SENA ADSO

## Contexto
Los sistemas basados en c?digos QR est?ticos fracasan en ambientes formativos debido a que los aprendices env?an fotos instant?neas del QR a trav?s de aplicaciones de mensajer?a (WhatsApp/Telegram), permitiendo registrar asistencia a aprendices que est?n fuera de la instituci?n.

## Decisi?n
Implementar un algoritmo de c?digo de un solo uso basado en tiempo (TOTP simplificado) con firma HMAC-SHA256 truncada a 8 caracteres hexadecimales, rotado cada 30 segundos con una tolerancia m?xima de 1 per?odo ($\pm 30$s).

## Consecuencias
- **Positivas:** Imposibilita la efectividad del reenv?o de capturas de pantalla, garantizando que el aprendiz est? f?sicamente frente a la pantalla proyectada en el aula.
- **Negativas:** Requiere sincronizaci?n horaria adecuada en el servidor y una ventana de gracia para aprendices con latencia de red m?vil.
