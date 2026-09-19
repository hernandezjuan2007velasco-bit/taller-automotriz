# ADR-001: Adopci?n de Microframework Flask con Blueprints Modulares

> Estado: ?? Aprobado | Fecha: 2026-09-18
> Decisores: Equipo de Arquitectura y Desarrollo SENA ADSO

## Contexto
El sistema de asistencia requiere ser ligero, r?pido de iniciar en entornos locales de aula, compatible con empaquetado en contenedores y f?cilmente entendible con prop?sitos formativos en el SENA.

## Decisi?n
Se seleccion? **Flask 3.1** organizando la aplicaci?n mediante la f?brica `crear_app()` y dividiendo las responsabilidades funcionales en Blueprints independientes (`auth`, `instructor`, `aprendiz`, `admin`), acoplados con plantillas Jinja2 y hojas de estilo desacopladas.

## Consecuencias
- **Positivas:** Bajo consumo de recursos de memoria (<60MB en ejecuci?n), inicio instant?neo, estructura modular limpia sin la sobrecarga de un framework monol?tico pesado.
- **Negativas:** Se deben gestionar manualmente aspectos que otros frameworks resuelven por convenci?n (como formularios y migraciones).
