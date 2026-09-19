# Documentaci?n T?cnica del Sistema: Asistencia QR (SENA)

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Programa: An?lisis y Desarrollo de Software (ADSO) ? Regional Huila

Bienvenido al repositorio documental central del proyecto **Asistencia QR**, desarrollado bajo los lineamientos y est?ndares de calidad de ingenier?a de software del SENA.

---

## Estructura y Navegaci?n de la Documentaci?n

La documentaci?n est? organizada tem?ticamente desde la carpeta `00` hasta la `06`:

| Secci?n | Nombre | Descripci?n del Contenido | Estado |
|---|---|---|---|
| [00-governance](./00-governance/) | **Gobierno y Convenciones** | Reglas de nombrado, GitFlow, normas de seguridad y criterios de entrada/salida (DoR/DoD). | ?? Estable |
| [01-context](./01-context/) | **Contexto Institucional** | Justificaci?n institucional SENA, problem?tica de la asistencia, alcance y glosario. | ?? Estable |
| [02-domain](./02-domain/) | **Modelo de Dominio** | Mapa de contextos delimitados, entidades clave, reglas de negocio e invariantes, y eventos. | ?? Estable |
| [03-product](./03-product/) | **Visi?n y Producto** | Declaraci?n de visi?n, propuesta de valor, roadmap por fases y product backlog MoSCoW. | ?? Estable |
| [04-requirements](./04-requirements/) | **Requisitos del Sistema** | Requisitos funcionales (RF), no funcionales (RNF), historias de usuario y matriz de trazabilidad. | ?? Estable |
| [05-architecture](./05-architecture/) | **Arquitectura y ADRs** | Diagramas C4 (Contexto/Contenedores/Componentes), topolog?a f?sica, aspectos transversales y ADRs. | ?? Estable |
| [06-data](./06-data/) | **Capa de Datos** | Modelo Entidad-Relaci?n (Mermaid ER), diccionario de las 8 tablas y estrategia de migraci?n. | ?? Estable |

---

## Acceso R?pido a Documentos Cr?ticos

- [Reglas de Seguridad y Manejo de Secretos](./00-governance/security-rules.md)
- [Reglas de Negocio Anti-Fraude](./02-domain/entities-and-rules.md)
- [Historias de Usuario con Sintaxis Gherkin](./04-requirements/user-stories.md)
- [Vista de Arquitectura y Componentes](./05-architecture/overview.md)
- [Diccionario Exhaustivo de Base de Datos](./06-data/data-dictionary.md)
