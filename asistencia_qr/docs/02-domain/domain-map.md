# Mapa de Dominio y Contextos Delimitados

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. Subdominios y Bounded Contexts

El sistema se estructura en 5 contextos delimitados bien diferenciados:

```mermaid
graph TD
    subgraph Core ["Subdominio Central (Core Domain)"]
        AsistenciaBC["Contexto de Asistencia & Anti-Fraude<br/>(Sesiones, QR HMAC, Verificaci?n)"]
        DesercionBC["Contexto de Alertas & Deserci?n<br/>(Detecci?n de riesgo, Seguimiento)"]
    end

    subgraph Generic ["Subdominios Gen?ricos / Soporte"]
        AuthBC["Contexto de Identidad & Acceso<br/>(Usuarios, Credenciales, RBAC)"]
        FormacionBC["Contexto de Formaci?n & Fichas<br/>(Fichas, Programas, Matr?cula)"]
        AuditoriaBC["Contexto de Auditor?a & Cumplimiento<br/>(Trazabilidad inmutable)"]
    end

    AuthBC -->|Provee identidad| AsistenciaBC
    AuthBC -->|Provee identidad| FormacionBC
    FormacionBC -->|Define grupos| AsistenciaBC
    FormacionBC -->|Define grupos| DesercionBC
    AsistenciaBC -->|Alimenta m?tricas de falta| DesercionBC
    AsistenciaBC -->|Reporta eventos| AuditoriaBC
    AuthBC -->|Reporta accesos| AuditoriaBC
```

### Descripci?n de Contextos:

1. **Contexto de Asistencia & Anti-Fraude (Core):** Responsable del ciclo de vida de la sesi?n presencial, generaci?n de c?digos ef?meros HMAC, validaci?n de proximidad de red y persistencia del estado de llegada.
2. **Contexto de Alertas & Deserci?n (Core):** Analiza el patr?n hist?rico de faltas de cada aprendiz frente a los umbrales de riesgo, notificando al instructor para intervenci?n oportuna.
3. **Contexto de Identidad & Acceso:** Gesti?n de roles (`admin`, `instructor`, `aprendiz`), autenticaci?n segura y pol?ticas de sesi?n.
4. **Contexto de Formaci?n & Fichas:** Estructuraci?n de fichas de caracterizaci?n, programas formativos y membres?a del aprendiz.
5. **Contexto de Auditor?a:** Bit?cora inmutable de eventos sensibles para garantizar transparencia y no repudio.
