# Topolog?a de Despliegue

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

El sistema est? dise?ado para operar tanto en un entorno de desarrollo local como en una infraestructura en la nube moderna de bajo costo (PaaS + Serverless DB):

```mermaid
graph LR
    subgraph Clientes ["Dispositivos de Usuario"]
        PC["PC de Instructor<br/>(Proyector del Aula)"]
        Movil["Smartphones de Aprendices<br/>(Wi-Fi SENA)"]
    end

    subgraph PaaS ["PaaS - Servidor de Aplicaciones (Render / Cloud)"]
        Gunicorn["Gunicorn WSGI Server<br/>(22.0.0, 2-4 Workers)"]
        Flask["Flask App (Python 3.11+)<br/>asistencia_qr"]
    end

    subgraph DBaaS ["DBaaS - Base de Datos Distribuida (TiDB Cloud)"]
        TiDBGateway["Gateway TLS (Port 4000)<br/>gateway01.us-east-1.prod.aws.tidbcloud.com"]
        Storage["Storage Serverless Autoescalable"]
    end

    PC -->|HTTPS / TLS| Gunicorn
    Movil -->|HTTPS / TLS| Gunicorn
    Gunicorn --> Flask
    Flask -->|TLS 1.2+ con Certifi CA| TiDBGateway
    TiDBGateway --> Storage
```

### Ambientes:

| Ambiente | Host de Aplicaci?n | Base de Datos | Configuraci?n SSL |
|---|---|---|---|
| **Desarrollo Local** | `localhost:5000` (Flask Dev Server) | TiDB Cloud / MySQL Local | `ssl_verify_cert=True`, `certifi` |
| **Producci?n (Render)** | Web Service en Render con Gunicorn | TiDB Cloud Serverless | Forzar HTTPS, `SESSION_COOKIE_SECURE=True` |
