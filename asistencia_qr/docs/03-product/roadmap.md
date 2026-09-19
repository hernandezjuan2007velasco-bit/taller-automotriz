# Roadmap de Producto (Hoja de Ruta)

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

```mermaid
gantt
    title Roadmap de Evoluci?n - Asistencia QR
    dateFormat  YYYY-MM
    section Fase 1: MVP Funcional
    Core Asistencia QR y HMAC         :done, p1, 2026-06, 2026-07
    Base de datos TiDB Cloud          :done, p2, 2026-07, 2026-08
    Alertas y Auditor?a               :done, p3, 2026-08, 2026-09
    Correcci?n de Bugs y Estabilidad  :done, p4, 2026-09, 2026-09
    section Fase 2: Robustecimiento
    Protecci?n CSRF en Formularios    :active, p5, 2026-10, 2026-11
    Scanner con c?mara WebRTC integrado :p6, 2026-11, 2026-12
    Exportaci?n nativa a PDF          :p7, 2026-12, 2027-01
    section Fase 3: Integraci?n
    Notificaciones por Correo/WhatsApp :p8, 2027-01, 2027-02
    Integraci?n API SOFIA Plus        :p9, 2027-02, 2027-04
```

### Detalle de Hitos:

- **Hito 1 (Completado): MVP 100% Funcional**
  - Implementaci?n completa de roles (Admin, Instructor, Aprendiz).
  - Algoritmo de QR rotativo HMAC SHA-256 (30s) y vista de proyecci?n.
  - Cierre at?mico con marcaci?n masiva de ausentes.
  - Pool de conexiones a base de datos y auditor?a de eventos.
- **Hito 2 (En Progreso): Experiencia de Usuario Avanzada**
  - Incorporaci?n de lector de c?mara directo en la app web (`html5-qrcode`).
  - Generaci?n de certificados y reportes descargables en PDF.
- **Hito 3 (Futuro): Ecosistema Institucional**
  - Enlace con bases de datos de matr?cula institucional del SENA.
